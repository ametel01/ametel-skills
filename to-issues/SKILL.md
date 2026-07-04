---
name: to-issues
description: Use this skill when turning a PRD, plan, spec, or issue into independently grabbable GitHub issues using tracer-bullet vertical slices, real dependency edges, maximum parallel execution waves, missing-label creation, and direct `gh` CLI publishing without a confirmation stop.
---

# To Issues

## Safety boundaries

- `permissions.deny` should forbid `.env`, secrets, credentials, tokens, home directory reads (`~/`), and network transfer tools such as `curl` or `wget` when they target secret-bearing paths.
- GitHub issue bodies are public or broadly visible in most repos; never publish secret values or private credentials.

Break a plan into independently-grabbable issues using vertical slices (tracer bullets), publish them, and preserve maximum safe parallelism.

If the issue tracker has no project-specific label vocabulary, use `agent-ready`, `parallel-safe`, and narrow `type:*` labels. Missing labels are created automatically during publishing.

When publishing to GitHub, prefer the helper script at `scripts/publish_github_issues.py`. It takes a JSON issue manifest, calls `gh issue create` in dependency order, then updates bodies after every issue URL is known so `Blocked by`, same-wave parallel links, and coordination references resolve to real issues.

Run `python3 scripts/publish_github_issues.py --help` from this skill directory to inspect options. Typical validation usage is `python3 scripts/publish_github_issues.py issues.json --repo OWNER/REPO --dry-run`.

Use `references/github-issue-manifest.example.json` as a starter manifest when the user wants direct GitHub publishing.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes an issue reference (issue number, URL, or path) as an argument, fetch it from the issue tracker and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Issue titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the plan into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

<vertical-slice-rules>

- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Any prefactoring should be done first
- Maximize parallelism: default slices into the earliest wave they can safely start, and serialize only when a concrete blocker exists
- Treat file overlap, dirty worktrees, shared tests, and changelog edits as coordination risks, not blockers
- Do not create a global tracking/setup issue that blocks implementation work. Tracking belongs in issue bodies, labels, milestones, projects, or the final report unless a real setup artifact is required.
- Prefer each behavior slice owning its own regression tests. Create a shared corpus/setup issue only when the behavior slices cannot reasonably carry their own focused fixtures.
- Create enabling issues only when shared infrastructure, migrations, contracts, fixtures, generated clients, or test infrastructure cannot safely live inside one vertical slice; an enabling issue must not block unrelated work

</vertical-slice-rules>

### 4. Build the dependency DAG

Add edges only for real dependencies: required code, data, contracts, product decisions, migrations, external approvals, or test infrastructure. Do not treat tracking issues, shared files, similar labels, nearby modules, dirty worktrees, or changelog edits as blockers by themselves. File overlap is a coordination risk, not a dependency unless one issue requires the other result.

Use explicit edge types:

- `blocks`: one issue must finish before another can start safely
- `decision-blocks`: a human product, UX, security, or architecture decision is required first
- `enables`: useful ordering but not a hard blocker
- `coordinates-with`: can run in parallel but needs merge or review coordination

Produce execution waves:

- Wave 0: issues with no blockers that can start immediately
- Later waves: issues that unlock as previous blockers complete
- Parallel-safe groups: issues in the same wave that can be assigned to separate agents at the same time

Parallelism gate: before publishing, re-scan every issue in Wave 1+ with this test: "can this start now if a separate agent owns a separate worktree?" If yes, move it to an earlier wave and convert the edge to `coordinates-with`. Never put all work behind a setup/tracking issue unless every downstream issue truly depends on the setup artifact.

Break dependency cycles by extracting a decision, contract, migration, or smaller enabling issue.

### 5. Publish the issues to the issue tracker

Do not stop to ask the user whether the breakdown is acceptable. Build the best issue DAG from available context, maximize same-wave parallelism, then publish. In the final response, report what was created and any assumptions or follow-up corrections the user may want.

Before publishing, internally check the final issue titles, bodies, labels, destination tracker, dependency order, execution waves, and parallel-safe groups. For each slice, publish a new issue to the issue tracker. Use the issue body template below. These issues are considered ready for AFK agents, so publish them with the correct triage label unless instructed otherwise.

