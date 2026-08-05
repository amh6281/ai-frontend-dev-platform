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

## Performance

- Identify the actual bottleneck before optimizing, and optimize only for a measured or clearly plausible cost.
- Avoid unnecessary O(n^2) operations; prefer `Map` or `Set` for repeated lookups.
- Keep expensive calculations out of render paths.
- Use memoization only when it prevents a measured or clearly plausible cost, and keep referential identity stable for memoized subtrees.
- Throttle or debounce high-frequency events such as scroll, resize, pointer move, and typing.
- Prefer pagination, filtering, or virtualization for large collections.
- Start independent requests in parallel, deduplicate repeated ones, and cancel or ignore stale responses.
- Check bundle impact before adding a dependency, and split heavy routes, dialogs, editors, and charts behind dynamic imports.
- Reserve space for async content so loading does not shift layout.
- State what was measured and the before and after numbers when claiming a performance improvement.

## TypeScript And React

- Never introduce `any`.
- Prefer `unknown`, generics, discriminated unions, and type guards.
- Do not use `React.FC`; use explicit props interfaces instead.
- Prefer `as const` with union types over `enum`.
- Use `interface` for object contracts and `type` for unions or compositions.
- Add explicit return types to exported utilities and shared helpers.
- Use `import type` for type-only imports.
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

## Writing Style

Apply to any prose you produce: code comments, documentation, commit messages, PR descriptions, UI copy, and responses. Korean patterns are adapted from the im-not-ai AI-tell taxonomy (https://github.com/epoko77-ai/im-not-ai).

- Preserve meaning: never change facts, numbers, proper nouns, or direct quotes to fix style; edit only spans that read as an AI tell.
- Do not over-edit: keep the genre and register, and stop once the tell is gone.
- English: do not use em dashes (—) or en dashes (–) as sentence punctuation; use commas, parentheses, colons, or separate sentences.
- English: cut hype words (seamless, robust, powerful, leverage, delve, dive in, elevate, unlock, supercharge, game-changer); prefer "use" over "leverage" and "explore" over "delve into".
- English: drop filler openers ("It's worth noting", "It's important to note") and empty closers ("In conclusion", "Overall", "In summary"), and avoid "not just X, but Y".
- Korean: 번역투를 줄입니다 — "~를 통해" → "~로", "~에 대해" → "~을", "~에 있어서" → "~에서 / ~할 때", "~되어진다" → "~된다".
- Korean: AI 관용구("결론적으로", "시사하는 바가 크다", "주목할 만하다", "혁신적인")와 완곡 표현("~할 수 있을 것으로 보인다")을 걷어냅니다.
- Korean: 기계적 병렬("첫째 / 둘째 / 셋째"), 문두 접속사("또한 / 따라서 / 즉") 연속, 형식명사("~하는 것이다", "~할 필요가 있다"), 대시(—) 남발을 피합니다.
- Do not lean on bold, headings, bullet lists, or emoji where a plain sentence is clearer; match the voice of existing comments, docs, and copy, and never add meta references to being an AI or language model.
