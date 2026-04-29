jemdoc-cvx
==========
A Claude-coded modernization of *jemdoc* (Jacob Mattingley's static-site generator) and
*jemdoc+MathJax* (Wonseok Shin's MathJax-aware fork). This fork keeps the
same `.jemdoc` input format and the iconic look of generated pages, but
modernizes the tool itself: HTML5 output, CSS3, Python 3.11+, and **server-side
equation rendering with [KaTeX](https://katex.org/)**.

`.jemdoc` files that worked with prior jemdoc versions continue to work here.
The original usage guide at jemdoc.jaboc.net is no longer reachable, so this
README is self-contained: read on for everything needed to build a site.

Usage
-----

### Install

The whole tool is a single executable Python script. From a clone of this
repo:

    git clone https://github.com/cvxgrp/cvxdoc.git
    cd cvxdoc
    sudo install ./jemdoc /usr/local/bin/jemdoc   # optional, puts it on $PATH

You can also just invoke `./jemdoc` directly from the clone, or copy it into
your project. It depends only on the Python 3.11+ standard library; no `pip
install` is needed for everyday use.

For server-side equation rendering, install the pinned KaTeX CLI from this
repo (one-time):

    npm install

If you skip this, math will fall back to client-side rendering — see
[KaTeX vs MathJax](#katex-vs-mathjax) below.

### A one-page site

Make a working directory, copy a stylesheet next to it, and write a source
file:

    mkdir mysite && cd mysite
    cp /path/to/cvxdoc/css/jemdoc.css .
    cat > index.jemdoc <<'EOF'
    = My first jemdoc page

    Welcome. This is a paragraph of text. Here is *bold*, /italic/,
    +monospace+ and a [https://example.com link].

    == A subsection
    - bullet one
    - bullet two
        -- nested bullet

    A bit of math: $f(x) = x^2 + 2x + 1$.
    EOF

Then render it:

    jemdoc index.jemdoc

That produces `index.html` next to the source. Open it in a browser; the
stylesheet `jemdoc.css` in the same directory is what makes it look like
jemdoc. (Edit the source, re-run `jemdoc index.jemdoc`, refresh the browser
— that's the whole iteration loop.)

If you want the output somewhere else:

    jemdoc -o html/index.html index.jemdoc      # explicit output path
    jemdoc -o html/ index.jemdoc                # output dir; same basename

### Markup essentials

Headings start a line with `=`. More `=`s mean deeper nesting:

    = Page title (h1)
    == Section (h2)
    === Subsection (h3)

Paragraphs are separated by blank lines. Inline formatting: `*bold*`,
`/italic/`, `_underline_`, `+monospace+`. Smart quotes, en/em dashes, and
ellipses are auto-substituted: `--` → en-dash, `---` → em-dash, `...` →
ellipsis, `` `quoted' `` and `"quoted"` become typographic quotes.

Lists:

    - bullet one
    - bullet two
        -- nested bullet

    . numbered one
    . numbered two

    : {term} definition
    : {jemdoc} light markup

Links: `[url label]` — if the label is omitted, the URL itself is used.
Internal links: `[other.html See also]`. Email: `[user@example.com Email me]`
auto-becomes a `mailto:` link.

Code/info blocks are fenced with `~~~`:

    ~~~
    {Optional title}{python}
    def hello(name):
        print(f"Hello, {name}!")
    ~~~

The first `{...}` is an optional title; the second is a syntax-highlighter
language hint (`python`, `c`, `sh`, `matlab`, etc.). Omit both for a plain
info-block:

    ~~~
    A boxed information block. Ordinary jemdoc markup applies inside.
    ~~~

Equations: `$x^2$` for inline, and a paragraph that begins with `\(` and
ends with `\)` becomes a centred display equation:

    Inline: $a^2 + b^2 = c^2$.

    \(
    \int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2}
    \)

Raw HTML: `{{<span class="foo">x</span>}}` inserts inline HTML untouched.
For larger blocks, use a raw fenced block:

    ~~~
    {}{raw}
    <div>any html here is copied verbatim</div>
    ~~~

Comments: lines starting with `#` are comments (except modeline directives
like `# jemdoc: menu{...}`).

For the full reference, see `www/cheatsheet.jemdoc` (or its rendered form,
`make docs && open www/html/cheatsheet.html`).

### A multi-page site with a menu

A typical jemdoc site lives in one directory:

    mysite/
        jemdoc.css         # stylesheet
        MENU               # sidebar definition
        index.jemdoc       # one .jemdoc per page
        about.jemdoc
        contact.jemdoc

Write `MENU` with categories (no leading whitespace) and items (indented,
with the link in `[brackets]`):

    My site
        home          [index.html]
        about         [about.html]
        contact       [contact.html]

    elsewhere
        github        [https://github.com/me]

Then add a modeline as the **first line** of each `.jemdoc` source:

    # jemdoc: menu{MENU}{index.html}
    = Home

    Welcome to my site.

The first arg `{MENU}` is the menu file; the second is *this page's* output
filename — jemdoc uses it to highlight the current entry in the sidebar.
Modelines can chain options with commas:

    # jemdoc: menu{MENU}{about.html}, nofooter, showsource

Useful modeline flags:

- `nofooter` — suppress the "page generated …" footer
- `nodate` / `notime` — keep the footer but drop the timestamp
- `showsource` — add a "(source)" link to the footer pointing at the
  `.jemdoc` source
- `noeqs` — disable equation processing for this page
- `addcss{extra.css}` — link an extra stylesheet (in addition to `jemdoc.css`)
- `nodefaultcss` — don't link `jemdoc.css`
- `analytics{UA-XXXXXX-X}` — emit a Google Analytics snippet
- `title{Window title}` — override the `<title>` tag (defaults to the page's
  H1)

Build all pages at once:

    jemdoc *.jemdoc

…or build into a separate output directory:

    mkdir -p html
    jemdoc -o html/ *.jemdoc

### A simple Makefile

Drop this `Makefile` next to your sources for an iterative workflow:

    DOCS = index about contact
    HTML = $(addprefix html/, $(addsuffix .html, $(DOCS)))

    JEMDOC ?= jemdoc

    .PHONY: docs clean
    docs: $(HTML)

    html/%.html: %.jemdoc MENU | html
        $(JEMDOC) -o $@ $<

    html: ; mkdir -p html

    clean: ; rm -f html/*.html

`make` rebuilds only the pages whose source changed. `make clean` wipes the
output.

### Custom CSS

The repo ships several themes in `css/`: `jemdoc.css` (default), plus
`white.css`, `green.css`, `jacob.css`, `exp.css`, `prob.css`, `page.css`,
`nolines.css`. Copy whichever one(s) you want next to your output html and
either rely on the default `<link rel="stylesheet" href="jemdoc.css">`, or
add an extra stylesheet via the modeline:

    # jemdoc: menu{MENU}{index.html}, addcss{green}

`addcss{green}` resolves to `<link rel="stylesheet" href="green.css">`. You
can also write your own CSS from scratch — jemdoc's HTML5 output uses stable
selectors (`#tlayout`, `#layout-menu`, `#layout-content`, `.codeblock`,
`.infoblock`, `.imgtable`, `.eqwl`, `code`, `pre`).

### Conf overrides (advanced)

For everything beyond modelines — changing the `<head>`, adding analytics
scripts, embedding extra HTML around the layout — provide a *conf file*
that overrides one or more named template blocks. Print the defaults:

    jemdoc --show-config

Pick a block (e.g. `[bodystart]`), copy it into a `mysite.conf`, edit, then:

    jemdoc -c mysite.conf *.jemdoc

The repo's own `www/jemdoc.conf` and `example/mysite.conf` are short worked
examples.

### Equations

Inline math is `$x^2$`; a paragraph starting with `\(` and ending with `\)`
is a centred display equation. Both are rendered to HTML at build time by
the `katex` CLI and embedded inline; the page does not need any client-side
JavaScript. Output is cached by content hash in `katexcache/` next to the
source so repeat builds are fast.

If `katex` isn't installed, equation markers pass through unchanged
(`\(...\)`/`\[...\]`) so a conf-loaded MathJax script can still render them
in the browser.

### Reference example

The full project documentation in `www/` is itself a jemdoc site —
`www/index.jemdoc`, `www/cheatsheet.jemdoc`, `www/menu.jemdoc`, etc., built
with `www/MENU`, `www/jemdoc.conf`, and `www/Makefile`. Build it with:

    make docs

…and open `www/html/index.html` to see a fully realised multi-page site
with menu, code blocks, equations, and tables. The `example/` directory is
a smaller demo of just the math-specific syntax.

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
