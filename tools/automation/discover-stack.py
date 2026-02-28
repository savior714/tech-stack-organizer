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
    },
    "pyhwpx": {
        "official": "https://pyhwpx.readthedocs.io/",
        "github": "https://github.com/updaun/pyhwpx",
        "registry": "https://pypi.org/project/pyhwpx/",
        "curation": "https://pypi.org/project/pyhwpx/"
    },
    "requests": {
        "official": "https://requests.readthedocs.io/",
        "github": "https://github.com/psf/requests",
        "registry": "https://pypi.org/project/requests/"
    },
    "pandas": {
        "official": "https://pandas.pydata.org/docs/",
        "github": "https://github.com/pandas-dev/pandas",
        "registry": "https://pypi.org/project/pandas/"
    },
    "pymupdf": {
        "official": "https://pymupdf.readthedocs.io/",
        "github": "https://github.com/pymupdf/PyMuPDF",
        "registry": "https://pypi.org/project/PyMuPDF/"
    }
}

class StackDiscoverer:
    def __init__(self, target_project_path: Path):
        self.target_path = target_project_path
        self.found_stacks = {}

    def get_dependency_files(self):
        """프로젝트 전체 폴더에서 의존성 파일을 재귀적으로 탐색 (제외 폴더 준수)"""
        exclude_dirs = {".venv", "node_modules", ".git", "__pycache__", "build", "dist", ".agents"}
        files = {
            "requirements": [],
            "package_json": [],
            "cargo_toml": [],
            "pyproject_toml": []
        }
        
        print(f"[*] Deep scanning project tree: {self.target_path.resolve()}")
        for root, dirs, filenames in os.walk(self.target_path):
            # 대규모 종속성 폴더는 탐색에서 제외
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for filename in filenames:
                full_path = Path(root) / filename
                if filename == "requirements.txt":
                    files["requirements"].append(full_path)
                elif filename == "package.json":
                    files["package_json"].append(full_path)
                elif filename == "Cargo.toml":
                    files["cargo_toml"].append(full_path)
                elif filename == "pyproject.toml":
                    files["pyproject_toml"].append(full_path)
        
        return files

    def process_requirements(self, file_paths):
        for path in file_paths:
            content = path.read_text(encoding="utf-8", errors="ignore")
            packages = re.findall(r"^([a-zA-Z0-9\-_]+)", content, re.MULTILINE)
            for pkg in packages:
                self.register_stack(pkg)

    def process_package_json(self, file_paths):
        for path in file_paths:
            try:
                data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                for dep in deps:
                    self.register_stack(dep)
            except Exception: pass

    def process_cargo_toml(self, file_paths):
        for path in file_paths:
            self.register_stack("rust")
            content = path.read_text(encoding="utf-8", errors="ignore")
            if "tauri" in content.lower():
                self.register_stack("tauri")

    def process_pyproject_toml(self, file_paths):
        for path in file_paths:
            content = path.read_text(encoding="utf-8", errors="ignore")
            matches = re.finditer(r'["\']([a-zA-Z0-9\-_]+)[>=<~]*', content)
            for match in matches:
                self.register_stack(match.group(1).lower())

    def register_stack(self, pkg):
        pkg_lower = pkg.lower()
        if pkg_lower in TEMPLATES:
            self.found_stacks[pkg_lower] = TEMPLATES[pkg_lower]
        else:
            # 템플릿에 없더라도 발견된 경우 기본 구조로 등록
            if pkg_lower not in self.found_stacks:
                self.found_stacks[pkg_lower] = {
                    "official": "", 
                    "github": f"https://github.com/search?q={pkg}&type=repositories", 
                    "registry": f"https://pypi.org/project/{pkg}/", 
                    "curation": ""
                }

    def discover(self):
        dep_files = self.get_dependency_files()
        
        self.process_requirements(dep_files["requirements"])
        self.process_package_json(dep_files["package_json"])
        self.process_cargo_toml(dep_files["cargo_toml"])
        self.process_pyproject_toml(dep_files["pyproject_toml"])
        
        # Python 기본 추가
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
    # [루트 탐색 로직 강화]
    # 서브모듈 내부가 아닌, 실제 .git 디렉토리가 존재하는 최상위 프로젝트 루트를 찾아 거슬러 올라감
    current_path = Path.cwd()
    target = current_path
    
    # 상위 경로로 거슬러 올라가며 .git 디렉토리를 찾음
    # (서브모듈의 .git 파일이 아닌, 실제 프로젝트 루트의 .git을 찾기 위해 .is_dir() 확인 또는 반복 탐색)
    temp_path = current_path
    found_git_root = None
    for _ in range(5):  # 최대 5단계까지 상위 탐색
        git_path = temp_path / ".git"
        if git_path.exists():
            found_git_root = temp_path
            # 만약 .git이 디렉토리라면 최상위 루트로 간주하고 중단 (서브모듈은 .git이 파일일 확률이 높음)
            if git_path.is_dir():
                break
        if temp_path.parent == temp_path:
            break
        temp_path = temp_path.parent

    if found_git_root:
        target = found_git_root
        print(f"[+] Project root identified: {target}")
    else:
        print(f"[!] Warning: .git root not found. Using current directory: {target}")
        
    discoverer = StackDiscoverer(target)
    found = discoverer.discover()
    
    # 설정 파일은 항상 이 도구(tech-stack-organizer)의 루트 내 config/에 저장함
    script_root = Path(__file__).resolve().parent.parent.parent
    config_file = script_root / "config" / "sources.json"
    discoverer.generate_sources_json(config_file)
    
    print(f"[*] Found {len(found)} stacks: {', '.join(found.keys())}")
    print("[!] Please review 'config/sources.json' and run 'start.bat' to sync documentation.")
