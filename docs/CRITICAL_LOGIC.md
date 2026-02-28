# CRITICAL LOGIC (Universal System Core)

본 문서는 **Tech Stack Organizer Framework**의 구동 원리와 운영 규칙을 정의하는 최상위 SSoT(Single Source of Truth)입니다.
4. 타 프로젝트에 연결할 수 있는 Plug-and-Play 방식으로 사용성 간소화
5. `REASONING_PROMPT.md` 기반의 외부 LLM 협업 루틴 정립 (지식 심화 가속화)
6. `discover-stack.py`를 통한 타겟 프로젝트 기술 스택 자동 탐지 엔진 구축
7. 에이전트 설치 보고 및 사용자 승인(Accept) 프로토콜 표준화 (UX 고도화)
8. 수집 완료 후 '비즈니스 솔루션 제안' 2차 승인 루틴 추가
본 프로젝트는 특정 서비스에 종속되지 않는 범용적인 지식 자동화 플러그인을 지향합니다.

---

## 1. 프레임워크 설계 철학 (Architecture Philosophy)
- **Plugin-Ready Architecture:** 어떤 프로젝트에도 서브모듈(Submodule)로 연동되어 기술 스택별 최신 인텔리전스를 제공한다.
- **Knowledge-As-A-Code:** 지식은 단순한 텍스트가 아니라, 자동화된 파이프라인(`tools/`)과 설정(`config/`)을 통해 관리되는 코드처럼 취급된다.
- **Agent-Friendly Interface:** AI 에이전트가 별도의 학습 없이도 `docs/` 트리를 읽는 것만으로 현재 프로젝트의 기술적 배경지식을 100% 확보할 수 있게 한다.

---

## 2. 도메인 구조 (Domain Breakdown)
프라이머리 프로젝트는 DDD(Domain-Driven Design)를 기반으로 도메인이 격리되어 있습니다.

### **[Knowledge Domain] `/docs`**
- **역할:** 자동화 엔진에 의해 수립된 최신 기술 데이터와 공통 가이드(Nuitka 최적화 등) 저장.
- **주요 파일:**
  - `CRITICAL_LOGIC.md`: 시스템의 핵심 구동 규칙 (현재 문서).
  - `{stack}/`: 각 기술 스택별 자동 생성된 마크다운 문서들.
  - `{stack}/error-solutions.md`: 해결된 트러블슈팅 사례 기록.

### **[Standard Domain] `/patterns`**
- **역할:** 범용적인 설계 표준과 코드 스타일 가이드라인 제공.
- **주요 파일:**
  - `architecture-standard.md`: 확장 가능한 3-Layer(Definition, Repository, Service) 패턴 명세.

### **[Automation Domain] `/tools`**
- **역할:** 기술 데이터 수집 및 공통 빌드 자동화를 위한 비즈니스 로직.
- **주요 파일:**
  - `automation/update-docs.py`: 5대 채널(Official, GitHub, Registry, Proposals, Curation) 통합 수집 엔진.
  - `start.bat`: 가상환경 및 수집 파이프라인 통합 실행기.

---

## 3. 핵심 기능 동작 원리 (Core Framework Logic)

### **A. Doc-Fetcher: 지능형 지식 동기화**
0. **Auto-Discovery:** `tools/automation/discover-stack.py`가 부모 프로젝트의 의존성 파일(requirements.txt, package.json, pyproject.toml 등)을 스캔하여 기술 스택을 자동 탐지한다.
1. **5-Channel Discovery:** 탐지된 기술의 생애주기(기획-개발-배포-운영-트렌드)를 추적하는 5대 표준 채널 수집.
2. **Jina-Markdown Transformation:** 외부 웹 콘텐츠를 LLM 인덱싱에 최적화된 마크다운으로 변환.
3. **Fingerprint Validation:** MD5 해시 기반의 지문 비교를 통해, 실제 내용 변화가 있는 경우에만 파일을 업데이트하는 증분식 관리(Idempotency).

### **B. Universal Update Flow**
- 새로운 기술 스택을 도입하고자 할 때, 사용자는 오직 `config/sources.json`에 URL 한 줄을 추가하고 `start.bat`을 실행하는 것만으로 프로젝트의 지식 베이스를 확장할 수 있다.
  - 범용 파이프라인의 완성도를 높여, `config/sources.json`만 갈아끼우면 어떤 앱의 기술 스택이든 문서화할 수 있는 준비 완료.
