from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import SimpleNamespace
import unittest

from mkdocs.exceptions import PluginError


ROOT = Path(__file__).parents[1]
CHAPTER = (ROOT / "docs/chapters/01-even-numbers.md").read_text()
SCRIPT = (ROOT / "docs/javascripts/reference-panel.js").read_text()
CONFIG = (ROOT / "mkdocs.yml").read_text()
PLUGIN_PATH = ROOT / "plugins/proof_references.py"
SPEC = spec_from_file_location("proof_references", PLUGIN_PATH)
proof_references = module_from_spec(SPEC)
SPEC.loader.exec_module(proof_references)
PAGE = SimpleNamespace(file=SimpleNamespace(src_uri="sample.md"))


class ProofReferenceTests(unittest.TestCase):
    def test_sample_uses_directives_not_author_html(self):
        self.assertIn('::: proof-ref id="definition-even"', CHAPTER)
        self.assertIn('[[Lemma 1.2|lemma-even-square]]', CHAPTER)
        self.assertNotIn('<section', CHAPTER)
        self.assertNotIn('<button', CHAPTER)

    def test_python_hook_generates_sections_and_buttons(self):
        rendered = proof_references.on_page_markdown(CHAPTER, page=PAGE, config={}, files=[])
        self.assertIn('class="reference-source"', rendered)
        self.assertIn('class="reference-trigger"', rendered)
        self.assertIn('data-reference-id="lemma-even-square"', rendered)

    def test_missing_reference_is_a_build_error(self):
        with self.assertRaises(PluginError):
            proof_references.on_page_markdown('[[Missing lemma|not-defined]]', page=PAGE, config={}, files=[])

    def test_static_ui_module_does_not_build_or_clone_proof_content(self):
        self.assertNotIn("cloneNode", SCRIPT)
        self.assertNotIn("renderMath", SCRIPT)
        self.assertNotIn("innerHTML", SCRIPT)
        self.assertNotIn("IntersectionObserver", SCRIPT)
        self.assertNotIn("card.hidden = false;\n    host.append(card)", SCRIPT)
        self.assertIn('document.addEventListener("click"', SCRIPT)
        self.assertNotIn("addEventListener(\"click\", () => open", SCRIPT)
        self.assertIn("closeWhenTriggerLeavesViewport", SCRIPT)

    def test_build_hook_emits_complete_card_without_a_subtitle(self):
        page_html = '''<article class="md-content__inner">
        <section class="reference-source" id="lemma-even-square"><h2 id="lemma">Lemma 1.2</h2><p>Proof text.</p></section>
        </article>'''
        rendered = proof_references.on_post_page(page_html, page=PAGE, config={})
        self.assertIn('data-reference-id="lemma-even-square"', rendered)
        self.assertIn('href="#lemma-even-square">Open full section</a>', rendered)
        self.assertNotIn("Earlier section", rendered)

    def test_static_katex_and_left_toc_are_configured(self):
        self.assertIn("markdown_katex", CONFIG)
        self.assertIn("toc.integrate", CONFIG)
        self.assertNotIn("katex.min.js", CONFIG)


if __name__ == "__main__":
    unittest.main()
