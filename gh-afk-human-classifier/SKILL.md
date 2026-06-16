---
name: gh-afk-human-classifier
description: Classify GitHub issues or planned development tasks as safe for unattended agent execution, needing human review, needing human decision, or blocked. Use when Codex is preparing AFK agent batches, triaging a milestone, choosing which issues can be delegated, or labeling GitHub issues for agent versus human workflow.
---

# GH AFK Human Classifier

## Classes

- `afk-safe`: clear scope, deterministic implementation path, local validation available, low product judgment, and no destructive production action.
- `human-review`: agent can implement, but a human should review UX, architecture, security, migration, or behavior before merge.
- `human-decision`: implementation should not start until a product, domain, architecture, legal, security, or UX decision is made.
- `blocked`: missing prerequisite code, dependency, credentials, environment, upstream issue, or external approval.
- `split-first`: too broad or mixed; decompose before assigning to any worker.

## Classification Rules

Prefer `afk-safe` only when the issue has:

- checkable acceptance criteria
- known repo or subsystem boundaries
- a focused test command or validation path
- no ambiguous user-facing behavior
- no irreversible data, billing, security, credential, release, or production operation

Prefer `human-review` when the issue is implementable but changes a public contract, user journey, data migration, permissions, auth, payments, observability, or shared architecture.

Prefer `human-decision` when two reasonable implementations would produce different product or domain behavior.

Prefer `split-first` when the issue bundles unrelated outcomes, has layer-only scope, or spans multiple independent PRs.

## Output Format

Return a table with:

- `Issue`
- `Class`
- `Reason`
- `Missing info or risk`
- `Next action`
- `Suggested labels`

Suggested labels include `afk-safe`, `human-review`, `needs-decision`, `blocked`, and `split-first`.
