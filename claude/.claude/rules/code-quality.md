# Code Quality Rules

Use these rules when writing, reviewing, or modifying code.

## Workflow

- Make changes narrowly and file by file.
- Verify information before presenting it.
- Preserve existing behavior and unrelated code.
- Do not suggest changes when no actual modification is needed.
- Link to real files when summarizing work.

## Code Quality

- Replace meaningful hard-coded values with named constants.
- Prefer names that explain intent over shorthand.
- Keep functions small and focused on one responsibility.
- Extract repeated logic into reusable functions or shared abstractions.
- Keep related code together and follow existing file and folder conventions.
- Hide implementation details behind clear interfaces.
- Move nested conditionals into well-named functions when that improves readability.

## Performance

- Avoid unnecessary O(n^2) operations.
- Prefer `Map` or `Set` for repeated lookups.
- Keep expensive calculations out of render paths.
- Memoize only when it prevents a measured or clearly plausible cost.

## Comments

- Prefer self-documenting code over comments that repeat what the code does.
- Use comments to explain why code exists, non-obvious side effects, APIs, or complex algorithms.

## Maintenance

- Refactor only when it supports the current task.
- Remove imports, variables, functions, or files made unused by the current change.
- Mention unrelated dead code or cleanup opportunities instead of changing them without being asked.
