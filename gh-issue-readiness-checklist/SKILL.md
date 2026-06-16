---
name: gh-issue-readiness-checklist
description: Evaluate whether a GitHub issue is ready for implementation by an agent or developer. Use when Codex is reviewing issue quality, preparing issues for AFK execution, checking acceptance criteria, rewriting an issue body, or deciding whether a task needs clarification, decomposition, or dependency resolution before coding begins.
---

# GH Issue Readiness Checklist

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
