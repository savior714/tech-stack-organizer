# Mission: 설치 표준화 및 범용성 강화

## 목표
1. 설치 경로 불일치 문제 해결: `.agents/tech-stack-organizer`를 표준 경로로 강제.
2. `start.bat` 실행 에러 해결: `.venv` 존재 시 에러가 아닌 정상 활용하도록 로직 견고화.
3. 범용성 확장: 부모 프로젝트 루트 탐지 로직 개선 및 `pyproject.toml` 지원 추가.

## 작업 내역
- [x] `docs/mission.md`, `docs/context.md`, `docs/checklist.md` 생성
- [x] `start.bat` 로직 수정 (가상환경 체크 강화 및 무조건적 자동 탐지 실행)
- [x] `INSTALL_AGENT_PROMPT.md` 수정 (설치 경로 표준 규정 강화)
- [x] `README.md` 수정 (표준 경로 강조)
- [x] `tools/automation/bootstrap-rules.py` 수정 (경로 위반 탐지 및 경고 추가)
- [x] `tools/automation/discover-stack.py` 수술 (상위 루트 탐지 및 `pyproject.toml` 지원)
- [x] 시스템 안정성 검증 및 문서 동기화 테스트 완료
