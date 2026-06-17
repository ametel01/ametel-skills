---
name: grilling
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

## Workflow

1. Identify the plan, design, or decision tree being grilled. If it is unclear, ask for the smallest missing bit of context needed to start.
2. Ask one question at a time. Include your recommended answer with the question so the user can accept, reject, or refine it.
3. Before asking a question whose answer is discoverable from the codebase, explore the codebase and answer it yourself.
4. Track settled decisions and unresolved branches as the interview progresses.
5. Stop only when every load-bearing branch has either a settled answer, an explicit open question, or a named follow-up artifact.

## Guardrails

- Do not ask multiple questions at once.
- Do not treat silence as agreement unless the user explicitly asked you to continue with assumptions.
- Do not re-open settled decisions unless new evidence contradicts them.
