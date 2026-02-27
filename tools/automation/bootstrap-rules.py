import os
import sys
from pathlib import Path

def setup_bootstrap():
    """
    부모 프로젝트의 에이전트 설정 파일(.cursorrules 등)에 
    Tech Stack Organizer의 운영 규칙을 자동 주입합니다.
    """
    # 1. 경로 설정 (현재 스크립트 위치 기준 부모의 부모의 부모가 프로젝트 루트일 가능성이 높음)
    # .agents/tech-stack-organizer/tools/automation/bootstrap-rules.py 구조 가정
    current_path = Path(__file__).resolve()
    plugin_root = current_path.parent.parent.parent
    
    # 부모 프로젝트 루트 찾기
    parent_project_root = None
    is_standard_path = True
    
    # 만약 .agents 폴더 안에 있다면 그 위가 부모 루트
    if plugin_root.parent.name == ".agents" or plugin_root.parent.name == "_agents":
        parent_project_root = plugin_root.parent.parent
        if plugin_root.name != "tech-stack-organizer":
            is_standard_path = False
    else:
        # 서브모듈이 아닌 직접 설치되었거나 비표준 경로에 있는 경우
        parent_project_root = plugin_root
        # 현재 폴더가 .agents 내부에 있지 않다면 비표준으로 간주 (단, 직접 프로젝트인 경우는 예외)
        if not (plugin_root / ".git").exists() or plugin_root.name != "tech-stack-organizer":
             is_standard_path = False

    print(f"[*] Target Project Root: {parent_project_root}")
    
    if not is_standard_path:
        print("\n" + "!" * 60)
        print("[FATAL ERROR] Non-standard installation path detected!")
        print(f"Current Path: {plugin_root}")
        print("Required Path: [project_root]/.agents/tech-stack-organizer")
        print("-" * 60)
        print("AI AGENT GUIDANCE:")
        print("You have installed this plugin in the wrong directory.")
        print("To fix this, you MUST run the following command immediately:")
        print(f"\ngit mv {plugin_root.relative_to(parent_project_root)} .agents/tech-stack-organizer\n")
        print("After moving, re-run this bootstrap script.")
        print("!" * 60 + "\n")
        sys.exit(1) # 차단: 잘못된 경로에서는 규칙 주입을 거부함

    # 2. 주입할 규칙 정의 (Antigravity Senior Architect Persona + Steps Activation)
    rules_to_inject = f"""
# --- [Tech Stack Organizer: Senior Architect Persona] ---
# 이 섹션은 tech-stack-organizer 플러그인에 의해 자동 주입되었습니다.
# 수정 시 플러그인의 운영 규칙이 파괴될 수 있습니다.

## 1. Persona & Communication
* **Role:** 10년 경력의 Senior Full-stack Architect.
* **Tone:** 차분하고 논리적이며, 핵심 문장은 **굵게(Bold)** 표시.
* **Language:** 모든 설명, 주석, 답변은 **한국어(Korean)** 사용.
* **Emoji:** 답변 내 이모지 사용을 **절대 금지**.

## 2. Operational Protocol (Steps & Atomic Tasks)
* **ReAct Workflow:** 지시 분석 -> 계획 수립 -> 원자적 작업 -> 검증 -> 보고 루프 준수.
* **Atomic Step:** 한 번의 턴에 하나의 `docs/checklist.md` 항목만 수행 후 즉시 멈춤.
* **Physical Evidence:** 추측 금지. 반드시 `Get-Content`나 테스트 명령어로 결과를 확인 후 보고.
* **Steps UI:** 도구 실행 전후로 사고 과정(Thought)을 명확히 노출하여 Antigravity Steps UI가 활성화되도록 함.

## 3. Knowledge Base Binding
* 프로젝트 내 새로운 기술 도입이나 로드블록 발생 시 즉시 `.agents/tech-stack-organizer/tools/automation/update-docs.py` 실행 제안.
* 의사결정 전 `.agents/tech-stack-organizer/docs/CRITICAL_LOGIC.md`를 최우선 참조.
# --- [End of Tech Stack Organizer Rules] ---
"""

    # 3. 대상 파일 목록
    target_files = [
        ".cursorrules",
        ".clinerules",
        ".windsurfrules",
        ".atlassianrules",
        ".github/copilot-instructions.md"
    ]

    modified_count = 0
    for filename in target_files:
        rule_file = parent_project_root / filename
        
        # 상위 디렉토리가 없으면 생성 (예: .github)
        if not rule_file.parent.exists():
            rule_file.parent.mkdir(parents=True, exist_ok=True)

        content = ""
        if rule_file.exists():
            try:
                content = rule_file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # ANSI 등에 대응 (필요시)
                content = rule_file.read_text(encoding="cp949")

        # 이미 주입되어 있는지 확인
        if "Tech Stack Organizer" in content:
            print(f"[-] {filename} is already bootstrapped. Skipping.")
            continue

        # 규칙 주입 (파일 앞부분에 추가)
        new_content = rules_to_inject + "\n" + content
        
        try:
            rule_file.write_text(new_content, encoding="utf-8")
            print(f"[+] Successfully bootstrapped {filename}")
            modified_count += 1
        except Exception as e:
            print(f"[!] Error writing to {filename}: {e}")

    # 4. 워크플로우 폴더 체크 및 심볼릭 링크 제안 (옵션)
    # Antigravity는 .agents/workflows를 자동으로 읽으므로 서브모듈 경로가 맞으면 별도 작업 불필요

    print(f"\n[*] Bootstrapping completed. {modified_count} files modified.")
    print("[!] Now, restart your agent or type 'reload rules' to activate the Senior Architect mode.")

if __name__ == "__main__":
    setup_bootstrap()
