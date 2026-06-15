---
name: refactor
description: Analyze target files against the project standards in codex/AGENTS.md, propose refactoring points, and apply changes only after approval. Use when the user asks Codex to refactor files or a scope without changing behavior.
---

# Refactor

Analyze target files against the project standards in `codex/AGENTS.md`, propose refactoring points, and apply approved changes. Refactoring is limited to structure, type, and readability improvements. It must not change runtime behavior.

## Principles

- Base every refactoring point on the project standards in `codex/AGENTS.md`. Do not propose taste or style preferences that are not grounded in those standards.
- Do not change runtime behavior. Limit changes to structure, type, and readability.
- Show the proposal plan first and wait for approval. Never edit files without approval.
- Apply only the approved items.

## Stop Conditions

Stop and explain the reason before doing anything when any of these are true:

| State | How to check | Message |
| --- | --- | --- |
| No standards source | `codex/AGENTS.md` is not available | Cannot find the standards source for refactor criteria |
| Target file missing | A file the user specified does not exist | Confirm the target file and rerun |
| No target or scope | The user specified neither a file nor a scope | Specify a target file or scope and rerun |

## Workflow

### 1. Load standards

Read `codex/AGENTS.md` and use it as the only source of refactoring criteria. The relevant sections are:

- `Implementation Standards`
- `Performance`
- `TypeScript And React`
- `React`
- `Accessibility`
- `Verification`

### 2. Determine the target

Decide the target from the user input:

| Input | Action |
| --- | --- |
| One or more file paths | Analyze only those files |
| A directory | Analyze all `.ts` and `.tsx` files under it |
| "all" or unspecified scope | Analyze all `.ts` and `.tsx` files under `src/` |

Example of confirming the file list:

```bash
find src -name "*.ts" -o -name "*.tsx" | sort
```

### 3. Analysis criteria

Review the target against the standards in `codex/AGENTS.md`, in order.

**Implementation Standards**

- Magic numbers or magic strings -> extract into named constants.
- Repeated logic (DRY) -> extract into a shared function or helper.
- Functions doing more than one thing (single responsibility) -> split into smaller focused functions.
- Nested conditionals -> simplify with early returns or well-named helper functions.

**Performance**

- Heavy computation in render paths -> move out of render or memoize when it prevents a clear cost.
- O(n^2) lookups -> replace with `Map` or `Set`.

**TypeScript And React**

- `any` usage -> replace with `unknown`, generics, discriminated unions, or type guards (including callback parameters).
- `React.FC` -> replace with an explicit props interface.
- `enum` -> replace with an `as const` object plus a derived union type.
- `interface` vs `type` mix -> use `interface` for object contracts and `type` for unions or compositions.
- Inline object types -> extract into named `interface` or `type`.
- Exported utilities and shared helpers without explicit return types -> add explicit return types.
- Type-only imports without `import type` -> apply `import type`.
- Unsafe `as` assertions -> replace with a type guard or safe narrowing.
- Broad primitive types -> narrow to literal unions when the values are known.
- Functions with several related parameters -> group into an object parameter.
- `satisfies` opportunities -> validate object shape with `satisfies` while preserving literal types.

**Accessibility**

- Generic containers where semantic elements fit -> replace with the appropriate semantic element.
- Missing accessibility attributes (accessible names for icon-only controls, meaningful `alt`, accurate ARIA roles, names, and states) -> add them.

### 4. Proposal plan (approval before editing)

After analysis, and **before editing any code**, show the proposal list in this format and wait for approval:

```
Refactor plan — <target files or scope>

  1. [Implementation] <file>:<line> — <one-line summary>
  2. [TypeScript]      <file>:<line> — <one-line summary>
  3. [Accessibility]   <file>:<line> — <one-line summary>
  ...

Apply? y / n / number selection (e.g. "1, 3 only")
```

Act on the user response:

| Response | Action |
| --- | --- |
| `y` or "apply all" | Apply every item |
| Number selection ("1, 3 only", etc.) | Apply only those items, skip the rest |
| `n` or "cancel" | Exit without editing |
| Edit request for a specific item | Revise it, re-show the plan, and wait for approval again |

- Never edit files without approval.
- If there are no refactoring points, skip the plan step and print "No refactor targets" and exit.

### 5. Edit code

Edit files only for the approved items.

- Edit one file at a time, then move to the next.
- Do not make changes that affect runtime behavior.
- Limit changes to the approved items. Do not touch related but unapproved code.
- After editing, summarize the changed files and applied items.

### 6. Final response

**When changes were applied**

```
Refactor result : applied

Changed files : <count>
Applied items : <count>

1. [TypeScript]      src/components/UserCard.tsx:12 — any → User type
2. [Implementation]  src/components/UserCard.tsx:34 — magic string → ERROR_MESSAGE constant
3. [TypeScript]      src/hooks/useAuth.ts:8        — added explicit return type
```

**When there is nothing to refactor**

```
Refactor result : clean

Found no items that need refactoring against the project standards.
```

**When cancelled**

```
Refactor result : cancelled

Exited without changes.
```

## Failure Handling

| When | Action |
| --- | --- |
| Standards source read fails | Confirm `codex/AGENTS.md` exists and rerun |
| File analysis fails | Skip that file and continue with the rest |
| Edit fails | Report the failed item and its cause, and continue with the rest |

## Boundaries

- Do not propose anything not grounded in the project standards in `codex/AGENTS.md`.
- Do not change runtime behavior; limit changes to structure, type, and readability.
- Do not edit any file before the user approves the plan.
- Do not touch related but unapproved code, even when it is nearby.
