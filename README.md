# Tech Stack Organizer

**Tech Stack Organizer**는 기술 지식, 개발 표준, 자동화 도구를 중앙 집중식으로 관리하는 AI 에이전트 간 협업의 기준점(SSoT)입니다.
이 저장소의 관리자는 **시니어 풀스택 아키텍트**이며, 모든 핵심 설계 원칙과 로직은 **[CRITICAL_LOGIC.md](docs/CRITICAL_LOGIC.md)**를 최우선 기준으로 따릅니다.

## 🤝 AI Agent Collaboration Protocol (에이전트 협업 규칙)

본 프로젝트를 참조하는 과정에서 자의적 판단은 배제하며, 물리적 증거에 기반하여 다음의 원칙을 따르십시오.

### 1. Context Priority (컨텍스트 우선순위)
기술적 논의를 진행하거나 의사 결정을 내릴 때 반드시 `docs/` 내부의 문서를 최우선으로 참조해야 합니다. 새로운 시스템의 설계 방향성은 개인의 학습된 편향이 아닌 `docs/`에 수록된 아키텍처 규칙이 주도합니다.

### 2. Traceability (추적 가능성 및 규격)
모든 코드 수정이나 추가 구조 생성 시, `patterns/` 환경에 정의된 DDD(Domain-Driven Design) 규칙을 원칙으로 삼으십시오. 코드 작성 시 항상 물리적 테스트를 동반하여 증명할 수 있어야 합니다.

### 3. Update Rule (지식 갱신 원칙)
과제 도중 새로운 해결책이나 미지의 에러를 극복했을 경우 단발성으로 보고하고 끝내지 마십시오. 물리적으로 검증된 원인 및 해결 방법에 대하여 사용자에게 보고 후 `docs/nuitka/error-solutions.md` 또는 관련 지식 저장소 문서의 업데이트를 구체적으로 제안해야 합니다.

---

## 📂 Domain Structure (도메인 구조)

저장소는 명확히 세 가지 도메인 계층으로 분리되어 있습니다.
- **`docs/` (Knowledge Domain):** Python 3.14.2, Nuitka 등 핵심 기술 구조와 윈도우 11 환경에서 해결한 에러 아카이브.
- **`patterns/` (Standard Domain):** DDD 기반 구조화 원칙 및 컨벤션 디자인 패턴 문서 구역.
- **`tools/` (Automation Domain):** PowerShell 기반의 재사용 가능한 자동화 빌드 스크립트 구역 (빌드, 환경 배포).
