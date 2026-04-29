jemdoc-cvx
==========
A Claude-coded modernization of *jemdoc* (Jacob Mattingley's static-site generator) and
*jemdoc+MathJax* (Wonseok Shin's MathJax-aware fork). This fork keeps the
same `.jemdoc` input format and the iconic look of generated pages, but
modernizes the tool itself: HTML5 output, CSS3, Python 3.11+, and **server-side
equation rendering with [KaTeX](https://katex.org/)**.

See <http://jemdoc.jaboc.net/> for the original jemdoc usage. `.jemdoc` files
that worked with prior jemdoc versions continue to work here.

What's new in jemdoc-cvx
------------------------
- HTML5 output (no XHTML 1.1, no `xmlns`, no XML self-closing on void elements).
- Semantic layout: the page menu/content uses `<nav>`/`<main>` inside a CSS-grid
  `<div id="tlayout">` instead of a layout `<table>`.
- Inline `+monospace+` emits `<code>` instead of the obsolete `<tt>`.
- **Server-side math via KaTeX**: equations in `$...$` (inline) and `\(...\)`
  block (display) are rendered to HTML at build time, with no client-side
  script required to view the page.
- Python 3.11+ only. Drops Python 2 compatibility scaffolding, `latexmath2png.py`,
  and the dead `geneq` PNG-via-LaTeX equation path.
- Repo plumbing: `pyproject.toml`, regression-fixture tests in `tests/`, and
  a portable Makefile that no longer hard-codes the maintainer's home directory.

KaTeX vs MathJax
----------------
The previous fork (jemdoc+MathJax) emitted raw `\(...\)` placeholders that a
client-side MathJax script rendered in the browser. This fork instead uses
[KaTeX](https://katex.org/), invoked at build time via its npm CLI, and embeds
the rendered HTML directly in the page.

KaTeX supports a large subset of LaTeX but not everything MathJax does. In
particular, equation cross-referencing (`\label{...}` / `\eqref{...}`) and
some AMSmath constructs are not supported and will render with a small red
error indicator. If your site needs full MathJax behaviour, drop the rendered
output by adding `# jemdoc: noeqs` to the source and override `[bodystart]`
in your conf to load MathJax client-side, as the previous fork did.

Requirements
------------
- Python 3.11 or newer.
- For server-side equation rendering: Node.js and the
  [`katex`](https://www.npmjs.com/package/katex) CLI. Install locally with
  `npm install` from this repo (uses the pinned version in `package.json`).
  If `katex` isn't on `PATH`, jemdoc-cvx falls back to emitting raw
  `\(...\)` / `\[...\]` so you can still ship pages that get rendered by a
  conf-loaded client-side script.
- For contributing (running tests / lint): [uv](https://docs.astral.sh/uv/).
  `jemdoc` itself uses only the Python stdlib, so end users who only run the
  tool need nothing more than a Python 3.11 interpreter.

Development setup
-----------------
Dev tooling (pytest, ruff) is managed by uv. From a fresh clone:

    uv sync           # creates .venv/ and installs the dev dependency group
    npm install       # installs the pinned KaTeX CLI

Then `make test` runs the regression harness via `uv run pytest`, and
`make lint` runs ruff. The `.venv/` directory is gitignored; `uv.lock` is
committed so installs are reproducible.

Usage
-----
Render a single source file:

    ./jemdoc index.jemdoc

With a config file:

    ./jemdoc -c mysite.conf foo.jemdoc

The example site is in `example/`; build it with:

    cd example && ../jemdoc -c mysite.conf *.jemdoc

The project's own documentation is in `www/`; build with `make docs`.

Tests
-----
`make test` runs the regression harness in `tests/`. Each `.jemdoc` source is
re-rendered and byte-compared against the committed fixture (with the
"page generated" timestamp normalised). Update fixtures intentionally when
you change emitted HTML.

License
-------
GPL-3.0-or-later. See `LICENSE` for the original jemdoc copyright; the
KaTeX modernization changes are likewise GPL-3.0-or-later.
