import asyncio
import hashlib
import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path

import httpx

# 로그 설정 (한국어 및 상세 정보 출력)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Jina Reader API Endpoint (LLM Friendly Markdown 변환 서버)
JINA_READER_URL = "https://r.jina.ai/"

class TechDocFetcher:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.root_dir = config_path.parent.parent
        self.client = httpx.AsyncClient(
            timeout=60.0, 
            follow_redirects=True,
            headers={"User-Agent": "TechStackOrganizer/2.0 (5-Channel Engine)"}
        )

    async def fetch_content(self, url: str) -> str:
        """Jina Reader를 거쳐 마크다운 형식으로 데이터 획득"""
        if not url: return ""
        
        target_url = f"{JINA_READER_URL}{url}"
        try:
            response = await self.client.get(target_url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"  -> 수집 실패 ({url}): {e}")
            return ""

    def add_frontmatter(self, content: str, stack: dict, channel_type: str, url: str) -> str:
        """문서 상단에 메타데이터(Front-matter)를 주입"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metadata = [
            "---",
            f"tech_stack: {stack['name']}",
            f"channel: {channel_type}",
            f"source_url: {url}",
            f"last_updated: {now}",
            f"tech_version: {stack.get('version', 'latest')}",
            "status: automated_pipeline",
            "---",
            "\n"
        ]
        return "\n".join(metadata) + content

    def get_hash(self, content: str) -> str:
        """실질적인 본문 내용 변화를 감지하기 위한 해시 생성"""
        # 공백 및 특수기호 제거 후 해시 계산 (노이즈 방지)
        text_only = re.sub(r'\s+', '', content)
        return hashlib.md5(text_only.encode('utf-8')).hexdigest()

    async def process_channel(self, stack: dict, channel_type: str, url: str) -> bool:
        """각 채널별 문서 수집 및 증분 업데이트 실행"""
        target_dir = self.root_dir / stack["target_dir"]
        target_filename = f"{stack['name']}-{channel_type}.md"
        target_path = target_dir / target_filename
        
        logger.info(f"[{stack['name'].upper()}] {channel_type} 채널 수집 시도...")
        
        # 1. 콘텐츠 획득
        raw_md = await self.fetch_content(url)
        if not raw_md or len(raw_md.strip()) < 100:
            logger.warning(f"  -> 유효한 콘텐츠가 부족합니다 ({len(raw_md)} bytes).")
            return False
            
        current_hash = self.get_hash(raw_md)
        
        # 2. 멱등성 검사 (기존 파일 존재 시 해시 비교)
        if target_path.exists():
            existing_text = target_path.read_text(encoding="utf-8")
            if f"Fingerprint: {current_hash}" in existing_text:
                logger.info(f"  -> [Skip] 변경 사항 없음: {target_filename}")
                return False

        # 3. 메타데이터 결합 및 지문(Fingerprint) 추가
        final_doc = self.add_frontmatter(raw_md, stack, channel_type, url)
        final_doc += f"\n\n---\n*Fingerprint: {current_hash}*"
        
        # 4. 물리적 저장
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(final_doc, encoding="utf-8")
        logger.info(f"  -> [Update] 문서 저장 완료: {target_filename}")
        return True

    async def run(self):
        """설정된 모든 기술 스택과 채널을 순회하며 수집"""
        if not self.config_path.exists():
            logger.error(f"설정 파일을 찾을 수 없습니다: {self.config_path}")
            return

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        tasks = []
        for stack in config.get("tech_stacks", []):
            channels = stack.get("channels", {})
            for ch_type, url in channels.items():
                tasks.append(self.process_channel(stack, ch_type, url))

        logger.info(f"총 {len(tasks)}개의 기술 채널 수집 파이프라인 가동 중...")
        results = await asyncio.gather(*tasks)
        
        updated_count = sum(1 for r in results if r)
        logger.info("========================================")
        logger.info(f"동기화 요약: 총 {len(tasks)}건 중 {updated_count}건의 지식 업데이트 성공.")
        logger.info("========================================")
        
        await self.client.aclose()

if __name__ == "__main__":
    # 프로젝트 루트 기반 설정 로드
    base_dir = Path(__file__).resolve().parent.parent.parent
    config_file = base_dir / "config" / "sources.json"
    
    fetcher = TechDocFetcher(config_file)
    asyncio.run(fetcher.run())
