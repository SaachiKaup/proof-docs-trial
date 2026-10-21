# Proof Notes POC

A small MkDocs Material prototype for mathematical proofs with Tufte-inspired reference cards. Python builds proof-reference markup and static math; browser JavaScript only controls the reference-card UI.

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
node --check docs/javascripts/reference-panel.js
.venv/bin/mkdocs build --strict
```

## Authoring references

Wrap a previewable section in a Python-validated directive, then use its ID in an inline reference:

```md
::: proof-ref id="lemma-even-square"
## Lemma 1.2
...
:::

By [[Lemma 1.2|lemma-even-square]], the claim follows.
```

Authors write no HTML. The MkDocs hook generates the source section, reference buttons, and complete hidden cards during the build. This POC handles references within the active chapter; a later production version can add a build-time index for cross-chapter previews.
