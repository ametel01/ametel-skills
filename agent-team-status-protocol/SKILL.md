---
name: agent-team-status-protocol
description: Use when coordinating multiple Codex terminal agents as a development team. Defines the shared STATUS.md contract, handoff format, ownership rules, cycle counters, stop conditions, and durable memory used by coordinator, spec, builder, checker, and reviewer agents.
---

# Agent Team Status Protocol

Use this protocol whenever multiple agent terminals collaborate on one repository or issue queue. The repo and files are shared infrastructure; the status file is the team memory.

## Shared State

Use `STATUS.md` at the repository root unless the coordinator names another file. If a repo already has a status convention, follow it and preserve its structure.

Every role must read `STATUS.md` before acting and update it after a meaningful state change. Keep it short, factual, and durable. Do not paste logs; link to commands, PRs, commits, or concise summaries.

Recommended shape:

```markdown
# Agent Team Status

## Active Work
- issue: #123
  owner: builder-agent
  branch: fix/issue-123-topic
  worktree: /abs/path
  pr: https://github.com/org/repo/pull/456
  phase: implementing | checking | review | waiting-ci | blocked | approved
  cycle: 2/5

## Completion Contract
- outcome:
- non-goals:
- required evidence:
- do-not-touch:

## Handoffs
- from:
  to:
  timestamp:
  request:
  evidence:
  next-action:

## Gates
- command:
  result:
  evidence:

## Review Threads
- thread:
  status: open | fixed | replied | resolved | blocked
  owner:
  evidence:

## Decisions And Lessons
- date:
  signal:
  rule:
```

## Handoff Contract

Every handoff between roles must include:

- Current objective.
- Files, issue, branch, worktree, PR, or thread involved.
- Exact requested next action.
- Evidence already collected.
- Stop condition for the recipient.

Do not hand off raw confusion. If the next action is ambiguous, mark the work `blocked` and name the missing decision.

## Ownership Rules

- One owner per active work item.
- One worktree branch per implementation stream.
- Builders may edit code; checkers and reviewers do not edit unless explicitly reassigned.
- Coordinator changes ownership, not individual agents.
- Do not overwrite another role's uncommitted work.

## Loop Brakes

Stop and escalate when:

- The same failure appears twice in a row.
- Five cycles run without approval.
- A fix breaks a previously passing required gate.
- A role needs credentials, product judgment, or repo permissions it does not have.
- Two agents are about to edit the same branch or worktree.

## Memory Rules

Persist only signal:

- What failed.
- What worked.
- What should be avoided next.
- What repeated reviewer or maintainer feedback should become a future rule.

One comment is noise. A repeated pattern across comments, CI, or reviews can become a rule.
