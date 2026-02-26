import argparse
import asyncio
import hashlib
import json
import logging
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

import httpx

# [Configuration]
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
READER_API_PREFIX = "https://r.jina.ai/"


def setup_logging(log_dir: Path) -> logging.Logger:
    """파일 + 콘솔 동시 출력 로거 초기화"""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_filename = log_dir / f"update-docs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logger = logging.getLogger("TechDocFetcher")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s", datefmt="%H:%M:%S")

    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Log file: {log_filename}")
    return logger


class TechDocFetcher:
    def __init__(self, config_path: Path, logger: logging.Logger):
        self.config_path = config_path
        self.root_dir = config_path.parent.parent
        self.logger = logger
        # 동시성 극단적 제한 (Jina Rate Limit 우회용)
        self.semaphore = asyncio.Semaphore(1)
        self.client = httpx.AsyncClient(
            timeout=60.0,
            follow_redirects=True,
            http2=False,  # Cloudflare Fingerprinting 방지 (HTTP/1.1 강제)
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            },
        )

    async def fetch_content(self, url: str) -> str:
        """Jina Reader를 거쳐 마크다운 형식으로 데이터 획득 (세마포어 및 재시도 적용)"""
        if not url:
            return ""

        target_url = f"{READER_API_PREFIX}{url}"
        async with self.semaphore:
            for attempt in range(2):
                try:
                    await asyncio.sleep(2.0 + (attempt * 2))
                    response = await self.client.get(target_url)

                    if response.status_code == 403:
                        self.logger.warning(f"[RETRY] 403 Forbidden for {url}. Falling back to urllib...")
                        return self._urllib_fallback(target_url, url)

                    response.raise_for_status()
                    return response.text

                except Exception as e:
                    self.logger.warning(f"[ERROR] Attempt {attempt + 1} failed for {url}: {e}")
                    if attempt == 1:
                        self.logger.warning(f"[FALLBACK] Trying urllib for {url}...")
                        return self._urllib_fallback(target_url, url)

        return ""

    def _urllib_fallback(self, target_url: str, original_url: str) -> str:
        """httpx 실패 시 urllib 폴백"""
        try:
            req = urllib.request.Request(
                target_url,
                headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
            )
            with urllib.request.urlopen(req, timeout=30) as res:
                return res.read().decode("utf-8")
        except Exception as fe:
            self.logger.error(f"[ERROR] urllib fallback failed for {original_url}: {fe}")
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
            "\n",
        ]
        return "\n".join(metadata) + content

    def get_hash(self, content: str) -> str:
        """내용 변화 감지를 위한 MD5 해시 생성 (멱등성 보장)"""
        text_only = re.sub(r"\s+", "", content)
        return hashlib.md5(text_only.encode("utf-8")).hexdigest()

    async def process_channel(self, stack: dict, channel_type: str, url: str) -> str:
        """단일 채널 수집 및 증분 업데이트. 결과 상태 문자열 반환: 'updated' | 'skipped' | 'failed'"""
        target_dir = self.root_dir / stack["target_dir"]
        target_filename = f"{stack['name']}-{channel_type}.md"
        target_path = target_dir / target_filename

        # 1. 콘텐츠 획득
        raw_md = await self.fetch_content(url)
        if not raw_md or len(raw_md.strip()) < 100:
            self.logger.warning(f"[FAILED] {stack['name']} ({channel_type}): empty or too short content.")
            return "failed"

        current_hash = self.get_hash(raw_md)

        # 2. 증분 업데이트 확인 (Fingerprint 기반)
        if target_path.exists():
            existing_text = target_path.read_text(encoding="utf-8")
            if f"Fingerprint: {current_hash}" in existing_text:
                self.logger.info(f"[-] No changes: {stack['name']} ({channel_type}). Skipping.")
                return "skipped"

        # 3. 문서 결합 및 저장
        full_content = self.add_front_matter(raw_md, stack, channel_type, url)
        full_content += f"\n\n---\n*Fingerprint: {current_hash}*"

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(full_content, encoding="utf-8")
        self.logger.info(f"[+] Updated: {target_path}")
        return "updated"

    async def run(self, filter_stacks: list[str] | None = None, filter_channels: list[str] | None = None):
        """전체 파이프라인 가동"""
        if not self.config_path.exists():
            self.logger.error(f"Configuration file not found: {self.config_path}")
            return

        config = json.loads(self.config_path.read_text(encoding="utf-8"))

        tasks = []
        task_labels = []
        for stack in config.get("tech_stacks", []):
            if filter_stacks and stack["name"] not in filter_stacks:
                continue
            channels = stack.get("channels", {})
            for ch_type, url in channels.items():
                if filter_channels and ch_type not in filter_channels:
                    continue
                if url:
                    tasks.append(self.process_channel(stack, ch_type, url))
                    task_labels.append(f"{stack['name']}/{ch_type}")

        if not tasks:
            self.logger.warning("[!] No matching URLs found to update.")
            await self.client.aclose()
            return

        self.logger.info(f"[*] Starting update for {len(tasks)} documentation sources...")
        results = await asyncio.gather(*tasks)

        # 결과 요약
        counts = {"updated": 0, "skipped": 0, "failed": 0}
        for label, result in zip(task_labels, results):
            counts[result] += 1

        self.logger.info("=" * 54)
        self.logger.info(f"[SUMMARY] Total: {len(tasks)} | "
                         f"Updated: {counts['updated']} | "
                         f"Skipped: {counts['skipped']} | "
                         f"Failed: {counts['failed']}")
        if counts["failed"] > 0:
            failed_labels = [label for label, r in zip(task_labels, results) if r == "failed"]
            self.logger.warning(f"[FAILED CHANNELS] {', '.join(failed_labels)}")
        self.logger.info("=" * 54)

        await self.client.aclose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tech Stack Organizer - Documentation Fetcher")
    parser.add_argument("--stacks", nargs="+", metavar="STACK",
                        help="Update only specific stacks (e.g. --stacks python nuitka)")
    parser.add_argument("--channels", nargs="+", metavar="CHANNEL",
                        help="Update only specific channels (e.g. --channels official github)")
    args = parser.parse_args()

    # Windows 환경에서의 비동기 정책 설정
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # 프로젝트 루트 기반 절대경로 설정
    base_dir = Path(__file__).resolve().parent.parent.parent
    config_file = base_dir / "config" / "sources.json"
    log_dir = base_dir / "logs"

    logger = setup_logging(log_dir)
    fetcher = TechDocFetcher(config_file, logger)
    asyncio.run(fetcher.run(filter_stacks=args.stacks, filter_channels=args.channels))
