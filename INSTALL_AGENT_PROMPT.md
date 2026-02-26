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
3. **설치 완료 보고 및 사용자 승인 (필수):**
   에이전트는 설치를 마치며 다음과 같은 형식으로 요약 보고를 수행하고 사용자의 실행 승인을 기다린다.

---
### 📦 [Tech-Stack Organizer] 설치 및 분석 완료
* **탐지된 기술 스택:**
  - Python (requirements.txt)
  - Nuitka (requirements.txt)
  - (기타 탐지된 스택 리스트...)
* **보고:** "현재 프로젝트의 의존성을 분석하여 맞춤형 지식 수집 설정을 완료했습니다. 이제 공식 문서, 릴리스 노트, 큐레이션 데이터를 마크다운 형태로 가져올 수 있습니다."

**"위 기술 스택에 대한 최신 문서 수집을 시작할까요 (start.bat 실행)?"**
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
