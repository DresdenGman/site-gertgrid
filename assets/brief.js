const QUESTIONS = [
  {
    id: "interpretation",
    prompt: "The recorded load falls. What can this curve alone establish?",
    options: [
      "The grid became safer.",
      "Electricity demand disappeared.",
      "Recorded load fell; unmet demand and reliability remain unresolved.",
    ],
  },
  {
    id: "gap",
    prompt: "In a separate hypothetical one-hour example, load is 65,000 MW and assumed capacity is 60,000 MW. What is the arithmetic gap energy?",
    options: [
      "5,000 MWh, under those assumptions.",
      "5,000 MW of proven outage savings.",
      "65,000 MWh of expected unserved energy.",
    ],
  },
];

function initBrief(root) {
  const groups = [...root.querySelectorAll("[data-q]")];
  const checkButton = root.querySelector("[data-brief-check]");
  const downloadButton = root.querySelector("[data-brief-download]");
  const status = root.querySelector("[data-brief-status]");
  let answers = null;

  function selectedIndex(group) {
    const checked = group.querySelector("input[type='radio']:checked");
    return checked ? Number(checked.value) : null;
  }

  checkButton.addEventListener("click", () => {
    answers = groups.map(selectedIndex);
    if (answers.some((value) => value === null)) {
      status.textContent = "Answer each question before the receipt can be created.";
      downloadButton.disabled = true;
      return;
    }
    groups.forEach((group, i) => {
      const feedback = group.querySelector("[data-q-feedback]");
      const correct = Number(group.dataset.correct);
      const right = answers[i] === correct;
      feedback.hidden = false;
      feedback.textContent = `${right ? "Correct." : "Not quite."} ${group.dataset.explain}`;
    });
    status.textContent = "Checked on this device. You can download the receipt; it is not sent anywhere.";
    downloadButton.disabled = false;
  });

  downloadButton.addEventListener("click", () => {
    if (!answers) return;
    const receipt = {
      schema: "gert-self-check-v1",
      brief_version: "winter-load-brief-v1",
      source_url: "https://gertgrid.space/briefs/winter-load",
      generated_at: new Date().toISOString(),
      responses: QUESTIONS.map((question, i) => ({
        id: question.id,
        prompt: question.prompt,
        selected_index: answers[i],
        selected: question.options[answers[i]],
        correct: answers[i] === Number(groups[i].dataset.correct),
      })),
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
