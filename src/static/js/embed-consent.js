document.addEventListener("click", (e) => {
  const button = e.target.closest(".embed-consent button");
  if (!button) return;

  const embedConsent = button.closest(".embed-consent");
  if (!embedConsent) return;

  const template = embedConsent.querySelector("template");
  if (!template) return;

  const content = template.content.cloneNode(true);
  embedConsent.replaceWith(content);
});
