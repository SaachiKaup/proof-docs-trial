from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
CHAPTER = (ROOT / "docs/chapters/01-even-numbers.md").read_text()
SCRIPT = (ROOT / "docs/javascripts/proof-notes.js").read_text()
CONFIG = (ROOT / "mkdocs.yml").read_text()


class PrototypeContractTests(unittest.TestCase):
    def test_sample_has_referenceable_sections(self):
        self.assertIn('id="definition-even"', CHAPTER)
        self.assertIn('id="lemma-even-square"', CHAPTER)
        self.assertIn('id="theorem-even-sum"', CHAPTER)

    def test_theorem_references_earlier_sections(self):
        self.assertIn('data-reference="definition-even"', CHAPTER)
        self.assertIn('data-reference="lemma-even-square"', CHAPTER)

    def test_external_citation_is_an_absolute_url(self):
        self.assertIn("https://openstax.org/", CHAPTER)

    def test_toc_is_integrated_into_left_navigation(self):
        self.assertIn("toc.integrate", CONFIG)

    def test_interaction_prevents_internal_navigation_and_supports_cards(self):
        self.assertIn("bindReferenceTriggers", SCRIPT)
        self.assertIn(".md-main__inner", SCRIPT)
        self.assertIn("host.append(card)", SCRIPT)
        self.assertIn('event.key !== "Escape"', SCRIPT)
        self.assertIn("IntersectionObserver", SCRIPT)
        self.assertIn("existing.closeReference(false)", SCRIPT)
        self.assertIn('source.textContent = "Open full section"', SCRIPT)


if __name__ == "__main__":
    unittest.main()
