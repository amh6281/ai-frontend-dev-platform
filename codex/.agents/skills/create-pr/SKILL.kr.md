# Create PR 참고본

이 문서는 사람이 읽기 쉽게 정리한 한국어 참고본입니다.
Codex의 실제 skill trigger와 instruction 로딩에는 사용되지 않습니다.
실제 적용되는 skill 본문은 같은 위치의 `SKILL.md`를 기준으로 합니다.

## 용도

- 현재 변경사항을 분석해 팀 컨벤션에 맞는 커밋과 PR을 만드는 skill입니다.
- 커밋 제목과 PR 본문을 생성한 뒤, git/gh 명령을 실행해 PR을 생성하거나 기존 PR을 업데이트합니다.
- 브랜치명에 이슈 번호가 없으면 진행하지 않고 멈춥니다.

## 관련 파일

- `SKILL.md`: Codex가 실제로 읽는 skill 본문입니다.
- `agents/openai.yaml`: skill 목록 UI에서 보이는 이름, 짧은 설명, 기본 프롬프트 같은 메타데이터를 정의합니다.

즉, 실제 PR 생성 workflow는 `SKILL.md`가 담당하고,
`openai.yaml`은 사람이 skill을 고르거나 호출할 때 보조하는 표시용 설정에 가깝습니다.

## 언제 쓰나

- 사용자가 현재 변경사항으로 PR을 만들어 달라고 요청할 때
- 커밋과 PR을 팀 컨벤션에 맞춰 한 번에 처리해야 할 때
- 같은 브랜치에 이미 열린 PR이 있으면 본문을 업데이트해야 할 때

## 작업 흐름

1. 현재 git diff를 분석해 변경 파일과 기능, 변경 성격을 파악합니다.
2. 브랜치명에서 이슈 번호를 추출하고, 없으면 안내 메시지를 출력하고 멈춥니다.
3. 변경 성격에 맞는 commit type을 한 가지 고릅니다.
4. `<Type>(<IssueNumber>): <한글 요약>` 형식으로 커밋 제목을 만듭니다.
5. `.github/pull_request_template.md`를 기준으로 PR 본문을 채웁니다.
6. `git add -A` → `commit` → `push -u origin HEAD` 순으로 실행하고, 기존 PR이 있으면 `gh pr edit`, 없으면 `gh pr create`로 PR을 만든 뒤 URL을 출력합니다.

## 핵심 기준

- 브랜치명에 이슈 번호가 반드시 있어야 하며, 없으면 멈춥니다.
- 커밋 제목은 최대 50자, 마침표·특수문자 금지, 개조식 한글로 작성합니다.
- Checklist는 선택한 commit type에 맞는 항목 하나만 체크합니다.
- 명령은 순서대로 실행하고 실패 시 멈추며, interactive git flag와 force push는 사용하지 않습니다.
