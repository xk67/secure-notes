document.addEventListener("DOMContentLoaded", function () {
  const buttonWrite = document.getElementById("button-write");
  const buttonPreview = document.getElementById("button-preview");
  const textarea = document.getElementById("md-textarea");
  const previewDiv = document.getElementById("preview-content");

  buttonWrite.addEventListener("click", function () {
    if (buttonWrite.classList.contains("active")) return;

    textarea.style.display = "block";
    previewDiv.style.display = "none";

    buttonWrite.classList.add("active");
    buttonPreview.classList.remove("active");
  });

  buttonPreview.addEventListener("click", async function () {
    if (buttonPreview.classList.contains("active")) return;

    const markdown = textarea.value;

    try {
      const response = await fetch("/note/preview", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          markdown: markdown,
          csrfmiddlewaretoken: getCSRFToken(),
        }),
      });

      const html = await response.text();
      previewDiv.innerHTML = html;

      textarea.style.display = "none";
      previewDiv.style.display = "block";

      buttonPreview.classList.add("active");
      buttonWrite.classList.remove("active");
    } catch (error) {
      console.error("Preview failed:", error);
    }
  });
});

function getCSRFToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
}
