import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path

import httpx

# 로그 설정
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
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)

    async def fetch_markdown(self, url: str) -> str:
        """Jina Reader API를 사용하여 웹페이지를 마크다운으로 변환"""
        fetch_url = f"{JINA_READER_URL}{url}"
        try:
            response = await self.client.get(fetch_url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return ""

    def add_metadata(self, content: str, source: dict) -> str:
        """문서 상단에 Front-matter 메타데이터 삽입"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metadata = [
            "---",
            f"title: {source.get('title')}",
            f"tech: {source.get('tech')}",
            f"source_url: {source.get('url')}",
            f"extracted_at: {now}",
            "version: Python 3.14.2",
            "---",
            "\n"
        ]
        return "\n".join(metadata) + content

    async def process_source(self, source: dict) -> bool:
        """단일 소스 처리 및 업데이트 여부 결정"""
        url = source["url"]
        target_rel_path = source["target_path"]
        target_path = self.root_dir / target_rel_path
        
        logger.info(f"Processing: {source['title']} ({url})")
        
        # 1. 마크다운 추출
        raw_markdown = await self.fetch_markdown(url)
        if not raw_markdown:
            return False
            
        full_content = self.add_metadata(raw_markdown, source)
        
        # 2. 증분 업데이트 확인 (내용 비교)
        if target_path.exists():
            existing_content = target_path.read_text(encoding="utf-8")
            # 메타데이터를 제외한 본문 비교 (실제로는 메타데이터 날짜 때문에 매번 바뀔 수 있으므로 본문 위주 비교 권장)
            # 여기서는 단순 전체 비교를 수행하되, 필요시 정교화 가능
            if existing_content.strip() == full_content.strip():
                logger.info(f"  -> No changes detected for {source['title']}.")
                return False

        # 3. 파일 저장
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(full_content, encoding="utf-8")
        logger.info(f"  -> Successfully updated: {target_rel_path}")
        return True

    async def run(self):
        """전체 파이프라인 실행"""
        if not self.config_path.exists():
            logger.error(f"Config file not found: {self.config_path}")
            return

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        sources = config.get("sources", [])
        tasks = [self.process_source(s) for s in sources]
        
        results = await asyncio.gather(*tasks)
        updated_count = sum(1 for r in results if r)
        
        logger.info("========================================")
        logger.info(f"Task Completed: {updated_count}/{len(sources)} documents updated.")
        logger.info("========================================")
        
        await self.client.aclose()

if __name__ == "__main__":
    # 프로젝트 루트 기준 경로 설정
    current_dir = Path(__file__).parent
    config_file = current_dir.parent.parent / "config" / "sources.json"
    
    fetcher = DocFetcher(config_file)
    asyncio.run(fetcher.run())
