---
name: review
description: Review an open pull request and leave inline, line-level GitHub review comments on diff lines when needed. Use when the user asks Codex to review a PR. Comments are authored in Korean by team convention.
---

# Review Pull Request

This skill does not create or modify pull requests. It reviews the diff of an open PR and leaves **line-level review comments**, the same kind you add with the `+` button on a GitHub PR diff.

## Working Principles

- Any **open PR** can be a review target, regardless of assignee, PR author, or reviewer assignment.
- When the user specifies a PR number or URL, use that one first.
- When a PR number/URL is specified, proceed regardless of the current branch.
- When the user specifies nothing, target the **single open PR whose head is the current branch**.
- Limit review scope to the target PR's **diff against its base**.
- Focus the review on **bugs, regressions, missing validation, and risky design**.
- Prefer **inline review comments attached to code lines** over general conversation comments.
- Do not invent comments when there is no real issue.
- Never automatically `APPROVE` or `REQUEST_CHANGES`. The default is **submitting a `COMMENT` review**.

## Stop Conditions

Stop immediately and explain the reason when any of these states apply.

| State | How to judge | Guidance message |
| --- | --- | --- |
| Detached HEAD | No PR number/URL specified and current branch name is empty | Check out a branch or specify a PR, then rerun |
| No review target PR | No specified PR and no open PR for the current branch | No PR to review |
| Multiple matching PRs | User specified nothing but the current branch has 2+ PRs | Specify a PR number or URL, then rerun |
| Diff unavailable | Failed to fetch PR files or diff | Check GitHub auth/permissions, then rerun |
| Line mapping impossible | There is an issue but the exact diff line cannot be computed | Rerun once file/line are determinable |

## Workflow

### 1. Gather context

Confirm all of the following.

| Item | How to find it |
| --- | --- |
| Current branch name | From git when no PR is specified |
| Review target PR | User-specified PR, or open PR for the current branch |
| PR title / URL | From target PR metadata |
| base / head branch | From target PR metadata |
| PR author | From target PR metadata |
| latest review decision | From existing review state |
| Changed file list | Changed files and their status for the PR |
| Full diff | The PR diff |
| Existing review comments | Whether the same point was already raised |
| Existing review threads | Whether there are unresolved or repeated comments |
| HEAD SHA | The latest commit to use when creating review comments |

Select one target PR by priority.

1. The user directly specified a PR number or URL in natural language → that PR
2. Exactly one open PR has the current branch as its head → that PR
3. Otherwise → explain the reason and stop

Example commands:

```
git branch --show-current
gh pr list --state open --head "$(git branch --show-current)" --json number,title,url,author,baseRefName,headRefName,reviewDecision --jq '.[0] // empty'
gh pr view <PR_NUMBER> --json number,title,url,author,baseRefName,headRefName,reviewDecision,commits
gh pr diff <PR_NUMBER>
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/reviews
```

Always find the basis for review in the **current PR diff**. If you need context outside the base branch, read the related files, but keep comments limited to problems visible in the diff.

### 2. Review criteria

Review **every item** in the priority tiers below, in order. Comment on lower-tier items only when there is no higher-tier issue.
However, **even when no higher-tier issue exists, leave a comment if a Low is concrete and reproducible from the diff.**
That is, `no Critical–Medium + Low present` is **not `Type: none`** — it is a **`Type: comment`** case.

#### Critical — block immediately

- **Runtime crash**: null/undefined dereference, array out-of-bounds, invalid type operation
- **Security vulnerability**: SQL/Command injection, XSS (user input inserted directly into the DOM), logging or client-exposing sensitive data (tokens, passwords, PII), auth/authorization bypass
- **Data loss**: overwrite, unrecoverable deletion, missing transaction

#### High — high risk

- **Regression of existing behavior**: a path that worked before the change may break
- **Concurrency/async problems**: race condition, non-atomic shared-state mutation, `.then` without `catch` or unhandled rejection, performance loss from unnecessary serial awaits
- **Infinite loop or missing recursion exit condition**
- **Duplicate calls / duplicate execution**: same API called multiple times, event listeners registered repeatedly

#### Medium — medium risk

- **Missing exception handling**: errors from external I/O (API, DB, file) not propagated or swallowed
- **Type/contract mismatch**: function signature vs. actual passed value mismatch, implicit type coercion
- **Side-effect scope overrun**: a function mutates unintended global state or external resources
- **Dependency problems**: circular dependency, unused import, missing version pinning

#### Low — low risk (only when no Critical–Medium issue exists)

- **Missing tests**: changed logic has no unit/integration test at all
- **Insufficient validation**: input range/format used without validation
- **Performance drop**: O(n²)-or-worse algorithm, heavy I/O inside a loop
- **Readability/style**: only when it clearly causes confusion

Leave a Low comment only when all of these hold.

- Directly connected to a change in the current diff
- Explainable not as taste but as one of **maintainability, validation gap, or potential performance degradation**
- The reason it is a problem can be made concrete in one or two sentences

#### When NOT to comment

- Pure taste differences (formatting style, variable-name preference, etc.)
- Speculation that cannot be confirmed from the current diff alone
- Vague naming preference without a team-convention basis
- A point already raised the same way in another review comment
- Broad refactoring suggestions the reviewer cannot apply immediately

