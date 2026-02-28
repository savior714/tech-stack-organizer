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

    def clean_content(self, content: str, channel_type: str, url: str) -> str:
        """문서 유형별로 불필요한 보일러플레이트(GNB, LNB, Footer)를 제거하여 핵심 내용만 추출"""
        lines = content.splitlines()
        result = []
        
        # 1. Github Releases 채널 특화 (릴리즈 본문 집중 추출)
        if channel_type == "github" or "github.com" in url:
            started = False
            for line in lines:
                text = line.strip()
                # 릴리즈 태그나 메인 헤더가 등장할 때부터 클리닝 없이 모두 기록 시작
                if not started:
                    if re.match(r'^(v\d+\.|[a-zA-Z0-9_\-]+@\d+\.|Releases: |##\s+v\d+)', text):
                        started = True
                
                if started:
                    # 마크다운 형태소 중 불필요한 GitHub UI 단골 문구 제거
                    if "reacted with" in text or "people reacted" in text or "All reactions" in text: continue
                    if text.startswith("👍") or text.startswith("🎉") or text.startswith("❤️") or text.startswith("🚀") or text.startswith("👀") or text.startswith("*   👍") or text.startswith("*   🎉") or text.startswith("*   🚀"): continue
                    if "This commit was created on GitHub.com and signed" in text or "This commit was signed with the committer’s" in text or "verified signature" in text: continue
                    if "GPG key ID:" in text or "SSH Key Fingerprint:" in text: continue
                    if "Learn about vigilant mode" in text or text == "Verified" or text == "Compare": continue
                    if "Choose a tag to compare" in text or "Sorry, something went wrong" in text: continue
                    if text == "Pre-release" or text == "Filter" or text == "Loading": continue
                    if "There was an error while loading." in text: continue
                    if text == "No results found" or "View all tags" in text: continue
                    if re.match(r'^\*?\s*\[([a-f0-9]{7})\]', text): continue # 커밋 해시 링크
                    if re.match(r'^!\[Image .*\]\(.*avatars\.githubusercontent\.com', text): continue # 아바타 (본분 외)
                    if re.match(r'^\*?\s*\[v\d+\.\d+\.\d+.*\]\(.*compare/v.*', text): continue # 버전 비교 리스트 전체 삭제
                    if re.match(r'^Assets(\s+\d+)?$', text) or "Source code(zip)" in text or "Source code(tar.gz)" in text: continue
                    if text in ("=======================", "----------------------------"): continue
                    
                    result.append(line)
            
            if result:
                return "\n".join(result)
        
        # 2. PyPI (Python Registry) 전용 클리닝 (가장 악명 높은 휠 파일, 해시, 릴리즈 폭탄 제거)
        if "pypi.org" in url:
            started = False
            for line in lines:
                text = line.strip()
                if text == "Project description":
                    started = True
                
                # 우측 사이드바 메타데이터 복제본(Project details 이후) 및 방대한 파일 리스트 차단
                if text.startswith("Project details") or text.startswith("Release history") or text.startswith("Download files"):
                    break
                    
                if started:
                    if text in ("Project description", "-------------------"): continue
                    # 라인 전체가 뱃지로만 이루어진 경우 스킵
                    if re.match(r'^(!?\[Image [^\]]+\]\([^)]+\))+\s*$', text): continue
                    result.append(line)
            
            if result:
                return "\n".join(result)

        # 3. Crates.io (Rust Registry) 특화
        if "crates.io" in url:
            for line in lines:
                text = line.strip()
                # 인라인 뱃지들 일괄 제거
                line_no_badges = re.sub(r'!?\[Image [^\]]+\]\([^)]+\)', '', line)
                line_no_badges_link = re.sub(r'\[(!?\[Image [^\]]+\]\([^)]+\))\]\([^)]+\)', '', line)
                if len(line_no_badges.strip()) == 0 or len(line_no_badges_link.strip()) == 0:
                    continue
                if text.startswith("| Component | Version |") or text.startswith("| --- | --- |"): continue
                if re.match(r'^\|\s*tauri\s*\|\s*!\[Image', text): continue
                result.append(line)
                
            if result:
                return "\n".join(result)

        # 4. 범용 웹사이트 클리닝 (Official, Registry 공통)
        skip_phrases = [
            "Skip to content", "Navigation Menu", "Toggle navigation", 
            "Sign in", "Sign up", "Search or jump to", 
            "Provide feedback", "We read every piece of feedback",
            "Appearance settings", "Security Update: Classic tokens",
            "package search", "Readme Code Beta", "Dependencies", "Dependents"
        ]
        
        # npm registry 등 범용에서 흔히 보이는 Header, Footer 제거용 상태 변수
        in_footer = False
        
        for line in lines:
            text = line.strip()
            if text == "Footer" or text.startswith("Footer navigation") or text == "Terms & Policies":
                in_footer = True
            
            if in_footer:
                continue

            if any(phrase in text for phrase in skip_phrases) and len(text) < 120:
                continue
                
            # NPM 탭 메뉴 및 자잘한 UI 텍스트 제거
            if re.match(r'^\*\s+\[(Readme|Code Beta|\d+ Dependencies|\d+ Dependents|[\d,]+ Versions)\]', text): continue
            
            result.append(line)
            
        # 연속된 빈 줄(3줄 이상) 및 구분선 압축. 공백문자가 섞인 경우도 포괄하여 파괴적인 공백 압축
        cleaned_text = "\n".join(result)
        cleaned_text = re.sub(r'\n[ \t]*\n([ \t]*\n)+', '\n\n', cleaned_text)
        return cleaned_text.strip()

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

        # 1.5. 본문 핵심 요소 추출 (보일러플레이트 제거 파이프라인)
        cleaned_md = self.clean_content(raw_md, channel_type, url)
        # 필터링 부작용으로 본문이 날아간 경우 원본 복구 (안전망)
        if len(cleaned_md) < 200:
            cleaned_md = raw_md

        current_hash = self.get_hash(cleaned_md)

        # 2. 증분 업데이트 확인 (Fingerprint 기반)
        if target_path.exists():
            existing_text = target_path.read_text(encoding="utf-8")
            if f"Fingerprint: {current_hash}" in existing_text:
                self.logger.info(f"[-] No changes: {stack['name']} ({channel_type}). Skipping.")
                return "skipped"

        # 3. 문서 결합 및 저장
        full_content = self.add_front_matter(cleaned_md, stack, channel_type, url)
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
