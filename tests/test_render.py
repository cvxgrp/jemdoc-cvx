"""Regression test: rendering each .jemdoc input must match the committed fixture.

The fixtures in ``tests/fixtures/`` were captured from the pre-modernization binary.
Phase 1 (Python cleanup) must not change output. Later phases that intentionally
change HTML (Phase 3 doctype/void elements, Phase 4 semantic layout, Phase 5 KaTeX)
will regenerate fixtures in the same PR — review the diff manually.

The "Page generated <timestamp>" line is normalized before comparison.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
JEMDOC = REPO / "jemdoc"
FIXTURES = REPO / "tests" / "fixtures"

EXAMPLE_INPUTS = ["link", "mathjax", "underscore"]
WWW_INPUTS = [
    "index",
    "cheatsheet",
    "contact",
    "download",
    "revision",
    "using",
    "menu",
    "stuff",
    "extra",
    "example",
    "modelines",
    "htmlchanges",
    "latex",
    "tables",
]

TIMESTAMP_RE = re.compile(r"Page generated \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]+,")


def _normalize(html: str) -> str:
    return TIMESTAMP_RE.sub("Page generated <NORMALIZED>,", html)


def _render(source_dir: Path, conf_name: str, name: str, out_dir: Path) -> str:
    out_path = out_dir / f"{name}.html"
    subprocess.run(
        [str(JEMDOC), "-o", str(out_path), "-c", conf_name, f"{name}.jemdoc"],
        cwd=source_dir,
        check=True,
        capture_output=True,
    )
    return out_path.read_text(encoding="utf-8")


@pytest.mark.parametrize("name", EXAMPLE_INPUTS)
def test_example_fixture(name: str, tmp_path: Path) -> None:
    rendered = _render(REPO / "example", "mysite.conf", name, tmp_path)
    expected = (FIXTURES / "example" / f"{name}.html").read_text(encoding="utf-8")
    assert _normalize(rendered) == _normalize(expected)


@pytest.mark.parametrize("name", WWW_INPUTS)
def test_www_fixture(name: str, tmp_path: Path) -> None:
    rendered = _render(REPO / "www", "jemdoc.conf", name, tmp_path)
    expected = (FIXTURES / "www" / f"{name}.html").read_text(encoding="utf-8")
    assert _normalize(rendered) == _normalize(expected)
