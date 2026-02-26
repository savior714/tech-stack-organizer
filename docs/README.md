# Knowledge Domain (docs)

플러그인에 연결된 대상 프로젝트의 최신 기술 문서 및 SSoT 가이드 라인이 수록되는 지식 도메인입니다.
해당 폴더는 AI 에이전트들의 작업 기억 장치(Working Memory)이자 영구 지식 저장소 역할을 수행합니다.

- **`{tech_stack}/`**: Doc-Fetcher 파이프라인에 의해 자동 생성, 갱신되는 해당 프로젝트의 스택별 마크다운 문서들 (`sources.json` 기반 동적 생성).
- **`CRITICAL_LOGIC.md`**: 로직 일반화를 위한 플러그인 프레임워크 자체의 아키텍처 마스터 코어 가이드.
- **`mission.md`, `context.md`, `checklist.md`**: 작업의 목적과 진척 상황을 단기 기억으로 파악하기 위한 관리 영역.
