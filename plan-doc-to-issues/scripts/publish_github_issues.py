#!/usr/bin/env python3
"""Delegate plan-doc-to-issues publishing to the sibling to-issues helper."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


USAGE = """usage: publish_github_issues.py <issues.json> --repo OWNER/REPO [--dry-run] [--output created-issues.json]

Delegates to ../to-issues/scripts/publish_github_issues.py so this composed
skill has a local, portable script reference while preserving the canonical
publisher implementation.
"""


def main() -> None:
    if any(arg in {"-h", "--help"} for arg in sys.argv[1:]):
        print(USAGE)
        return

    target = Path(__file__).resolve().parents[2] / "to-issues" / "scripts" / "publish_github_issues.py"
    if not target.is_file():
        print(f"error: sibling publisher not found: {target}", file=sys.stderr)
        raise SystemExit(1)

    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()
