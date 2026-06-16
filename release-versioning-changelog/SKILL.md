---
name: release-versioning-changelog
description: Use this skill when doing ametel01 release, version bump, changelog, tag, GitHub Release, PyPI, GoReleaser, semantic versioning, Keep a Changelog, or release-notes work. Detect each repo's release variant before editing.
---

# Release Versioning Changelog

## Purpose

Handle release work without forcing one release model across repositories. The account commonly uses semantic versions, `v*` tags, GitHub Releases, and changelog entries, but automation differs by stack.

## When to use

Use when bumping versions, editing `CHANGELOG.md`, creating release notes, changing tag workflows, or touching release scripts.

## Evidence from repositories

Strength: Moderate.

- `weld-cli`: `CHANGELOG.md` follows Keep a Changelog and SemVer; `pyproject.toml` holds version; release workflow validates tag/input version, asserts `Unreleased` is empty, extracts release notes, builds with `uv build`, publishes to PyPI, and creates a GitHub Release.
- `agents-toolbelt`: `CHANGELOG.md` follows Keep a Changelog and SemVer; release workflow triggers on `v*` tags, uses GoReleaser, cosign, checksums, and provenance attestation.
- `vitals-db`: `CHANGELOG.md` follows Keep a Changelog/SemVer and release entries include release gates and GitHub tag links.
- `horizon-starknet`: release workflow creates GitHub releases for `v*` tags with generated notes and prerelease detection.
- `claw-training-dashboard` and `orgs-ai-harness`: no strong release evidence in sampled files.

## Standard workflow

1. Detect the repo's version source:
   - Python package: `pyproject.toml`.
   - Node/Bun package: package-local `package.json` versions when present.
   - Go CLI: tags and GoReleaser config/workflow.
   - Cairo package: `contracts/Scarb.toml`.
2. Read `CHANGELOG.md` if present before editing release notes.
3. Keep Keep a Changelog headings and SemVer tag style where already used.
4. Move `Unreleased` entries into the target version section when the repo requires it.
5. Run the repo's release gate or closest local equivalent before tagging.

## Commands

```bash
# weld-cli
ASSERT_UNRELEASED_EMPTY="<path-to-bundled-assert_unreleased_empty.py>"
EXTRACT_RELEASE_NOTES="<path-to-bundled-extract_release_notes.py>"
uv run python "$ASSERT_UNRELEASED_EMPTY" --help
uv run python "$ASSERT_UNRELEASED_EMPTY" --changelog CHANGELOG.md
uv run python "$EXTRACT_RELEASE_NOTES" --help
uv run python "$EXTRACT_RELEASE_NOTES" --changelog CHANGELOG.md --version VERSION
uv build

# agents-toolbelt
make verify

# horizon-starknet release is workflow-driven from v* tags
git tag vX.Y.Z

# vitals-db release gates are documented per changelog entry
bun run check:ci
bun run typecheck
bun run test
bun run build
```

## Required checks

- Version in code/config must match the intended tag when the repo has an explicit version file.
- Changelog entry must describe user-visible or functional changes, not just implementation churn.
- Release notes should come from the version's changelog section when scripts support that.
- Release workflows must preserve artifact, publishing, and provenance steps.

## Invariants

- Use `v*` tag style for repos whose release workflows trigger on `v*`.
- Do not leave populated `Unreleased` sections when a workflow asserts they are empty.
- Do not create a changelog section unsupported by existing format.
- Do not change license or release channel without explicit user direction.

## Common pitfalls

- `weld-cli` can be released manually through workflow dispatch, but the input version must match `pyproject.toml`.
- `horizon-starknet` generated release notes are workflow-driven; do not invent a manual changelog requirement there.
- `vitals-db` changelog entries include explicit release gates; preserve that habit when adding entries.

## Exceptions

If a repo has no changelog or release workflow, treat release guidance as conditional. Ask before adding a new release system.
