---
name: codex-dev-team-goal
description: Use when the user wants a long-running Codex dev-team goal. Coordinate agents and worktrees until agent-actionable GitHub issues are closed or externally blocked.
---

# Codex Dev Team Goal

Run this as the lead coordinator for a repository's Codex development team. Load and follow `team-coordinator` and `agent-team-status-protocol` first.

The goal is complete only when every target issue is closed by a merged PR and every related PR is merged. Dependency blockers are active work, not completion.

Human approval boundary: treat the user's explicit long-running dev-team goal as approval for scoped repo and GitHub writes needed to close the target issues. Ask for explicit confirmation before production deploys, releases, secret changes, billing changes, or work outside the target issue set.

## Agent Review Acceptance

The `maintainer-reviewer` agent's explicit `Approve` decision is the review acceptance gate for this workflow. After required checks pass and reviewer-requested fixes are addressed, merge the PR.

Do not wait for, request, or mark blocked on a non-author formal GitHub approval solely because the authenticated `gh` identity is also the PR author. If GitHub refuses to record `APPROVE` or `REQUEST_CHANGES` from that identity, same-author review comments and `STATUS.md` reviewer evidence are sufficient review evidence for this workflow.

A missing non-author formal approval is not a terminal blocker unless an actual merge attempt is rejected by GitHub branch protection or permissions. If `gh pr merge` fails, record the exact command and output, then decide whether a real external blocker remains.

## PR Context Gate

Every PR must be reviewable from GitHub without private conversation or local `STATUS.md` context. Before review and before merge, ensure the PR body includes:

- Primary linked issue, using a closing keyword when the PR should close it.
- Related issue and PR references: upstream dependencies, stacked/base PRs, downstream PRs or issues it unblocks, superseded PRs, and sibling PRs that coordinate with it; write `None` for categories that do not apply.
- Behavior scope, non-goals, and any user-visible or system-visible change.
- Validation evidence: commands run, pass/fail status, CI/checker status, skipped checks, and why any skipped check is acceptable.
- Known risks, follow-up work, migration/rollout notes, and merge/retargeting order for stacked PRs.

If a PR lacks full context, update it with `gh pr edit --body-file <file>` before sending it to the reviewer. The reviewer must treat missing PR context as blocking until the coordinator or builder updates the PR body.

## Coordinator Loop

1. Inspect repository state, GitHub issues, open PRs, PR checks, review comments, branches, remotes, `git worktree list --porcelain`, and `STATUS.md`.
2. Build or refresh a dependency graph of open agent-actionable issues and PRs.
3. Spawn `issue-spec-agent` sub-agents in parallel for all unspecced issues that can be analyzed independently.
4. Put open PRs, failing required checks, unresolved review threads, and repo-local dependency blockers ahead of downstream issue work.
5. For every independent ready issue or fix stream, create or reuse a separate Git worktree and branch, then spawn one `builder-agent` for that stream.
6. Saturate safe parallelism: no independent ready issue should sit idle while local resources can support another worktree and sub-agent.
7. When a builder finishes, spawn a `checker-agent`; route exact failures back to that stream's builder and re-check after fixes.
8. After checker evidence passes, open or update a draft PR, then run the PR Context Gate and update the PR body until it is complete.
9. Preflight draft state, required checks, merge method, branch protection, PR author, and authenticated GitHub identity; use identity only to choose review submission mode, not to require a non-author reviewer.
10. Spawn `maintainer-reviewer` to review the actual PR and submit a real GitHub review when possible; if GitHub blocks a formal same-author review, submit comment evidence and record the reviewer decision in `STATUS.md`.
11. Route reviewer changes, CI failures, and external PR comments through builder, checker, reviewer, and PR update loops until merge-ready.
12. Merge after required checks pass, the PR Context Gate passes, and the `maintainer-reviewer` decision is `Approve`. Do not treat missing non-author formal approval as a blocker unless `gh pr merge` is actually rejected.
13. After merge, close/update the linked issue, compact completed detail from `STATUS.md` to `STATUS.archive.md`, and spawn `process-retrospective-agent`.
14. Refresh the dependency graph and immediately start every newly unblocked independent stream.
15. Before declaring the goal complete, run the Closure Gate below and record the evidence in `STATUS.md`.

