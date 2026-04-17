# Codex Coding Rules

Codex works from a separate rule set from Cursor.
This document defines the default coding behavior for Codex agents in this repository.

These rules are optimized for implementation, review, and multi-agent coordination.

## 1. Working Style

- Verify the current code before proposing or changing behavior.
- Change only the files needed for the task.
- Preserve unrelated logic, structure, and user-visible behavior.
- Prefer the smallest defensible change over broad refactors.
- Keep changes easy to review and easy to revert.

## 2. Collaboration

- Treat planner, designer, frontend engineer, and reviewer as separate roles with separate responsibilities.
- Do not mix planning, design, implementation, and review output unless the task requires it.
- When handing work across roles, make assumptions and risks explicit.
- When reviewing, prioritize correctness, regressions, accessibility, and missing verification over style-only feedback.

## 3. Code Quality

- Replace hard-coded business values with named constants when they carry meaning.
- Use names that explain intent, not shorthand that hides it.
- Prefer small functions with one clear responsibility.
- Extract repeated logic instead of copying behavior across files.
- Hide implementation details behind clear interfaces or helper functions.
- Avoid speculative cleanup that is unrelated to the task.

## 4. TypeScript and React

- Never introduce `any`.
- Prefer `unknown`, generics, discriminated unions, and type guards.
- Do not use `React.FC`; use explicit props interfaces instead.
- Prefer `as const` with union types over TypeScript `enum`.
- Use `interface` for object contracts and `type` for unions or compositions.
- Prefer named types over large inline object annotations.
- Add explicit return types to exported utilities and shared helpers.
- Use `import type` for type-only imports.
- Prefer narrow types over broad `string` or `boolean` shapes when the domain is known.
- Avoid unsafe assertions when a guard or safe narrowing can express the same intent.

## 5. Rendering and Performance

- Keep expensive computation out of render paths.
- Avoid repeated linear lookups when `Map` or `Set` would simplify the logic.
- Avoid unnecessary nested loops.
- Memoize only when the computation or re-render cost justifies it.

## 6. Accessibility and HTML

- Prefer semantic elements over generic containers.
- Use real interactive elements such as `button`, `a`, and form controls.
- Ensure icon-only controls have accessible names.
- Provide meaningful `alt` text for informative images.
- Keep keyboard interaction and focus behavior intact when changing UI.
- Do not rely on color alone to communicate status or meaning.

## 7. Comments and Documentation

- Write code that explains what it does through structure and naming.
- Use comments only for non-obvious intent, constraints, or tradeoffs.
- Do not add comments that merely restate the code.
- Document side effects and risky assumptions when they are not obvious from the API.

## 8. Testing and Verification

- Verify the exact behavior you changed.
- Add or update tests when fixing bugs or changing stable behavior.
- Prefer readable tests that cover edge cases and failure paths.
- Do not claim behavior is verified unless it was actually checked.

## 9. Response Discipline

- Do not speculate about implementation details that were not verified.
- Do not suggest edits when no file change is needed.
- Keep summaries focused on the actual change, risk, and verification.
- Use real repository file paths when referencing changed files.
