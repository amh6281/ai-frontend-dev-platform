---
name: git-commit
description: Create a Git commit from staged changes only, derive a concise commit title, and ask before pushing. Use when the user asks Codex to commit, write a commit message, or commit and optionally push local changes.
---

# Git Commit

Create commits from staged changes only. Do not use unstaged changes as evidence for the commit title or summary.

## Stop Conditions

Stop and explain the reason before committing when any of these are true:

| State | How to check |
| --- | --- |
| Detached HEAD | Current branch name is empty |
| Merge conflict | Staged entries include unmerged paths |
| No staged changes | There is nothing staged to commit |

## Workflow

### 1. Gather context

Check:

- Current branch name
- Issue key
- Staged file list with change types
- Upstream tracking branch
- Staged diff summary, only when needed to understand the change

Issue key extraction priority:

1. First `[A-Z]+-\d+` pattern in the branch name
2. Last branch segment when no issue pattern exists
3. `NO-ISSUE` when neither is useful

### 2. Choose commit title

Format:

```text
<Type>(<IssueKey>): <Summary>
```

Choose `Type` by the staged changes:

| Priority | Condition | Type |
| --- | --- | --- |
| 1 | Initial project setup | `Init` |
| 2 | Only deletions | `Remove` |
| 3 | Mostly moves or renames | `Rename` |
| 4 | Test-only changes | `Test` |
| 5 | CSS, SCSS, style-only changes | `Style` |
| 6 | New feature, screen, or API integration | `Feat` |
| 7 | Bug fix, exception handling, or typo fix | `Fix` |
| 8 | Source structure or implementation cleanup | `Refactor` |
| 9 | Package, lockfile, Dockerfile, workflow, or asset changes | `Chore` |
| 10 | Anything else | `Chore` |

Summary rules:

- Use the user's requested commit title when they clearly provided one.
- Otherwise summarize what changed, not just filenames.
- Keep it under 50 characters when practical.
- Do not end with punctuation.
- Use `작업 반영` only when the staged changes are unclear.

### 3. Commit

Run the commit using only staged changes.

If commit fails, report the failure reason and the staged status.

### 4. Ask before push

Do not push automatically after committing.

After the commit, show:

```text
커밋을 생성했습니다.

- Type    : <TYPE>
- Summary : <SUMMARY>
- Commit  : <COMMIT_TITLE>
- Branch  : <BRANCH>
- Upstream: <UPSTREAM or (no upstream)>
- Push To : <origin HEAD or current upstream branch>

이 커밋을 원격에 push 할까요? `accept` 또는 `run`이면 진행합니다.
```

Only push when the user replies with `accept` or `run`.

Push target:

| State | Action |
| --- | --- |
| No upstream | Push with upstream to `origin HEAD` |
| Has upstream | Push to the current upstream branch |

### 5. Final result

Report:

```text
Commit : <commit title>
SHA    : <commit SHA>
Pushed : yes | no
Branch : <push target or branch>
```

## Boundaries

- Do not stage files unless the user explicitly asks.
- Do not include unstaged changes in the commit rationale.
- Do not amend, rebase, reset, or clean unless the user explicitly asks.
- If unrelated staged changes are mixed together, call that out before committing.
