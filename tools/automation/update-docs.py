import asyncio
import hashlib
import json
import logging
import re
from datetime import datetime
from pathlib import Path

import httpx

# 로그 설정 (한국어 출력 대응)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Jina Reader API Endpoint
JINA_READER_URL = "https://r.jina.ai/"

class DocFetcher:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.root_dir = config_path.parent.parent
        self.client = httpx.AsyncClient(
            timeout=60.0, 
            follow_redirects=True,
            headers={"User-Agent": "TechStackOrganizer/1.0 (Automation Architect)"}
        )

    async def fetch_markdown(self, url: str) -> str:
        """Jina Reader API를 사용하여 웹페이지를 최적화된 마크다운으로 변환"""
        fetch_url = f"{JINA_READER_URL}{url}"
        try:
            logger.info(f"  -> 패치 시작: {fetch_url}")
            response = await self.client.get(fetch_url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"  -> 패치 실패 ({url}): {e}")
            return ""

    def add_frontmatter(self, content: str, source: dict) -> str:
        """YAML Front-matter 메타데이터 주입"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metadata = [
            "---",
            f"title: {source.get('title')}",
            f"tech_stack: {source.get('tech')}",
            f"source_url: {source.get('url')}",
            f"collected_at: {now}",
            f"python_version: 3.14.2",
            "status: automated",
            "---",
            "\n"
        ]
        return "\n".join(metadata) + content

    def clean_doc(self, content: str) -> str:
        """불필요한 공백 및 노이즈 제거 기초 정제"""
        content = re.sub(r'\n{3,}', '\n\n', content)
        return content.strip()

    def get_hash(self, content: str) -> str:
        """내용 변화 감지를 위한 MD5 해시 생성"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    async def process_source(self, source: dict) -> bool:
        """단일 소스 수집 및 증분 업데이트 처리"""
        url = source["url"]
        target_path = self.root_dir / source["target_path"]
        
        logger.info(f"기술 문서 수집 중: {source['title']}")
        
        # 1. 획득 및 정제
        raw_md = await self.fetch_markdown(url)
        if not raw_md:
            return False
            
        cleaned_md = self.clean_doc(raw_md)
        current_hash = self.get_hash(cleaned_md)
        
        # 2. 멱등성 검사 (본문 해시 비교)
        if target_path.exists():
            existing_text = target_path.read_text(encoding="utf-8")
            if f"Fingerprint: {current_hash}" in existing_text:
                logger.info(f"  -> [Skip] 변경 사항 없음: {source['title']}")
                return False

        # 3. 메타데이터 및 지문 기록 후 저장
        final_doc = self.add_frontmatter(cleaned_md, source)
        final_doc += f"\n\n---\n*Fingerprint: {current_hash}*"
        
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(final_doc, encoding="utf-8")
        logger.info(f"  -> [Update] 문서 반영 완료: {source['target_path']}")
        return True

    async def run(self):
        """파이프라인 실행 엔진"""
        if not self.config_path.exists():
            logger.error(f"설정 파일을 찾을 수 없습니다: {self.config_path}")
            return

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        sources = config.get("sources", [])
        logger.info(f"총 {len(sources)}개의 소스 분석을 시작합니다.")
        
        # 동시성 처리
        tasks = [self.process_source(s) for s in sources]
        results = await asyncio.gather(*tasks)
        
        updated = sum(1 for r in results if r)
        logger.info("========================================")
        logger.info(f"결과 요약: 전체 {len(sources)}건 중 {updated}건 업데이트 완료.")
        logger.info("========================================")
        
        await self.client.aclose()

if __name__ == "__main__":
    # 실행 경로 기준 설정 로드
    base_path = Path(__file__).resolve().parent.parent.parent
    config_p = base_path / "config" / "sources.json"
    
    fetcher = DocFetcher(config_p)
    asyncio.run(fetcher.run())
