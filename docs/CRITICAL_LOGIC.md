# CRITICAL LOGIC (Universal System Core)

본 문서는 **Tech Stack Organizer Framework**의 구동 원리와 운영 규칙을 정의하는 최상위 SSoT(Single Source of Truth)입니다. 본 프로젝트는 특정 서비스에 종속되지 않는 범용적인 지식 자동화 플러그인을 지향합니다.

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
1. **5-Channel Discovery:** 기술의 생애주기(기획-개발-배포-운영-트렌드)를 추적하는 5대 표준 채널 수집.
2. **Jina-Markdown Transformation:** 외부 웹 콘텐츠를 LLM 인덱싱에 최적화된 마크다운으로 변환.
3. **Fingerprint Validation:** MD5 해시 기반의 지문 비교를 통해, 실제 내용 변화가 있는 경우에만 파일을 업데이트하는 증분식 관리(Idempotency).

### **B. Universal Update Flow**
- 새로운 기술 스택을 도입하고자 할 때, 사용자는 오직 `config/sources.json`에 URL 한 줄을 추가하고 `start.bat`을 실행하는 것만으로 프로젝트의 지식 베이스를 확장할 수 있다.

---

## 4. 운영 및 협업 가이드 (Governance)
1. **Separation of Content:** 본 저장소에는 특정 서비스의 비즈니스 로직을 담지 않으며, 오직 기술적 사실(Technical Facts)과 공통 패턴만을 관리한다.
2. **Standard Compliance:** 모든 자동화 스크립트와 가이드는 `patterns/`에 정의된 설계 표준을 최우선으로 준수한다.
3. **Manual Override:** 자동 수집된 문서 외에 중요한 트러블슈팅 사례는 `{stack}/error-solutions.md` 폴더를 통해 수동으로 보완할 것을 권장한다.
