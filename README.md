# Proof Notes POC

A small, shareable documentation site for mathematical proofs. It uses a clean
book-like layout: navigation is on the left, the proof stays in the centre, and
an earlier definition or lemma can be opened in a closeable card on the right.
The reader does not lose their place in the proof.

## Run locally

Run these commands from this directory (`proof-docs`):

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
npm install
.venv/bin/mkdocs serve
```

Open <http://127.0.0.1:8000>. Stop the server with `Ctrl+C`.

`npm install` is needed once because the Python KaTeX extension uses the local
KaTeX command to turn maths into static HTML. If it reports that KaTeX is
missing, run `npm install katex` and start the server again.

## What a reader sees

- The left menu contains the chapter and its table of contents.
- A reference such as `Lemma 1.2` opens that lemma in the right-hand column.
- Clicking the same reference again closes its card. Different references can
  stay open together.
- When the reader scrolls past the reference that opened a card, that card
  closes. `Open full section` is the one deliberate link that takes the reader
  to the original text.
- On a narrow screen, cards become a closeable panel along the bottom, because
  there is not enough space for a useful right column.

## How it is put together

There is a clear boundary between the build and the small amount of browser
behaviour:

| Part | Job | Why it exists |
| --- | --- | --- |
| Markdown in `docs/` | The proof text, headings, and references | Authors can write normal, reviewable text. |
| Python hook in `plugins/proof_references.py` | Checks references and creates the complete hidden cards at build time | The browser never has to interpret proof Markdown or clone proof content. |
| CSS in `docs/stylesheets/proof-notes.css` | The book-like layout and responsive right-hand cards | Keeps presentation separate from content. |
| Small JS file in `docs/javascripts/reference-panel.js` | Opens, closes, and stacks cards | This interaction cannot be done reliably with HTML and CSS alone. |

Math is also rendered during the build, rather than after the page loads. That
keeps the page usable without a large client-side maths library and makes the
generated site easy to host anywhere.

## Authoring a local reference

Wrap a section that may be shown as a card in a `proof-ref` block. Then refer
to its ID where it is needed:

```md
::: proof-ref id="lemma-even-square"
## Lemma 1.2: Squaring preserves evenness
...
:::

By [[Lemma 1.2|lemma-even-square]], the claim follows.
```

Authors write no HTML. A typo or missing target stops the build instead of
silently creating a broken reference. This prototype supports references within
the current chapter. Cross-chapter previews can be added later with a
build-time index of all marked sections.

External citations remain ordinary Markdown links and footnotes. They should
take a reader to the original source rather than pretending that the source is
part of this document.

## Choices and trade-offs

### Chosen: MkDocs + a Python build hook + small JavaScript

This is the simplest option that keeps proof writing in Markdown while still
allowing interactive local references. Python owns validation and generated
content; JavaScript only changes the visibility of cards. The trade-off is that
there is a small JS file, because a closeable, stackable panel needs browser
state.

### Alternative: plain MkDocs with normal anchors

This would have no custom code and is excellent for a conventional textbook.
It was not chosen because clicking `Lemma 1.2` would move the reader away from
the proof they are currently following.

### Alternative: a React/MDX or Next.js site

This could provide richer search, animated panels, cross-chapter previews, and
more elaborate editing tools. It was not chosen for the prototype because it
adds a larger toolchain and makes simple proof writing harder than necessary.

### Alternative: all JavaScript in the browser

The browser could scan Markdown-like content and construct cards itself. It was
not chosen because it mixes authoring, proof parsing, and UI logic in one
place, makes broken references harder to catch, and risks a flash of unrendered
maths.

### Alternative: all Python with no JavaScript

Python can generate the page, but it cannot respond to a click in a static page
after it has been published. This works only if references are ordinary links
or if a server application is added. A server is unnecessary for this document
site.

## Verify a change

```sh
.venv/bin/python -m unittest discover -s tests -v
node --check docs/javascripts/reference-panel.js
.venv/bin/mkdocs build --strict
```

The generated static site is placed in `site/`. It can be uploaded to any
static host after a successful build.
