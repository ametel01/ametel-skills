---
name: yes-flag-test-skill
description: Use this skill when the user asks for deterministic non-interactive testing in `-y` mode, including dry-run validation, scripted approvals, or CI-like flows.
---

# Yes-Flag Test Skill

Use this skill to validate commands that must run in non-interactive mode (`-y`, batch, or assume-yes) without manual confirmation drift.

## Workflow

1. Confirm scope.
   - Identify the command family (`install`, `delete`, `migrate`, etc.) and target environment.
   - List destructive operations and required safeguards (backups, dry-run, rollback path).
2. Prepare command configuration.
   - Use non-interactive flags explicitly (`-y`, `--yes`, `--non-interactive`, `--batch`) based on tool expectations.
   - Pass explicit input files/paths, not defaults.
3. Execute with a safety pass.
   - Prefer `--dry-run` or equivalent when available.
   - Capture output plus exit status.
4. Validate outcome.
   - Check command return code, created/modified files, and status messages.
   - Confirm no unexpected prompts were triggered.
5. Record the exact command and evidence in the final output.

## Gotchas

- Some tools ignore `-y` unless combined with environment flags (`CI=1`, `DEBIAN_FRONTEND=noninteractive`, etc.).
- Retrying a `-y` path can re-use cache state; check idempotency before second execution.
- If a command exposes a hidden interactive fallback, stop and convert to scripted input.

## Example

```bash
CI=1 docker-compose up --detach --remove-orphans
rg -n "^\[y/n\]" logs/build.log || true
```

## Validation loop

- If validation fails, adjust flags and rerun once; do not switch to a different mode unless needed.
