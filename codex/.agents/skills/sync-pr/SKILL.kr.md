# Sync PR 참고본

이 문서는 사람이 읽기 쉽게 정리한 한국어 참고본입니다.
Codex의 실제 skill trigger와 instruction 로딩에는 사용되지 않습니다.
실제 적용되는 skill 본문은 같은 위치의 `SKILL.md`를 기준으로 합니다.

## 용도

- 현재 브랜치에 대한 PR을 새로 만들거나, 이미 열린 PR의 본문을 최신 push된 커밋 기준으로 업데이트하는 skill입니다.
- 이 skill은 커밋을 만들지 않습니다. 미완성 작업이 있으면 먼저 `git-commit` skill(`$git-commit`)로 커밋·push를 끝낸 뒤 실행합니다.
- 이미 열린 PR은 본문만 갱신하고 제목·라벨·assignee는 건드리지 않습니다.

## 관련 파일

- `SKILL.md`: Codex가 실제로 읽는 skill 본문입니다.
- `agents/openai.yaml`: skill 목록 UI에서 보이는 이름, 짧은 설명, 기본 프롬프트 같은 메타데이터를 정의합니다.

## 언제 쓰나

- 현재 브랜치 작업을 PR로 올려야 할 때
- 이미 열린 PR의 본문을 최신 커밋 기준으로 다시 정리해야 할 때
- 커밋·push는 끝났고 PR 생성/업데이트만 남았을 때

## 작업 흐름

1. 실행 전 중단 조건(detached HEAD, merge conflict, upstream 없음, 미push 커밋 존재)을 확인하고 해당하면 멈춥니다.
2. 브랜치명, 원격 동기화 상태, 이슈 번호, Jira URL, develop 이후 커밋, 변경 파일, 기존 열린 PR 여부를 파악합니다.
3. PR 제목을 결정합니다. 이미 열린 PR이면 제목을 건드리지 않습니다.
4. `.github/pull_request_template.md` 기반으로 본문을 작성합니다. 파일명 나열 없이 기능·동작 단위로 서술합니다.
5. 열린 PR이 없으면 base `develop`으로 새 PR을 만들고, 있으면 본문만 업데이트합니다.
6. `agent-generated` 라벨, assignee, CODEOWNERS reviewer를 후처리합니다. 이미 설정된 값은 덮어쓰지 않습니다.

## 핵심 기준

- 이슈 번호는 브랜치명에서 `[A-Z]+-\d+`를 우선 추출하고, 없으면 마지막 segment, 그것도 없으면 `NO-ISSUE`를 씁니다.
- 제목은 최대 50자, 마침표·특수기호 없이 `Type(scope): 설명` 형식을 따릅니다.
- 본문은 파일명·경로를 나열하지 않고 변경 의도·동작·영향 범위를 전달합니다.
- 이미 열린 PR의 제목·라벨·assignee와 기존에 설정된 값은 덮어쓰지 않습니다.
- 커밋은 만들지 않습니다. 미완성·미push 작업은 `git-commit` skill(`$git-commit`)로 안내합니다.
