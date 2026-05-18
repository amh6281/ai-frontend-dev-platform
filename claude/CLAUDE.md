# Claude Workspace Instructions

This file defines Claude-specific guidance for the `claude/` workspace.
When Claude starts inside `claude/`, treat this directory as the effective project root for instruction discovery.

## Discovery Notes

- Expected instruction file for this workspace: `/claude/CLAUDE.md`
- Keep Claude-specific guidance inside `claude/` so it stays isolated from Codex and Cursor configuration.
- If a future override file is introduced for Claude workflows, document its precedence here before relying on it.

## Working Agreements

- Keep changes narrowly scoped to the task and preserve unrelated behavior.
- Verify the current code before proposing or changing behavior.
- Prefer the smallest defensible change over broad refactors.
- Keep summaries focused on the actual change, risk, and verification.
- Treat `claude/` as the active workspace root when resolving local documentation and config paths.

## Collaboration

- Treat planning, design, code mapping, frontend implementation, documentation research, review, security review, accessibility review, performance review, and test engineering as separate modes of work.
- Do read-heavy code path discovery before implementation when ownership or execution flow is unclear.
- Verify framework or API behavior against official documentation when the behavior is uncertain or likely to have changed.
- Give extra scrutiny to changes touching secrets, auth, permissions, unsafe rendering, dependencies, or sensitive data boundaries.
- Make assumptions, risks, and open questions explicit when handing work across modes of work.
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
- Preserve visible focus indicators and predictable tab order.
- Use native form controls, labels, validation messages, and disabled states whenever possible.
- Manage focus for dialogs, popovers, routed views, validation errors, and async updates.
- Announce loading, success, error, and status changes when they are not visually persistent.
- Keep text, controls, and interactive targets usable across responsive layouts and zoom.
- Respect reduced-motion preferences for non-essential animation.
- Check contrast for text, icons, focus rings, borders that convey state, and disabled-but-readable content.
- Prefer native HTML behavior before adding ARIA; when ARIA is needed, keep roles, names, and states accurate.
- Include accessibility verification for user-facing changes, at least with keyboard navigation and relevant screen reader expectations.

## Security

- Do not expose secrets, tokens, API keys, credentials, private keys, or sensitive user data in code, logs, URLs, client bundles, or documentation.
- Treat environment variables as public when they are intentionally exposed to the client, and keep server-only values behind server-only boundaries.
- Avoid unsafe HTML injection and user-controlled DOM sinks; sanitize or avoid rendering untrusted markup.
- Keep authentication, authorization, role, tenant, and permission assumptions explicit when changing protected flows.
- Do not store sensitive tokens in browser storage unless the product architecture explicitly requires it and the risk is understood.
- Avoid logging sensitive request, response, session, or user data.
- Review dependency additions and package scripts for supply-chain, bundle, and security implications.
- Include security verification when changing auth, permissions, secret handling, external input parsing, redirects, downloads, uploads, or dependency boundaries.

## Verification

- Verify the exact behavior you changed.
- Add or update tests when fixing bugs or changing stable behavior.
- Prefer readable tests that cover edge cases and failure paths.
- Do not claim behavior is verified unless it was actually checked.
- Mention the changed file paths or key artifacts in the final response.
