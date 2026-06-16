#!/usr/bin/env python3
"""Assert that a Keep a Changelog Unreleased section is empty."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail when CHANGELOG.md has content under ## [Unreleased].",
    )
    parser.add_argument(
        "--changelog",
        default="CHANGELOG.md",
        help="Path to the changelog file. Defaults to CHANGELOG.md.",
    )
    return parser.parse_args()


def unreleased_body(text: str) -> str | None:
    matches = list(HEADING_RE.finditer(text))
    for index, match in enumerate(matches):
        heading = match.group(1).strip().lower()
        if "unreleased" not in heading:
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

    body = unreleased_body(changelog.read_text(encoding="utf-8"))
    if body is None:
        print("error: no ## [Unreleased] section found", file=sys.stderr)
        return 2
    if body:
        print("error: Unreleased section is not empty", file=sys.stderr)
        print(body, file=sys.stderr)
        return 1

    print("Unreleased section is empty")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
