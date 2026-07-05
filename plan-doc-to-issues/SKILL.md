---
name: plan-doc-to-issues
description: Use this skill when the user wants a one-prompt workflow that reads local source docs, creates a scoped `/goal`-ready `PLAN.md`, then decomposes that plan into independently grabbable GitHub issues without separately invoking `create-plan-from-doc` and `to-issues`.
---

# Plan Doc To Issues

Create a bounded implementation plan from source documents, then publish tracer-bullet GitHub issues from that plan in the same run.

This skill composes the sibling skills `create-plan-from-doc` and `to-issues`. Treat those skills as normative contracts and read them completely before acting when available:

- `../create-plan-from-doc/SKILL.md`
- `../to-issues/SKILL.md`

If either sibling skill is missing, continue with the workflow below and report the missing contract in the final response.

## Inputs

Require at least one source document path. If the user gives no document path, ask for one before proceeding.

Also infer or accept:

- Scope within the document, such as a feature, section, issue, milestone, or implementation area.
- Project root and repository target.
- Optional parent issue URL or number.
- Optional dry-run instruction.

Resolve relative paths from the current working directory. Confirm every source file exists before planning. Stop for clarification only when a missing path, ambiguous path, or undetectable destination repo would make publishing unsafe.

## Boundaries

- Allowed inputs: local source documents, repo context, optional parent issue references, and optional dry-run or tracker instructions.
- Allowed outputs: `PLAN.md`, a local issue manifest, optional `PROGRESS.md`/`CHANGELOG.md` setup instructions, and GitHub issues in the detected destination repo.
- Forbidden actions: do not publish when the user asked for a dry run, do not close or edit parent issues, do not modify source documents, and do not create issues outside the detected or explicitly requested repository.

## Workflow

### 1. Build The Plan

Follow `create-plan-from-doc` semantics:

- Read the supplied documents enough to understand requirements, constraints, acceptance criteria, and conflicts.
- Track which requirements came from which source.
- Establish repository context from the nearest Git root and inspect the toolchain: package manager files, Makefile, CI workflows, test/lint/format/build configuration, and relevant source/test directories.
- Identify exact quality-gate commands for baseline, format, lint, tests, typecheck, build, and other project-specific checks.
- Write or replace `PLAN.md` in the project root unless the user explicitly requests another location.

`PLAN.md` must be `/goal` ready and include the required sections from `create-plan-from-doc`:

- `Source Documents`
- `Goals`
- `Non-Goals`
- `Definition of Done`
- `Assumptions and Open Questions`
- `Implementation Approach`
- `Quality Gates`
- `Progress Tracking`
- `Changelog Tracking`
- `Goal Handoff`
- `Incremental Steps`

Always include `Step 0: Progress and Changelog Tracking Setup`. Omit a distinct quality-gates setup step only when the repo already has clear gate commands and the plan lists them exactly.

Make each implementation step small enough for a focused commit. Each step must include concrete changes, validation commands, `PROGRESS.md` update instructions, `CHANGELOG.md` decision instructions, and a suggested commit message.

### 2. Convert The Plan Into Issues

Do not stop after writing `PLAN.md`. Use the completed plan as the canonical source for issue creation.

Follow `to-issues` semantics:

- Break the plan into vertical tracer-bullet issues that produce independently verifiable behavior.
- Prefer behavior slices over horizontal layer slices.
- Create enabling issues only for real prerequisites such as shared contracts, migrations, fixtures, quality-gate setup, or required tracking artifacts.
- Do not create a generic tracking issue. A `PROGRESS.md`/`CHANGELOG.md` setup issue is allowed only because `PLAN.md` requires concrete repository files before implementation.
- Assign dependency edges only for real blockers: required code, data, contracts, product decisions, migrations, external approvals, or test infrastructure.
- Treat shared files, dirty worktrees, changelog edits, and nearby modules as coordination risks unless one issue truly requires another result.
- Maximize parallelism by moving every issue to the earliest safe execution wave.

Each issue must record:

- Title
- Wave
- Blocked by, using `None - can start immediately` when unblocked
- Dependency edge type: `blocks`, `decision-blocks`, `enables`, or `coordinates-with`
- Parallel-safe siblings
- Coordination risks
- User stories or source requirements covered when available
- Acceptance criteria

## GitHub Publishing

Use GitHub publishing by default unless the user explicitly asks for a dry run or another tracker.

Before publishing:

1. Run `gh auth status`.
2. Detect the destination repo with `gh repo view --json nameWithOwner`.
3. Create a JSON issue manifest in the project root or a clearly named temporary planning file.
4. Use labels from the repo when obvious; otherwise use `agent-ready`, `parallel-safe`, and narrow `type:*` labels.

Prefer the bundled helper, which delegates to the sibling `to-issues` publisher:

```bash
python3 scripts/publish_github_issues.py --help
python3 scripts/publish_github_issues.py issues.json --repo OWNER/REPO --dry-run
python3 scripts/publish_github_issues.py issues.json --repo OWNER/REPO --output created-issues.json
```

Output contract: dry runs print a human-readable command preview to stdout; real publishing writes created issue data to the `--output` JSON file when supplied and sends diagnostics to stderr.

Run the dry run only when the user asks for a dry run or repo detection/authentication is unclear. Otherwise publish without asking for another confirmation.

After publishing, keep `PLAN.md` in place. Do not close or modify any parent issue.

## Final Response

Report:

- `PLAN.md` path.
- Created issue URLs grouped by execution wave.
- Same-wave issues that can be started by separate agents/worktrees at the same time.
- Any assumptions, skipped gates, missing sibling skill contracts, or GitHub publishing warnings.

If publishing could not complete, report the completed `PLAN.md`, the manifest path if created, and the exact blocker.
