# Strict Diataxis For Codebase-Backed Documentation

Use this reference when creating documentation from source code.
Every content page must be one Diataxis form: tutorial, how-to guide, reference, or explanation.
Use landing pages only for orientation and navigation.
Before choosing the Diataxis form, choose the audience: end user of the deployed product, or developer/maintainer of the codebase.

## Audience Boundary

User docs are for people using the deployed application or product.
Think SaaS help center: what the user can understand and do in the live product.
User docs must not include:

- local setup or running the application locally
- package-manager commands
- testing, linting, typechecking, or build commands
- repository layout
- source-code architecture for maintainers
- CI, release, deployment internals, or contributor workflows

Developer docs are for people working on, integrating with, operating, or contributing to the codebase.
Developer docs should cover, when supported by code evidence:

- architecture and implementation logic
- domain model and data flow
- local setup and run commands
- testing, linting, typechecking, and build commands
- package scripts and Make targets
- source layout and module boundaries
- CI, deployment internals, release workflow, and contribution workflow

## Default Full Markdown Set

When the user asks to document a codebase without naming a specific artifact, create both user and developer docs.
Do not ask the user to pick a target first.
Use `documentation/` as the default root for new full-set docs; do not default to `docs/`.

Scope arguments override the default:

- `author-codebase-docs dev` or `author-codebase-docs developer`: create only developer docs.
- `author-codebase-docs user` or `author-codebase-docs users`: create only user docs.

Baseline tree:

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

Developer-only tree:

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

User-only tree:

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

Adapt the tree to the codebase:

- Create specific content pages inside the Diataxis category directories, such as `tutorials/first-success.md`, `how-to-guides/deploy.md`, `reference/cli.md`, or `explanation/architecture.md`.
- Split how-to material into one page per real user task.
- Split reference material into API, CLI, config, data-model, event, or extension reference pages when the codebase has those surfaces.
- Omit pages that would be empty or speculative.
- Use an existing non-`docs/` documentation root if the repo already has a coherent one.
- Treat existing `docs/` pages as source material unless the user explicitly asks to update `docs/`.

Never create ambiguous content pages such as `overview.md`, `getting-started.md`, `setup.md`, `guide.md`, or `concepts.md`.
If that content is needed, classify it first:

- first-run learning path -> tutorial
- operational task -> how-to guide
- command/API/config facts -> reference
- architecture/rationale/concepts -> explanation

## Compass

Ask two questions:

1. Does the content inform action or cognition?
2. Does it serve acquisition of skill or application of skill?

| Content informs | User is | Documentation form |
| --- | --- | --- |
| Action | Acquiring skill | Tutorial |
| Action | Applying skill | How-to guide |
| Cognition | Applying skill | Reference |
| Cognition | Acquiring skill | Explanation |

## Codebase Evidence By Form

### Tutorial

Use examples, tests, sample apps, fixtures, local dev scripts, and quick-start commands as evidence.
Design a safe first success. Keep the path linear and avoid options.

For user docs, the first success must happen in the deployed product or a user-facing product surface.
Do not document local setup in user tutorials.
For developer docs, first success can be local setup, first test run, or first code change.

Good sources:

- `README` quick starts
- example directories
- smoke tests
- package scripts
- local dev compose files
- minimal API or CLI usage in tests

### How-To Guide

Use real workflows from scripts, CI, deployment config, integration tests, issue patterns, or existing operational docs.
Start from a user goal, not from a product feature.

For user docs, the goal must be something an end user can accomplish in the deployed product.
For developer docs, the goal may be local setup, debugging, testing, linting, building, deploying, or extending the codebase.

Good sources:

- Make targets and package scripts
- CI workflows
- deployment manifests
- integration tests
- CLI commands
- route handlers and service boundaries
- troubleshooting comments in existing docs

### Reference

Use source definitions and tests as the authority.
Keep wording neutral and patterned.

For user docs, reference must describe user-visible product facts: screens, fields, roles, permissions, user-visible states, limits, errors, settings, or customer-facing public APIs.
For developer docs, reference may describe internal APIs, CLI flags, config, environment variables, schemas, package scripts, test commands, modules, events, or extension points.

Good sources:

- exported types and functions
- route definitions
- API schemas
- CLI parser definitions
- config/env schema validation
- event definitions
- database migrations
- generated docs if present

### Explanation

Use architecture, data flow, design tradeoffs, constraints, and rationale visible in the code or existing decision records.
If rationale is not present, describe observed structure and label any inference.

For user docs, explanation should cover product concepts and user-visible behavior.
For developer docs, explanation should cover architecture, implementation logic, domain model, data flow, design rationale, and operational internals.

Good sources:

- ADRs and design docs
- module boundaries
- dependency direction
- domain model files
- tests that encode business rules
- comments explaining non-obvious constraints
- git history only when useful and cheap

## Distinctions To Preserve

- Tutorial vs how-to: the difference is study vs work, not beginner vs advanced.
- Reference vs explanation: the difference is lookup while working vs understanding while reflecting.
- Tutorial content should eliminate the unexpected; how-to content should prepare for real-world variation.
- Reference should describe facts; explanation may discuss why, tradeoffs, and alternatives.
- Audience groupings such as `user/` and `developer/` are allowed, but each audience subtree must still preserve the four Diataxis forms.
- README files are landing pages only. They may summarize and link, but must not become mixed-purpose documentation.
- User docs must never contain local run, test, lint, build, source install, CI, or contributor instructions.
- Developer docs should contain local run, test, lint, build, architecture, logic, and workflow documentation when supported by evidence.

## Audit Questions

- What user need does this page serve?
- Is the user studying or working?
- Is the page guiding action or supporting cognition?
- Is this page exactly one Diataxis form?
- Is this page exactly one audience: deployed-product user or codebase developer?
- If this is user docs, is every topic relevant to a user of the deployed product?
- If this is user docs, did you exclude local setup, testing, linting, build, CI, and contributor commands?
- If this is developer docs, did you include the relevant architecture, logic, local run, test, lint, and build information supported by the repo?
- Are commands and options backed by current source or tests?
- Are examples safe to run and likely to produce the documented result?
- Is explanation interrupting a tutorial or how-to guide?
- Is task guidance polluting a reference page?
- Is any root-level audience page hiding content that belongs under tutorials, how-to guides, reference, or explanation?
- Would splitting, moving, linking, or trimming make the page more useful?