## Git Worktrees

Use regular Git commands for worktree management:

```bash
git fetch --all --prune
git worktree list --porcelain
git worktree add <path> -b <branch> <base-ref>
git worktree add <path> <existing-branch>
git worktree remove <path>
```

Create new worktrees instead of waiting when missing worktrees are the only capacity limit. Reuse an existing branch only when it is not checked out elsewhere. Before any `git worktree remove`, validate the exact path and branch with `git worktree list --porcelain` and `git status --short --branch`; preserve the worktree unless its branch is pushed, its PR/commit is recorded in `STATUS.md`, and the status is clean. If any dirty, unpushed, or unrecorded state remains, keep the worktree unless the user explicitly approves discarding that exact path and branch.

Each implementation stream must have exactly one branch, one local worktree, and one builder owner. Stop before two agents edit the same branch, worktree, or conflicting files.

## Shared State

Use `STATUS.md` at the repo root. Every role reads it before acting and updates it after meaningful progress.

Track each active issue/PR with owner, phase, branch, worktree, PR URL, cycle count, gates, blockers, and next action. Track all local worktrees, their branches, owners, and cleanliness. Keep dependency blockers separate from terminal blockers.

Keep hot status concise. Move old checker logs, completed handoffs, completed retrospectives, and stale review bodies to `STATUS.archive.md` after merge or terminal blocker.

## Closure Gate

Run this gate before marking the goal complete:

1. Verify GitHub state: `gh issue list --state open` and `gh pr list --state open` show no remaining target issues, related PRs, repo-local blockers, failed checks, or review threads.
2. Verify worktree state: `git worktree list --porcelain` matches the `STATUS.md` Worktrees section; every removed worktree is absent, every preserved worktree has a reason, and every active branch has an owner or cleanup disposition.
3. Verify repository state: `git status --short --branch --untracked-files=all` matches the `STATUS.md` cleanliness notes; do not claim files or archive artifacts exist unless they are present on disk.
4. Compact hot state: `STATUS.md` contains only current active work, current blockers, current worktrees, final issue/PR/commit/review links, and durable lessons. Move full contracts, historical checker logs, completed handoffs, completed retrospectives, old gate output, and stale review bodies to `STATUS.archive.md`.
5. Close retrospective recommendations: every `create-process-issue` or `assign-builder` recommendation has an issue URL, assigned active stream, completed PR, or explicit declined/downgraded reason.
6. Record the closure evidence in `STATUS.md`. If any item fails, keep the goal active or mark the exact external blocker.

## Sub-Agent Prompts

Before spawning role agents, read [sub-agent-prompts.md](references/sub-agent-prompts.md). Include each assigned role prompt verbatim or semantically intact, starting with its `Use the ... skills` line. No role agent may run without its role-specific skill and `agent-team-status-protocol`.

## Stop Rules

- Do not stop just because downstream issues are dependency-blocked; work the upstream blocker.
- Stop or escalate if the same fix attempt fails twice with no new hypothesis.
- Stop or escalate after five implementation/review cycles on the same item without progress.
- Stop or escalate if a fix breaks a previously passing required gate and cannot be isolated.
- Stop or escalate if credentials, permissions, merge rights, or product decisions are missing after an exact attempted operation fails. Do not treat missing non-author formal approval as missing merge rights unless GitHub rejects the merge.
- Stop or escalate if two agents are about to edit the same branch, worktree, or conflicting files.

If terminally blocked, leave exact evidence, commands, issue/PR/check URLs, agents used, and the next human decision needed.
