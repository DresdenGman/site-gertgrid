function formatNumber(value) {
  return Number(value).toLocaleString("en-US");
}

function render(root, payload, index) {
  const step = payload.steps[index];
  const set = (name, text) => {
    const node = root.querySelector(`[data-field="${name}"]`);
    if (node) node.textContent = text;
  };
  set("title", payload.title);
  set("note", payload.methodology_note);
  set("provenance", payload.provenance);
  set("event", payload.event_id);
  set("hour", `${step.timestamp_label} · hour ${step.hour} of ${payload.total_hours - 1}`);
  set("temperature", `${step.temperature}°C`);
  set("load", `${formatNumber(step.actual_load_mw)} MW`);
  set("capacity", `${formatNumber(step.capacity_mw)} MW`);
  set("p99", `${formatNumber(step.gert_p99_load_mw)} MW`);
  set("risk", String(step.risk_score));
  const logs = root.querySelector("[data-logs]");
  logs.innerHTML = "";
  payload.logs.filter((entry) => entry.hour <= step.hour).forEach((entry) => {
    const item = document.createElement("p");
    item.className = `log ${entry.severity}`;
    item.textContent = `Hour ${entry.hour} · ${entry.severity} · ${entry.source}: ${entry.message}`;
    logs.appendChild(item);
  });
  const range = root.querySelector("[data-hour]");
  range.max = String(payload.total_hours - 1);
  range.value = String(index);
  range.setAttribute("aria-valuetext", step.timestamp_label);
}

async function init(root) {
  const status = root.querySelector("[data-replay-status]");
  try {
    const response = await fetch("/api/gert/events/playback/polar-vortex");
    const payload = await response.json();
    if (!response.ok) {
      const reason = payload.message || payload.error || `HTTP ${response.status}`;
      throw new Error(reason);
    }
    if (payload.provenance !== "synthetic_reconstruction" || !Array.isArray(payload.steps) || payload.steps.length === 0) {
      throw new Error("Playback response is missing its educational-reconstruction label.");
    }
    let index = 0;
    let timer = 0;
    const range = root.querySelector("[data-hour]");
    const play = root.querySelector("[data-play]");
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const stop = () => {
      if (timer) window.clearInterval(timer);
      timer = 0;
      play.setAttribute("aria-pressed", "false");
      play.textContent = "Play";
    };
    const show = (next) => {
      index = next;
      render(root, payload, index);
    };
    range.addEventListener("input", () => {
      stop();
      show(Number(range.value));
    });
    play.addEventListener("click", () => {
      if (timer) {
        stop();
        return;
      }
      if (reduced) {
        status.textContent = "Playback stays on the selected hour because reduced motion is requested. Use the slider to move through the reconstruction.";
        return;
      }
      play.setAttribute("aria-pressed", "true");
      play.textContent = "Pause";
      timer = window.setInterval(() => {
        if (index >= payload.total_hours - 1) {
          stop();
          return;
        }
        show(index + 1);
      }, 700);
    });
    show(0);
    root.querySelector("[data-replay-body]").hidden = false;
    status.textContent = "Showing the labeled educational reconstruction. These figures are not an official ERCOT historical record.";
  } catch (error) {
    status.textContent = error instanceof Error
      ? `Event replay failed: ${error.message}`
      : "Event replay failed.";
  }
}

document.querySelectorAll("[data-replay]").forEach((root) => init(root));
