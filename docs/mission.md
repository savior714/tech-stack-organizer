# Mission

- **Objective:** 기술 스택 최신 지식 자동화 수집 프레임워크(`tech-stack-organizer`) 로직 일반화 및 플러그인화
- **Target:** 특정 비즈니스 종속성을 제거하고 공용 플러그인(Submodule) 형태로 다양한 프로젝트에 결합할 수 있는 지능형 데이터셋 템플릿 완성
- **Scope:** 
  1. `config/sources.json`을 단일/범용 구조로 초기화 (보일러플레이트 구조로 전환)
  2. 종속적인 비즈니스 도메인(Tauri, HIRA, HWP, Sentinel 등) 관련 파일 삭제
  3. `CRITICAL_LOGIC.md`를 범용 프레임워크 운영 규칙 기반으로 리팩토링
  4. 타 프로젝트에 연결할 수 있는 Plug-and-Play 방식으로 사용성 간소화
  5. `REASONING_PROMPT.md` 기반의 외부 LLM 협업 루틴 정립 (지식 심화 가속화)
  6. `discover-stack.py`를 통한 타겟 프로젝트 기술 스택 자동 탐지 엔진 구축
  7. 에이전트 설치 보고 및 사용자 승인(Accept) 프로토콜 표준화 (UX 고도화)
