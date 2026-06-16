---
name: ci-security-gates
description: Use this skill when changing CI, dependencies, release workflows, install scripts, secrets, audits, GitHub Actions, Vercel deploys, PyPI publishing, GoReleaser, TruffleHog, detect-secrets, pip-audit, govulncheck, or Dependabot in ametel01 repos.
---

# CI Security Gates

## Purpose

Preserve the account's security and CI posture while changing code, workflows, dependency management, or deployment paths. Security checks are implemented differently per repo.

## When to use

Use when editing `.github/workflows`, dependency manifests, install/update paths, deploy config, environment handling, secret-bearing code paths, or release automation.

## Evidence from repositories

Strength: Moderate.

- `weld-cli`: `.github/workflows/ci.yml` has lint, test matrix, and security jobs; uses `pip-audit` and `detect-secrets scan --baseline .secrets.baseline`.
- `horizon-starknet`: frontend CI runs TruffleHog with `--only-verified`; Dependabot covers frontend, indexer, and GitHub Actions; frontend deploy uses Vercel secrets and environments.
- `agents-toolbelt`: `Makefile` runs `govulncheck`; release workflow grants provenance permissions and attests build artifacts.
- `vitals-db`: CI runs Bun frozen install, Biome, TypeScript, tests, and build.
- `claw-training-dashboard` and `orgs-ai-harness`: no sampled GitHub Actions workflows; validate locally from package or test files.

## Standard workflow

1. Read the target workflow and local gate it invokes.
2. Identify security checks by stack:
   - Python: `pip-audit`, `detect-secrets`.
   - Go: `govulncheck`, strict `golangci-lint`, checksum/signature release paths.
   - TypeScript frontend/indexer: Biome security rules, TruffleHog in CI where configured.
   - Cairo contracts: Scarb build/check/fmt and snforge tests; security review docs may define extra expectations.
3. Keep workflow permissions minimal and explicit.
4. Use repository or environment secrets only through GitHub Actions expressions; never hardcode secret values.
5. If changing deployment, preserve branch/path filters and environment gates unless intentionally changing release policy.

## Commands

```bash
# Python security
uv run pip-audit
uv run detect-secrets scan --baseline .secrets.baseline

# Go security
make vulncheck
make verify

# Bun/TypeScript checks
bun run check
bun run typecheck
bun run test

# Cairo contracts
cd contracts
scarb fmt --check
scarb check
scarb build
snforge test
```

## Required checks

- Run or mirror the relevant workflow locally before touching CI.
- For secret-handling changes, run the repo's secret scanning path if present.
- For dependency updates, run the package manager's frozen install and full test gate.
- For release workflow edits, verify permissions, tag trigger, artifact paths, and version checks.

## Invariants

- Do not print secrets, tokens, or DSNs in logs. Public DSN-like telemetry config may exist, but do not add credentials.
- Do not replace verified release or audit steps with unchecked publish steps.
- Keep CI path filters aligned with package layout.
- Preserve provenance, checksum, or attestation steps in release workflows unless the user explicitly approves removal.

## Common pitfalls

- `horizon-starknet` deploy workflows use separate staging and production secrets. Do not collapse them.
- `weld-cli` release verifies `pyproject.toml` version and empty `Unreleased`; keep those gates.
- `agents-toolbelt` release relies on GoReleaser, cosign, and provenance attestation.
- Repos without workflows still need local validation; absence of CI is not permission to skip checks.
