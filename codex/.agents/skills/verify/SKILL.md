---
name: verify
description: Run project quality checks (lint, type, build) across the whole project and summarize the results. Use when the user asks Codex to verify the project, run quality checks, or check lint, type, and build status before a commit or PR.
---

# Verify Project

Run quality checks (lint, type, build) for the current project and summarize the results.

The verification target is the **entire project rooted at the current working directory**. This runs regardless of commit state. When any check fails, summarize the clear failure cause and location instead of dumping full logs, and propose a one-line fix direction when possible. When everything passes, report success clearly.

## Stop Conditions

Stop and explain the reason before running when any of these are true:

| State | How to check | Message |
| --- | --- | --- |
| No package.json | No `package.json` at project root | Not a Node project, cannot run |
| Dependencies not installed | No `node_modules` | `npm install` or `pnpm install` needed |

## Workflow

### 1. Gather context

Check all of these:

| Item | How to check |
| --- | --- |
| package.json exists | Confirm at project root |
| Package manager | Check lock file (`package-lock.json` / `pnpm-lock.yaml`) |
| eslint config exists | Check `.eslintrc.*` or `eslint.config.*` |
| tsconfig exists | Check `tsconfig.json` or `tsconfig.*.json` |
| build script exists | Check `scripts.build` in `package.json` |

Example check commands:

```bash
ls package.json tsconfig.json 2>/dev/null
cat package.json | jq '.scripts'
ls .eslintrc.* eslint.config.* 2>/dev/null
```

### 2. Run verification

Run the steps in this order. Run each step only when its config exists; otherwise skip it.

#### Step 1 — Lint check

Run when an eslint config exists.

```bash
eslint . --quiet
```

#### Step 2 — Type check

Run for TypeScript projects (`tsconfig.json` exists).

```bash
tsc -b
```

#### Step 3 — Build check

Run when `package.json` has a `build` script.

```bash
# npm
npm run build

# pnpm
pnpm build
```

### 3. Interpret results

#### Failure judgment

- Any exit code ≠ 0 marks that item as **failed**.
- Warnings are not treated as failures (note them separately if needed).

#### Output rules

- Do not print the full error log verbatim.
- Summarize only these:

| Item | Content |
| --- | --- |
| File | Path of the file where the error occurred |
| Line | Line number when available |
| Cause | Core error message |
| Impact | What problem it causes (briefly) |

### 4. Output format

#### When failed

```text
Verify result : failed

1. [Lint] src/components/xxx.tsx:12
   - Unexpected any usage
   - 타입 안정성 저하 가능

2. [Type] src/api/user.ts:34
   - Type 'undefined' is not assignable to type 'string'
   - 런타임 에러 발생 가능

3. [Build]
   - Failed to resolve import '@/utils/xxx'
   - 빌드 실패
```

#### When success

```text
Verify result : success

- Lint  : passed
- Type  : passed
- Build : passed
```

#### When no runnable check exists

```text
Verify result : skipped
Reason        : No verification scripts found
```

### 5. Additional rules

- Run only the checks that are available, even when only some of lint / type / build exist.
- Keep the run order Lint → Type → Build.
- Continue running the remaining checks even when one fails, so the full result is known.
- When the same file has many errors of the same kind, summarize only 1-2 representative cases and show the rest as a count.

## Failure Handling

| When | How to handle |
| --- | --- |
| Lint run fails | Judge eslint config issue or code error, then output summary |
| Type check fails | Summarize the file, line, and cause of the type error |
| Build fails | Summarize the core build error message |
| Command missing | Skip that item and continue |

## Boundaries

- Do not modify files or fix errors as part of verification; only run checks and report.
- Do not stop the whole run when a single check fails; continue the remaining checks.
- Do not dump full logs; summarize file, line, cause, and impact.
- Do not treat warnings as failures unless explicitly flagged.
