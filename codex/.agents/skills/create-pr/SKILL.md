---
name: create-pr
description: Analyze git changes, generate a commit and pull request following the team convention, then create or update the PR automatically. Use when the user asks Codex to create a PR, open a pull request, or commit and push changes into a PR.
---

# Create Pull Request

Analyze the current changes, build a commit title and PR body from the team convention, then run the git and gh commands to create or update the pull request.

Some agents or editors may require manual approval for commands that modify the repo or access the network (for example `git push`, `gh pr create`). This skill generates the commit title and PR body, then executes the git and gh commands automatically. Approval prompts may still appear.

## Workflow

### 1. Analyze changes

Analyze the current git diff to understand:

- What files changed
- What functionality changed
- Whether the change is a feature, fix, refactor, style, or another category

### 2. Extract issue number

Extract the issue number from the current branch name.

Examples:

```text
feature/TK-1325-card-delete  → TK-1325
fix/TK-210-login-error       → TK-210
```

Rules:

- The issue number **must exist**.
- If no issue number is found, stop and output:

```text
Branch name must include an issue number (example TK-1325)
```

### 3. Determine commit type

Select the **most representative** type from the list:

```text
Feat: 새로운 기능 추가
Fix: 버그 수정 또는 typo
Refactor: 리팩토링 코드 구조 개선 기능 변경 없음
Style: CSS 등 UI 디자인 변경
Comment: 주석 추가 또는 변경
Test: 테스트 코드 추가 수정 삭제
Chore: 빌드 설정 패키지 assets 변경
Init: 프로젝트 초기 생성
Rename: 파일 또는 폴더 이름 변경
Remove: 파일 삭제 작업
```

### 4. Generate commit title

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

### 5. Generate PR description

Use `.github/pull_request_template.md` as the source template.

- Load `.github/pull_request_template.md` and keep the same section layout (`Related Issue`, `Summary`, `Checklist`).
- Fill placeholders from the diff analysis and the extracted issue number.
- In Checklist, set exactly one checked item that matches the selected commit type.
- Do not embed the full template contents inside this skill definition.

Commit type to checklist mapping:

- Feat → 새로운 기능 추가
- Fix → 버그 수정
- Style → CSS 등 사용자 UI 디자인 변경
- Refactor → 코드 리팩토링
- Comment → 주석 추가 및 수정
- Test → 테스트 추가, 테스트 리팩토링
- Chore → 빌드 부분 혹은 패키지 매니저 수정
- Rename → 파일 혹은 폴더명 수정
- Remove → 파일 혹은 폴더 삭제

### 6. Execute commands

After generating the PR title and body, run the following commands in order:

1. `git add -A`
2. `git commit -m "<PR title>"`
3. `git push -u origin HEAD`
4. `BRANCH=$(git branch --show-current)`
5. `EXISTING_PR_NUMBER=$(gh pr list --state open --head "$BRANCH" --json number --jq '.[0].number // empty')`
6. Create or update the PR:

   ```bash
   if [ -n "$EXISTING_PR_NUMBER" ]; then
     gh pr edit "$EXISTING_PR_NUMBER" --title "<PR title>" --body "<PR body>"
     gh pr view "$EXISTING_PR_NUMBER" --json url --jq .url
   else
     gh pr create --title "<PR title>" --body "<PR body>"
   fi
   ```

Rules:

- Execute in order and stop on failure.
- Do not use interactive git flags.
- Do not force push.
- Print the PR URL whether the PR was created or updated.

## Boundaries

- Stop and output the issue-number message when the branch name has no issue number.
- Do not embed the full PR template contents inside this skill.
- Set exactly one checked Checklist item, matching the selected commit type.
- Do not use interactive git flags and do not force push.
- Run the Step 6 commands in order and stop on the first failure.
