# React Rules

Use these rules when building, reviewing, or refactoring React components, hooks, pages, and user-facing interactions.

## Components

- Do not use `React.FC`; use explicit props interfaces instead.
- Keep components focused on one responsibility: layout, data wiring, or reusable UI behavior.
- Prefer composition over large prop-driven components with many conditional branches.
- Do not introduce shared components until at least two real call sites need the same behavior.
- Keep domain-specific components close to their feature unless the project already has a shared component convention.
- Prefer existing design-system primitives, tokens, variants, and interaction patterns before creating new UI primitives.

## State

- Store the minimum state needed to render the UI.
- Derive cheap deterministic values during render instead of duplicating them in state.
- Avoid duplicating props in state unless the component intentionally owns an editable draft.
- Prefer discriminated unions for async and multi-step UI states.
- Keep loading, empty, error, success, disabled, and optimistic states explicit when users can observe them.

## Effects

- Do not use `useEffect` for values that can be derived during render.
- Keep effects tied to external synchronization such as subscriptions, timers, network calls, browser APIs, or imperative integrations.
- Include all required dependencies; restructure code instead of suppressing dependency rules.
- Clean up subscriptions, timers, listeners, and async work that can outlive the component.
- Avoid effect chains where one effect only sets state for another effect.

## Rendering

- Avoid expensive work inside render paths for large lists or high-frequency updates.
- Use `useMemo`, `useCallback`, and `React.memo` only when they prevent a measured or clearly plausible cost.
- Prefer pagination, filtering, or virtualization for large collections.
- Keep list keys stable and tied to item identity, not array index, when order can change.

## Forms And Events

- Prefer controlled form fields when validation, formatting, or conditional UI depends on the value.
- Keep validation messages connected to the relevant fields.
- Prevent duplicate submits during pending states.
- Handle async event failures with visible user feedback.
- Use semantic buttons and links for actions and navigation.