### 3. Comment-writing rules

A line comment must be a **concrete, reproducible problem**.

- Attach it directly to the relevant code line whenever possible.
- Explain **why it is a problem** briefly and clearly, not a whole-file summary.
- Always include **when it breaks / what input is dangerous / what is missing**.
- For a Low, write concretely **what maintenance cost, validation gap, or performance problem** it creates.
- Do not force a solution; suggest one in about one line if helpful.
- Write consistently in Korean.
- Put only one issue in one comment.
- Do not leave praise comments or style preferences by default.
- Prefix the severity label: `[Critical]`, `[High]`, `[Medium]`, `[Low]`.

Good examples:

```text
[Critical] `data`가 undefined인 첫 렌더에서 아래 `.map()` 호출 시 런타임 에러가 발생합니다.
로딩 전 초기값(`[]`) 또는 옵셔널 체이닝(`data?.map(...)`)으로 가드가 필요해 보입니다.
```

```text
[High] 이 함수는 `catch` 없이 `.then`만 체이닝하고 있어 unhandled rejection이 발생할 수 있습니다.
`.catch(err => ...)` 또는 `try/await` 블록으로 감싸는 게 안전합니다.
```

Bad example:

```text
이거 별로예요. 수정 부탁드립니다.
```

### 4. Review-plan approval (before submitting)

When issue analysis is done, **before actually posting to GitHub**, show the plan to the user in the format below and wait for approval.

```
Review plan — #<PR_NUMBER>

  1. [Critical] <file>:<line> — <one-line issue summary>
  2. [High]     <file>:<line> — <one-line issue summary>
  3. [Medium]   <file>:<line> — <one-line issue summary>
  4. [Low]      <file>:<line> — <one-line issue summary>

Submit? y / n / number selection (e.g. "only 2, 3")
```

Act on the user's response.

| Response | Action |
| --- | --- |
| `y` or "submit all" | Submit everything |
| Number selection ("only 2, 3", etc.) | Submit only those items, skip the rest |
| `n` or "cancel" | End without submitting |
| Request to edit a specific comment | Edit, show the plan again, and wait for re-approval |

- Do not submit comments to GitHub without approval.
- When there are no issues, skip the plan step, print "No issues found", and end.

### 5. Inline review comment creation

When issues are confirmed, leave them as **inline review comments** attached to GitHub PR diff lines.

When multiple lines must be seen together for the point to make sense, leave a **multiline review comment** with the `start_line` + `line` parameters.
If both line numbers cannot be confirmed from the diff, fall back to a single-line comment.

Before creating a comment, always confirm the following.

- `path`
- `commit_id`
- `side`
- `line` (single) or `start_line` + `line` (multiline)

Principles:

1. Leave an inline comment **only when it maps directly to an added or changed line**.
2. Use a multiline comment when **a point is only explained by reading several lines together**, such as conditionals, function calls, or JSX blocks.
3. Skip it if the same kind of comment already exists on that file/line.
4. When there are multiple issues, bundle them into **a single review** as a `comments` array whenever possible.
5. When line mapping is impossible, fall back to a general review comment that includes the filename and context.

Default submission:

- Create an `event=COMMENT` review with `gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/reviews`.
- Submit each comment together in the `comments` array.

When only individual comments are possible:

- Use `gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments`.
- Still prefer a single review submission over scattering many comments.

### 6. Handling no comments

When you find no concrete issue worth leaving, do not create a review comment.
A "concrete issue" here **includes Low: missing tests / insufficient validation / performance problems / confusing readability problems**.
So **do not skip a Low comment just because there is no Critical–Medium issue**.

- Do not force a short comment like `LGTM`.
- Do not approve automatically.
- The user receives a "No issues found" state **only when there is not a single concrete issue worth commenting across all tiers (Critical–Low)**.

### 7. Final response format

Summarize briefly for the user in the formats below.

#### When there are issues

```
Reviewed : yes
PR       : <URL>
Number   : #<number>
Type     : comment
Comments : <count submitted>

[Critical] <one-line core issue summary>
[High]     <one-line core issue summary>
[Medium]   <one-line core issue summary>
[Low]      <one-line core issue summary>
```

#### When there are no issues

```
Reviewed : yes
PR       : <URL>
Number   : #<number>
Type     : none
Comments : 0
Result   : No actionable issues found.
```

## Failure Handling

| Point | Handling |
| --- | --- |
| No review target PR | Explain that no PR is specified and no open PR exists for the current branch, then stop |
| Multiple matching PRs | Explain that a PR number or URL is required, then stop |
| Diff fetch failed | Explain a possible auth/permission issue and stop |
| Line mapping failed | Output the found-issue summary together with why an inline comment is not possible |
| Comment registration failed | Output the intended-issue summary together with the failure cause |
| Only ambiguous issues | End without commenting and explain that no certain problem was found |

## Boundaries

- Do not create or modify pull requests; this skill only reviews and comments.
- Do not run `APPROVE` or `REQUEST_CHANGES`; the default review event is `COMMENT`.
- Do not submit any comment to GitHub before the user approves the review plan.
- Do not comment on issues outside the target PR's diff against its base.
- Do not force `LGTM` or praise comments when there is no actionable issue.
- Author every review comment in Korean per team convention.
