# 아키텍처 및 코딩 표준 (DDD & Architecture Standards)

[System-Context]
- Framework: Next.js (App Router), FastAPI, or Generic Python
- Pattern: Domain-Driven Design (DDD)
- Philosophy: SSOT (Single Source of Truth), Separation of Concerns

## 1. Directory Structure (3-Layer Pattern)

모든 도메인 로직은 다음의 3계층 구조를 엄격히 준수해야 합니다. 에이전트는 새로운 기능을 추가할 때 이 구조를 벗어나는 위치에 파일을 생성해서는 안 됩니다.

### **계층 1: Definition (도메인 정의)**
- **역할:** 비즈니스 엔티티, 인터페이스(Interface), 타입 정의, 상수.
- **특징:** 외부 의존성(DB, API)이 없어야 하며 순수한 비즈니스 규칙만 포함합니다.

### **계층 2: Repository (데이터 접근)**
- **역할:** 데이터베이스 CRUD, 외부 API 통신.
- **특징:** 도메인 엔티티를 영속화하거나 외부 데이터를 가져오는 기술적 세부 사항을 다룹니다.

### **계층 3: Service/Logic (비즈니스 실행)**
- **역할:** 어플리케이션 흐름 제어, 복합 엔티티 간의 논리 수행.
- **특징:** Definition과 Repository를 조합하여 사용자 요구사항을 완성합니다.

---

## 2. Naming Conventions (명명 규칙)

- **Variables/Functions:** `snake_case` (Python), `camelCase` (JS/TS)
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private Members:** `_` 프리픽스 사용 (예: `_internal_method`)

---

## 3. Implementation Rules

1. **Async First:** 모든 I/O 작업(Network, DB)은 반드시 `async/await`를 사용합니다.
2. **Strict Type Hinting:** Python의 경우 `typing` 모듈을 통한 엄격한 타입 힌팅을 강제합니다.
3. **SSOT Sync:** 비즈니스 핵심 로직의 변경이 발생하면 반드시 `docs/CRITICAL_LOGIC.md`를 최신화해야 합니다.
4. **Error Handling:** 단순히 `try-except`로 뭉뚱그리지 않고, 도메인별 Custom Exception을 정의하여 처리합니다.
