# Workspace Doc Sync 참고본

이 문서는 사람이 읽기 쉽게 정리한 한국어 참고본입니다.
Codex의 실제 skill trigger와 instruction 로딩에는 사용되지 않습니다.
실제 적용되는 skill 본문은 같은 위치의 `SKILL.md`를 기준으로 합니다.

## 용도

- 작업 루트 구조가 바뀌었을 때 문서 정합성을 맞추는 skill입니다.
- `README`, `AGENTS`, hooks, skills 관련 설명이 실제 폴더 구조와 어긋났을 때 사용합니다.
- 특히 `codex/`와 `cursor/`가 서로 독립적인 작업 루트일 때 문서 표현을 바로잡는 데 적합합니다.

## 관련 파일

- `SKILL.md`: Codex가 실제로 읽는 skill 본문입니다.
- `agents/openai.yaml`: skill 목록 UI에서 보이는 이름, 짧은 설명, 기본 프롬프트 같은 메타데이터를 정의합니다.

즉, 실제 skill instruction은 `SKILL.md`가 담당하고,
`openai.yaml`은 사람이 skill을 고르거나 호출할 때 보조하는 표시용 설정에 가깝습니다.

## 언제 쓰나

- 폴더 구조를 옮긴 뒤 README 설명이 예전 기준으로 남아 있을 때
- Codex 루트와 Cursor 루트 경계를 문서에 다시 반영해야 할 때
- hooks와 skills 사용법을 문서에 추가하거나 정정해야 할 때
- `AGENTS.md`, `README.md`, tool-local 문서가 서로 충돌할 때

## 작업 흐름

1. 실제 폴더 구조를 먼저 확인합니다.
2. 어떤 디렉터리가 각 도구의 작업 루트인지 명확히 정리합니다.
3. 관련 문서를 함께 수정합니다.
4. 자동 동작과 명시 동작을 구분해서 설명합니다.

## 핵심 기준

- 존재하지 않는 경로를 문서에 쓰지 않습니다.
- Codex 루트가 `codex/`라면 Codex 관련 설명은 그 안에서 닫히게 유지합니다.
- Cursor 루트가 `cursor/`라면 Cursor 관련 설명도 그 안에서 닫히게 유지합니다.
- hooks와 skills를 같은 메커니즘처럼 설명하지 않습니다.

## 예시 요청

- "`codex/` 안이 실제 루트라는 기준으로 문서 다시 정리해줘"
- "폴더 구조 바뀌었으니 README랑 AGENTS 맞춰줘"
- "hooks랑 skills 사용법까지 포함해서 Codex 문서 업데이트해줘"
