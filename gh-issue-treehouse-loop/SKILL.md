---
name: gh-issue-treehouse-loop
description: Use when an agent should autonomously pick up an unassigned GitHub issue, claim it, lease a Treehouse worktree, implement the fix, run required quality/security gates, commit, push, open a pull request, monitor reviews and comments, address requested changes, reply to reviewers, resolve conversations, and continue until approval or a clear blocker.
---

# GitHub Issue Treehouse Loop

Run this workflow as an issue-owning coding agent. You are responsible for the full issue-to-approved-PR loop, not just a patch. Keep the loop bounded, evidence-driven, and recoverable.

Use `treehouse` for worktree lifecycle. Prefer non-interactive leases so the workflow survives outside an interactive subshell.

## Stop Rules

Stop and report a blocker instead of spinning when:

- The issue is already assigned, claimed in comments, closed, or has unresolved maintainer questions.
- `gh auth status` fails or the upstream remote cannot be identified.
- Treehouse cannot lease a worktree.
- Five implementation/review cycles have run without approval.
- The same test, CI, or review failure repeats twice without new evidence.
- A previously passing required gate starts failing after a feedback fix.
- A requested fix conflicts with the issue contract, maintainer comments, or existing behavior.
- Required quality gates cannot run and CI cannot substitute for them.
- The PR is approved, merged, or the user tells you to stop.

Never delete, reset, or return a dirty worktree with `--force` unless the work has been safely pushed or the user explicitly approves discarding it.

## Local Run State

Keep a short local state note for any run that may span multiple turns, CI waits, or review cycles. Prefer an untracked file such as `.treehouse-issue-status.md` in the leased worktree unless the repo has an established agent status file.

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

## 2. Lease A Treehouse Worktree

From the backing repository, acquire a durable worktree lease:

```bash
treehouse status
worktree_path="$(treehouse get --lease --lease-holder "issue-<number>")"
printf '%s\n' "$worktree_path"
cd "$worktree_path"
```

After entering the leased worktree:

1. Verify it is the expected repository with `git remote -v` and `git status --short --branch`.
2. Fetch the upstream default branch.
3. Create or switch to a branch named for the issue, such as `fix/issue-<number>-short-topic`.
4. Ensure the branch starts from the latest upstream default branch unless the issue requires another base.

Use `treehouse return "$worktree_path"` only after the work is pushed and there is no local state that must be preserved. Use `treehouse status` to confirm leases.

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

## Validation
- ...

## Notes
- ...
PR_BODY
)"
```

The PR body must include the issue link, behavioral scope, validation commands with pass/fail status, and known residual risk. Do not hide skipped checks.

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

## 8. Return Or Preserve The Worktree

When the PR is approved or the workflow is otherwise complete:

1. Confirm all commits are pushed: `git status --short --branch`.
2. If the worktree is clean and no local-only state is needed, release it:
   - `treehouse return "$worktree_path"`
3. If the worktree must remain available for follow-up, keep the lease and report the path, branch, PR URL, and reason.
4. Use `treehouse prune` only as a dry-run cleanup check unless the user explicitly asks to delete candidates.

## Final Report

Report:

- Issue number and PR URL.
- Worktree path and whether it was returned or remains leased.
- Branch and commit hashes pushed.
- Acceptance checklist status.
- Quality/security gates run and results.
- Review threads or CI failures handled.
- Remaining blockers, risks, or reviewer decisions.

If the PR is approved, say so plainly. If not, state the exact next condition needed for approval.
