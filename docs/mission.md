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
  8. 수집 완료 후 '비즈니스 솔루션 제안' 2차 승인 루틴 추가
  9. **[Atomic Operations]:** 모든 작업은 `docs/checklist.md`에 정의된 1회 출력 단위로 분할 실행.
  10. **[Context Handoff]:** 컨텍스트 포화 시 `docs/handoff_current.md`를 통해 새 대화로 즉시 전환 가능한 프롬프트 생성.

---

## Operational Protocol (Option 1)
- **Single Step per Turn:** 한 번의 응답에 오직 하나의 checklist 항목만 완료함.
- **Physical Evidence First:** 모든 작업 완료 후 반드시 명령어를 통해 결과를 검증함.
- **JIT Handoff:** 사용자가 요청하거나 컨텍스트가 80% 이상 차오르면 즉시 인수인계 프롬프트 준비.
