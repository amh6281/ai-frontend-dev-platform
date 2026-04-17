# Agent Definitions

## Intent

- Files in this directory define role-specific behavior for Codex sub-agents.
- Each agent should inherit shared repository guidance through the `AGENTS.md` chain.

## Prompt Design Rules

- Keep each agent prompt centered on its unique responsibility.
- Describe expected output shape, constraints, and non-goals clearly.
- Avoid copying shared coding standards or general workflow rules into every agent.
- Use `sandbox_mode` to reflect the role's true responsibility: read-only for planning, design, and review; write access only for implementation roles.
