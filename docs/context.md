# Context Snapshot

- **Branch:** main
- **Current State:** 비즈니스 로직(cheonggu) 종속성 제거 및 범용 플러그인 형태로 프레임워크 일반화(Generalization) 완료.
- **Latest Change:** `docs/CRITICAL_LOGIC.md`, `config/sources.json` 및 `docs/mission.md` 갱신을 통해 특정 프로젝트의 그림자를 제거함.
- **Key Decisions:**
  - 본 프레임워크를 다른 프로젝트(예: `cheonggu`)에서 Submodule 형태로 사용할 수 있도록, 내부에는 오직 기술적 지식 정보 수집 플러그인 로직(`update-docs.py` 및 `start.bat`)만 남김.
  - SSoT 문서(`CRITICAL_LOGIC.md`) 역시 '프레임워크 사용법'에 초점을 맞추도록 변경.
  - 범용 파이프라인의 완성도를 높여, `config/sources.json`만 갈아끼우면 어떤 앱의 기술 스택이든 문서화할 수 있는 준비 완료.
  - `REASONING_PROMPT.md`를 통한 'Reasoning Loop' 워크플로우를 추가하여 자동 수집의 한계를 외부 지능으로 보완하는 구조 확립.
  - `tools/automation/discover-stack.py` 추가를 통해 수동 설정 없이도 프로젝트 기술 스택을 자동 식별하고 `sources.json`을 생성하는 기능 구현.
  - 에이전트 설치 직후 분석 리포트 제출 및 사용자 승인을 받는 'UX 프로토콜'을 `INSTALL_AGENT_PROMPT.md`에 통합 완료.
  - 지식 수집 완료 후 '문제 해결 전략 제안'으로 연결되는 2단계 승인 파이프라인 정립.
  - **[Phase 2 완료]:** LLM의 컨텍스트 포화 및 토큰 초과 문제를 해결하기 위한 원자적(Atomic) 작업 모델(`1 Turn = 1 Task`)과 `handoff_current.md` 기반의 새 대화창 인수인계 프로토콜 구축 완료.
