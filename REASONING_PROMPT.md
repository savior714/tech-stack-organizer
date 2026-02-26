# REASONING_PROMPT (Deep Tech Analysis)

본 문서는 다른 대규모 LLM(Reasoning LLM)에게 특정 기술 스택에 대한 심층 분석을 요청하기 위한 공식 프롬프트 템플릿입니다. 이 프롬프트를 통해 얻은 답변은 본 프로젝트의 지식 베이스를 강화하는 데이터 소스로 활용됩니다.

---

## 🛠️ Reasoning Prompt Template

아래 내용을 복사하여 원하는 LLM(Claude 4.6 Opus, Gemini 3.1 Pro 등)에 입력하십시오.

```markdown
# Role: Senior Tech-Stack Architect
# Task: 지능형 기술 지식 저장소(Tech-Stack Organizer)를 위한 심층 지식 구조 설계 및 소스 발굴

당신은 특정 기술 스택을 완전히 분해하여 분석하고, 이를 에이전트가 읽기 편한 '지식 자동화 자산'으로 변환하는 시니어 아키텍트입니다. 현재 우리는 [기술 스택명: 입력하세요]를 프로젝트의 핵심 스택으로 채택했으며, 이를 위한 '지식 베이스 엔진'을 구축 중입니다.

단순히 공식 문서를 읽는 수준을 넘어, 프로젝트의 안정성과 성능을 보장할 수 있는 '심층 지식 체계'를 구축하기 위해 다음 질문에 답해 주세요.

---

## 1. 지식 소스 확장 (Source Expansion)
현재 우리는 [Official Docs, GitHub Releases, PyPI, Proposals, Awesome-List]의 5대 채널을 추적하고 있습니다. 하지만 이것만으로는 '딥 테크' 대응이 부족합니다.
- 해당 기술의 핵심 개발자 블로그, RFC 토론장, 특정 커뮤니티(StackOverflow 특정 태그, Discord/Gitter 아카이브 등) 중 실질적인 'Deep Knowledge'가 흐르는 경로 3~5곳을 정확한 URL과 함께 추천해 주세요.
- 보안 취약점(CVE)이나 패키징 의존성 변화를 가장 빠르게 알 수 있는 소스는 어디입니까?

## 2. 심층 분석 템플릿 설계 (Deep-Analysis Template)
에이전트나 개발자가 해당 기술을 마스터하기 위해 반드시 기록해야 할 '심층 분석 항목' 템플릿을 만들어 주세요. 다음 항목을 포함하거나 더 고도화해 주세요.
- [Internal Engine]: 핵심 동작 원리 (최하단 구현 레벨의 로직)
- [Performance Tuning]: 최적화 기법 및 설정 조합
- [Edge Cases]: 환경별(OS, Runtime 등) 특이 이슈 및 해결 전략
- [Compatibility Hierarchy]: 주요 라이브러리/프레임워크와의 연동 시의 특이사항

## 3. 핵심 검색 쿼리 (Expert Search Queries)
이 기술의 최신 동향과 트러블슈팅 사례를 수집하기 위해, 우리가 Perplexity나 Google에 입력해야 할 '시니어 수준의 검색 쿼리' 5가지를 제안해 주세요.

## 4. 아키텍트의 조언 (Architect's Insight)
이 기술 스택을 실무에 적용할 때, 공식 문서에는 잘 나오지 않지만 경험적으로 반드시 주의해야 하는 '치명적인 함정(Pitfall)'은 무엇입니까?
```

---

## 🔄 Workflow for Architect (Antigravity)

다른 LLM으로부터 답변을 받으면, 아래와 같이 명령하여 본 저장소에 반영하십시오.

> "전달받은 [기술명] 심층 분석 답변을 기반으로 sources.json 업데이트 및 docs/{stack} 문서 고도화를 진행해줘."
