# Tech Stack Organizer (Agentic Knowledge Plugin)

**Tech Stack Organizer**는 어떠한 프로젝트에도 Git Submodule 형태로 부착되어, 독립적이고 자동화된 **기술 스택 지식 베이스(Technical Knowledge Base)**를 제공하는 플러그인 프레임워크입니다.
이 저장소는 특정 비즈니스 로직을 전혀 포함하지 않으며, 오직 대상 프로젝트의 기술 스택을 동기화하고 관리하는 **자동화 파이프라인 엔진**으로만 동작합니다.

---

## 🚀 Plugin Features (핵심 기능)

1. **Plug-and-Play 구조:** `config/sources.json` 파일에 추적할 기술 스택URL만 입력하면, 프로젝트 전용 맞춤형 SSoT(Single Source of Truth)가 즉시 생성됩니다.
2. **Automated Doc-Fetcher:** 5대 채널(Official, GitHub, Registry, Proposals, Curation)을 실시간 추적하여, 에이전트가 읽기 편한 마크다운 문서로 변환 저장 및 증분(Fingerprint) 업데이트 수행.
3. **Agent-Ready Data:** 생성된 모든 `docs/` 파일들은 AI 에이전트(Cursor, Antigravity 등)가 컨텍스트로 쉽게 소화할 수 있는 LLM 친화적 구조를 가집니다.

---

## 🤝 AI Agent Collaboration Protocol (에이전트 협업 규칙)

본 플러그인을 참조하는 과정에서 AI 에이전트들은 다음의 규칙을 엄수해야 합니다:

### 1. Context Priority (컨텍스트 우선순위)
본 저장소 내부의 `docs/CRITICAL_LOGIC.md`가 모든 시스템의 최상단 헌법 역할을 설계합니다. 프로젝트의 아키텍처나 구조를 파악하려면 반드시 해당 문서를 기준으로 삼으십시오.

### 2. Generalization Strictness (일반화 엄수)
본 프로젝트 내부에 특정 서비스(예: 특정 앱 이름, 특화된 비즈니스 용어 등)의 코드를 추가하는 행위를 완전히 금지합니다. 모든 아키텍처 문서는 **'범용성(Universal)'**을 해치지 않게 작성되어야 합니다.

### 3. Verification First (물리적 증명 우선)
Doc-Fetcher나 빌드 파이프라인의 코드를 수정할 때는 주관적 예상이 아닌, 로그를 통한 터미널 출력 및 파일 검사(물리적 검증) 결과를 바탕으로 작업 완수 여부를 보고해야 합니다.

---

## 📂 Domain Structure (도메인 구조)

저장소는 명확히 세 가지 도메인 계층으로 분리되어 격리성을 유지합니다:
- **`docs/` (Knowledge Domain):** `update-docs.py` 로직에 의해 생성되는 기술 문서와 플러그인 자체 운영 지침서가 모이는 SSoT 저장소입니다.
- **`patterns/` (Standard Domain):** 프로젝트의 공통 설계 표준과 스타일 가이드(로깅, 에러 핸들링 등)가 구조화되는 공간입니다.
- **`tools/` (Automation Domain):** Jina API 등 외부 프로토콜과 연동하여 문서 갱신과 자동화를 이끄는 플러그인의 '엔진' 스크립트들이 상주합니다.

> **시작 방법:** 터미널에서 `.\start.bat`를 실행하면 즉시 환경 구축과 지식 다운로드가 시작됩니다.
