# Context Snapshot

- **Branch:** main
- **Current State:** 비즈니스 로직(cheonggu) 종속성 제거 및 범용 플러그인 형태로 프레임워크 일반화(Generalization) 완료.
- **Latest Change:** `docs/CRITICAL_LOGIC.md`, `config/sources.json` 및 `docs/mission.md` 갱신을 통해 특정 프로젝트의 그림자를 제거함.
- **Key Decisions:**
  - 본 프레임워크를 다른 프로젝트(예: `cheonggu`)에서 Submodule 형태로 사용할 수 있도록, 내부에는 오직 기술적 지식 정보 수집 플러그인 로직(`update-docs.py` 및 `start.bat`)만 남김.
  - SSoT 문서(`CRITICAL_LOGIC.md`) 역시 '프레임워크 사용법'에 초점을 맞추도록 변경.
  - 범용 파이프라인의 완성도를 높여, `config/sources.json`만 갈아끼우면 어떤 앱의 기술 스택이든 문서화할 수 있는 준비 완료.
