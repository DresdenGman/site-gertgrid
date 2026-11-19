const EXPECTED_ARCHIVE_SHA = "f403890ad50a654f85584e03642267d1a06bafb25bf4799346bbf87c4999181b";

function roundMwh(value) {
  return Math.round(value);
}

function analyze(hours, capacity, reductionPct) {
  const factor = 1 - reductionPct / 100;
  let hoursAbove = 0;
  let gapEnergy = 0;
  let peak = 0;
  const rows = hours.map((hour) => {
    const recorded = hour.load_mw;
    if (recorded > peak) peak = recorded;
    const adjusted = recorded * factor;
    const gap = Math.max(0, adjusted - capacity);
    if (gap > 0) hoursAbove += 1;
    gapEnergy += gap;
    return {
      timestamp: hour.timestamp,
      recorded,
      adjusted,
      capacity,
      gap,
    };
  });
  const minReduction = peak > 0 ? Math.max(0, 100 * (1 - capacity / peak)) : 0;
  return { rows, hoursAbove, gapEnergy, peak, minReduction };
}

function formatMw(value, digits) {
  return value.toLocaleString("en-US", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  });
}

async function sha256Hex(buffer) {
  const digest = await crypto.subtle.digest("SHA-256", buffer);
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function drawChart(svg, rows, capacity) {
  const width = 720;
  const height = 180;
  const peak = Math.max(capacity, ...rows.map((row) => row.recorded));
  const barWidth = width / rows.length;
  const scale = (value) => height - (value / peak) * (height - 16) - 8;
  const bars = rows.map((row, index) => {
    const x = index * barWidth;
    const y = scale(row.recorded);
    const fill = row.gap > 0 ? "#ff4d00" : "#141414";
    return `<rect x="${x.toFixed(2)}" y="${y.toFixed(2)}" width="${Math.max(barWidth - 1, 0.5).toFixed(2)}" height="${(height - y - 8).toFixed(2)}" fill="${fill}"></rect>`;
  }).join("");
  const yCap = scale(capacity);
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.innerHTML = `${bars}<line x1="0" x2="${width}" y1="${yCap.toFixed(2)}" y2="${yCap.toFixed(2)}" stroke="#1c5c38" stroke-width="2"></line>`;
}

function renderTable(table, rows) {
  const body = rows.map((row) => `<tr>
    <td>${row.timestamp}</td>
    <td>${formatMw(row.recorded, 3)}</td>
    <td>${formatMw(row.adjusted, 3)}</td>
    <td>${formatMw(row.capacity, 0)}</td>
    <td>${formatMw(row.gap, 3)}</td>
  </tr>`).join("");
  table.querySelector("tbody").innerHTML = body;
}

function setText(root, name, text) {
  const node = root.querySelector(`[data-field="${name}"]`);
  if (!node) return;
  if (node.tagName === "A") {
    node.href = text;
    return;
  }
  node.textContent = text;
}

async function initLab(root) {
  const status = root.querySelector("[data-lab-status]");
  try {
    const response = await fetch("/data/historical-cases.json");
    if (!response.ok) throw new Error(`Archive request failed (${response.status}).`);
    const buffer = await response.arrayBuffer();
    const hash = await sha256Hex(buffer);
    if (hash !== EXPECTED_ARCHIVE_SHA) {
      throw new Error("Bundled archive checksum does not match the Zenodo record. Interactive results withheld.");
    }
    const data = JSON.parse(new TextDecoder().decode(buffer));
    const cases = data.cases;
    const caseButtons = [...root.querySelectorAll("[data-case]")];
    const capacityInput = root.querySelector("[data-capacity]");
    const reductionInput = root.querySelector("[data-reduction]");
    const reductionOut = root.querySelector("[data-reduction-out]");
    const svg = root.querySelector("[data-chart]");
    const table = root.querySelector("[data-hours]");
    const results = root.querySelector(".results");
    let active = cases.find((item) => item.id === root.dataset.referenceCase) || cases[0];
    let lastState = null;

    function publish() {
      const capacity = Number(capacityInput.value);
      const reduction = Number(reductionInput.value);
      reductionOut.textContent = `${reduction.toFixed(1)}%`;
      if (!Number.isFinite(capacity) || capacity <= 0) {
        results.hidden = true;
        status.textContent = "Assumed capacity has to be a positive number of megawatts. No result is shown.";
        return;
      }
      if (!Number.isFinite(reduction) || reduction < 0 || reduction > 100) {
        results.hidden = true;
        status.textContent = "Load reduction has to be between 0% and 100%. No result is shown.";
        return;
      }
      results.hidden = false;
      const before = analyze(active.hours, capacity, 0);
      const after = analyze(active.hours, capacity, reduction);
      const referenceMatch = active.id === root.dataset.referenceCase
        && capacity === Number(root.dataset.referenceCapacity)
        && reduction === Number(root.dataset.referenceReduction);
      if (referenceMatch) {
        const expected = {
          hoursBefore: Number(root.dataset.referenceHoursBefore),
          hoursAfter: Number(root.dataset.referenceHoursAfter),
          energyBefore: Number(root.dataset.referenceEnergyBefore),
          energyAfter: Number(root.dataset.referenceEnergyAfter),
          minReduction: root.dataset.referenceMinReduction,
        };
        const minText = after.minReduction.toFixed(3);
        if (
          before.hoursAbove !== expected.hoursBefore
          || after.hoursAbove !== expected.hoursAfter
          || roundMwh(before.gapEnergy) !== expected.energyBefore
          || roundMwh(after.gapEnergy) !== expected.energyAfter
          || minText !== expected.minReduction
        ) {
          results.hidden = true;
          status.textContent = "This archive does not reproduce the published reference case. Interactive results withheld.";
          return;
        }
      }
      setText(root, "case-title", active.title);
      setText(root, "case-note", active.note);
      setText(root, "hours", `${before.hoursAbove} → ${after.hoursAbove}`);
      setText(root, "hours-detail", `Before → after the assumed reduction, out of ${active.hours.length} hours.`);
      setText(root, "energy", `${roundMwh(after.gapEnergy).toLocaleString("en-US")} MWh`);
      setText(root, "energy-detail", `Before reduction: ${roundMwh(before.gapEnergy).toLocaleString("en-US")} MWh. Rounded sum of hourly gaps. Not expected unserved energy.`);
      setText(root, "min", `${after.minReduction.toFixed(3)}%`);
      setText(root, "peak", `${formatMw(after.peak, 3)} MW`);
      setText(root, "sha", active.source_archive_sha256);
      setText(root, "source", active.source_url);
      const sample = after.rows.find((row) => row.timestamp === "2023-08-10T15:00:00-05:00") || after.rows.reduce((best, row) => row.recorded > best.recorded ? row : best);
      const beforeGap = Math.max(0, sample.recorded - capacity);
      const caseLabel = { "summer-2023": "Summer 2023", "spring-2023": "Spring 2023", "winter-2021": "Winter 2021" }[active.id] || active.title;
      setText(root, "sample-case", caseLabel);
      setText(root, "sample-capacity", `${formatMw(capacity, 0)} MW`);
      setText(root, "sample-reduction", `${reduction}%`);
      setText(root, "sample-time", sample.timestamp);
      setText(root, "sample-recorded", `${formatMw(sample.recorded, 2)} MW`);
      setText(root, "sample-math", `${formatMw(sample.recorded, 2)} × (1 − ${reduction} / 100) = ${formatMw(sample.adjusted, 2)} MW`);
      setText(root, "sample-gap", `max(0, ${formatMw(sample.adjusted, 2)} − ${formatMw(capacity, 0)}) = ${formatMw(sample.gap, 2)} MW`);
      setText(root, "sample-before", `${formatMw(beforeGap, 2)} MW`);
      drawChart(svg, after.rows, capacity);
      renderTable(table, after.rows);
      lastState = { active, capacity, reduction, before, after };
      status.textContent = referenceMatch
        ? "Reference case matches the published Historical Lab figures."
        : "Results were recomputed in the browser from the checksummed archive.";
      root.dataset.ready = "true";
    }

    const params = new URLSearchParams(location.search);
    const wantedCase = params.get("case");
    if (wantedCase) {
      const found = cases.find((item) => item.id === wantedCase);
      if (found) {
        active = found;
        caseButtons.forEach((other) => other.setAttribute("aria-pressed", other.dataset.case === found.id ? "true" : "false"));
        capacityInput.value = String(found.default_capacity_mw);
      }
    }
    if (params.has("capacity")) {
      const capParam = Number(params.get("capacity"));
      if (Number.isFinite(capParam) && capParam >= 1000 && capParam <= 100000) capacityInput.value = String(capParam);
    }
    if (params.has("reduction")) {
      const redParam = Number(params.get("reduction"));
      if (Number.isFinite(redParam) && redParam >= 0 && redParam <= 20) reductionInput.value = String(redParam);
    }

    caseButtons.forEach((button) => {
      button.addEventListener("click", () => {
        active = cases.find((item) => item.id === button.dataset.case);
        caseButtons.forEach((other) => other.setAttribute("aria-pressed", other === button ? "true" : "false"));
        capacityInput.value = String(active.default_capacity_mw);
        publish();
      });
    });
    capacityInput.addEventListener("input", publish);
    reductionInput.addEventListener("input", publish);

    function saveFile(name, text, type) {
      const url = URL.createObjectURL(new Blob([text], { type }));
      const link = document.createElement("a");
      link.href = url;
      link.download = name;
      document.body.appendChild(link);
      try { link.click(); } finally { link.remove(); }
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    }
    const dlJson = root.querySelector("[data-dl-json]");
    const dlCsv = root.querySelector("[data-dl-csv]");
    if (dlJson) dlJson.addEventListener("click", () => {
      if (!lastState) return;
      const { active: c, capacity, reduction, before, after } = lastState;
      const report = {
        schema: "gert-historical-lab-report-v1",
        case: c.id,
        case_title: c.title,
        capacity_mw: capacity,
        reduction_pct: reduction,
        hours_above_before: before.hoursAbove,
        hours_above_after: after.hoursAbove,
        gap_energy_before_mwh: roundMwh(before.gapEnergy),
        gap_energy_after_mwh: roundMwh(after.gapEnergy),
        min_reduction_pct: Number(after.minReduction.toFixed(3)),
        peak_mw: Number(after.peak.toFixed(3)),
        source_archive_sha256: c.source_archive_sha256,
        rows: after.rows.map((row) => ({
          timestamp: row.timestamp,
          recorded_mw: Number(row.recorded.toFixed(3)),
          adjusted_mw: Number(row.adjusted.toFixed(3)),
          capacity_mw: capacity,
          gap_mw: Number(row.gap.toFixed(3)),
        })),
      };
      saveFile(`gert-historical-lab-${c.id}.json`, JSON.stringify(report, null, 2), "application/json");
    });
    if (dlCsv) dlCsv.addEventListener("click", () => {
      if (!lastState) return;
      const lines = ["timestamp,recorded_mw,adjusted_mw,capacity_mw,gap_mw"];
      lastState.after.rows.forEach((row) => {
        lines.push([row.timestamp, row.recorded.toFixed(3), row.adjusted.toFixed(3), lastState.capacity, row.gap.toFixed(3)].join(","));
      });
      saveFile(`gert-historical-lab-${lastState.active.id}.csv`, lines.join("\n") + "\n", "text/csv");
    });

    publish();
  } catch (error) {
    status.textContent = error instanceof Error ? error.message : "The Historical Lab could not load the archive.";
  }
}

document.querySelectorAll("[data-lab]").forEach((root) => {
  initLab(root);
});
