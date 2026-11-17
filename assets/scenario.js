document.querySelectorAll("[data-run]").forEach((button) => {
  button.addEventListener("click", () => {
    const panel = document.getElementById(button.getAttribute("aria-controls"));
    if (!panel) return;
    panel.hidden = false;
    panel.focus();
  });
});
