# Review PR 참고본

이 문서는 사람이 읽기 쉽게 정리한 한국어 참고본입니다.
Codex의 실제 skill trigger와 instruction 로딩에는 사용되지 않습니다.
실제 적용되는 skill 본문은 같은 위치의 `SKILL.md`를 기준으로 합니다.

## 용도

- 열려 있는 PR의 diff를 검토하고, GitHub PR diff의 `+` 버튼으로 다는 것과 같은 **라인 단위 review comment** 를 남기는 skill입니다.
- PR을 생성하거나 수정하지 않습니다. 리뷰와 코멘트만 담당합니다.
- 승인(`APPROVE`)이나 변경요청(`REQUEST_CHANGES`)은 자동으로 하지 않고, 기본은 `COMMENT` review 제출입니다.
- 팀 컨벤션에 따라 모든 리뷰 코멘트는 한국어로 작성합니다.

## 관련 파일

- `SKILL.md`: Codex가 실제로 읽는 skill 본문입니다.
- `agents/openai.yaml`: skill 목록 UI에서 보이는 이름, 짧은 설명, 기본 프롬프트 같은 메타데이터를 정의합니다.

## 언제 쓰나

- 사용자가 열린 PR을 리뷰해 달라고 요청할 때
- 사용자가 PR 번호 또는 URL을 직접 지정한 경우 → 해당 PR을 우선 대상으로 사용
- 사용자가 지정하지 않으면 현재 브랜치를 head로 하는 열린 PR 1건을 대상으로 함
- 현재 브랜치 기준 PR이 없거나 2개 이상이면 멈추고 PR 지정을 요청

## 작업 흐름

1. 현재 브랜치, 대상 PR, base/head, author, 변경 파일, 전체 diff, 기존 코멘트, HEAD SHA를 확인합니다.
2. detached HEAD, 리뷰 대상 PR 없음, 복수 매칭, diff 조회 불가, line 매핑 불가 상태에서는 멈춥니다.
3. Critical → High → Medium → Low 티어 순서로 빠짐없이 검토합니다.
4. 제출 전 리뷰 계획을 사용자에게 보여주고 `y / n / 번호 지정` 응답을 기다립니다.
5. 승인된 항목만 `gh api .../reviews` 의 `event=COMMENT` review로, `comments` 배열에 묶어 제출합니다.
6. 최종 응답을 이슈 있음/없음 형식으로 정리합니다.

## 핵심 기준

- bug, regression, 누락된 검증, 위험한 설계 중심으로 본다.
- 일반 conversation comment보다 코드 라인에 붙는 inline review comment를 우선한다.
- **Critical–Medium이 없어도 Low가 구체적이고 diff에서 재현 가능하면 코멘트한다.** 즉 `Critical–Medium 없음 + Low 있음 = Type: comment`(NOT none).
- 코멘트에는 심각도 레이블(`[Critical]`/`[High]`/`[Medium]`/`[Low]`)을 붙이고, 한 코멘트에 한 이슈만 담는다.
- 언제 깨지는지 / 어떤 입력에서 위험한지 / 무엇이 누락됐는지를 반드시 설명한다.
- 단순 취향 차이, 확정 불가한 추측, 이미 지적된 내용, 즉시 고칠 수 없는 넓은 리팩터링은 코멘트하지 않는다.
- 사용자 승인 전에는 GitHub에 코멘트를 제출하지 않으며, 모든 티어에서 구체적 이슈가 하나도 없을 때만 "문제 발견 없음"으로 종료한다.
