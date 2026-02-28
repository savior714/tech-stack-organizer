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
        "github": "https://github.com/psf/requests/releases",
        "registry": "https://pypi.org/project/requests/"
    },
    "pandas": {
        "official": "https://pandas.pydata.org/docs/",
        "github": "https://github.com/pandas-dev/pandas/releases",
        "registry": "https://pypi.org/project/pandas/"
    },
    "pymupdf": {
        "official": "https://pymupdf.readthedocs.io/",
        "github": "https://github.com/pymupdf/PyMuPDF/releases",
        "registry": "https://pypi.org/project/PyMuPDF/"
    },
    "playwright": {
        "official": "https://playwright.dev/python/docs/intro",
        "github": "https://github.com/microsoft/playwright-python/releases",
        "registry": "https://pypi.org/project/playwright/"
    },
    "httpx": {
        "official": "https://www.python-httpx.org/",
        "github": "https://github.com/encode/httpx/releases",
        "registry": "https://pypi.org/project/httpx/"
    },
    "fastapi": {
        "official": "https://fastapi.tiangolo.com/",
        "github": "https://github.com/tiangolo/fastapi/releases",
        "registry": "https://pypi.org/project/fastapi/"
    },
    "typescript": {
        "official": "https://www.typescriptlang.org/docs/",
        "github": "https://github.com/microsoft/TypeScript/releases",
        "registry": "https://www.npmjs.com/package/typescript"
    },
    "vite": {
        "official": "https://vitejs.dev/guide/",
        "github": "https://github.com/vitejs/vite/releases",
        "registry": "https://www.npmjs.com/package/vite"
    },
    "tailwindcss": {
        "official": "https://tailwindcss.com/docs",
        "github": "https://github.com/tailwindlabs/tailwindcss/releases",
        "registry": "https://www.npmjs.com/package/tailwindcss"
    }
}

# 기술 스택으로 오인될 수 있는 일반 단어 또는 프로젝트 내부 구조
BLACKLIST = {
    "src", "test", "tests", "docs", "build", "dist", "bin", "app", 
    "readme", "license", "main", "core", "index", "utils", "config",
    "scripts", "tools", "version", "name", "author", "description",
    "0", "1", "2", "add", "alt", "graph", "internal", "private", "temp",
    "venv", ".venv", "node_modules", "cheonggu", "none", "true", "false",
    "repository", "homepage", "bugs", "keywords", "scripts", "dependencies",
    "dev-dependencies", "group", "tool"
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
            # 주석 및 버전 제약 조건 제외한 순수 패키지 명만 추출
            packages = re.findall(r"^[ \t]*([a-zA-Z0-9\-_]+)", content, re.MULTILINE)
            for pkg in packages:
                self.register_stack(pkg)

    def process_package_json(self, file_paths):
        for path in file_paths:
            try:
                data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
                # dependencies, devDependencies 필드 내의 키값만 추출
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                for dep in deps:
                    self.register_stack(dep)
            except Exception: pass

    def process_cargo_toml(self, file_paths):
        for path in file_paths:
            self.register_stack("rust")
            content = path.read_text(encoding="utf-8", errors="ignore")
            # Cargo.toml은 [dependencies] 섹션 이후의 키값을 찾는 것이 좋으나, tauri 여부만 우선 체크
            if "tauri" in content.lower():
                self.register_stack("tauri")

    def process_pyproject_toml(self, file_paths):
        for path in file_paths:
            content = path.read_text(encoding="utf-8", errors="ignore")
            # [project.dependencies], [tool.poetry.dependencies] 등 의존성 섹션 탐색
            # 간단하게 dependency 라는 단어가 포함된 라인 주변의 패키지명만 추출하도록 개선
            in_deps_section = False
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#"): continue
                
                # 섹션 변경 확인
                if line.startswith("[") and line.endswith("]"):
                    section = line.lower()
                    if "dependenc" in section or "requires" in section:
                        in_deps_section = True
                    else:
                        in_deps_section = False
                    continue
                
                if in_deps_section:
                    # 'package = "..." ' 또는 ' "package" = "..." ' 또는 ' "package" ' 형식 추출
                    match = re.search(r'^["\']?([a-zA-Z0-9\-_]+)["\']?[ \t]*=', line)
                    if match:
                        self.register_stack(match.group(1))
                    elif line.startswith('"') or line.startswith("'"):
                        # ' "package" ' 같이 리스트 형태인 경우
                        match = re.search(r'^["\']([a-zA-Z0-9\-_]+)["\']', line)
                        if match:
                            self.register_stack(match.group(1))

    def register_stack(self, pkg):
        pkg_lower = pkg.lower()
        
        # 블랙리스트 필터링 및 이름 길이 검사 (너무 짧거나 긴 것은 제외 가능성 높음)
        if pkg_lower in BLACKLIST or len(pkg_lower) < 2:
            return
            
        if pkg_lower in TEMPLATES:
            self.found_stacks[pkg_lower] = TEMPLATES[pkg_lower]
        else:
            # 템플릿에 없더라도 발견된 경우 등록하되, '천편일률적인 검색 결과'를 피하기 위해
            # 공식 문서가 없으면 github 검색 링크도 일단 비워둠 (사용자가 직접 정리가능하도록)
            # registry 링크는 어느정도 신뢰성이 있으므로 유지 (pypi/npm 구분 필요하나 현재는 pypi 기본)
            if pkg_lower not in self.found_stacks:
                self.found_stacks[pkg_lower] = {
                    "official": "", 
                    "github": "", # 검색 결과보다는 빈 칸이 나음 (오인 탐지 시 필터링 용이)
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

    def update_gitignore(self, script_root: Path):
        """방대한 기술 스택 문서들이 git repo를 오염시키지 않도록 .gitignore 동적 업데이트"""
        gitignore_path = script_root / ".gitignore"
        
        if gitignore_path.exists():
            content = gitignore_path.read_text(encoding="utf-8")
        else:
            content = (
                "# 1. Dynamic Config\nconfig/sources.json\n\n"
                "# 2. Python & Build\n.venv/\nlogs/\n__pycache__/\n*.py[cod]\nbuild/\ndist/\n*.egg-info/\n\n"
                "# 3. OS & System\n.DS_Store\nThumbs.db\n\n"
                "# 4. IDE settings\n.vscode/\n.idea/\n\n"
                "# 5. AI Agents\n.claude/\n.agents/\n.gemini/\n\n"
            )
            
        start_marker = "# --- AUTO-GENERATED TECH STACKS START ---"
        end_marker = "# --- AUTO-GENERATED TECH STACKS END ---"
        
        if start_marker in content and end_marker in content:
            before = content.split(start_marker)[0]
            after = content.split(end_marker)[1]
        else:
            before = content
            if not before.endswith("\n"):
                before += "\n"
            after = "\n"
            
        new_block = [start_marker]
        for name in sorted(self.found_stacks.keys()):
            new_block.append(f"docs/{name}/")
        new_block.append(end_marker)
        
        new_content = before + "\n".join(new_block) + after
        gitignore_path.write_text(new_content, encoding="utf-8")
        print(f"[+] Updated .gitignore with {len(self.found_stacks)} dynamically discovered stacks.")

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
    discoverer.update_gitignore(script_root)
    
    print(f"[*] Found {len(found)} stacks: {', '.join(found.keys())}")
    print("[!] Please review 'config/sources.json' and run 'start.bat' to sync documentation.")
