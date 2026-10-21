(function () {
  "use strict";

  function close(card, restoreFocus) {
    if (!card) return;
    card.referenceCleanup?.();
    card.referenceCleanup = undefined;
    card.hidden = true;
    card.referenceTrigger?.setAttribute("aria-expanded", "false");
    if (restoreFocus) card.referenceTrigger?.focus();
  }

  function open(identifier, trigger) {
    const host = document.getElementById("proof-reference-cards");
    const card = host?.querySelector(`[data-reference-id="${identifier}"]`);
    if (!card) return;
    if (!card.hidden) {
      close(card, false);
      return;
    }

    card.hidden = false;
    card.referenceTrigger = trigger;
    trigger.setAttribute("aria-expanded", "true");

    // Do not move the card in the DOM when it opens: grid auto-placement can
    // otherwise put it below the article on a subsequent toggle. Assigning a
    // visual order still stacks separately opened cards by opening time.
    open.order = (open.order || 0) + 1;
    card.style.order = String(open.order);

    // Observe actual reader scrolling rather than the layout reflow caused by
    // opening a card. The latter made an opened card close unpredictably.
    const closeWhenTriggerLeavesViewport = () => {
      const bounds = trigger.getBoundingClientRect();
      if (bounds.bottom < 0 || bounds.top > window.innerHeight) close(card, false);
    };
    window.addEventListener("scroll", closeWhenTriggerLeavesViewport, { passive: true });
    card.referenceCleanup = () => {
      window.removeEventListener("scroll", closeWhenTriggerLeavesViewport);
    };
  }

  function initialise() {
    const article = document.querySelector(".md-content__inner");
    if (!article) return;
    const oldHost = document.getElementById("proof-reference-cards");
    oldHost?.querySelectorAll(".reference-card").forEach((card) => card.referenceCleanup?.());
    oldHost?.remove();

    // Keep the cards inside the content column.  Appending a fourth child to
    // Material's outer three-column grid makes CSS create a new row below the
    // page, which is why cards previously seemed to jump between top/bottom.
    const layout = document.querySelector(".md-content");
    const host = document.createElement("aside");
    host.id = "proof-reference-cards";
    host.setAttribute("aria-live", "polite");
    (layout || document.body).append(host);
    article.querySelectorAll(".reference-card").forEach((card) => host.append(card));
    document.querySelectorAll(".reference-trigger[data-reference-id]").forEach((trigger) => {
      trigger.setAttribute("aria-expanded", "false");
    });
  }

  document.addEventListener("click", (event) => {
    const closeButton = event.target.closest(".reference-card__close");
    if (closeButton) {
      close(closeButton.closest(".reference-card"), true);
      return;
    }

    const trigger = event.target.closest(".reference-trigger[data-reference-id]");
    if (trigger) {
      event.preventDefault();
      open(trigger.dataset.referenceId, trigger);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    const cards = document.querySelectorAll("#proof-reference-cards .reference-card:not([hidden])");
    if (cards.length) close(cards[cards.length - 1], true);
  });

  if (window.document$) window.document$.subscribe(initialise);
  else document.addEventListener("DOMContentLoaded", initialise);
}());
