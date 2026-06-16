---
name: repo-toolchain-detector
description: Use this skill when entering an ametel01 repo and choosing install, build, test, lint, format, release, or CI commands. Detect Bun, uv, Go, Scarb, Makefile, lockfile, and workflow variants before running commands; do not assume one package manager or quality gate across the account.
---

# Repo Toolchain Detector

## Purpose

Choose commands from the target repository's own files before acting. The account uses several toolchains side by side: Bun/Biome TypeScript, uv/Ruff/Pyright Python, Go with Makefile verification, and Scarb/snforge Cairo.

## When to use

Use this before running install, build, test, lint, typecheck, format, security, release, or deployment commands in any sampled repo.

## Evidence from repositories

Strength: Strong.

- `vitals-db`: `package.json`, `bun.lock`, `biome.json`, `tsconfig.json`, `.github/workflows/ci.yml`.
- `horizon-starknet`: `contracts/Scarb.toml`, `contracts/Scarb.lock`, `Makefile`, `packages/frontend/package.json`, `packages/indexer/package.json`, per-package `bun.lock`, multiple `.github/workflows/*.yml`.
- `claw-training-dashboard`: `package.json`, `bun.lock`, `biome.json`, `tsconfig.json`.
- `weld-cli`: `pyproject.toml`, `uv.lock`, `Makefile`, `.github/workflows/ci.yml`, `.github/workflows/release.yml`.
- `agents-toolbelt`: `go.mod`, `go.sum`, `Makefile`, `.golangci.yml`, `.github/workflows/ci.yml`.
- `orgs-ai-harness`: `pyproject.toml`, `tests/test_org_pack_foundation.py`; minimal Python packaging without the richer weld-cli gates.

## Detection workflow

1. Inspect top-level and package-local manifests first:
   - `package.json`, lockfiles, `biome.json`, `tsconfig.json`
   - `pyproject.toml`, `uv.lock`, `Makefile`
   - `go.mod`, `go.sum`, `.golangci.yml`
   - `contracts/Scarb.toml`, `contracts/Scarb.lock`
   - `.github/workflows/*.yml`
2. Prefer the command in `package.json` scripts or `Makefile` targets over reconstructing raw commands.
3. If a repo has multiple subprojects, run commands from the subproject working directory shown by the manifest or workflow.
4. If CI exists, mirror CI order locally when practical.
5. If no workflow or Makefile exists, choose the smallest command that validates the touched area.

## Command decision table

| Detected files | Default commands |
|---|---|
| `package.json` plus `bun.lock` | `bun install --frozen-lockfile`, then repo scripts such as `bun run check`, `bun run typecheck`, `bun run test`, `bun run build` |
| `biome.json` | Use `biome` through scripts; do not substitute ESLint or Prettier unless the repo contains those configs |
| `pyproject.toml` plus `uv.lock` | `uv sync --frozen`, `uv run ruff format --check .`, `uv run ruff check .`, `uv run pyright`, `uv run pytest` |
| `Makefile` with `verify` or `ci` | Prefer `make verify` or `make ci`; use individual targets while iterating |
| `go.mod` | Prefer `make verify` when present; otherwise use `go test ./...`, `go vet ./...`, and configured linters |
| `contracts/Scarb.toml` | `cd contracts && scarb fmt --check`, `scarb check`, `scarb build`, `snforge test` |

## Invariants

- Never mix package managers in one repo unless the repo already does so.
- Lockfiles are authoritative: use frozen installs in CI-like validation.
- Scope commands to the changed package when workflows are path-scoped.
- Do not invent an org-wide command; this account intentionally has variants.

## Common pitfalls

- Assuming pnpm or npm in TypeScript repos. The sampled TypeScript repos use Bun.
- Running root `bun install` in `horizon-starknet`; frontend and indexer have separate package directories and lockfiles.
- Treating `orgs-ai-harness` like `weld-cli`; it is a simpler Python package without uv lock or Ruff/Pyright config.
- Skipping Makefile gates in repos where CI calls `make verify`.

## Escalation

If manifests and workflows disagree, report the conflict and run the command used by CI unless the user asks for a narrower local check.
