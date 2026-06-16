---
name: author-codebase-docs
description: "Use this skill when creating or updating codebase documentation as strict Diataxis Markdown, including user docs, developer docs, README content, API/CLI reference, architecture notes, and contributor guides."
---

# Author Codebase Docs

Use this skill to produce documentation whose claims are backed by the repository.
Treat the codebase as the source of truth, and use Diataxis to choose the right documentation form.
Strictly follow Diataxis in every content page, page name, section boundary, and hierarchy decision.
Keep user docs and developer docs separate by audience before applying Diataxis.
When the user does not specify an artifact, create a full Markdown documentation set for both users and developers.
When the invocation includes `dev` or `developer`, create only developer docs.
When the invocation includes `user` or `users`, create only user docs.

## Reference

Read [references/diataxis-codebase-docs.md](references/diataxis-codebase-docs.md) when deciding whether content should be tutorial, how-to, reference, or explanation, or when planning a documentation hierarchy.

## Workflow

1. Establish scope.
   - If the user names a specific artifact, update or create that artifact.
   - If the invocation includes `dev` or `developer`, create only `documentation/developer/` plus an index if needed.
   - If the invocation includes `user` or `users`, create only `documentation/user/` plus an index if needed.
   - If the user only asks to document the codebase, generate the default full documentation set without asking which target to use.
   - Default output root for a new full set is `documentation/`, not `docs/`.
   - If the repo already has a non-`docs/` documentation root, use the existing structure when it is coherent.
   - If the repo only has `docs/`, do not default to adding new full-set pages there; keep existing `docs/` content as source material and create the new full set under `documentation/` unless the user explicitly asks to update `docs/`.

2. Map the codebase before writing.
   - Read existing `README`, `docs/**`, `AGENTS.md`, `CONTRIBUTING`, changelog, package manifests, Makefile/task files, CI workflows, and deployment config.
   - Inspect public interfaces: exported modules, APIs, CLI entrypoints, routes, config schemas, environment variables, generated artifacts, examples, and tests.
   - Prefer `rg`/`rg --files` and targeted reads. Do not infer behavior from filenames alone.

3. Choose the documentation form.
   - First choose the audience.
   - User docs are for users of the deployed application/product. Include only product capabilities, workflows, concepts, limits, and in-product reference that an end user can use.
   - Developer docs are for maintainers, contributors, integrators, or operators working with the codebase. Include architecture, domain logic, local setup, test/lint/build commands, deployment internals, APIs for developers, and contribution workflows.
   - Never put local development, testing, linting, build, install-from-source, repository structure, or contributor commands in user docs.
   - Tutorial: guided learning path for a new user acquiring skill.
   - How-to guide: task-focused directions for a competent user at work.
   - Reference: factual description of commands, APIs, options, config, data models, or behavior.
   - Explanation: context, rationale, architecture, tradeoffs, or conceptual overview.
   - Split mixed content instead of forcing one page to do several jobs.
   - Do not create ambiguous content pages such as `overview.md`, `getting-started.md`, `setup.md`, or `architecture.md` at an audience root. Classify the content as tutorial, how-to, reference, or explanation and place it under that category.

4. Plan the documentation tree when no artifact is specified.
   - Create `documentation/README.md` as the documentation index.
   - Create `documentation/user/` for user-facing docs unless the invocation is developer-only.
   - Create `documentation/developer/` for developer-facing docs unless the invocation is user-only.
   - Under each selected audience, use only Diataxis category directories: `tutorials/`, `how-to-guides/`, `reference/`, and `explanation/`.
   - Use `README.md` files only as landing/contents pages that orient the reader and link to Diataxis-category content; do not put mixed tutorial/how-to/reference/explanation content in a landing page.
   - Add only pages that the codebase can support with evidence; prefer accurate coverage over empty stub pages.
   - For the default no-scope invocation, use this strict baseline tree unless the codebase clearly calls for a different non-`docs/` structure:

```text
documentation/
  README.md
  user/
    README.md
    tutorials/
    how-to-guides/
    reference/
    explanation/
  developer/
    README.md
    tutorials/
    how-to-guides/
    reference/
    explanation/
```

   - For `author-codebase-docs user`, use only this subtree:

```text
documentation/
  README.md
  user/
    README.md
    tutorials/
    how-to-guides/
    reference/
    explanation/
```

   - For `author-codebase-docs dev` or `author-codebase-docs developer`, use only this subtree:

