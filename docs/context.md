# Context Snapshot

- **Branch:** main
- **Current State:** 디렉토리 뼈대 구축 및 에이전트 코어 가이드 작성 완료, 자동화 문서 수집 파이프라인 구축 완료
- **Latest Change:** `tools/automation/update-docs.py` 및 `config/sources.json` 생성
- **Key Decisions:**
  - AI 에이전트 간 SSoT 역할을 수행하기 위해, 주석 없는 모호한 설계 금지.
  - 빌드 스크립트는 `Get-ChildItem` 등을 활용해 물리적인 결과물을 확인하도록 작성 완료됨.
  - 전역 룰(Global Rule)에 따라 모든 문서는 `docs/` 하위로 위치하여 정리.
