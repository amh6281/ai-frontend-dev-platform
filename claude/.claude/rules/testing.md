# Testing Rules

Use these rules when adding tests, fixing bugs, changing stable behavior, or verifying frontend flows.

## Test Intent

- A test should protect behavior that users, integrations, or future maintainers rely on.
- Bug fixes should include a failing reproduction test when the project has a suitable test setup.
- Avoid tests that only assert implementation details, private state, or incidental markup.
- Prefer a small number of meaningful tests over broad snapshot churn.

## Placement

- Follow the project's existing test location, naming, runner, and helper conventions.
- Keep unit tests close to pure utilities and component tests close to user-facing behavior.
- Put cross-module behavior in integration tests when unit tests would over-mock the real contract.
- Do not add a new test framework unless the task explicitly requires it.

## UI Testing

- Prefer user-level interactions such as click, keyboard, typing, focus, submit, and navigation.
- Query by accessible role, label, placeholder, text, or alt text before using test IDs.
- Cover loading, empty, error, success, disabled, and validation states when changed behavior depends on them.
- Verify accessible names and focus behavior for icon-only controls, dialogs, menus, and forms.

## Async And Reliability

- Await async UI updates through the test framework's recommended utilities.
- Avoid arbitrary sleeps and timer delays unless the behavior specifically depends on time.
- Keep tests deterministic by controlling dates, randomness, network responses, storage, and timers when needed.
- Clean up mocks, listeners, and global mutations between tests.

## Mocks And Fixtures

- Mock external boundaries such as network, browser APIs, storage, and time.
- Avoid mocking the unit under test or the behavior the test is supposed to prove.
- Keep fixtures small, named, and focused on the scenario.
- Include edge cases for invalid input, missing data, permission failures, and rejected promises when relevant.

## Verification Reporting

- State which test, lint, type, build, or manual checks were run.
- If verification could not run, say so explicitly and include the reason.
- Do not claim a flow is verified unless it was actually exercised.
