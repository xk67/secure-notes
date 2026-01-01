document.querySelectorAll(".embed-consent").forEach((el) => {
  const button = el.querySelector("button");
  const template = el.querySelector("template");

  if (!button || !template) return;

  button.addEventListener("click", () => {
    const content = template.content.cloneNode(true);
    el.replaceWith(content);
  });
});
