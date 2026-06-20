---
name: issue-backed-oss-contribution-review
description: Use this skill when reviewing, planning, or implementing an OSS contribution tied to a GitHub issue or PR, especially when the user asks whether a branch actually fixes an upstream issue, wants unresolved gaps found, needs contribution docs applied, or needs merge-conflict and PR-readiness work grounded in maintainer discussion.
---

# Issue-Backed OSS Contribution Review

## Workflow

1. Establish the issue contract.
   - Identify the upstream issue, PR, local branch, target base branch, and any linked specifications or maintainer comments.
   - Fetch GitHub issue and PR context with `gh` when available. Prefer read-only `gh issue view`, `gh pr view`, and `gh pr diff` before browser or ad hoc scraping.
   - If the issue has unresolved maintainer questions or product/API choices, surface them before implementing.

2. Read contribution rules before judging code.
   - Read the repository's `CONTRIBUTING`, pull request, testing, style, release-note, and docs rules relevant to the touched area.
   - Note required commands, commit/PR conventions, changelog fragments, generated files, and forbidden workflow changes.
   - Do not update remotes, push, or rewrite history unless the user explicitly asks.

3. Build an acceptance checklist.
   - Convert the issue discussion into checkable bullets: behavior to add or fix, non-goals, compatibility promises, docs expectations, tests, and maintainer constraints.
   - Include every linked external spec or upstream issue that changes expected behavior.
   - Treat broader-than-requested changes as risks unless the issue discussion clearly supports them.

4. Compare the branch to the checklist.
   - Inspect `git status`, current branch, merge base, and diff against the intended base.
   - Read changed files plus related callers, tests, schemas, docs, and public API definitions before editing.
   - Look for missing paths, inconsistent semantics across old/new implementations, stale docs, incomplete tests, migration or compatibility gaps, and changes that only satisfy part of the issue.

5. Report or fix with issue traceability.
   - For review-only requests, lead with findings ordered by severity. Each finding must cite the issue requirement and local evidence.
   - For implementation requests, make the smallest changes that close checklist gaps, preserving unrelated user work.
   - When the right fix is ambiguous, stop with the exact decision needed and the tradeoff.

6. Validate like an upstream maintainer.
   - Run the repository's required targeted tests and formatting/lint checks for the touched area.
   - If full validation is too expensive or unavailable, run the closest targeted checks and state the remaining risk.
   - Re-check the acceptance checklist after tests pass; do not call the contribution ready while any issue requirement is unaccounted for.

7. Package the PR state.
   - Summarize what now satisfies the issue, what tests ran, and any residual maintainer decisions.
   - If asked to update a PR body, include issue links, behavioral scope, validation, and known non-goals.
   - If conflicts were fixed, call out conflict-sensitive files and rerun validation touching those areas.

## Output Rules

- Keep private local paths out of reusable summaries unless the user needs a local command.
- Prefer concrete file and line evidence over broad judgments.
- Distinguish `bug`, `scope gap`, `maintainer decision`, `test gap`, and `docs gap`.
- Do not present a branch as upstream-ready solely because tests pass; it must satisfy the issue contract and contribution rules.
