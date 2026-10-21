(function () {
  "use strict";

  let cardCount = 0;

  function findSection(target) {
    const source = document.getElementById(target);
    if (!source || !source.classList.contains("reference-source")) return null;
    const section = source.cloneNode(true);
    section.removeAttribute("id");
    section.classList.remove("reference-source");
    section.classList.add("reference-card__content");
    return section;
  }

  function makeCard(target, trigger) {
    const host = document.getElementById("proof-reference-cards");
    const existing = Array.from(host.querySelectorAll(".reference-card"))
      .find((card) => card.dataset.referenceTarget === target);
    if (existing) {
      existing.closeReference(false);
      return;
    }

    const content = findSection(target);
    if (!content) return;
    const title = document.getElementById(target).dataset.referenceTitle;
    const card = document.createElement("aside");
    const cardId = `reference-card-${++cardCount}`;
    card.className = "reference-card";
    card.id = cardId;
    card.dataset.referenceTarget = target;
    card.setAttribute("role", "dialog");
    card.setAttribute("aria-label", `Reference: ${title}`);
    card.innerHTML = `<header class="reference-card__header"><span>Earlier section</span><button class="reference-card__close" type="button" aria-label="Close ${title}">×</button></header>`;
    card.append(content);
    const source = document.createElement("a");
    source.className = "reference-card__source";
    source.href = `#${target}`;
    source.textContent = "Open full section";
    card.append(source);

    const close = (restoreFocus) => {
      if (card.referenceObserver) card.referenceObserver.disconnect();
      card.remove();
      trigger.setAttribute("aria-expanded", "false");
      if (restoreFocus) trigger.focus();
    };
    card.closeReference = close;
    card.querySelector(".reference-card__close").addEventListener("click", () => close(true));
    host.append(card);
    bindReferenceTriggers(card);
    trigger.setAttribute("aria-expanded", "true");
    trigger.setAttribute("aria-controls", cardId);
    card.referenceObserver = new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting) close(false);
    }, { rootMargin: "-12% 0px -30% 0px" });
    card.referenceObserver.observe(trigger);
    card.querySelector(".reference-card__close").focus();
  }

  function bindReferenceTriggers(root) {
    root.querySelectorAll(".reference-trigger[data-reference]").forEach((trigger) => {
      const target = trigger.dataset.reference;
      if (!target || !document.getElementById(target) || trigger.dataset.referenceBound) return;
      trigger.dataset.referenceBound = "true";
      trigger.setAttribute("aria-expanded", "false");
      trigger.addEventListener("click", () => makeCard(target, trigger));
    });
  }

  function renderMath(root) {
    if (!window.renderMathInElement) return;
    window.renderMathInElement(root, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true },
        { left: "$", right: "$", display: false }
      ],
      throwOnError: false
    });
  }

  function initialise() {
    const article = document.querySelector(".md-content__inner");
    if (!article) return;
    if (!document.getElementById("proof-reference-cards")) {
      const host = document.createElement("div");
      host.id = "proof-reference-cards";
      host.setAttribute("aria-live", "polite");
      const layout = document.querySelector(".md-main__inner");
      (layout || document.body).append(host);
    }
    renderMath(article);
    bindReferenceTriggers(article);
  }

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    const cards = document.querySelectorAll(".reference-card");
    const last = cards[cards.length - 1];
    if (last) last.querySelector(".reference-card__close").click();
  });

  document.addEventListener("DOMContentLoaded", initialise);
  if (window.document$) window.document$.subscribe(initialise);
}());
