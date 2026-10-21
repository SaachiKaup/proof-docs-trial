"""Build-time authoring support for local proof-reference cards."""

from __future__ import annotations

from copy import deepcopy
from html import escape
import re

from bs4 import BeautifulSoup
from mkdocs.exceptions import PluginError


BLOCK = re.compile(
    r'^:::\s*proof-ref\s+id="(?P<id>[a-z][a-z0-9-]*)"\s*\n'
    r'(?P<content>.*?)^:::\s*$',
    re.MULTILINE | re.DOTALL,
)
REFERENCE = re.compile(r"\[\[(?P<label>[^\]|]+)\|(?P<id>[a-z][a-z0-9-]*)\]\]")
INLINE_MATH = re.compile(r"(?<!\\$)\$(?!\$)(.+?)(?<!\\)\$(?!\$)")
DISPLAY_MATH = re.compile(r"^\$\$\s*\n?(.*?)\n?\$\$$", re.MULTILINE | re.DOTALL)


def _math_for_static_katex(markdown: str) -> str:
    markdown = DISPLAY_MATH.sub(lambda match: f"```math\n{match.group(1).strip()}\n```", markdown)
    return INLINE_MATH.sub(lambda match: f"$`{match.group(1)}`$", markdown)


def on_page_markdown(markdown, *, page, config, files):
    identifiers = {match.group("id") for match in BLOCK.finditer(markdown)}

    def section(match):
        identifier = match.group("id")
        return (
            f'<section class="reference-source" id="{identifier}" markdown="1">\n\n'
            f'{match.group("content").strip()}\n\n</section>'
        )

    markdown = BLOCK.sub(section, markdown)

    def trigger(match):
        identifier = match.group("id")
        if identifier not in identifiers:
            raise PluginError(f"{page.file.src_uri}: reference '{identifier}' has no proof-ref block on this page")
        return (
            '<button class="reference-trigger" type="button" '
            f'data-reference-id="{identifier}">{escape(match.group("label"))}</button>'
        )

    return _math_for_static_katex(REFERENCE.sub(trigger, markdown))


def on_post_page(output, *, page, config):
    soup = BeautifulSoup(output, "html.parser")
    article = soup.select_one(".md-content__inner")
    if article is None:
        return output

    for source in article.select("section.reference-source"):
        identifier = source.get("id")
        if not identifier:
            continue
        heading = source.select_one("h1, h2, h3, h4, h5, h6")
        if heading:
            for permalink in heading.select(".headerlink"):
                permalink.decompose()
        title = heading.get_text(" ", strip=True) if heading else identifier
        card = soup.new_tag("aside")
        card["class"] = ["reference-card"]
        card["data-reference-id"] = identifier
        card["hidden"] = ""
        card["aria-label"] = f"Reference: {title}"
        header = soup.new_tag("header")
        header["class"] = ["reference-card__header"]
        close = soup.new_tag("button", type="button")
        close["class"] = ["reference-card__close"]
        close["aria-label"] = f"Close {title}"
        close.string = "×"
        header.append(close)
        card.append(header)

        content = deepcopy(source)
        content.attrs.pop("id", None)
        content["class"] = ["reference-card__content"]
        for element in content.select("[id]"):
            element.attrs.pop("id", None)
        card.append(content)

        full_section = soup.new_tag("a", href=f"#{identifier}")
        full_section["class"] = ["reference-card__source"]
        full_section.string = "Open full section"
        card.append(full_section)
        article.append(card)

    return str(soup)
