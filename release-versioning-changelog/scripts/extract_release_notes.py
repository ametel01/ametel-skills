#!/usr/bin/env python3
"""Extract one version section from a Keep a Changelog file."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print the changelog body for a requested release version.",
    )
    parser.add_argument(
        "--changelog",
        default="CHANGELOG.md",
        help="Path to the changelog file. Defaults to CHANGELOG.md.",
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Version to extract, with or without a leading v.",
    )
    return parser.parse_args()


def normalized(value: str) -> str:
    return value.strip().lower().removeprefix("v")


def section_for_version(text: str, version: str) -> str | None:
    wanted = normalized(version)
    matches = list(HEADING_RE.finditer(text))
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        heading_key = normalized(heading.split("]", 1)[0].lstrip("["))
        if not heading_key.startswith(wanted):
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        return text[start:end].strip()
    return None


def main() -> int:
    args = parse_args()
    changelog = Path(args.changelog)
    if not changelog.exists():
        print(f"error: changelog not found: {changelog}", file=sys.stderr)
        return 2

    notes = section_for_version(changelog.read_text(encoding="utf-8"), args.version)
    if notes is None:
        print(f"error: version section not found: {args.version}", file=sys.stderr)
        return 1

    print(notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
