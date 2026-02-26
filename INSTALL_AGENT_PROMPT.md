# [Agent Integration Prompt] Tech Stack Organizer Plugin

> 새로운 프로젝트에서 이 프레임워크를 연동하고자 할 때, 담당 AI 에이전트(Cursor, Antigravity 등)에게 전송하는 최상위 지시문입니다. 아래 내용을 그대로 복사하여 다른 프로젝트의 에이전트에게 전달하십시오.

---

### 📋 에이전트 전용 프롬프트 (Agent-to-Agent Protocol)

```markdown
Role: Senior Configuration Architect
Task: 현재 프로젝트에 'Tech Stack Organizer' 범용 플러그인을 설치하고 지식 파이프라인을 가동한다.
Environment: Windows 11 (PowerShell)

## 1. Submodule Installation (플러그인 부착)
본 프로젝트의 비즈니스 로직과 섞이지 않도록 `knowledge/` 폴더에 서브모듈로 플러그인을 부착한다.
## 🛠️ 설치 및 가동 워크플로우 (Installation Workflow)

1. **서브모듈 설치:** 
   `git submodule add [본 저장소 주소] .agents/tech-stack-organizer`
2. **자동 탐지 및 구성:** 
   설치 직후 에이전트는 `tools/automation/discover-stack.py`를 실행하여 부모 프로젝트의 기술 스택을 식별하고 `config/sources.json`을 자동 생성한다.
3. **설치 보고 및 1차 승인 (Collection):**
   에이전트는 설치를 마치며 요약 보고를 수행하고 **"위 기술 스택에 대한 최신 문서 수집을 시작할까요?"**라고 질문한다.
4. **지식 동기화:** 
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
  - `knowledge/config/sources.json` 파일을 편집하여 현재 프로젝트의 5대 핵심 기술 스택 URL(공식, GitHub, 레지스트리 등)로 교체 및 갱신한다. (예시 스택은 전부 삭제할 것)

## 3. Pipeline Activation (지능형 문서 동기화)
최신 기술 문서를 끌어오기 위해 수집 엔진을 가동한다.
  - 터미널에서 `cd knowledge` 로 이동한다.
  - `.\start.bat` 배치 파일을 실행하여 가상환경 세팅 및 Jina API 기반 마크다운 자동 수집을 완수한다.
  - 가동이 완료되면 `knowledge/docs/` 폴더 트리를 검색하여 최신 기술 문서가 정상적으로 다운로드 되었는지 물리적 수치로 보고한다.

## 4. Context Binding Rule (SSoT 법전 강제 적용)
**[CRITICAL INSTRUCTION]**
이제부터 본 프로젝트에서 코드를 작성하거나 아키텍처 관련 의사결정을 내릴 때는, 사용자에게 질문하기 전에 반드시 `knowledge/docs/CRITICAL_LOGIC.md`와 새롭게 수집된 스택별 기술 문서를 **최우선 법전(SSoT)**으로 열람하고 준수해야 한다.
```
