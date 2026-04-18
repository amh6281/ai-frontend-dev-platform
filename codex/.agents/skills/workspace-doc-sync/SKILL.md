---
name: workspace-doc-sync
description: Update workspace documentation after directory structure, tool-root boundaries, or Codex/Cursor configuration changes. Use when README, AGENTS, hooks, skills, or tool-specific folder layouts may be out of sync with the actual repository structure, especially when `codex/` and `cursor/` are treated as independent working roots.
---

# Workspace Doc Sync

## Overview

Align documentation with the real workspace layout before making claims about how Codex or Cursor discovers instructions, hooks, skills, commands, or rules.
Prefer updating the smallest set of files that restores consistency across root docs and tool-specific docs.

## Workflow

### 1. Inspect the real structure first

- Check which directories are the actual working roots for each tool.
- Confirm where instructions, hooks, skills, commands, rules, and agent configs live before editing any docs.
- Do not describe a path that is not present in the repository.

### 2. Resolve root-boundary rules explicitly

- State clearly whether the repository root is only an overview layer or an actual tool root.
- If `codex/` is the Codex root, keep Codex instruction discovery, hooks, and skills scoped to `codex/`.
- If `cursor/` is the Cursor root, keep Cursor instruction and settings scoped to `cursor/`.
- Avoid mixing Codex and Cursor path semantics in the same section unless the comparison is intentional.

### 3. Update the affected documents together

- When structure changes, update the relevant root `README.md` plus the tool-local `README.md`.
- When Codex discovery behavior changes, update `codex/AGENTS.md`, `codex/AGENTS.kr.md`, and `codex/README.md` together when needed.
- When skills or hooks are added, reflect both the physical path and the usage model in docs.
- Keep wording consistent across files so one document does not contradict another.

### 4. Prefer concrete usage language

- Explain whether a feature is automatic, explicit, or optional.
- For hooks, say they run automatically on lifecycle events.
- For skills, say they are explicitly invoked with `$skill-name` or selected implicitly by description matching.
- For AGENTS discovery, say exactly which directory is treated as the effective root.

### 5. Keep the final response operational

- Mention the files that changed.
- Mention whether verification was run.
- Call out any assumption about workspace roots or discovery behavior if it matters to the result.

## Common Targets

- Root `README.md`
- `codex/README.md`
- `cursor/README.md`
- `codex/AGENTS.md`
- `codex/AGENTS.kr.md`
- `codex/.codex/config.toml`
- `codex/.codex/hooks.json`
- `codex/.agents/skills/`

## Example Requests

- "폴더 구조 바뀌었으니 README랑 AGENTS 맞춰줘"
- "`codex/` 안이 실제 루트라는 기준으로 문서 다시 정리해줘"
- "hooks랑 skills 사용법까지 포함해서 Codex 문서 업데이트해줘"
- "Cursor와 Codex가 각자 독립 루트라는 점이 문서에 드러나게 맞춰줘"

## Boundaries

- Do not invent discovery behavior that is not supported by the current repository layout.
- Do not add extra docs that are not needed for keeping the workspace understandable.
- Do not create root-level Codex instruction files if the project defines `codex/` itself as the Codex root.
- Do not describe hooks and skills as the same mechanism.

This skill is instruction-only. Do not create `scripts/`, `references/`, or `assets/` unless the workflow later proves they are needed.
