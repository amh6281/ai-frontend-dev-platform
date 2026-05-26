# Behavioral Guidelines

Use these rules to reduce common LLM coding mistakes.

## Think Before Coding

- State assumptions explicitly.
- Ask when ambiguity would make implementation risky.
- Surface tradeoffs when multiple interpretations exist.
- Push back when a simpler or safer approach is more appropriate.

## Simplicity First

- Implement only what was asked.
- Avoid abstractions for single-use code.
- Avoid speculative flexibility or configurability.
- Avoid unnecessary error handling for impossible scenarios.
- Simplify when the implementation is larger than the problem requires.

## Surgical Changes

- Touch only what is needed for the request.
- Do not improve adjacent code, comments, or formatting unless it directly supports the task.
- Match existing style.
- Remove only dead code created by the current change.
- Mention unrelated cleanup opportunities instead of changing them.

## Goal-Driven Execution

- Convert work into verifiable goals.
- For bug fixes, reproduce the bug when possible before fixing it.
- For refactors, ensure relevant tests pass before and after when practical.
- Loop until the requested behavior is implemented and verified, or clearly state the blocker.
