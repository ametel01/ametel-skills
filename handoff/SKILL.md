---
name: handoff
description: Use this skill when the user wants to preserve the current conversation for a fresh session, branch into another workflow, resume later, or create a compact handoff document for another agent.
---

# Handoff

Write a handoff document summarising the current conversation so a fresh agent can continue the work.

## Workflow

1. Identify the next session's purpose. If the user passed arguments, treat them as that focus and tailor the document accordingly.
2. Gather the durable artifacts already created: PRDs, plans, ADRs, issues, commits, diffs, notes, or generated files.
3. Write a concise markdown handoff to the OS temp directory, not the current workspace. Resolve the temp directory from `$TMPDIR`, falling back to `/tmp` on Unix-like systems or `%TEMP%` on Windows.
4. Include sections for current goal, key context, completed work, remaining work, important files or links, suggested skills, and risks or open questions.
5. Redact sensitive information such as API keys, passwords, tokens, private URLs, and personally identifiable information.
6. Report the absolute handoff path to the user.

## Gotchas

- Do not duplicate content already captured in other artifacts. Reference artifacts by path or URL instead.
- Keep the document useful to a fresh agent with no chat history.
- Suggested skills should name only skills that are relevant to the next session's work.
