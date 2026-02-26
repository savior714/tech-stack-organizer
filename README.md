# Tech Stack Organizer (Agentic Knowledge Plugin)

**Tech Stack Organizer**는 어떠한 프로젝트에도 Git Submodule 형태로 부착되어, 독립적이고 자동화된 **기술 스택 지식 베이스(Technical Knowledge Base)**를 제공하는 지능형 플러그인 프레임워크입니다.

이 도구는 단순한 문서 수집기를 넘어, 프로젝트의 의존성을 스스로 파악하고 LLM의 추론 능력을 결합하여 기술적 통찰을 실시간으로 자산화하는 **AI 에이전트 전용 지식 엔진**으로 동작합니다.

---

## 🚀 Key Features (핵심 기능)

1.  **Auto-Discovery (자동 탐지 엔진):**
    *   프로젝트 루트의 `requirements.txt`, `package.json`, `Cargo.toml` 등을 스캔하여 사용 중인 기술 스택을 자동으로 식별합니다.
    *   별도의 수동 설정 없이도 식별된 기술에 대한 최적화된 지식 수집 설정(`sources.json`)을 즉시 생성합니다.

2.  **5-Channel Automated Fetcher:**
    *   기술의 생애주기(Official Docs, GitHub Releases, Registry Status, Evolution Proposals, Best-Practice Curations)를 추적하는 5표준 채널 시스템을 통해 마크다운 기반의 최신 지식을 동기화합니다.
    *   **Fingerprint Validation:** MD5 해시 기반의 지문 비교를 통해 실제 내용 변화가 있는 경우에만 업데이트하는 멱등성(Idempotency)을 보장합니다.

3.  **Reasoning Loop (지능형 지식 심화):**
    *   `REASONING_PROMPT.md`를 활용하여 대규모 LLM(o1, GPT-4o 등)의 심층 분석 내용을 지식 베이스에 환류시킵니다.
    *   자동 수집의 한계를 외부 지능으로 보완하여, 단순 매뉴얼 이상의 '아키텍처 인사이트'를 확보합니다.

4.  **UX-Centered Interaction Protocol:**
    *   에이전트가 설치 직후 [탐지 결과 / 분석 리포트 / 승인 요청]으로 구성된 요약 리포트를 제출하고, 사용자의 승인 하에 실행되는 투명한 워크플로우를 제공합니다.

---

## 🤝 AI Agent Collaboration Protocol (에이전트 협업 규칙)

본 시스템을 운용하는 AI 에이전트들은 다음의 3대 원칙을 엄수해야 합니다.

1.  **Context Priority (컨텍스트 우선순위):** 모든 기술적 배경지식은 반드시 서브모듈의 `docs/` 폴더를 최우선으로 참조하십시오.
2.  **Generalization Strictness (일반화 엄수):** 본 플러그인 내에 특정 서비스 전용 비즈니스 로직을 포함하지 마십시오. 오직 '기술적 사실'과 '범용 패턴'만을 관리합니다.
3.  **Knowledge Loopback (지식 환류):** 문제 해결 과정에서 얻은 고부가가치 해결책은 반드시 `{stack}/error-solutions.md`에 기록하여 자산화하십시오.

---

## 📂 Domain Structure (도메인 구조)

저장소는 DDD(Domain-Driven Design) 원칙에 따라 명확히 계층화되어 있습니다.
-   **`docs/` (Knowledge Domain):** 자동 생성된 기술 문서와 시스템 운영 지침(`CRITICAL_LOGIC.md`)이 모이는 공간입니다.
-   **`patterns/` (Standard Domain):** 범용적인 설계 표준과 3-Layer 아키텍처 가이드라인이 정의됩니다.
-   **`tools/` (Automation Domain):** 자동 탐지(`discover-stack.py`) 및 수집(`update-docs.py`)을 담당하는 핵심 엔진입니다.
-   **`config/` (Configuration Domain):** 기술 스택별 추적 URL을 관리하는 제어 센터입니다.

---

## 🛠️ Usage (사용 방법)

1.  **설치:** 타겟 프로젝트에서 서브모듈로 추가합니다.
    ```powershell
    git submodule add [본 저장소 주소] .agents/tech-stack-organizer
    ```
2.  **가동:** 해당 폴더 진입 후 리포지토리의 `start.bat`을 실행합니다.
    *   최초 실행 시 의존성 파일을 분석하여 설정을 자동 구성합니다.
    *   에이전트의 요약 보고를 확인하고 문서 수집을 승인하십시오.

> **Note:** 본 프로젝트는 **Senior Full-stack Architect**의 페르소나를 가진 에이전트와 협업할 때 최대의 성능을 발휘하도록 최적화되어 있습니다.
