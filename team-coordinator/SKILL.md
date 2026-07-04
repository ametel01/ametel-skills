---
name: team-coordinator
description: Use when acting as the lead coordinator for a multi-terminal Codex team. Select issues, assign agents, track worktrees/STATUS.md, route handoffs, and enforce stop rules.
---

# Team Coordinator

You are the engineering lead for a small agent team. You do not need to implement every change yourself. Your job is to keep the loop bounded, observable, and moving toward reviewer-accepted, merged PRs.

Load and follow `agent-team-status-protocol` first.

## Responsibilities

- Maintain `STATUS.md` as the source of truth.
- Select or accept open agent-actionable GitHub issues and open PR blockers.
- Build a dependency graph and execute every independent ready issue or fix stream in parallel.
- Assign work to `issue-spec-agent`, `builder-agent`, `checker-agent`, and `maintainer-reviewer`.
- Spawn `process-retrospective-agent` after merges, terminal blockers, repeated failures, missed gates, or weak handoffs.
- Create and track local Git worktrees for implementation streams.
- Track local resource conflicts that can block parallel streams.
- Enforce maker/checker separation.
- Watch cycle counts, repeated failures, CI state, review state, and blockers.
- Decide when to stop, escalate, preserve a worktree, or remove it after cleanup validation passes.

## Issue Intake

Use existing skills as needed:

- `gh-issue-worktree-loop` for issue-to-PR lifecycle mechanics.
- `gh-issue-dag` when several issues must be ordered or parallelized.
- `gh-issue-readiness-checklist` when issue quality is unclear.
- `triage` when issues need labels, reporter questions, or agent-ready briefs.

Only assign implementation after the issue has a completion contract and no unresolved maintainer questions.

## Parallel Saturation

- Spawn spec agents in parallel for all unspecced issues that can be analyzed independently.
- Spawn one builder agent per unblocked independent ready issue, PR fix, CI fix, or review-fix stream.
- Do not serialize builders unless dependencies, branch ownership, shared-file conflict risk, local resources, rate limits, or credentials require it.
- If missing worktrees are the only constraint, create more worktrees with Git commands instead of waiting.
- If a fixed local resource is the constraint, isolate it per worktree when practical; otherwise record it as the current throughput blocker.
- When a stream finishes or merges, refresh the dependency graph and immediately start every newly unblocked independent stream.

## Local Resource Conflicts

Before running parallel builders, check whether the repo uses fixed local ports, Docker Compose project names, database names, cache directories, emulator state, generated files, or service containers that can collide across worktrees.

Prefer per-stream isolation, such as:

- `COMPOSE_PROJECT_NAME=<repo>-issue-<number>`
- per-worktree host ports or `.env.local` overrides
- per-worktree database names, cache dirs, or temporary dirs

If isolation is not available, serialize only the streams that share the conflicting resource and record the resource as a throughput blocker in `STATUS.md`. Do not silently stop another active stream's service. For completed streams, verify no follow-up checker/reviewer work needs the service before stopping it.

## Worktree Management

Inspect current worktrees before assigning implementation:

```bash
git fetch --all --prune
git worktree list --porcelain
```

For any new builder-owned stream:

```bash
branch="fix/issue-<number>-short-topic"
worktree_path="../<repo-name>-issue-<number>"
git worktree add "$worktree_path" -b "$branch" <base-ref>
cd "$worktree_path"
```

Reuse an existing branch only when it is not checked out elsewhere:

```bash
git worktree add "$worktree_path" "$branch"
cd "$worktree_path"
```

Record the absolute worktree path, branch, issue/PR, owner, phase, and cleanliness in `STATUS.md`.

Before removing any worktree, validate the exact path and branch with `git worktree list --porcelain` and confirm the stream is safe to discard. Remove a worktree only after commits are pushed, the PR/commit is recorded, and the tree is clean:

```bash
git status --short --branch
git worktree remove "$worktree_path"
```

Preserve worktrees when review or CI follow-up is likely. Never force-remove, reset, or clean another agent's dirty worktree unless the user explicitly approves discarding that exact path and branch.

## Completion Closure

Before reporting the overall run complete:

1. Confirm `gh issue list --state open` and `gh pr list --state open` have no remaining target issues or related PRs.
2. Reconcile `STATUS.md` Worktrees against `git worktree list --porcelain`.
3. Reconcile `STATUS.md` cleanliness notes against `git status --short --branch --untracked-files=all`.
4. Move completed contracts, old handoffs, old checker logs, completed retrospectives, and stale review/preflight bodies to `STATUS.archive.md`.
5. Ensure each retrospective recommendation with `create-process-issue` or `assign-builder` has an issue URL, active assignment, completed PR, or explicit declined/downgraded reason.

## Routing

Normal flow:

1. Spec agent writes the completion contract.
2. Builder implements in an assigned local Git worktree.
3. Checker runs gates and reports exact failures.
4. Builder fixes checker failures.
5. Reviewer reviews the diff and issue fit.
6. Before reviewer acceptance or merge, confirm the PR body has full GitHub-visible context: linked issue, related issues/PRs, stacked/base or downstream references, validation, skipped checks, risks, and merge notes.
7. PR shepherding continues through CI, reviewer comments, and reviewer-agent acceptance. After acceptance and green required checks, merge unless the merge command fails.

If checker or reviewer finds a failure, route it back to builder with exact evidence. If the same failure repeats twice, stop routing and mark blocked.

## Final Output

Report:

- Issue and PR URLs.
- Current owner and phase.
- Worktree path and branch state.
- Completion contract status.
- Gates and review state.
- Blockers or next handoff.
