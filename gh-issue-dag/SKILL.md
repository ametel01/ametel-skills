---
name: gh-issue-dag
description: Use this skill when building or reviewing a dependency graph for GitHub issues, milestones, releases, refactors, or task plans.
---

# GH Issue DAG

Read-only by default: produce ordering guidance and label suggestions, but ask the user for confirmation before editing GitHub issues, labels, milestones, or project fields.

## Workflow

1. Normalize each issue into a node with an ID, title, outcome, and current status if available.
2. Add edges only for real dependencies: required code, data, contracts, product decisions, migrations, external approvals, or test infrastructure.
3. Do not treat shared files or similar labels as dependencies by themselves. File overlap is a coordination risk, not a blocker unless one issue requires the other result.
4. Detect cycles. Break a cycle by extracting a decision, contract, migration, or smaller enabling issue.
5. Produce execution waves from the graph: wave 0 has no blockers, later waves unlock as dependencies complete.
6. Flag issues that are blocked by human decisions separately from issues blocked by implementation work.

## Edge Types

Use explicit edge labels:

- `blocks`: one issue must finish before another can start safely.
- `decision-blocks`: a human product, UX, security, or architecture decision is required first.
- `enables`: useful ordering but not a hard blocker.
- `coordinates-with`: can run in parallel but needs merge or review coordination.

## Output Format

Produce:

- `Dependency graph`: bullet list of issue relationships.
- `Execution waves`: groups of issues that can run in parallel.
- `Blocked items`: issue, blocker, owner, and next action.
- `Cycle risks`: any suspected loops and the proposed split.
- `Label suggestions`: `blocked`, `needs-decision`, `parallel-safe`, `coordination-risk`, `milestone:<name>`.

Use Mermaid only when the user asks for a diagram or the graph is easier to inspect visually.
