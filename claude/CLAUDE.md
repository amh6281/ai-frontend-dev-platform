# Claude Workspace Instructions

This file defines Claude-specific guidance for the `claude/` workspace.
When Claude starts inside `claude/`, treat this directory as the effective project root for instruction discovery.

## Discovery Notes

- Expected instruction file for this workspace: `/claude/CLAUDE.md`
- Keep Claude-specific guidance inside `claude/` so it stays isolated from Codex and Cursor configuration.
- Detailed Claude rule files live in `/claude/.claude/rules/`.
- Cursor code quality, TypeScript, React, testing, accessibility, and LLM behavior rules have been adapted into Claude rule files.
- If a future override file is introduced for Claude workflows, document its precedence here before relying on it.

## Rule Files

- `.claude/rules/code-quality.md` — code quality, workflow, comments, maintenance, and performance rules.
- `.claude/rules/typescript.md` — TypeScript type safety and API conventions.
- `.claude/rules/react.md` — React component, state, effect, rendering, form, and event rules.
- `.claude/rules/accessibility.md` — semantic HTML, names, keyboard, focus, announcements, contrast, and verification.
- `.claude/rules/testing.md` — test intent, placement, UI testing, async reliability, mocks, and verification reporting.
- `.claude/rules/karpathy-guidelines.md` — LLM behavior guidance for simplicity, surgical changes, assumptions, and verification goals.

## Working Agreements

- Keep changes narrowly scoped to the task and preserve unrelated behavior.
- Verify the current code before proposing or changing behavior.
- Prefer the smallest defensible change over broad refactors.
- State assumptions and tradeoffs explicitly when the request has multiple plausible interpretations.
- Ask before implementing when ambiguity would make the change risky.
- Keep summaries focused on the actual change, risk, and verification.
- Treat `claude/` as the active workspace root when resolving local documentation and config paths.
- Provide links to real changed files when summarizing work.

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
- Keep related code together and follow existing file and folder naming conventions.
- Hide implementation details behind clear interfaces.
- Move nested conditionals into well-named functions when that improves readability.
- Avoid speculative cleanup unrelated to the task.
- Match the existing local style, even when another style would also be valid.
- Remove imports, variables, functions, or files made unused by the current change.

## Performance

- Avoid unnecessary O(n^2) operations; prefer `Map` or `Set` for repeated lookups.
- Keep expensive calculations out of render paths.
- Use memoization only when it prevents a measured or clearly plausible cost.
- Prefer pagination, filtering, or virtualization for large collections.

## TypeScript And React

- Never introduce `any`.
- Prefer `unknown`, generics, discriminated unions, and type guards.
- Do not use `React.FC`; use explicit props interfaces instead.
- Prefer `as const` with union types over `enum`.
- Use `interface` for object contracts and `type` for unions or compositions.
- Prefer named types over large inline object types.
- Add explicit return types to exported utilities and shared helpers.
- Use `import type` for type-only imports.
- Prefer `readonly` for immutable data.
- Prefer narrow literal unions over broad primitive types.
- Prefer object parameters when a function accepts several related values.
- Use exhaustive `never` checks for discriminated unions and switch-style state handling.
- Use `satisfies` when validating object shape while preserving literal types.
- Avoid unsafe assertions when a guard or safe narrowing can express the same intent.

## React

- Keep components focused on one responsibility: layout, data wiring, or reusable UI behavior.
- Prefer composition over large prop-driven components with many conditional branches.
- Do not introduce shared components until at least two real call sites need the same behavior.
- Keep domain-specific components close to their feature unless the project already has a shared component convention.
- Prefer existing design-system primitives, tokens, variants, and interaction patterns before creating new UI primitives.
- Store the minimum state needed to render the UI.
- Derive cheap deterministic values during render instead of duplicating them in state.
- Prefer discriminated unions for async and multi-step UI states.
- Keep loading, empty, error, success, disabled, and optimistic states explicit when users can observe them.
- Do not use `useEffect` for values that can be derived during render.
- Keep effects tied to external synchronization such as subscriptions, timers, network calls, browser APIs, or imperative integrations.
- Include all required effect dependencies; restructure code instead of suppressing dependency rules.
- Clean up subscriptions, timers, listeners, and async work that can outlive the component.
- Keep list keys stable and tied to item identity, not array index, when order can change.
- Prefer controlled form fields when validation, formatting, or conditional UI depends on the value.
- Prevent duplicate submits during pending states.
- Handle async event failures with visible user feedback.

## Accessibility

- Prefer semantic elements over generic containers.
- Use landmarks such as `header`, `nav`, `main`, `section`, `article`, `aside`, and `footer` when they match the content.
- Keep heading levels meaningful and ordered.
- Keep keyboard interaction intact for interactive UI.
- Ensure icon-only controls have accessible names.
- Associate form inputs with labels.
- Connect helper text, constraints, and validation errors with `aria-describedby` when needed.
- Mark invalid fields with `aria-invalid`.
- Provide meaningful `alt` text for informative images.
- Use empty `alt=""` for decorative images.
- Do not rely on color alone to communicate meaning.
- Preserve visible focus indicators and predictable tab order.
- Use native form controls, labels, validation messages, and disabled states whenever possible.
- Manage focus for dialogs, popovers, routed views, validation errors, and async updates.
- Let Escape close dismissible overlays when that is the expected platform behavior.
- Avoid keyboard traps unless the UI is an active modal that intentionally contains focus.
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
- Follow the project's existing test location, naming, runner, and helper conventions.
- Test user-observable behavior rather than implementation details.
- Prefer accessible roles, labels, visible text, placeholder text, and alt text before test IDs.
- Cover loading, empty, error, success, disabled, and validation states when changed behavior depends on them.
- Await async UI updates through the test framework's recommended utilities.
- Avoid arbitrary sleeps and timer delays unless the behavior specifically depends on time.
- Keep tests deterministic by controlling dates, randomness, network responses, storage, and timers when needed.
- Clean up mocks, listeners, and global mutations between tests.
- Do not claim behavior is verified unless it was actually checked.
- Mention the changed file paths or key artifacts in the final response.
