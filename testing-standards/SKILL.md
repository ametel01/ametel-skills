---
name: testing-standards
description: Use this skill when adding or changing tests in ametel01 repos, including Bun/Vitest/Playwright, Go tests, pytest, unittest, Cairo snforge tests, regression coverage, deterministic fixtures, test markers, race tests, or e2e checks.
---

# Testing Standards

## Purpose

Add focused, deterministic tests that match each repo's test runner and risk level. Test tooling varies, but the shared pattern is to cover behavior changes and run the target repo's canonical checks.

## When to use

Use for bug fixes, behavior changes, CLI changes, API contracts, data ingest logic, contract logic, UI workflows, or refactors that need regression protection.

## Evidence from repositories

Strength: Strong.

- `agents-toolbelt`: `CONTRIBUTING.md` requires tests for new packages and non-trivial behavior changes; tests use Go `testing`, many `t.Parallel()`, fakes, temp dirs, and race tests via `make test`.
- `weld-cli`: `pyproject.toml` defines pytest markers `unit`, `cli`, `integration`, `slow`; docs require tests and type hints; test suite uses `CliRunner`, `tmp_path`, async markers, and regression tests.
- `vitals-db`: `package.json` uses `bun test`; changelog release gates cite targeted test runs plus typecheck/build.
- `claw-training-dashboard`: scripts split unit, integration, and e2e tests; uses Vitest, Supertest, Testing Library, and Playwright.
- `horizon-starknet`: contracts use snforge tests; `docs/TEST_QUALITY_AUDIT.md` emphasizes deterministic tests, observable behavior, isolated state, focused assertions, and actionable failures.
- `orgs-ai-harness`: Python `unittest` tests exercise validation, registry, onboarding, and redaction behaviors.

## Standard workflow

1. Read nearby tests before editing production code.
2. Add or update focused tests for changed behavior.
3. Use repo-native helpers and fixtures instead of inventing a new harness.
4. Prefer observable behavior over internal implementation details.
5. Run the smallest relevant test first, then the aggregate gate if feasible.

## Commands

```bash
# Bun repos
bun test
bun run test:unit
bun run test:integration
bun run test:e2e

# Go
make test
make verify

# Python with uv
uv run pytest tests/path_or_test.py -v
make test
make ci

# Minimal Python package without uv
python -m unittest

# Cairo
cd contracts
snforge test
SNFORGE_BACKTRACE=1 snforge test
```

## Required checks

- Bug fixes should include regression coverage where practical.
- API or DTO changes need tests at the query/server boundary and docs updates when contracts change.
- CLI changes need command-level tests, not just pure function tests.
- UI workflow changes need component tests or Playwright when behavior spans browser interaction.
- Contract changes need snforge tests covering success and failure paths.

## Invariants

- Keep tests deterministic. Avoid real network, clock, machine state, and shared global state unless explicitly controlled.
- Use temp dirs, fakes, fixtures, or mock servers for filesystem and external integration behavior.
- Keep tests parallelizable unless they mutate process-global state such as env vars, cwd, or blockchain cheat state.
- Use actionable assertions that show what behavior failed.
- Do not lower coverage thresholds, remove race tests, or skip security-sensitive tests to pass locally; if the user explicitly approves replacing coverage, validate the replacement against the same failure mode before finishing.

## Common pitfalls

- In Go, forgetting `t.Parallel()` where the package pattern expects it, or using real process state instead of fakes.
- In `weld-cli`, omitting pytest markers for unit, CLI, integration, or slow tests when adding new categories.
- In `claw-training-dashboard`, running only unit tests when server/API or Playwright behavior changed.
- In Cairo tests, relying on broad approximate equality or hidden internal state when public behavior can be asserted.
- In data ingest repos, using nondeterministic timestamps or real personal data fixtures.

## Exceptions

If a repo has no aggregate test command, run the runner visible in existing tests and report the limitation. For very expensive e2e suites, run focused lower-level tests and state the skipped e2e gate.
