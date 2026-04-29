#!/usr/bin/env python3
"""Bump the jemdoc-cvx version across jemdoc, pyproject.toml, and package.json.

Single source of truth is `__version__` in the `jemdoc` script; this helper
keeps the other two files (pyproject.toml's project.version and package.json's
top-level version) in lockstep. Historical version references in www/*.jemdoc
documentation are intentionally not touched — those describe specific past
releases.

Usage:
    python3 scripts/bump_version.py X.Y.Z

The release workflow (.github/workflows/release.yml) verifies all three files
match the pushed tag, so a missed bump fails CI loudly.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def replace_once(path: Path, pattern: str, replacement: str, *, flags: int = 0) -> None:
    text = path.read_text()
    new, n = re.subn(pattern, replacement, text, count=1, flags=flags)
    if n == 0:
        sys.exit(f"error: no match for version pattern in {path}")
    path.write_text(new)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: bump_version.py X.Y.Z")
    new = sys.argv[1]
    if not VERSION_RE.match(new):
        sys.exit(f"error: invalid version {new!r}; expected X.Y.Z")

    repo = Path(__file__).resolve().parent.parent

    replace_once(
        repo / "jemdoc",
        r'^__version__ = "[^"]*"',
        f'__version__ = "{new}"',
        flags=re.MULTILINE,
    )
    replace_once(
        repo / "pyproject.toml",
        r'^version = "[^"]*"',
        f'version = "{new}"',
        flags=re.MULTILINE,
    )
    replace_once(
        repo / "package.json",
        r'"version": "[^"]*"',
        f'"version": "{new}"',
    )

    print(f"bumped to {new} in: jemdoc, pyproject.toml, package.json")
    print(
        f"next steps: uv lock; git commit -am 'Bump to {new}'; "
        f"git tag -a v{new} -m 'Release {new}'"
    )


if __name__ == "__main__":
    main()
