# [Agent Integration Prompt] Tech Stack Organizer Plugin

> 새로운 프로젝트에서 이 프레임워크를 연동하고자 할 때, 담당 AI 에이전트(Cursor, Antigravity 등)에게 전송하는 최상위 지시문입니다. 아래 내용을 그대로 복사하여 다른 프로젝트의 에이전트에게 전달하십시오.

---

### 📋 에이전트 전용 프롬프트 (Agent-to-Agent Protocol)

```markdown
Role: Senior Configuration Architect
Task: 현재 프로젝트에 'Tech Stack Organizer' 범용 플러그인을 설치하고 지식 파이프라인을 가동한다.
Environment: Windows 11 (PowerShell)

## 1. Submodule Installation (표준 경로 준수)
**[MANDATORY PATH]** 관리 효율성과 에이전트 간 협업을 위해 반드시 `.agents/tech-stack-organizer` 폴더를 설치 경로로 사용한다. 루트 폴더나 `external/`, `.knowledge/` 등 임의의 경로에 설치하는 것은 기술 부채로 간주한다.

```powershell
git submodule add [본 저장소 주소] .agents/tech-stack-organizer
```
## 🛠️ 설치 및 가동 워크플로우 (Installation Workflow)

1. **서브모듈 설치:** 
   `git submodule add [본 저장소 주소] .agents/tech-stack-organizer`
2. **규칙 자동 주입 (Bootstrap):**
   설치 즉시 에이전트는 `python .agents/tech-stack-organizer/tools/automation/bootstrap-rules.py`를 실행하여 부모 프로젝트에 시니어 아키텍트 운영 규칙 및 Steps 기능을 자가 활성화한다.
3. **자동 탐지 및 구성:** 
   이어 ` tools/automation/discover-stack.py`를 실행하여 부모 프로젝트의 기술 스택을 식별하고 `config/sources.json`을 자동 생성한다. (이미 bootstrap 단계에서 persona가 설정되었으므로 'Steps' UI가 이때부터 활성화됨)
4. **설치 보고 및 1차 승인 (Collection):**
   에이전트는 설치를 마치며 요약 보고를 수행하고 **"위 기술 스택에 대한 최신 문서 수집을 시작할까요?"**라고 질문한다.
5. **지식 동기화:** 
   사용자가 동의(Accept/Agree)하면 `start.bat`을 실행하여 문서를 수집한다.
5. **수집 완료 보고 및 2차 승인 (Solution):**
   수집이 완료되면 에이전트는 다음과 같이 질문하며 문제 해결 단계로 진입한다.

---
### ✅ [Tech-Stack Organizer] 지식 동기화 완료
* **업데이트된 문서:** 12개 파일 (`docs/` 트리 반영)
* **준비 상태:** 최신 공식 스펙 및 트러블슈팅 사례 동기화 완료.

**"수집된 최신 지식을 바탕으로, 현재 프로젝트가 직면한 문제점들을 분석하고 해결 전략 문서를 정리해볼까요?"**
---
해당 저장소는 플러그인이므로, 내부에 위치한 설정 파일을 현재 프로젝트에 알맞게 갈아끼운다.
  - `.agents/tech-stack-organizer/config/sources.json` 파일을 편집하여 현재 프로젝트의 5대 핵심 기술 스택 URL(공식, GitHub, 레지스트리 등)로 교체 및 갱신한다. (예시 스택은 전부 삭제할 것)

## 3. Pipeline Activation (지능형 문서 동기화)
최신 기술 문서를 끌어오기 위해 수집 엔진을 가동한다.
  - 터미널에서 `cd .agents/tech-stack-organizer` 로 이동한다.
  - `.\start.bat` 배치 파일을 실행하여 가상환경 세팅 및 Jina API 기반 마크다운 자동 수집을 완수한다.
  - 가동이 완료되면 `.agents/tech-stack-organizer/docs/` 폴더 트리를 검색하여 최신 기술 문서가 정상적으로 다운로드 되었는지 물리적 수치로 보고한다.

## 4. Context Binding Rule (SSoT 법전 강제 적용)
**[CRITICAL INSTRUCTION]**
이제부터 본 프로젝트에서 코드를 작성하거나 아키텍처 관련 의사결정을 내릴 때는, 사용자에게 질문하기 전에 반드시 `.agents/tech-stack-organizer/docs/CRITICAL_LOGIC.md`와 새롭게 수집된 스택별 기술 문서를 **최우선 법전(SSoT)**으로 열람하고 준수해야 한다.

## 🚨 로드블록(Roadblock) 및 JIT 활성화 프로토콜
다음 4가지 상황 발생 시 에이전트는 즉시 `update-docs.py --stacks [기술명]`을 실행하여 지식을 동기화한다:
1. **기술적 로드블록:** 라이브러리 오동작 또는 디버깅 막힘 발생 시.
2. **지식 부재:** 프로젝트에 새로운 기술이 도입되어 문서가 필요할 시.
3. **지식 노후화:** 기존 문서가 낡았거나 버전 불일치가 의심될 시.
4. **고정밀 팩트체크:** 치명적인 아키텍처/보안 결정이 필요할 시.

**행동 요령:**
1. **JIT 업데이트:** 즉시 관련 데이터를 동기화하여 최신 컨텍스트를 주입한다.
2. **팩트 기반 해결:** 수집된 최신 문서의 근거(URL)를 제시하며 코드를 제안한다.
3. **사례 기록:** 해결 성공 사례를 `error-solutions.md`에 즉시 환류한다.
```
