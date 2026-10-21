# Proof Notes POC

A small MkDocs Material prototype for mathematical proofs with Tufte-inspired reference cards.

## Run locally

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

Open the chapter, then click the buttons for Definition 1.1 and Lemma 1.2 in Theorem 1.3. Each opens a closeable card without moving the reader away from the proof; it closes automatically when its button scrolls out of the reading area.

## Verify

```sh
python3 -m unittest discover -s tests -v
node --check docs/javascripts/proof-notes.js
.venv/bin/mkdocs build --strict
```

Previewable material is fenced in Markdown using a `<section class="reference-source" ... markdown="1">` wrapper, and references are explicit `<button class="reference-trigger" data-reference="...">` controls. This POC handles references within the active chapter. A later production version can add a build-time reference index for cross-chapter previews.
