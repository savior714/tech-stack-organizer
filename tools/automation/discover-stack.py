import json
import os
import re
from pathlib import Path

# [Tech Stack Templates]
# 자주 사용되는 기술 스택별 표준 채널 템플릿
TEMPLATES = {
    "python": {
        "official": "https://docs.python.org/3/whatsnew/index.html",
        "github": "https://github.com/python/cpython/releases",
        "registry": "https://pypi.org/project/python/",
        "proposals": "https://peps.python.org/",
        "curation": "https://awesome-python.com/"
    },
    "nuitka": {
        "official": "https://nuitka.net/doc/user-manual.html",
        "github": "https://github.com/Nuitka/Nuitka/blob/develop/Changelog.rst",
        "registry": "https://pypi.org/project/Nuitka/",
        "curation": "https://nuitka.net/blog/"
    },
    "tauri": {
        "official": "https://tauri.app/v1/guides/",
        "github": "https://github.com/tauri-apps/tauri/releases",
        "registry": "https://crates.io/crates/tauri",
        "curation": "https://github.com/tauri-apps/awesome-tauri"
    },
    "rust": {
        "official": "https://doc.rust-lang.org/stable/reference/",
        "github": "https://github.com/rust-lang/rust/releases",
        "registry": "https://crates.io/",
        "curation": "https://github.com/rust-unofficial/awesome-rust"
    },
    "react": {
        "official": "https://react.dev/blog",
        "github": "https://github.com/facebook/react/releases",
        "registry": "https://www.npmjs.com/package/react",
        "curation": "https://github.com/enaqx/awesome-react"
    }
}

class StackDiscoverer:
    def __init__(self, target_project_path: Path):
        self.target_path = target_project_path
        self.found_stacks = {}

    def scan_requirements_txt(self):
        req_file = self.target_path / "requirements.txt"
        if req_file.exists():
            content = req_file.read_text(encoding="utf-8")
            # 간단한 패키지명 추출 (버전 제외)
            packages = re.findall(r"^([a-zA-Z0-9\-_]+)", content, re.MULTILINE)
            for pkg in packages:
                pkg_lower = pkg.lower()
                if pkg_lower in TEMPLATES:
                    self.found_stacks[pkg_lower] = TEMPLATES[pkg_lower]
                else:
                    # 템플릿에는 없지만 발견된 경우 빈 구조 생성
                    self.found_stacks[pkg_lower] = {
                        "official": "", "github": "", "registry": f"https://pypi.org/project/{pkg}/", "curation": ""
                    }

    def scan_package_json(self):
        pkg_file = self.target_path / "package.json"
        if pkg_file.exists():
            try:
                data = json.loads(pkg_file.read_text(encoding="utf-8"))
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                for dep in deps:
                    dep_lower = dep.lower()
                    if dep_lower in TEMPLATES:
                        self.found_stacks[dep_lower] = TEMPLATES[dep_lower]
                    elif "react" in dep_lower:
                        self.found_stacks["react"] = TEMPLATES["react"]
            except Exception:
                pass

    def scan_cargo_toml(self):
        cargo_file = self.target_path / "Cargo.toml"
        if cargo_file.exists():
            self.found_stacks["rust"] = TEMPLATES["rust"]
            content = cargo_file.read_text(encoding="utf-8")
            if "tauri" in content.lower():
                self.found_stacks["tauri"] = TEMPLATES["tauri"]

    def discover(self):
        print(f"[*] Scanning for tech stacks in: {self.target_path.resolve()}")
        self.scan_requirements_txt()
        self.scan_package_json()
        self.scan_cargo_toml()
        
        # Python은 기본으로 추가 (대부분의 우리 프로젝트 환경)
        if "python" not in self.found_stacks:
            self.found_stacks["python"] = TEMPLATES["python"]

        return self.found_stacks

    def generate_sources_json(self, output_path: Path):
        stacks_list = []
        for name, channels in self.found_stacks.items():
            stacks_list.append({
                "name": name,
                "version": "latest",
                "channels": channels,
                "target_dir": f"docs/{name}"
            })
        
        config = {"tech_stacks": stacks_list}
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(config, indent=4), encoding="utf-8")
        print(f"[+] Configuration generated: {output_path}")

if __name__ == "__main__":
    # 서브모듈로 사용될 경우 부모 디렉토리가 대상 프로젝트임
    # 하지만 현재 개발 환경 고려하여 루트 또는 부모 확인
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    
    # 만약 현재 디렉토리에 .git이 없고 부모 디렉토리에 있다면 서브모듈 상황으로 가정
    parent_dir = project_root.parent
    target = project_root
    if (parent_dir / ".git").exists():
        target = parent_dir
        
    discoverer = StackDiscoverer(target)
    found = discoverer.discover()
    
    config_file = project_root / "config" / "sources.json"
    discoverer.generate_sources_json(config_file)
    
    print(f"[*] Found {len(found)} stacks: {', '.join(found.keys())}")
    print("[!] Please review 'config/sources.json' and run 'start.bat' to sync documentation.")