```text
documentation/
  README.md
  developer/
    README.md
    tutorials/
    how-to-guides/
    reference/
    explanation/
```
   - Within each category directory, create specific pages named after the user need they serve, such as `tutorials/first-success.md`, `how-to-guides/configure-authentication.md`, `reference/cli.md`, or `explanation/architecture.md`.

5. Draft from evidence.
   - Ground commands, options, imports, endpoint paths, env vars, file locations, and workflows in code or existing tests.
   - Prefer executable examples that match the repo's actual package manager and scripts.
   - For user docs, translate source evidence into deployed-product behavior and omit codebase commands unless they are user-facing product commands.
   - For developer docs, document local commands, repo workflows, architecture, implementation logic, tests, linting, and builds when supported by the codebase.
   - Link or name source modules sparingly when useful for maintainers; do not turn user docs into an implementation dump.
   - Mark unresolved assumptions explicitly rather than presenting guesses as facts.

6. Shape the documentation for use.
   - Put the user's likely first question near the top.
   - Keep tutorials safe, linear, concrete, and minimal on explanation.
   - Keep how-to guides goal-oriented and free of exhaustive reference detail.
   - Keep reference complete, patterned, neutral, and easy to scan.
   - Keep explanation bounded around a question or topic.
   - Add navigation links only where they improve the reader's next step.

7. Verify.
   - Run cheap checks that validate documented commands, examples, generated tables, links, or markdown formatting when available.
   - If commands are expensive, unavailable, or unsafe, state what was not run and why.
   - Re-read changed docs for stale claims, unsupported promises, broken headings, and duplicated content.

## Output Standards

- Use the repo's existing documentation style, vocabulary, heading levels, and file layout.
- Keep documentation current-state, not aspirational, unless the file is explicitly a plan or roadmap.
- Do not invent setup steps, configuration keys, API fields, command flags, ports, or guarantees.
- Do not mix Diataxis forms in one content page. Move or link material instead.
- Do not mix audiences in one content page. User docs and developer docs must answer different needs.
- Do not include local setup, testing, linting, build, package-manager, source install, repository layout, CI, or contributor workflow content in user docs.
- Do include architecture, implementation logic, local setup, testing, linting, build, package-manager, source install, repository layout, CI, and contributor workflow content in developer docs when the codebase supports it.
- Do not use vague catch-all pages such as `overview.md`, `getting-started.md`, `setup.md`, `guide.md`, or `concepts.md` unless they are landing pages named `README.md`; classify their content by Diataxis type.
- Do not put tutorials, how-to guides, reference, and explanation side-by-side in one README except as short navigational summaries.
- Do not ask the user to choose a target when the prompt already asks for codebase documentation; use the default full documentation set.
- Do not create user docs when invoked with `dev` or `developer`.
- Do not create developer docs when invoked with `user` or `users`.
- Do not place a new full documentation set under `docs/` by default.
- Do not create changelogs or policy docs unless requested or clearly consistent with the repo.
- Preserve unrelated user changes in dirty worktrees.
- Prefer a small, accurate document over a comprehensive but weakly evidenced one.

## Common Artifact Patterns

### README

Use only as a landing/contents page: identify the audience, describe what the documentation set contains, and link to tutorials, how-to guides, reference, and explanation. Keep executable steps and detailed concepts out of README landing pages.

### Tutorial

Use for first success: prerequisites, a safe toy scenario, exact steps, expected outputs, cleanup/reset, and links to how-to/reference pages.
For user docs, this means first success in the deployed product UI or user-facing product surface.
For developer docs, this can mean first local run, first test run, or first code change.

### How-To Guide

Use for real tasks: goal, prerequisites, decision points, steps, verification, troubleshooting, and links to reference for exhaustive options.
For user docs, tasks must be deployed-product tasks.
For developer docs, tasks may include local setup, debugging, testing, linting, building, releasing, or extending the codebase.

### Reference

Use for factual lookup: command flags, API endpoints, exported modules, config files, environment variables, data models, events, errors, or extension points. Mirror the structure of the thing documented.
For user docs, reference must be product-facing: screens, fields, roles, permissions, user-visible states, limits, errors, settings, or public product APIs meant for customers.
For developer docs, reference may include source modules, internal APIs, CLI flags, config, environment variables, schemas, generated artifacts, tests, or extension points.

### Explanation

Use for understanding: architecture, lifecycle, data flow, design rationale, security model, tradeoffs, constraints, or operational concepts.
For user docs, explanation should describe product concepts and user-visible behavior.
For developer docs, explanation should describe system architecture, domain model, implementation logic, data flow, design rationale, and operational internals.
