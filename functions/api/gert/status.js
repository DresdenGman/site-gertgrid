// GET /api/gert/status
// This deployment does not connect to ERCOT's operational API and does
// not serve estimated load or weather in its place. Inference stays off
// because ercot-delta-quantile-v1.4 failed its predeclared calibration gate.
const PAYLOAD = {
  status: "degraded",
  environment: "production",
  model_status: "rejected_candidate",
  model_version: "ercot-delta-quantile-v1.4",
  api_version: "1.2.0",
  release_sha: "sites",
  deployment_platform: "sites",
  capabilities: {
    historical_analysis: true,
    official_ercot_data: false,
    probabilistic_prediction: false,
    scenario_analysis: false,
    validated_backtest: false,
    ai_analysis: false,
    // No simulated forecast mode is shipped on this site. The polar-vortex
    // playback is a separately labeled educational reconstruction.
    presentation_mode: false,
  },
};

export function onRequestGet() {
  return Response.json(PAYLOAD, {
    headers: { "cache-control": "no-store" },
  });
}
