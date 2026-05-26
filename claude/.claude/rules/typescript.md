# TypeScript Rules

Use these rules for TypeScript files.

## Type Safety

- Never introduce `any`.
- Prefer `unknown`, generics, discriminated unions, and type guards.
- Avoid unsafe type assertions when a guard or safe narrowing can express the same intent.
- Prefer type predicates when handling `unknown`.
- Prefer narrow literal unions over broad primitive types.
- Use exhaustive `never` checks for discriminated unions and switch-style state handling.

## Type Shape

- Use `interface` for object contracts.
- Use `type` for unions, intersections, and compositions.
- Prefer named types over large inline object types.
- Prefer `readonly` for immutable data.
- Prefer object parameters when a function accepts several related values.
- Use built-in utility types such as `Partial`, `Pick`, `Omit`, `Record`, `ReturnType`, and `Parameters` when they fit.

## Constants

- Prefer `as const` with union types over `enum`.
- Use `satisfies` when validating object shape while preserving literal types.
- Avoid magic strings by defining named constant objects or arrays.

## Imports And APIs

- Use `import type` for type-only imports.
- Add explicit return types to exported utilities and shared helpers.
- Keep types close to their domain and follow the project’s existing type location conventions.
