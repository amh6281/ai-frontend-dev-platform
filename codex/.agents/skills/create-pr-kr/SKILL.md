---
name: create-pr-kr
description: Run the Korean-convention PR workflow — analyze the git diff, build a Korean commit title and PR body following the team convention, then create or update the PR automatically. Use when the user asks Codex to open or update a pull request using the Korean team PR workflow.
---

# Create PR (KR)

Run the Korean-convention pull request workflow. Analyze the current changes, generate a commit title and PR body that follow the team commit convention, and create or update the PR automatically.

The team convention values — the Korean commit summary, the Korean title rules, and the checklist labels — stay in Korean because they are the convention itself.

## Important Note (Agent / Editor Approval)

Some agents or editors may require a manual **Run** approval for commands that modify the repo or access the network (e.g. `git push`, `gh pr create`). This skill will therefore:

- Generate the commit title + PR body
- Execute the git/gh commands automatically (may still prompt for approval)

This aims to minimize manual work while staying within the security model.

## Step 1 — Analyze Changes

Analyze the current git diff to understand:

- What files changed
- What functionality changed
- Whether the change is a feature, fix, refactor, style, etc.

## Step 2 — Extract Issue Number

Extract the issue number from the current branch name.

Examples:

- `feature/TK-1325-card-delete`
- `fix/TK-210-login-error`

→ Issue number = `TK-1325`

Rules:

- Issue number **must exist**.
- If not found, stop and output:

```text
브랜치명에 이슈 번호가 포함되어야 합니다 (예: TK-1325)
```

## Step 3 — Determine Commit Type

Select one of the following commit types:

| Type | 의미 |
| --- | --- |
| `Feat` | 새로운 기능 추가 |
| `Fix` | 버그 수정 또는 typo |
| `Refactor` | 리팩토링 코드 구조 개선 기능 변경 없음 |
| `Style` | CSS 등 UI 디자인 변경 |
| `Comment` | 주석 추가 또는 변경 |
| `Test` | 테스트 코드 추가 수정 삭제 |
| `Chore` | 빌드 설정 패키지 assets 변경 |
| `Init` | 프로젝트 초기 생성 |
| `Rename` | 파일 또는 폴더 이름 변경 |
| `Remove` | 파일 삭제 작업 |

Choose the **most representative type** for the change.

## Step 4 — Generate Commit Title

Format:

```text
<Type>(<IssueNumber>): <한글 요약>
```

Rules:

- 최대 **50자**
- **마침표 사용 금지**
- **특수문자 사용 금지**
- **개조식 구문**
- **한글 작성**

Examples:

```text
Feat(TK-1325): 카드 삭제 버튼 추가
Fix(TK-210): 로그인 토큰 갱신 오류 수정
Refactor(TK-98): Zustand store 구조 정리
Chore(TK-450): 에이전트 규칙 구조 추가
```

## Step 5 — Generate PR Description

Use `.github/pull_request_template.md` as the source template.

- Load `.github/pull_request_template.md` and keep the same section layout (`Related Issue`, `Summary`, `Checklist`).
- Fill placeholders from the diff analysis and the extracted issue number.
- In Checklist, set exactly one checked item that matches the selected commit type.
- Do not embed the full template contents inside this skill definition.

Commit type → checklist mapping:

- `Feat` → 새로운 기능 추가
- `Fix` → 버그 수정
- `Style` → CSS 등 사용자 UI 디자인 변경
- `Refactor` → 코드 리팩토링
- `Comment` → 주석 추가 및 수정
- `Test` → 테스트 추가, 테스트 리팩토링
- `Chore` → 빌드 부분 혹은 패키지 매니저 수정
- `Rename` → 파일 혹은 폴더명 수정
- `Remove` → 파일 혹은 폴더 삭제

## Step 6 — Execute Commands Automatically

After generating the PR title and body, run the following commands in order:

1. `git add -A`
2. `git commit -m "<PR title>"`
3. `git push -u origin HEAD`
4. `BRANCH=$(git branch --show-current)`
5. `EXISTING_PR_NUMBER=$(gh pr list --state open --head "$BRANCH" --json number --jq '.[0].number // empty')`
6. Detect an existing PR and create or update accordingly:

   ```bash
   if [ -n "$EXISTING_PR_NUMBER" ]; then
     gh pr edit "$EXISTING_PR_NUMBER" --title "<PR title>" --body "<PR body>";
     gh pr view "$EXISTING_PR_NUMBER" --json url --jq .url;
   else
     gh pr create --title "<PR title>" --body "<PR body>";
   fi
   ```

Rules:

- Execute in order and stop on failure.
- Do not use interactive git flags.
- Do not force push.
- Print the PR URL whether the PR was created or updated.

## Boundaries

- Do not proceed when the branch name has no issue number; stop with the Korean message from Step 2.
- Do not embed the full `.github/pull_request_template.md` contents inside this skill.
- Do not check more than one checklist item.
- Do not force push or use interactive git flags.
- Keep the Korean commit summary, title rules, and checklist labels in Korean — they are the team convention.
