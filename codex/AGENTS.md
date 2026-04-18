# Project AGENTS

This is the primary Codex instruction file for this repository.
Keep project-wide guidance here unless a future subdirectory truly needs its own override.

## Working Agreements

- Keep changes narrowly scoped to the task and preserve unrelated behavior.
- Verify the current code before proposing or changing behavior.
- Prefer the smallest defensible change over broad refactors.
- Keep summaries focused on the actual change, risk, and verification.

## Collaboration

- Treat planner, designer, frontend engineer, and reviewer as separate roles.
- Make assumptions, risks, and open questions explicit when handing work across roles.
- Prioritize correctness, regressions, accessibility, and missing verification over style-only feedback.

## Implementation Standards

- Replace meaningful hard-coded values with named constants.
- Prefer names that explain intent over shorthand.
- Prefer small functions with one clear responsibility.
- Extract repeated logic instead of copying behavior across files.
- Avoid speculative cleanup unrelated to the task.

## TypeScript And React

- Never introduce `any`.
- Prefer `unknown`, generics, discriminated unions, and type guards.
- Do not use `React.FC`; use explicit props interfaces instead.
- Prefer `as const` with union types over `enum`.
- Use `interface` for object contracts and `type` for unions or compositions.
- Add explicit return types to exported utilities and shared helpers.
- Use `import type` for type-only imports.
- Avoid unsafe assertions when a guard or safe narrowing can express the same intent.

## Accessibility

- Prefer semantic elements over generic containers.
- Keep keyboard interaction intact for interactive UI.
- Ensure icon-only controls have accessible names.
- Provide meaningful `alt` text for informative images.
- Do not rely on color alone to communicate meaning.

## Verification

- Verify the exact behavior you changed.
- Add or update tests when fixing bugs or changing stable behavior.
- Prefer readable tests that cover edge cases and failure paths.
- Do not claim behavior is verified unless it was actually checked.
