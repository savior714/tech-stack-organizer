# Tech-Stack-Organizer Development Memory

## [Context]
The user reported that the Tech-Stack-Organizer failed to detect the tech stack in parent projects when installed as a submodule. The root cause was identified as incorrect root path detection (stopping at the submodule's own root) and missing `pyproject.toml` support for modern `uv`-based projects.

## [Action]
1.  Read `CRITICAL_LOGIC.md` to understand the system core.
2.  Verified that `tools/automation/discover-stack.py` and `start.bat` in the current repo do not yet have the proposed fixes.
3.  Implementing the "Surgical Repair" reported by the user to ensure universal compatibility.

## [Status]
In Progress: Applying fixes to `discover-stack.py` and `start.bat`.

## [Technical Note]
- Root detection must climb up parents searching for `.git` or `.hg` or other project markers, but should prioritize the main project root over the submodule's root.
- `pyproject.toml` parsing is essential for `uv` and `poetry` support.
- Force-running discovery in `start.bat` ensures that `sources.json` is always up-to-date with new dependencies.
[Action] Modified tools/automation/discover-stack.py with pyproject.toml support and enhanced root detection. Refactored start.bat to unconditionally run auto-discovery. Updated tech stack templates. 
 [Status] Completed fixes. 
 [Technical Note] Successfully integrated the reported surgical repair. Docs synchronization is now more robust across nested project structures.
[Action] Upgraded StackDiscoverer to perform a deep recursive scan using os.walk across the entire project tree. 
 [Status] Completed: The system now detects dependencies in nested folders while intelligently skipping .venv, 
ode_modules, and .agents to avoid noise and self-detection. 
 [Technical Note] Root detection logic successfully differentiates between submodule .git files and master project .git directories, ensuring the scan always starts from the true project root. Added universal registration for all found packages even without templates.

## [Context]
작업 완료 및 전체 문서 동기화, Git 푸시 요청 수신.

## [Action]
1. docs/mission.md, docs/checklist.md, docs/context.md 상태 확인 및 최신 작업 내용 반영 여부 검증.
2. docs/handoff_current.md에 discover-stack.py 수술 내역 및 범용 탐지 로직 개선 사항 반영.
3. 수정된 모든 파일(start.bat, discover-stack.py, docs/*) 스테이징 및 커밋.
4. 원격 저장소(origin/main)로 푸시 완료.

## [Status]
Completed: 모든 변경 사항이 문서에 정리되었고 Git에 동기화됨.

## [Technical Note]
- docs/handoff_current.md는 에이전트 간 연속성 보장을 위한 핵심 문서이므로, 수정 파일 목록에 discover-stack.py를 명시적으로 추가함.
- docs/memory.md는 Append-only 규칙을 준수하여 이력을 보존함.

## [Context]
사용자의 요청에 따라 루트 README.md 파일의 내용을 보강하고 가독성을 개선하는 작업 착수.

## [Action]
1. 기존 README.md 내용 분석 및 개선 방향 수립 (Mermaid 다이어그램 추가, 섹션 재구성, 인간 친화적 설명 보강).
2. 새로운 README.md 내용 작성 및 적용.
3. 작업 완료 후 Git Push 실행 예정.

## [Status]
In-Progress: README.md 내용 개선 중.

## [Context]
README.md 개선 완료 및 Git Pus 작업 대기 중.

## [Action]
1. README.md 파일의 물리적 보존 상태 확인.
2. `git add .`, `git commit -m "docs: improve README.md readability and content"`, `git push origin main` 명령 실행.

## [Status]
Completed: README.md 개선 완료 및 원격 저장소 동기화 완료.

## [Technical Note]
- Mermaid 다이어그램을 활용하여 시스템 가시성을 높임.
- 인간 사용자와 AI 에이전트 양쪽 모두에게 유용한 정보를 계층적으로 배치함.
- docs/memory.md 현재 줄 수: 68/200.


