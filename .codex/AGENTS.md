# Codex Workspace Guidance

## Scope

- This directory contains Codex-specific configuration, agent definitions, and workflows.
- Keep repository-wide behavior rules in the root `AGENTS.md`, not duplicated in agent prompts.

## Editing Rules

- Prefer small, reviewable changes to Codex configuration.
- Preserve existing agent names, models, and nicknames unless the task requires changing them.
- Keep `developer_instructions` focused on role-specific behavior.
- Do not restate repository-wide coding rules inside each agent file when inherited guidance already covers them.
- When adding new Codex config, choose names and structure that match the official `AGENTS.md` discovery model.
