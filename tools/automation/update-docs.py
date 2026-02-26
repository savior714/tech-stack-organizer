import asyncio
import hashlib
import json
import os
import re
from datetime import datetime
from pathlib import Path

import httpx

# [Configuration]
CONFIG_PATH = Path("config/sources.json")
READER_API_PREFIX = "https://r.jina.ai/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

class TechDocFetcher:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.root_dir = config_path.parent.parent
        self.client = httpx.AsyncClient(
            timeout=60.0, 
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT}
        )

    async def fetch_content(self, url: str) -> str:
        """Jina Reader를 거쳐 마크다운 형식으로 데이터 획득"""
        if not url: return ""
        
        target_url = f"{READER_API_PREFIX}{url}"
        try:
            response = await self.client.get(target_url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"[ERROR] Failed to fetch {url}: {str(e)}")
            return ""

    def add_front_matter(self, content: str, stack: dict, channel_type: str, url: str) -> str:
        """YAML Front-matter 메타데이터 주입 (사용자 정의 규격)"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metadata = [
            "---",
            f"Tech-Stack: {stack['name']}",
            f"Channel: {channel_type}",
            f"Source-URL: {url}",
            f"Last-Updated: {now}",
            f"Tech-Version: {stack.get('version', 'latest')}",
            f"Status: automated_pipeline",
            "---",
            "\n"
        ]
        return "\n".join(metadata) + content

    def get_hash(self, content: str) -> str:
        """내용 변화 감지를 위한 MD5 해시 생성 (멱등성 보장)"""
        text_only = re.sub(r'\s+', '', content)
        return hashlib.md5(text_only.encode('utf-8')).hexdigest()

    async def process_channel(self, stack: dict, channel_type: str, url: str) -> bool:
        """단일 채널 수집 및 증분 업데이트"""
        target_dir = self.root_dir / stack["target_dir"]
        target_filename = f"{stack['name']}-{channel_type}.md"
        target_path = target_dir / target_filename
        
        # 1. 콘텐츠 획득
        raw_md = await self.fetch_content(url)
        if not raw_md or len(raw_md.strip()) < 100:
            return False
            
        current_hash = self.get_hash(raw_md)
        
        # 2. 증분 업데이트 확인 (Fingerprint 기반)
        if target_path.exists():
            with open(target_path, "r", encoding="utf-8") as f:
                existing_text = f.read()
                if f"Fingerprint: {current_hash}" in existing_text:
                    print(f"[-] No changes detected for {stack['name']} ({channel_type}). Skipping.")
                    return False

        # 3. 문서 결합 및 저장
        full_content = self.add_front_matter(raw_md, stack, channel_type, url)
        full_content += f"\n\n---\n*Fingerprint: {current_hash}*"
        
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"[+] Successfully updated: {target_path}")
        return True

    async def run(self):
        """전체 파이프라인 가동"""
        if not self.config_path.exists():
            print(f"[ERROR] Configuration file not found at {self.config_path}")
            return

        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        tasks = []
        for stack in config.get("tech_stacks", []):
            channels = stack.get("channels", {})
            for ch_type, url in channels.items():
                if url:
                    tasks.append(self.process_channel(stack, ch_type, url))

        if tasks:
            print(f"[*] Starting update for {len(tasks)} documentation sources...")
            await asyncio.gather(*tasks)
            print("[*] All documentation updates completed.")
        else:
            print("[!] No URLs found to update.")
        
        await self.client.aclose()

if __name__ == "__main__":
    # Windows 환경에서의 비동기 정책 설정
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # 프로젝트 루트 기반 설정 로드
    base_dir = Path(__file__).resolve().parent.parent.parent
    config_file = base_dir / "config" / "sources.json"
    
    fetcher = TechDocFetcher(config_file)
    asyncio.run(fetcher.run())
