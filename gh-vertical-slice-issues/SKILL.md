---
name: gh-vertical-slice-issues
description: Use this skill when decomposing a feature, bug, PRD, milestone, or vague project into small vertical GitHub issues with reviewable user/system outcomes.
---

# GH Vertical Slice Issues

## Workflow

1. Identify the smallest coherent outcome the user wants. If the request is vague, ask only for decisions that materially change issue boundaries.
2. Slice by behavior, not technical layer. Prefer issues that include every layer needed for one observable outcome: data shape, backend behavior, UI/CLI/API surface, tests, and docs when relevant.
3. Create an enabling issue only when the work cannot be safely attached to one vertical slice, such as migrations, generated clients, contracts, fixtures, or shared infrastructure.
4. Keep each issue reviewable. Split when an issue has multiple user workflows, multiple independent acceptance criteria groups, risky migration plus feature work, or cannot be tested independently.
5. Preserve order and parallelism. Note dependencies, but avoid serializing unrelated slices.

## Issue Shape

For each issue, produce:

- `Title`: imperative and outcome-focused.
- `Outcome`: one sentence describing the visible behavior or system capability.
- `Scope`: concrete work included in the issue.
- `Acceptance criteria`: checkable bullets, not implementation wishes.
- `Test plan`: focused unit, integration, e2e, or manual checks.
- `Likely touchpoints`: files, modules, commands, or services to inspect first when known.
- `Dependencies`: prerequisite issues or decisions.
- `Out of scope`: adjacent work the issue must not absorb.
- `Labels`: suggested GitHub labels such as `vertical-slice`, `type:feature`, `type:bug`, `needs-decision`, or `blocked`.

## Sizing Rules

- Target one coherent PR and one focused review.
- Prefer 0.5-2 days of agent work when estimating is possible.
- Avoid issues titled with layers only, such as "Add database schema" or "Build frontend".
- Avoid catch-all issues with words like "misc", "cleanup", "finalize", or "wire up" unless the scope is made concrete.
- Add a follow-up issue instead of widening a slice after the acceptance criteria are clear.

## Output Format

Start with a short milestone summary, then list issues in recommended order. Add a final "Parallelizable" section that groups issues that can proceed at the same time.
