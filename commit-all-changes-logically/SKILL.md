---
name: commit-all-changes-logically
description: Use when the user asks to commit all current changes, commit all unstaged changes, commit implemented work, review unstaged changes before committing, or turn a dirty worktree into one or more logical git commits across Claude or Codex sessions.
---

# Commit All Changes Logically

## Workflow

1. Inspect the repository state with `git status --short` and identify the current branch.
2. Read the changed files before staging. Use `git diff`, `git diff --stat`, and targeted file reads to understand intent and avoid committing secrets, build artifacts, or unrelated local noise.
3. Decide whether the changes belong in a single commit or multiple logical commits. Use a single commit when the user explicitly asks for one or when all changes serve one coherent purpose.
4. If multiple commits are appropriate, group files by behavior, documentation, tests, dependency updates, or generated artifacts. Do not split changes in a way that leaves intermediate commits broken.
5. Stage deliberately with pathspecs or patch staging. Avoid `git add .` unless the full dirty state has been reviewed and is intended for commit.
6. Run the relevant lightweight verification for the touched ecosystem when feasible. If verification is skipped or fails, state that before committing unless the user already asked to commit regardless.
7. Write concise commit messages in imperative mood. Prefer a specific subject over a broad one, and add a short body only when it clarifies scope or risk.
8. After committing, report the commit hash, subject, included scope, and any verification performed.

## Guardrails

- `permissions.deny` should forbid `.env`, secrets, credentials, tokens, home directory reads (`~/`), and network transfer tools such as `curl` or `wget` when they target secret-bearing paths.
- Never overwrite, revert, or discard user changes unless the user explicitly requests it.
- Do not amend, rebase, push, or create a pull request unless requested.
- Do not commit files outside the repository or files ignored by git unless the user explicitly asks and the repository policy allows it.
- If unrelated changes are present, either leave them unstaged or ask for direction when they cannot be safely separated.
- If secrets, credentials, private keys, or large unintended artifacts appear in the diff, stop and surface the risk before staging.
