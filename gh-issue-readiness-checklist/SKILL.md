---
name: gh-issue-readiness-checklist
description: Evaluate GitHub issue readiness. Use when reviewing acceptance criteria, AFK suitability, decomposition, dependencies, or issue-body edits.
---

# GH Issue Readiness Checklist

Read-only by default: report readiness and suggested edits, but ask the user for confirmation before editing GitHub issues, labels, milestones, or project fields.

## Readiness States

- `ready`: implementation can start now.
- `needs-clarification`: missing behavior, acceptance criteria, or decision.
- `needs-decomposition`: too broad, mixed, or not reviewable as one PR.
- `blocked`: depends on another issue, environment, credential, migration, design, or approval.

## Checklist

Mark an issue ready only when it has:

- a clear problem or outcome
- expected behavior and non-goals
- checkable acceptance criteria
- implementation boundaries or likely touchpoints
- validation plan with test commands or manual checks
- known dependencies and sequencing
- data, migration, rollout, or rollback notes when relevant
- UX, security, privacy, auth, billing, or API-contract decisions resolved when relevant

## Rewrite Guidance

When the issue is not ready:

1. State the readiness state.
2. List only the missing information that blocks implementation.
3. Propose exact issue-body edits instead of general advice.
4. Add a short "Ready when" section with concrete conditions.
5. Avoid expanding scope while improving clarity.

## Output Format

Use this format:

```markdown
## Readiness
State: ready | needs-clarification | needs-decomposition | blocked

## Blocking Gaps
- ...

## Suggested Issue Edits
- ...

## Ready When
- ...
```

If the issue is ready, replace blocking gaps with the focused test plan and any residual risks.
