# Codex Workspace AGENTS

This file defines Codex-specific guidance for the `codex/` workspace.
When Codex starts inside `codex/`, treat this directory as the effective project root for instruction discovery.

## Discovery Notes

- Expected instruction chain for this workspace: `/codex/AGENTS.md`
- If a future `AGENTS.override.md` exists inside `codex/`, it takes precedence over this file.
- Fallback filenames are configured in `.codex/config.toml` and only apply when `AGENTS.override.md` and `AGENTS.md` are absent inside this workspace root.

## Working Agreements

- Keep changes narrowly scoped to the task and preserve unrelated behavior.
- Verify the current code before proposing or changing behavior.
- Prefer the smallest defensible change over broad refactors.
- Keep summaries focused on the actual change, risk, and verification.
- Treat `codex/` as the active workspace root when resolving local documentation and config paths.

## Collaboration

- Treat planner, designer, code mapper, frontend engineer, docs researcher, reviewer, security reviewer, accessibility reviewer, performance reviewer, and test engineer as separate roles.
- Use `code_mapper` for read-heavy code path discovery before implementation when the ownership or execution path is unclear.
- Use `docs_researcher` when framework or API behavior should be verified against official documentation before changing code.
- Use `security_reviewer` when changes touch secrets, auth, permissions, unsafe rendering, dependencies, or sensitive data boundaries.
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

## Feature-Sliced Design (FSD)

- Decide which layer a module belongs to before writing it.
- Use the layer order `app > pages > widgets > features > entities > shared`; a module may import only from layers strictly below it.
- Never let a lower layer import a higher layer, and forbid sideways imports between slices on the same layer.
- When sibling slices need shared logic, lift it to a lower layer (`shared`, or `entities` for domain logic) instead of importing sideways.
- Expose each slice and segment through an `index.ts` Public API and import other slices only through it, never their internal files.
- Organize a slice into `ui`, `model`, `api`, `lib`, and `config` segments by technical purpose.
- Colocate component-specific state, types, hooks, and helpers with the code that uses them.
- Extract to `shared` only when logic is domain-agnostic and duplicated across at least three real call sites; prefer `entities` for reused domain logic.
- Match existing FSD conventions before introducing new patterns, and avoid forcing a full restructure as part of an unrelated task.

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
