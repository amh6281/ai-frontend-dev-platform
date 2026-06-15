---
name: sync-pr
description: Create a pull request for the current branch or update the existing pull request body from the latest pushed commits. Use when the user asks Codex to open, sync, or update a PR.
---

# Sync Pull Request

This skill does not create commits. If there is uncommitted or unpushed work, tell the user to commit and push first with the `git-commit` skill (`$git-commit`) before running this skill.

## Stop Conditions

If any of these states is true, explain the reason and stop immediately.

| State | How to check | Guidance message |
| --- | --- | --- |
| Detached HEAD | Current branch name is empty | Re-run after `git checkout -b <branch-name>` |
| Merge conflict | Staged entries include unmerged paths | Re-run after resolving the conflict |
| No upstream | No remote tracking branch is configured | Re-run after `git push -u origin HEAD` |
| Unpushed commits ahead | Local is ahead of the remote | Re-run after the `git-commit` skill (`$git-commit`) or `git push` |

---

## 1. Gather context

Determine all of the following.

| Item | How to determine |
| --- | --- |
| Current branch name | Check from git |
| Remote sync state | Check with `git status` |
| Issue number | Extract the first `[A-Z]+-\d+` pattern from the branch name. If none, use the last segment. If neither is useful, use `NO-ISSUE` |
| Jira URL | `https://jira.mailplug.co.kr/browse/<issue-number>` |
| Commits since develop | Subjects and bodies of commits in the `origin/develop..HEAD` range |
| Changed file list | Files and their status versus `origin/develop` |
| Existing open PR | Whether an open PR exists with the current branch as head |

---

## 2. Choose the PR title

If a PR is already open, skip this step. **Never change the title.**

Apply in priority order.

1. The user specified a title in natural language -> use it as-is
2. Exactly one commit since develop -> use that commit subject as-is
3. Two or more commits since develop -> reconstruct one representative title from the core content. Keep the Type if all commits share it, otherwise use `Chore`
4. No commits -> `Chore(<issue-number>): 작업 반영`

The title follows these rules.

- 50 characters maximum
- No punctuation or special symbols
- Follow the `Type(scope): 설명` format

---

## 3. Write the PR body

Base the body on `.github/pull_request_template.md`. Replace placeholders with real values and fill each section by the criteria below.

### Related Issue

```md
## Related Issue 🔗

- Jira: [<issue-number>](<Jira URL>)
```

### Summary

A reviewer should understand why this PR is needed and what changed before opening the code. Do not list file names. Describe at the feature and behavior level.

If there is key code that reveals the intent of the change, attach it as a code block. Excerpt only the essential part, not the full diff.

````md
## Summary ✏️

### 변경 배경

<!-- 왜 이 작업이 필요했는가? 기존의 문제나 요구사항을 한두 문장으로 -->

### 핵심 변경사항

<!-- 무엇이 바뀌었는가? 파일명 나열 금지. 기능·동작·구조 단위로 설명 -->

<!-- 변경의 의도를 드러내는 핵심 코드가 있으면 아래에 첨부 -->

```ts
// 변경의 의도를 드러내는 핵심 코드 (해당 시)
```

### 기대 효과

<!-- 이 변경으로 무엇이 나아지는가? 정량적이면 더 좋음 -->
````

### Body writing rules

| Rule | Reason |
| --- | --- |
| Do not list file names or paths | Reviewers can see them in the diff. The body should convey intent |
| Describe at the feature and behavior level | Center the writing on the changed behavior and its reason, not file names |
| Attach a key code snippet | If code reveals the intent at a glance, insert it as a code block. Excerpt only the essential part, not the full diff |
| State review points | Call out design decisions or trade-offs separately |
| State impact scope | Always note side effects on other modules or pages |

---

## 4. Create or update the PR

| Situation | Action |
| --- | --- |
| No open PR | Create a new PR with base `develop` |
| Open PR exists | Update the body only. Do not touch the title, labels, or assignee |

---

## 5. Post-processing

Check the current GitHub user, then do the following. Never overwrite values that are already set.

1. If the `agent-generated` label does not exist, create it and add it to the PR
2. Add the current user as an assignee
3. If `.github/CODEOWNERS` exists, extract reviewers, exclude yourself, and add the rest

---

## 6. Result output

```
Action  : created | updated
Branch  : <branch-name>
PR      : <URL>
Number  : #<number>
Title   : <title>
Body    : updated
```

---

## Failure handling

| When | How to handle |
| --- | --- |
| A stop condition applies | Explain the current state and how to resolve it, then stop |
| No upstream | Advise `git push -u origin HEAD`, then stop |
| Unpushed commits ahead | Advise the `git-commit` skill (`$git-commit`) or `git push`, then stop |
| PR creation fails | Print the current branch name and the last commit subject, then stop |
| PR update fails | Print the existing PR number / URL and the failure reason, then stop |

---

## Boundaries

- Do not create commits. Direct the user to the `git-commit` skill (`$git-commit`) for uncommitted or unpushed work.
- Do not change the title, labels, or assignee of an already open PR.
- Do not overwrite assignee, reviewer, or label values that are already set.
- Do not push, amend, rebase, or reset.
