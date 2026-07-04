---
name: typescript-bun-biome
description: Use this skill when editing ametel01 TypeScript or React repos that use Bun, Biome, TypeScript, Vitest, Playwright, Next.js, Hono, Vite, or Apibara. Follow package scripts, strict tsconfig settings, Biome lint/format rules, and Bun lockfile workflows.
---

# TypeScript Bun Biome

## Purpose

Work consistently in the account's TypeScript repos. Bun is the package runner, Biome is the formatter/linter, TypeScript is strict, and tests vary by package.

## When to use

Use when editing TypeScript, React, Next.js, Hono, Vite, dashboard, indexer, or Bun scripts in `vitals-db`, `horizon-starknet/packages/frontend`, `horizon-starknet/packages/indexer`, or `claw-training-dashboard`.

## Evidence from repositories

Strength: Strong for TypeScript repos.

- `vitals-db`: root `package.json`, `bun.lock`, `biome.json`, root and package `tsconfig.json`, `.github/workflows/ci.yml`.
- `horizon-starknet`: `packages/frontend/package.json`, `packages/frontend/biome.json`, `packages/frontend/tsconfig.json`, `packages/indexer/package.json`, `packages/indexer/biome.json`, `packages/indexer/tsconfig.json`, frontend/indexer CI workflows.
- `claw-training-dashboard`: `package.json`, `bun.lock`, `biome.json`, `tsconfig.json`, Vitest and Playwright tests.

## Standard workflow

1. Read the nearest `package.json`, `biome.json`, and `tsconfig.json`.
2. Install with Bun only when dependencies are missing or changed:
   - `bun install --frozen-lockfile`
3. Run the smallest relevant script during iteration.
4. Before finishing, run the target repo's aggregate validation script if it exists.

## Commands

Common scripts:

```bash
bun run check
bun run typecheck
bun run test
bun run build
```

Repo-specific gates:

```bash
# vitals-db root
bun run check:ci
bun run typecheck
bun run test
bun run build

# horizon-starknet frontend
cd packages/frontend
bun run check
bun run test
bun run build
bun run test:e2e --project=chromium

# horizon-starknet indexer
cd packages/indexer
bun run check
bun run test
bun run build

# claw-training-dashboard
bun run verify
bun run test:e2e
```

## Required checks

- Run `typecheck` for TypeScript contract or API shape changes.
- Run `biome check` through the repo script for lint/format changes.
- Run focused tests for touched behavior; add e2e only when user-facing browser workflows change.
- Run build when touching Next.js, Vite, server bundle, indexer build, or package exports.

## Invariants

- Keep `strict` TypeScript expectations intact. Do not weaken `tsconfig.json` to make a change pass.
- Prefer `unknown`, narrow types, and DTO types over `any`; Biome often errors on explicit `any`.
- Keep import style and quote style matching the package-local `biome.json`.
- Respect exact optional property semantics where enabled.
- In `horizon-starknet`, frontend and indexer have separate Biome configs and line widths.

## Common pitfalls

- Do not add ESLint or Prettier configs to solve Biome failures.
- Do not invoke npm or pnpm installer commands in Bun repos.
- Do not edit generated outputs such as `dashboard/app.js`, `.next`, `dist`, coverage, or imported data unless the task explicitly targets generated assets.
- In `horizon-starknet`, rerun codegen scripts when contract or event ABI changes affect frontend or indexer types.

## Exceptions

- `vitals-db` is a Bun workspace; root scripts coordinate packages.
- `horizon-starknet` uses package-local Bun installs in `packages/frontend` and `packages/indexer`.
- `claw-training-dashboard` includes built legacy dashboard artifacts, but source changes should usually happen under `src`, `server/src`, `dashboard/src`, or `test`.
