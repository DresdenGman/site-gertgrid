const LIMITATION = "Invented two-hour teaching model, not ERCOT observations or an estimate of historical outage losses. A downloaded snapshot is not evidence of participation, review, or independent use.";

function world(demandMw, ceilingMw) {
  const rows = demandMw.map((demand, i) => {
    const deliveredMw = Math.min(demand, ceilingMw[i]);
    return {
      hour: i + 1,
      assumedDemandMw: demand,
      assumedDeliveryCeilingMw: ceilingMw[i],
      deliveredMw,
      unservedMwh: (demand - deliveredMw) * 1,
    };
  });
  return { rows, totalUnservedMwh: rows.reduce((sum, row) => sum + row.unservedMwh, 0) };
}

function scenario(secondHourDemandMw) {
  const a = world([60000, 45000], [90000, 90000]);
  const b = world([60000, secondHourDemandMw], [90000, 45000]);
  return {
    a,
    b,
    sameReadings: a.rows.every((row, i) => row.deliveredMw === b.rows[i].deliveredMw),
    differentUnservedEnergy: a.totalUnservedMwh !== b.totalUnservedMwh,
  };
}

function snapshot(secondHourDemandMw, createdAt) {
  return {
    schema: "gert-teaching-snapshot-v1",
    activity_version: "same-meter-v1",
    created_at: createdAt,
    model: "delivered = min(assumed demand, assumed delivery ceiling); unserved energy = (assumed demand - delivered) x interval hours",
    interval_hours: 1,
    second_hour_demand_mw: secondHourDemandMw,
    ...scenario(secondHourDemandMw),
    evidence_status: "local_model_snapshot_not_verified_participation",
    limitations: LIMITATION,
  };
}

const format = (value) => new Intl.NumberFormat("en-US").format(value);

function initSameMeter(root) {
  const input = root.querySelector("[data-sm-demand]");
  const out = root.querySelector("[data-sm-out]");
  const applied = root.querySelector("[data-sm-applied]");
  const unserved = root.querySelector("[data-sm-unserved]");
  const reveal = root.querySelector("[data-sm-reveal]");
  const tbody = root.querySelector("[data-sm-table] tbody");
  const notice = root.querySelector("[data-sm-notice]");
  const downloadButton = root.querySelector("[data-sm-download]");

  function render() {
    const demand = Number(input.value);
    const result = scenario(demand);
    out.textContent = `${demand / 1000} GW`;
    applied.textContent = `Applied input: ${demand / 1000} GW. The model outputs below have been recalculated.`;
    unserved.textContent = `${format(result.b.totalUnservedMwh)} MWh`;
    const rows = [
      ...result.a.rows.map((row) => ["A", row]),
      ...result.b.rows.map((row) => ["B", row]),
    ];
    tbody.innerHTML = rows.map(([key, row]) => `<tr>
      <td>${key} / ${row.hour}</td>
      <td>${format(row.assumedDemandMw)}</td>
      <td>${format(row.assumedDeliveryCeilingMw)}</td>
      <td>${format(row.deliveredMw)}</td>
      <td>${format(row.unservedMwh)}</td>
    </tr>`).join("");
    reveal.innerHTML = result.differentUnservedEnergy
      ? `<strong>Same two readings. Different unserved energy.</strong> World A leaves 0 MWh unserved; World B leaves ${format(result.b.totalUnservedMwh)} MWh unserved under its assumptions. The readings alone do not tell you which world you are in.`
      : `<strong>At 45 GW, both worlds serve all demand. Move above 45 GW to construct the counterexample.</strong> The different delivery ceilings alone do not imply unserved energy: demand must exceed the ceiling in this model.`;
  }

  input.addEventListener("input", render);
  downloadButton.addEventListener("click", () => {
    try {
      const data = snapshot(Number(input.value), new Date().toISOString());
      const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }));
      const link = document.createElement("a");
      link.href = url;
      link.download = "gert-same-meter-model.json";
      document.body.appendChild(link);
      try { link.click(); } finally { link.remove(); }
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      notice.textContent = "Download requested. The model snapshot is not a certificate or proof of independent use.";
    } catch {
      notice.textContent = "Download unavailable. You can copy the assumptions and calculations from the table above.";
    }
  });
  render();
}

document.querySelectorAll("[data-same-meter]").forEach((root) => initSameMeter(root));
