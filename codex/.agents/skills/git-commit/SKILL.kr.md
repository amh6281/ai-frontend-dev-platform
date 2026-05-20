# Git Commit 참고본

이 문서는 사람이 읽기 쉽게 정리한 한국어 참고본입니다.
Codex의 실제 skill trigger와 instruction 로딩에는 사용되지 않습니다.
실제 적용되는 skill 본문은 같은 위치의 `SKILL.md`를 기준으로 합니다.

## 용도

- staged changes만 기준으로 커밋을 만드는 skill입니다.
- 커밋 메시지를 staged 변경 내용에서 추론하고, 커밋 후 push 여부를 사용자에게 확인합니다.
- unstaged 변경사항은 커밋 근거나 메시지 판단에 사용하지 않습니다.

## 관련 파일

- `SKILL.md`: Codex가 실제로 읽는 skill 본문입니다.
- `agents/openai.yaml`: skill 목록 UI에서 보이는 이름, 짧은 설명, 기본 프롬프트 같은 메타데이터를 정의합니다.

즉, 실제 커밋 workflow는 `SKILL.md`가 담당하고,
`openai.yaml`은 사람이 skill을 고르거나 호출할 때 보조하는 표시용 설정에 가깝습니다.

## 언제 쓰나

- 사용자가 staged 변경사항을 커밋해 달라고 요청할 때
- staged 변경사항을 바탕으로 커밋 메시지를 만들어야 할 때
- 커밋 후 push 여부를 별도로 확인해야 할 때

## 작업 흐름

1. 현재 브랜치, staged 파일, upstream 설정을 확인합니다.
2. detached HEAD, merge conflict, staged 변경 없음 상태에서는 멈춥니다.
3. 브랜치명에서 이슈 키를 추출하고, 없으면 `NO-ISSUE`를 사용합니다.
4. staged 변경 성격에 맞춰 commit type과 summary를 정합니다.
5. staged 변경사항만 커밋합니다.
6. 커밋 후 push 여부를 사용자에게 묻고, 확인 전에는 push하지 않습니다.

## 커밋 메시지 기준

형식은 다음을 사용합니다.

```text
<Type>(<IssueKey>): <Summary>
```

주요 type 기준:

- `Feat`: 새 기능, 화면, API 연동, 새 skill 추가
- `Fix`: 버그, 예외처리, typo 수정
- `Docs`: 문서만 변경
- `Test`: 테스트만 변경
- `Refactor`: 동작 변경 없는 구조 개선
- `Chore`: 설정, 패키지, workflow, 기타 관리 작업

## 핵심 기준

- 사용자가 명시하지 않았다면 파일을 새로 stage하지 않습니다.
- unstaged 변경사항을 커밋 판단 근거로 쓰지 않습니다.
- 서로 무관한 staged 변경이 섞여 있으면 커밋 전에 사용자에게 알립니다.
- commit 이후 push는 `accept` 또는 `run` 확인을 받은 뒤에만 진행합니다.
