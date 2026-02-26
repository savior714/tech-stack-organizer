# CRITICAL LOGIC (진실의 원천 - SSOT)

본 문서는 `tech-stack-organizer` 프로젝트의 설계 철학, 핵심 아키텍처, 그리고 기술적 구동 로직을 총망라하는 **최상위 지침서**입니다. 모든 AI 에이전트는 프로젝트를 수정하거나 확장하기 전, 이 문서에 명시된 논리를 최우선으로 이해하고 준수해야 합니다.

---

## 1. 프로젝트 목적 및 철학 (Core Philosophy)
- **목적:** AI 에이전트와 시니어 아키텍트가 공유하는 **중앙 집중형 기술 지식 베이스(Technical Knowledge Base)** 구축.
- **철학:** 
  - **SSoT (Single Source of Truth):** 기술적 결정의 모든 근거는 `docs/` 내부에 물리적 마크다운 형태로 저장된다.
  - **Automation First:** 수동 지식 업데이트를 배제하고, 자동화된 파이프라인(Doc-Fetcher)을 통해 최신성을 유지한다.
  - **Agent-Centric:** AI 에이전트가 즉시 인덱싱하고 코드에 반영할 수 있도록 모든 문서는 LLM 친화적인 마크다운 형식을 유지한다.

---

## 2. 도메인 아키텍처 (DDD Structure)
프로젝트는 관심사 분리를 위해 세 가지 핵심 도메인으로 격리되어 있습니다.

### **[Knowledge Domain] `/docs`**
- **역할:** 기술적 사실(Facts)과 에러 해결책 아카이브.
- **핵심 파일:**
  - `CRITICAL_LOGIC.md`: 현재 읽고 있는 이 문서. 프로젝트의 뇌 역할을 수행.
  - `/nuitka/optimization-guide.md`: Nuitka 빌드 정체 및 최적화 규칙.
  - `/python-3.14.2/`: 파이썬 최신 바이트코드 변화 및 호환성 가이드.

### **[Standard Domain] `/patterns`**
- **역할:** "어떻게 코드를 작성할 것인가"에 대한 헌법.
- **핵심 파일:**
  - `architecture-standard.md`: 3-Layer(Definition, Repository, Service) DDD 패턴 및 명명 규칙 명세.

### **[Automation Domain] `/tools`**
- **역할:** 지식 수집 및 빌드 프로세스의 실질적 이행.
- **핵심 파일:**
  - `automation/update-docs.py`: 5대 채널(공식, GitHub, 레지스트리 등) 통합 수집 엔진.
  - `build/nuitka-build.ps1`: Windows 11 권한 최적화 빌드 자동화 스크립트.

---

## 3. 핵심 구동 로직 (Core Logic)

### **A. Doc-Fetcher: 지능형 문서 동기화 로직**
1. **추출 전략:** `Jina Reader API`를 사용하여 HTML을 마크다운으로 실시간 변환.
2. **채널 다각화:** 5대 채널(Official, GitHub, Registry, Proposals, Curation)을 통해 기술의 생애 주기를 추적.
3. **멱등성(Idempotency) 보장:** 본문의 공백을 제거한 순수 텍스트의 `MD5 해시`를 계산하여 `Fingerprint` 생성. 기존 파일 내 지문과 대조하여 실제 내용이 변했을 때만 업데이트 수행.

### **B. Nuitka-Build: 윈도우 11 최적화 빌드 로직**
1. **환경 검증:** Python 3.14.2 버전 여부를 엄격히 체크.
2. **권한 제어:** `--windows-uac-admin` 옵션을 포함하여 실행 파일의 권한 충돌 방지.
3. **가시성 확보:** 빌드 정체 구간(90% 분석 등) 파악을 위해 `--show-progress`, `--show-memory` 강제 활성화.

---

## 4. 에이전트 협업 수칙 (Agent Protocol)
1. **보고 의무:** 새로운 기술적 해결책 발견 시, 반드시 `docs/nuitka/error-solutions.md`에 업데이트를 제안할 것.
2. **검증 의무:** 모든 빌드 결과는 `tools/build` 스크립트의 물리적 출력 수치(n/m)로 보고할 것.
3. **동기화 의무:** 로직 수정 시, 반드시 이 `CRITICAL_LOGIC.md`와의 일치 여부를 상호 검증할 것.

---

## 5. 기술 스택 (Tech Stack)
- **Runtime:** Python 3.14.2 (64-bit)
- **Shell:** PowerShell 7 (pwsh)
- **OS:** Windows 11 Native
- **Libraries:** `httpx` (Async I/O), `hashlib` (Idempotency Checking)
