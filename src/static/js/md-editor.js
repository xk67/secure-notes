document.addEventListener("DOMContentLoaded", function () {
  const buttonWrite = document.getElementById("button-write");
  const buttonPreview = document.getElementById("button-preview");
  const textarea = document.querySelector("textarea");
  const previewDiv = document.getElementById("preview-content");

  buttonWrite.addEventListener("click", function () {
    textarea.style.display = "block";
    previewDiv.style.display = "none";
  });

  buttonPreview.addEventListener("click", async function () {
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
    } catch (error) {
      console.error("Preview failed:", error);
    }
  });
});

function getCSRFToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
}
