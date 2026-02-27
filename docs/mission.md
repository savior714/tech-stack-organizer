# Mission: 설치 표준화 및 실행 안정성 강화

## 목표
1. 설치 경로 불일치 문제 해결: `.agents/tech-stack-organizer`를 표준 경로로 강제.
2. `start.bat` 실행 에러 해결: `.venv` 존재 시 에러가 아닌 정상 활용하도록 로직 견고화.

## 작업 내역
- [ ] `docs/mission.md`, `docs/context.md`, `docs/checklist.md` 생성
- [ ] `start.bat` 로직 수정 (가상환경 체크 강화)
- [ ] `INSTALL_AGENT_PROMPT.md` 수정 (설치 경로 표준 규정 강화)
- [ ] `README.md` 수정 (표준 경로 강조)
- [ ] `tools/automation/bootstrap-rules.py` 수정 (경로 위반 탐지 및 경고 추가)
