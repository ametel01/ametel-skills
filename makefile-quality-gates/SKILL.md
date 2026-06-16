---
name: makefile-quality-gates
description: Use this skill when an ametel01 repo has a Makefile with verify, ci, check, test, lint, build, docs, security, or release targets. Prefer canonical Make targets and keep Makefile, CI, and contributor docs aligned when quality gates change.
---

# Makefile Quality Gates

## Purpose

Use Makefiles as the local contract for verification where the repo defines them. The exact stack varies, but Make targets encode the intended gate.

## When to use

Use in repos with `Makefile`, especially `agents-toolbelt`, `weld-cli`, and `horizon-starknet`.

## Evidence from repositories

Strength: Moderate.

- `agents-toolbelt`: `Makefile` defines `verify: check-go fmt vet lint test build vulncheck`; CI runs `make verify`.
- `weld-cli`: `Makefile` defines setup, lint, format, typecheck, security, `check`, `ci`, docs, build, and release targets; CI mirrors uv/Ruff/Pyright/pytest/security commands.
- `horizon-starknet`: `Makefile` defines Docker dev targets plus `build` and `test` for contracts.
- Repos without Makefile: `vitals-db`, `claw-training-dashboard`, and `orgs-ai-harness` require package or Python-specific detection instead.

## Standard workflow

1. Run `make help` or read the Makefile before choosing commands.
2. Use individual targets while iterating.
3. Use the aggregate gate before finishing when feasible:
   - `make verify` in `agents-toolbelt`
   - `make ci` or `make check` plus tests in `weld-cli`
   - `make build` and `make test` for `horizon-starknet` contracts
4. If you alter gates, update the Makefile, CI workflow, and contributing docs together.

## Commands

```bash
# agents-toolbelt
make verify
make test
make lint
make vulncheck

# weld-cli
make check
make test
make security
make ci
make docs-build

# horizon-starknet
make build
make test
make dev-up
make dev-down
```

## Required checks

- For Go changes in `agents-toolbelt`, `make verify` is canonical.
- For Python changes in `weld-cli`, run at least `make check` and relevant tests; `make ci` is the full local gate.
- For contract changes in `horizon-starknet`, run Scarb build/test targets, or direct `cd contracts` commands if faster.

## Invariants

- Do not bypass Makefile-managed local tool installation in `agents-toolbelt`; linters are pinned under `.tools/bin`.
- Do not weaken aggregate gates to get a change through.
- Keep target names stable when CI or docs call them.
- Prefer narrow target runs during development, then aggregate verification.

## Common pitfalls

- Running only `go test ./...` in `agents-toolbelt` misses lint, race tests, build, and vulnerability checks.
- Running only `pytest` in `weld-cli` misses Ruff, Pyright, audits, and secret scanning.
- Treating `horizon-starknet` Makefile as a full frontend/indexer gate; those packages have their own Bun scripts and workflows.

## Exceptions

If a Make target depends on unavailable external services or expensive Docker state, explain the skipped target and run the closest non-service validation.
