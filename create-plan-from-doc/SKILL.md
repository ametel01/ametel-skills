---
name: create-plan-from-doc
description: Create a detailed implementation plan from one or more supplied source document paths, writing the result to PLAN.md. Use when the user asks Codex to turn PRDs, specifications, design docs, issue briefs, RFCs, markdown files, text files, or other local docs into one incremental implementation plan with quality gates and per-step commits.
---

# Create Plan From Docs

Use this skill to produce an implementation plan, not to implement the feature.
Accept one or more source document paths from the user's prompt as the main argument.

## Workflow

1. Resolve the document paths.
   - If the user did not provide any doc path, ask for at least one before proceeding.
   - Resolve relative paths from the current working directory.
   - Confirm every file exists before planning. If any path is missing or ambiguous, stop and ask for clarification.
   - Read each document completely enough to understand its requirements, constraints, acceptance criteria, and open questions. If a file is long, inspect headings first, then read the relevant sections.
   - Track which requirements came from which source. When docs overlap or conflict, record the conflict in `PLAN.md` and choose a conservative assumption only when the safer choice is clear.

2. Establish repository context.
   - Find the project root, preferring the nearest Git root.
   - Inspect the existing toolchain before planning: package manager files, Makefile, CI workflows, test configuration, lint configuration, formatter configuration, build scripts, and relevant source/test directories.
   - Prefer existing project commands and conventions. Do not invent a new quality-gate setup when the repo already has one.

3. Define quality gates before any implementation step.
   - Identify the exact commands for format, lint, tests, typecheck, build, or equivalent repo-specific checks.
   - If any required gate is missing or unclear, add a "Quality Gates Setup" step immediately after `Step 0: Progress Tracking Setup` that adds or documents the missing gate before feature implementation begins.
   - Include a baseline gate run before implementation when practical, so later failures can be distinguished from pre-existing failures.

4. Write `PLAN.md`.
   - Create or replace `PLAN.md` in the project root unless the user explicitly requests another location.
   - The plan must be detailed enough that another agent can execute it without re-reading the source docs for intent.
   - Make `PROGRESS.md` setup the first prerequisite step in the plan, before quality-gate setup or implementation work.
   - Require `PROGRESS.md` to be updated after each completed step so the user can inspect execution status while the plan is being worked on.
   - Use clear, incremental steps. Each step must leave the repository in a working state.
   - Keep implementation steps small enough for a focused commit.

5. Do not start implementation.
   - Stop after writing `PLAN.md` unless the user explicitly asks to begin executing the plan.

## PLAN.md Requirements

`PLAN.md` must include these sections:

```markdown
# Implementation Plan

## Source Documents
- Path: <doc path>
  - Role: <primary PRD/design/spec/etc.>
  - Summary: <short summary of relevant requirements>
- Path: <doc path>
  - Role: <supporting context/constraints/etc.>
  - Summary: <short summary of relevant requirements>

## Goals
- <user-visible or system-visible outcome>

## Non-Goals
- <explicitly excluded work>

## Assumptions and Open Questions
- <assumption or question, with impact if unresolved>

## Quality Gates
- Setup status: <existing gates found, or setup required before implementation>
- Baseline command: `<command>`
- Format command: `<command>`
- Lint command: `<command>`
- Test command: `<command>`
- Additional gates: `<typecheck/build/security/etc.>`

## Progress Tracking
- File: `PROGRESS.md`
- Requirement: Create `PROGRESS.md` before any quality-gate setup or implementation work begins.
- Update rule: After each step is completed, update `PROGRESS.md` with the completed step, validation results, commit reference if available, current status, and next step.

## Incremental Steps

### Step 0: Progress Tracking Setup
Goal: Create a durable progress log the user can consult while the plan is being executed.

Changes:
- Create `PROGRESS.md` in the project root.
- Add the plan title/sources, a step checklist, current status, and a short update log.
- Document that the file must be updated after every completed step.

Validation:
- Confirm `PROGRESS.md` exists and contains the step checklist.

Progress:
- Mark Step 0 complete in `PROGRESS.md`, record validation results, set the current status, and identify the next step.

Commit:
- `<suggested commit message>`

### Step 1: Quality Gates Setup
Goal: Ensure format, lint, and test gates are runnable before implementation starts.

Depends on:
- Step 0

Changes:
- <exact files/config/scripts to inspect or add>

Validation:
- Run `<format command>`
- Run `<lint command>`
- Run `<test command>`
- Run any additional required gates

Progress:
- Update `PROGRESS.md` with completion notes, validation results, commit reference if available, current status, and next step.

Commit:
- `<suggested commit message>`

### Step 2: <small implementation outcome>
Goal: <concrete outcome>

Depends on:
- Step 0
- Any required quality-gate setup step

Changes:
- <specific modules, files, interfaces, data paths, or behavior to modify>
- <tests to add or update>
- <docs or config updates if needed>

Validation:
- Run `<format command>`
- Run `<lint command>`
- Run `<test command>`
- Run any additional required gates

Progress:
- Update `PROGRESS.md` with completion notes, validation results, commit reference if available, current status, and next step.

Commit:
- `<suggested commit message>`
```

Always include `Step 0: Progress Tracking Setup`. Omit the quality-gates setup step only when quality gates are already clearly configured and the plan includes the exact commands in `## Quality Gates`.

## Step Detail Standard

For each incremental implementation step:

- State the user-visible or system-visible outcome.
- List concrete files, modules, APIs, schemas, tests, and docs likely to change.
- Identify dependencies on earlier steps.
- Include acceptance criteria for the step.
- Include the full quality-gate command list to run after completing the step.
- Include an explicit `PROGRESS.md` update action after validation and before moving to the next step.
- Include a suggested commit message.
- Make the step small enough that it can be reviewed independently.

Every implementation step must end with:

1. Run all quality gates: format, lint, tests, and any project-specific checks.
2. Fix any failures before proceeding.
3. Update `PROGRESS.md` with the completed step, validation results, commit reference if available, current status, and next step.
4. Create a commit for that completed step.

## Planning Guidance

- Prefer vertical slices that produce working behavior over broad layer-by-layer rewrites.
- Put risk-reducing work early: quality gates, failing characterization tests, migrations, compatibility shims, or feature flags.
- Call out ordering constraints, rollback concerns, data migrations, external services, and environment variables.
- If any source document is ambiguous, record the ambiguity in `PLAN.md` and choose a conservative assumption when possible.
- If a requirement appears too large for one commit, split it into smaller observable outcomes.
