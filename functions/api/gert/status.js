// GET /api/gert/status
// Replicated verbatim from the response measured on the previous
// platform. The candidate model was rejected in calibration, so all
// inference capabilities remain false here exactly as they were.
const PAYLOAD = {
  "status": "degraded",
  "environment": "production",
  "model_status": "rejected_candidate",
  "model_version": "ercot-delta-quantile-v1.4",
  "api_version": "1.2.0",
  "release_sha": "sites",
  "deployment_platform": "sites",
  "capabilities": {
    "official_ercot_data": true,
    "probabilistic_prediction": false,
    "scenario_analysis": false,
    "validated_backtest": false,
    "ai_analysis": false,
    "presentation_mode": true
  }
};

export function onRequestGet() {
  return Response.json(PAYLOAD);
}
