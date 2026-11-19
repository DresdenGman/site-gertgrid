function field(name) {
  return document.querySelector(`[data-m="${name}"]`);
}

function setText(name, text) {
  const node = field(name);
  if (node) node.textContent = text;
}

async function loadStatus() {
  try {
    const response = await fetch("/api/gert/status");
    if (!response.ok) throw new Error(String(response.status));
    const data = await response.json();
    setText("model", data.model_status && data.model_version ? `${data.model_status} · ${data.model_version}` : "UNAVAILABLE");
    return true;
  } catch {
    setText("model", "UNAVAILABLE");
    return false;
  }
}

async function loadHealth() {
  try {
    const response = await fetch("/api/gert/health");
    if (!response.ok) throw new Error(String(response.status));
    const data = await response.json();
    setText("health", data.status ? String(data.status) : "UNAVAILABLE");
    setText("health-note", data.backend && data.api_version && data.timestamp
      ? `Backend ${data.backend} · API ${data.api_version} · answered ${data.timestamp}`
      : "The health endpoint answered without the expected fields.");
    return true;
  } catch {
    setText("health", "UNAVAILABLE");
    setText("health-note", "The health endpoint did not answer.");
    return false;
  }
}

async function loadWeather() {
  try {
    const url = "https://api.open-meteo.com/v1/forecast?latitude=30.2672&longitude=-97.7431&current=temperature_2m,wind_speed_10m,shortwave_radiation";
    const response = await fetch(url);
    if (!response.ok) throw new Error(String(response.status));
    const data = await response.json();
    const current = data.current;
    if (!current || !Number.isFinite(current.temperature_2m)) throw new Error("no current weather");
    setText("temp", `${current.temperature_2m.toFixed(1)} °C`);
    setText("wind", Number.isFinite(current.wind_speed_10m) ? `${(current.wind_speed_10m / 3.6).toFixed(1)} m/s` : "—");
    setText("solar", Number.isFinite(current.shortwave_radiation) ? `${Math.round(current.shortwave_radiation)} W/m²` : "—");
    setText("weather-time", String(current.time).replace("T", " "));
    return true;
  } catch {
    setText("temp", "UNAVAILABLE");
    setText("wind", "—");
    setText("solar", "—");
    setText("weather-time", "—");
    return false;
  }
}

async function refresh() {
  setText("banner", "Checking the status endpoints…");
  const core = await Promise.all([loadStatus(), loadHealth()]);
  setText(
    "banner",
    core.every(Boolean)
      ? "Status and health answered. The weather reading may take a few more seconds. Prediction stays gated; ERCOT load and capacity are not connected, so they stay UNAVAILABLE."
      : "Some sources did not answer; their fields say UNAVAILABLE. Prediction stays gated; ERCOT load and capacity are not connected."
  );
  loadWeather();
}

const refreshButton = document.querySelector("[data-m-refresh]");
if (refreshButton) refreshButton.addEventListener("click", refresh);
refresh();
