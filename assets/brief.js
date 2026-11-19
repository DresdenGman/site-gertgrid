function initBrief(root) {
  const groups = [...root.querySelectorAll("[data-q]")];
  const checkButton = root.querySelector("[data-brief-check]");
  const downloadButton = root.querySelector("[data-brief-download]");
  const status = root.querySelector("[data-brief-status]");
  if (!checkButton || !downloadButton || !status || groups.length === 0) return;
  let checked = false;

  function selectedIndex(group) {
    const input = group.querySelector("input[type='radio']:checked");
    return input ? Number(input.value) : null;
  }

  function selectedText(group, index) {
    const input = group.querySelector(`input[type='radio'][value="${index}"]`);
    const label = input ? input.closest("label") : null;
    return label ? label.textContent.trim() : "";
  }

  checkButton.addEventListener("click", () => {
    const answers = groups.map(selectedIndex);
    if (answers.some((value) => value === null)) {
      status.textContent = "Answer each question before the receipt can be created.";
      downloadButton.disabled = true;
      checked = false;
      return;
    }
    groups.forEach((group, i) => {
      const feedback = group.querySelector("[data-q-feedback]");
      const correct = Number(group.dataset.correct);
      const right = answers[i] === correct;
      feedback.hidden = false;
      feedback.textContent = `${right ? "Correct." : "Not quite."} ${group.dataset.explain}`;
    });
    checked = true;
    status.textContent = "Checked on this device. You can download the receipt; it is not sent anywhere.";
    downloadButton.disabled = false;
  });

  groups.forEach((group) => {
    group.addEventListener("change", () => {
      if (!checked) return;
      checked = false;
      downloadButton.disabled = true;
      status.textContent = "Answers changed. Check them again before downloading the receipt.";
    });
  });

  downloadButton.addEventListener("click", () => {
    if (!checked) return;
    const receipt = {
      schema: "gert-self-check-v1",
      brief_version: "winter-load-brief-v1",
      source_url: "https://gertgrid.space/briefs/winter-load",
      generated_at: new Date().toISOString(),
      responses: groups.map((group, i) => {
        const index = selectedIndex(group);
        const legend = group.querySelector("legend");
        return {
          id: group.dataset.qid || `q${i + 1}`,
          prompt: legend ? legend.textContent.trim() : "",
          selected_index: index,
          selected: selectedText(group, index),
          correct: index === Number(group.dataset.correct),
        };
      }),
      evidence_status: "local_self_check_not_verified_participation",
    };
    const url = URL.createObjectURL(new Blob([JSON.stringify(receipt, null, 2)], { type: "application/json" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = "gert-winter-load-self-check.json";
    document.body.appendChild(link);
    try { link.click(); } finally { link.remove(); }
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
}

document.querySelectorAll("[data-brief]").forEach((root) => initBrief(root));
