# Feature-Sliced Design (FSD) Rules

Use these rules when creating, moving, importing, or refactoring any frontend module. Decide which layer a module belongs to before writing it, and keep imports flowing in one direction.

## Layer Hierarchy

- Use the standard layer order, highest to lowest: `app > pages > widgets > features > entities > shared`.
- A module may import only from layers strictly below it.
- A lower layer must never import from a higher layer (`shared` never imports `entities`, `entities` never imports `features`, and so on).
- Place each module on the lowest layer that still expresses its real responsibility:
  - `app` — routing, providers, global styles, app-wide setup.
  - `pages` — full route screens composed from widgets, features, and entities.
  - `widgets` — self-contained UI blocks that combine features and entities.
  - `features` — user actions and interactions that deliver product value.
  - `entities` — business domain models and their basic UI/representation.
  - `shared` — reusable, domain-agnostic UI, lib, config, and API helpers.

## Import Direction And Slice Isolation

- Forbid sideways imports between slices on the same layer (a feature must not import another feature; a widget must not import another widget).
- When two slices on the same layer need to share logic, lift it to a lower layer (`shared`, or `entities` when it is domain logic) instead of importing sideways.
- Keep each slice independent so it can be understood, moved, or removed without editing sibling slices.
- If an import would point upward or sideways, treat it as a violation and refactor before continuing.

## Public API

- Expose every slice and segment through an `index.ts` Public API at its root.
- Import other slices only through their Public API; never reach into their internal files.
- Re-export only what other layers genuinely need; keep internal files private to the slice.
- Do not create import paths that dig into another slice's `ui`, `model`, `lib`, or `api` internals directly.

## Slice And Segment Structure

- Within a slice, organize code into standard segments by technical purpose:
  - `ui` — components and presentation.
  - `model` — state, stores, business logic, and types.
  - `api` — requests, data fetching, and mappers.
  - `lib` — slice-local helpers.
  - `config` — slice-local constants and configuration.
- `shared` and `app` may be organized by segments directly, since they are not split into business slices.
- Keep segment names consistent so slices stay predictable across the codebase.

## Colocation

- Keep component-specific state, types, hooks, and helpers in the same slice or segment as the code that uses them.
- Do not promote logic to a lower layer until it is actually reused.
- Keep a module's tests and styles next to the module unless the project already has a different convention.

## Extraction And Reuse

- Extract logic to `shared` only when it is domain-agnostic and duplicated across at least three real call sites.
- Extract domain logic to `entities` when multiple features or widgets depend on the same business model.
- Prefer keeping logic local and duplicated twice over a premature abstraction that couples unrelated slices.
- When extracting, expose the result through the target layer's Public API and update callers to import from it.

## Working With Existing Code

- Match the project's existing FSD conventions for layer names, slice naming, and segment layout before introducing new patterns.
- If the project does not yet follow FSD, keep changes narrowly scoped and do not force a full restructure as part of an unrelated task.
- When a change reveals an FSD violation in touched code, surface it and prefer the smallest fix that restores correct import direction.
