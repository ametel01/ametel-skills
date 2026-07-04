#!/usr/bin/env python3
"""Publish a to-issues JSON manifest with GitHub CLI."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


Issue = dict[str, Any]

DEFAULT_LABEL_DEFINITIONS: dict[str, dict[str, str]] = {
    "agent-ready": {
        "color": "0E8A16",
        "description": "Ready for autonomous agent implementation",
    },
    "parallel-safe": {
        "color": "1D76DB",
        "description": "Can be implemented in parallel with sibling issues",
    },
    "type:bug": {
        "color": "D73A4A",
        "description": "Bug fix work",
    },
    "type:docs": {
        "color": "0075CA",
        "description": "Documentation work",
    },
    "type:feature": {
        "color": "A2EEEF",
        "description": "Feature work",
    },
}

FALLBACK_LABEL = {
    "color": "C5DEF5",
    "description": "Created by to-issues publishing",
}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def run(cmd: list[str], *, dry_run: bool = False) -> str:
    if dry_run:
        print("+ " + shlex.join(cmd))
        return ""
    result = subprocess.run(cmd, check=False, text=True, capture_output=True)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        fail(f"command failed: {' '.join(cmd)}")
    return result.stdout.strip()


def issue_number(value: str) -> str:
    match = re.search(r"/issues/(\d+)(?:$|[?#])", value)
    if match:
        return match.group(1)
    match = re.fullmatch(r"#(\d+)", value)
    if match:
        return match.group(1)
    if re.fullmatch(r"\d+", value):
        return value
    return value


def looks_like_issue_ref(value: str) -> bool:
    return bool(
        re.fullmatch(r"\d+", value)
        or re.fullmatch(r"#\d+", value)
        or re.search(r"https://github\.com/[^/]+/[^/]+/issues/\d+(?:$|[?#])", value)
    )


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
    if not isinstance(data, dict):
        fail("manifest must be a JSON object")
    issues = data.get("issues")
    if not isinstance(issues, list) or not issues:
        fail("manifest must contain a non-empty issues array")
    if "default_labels" in data and not isinstance(data["default_labels"], list):
        fail("default_labels must be an array when present")
    if "label_definitions" in data and not isinstance(data["label_definitions"], dict):
        fail("label_definitions must be an object when present")
    for label, definition in data.get("label_definitions", {}).items():
        if not isinstance(definition, dict):
            fail(f"label_definitions.{label} must be an object")
        color = definition.get("color")
        if color is not None and not re.fullmatch(r"[0-9A-Fa-f]{6}", str(color)):
            fail(f"label_definitions.{label}.color must be a 6-character hex value")
        description = definition.get("description")
        if description is not None and not isinstance(description, str):
            fail(f"label_definitions.{label}.description must be a string")
    ids: set[str] = set()
    for i, issue in enumerate(issues):
        if not isinstance(issue, dict):
            fail(f"issues[{i}] must be an object")
        for field in ("id", "title", "what_to_build", "acceptance_criteria"):
            if field not in issue:
                fail(f"issues[{i}] missing required field: {field}")
        if not isinstance(issue["id"], str) or not issue["id"]:
            fail(f"issues[{i}].id must be a non-empty string")
        if not isinstance(issue["title"], str) or not issue["title"].strip():
            fail(f"issues[{i}].title must be a non-empty string")
        if not isinstance(issue["what_to_build"], str) or not issue["what_to_build"].strip():
            fail(f"issues[{i}].what_to_build must be a non-empty string")
        if issue["id"] in ids:
            fail(f"duplicate issue id: {issue['id']}")
        ids.add(issue["id"])
        if not isinstance(issue["acceptance_criteria"], list) or not issue["acceptance_criteria"]:
            fail(f"issues[{i}].acceptance_criteria must be a non-empty array")
        if any(not str(criterion).strip() for criterion in issue["acceptance_criteria"]):
            fail(f"issues[{i}].acceptance_criteria must not contain empty entries")
        issue.setdefault("wave", 0)
        if not isinstance(issue["wave"], int) or issue["wave"] < 0:
            fail(f"issues[{i}].wave must be a non-negative integer")
        issue.setdefault("blocked_by", [])
        issue.setdefault("parallel_safe_with", [])
        issue.setdefault("coordinates_with", [])
        issue.setdefault("coordination_risks", [])
        issue.setdefault("labels", [])
        for field in ("blocked_by", "parallel_safe_with", "coordinates_with", "coordination_risks", "labels"):
            if not isinstance(issue[field], list):
                fail(f"issues[{i}].{field} must be an array")
    for issue in issues:
        for field in ("blocked_by", "parallel_safe_with", "coordinates_with"):
            for ref in issue.get(field, []):
                value = str(ref)
                if value not in ids and not looks_like_issue_ref(value):
                    fail(
                        f"issue {issue['id']} has {field} reference {value!r}; "
                        "use a local issue id, issue number, #number, or GitHub issue URL"
                    )
    return data


def all_labels(manifest: dict[str, Any]) -> list[str]:
    labels = [str(label) for label in manifest.get("default_labels", [])]
    for issue in manifest["issues"]:
        labels.extend(str(label) for label in issue.get("labels", []))
    return unique(labels)


def label_definition(manifest: dict[str, Any], label: str) -> dict[str, str]:
    definitions = manifest.get("label_definitions", {})
    value = definitions.get(label) if isinstance(definitions, dict) else None
    if isinstance(value, dict):
        return {
            "color": str(value.get("color") or DEFAULT_LABEL_DEFINITIONS.get(label, FALLBACK_LABEL)["color"]),
            "description": str(
                value.get("description") or DEFAULT_LABEL_DEFINITIONS.get(label, FALLBACK_LABEL)["description"]
            ),
        }
    return DEFAULT_LABEL_DEFINITIONS.get(label, FALLBACK_LABEL)


def ensure_labels(repo: str, manifest: dict[str, Any], *, dry_run: bool) -> None:
    labels = all_labels(manifest)
    if not labels:
        return
    if dry_run:
        for label in labels:
            definition = label_definition(manifest, label)
            run(
                [
                    "gh",
                    "label",
                    "create",
                    label,
                    "--repo",
                    repo,
                    "--color",
                    definition["color"],
                    "--description",
                    definition["description"],
                ],
                dry_run=True,
            )
        return

    output = run(["gh", "label", "list", "--repo", repo, "--limit", "1000", "--json", "name"])
    try:
        existing = {item["name"] for item in json.loads(output)}
    except Exception as exc:  # noqa: BLE001 - command output is external
        fail(f"could not parse gh label list output: {exc}")

    for label in labels:
        if label in existing:
            continue
        definition = label_definition(manifest, label)
        run(
            [
                "gh",
                "label",
                "create",
                label,
                "--repo",
                repo,
                "--color",
                definition["color"],
                "--description",
                definition["description"],
            ]
        )


def topological_order(issues: list[Issue]) -> list[Issue]:
    by_id = {issue["id"]: issue for issue in issues}
    remaining = set(by_id)
    ordered: list[Issue] = []
    while remaining:
        ready = [
            by_id[issue_id]
            for issue_id in remaining
            if all(blocker not in by_id or blocker not in remaining for blocker in by_id[issue_id].get("blocked_by", []))
        ]
        if not ready:
            fail("dependency cycle detected in blocked_by issue ids")
        ready.sort(key=lambda issue: (int(issue.get("wave", 0)), issues.index(issue)))
        for issue in ready:
            ordered.append(issue)
            remaining.remove(issue["id"])
    return ordered


def resolve_ref(ref: str, created: dict[str, dict[str, str]], *, dry_run: bool) -> str:
    if ref in created:
        return created[ref]["url"]
    if dry_run and re.fullmatch(r"[A-Za-z0-9_.:-]+", ref):
        return f"[{ref}]"
    return ref


def render_refs(refs: list[str], created: dict[str, dict[str, str]], *, dry_run: bool) -> str:
    resolved = [resolve_ref(str(ref), created, dry_run=dry_run) for ref in refs]
    return ", ".join(resolved) if resolved else "None"


def render_body(issue: Issue, created: dict[str, dict[str, str]], *, dry_run: bool) -> str:
    if issue.get("body"):
        body = str(issue["body"])
        for issue_id, info in created.items():
            body = body.replace(f"{{{{issue:{issue_id}}}}}", info["url"])
        return body

    lines: list[str] = []
    parent = issue.get("parent")
    if parent:
        lines += ["## Parent", "", str(parent), ""]

    lines += ["## What to build", "", str(issue["what_to_build"]).strip(), ""]
    lines += ["## Acceptance criteria", ""]
    for criterion in issue["acceptance_criteria"]:
        text = str(criterion).strip()
        lines.append(text if text.startswith("- [ ]") else f"- [ ] {text}")
    lines.append("")

    wave = issue.get("wave", 0)
    wave_note = issue.get("wave_note") or (
        "Can start immediately." if not issue.get("blocked_by") else "Unlocks after the blocking issue(s) complete."
    )
    lines += ["## Execution wave", "", f"Wave {wave}. {wave_note}", ""]

    lines += ["## Blocked by", ""]
    blockers = issue.get("blocked_by", [])
    if blockers:
        for blocker in blockers:
            lines.append(f"- {resolve_ref(str(blocker), created, dry_run=dry_run)}")
    else:
        lines.append("None - can start immediately")
    lines.append("")

    lines += ["## Parallelism", ""]
    lines.append(f"- Parallel-safe with: {render_refs(issue.get('parallel_safe_with', []), created, dry_run=dry_run)}")
    lines.append(f"- Coordinates with: {render_refs(issue.get('coordinates_with', []), created, dry_run=dry_run)}")
    risks = issue.get("coordination_risks", [])
    lines.append("- Coordination risks: " + ("; ".join(str(risk) for risk in risks) if risks else "None"))
    lines.append("")

    stories = issue.get("user_stories", [])
    if stories:
        lines += ["## User stories covered", ""]
        for story in stories:
            lines.append(f"- {story}")
        lines.append("")

    extra = issue.get("body_extra")
    if extra:
        lines += ["## Notes", "", str(extra).strip(), ""]

    return "\n".join(lines).rstrip() + "\n"


def repo_from_gh() -> str:
    output = run(["gh", "repo", "view", "--json", "nameWithOwner"])
    try:
        return json.loads(output)["nameWithOwner"]
    except Exception as exc:  # noqa: BLE001 - command output is external
        fail(f"could not detect GitHub repository from gh output: {exc}")


def write_temp_body(body: str) -> str:
    temp = tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".md")
    with temp:
        temp.write(body)
    return temp.name


def create_issue(
    issue: Issue,
    repo: str,
    default_labels: list[str],
    created: dict[str, dict[str, str]],
    *,
    dry_run: bool,
) -> dict[str, str]:
    body_path = write_temp_body(render_body(issue, created, dry_run=dry_run))
    try:
        labels = unique(default_labels + [str(label) for label in issue.get("labels", [])])
        cmd = ["gh", "issue", "create", "--repo", repo, "--title", str(issue["title"]), "--body-file", body_path]
        for label in labels:
            cmd += ["--label", label]
        if issue.get("assignees"):
            cmd += ["--assignee", ",".join(str(assignee) for assignee in issue["assignees"])]
        if issue.get("milestone"):
            cmd += ["--milestone", str(issue["milestone"])]
        if issue.get("type"):
            cmd += ["--type", str(issue["type"])]
        if issue.get("parent"):
            cmd += ["--parent", issue_number(str(issue["parent"]))]
        blockers = [
            created[str(blocker)]["number"] if str(blocker) in created else issue_number(str(blocker))
            for blocker in issue.get("blocked_by", [])
        ]
        if blockers:
            cmd += ["--blocked-by", ",".join(blockers)]

        if dry_run:
            run(cmd, dry_run=True)
            return {
                "id": str(issue["id"]),
                "title": str(issue["title"]),
                "url": f"DRY-RUN:{issue['id']}",
                "number": str(issue["id"]),
                "wave": str(issue.get("wave", 0)),
            }

        url = run(cmd)
        return {
            "id": str(issue["id"]),
            "title": str(issue["title"]),
            "url": url,
            "number": issue_number(url),
            "wave": str(issue.get("wave", 0)),
        }
    finally:
        Path(body_path).unlink(missing_ok=True)


def update_body(issue: Issue, repo: str, created: dict[str, dict[str, str]], *, dry_run: bool) -> None:
    info = created[str(issue["id"])]
    body_path = write_temp_body(render_body(issue, created, dry_run=dry_run))
    try:
        cmd = ["gh", "issue", "edit", info["number"], "--repo", repo, "--body-file", body_path]
        run(cmd, dry_run=dry_run)
    finally:
        Path(body_path).unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish a to-issues manifest with gh issue create.")
    parser.add_argument("manifest", type=Path, help="Path to a JSON issue manifest.")
    parser.add_argument("--repo", help="GitHub repository in OWNER/REPO form. Defaults to manifest repo or gh repo view.")
    parser.add_argument("--output", type=Path, help="Write created issue URLs as JSON.")
    parser.add_argument("--dry-run", action="store_true", help="Print gh commands without creating issues.")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    repo = args.repo or manifest.get("repo")
    if not repo:
        if args.dry_run:
            repo = "OWNER/REPO"
        else:
            repo = repo_from_gh()

    default_labels = [str(label) for label in manifest.get("default_labels", [])]
    ordered = topological_order(manifest["issues"])

    if not args.dry_run:
        run(["gh", "auth", "status"])

    ensure_labels(str(repo), manifest, dry_run=args.dry_run)

    created: dict[str, dict[str, str]] = {}
    for issue in ordered:
        info = create_issue(issue, str(repo), default_labels, created, dry_run=args.dry_run)
        created[str(issue["id"])] = info
        print(f"{info['id']}: {info['url']}")

    for issue in ordered:
        update_body(issue, str(repo), created, dry_run=args.dry_run)

    result = {"repo": repo, "issues": [created[str(issue["id"])] for issue in ordered]}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