### **C. Reasoning Loop (GenAI Collaboration)**
- `REASONING_PROMPT.md`를 통한 'Reasoning Loop' 워크플로우를 추가하여 자동 수집의 한계를 외부 지능으로 보완하는 구조 확립.
- `tools/automation/discover-stack.py` 추가를 통해 수동 설정 없이도 프로젝트 기술 스택을 자동 식별하고 `sources.json`을 생성하는 기능 구현.

### **D. Agent-User Interaction Protocol (2-Stage Approval UX)**
1. **Initial Report & 1st Approval:** 설치 직후 탐지된 스택을 보고하고 '문서 수집(Collection)'에 대한 승인을 받는다.
2. **Sync Report & 2nd Approval:** 수집 완료 후, 동기화된 지식을 기반으로 '문제 해결 분석(Solution Delivery)' 단계로 진입할지 승인을 받는다.
### **E. Just-In-Time (JIT) Troubleshooting Protocol**
개발 중 다음과 같은 **4가지 JIT(Just-In-Time) 트리거 상황**이 발생하면, 에이전트는 즉시 관련 스택을 업데이트(`update-docs.py --stacks [target]`)해야 한다.

1. **기술적 로드블록:** 라이브러리가 예상과 다르게 동작하거나 해결 불가능한 에러 발생 시.
2. **지식 부재:** 새로운 기술 스택이 도입되었으나 `docs/` 내에 관련 문서가 없을 시.
3. **지식 노후화:** 기존 문서의 `Last-Updated`가 오래되었거나 현재 프로젝트 버전과 불일치할 시.
4. **고정밀 팩트체크:** 아키텍처나 보안 등 틀리면 치명적인 의사결정이 필요할 시.

**실행 절차:**
1. **JIT 업데이트:** 상황 감지 시 타겟 스택의 최신 데이터를 즉시 동기화한다.
2. **근거 중심 제안:** 수집된 최신 문서 내용을 요약 보고하고, '팩트 기반' 해결책을 제안한다.
3. **사례 저장:** 해결된 데이터는 `error-solutions.md`에 기록하여 지식 자산화한다.

---

## 4. 운영 및 협업 가이드 (Governance)
1. **Separation of Content:** 본 저장소에는 특정 서비스의 비즈니스 로직을 담지 않으며, 오직 기술적 사실(Technical Facts)과 공통 패턴만을 관리한다.
2. **Standard Compliance:** 모든 자동화 스크립트와 가이드는 `patterns/`에 정의된 설계 표준을 최우선으로 준수한다.
3. **Manual Override:** 자동 수집된 문서 외에 중요한 트러블슈팅 사례는 `{stack}/error-solutions.md` 폴더를 통해 수동으로 보완할 것을 권장한다.

---

## 5. 설치 및 운영 표준 (Deployment & Operation Standards)

### **A. 설치 경로 표준(Standard Path Strategy)**
- **MANDATORY PATH:** `.agents/tech-stack-organizer`
- **관리 철칙:** 관리 효율성과 에이전트 간 협업을 위해 반드시 표준 경로를 준수해야 한다. 루트, `external/`, `.knowledge/` 등 임의의 경로에 설치하는 것은 기술 부채로 간주하며, `bootstrap-rules.py` 실행 시 자동 탐지하여 경고를 출력한다.

### **B. 실행 안정성 및 가상환경(Virtual Environment Strategy)**
- **실행기:** `start.bat` (Windows PowerShell 기반 가동)
- **가상환경 정책:**
  - `uv`를 활용한 `.venv` 환경을 강제한다.
  - **Re-use Priority:** 가상환경 폴더가 이미 존재할 경우, 단순 존재 여부가 아닌 내부 실행 파일(`.venv\Scripts\python.exe`)의 유효성을 검증하여 최대한 재사용한다.
  - **Self-Healing:** 폴더는 존재하나 내부 파일이 파괴된 경우, 자동으로 기존 폴더를 삭제하고 재생성(Clean-Install)을 시도한다.
- **언어 및 인코딩:** 배치 파일 파싱 오류 및 한글 깨짐 방지를 위해 모든 터미널 출력은 **영어(English)**를 원칙으로 하며, ANSI(CP949) 혹은 UTF-8(No BOM) 인코딩을 엄수한다.
