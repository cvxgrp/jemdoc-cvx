jemdoc-cvx
==========
A Claude-coded modernization of *jemdoc* (Jacob Mattingley's static-site generator) and
*jemdoc+MathJax* (Wonseok Shin's MathJax-aware fork). This fork keeps the
same `.jemdoc` input format and the iconic look of generated pages, but
modernizes the tool itself: HTML5 output, CSS3, Python 3.11+, and **server-side
equation rendering with [KaTeX](https://katex.org/)**.

`.jemdoc` files that worked with prior jemdoc versions continue to work here.

Documentation
-------------
Full user guide, syntax reference, and worked examples:
**<https://cvxgrp.org/jemdoc-cvx/>**.

This README covers just enough to get a typical academic site up and running.
For everything else — markup syntax, the menu file, conf overrides, theme
switching, equations — see the documentation site.

Usage
-----

### Download

Grab the latest release from
**<https://github.com/cvxgrp/jemdoc-cvx/releases/latest>** — pick the
`.tar.gz` or `.zip`. The bundle contains the `jemdoc` script, the default
theme (`jemdoc-cvx.css`) plus its fonts, the legacy theme variants
(`jemdoc.css`, `jacob.css`, etc.), and a minimal `package.json` for the
optional KaTeX install. No `git clone` required for everyday use.

    tar -xzf jemdoc-cvx-1.0.0.tar.gz
    cd jemdoc-cvx-1.0.0
    ./jemdoc --version

If you'd rather track the source, `git clone https://github.com/cvxgrp/jemdoc-cvx.git`
also works.

### Building a typical academic website

A canonical academic page (homepage, publications list, teaching, CV) is just a
handful of `.jemdoc` source files alongside a `MENU` file and a stylesheet.
Recommended layout:

    mysite/
        MENU                  # sidebar menu, listed once
        index.jemdoc          # one .jemdoc per page
        publications.jemdoc
        teaching.jemdoc
        cv.jemdoc
        jemdoc-cvx.css        # the default theme stylesheet
        fonts/                # the woff2 files that go with the theme
            source-serif-4-latin-wght-normal.woff2
            source-serif-4-latin-wght-italic.woff2
            jetbrains-mono-latin-wght-normal.woff2
        papers/               # PDFs etc. served as-is
            mypaper.pdf

To bootstrap a new site, copy the theme assets out of the unpacked bundle (or
the cloned repo) and start writing pages:

    cp /path/to/jemdoc-cvx-1.0.0/css/jemdoc-cvx.css .
    cp -r /path/to/jemdoc-cvx-1.0.0/css/fonts .
    # write your .jemdoc sources, plus a MENU file, then build:
    /path/to/jemdoc-cvx-1.0.0/jemdoc *.jemdoc

`jemdoc` writes an `index.html` next to each `index.jemdoc`, etc. To send the
output to a separate directory:

    mkdir build
    ../jemdoc-cvx/jemdoc -o build/ *.jemdoc
    cp jemdoc-cvx.css build/
    cp -r fonts build/

Then point your webserver (Apache/nginx/whatever your faculty department runs)
at the directory containing the rendered `.html` files. The output is plain
static HTML — no server-side runtime is needed to serve it.

### Server-side equation rendering (KaTeX)

If your pages contain LaTeX equations (`$inline$` or `\(display\)` blocks),
install the pinned KaTeX CLI **once on the machine where you build the site**
(your laptop, or whichever machine runs `jemdoc`). It is *not* needed on the
machine that serves the resulting HTML:

    cd /path/to/jemdoc-cvx-1.0.0  # the unpacked release bundle (or clone)
    npm install                   # one-time, installs node_modules/.bin/katex

`jemdoc` automatically uses the local `katex` binary at build time and embeds
the rendered HTML directly in each page. Cached output goes in `katexcache/`
next to your sources, so subsequent builds are fast.

If you skip this step or `katex` isn't found on `PATH`, jemdoc-cvx falls back
to emitting raw `\(...\)` / `\[...\]` markers, which a client-side MathJax
script can render in the browser if you load one via a conf override. See the
[latex equations page](https://cvxgrp.org/jemdoc-cvx/latex.html) for details.

Requirements
------------
- **Python 3.11+** (standard library only; nothing to `pip install` for
  everyday use).
- **Node.js**, only if you want server-side equation rendering. Run
  `npm install` once in this repo to install the pinned KaTeX CLI.
- **[uv](https://docs.astral.sh/uv/)**, only if you want to contribute (run
  the test suite or the linter).

Development
-----------
Dev tooling (pytest, ruff) is managed by uv. From a fresh clone:

    uv sync                # creates .venv/ and installs the dev dependency group
    npm install            # installs the pinned KaTeX CLI

Then:

    make test              # uv run pytest tests/
    make lint              # uv run ruff check .
    make docs              # builds the project's own documentation site to www/html/

The `tests/fixtures/` directory holds reference HTML for every page in
`example/` and `www/`; tests assert byte-equality (with the timestamp footer
normalized) against those fixtures. Update them intentionally when you change
emitted HTML.

### Cutting a release

Version is canonical in `jemdoc` (the `__version__` constant near the top);
`pyproject.toml` and `package.json` mirror it. To bump them all in lockstep:

    make bump-version VERSION=1.1.0
    git commit -am "Bump to 1.1.0"
    git tag -a v1.1.0 -m "Release 1.1.0"
    git push origin main v1.1.0

Pushing the `vX.Y.Z` tag triggers `.github/workflows/release.yml`, which
verifies the tag matches all three files (failing CI if they've drifted),
builds the `.tar.gz` / `.zip` bundle, and creates a GitHub Release with
auto-generated notes.

License
-------
GPL-3.0-or-later. See `LICENSE` for the original jemdoc copyright; the
KaTeX/HTML5 modernization changes are likewise GPL-3.0-or-later.
