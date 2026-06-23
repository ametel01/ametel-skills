---
name: teach
description: Use this skill when the user wants a staged teaching workflow in this repository workspace, with lessons, learning records, and retention checks across multiple turns.
metadata:
  argument-hint: "What would you like to learn about?"
  disable-model-invocation: "true"
---

# Teach

Use this skill when the user wants stateful learning inside `teach/` and asks for repeated sessions, lessons, or practice planning.

## Activation check

- Trigger when the user asks for instruction, concept mastery, or progressive exercises tied to workspace files.
- If the request is a single factual answer, answer directly and skip the teaching workflow.
- If the request implies a sequence or retention objective, run the steps below.

## Teaching workspace state

The workspace state lives in:

- `MISSION.md` (format: `MISSION-FORMAT.md`)
- `RESOURCES.md` (format: `RESOURCES-FORMAT.md`)
- `learning-records/*.md` (format: `LEARNING-RECORD-FORMAT.md`)
- `reference/*.html`
- `lessons/*.html`
- `assets/*`
- `NOTES.md`

Treat these as source-of-truth for what to teach next and what to revisit.

## Learning workflow

1. Read `MISSION.md` first.
  - If missing, ask one clarifying question before creating content.
2. Read the latest `learning-records/*.md` and infer the zone of proximal development.
3. Select one lesson objective that matches `MISSION.md` and fills one concrete gap.
4. Create or update references under `reference/` before creating multiple lessons from the same concept.
5. Write one lesson to `lessons/000x-<dash-case-name>.html`.
6. Append one `learning-records/*.md` reflection entry before finishing.

## Lesson rules

- Lesson scope: one tightly-scoped concept with one immediate practice loop.
- Include a primary source link for each factual claim.
- End with retrieval/review prompt and next-step decision tied to evidence.
- Prefer a shared component from `assets/` before inventing new lesson markup.

## Core sections

### Philosophy

Three goals should be balanced:

- Knowledge from high-trust resources
- Skills via interactive practice loops
- Wisdom via community or real-world interaction

Keep lessons short and memorable: retrieval, spacing, and interleaving should dominate session design.

### Lessons

A lesson is the primary unit in this workspace and should be a single HTML file in `lessons/`.

### Assets

Read existing files in `assets/` first. Add components only when reuse is expected for future lessons.

### The Mission

If mission is unclear, ask a single clarifying question before proposing or authoring new lessons.

### Zone of proximal development

Before each lesson, rank the gap from `learning-records`: known → uncertain → risky. Train only one risk band per session.

### Skills and knowledge split

- Skills-first topics (interviewing, yoga, command-line practice): prioritize interaction and feedback.
- Knowledge-first topics (definitions, taxonomies, APIs): prioritize reference precision and retention checks.

### Wisdom

If a user asks questions needing real-world context, suggest practical communities or public practice groups and then teach how to test claims externally.

### Validation loop

1. Confirm lesson and records follow numbering and naming conventions.
2. Confirm references are stable and reachable.
3. Confirm the lesson gives one clearly measurable next-step check.