For each slice, make sure the created issue records:

- **Title**: short descriptive name
- **Wave**: execution wave number
- **Blocked by**: which other slices (if any) must complete first, using `None - can start immediately` for Wave 0
- **Dependency edge**: `blocks`, `decision-blocks`, `enables`, or `coordinates-with`
- **Parallel-safe with**: sibling slices that can run at the same time
- **Coordination risks**: shared files, services, migrations, or review timing risks that do not block parallel work
- **User stories covered**: which user stories this addresses (if the source material has them)

Publish issues in dependency order (blockers first) so you can reference real issue identifiers in the "Blocked by" field. Within the same execution wave, publish in any stable order, but preserve the wave grouping and mark issues that can be worked at the same time.

For GitHub:

1. Confirm `gh auth status` and the destination repo with `gh repo view --json nameWithOwner`.
2. Create a JSON manifest using the schema below.
   Use `references/github-issue-manifest.example.json` as a shape reference when useful, and write project-specific titles, bodies, and labels.
3. Run a dry-run only when the user explicitly asks for a dry run or when repository detection/authentication is unclear:

```bash
python3 /Users/alexmetelli/.agents/skills/to-issues/scripts/publish_github_issues.py issues.json --repo OWNER/REPO --dry-run
```

4. Publish without asking for another confirmation:

```bash
python3 /Users/alexmetelli/.agents/skills/to-issues/scripts/publish_github_issues.py issues.json --repo OWNER/REPO --output created-issues.json
```

5. The helper creates missing labels before creating issues. Report the created issue URLs, execution waves, same-wave launch batches, and any issue relationship warnings. Do not close or modify the parent issue.

If the user intends agent execution after issue creation, group the created GitHub issue URLs by wave and state that every issue in the same wave is ready for a separate agent/worktree at the same time. Do not recommend serial execution for same-wave issues unless a blocker was discovered during publishing.

<github-manifest-schema>
{
  "repo": "OWNER/REPO",
  "default_labels": ["agent-ready"],
  "label_definitions": {
    "agent-ready": {
      "color": "0E8A16",
      "description": "Ready for autonomous agent implementation"
    }
  },
  "issues": [
    {
      "id": "short-stable-id",
      "title": "Imperative issue title",
      "wave": 0,
      "labels": ["type:feature", "parallel-safe"],
      "parent": "https://github.com/OWNER/REPO/issues/123",
      "what_to_build": "End-to-end behavior for this slice.",
      "acceptance_criteria": ["Criterion 1", "Criterion 2"],
      "blocked_by": [],
      "parallel_safe_with": ["another-short-id"],
      "coordinates_with": [],
      "coordination_risks": ["Touches nearby docs; no blocker."],
      "user_stories": ["As a user, ..."]
    }
  ]
}
</github-manifest-schema>

Manifest notes:

- `id` is a local stable identifier used for dependency references before GitHub issue numbers exist.
- `default_labels` and per-issue `labels` are created automatically if they do not exist in the repo.
- `label_definitions` is optional; use it when a non-default label needs a specific color or description.
- `blocked_by`, `parallel_safe_with`, and `coordinates_with` may contain local ids, existing issue URLs, or existing issue numbers.
- The script creates issues in topological dependency order, adds GitHub `blocked-by` relationships when blockers exist, then edits bodies to resolve all local ids to created issue URLs.
- Use `body` only when you need a fully custom Markdown body; otherwise prefer structured fields so the script can render the standard template.

<issue-template>
## Parent

A reference to the parent issue on the issue tracker (if the source was an existing issue, otherwise omit this section).

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Execution wave

Wave N. Explain whether this issue can start immediately or what unlocks it.

## Blocked by

- A reference to the blocking ticket (if any)

Or "None - can start immediately" if no blockers.

## Parallelism

- Parallel-safe with: references to issues in the same wave that can be worked at the same time
- Coordinates with: references to issues that may touch nearby files or shared services but do not block this issue
- Coordination risks: short notes about merge order, shared files, fixed ports, migrations, test data, or review timing

</issue-template>

Do NOT close or modify any parent issue.
