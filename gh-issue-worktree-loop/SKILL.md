---
name: gh-issue-worktree-loop
description: Use when owning an unassigned GitHub issue end to end in an isolated worktree. Claim, implement, gate, PR, handle review, and continue to approval or blocker. In coordinator runs, use one loop per parallel-safe issue or PR-fix stream.
---

# GitHub Issue Worktree Loop

Run this workflow as an issue-owning coding agent. You are responsible for the full issue-to-approved-PR loop, not just a patch. Keep the loop bounded, evidence-driven, and recoverable.

Use default Git commands for worktree lifecycle. One implementation stream gets one branch and one local worktree.

## Parallel Streams

When coordinating several issues, run this loop concurrently for every independent ready issue or PR-fix stream that can proceed without dependency, branch, or shared-file conflict. Do not leave an independent ready issue idle while local resources can support another worktree and agent. Shared files are a coordination risk, not a dependency by themselves; serialize only when simultaneous edits would create real conflict.

Also check local resource conflicts before assuming streams are parallel-safe: fixed ports, Docker Compose project names, database names, emulator state, cache directories, generated files, or long-running local services can collide across worktrees. Prefer per-worktree isolation with environment overrides such as `COMPOSE_PROJECT_NAME`, per-stream ports, per-stream database names, and per-worktree temp/cache directories. If isolation is not available, record the resource as the throughput blocker and serialize only the streams that share it.

## Stop Rules

Stop and report a blocker instead of spinning when:

- The issue is already assigned, claimed in comments, closed, or has unresolved maintainer questions.
- `gh auth status` fails or the upstream remote cannot be identified.
- Git cannot create or reuse a clean, isolated worktree for the stream.
- Five implementation/review cycles have run without approval.
- The same test, CI, or review failure repeats twice without new evidence.
- A previously passing required gate starts failing after a feedback fix.
- A requested fix conflicts with the issue contract, maintainer comments, or existing behavior.
- Required quality gates cannot run and CI cannot substitute for them.
- The PR is approved, merged, or the user tells you to stop.
- Another agent is about to edit the same branch, worktree, or conflicting files.
- Another active stream owns a required fixed local resource that cannot be isolated safely.

Never delete, reset, remove, or force-clean a dirty worktree unless the work has been safely pushed or the user explicitly approves discarding it.

## Local Run State

Keep a short local state note for any run that may span multiple turns, CI waits, or review cycles. Prefer `STATUS.md` when the repo has an agent-team status convention; otherwise use an untracked file such as `.git-worktree-issue-status.md` in the worktree.

The note should contain only durable signal:

- Issue, branch, worktree path, PR URL, and current phase.
- Acceptance checklist and definition of done.
- Commands run and their results.
- Current CI/review status.
- What failed, what was tried, and what should be avoided next.

Read this note before each new cycle and update it after each major phase. Do not commit it unless the repository explicitly expects it.

## 1. Select And Claim An Issue

1. Identify the upstream repository and default branch:
   - `git remote -v`
   - `gh repo view --json nameWithOwner,defaultBranchRef`
2. Find candidate issues using `gh issue list`. Prefer issues that are:
   - open
   - unassigned
   - not already linked to an open PR
   - not recently claimed by another contributor in comments
   - actionable without private context
   - small enough for one bounded agent loop
3. Read the full issue before claiming:
   - `gh issue view <number> --comments`
   - linked issues, linked PRs, maintainer comments, labels, milestones, and reproduction details
4. Build an acceptance checklist from the issue discussion: expected behavior, non-goals, compatibility promises, docs, tests, and maintainer constraints.
5. Write a completion contract before claiming: exact result, evidence required, files/areas likely in scope, areas not to touch, and when to stop.
6. Claim the issue only after it is clearly safe to work:
   - assign yourself with `gh issue edit <number> --add-assignee @me`
   - add a short comment that you are starting work if the repository norm allows it

If the repository discourages self-assignment or claim comments, follow its contribution docs instead.

## 2. Create Or Reuse A Git Worktree

From the backing repository, create a durable local worktree:

```bash
git fetch --all --prune
git worktree list --porcelain
branch="fix/issue-<number>-short-topic"
worktree_path="../<repo-name>-issue-<number>"
git worktree add "$worktree_path" -b "$branch" <base-ref>
cd "$worktree_path"
```

If the branch already exists and is not checked out elsewhere, reuse it:

```bash
git worktree add "$worktree_path" "$branch"
cd "$worktree_path"
```

After entering the worktree:

1. Verify it is the expected repository with `git remote -v` and `git status --short --branch`.
2. Fetch the upstream default branch.
3. Ensure the branch starts from the latest upstream default branch unless the issue requires another base.
4. Record the absolute worktree path, branch, issue, PR, phase, and owner in the local run state or `STATUS.md`.

Use `git worktree remove "$worktree_path"` only after the work is pushed, the PR/commit is recorded, and there is no local state that must be preserved. Keep the worktree if follow-up review or CI work is likely.

## 3. Prepare The Work

Before editing:

- Read repo instructions: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING`, `README`, package scripts, CI workflows, and test docs.
- Inspect the changed area and at least one related caller, test, type/schema, or integration point.
- Convert the issue into a local checklist. Keep it short enough to fit in the active context.
- Decide the likely quality gates before implementation.
- Record the completion contract in the local run state.

Prefer the smallest change that satisfies the issue contract. Do not broaden scope because adjacent cleanup is tempting.

## 4. Implement And Verify

Implement in tight cycles:

1. Make a focused change.
2. Run targeted tests for the touched behavior.
3. Run typecheck, lint/format, build, or compile as required by the repo.
4. Add or update tests that would fail without the fix.
5. Update docs, examples, migration notes, or changelog fragments only when the issue or contribution rules require them.

Security and quality gates:

- If dependencies, lockfiles, install scripts, CI, auth, secrets, networking, parsing, uploads, or permissions changed, run the repo's audit/static/security checks when available.
- If database schemas or migrations changed, run migration validation or the closest local dry run.
- If frontend UX changed, verify accessible states and responsive behavior when feasible.
- If full gates are too expensive or unavailable, run the closest targeted subset and record the residual risk.

Do not mark the issue fixed until the acceptance checklist is satisfied and validation evidence exists.

If a gate fails, classify the failure before retrying: missing context, bad assumption, tool/environment failure, incomplete implementation, test expectation mismatch, formatting/schema failure, or policy/security conflict. Change strategy on the next attempt; do not rerun the same command-response loop blindly.

## 5. Commit, Push, And Open PR

Before committing:

- Run `git status --short` and inspect the diff.
- Ensure unrelated user or generated noise is not staged.
- Stop if secrets, credentials, private keys, or unintended large artifacts appear.

Commit logically:

```bash
git add <reviewed-paths>
git commit -m "Fix issue #<number>: <short summary>"
git push -u origin HEAD
```

Open the PR:

```bash
gh pr create \
  --base <default-branch> \
  --head "$(git branch --show-current)" \
  --title "<clear issue-focused title>" \
  --body "$(cat <<'PR_BODY'
Closes #<number>

## Summary
- ...

## Context
- Primary issue: Closes #<number>
- Related issues: None
- Related PRs: None
- Depends on: None
- Blocks/unblocks: None
- Stack/base: None

## Validation
- ...

## Risks
- ...

## Notes
- ...
PR_BODY
)"
```

The PR body must include enough GitHub-visible context to review without private conversation or local run state: primary issue link, related issues/PRs, upstream dependencies, stacked/base PRs, downstream PRs or issues it unblocks, behavioral boundaries, validation commands with pass/fail status, CI/checker evidence, skipped checks, known residual risk, and merge or retargeting notes. Write `None` for relationship categories that do not apply. Do not hide skipped checks.

## 6. Monitor CI, Reviews, And Comments

Poll deliberately; do not busy-wait.

Use:

- `gh pr view --json state,mergeStateStatus,reviewDecision,statusCheckRollup,url`
- `gh pr checks --watch` when active checks are running
- `gh pr view --comments`
- GraphQL `reviewThreads` when unresolved inline threads matter

Classify feedback:

- CI failure
- blocking requested change
- actionable suggestion
- clarification question
- stale/outdated comment
- non-actionable discussion

For each actionable item, map it back to the issue checklist or PR diff. If feedback is ambiguous, ask a clarifying question in the PR instead of guessing.

Treat "approved" as a claim until confirmed by both review state and required checks. Required checks must be passing, skipped by repo policy, or explicitly superseded by maintainer instruction.

## 7. Address Feedback

For each review cycle:

1. Pull or fetch the latest branch state.
2. Read unresolved review threads and failed CI logs.
3. Cluster related comments by behavior area.
4. Implement the smallest fix that addresses the cluster.
5. Rerun targeted tests and any gate related to the changed area.
6. Commit with a message that names the feedback area.
7. Push the branch.
8. Reply to each addressed comment with what changed and what validation ran.
9. Resolve conversations only after the fix is pushed and the reply is accurate.

Do not resolve a conversation merely because you disagree. If you disagree, reply with evidence and leave the thread for the reviewer.

Repeat until the PR is approved, all required checks pass, or a stop rule triggers.

After each review cycle, summarize the lesson in the local run state in under 120 words: what failed, what worked, what to avoid, and what to try next. Only turn reviewer feedback into a reusable project rule when the same pattern appears across multiple comments or reviews; one comment can be noise.

## 8. Remove Or Preserve The Worktree

When the PR is approved or the workflow is otherwise complete:

1. Confirm all commits are pushed: `git status --short --branch`.
2. If the worktree is clean and no local-only state is needed, remove it:
   - `git worktree remove "$worktree_path"`
3. If the worktree must remain available for follow-up, preserve it and report the path, branch, PR URL, and reason.
4. Use `git worktree prune --dry-run` as a cleanup check. Run pruning without `--dry-run` only when stale administrative entries are understood and no active agent work is affected.

## Final Report

Report:

- Issue number and PR URL.
- Worktree path and whether it was removed or preserved.
- Branch and commit hashes pushed.
- Acceptance checklist status.
- Quality/security gates run and results.
- Review threads or CI failures handled.
- Remaining blockers, risks, or reviewer decisions.

If the PR is approved, say so plainly. If not, state the exact next condition needed for approval.
