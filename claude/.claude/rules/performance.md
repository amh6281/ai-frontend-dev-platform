# Performance Rules

Use these rules when a change affects rendering, data loading, bundle size, or high-frequency interaction. Optimize against a real cost, not a guess.

## Measure Before Optimizing

- Identify the actual bottleneck before changing code: profiler, network panel, or bundle report.
- Optimize only for a measured cost or a clearly plausible one.
- Do not add complexity for gains users cannot perceive.
- State the baseline and the observed change when reporting a performance fix.

## Rendering

- Keep expensive calculations out of render paths.
- Avoid unnecessary O(n^2) work; prefer `Map` or `Set` for repeated lookups.
- Use `useMemo`, `useCallback`, and `React.memo` only when they prevent a measured or clearly plausible cost.
- Keep referential identity stable for values passed into memoized subtrees; memoizing the child while recreating its props does nothing.
- Prefer moving state down or passing content as children over wrapping large trees in memoization.
- Throttle or debounce high-frequency events such as scroll, resize, pointer move, and typing.
- Avoid layout thrash: batch DOM reads before writes, and animate `transform` and `opacity` rather than layout properties.
- Prefer pagination, filtering, or virtualization for large collections.

## Data Loading

- Fetch on the boundary that owns the data instead of repeating the request in every consumer.
- Start independent requests in parallel; avoid waterfalls caused by sequential awaits.
- Deduplicate and cache repeated requests instead of refetching on every render or mount.
- Cancel or ignore stale responses when inputs change or the component unmounts.
- Justify polling intervals; prefer events or subscriptions when the backend supports them.
- Request only the fields and page size the UI actually renders.

## Assets And Bundle

- Check bundle impact before adding a dependency, especially when only one helper is needed.
- Split heavy routes, dialogs, editors, charts, and rich text libraries behind dynamic imports.
- Import specific modules rather than pulling a whole package through a barrel that defeats tree shaking.
- Serve images at their rendered size with modern formats, explicit dimensions, and lazy loading below the fold.
- Subset and preload fonts, and avoid layout shift from late font swaps.
- Keep third-party scripts deferred and off the critical rendering path.

## Perceived Performance

- Reserve space for async content so loading does not shift layout.
- Give feedback within the interaction budget: pending state, skeleton, or disabled control.
- Keep the main thread free during interaction and move heavy work off the critical path.
- Use optimistic updates when the failure path is recoverable and visible to the user.

## Verification

- State what was measured, how it was measured, and the before and after numbers.
- Confirm that memoization, virtualization, or lazy loading did not regress behavior, focus, or accessibility.
- Say explicitly when a performance change is a judgment call that was not measured.
