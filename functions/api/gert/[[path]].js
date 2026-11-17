// Catch-all for /api/gert/* routes that do not have their own function.
//
// Inference routes stay closed because ercot-delta-quantile-v1.4 failed
// its predeclared calibration gate. Load and weather are a separate fact:
// this deployment is not connected to official ERCOT operating data, and
// it does not fill the gap with estimated_fallback numbers.

const INFERENCE = /^(predict|scenario|analyze|backtest|ai)(\/|$)/;

export function onRequest(context) {
  const rest = context.params.path;
  const joined = Array.isArray(rest) ? rest.join("/") : String(rest || "");

  if (joined.startsWith("events/")) {
    return Response.json(
      {
        status: "not_found",
        error: "unknown_event",
        message:
          "No labeled playback is published for this path. /api/gert/events/playback/polar-vortex serves an educational reconstruction (synthetic_reconstruction), not an official ERCOT record.",
      },
      { status: 404, headers: { "cache-control": "no-store" } },
    );
  }

  if (INFERENCE.test(joined)) {
    return Response.json(
      {
        status: "unavailable",
        error: "capability_disabled",
        message:
          "This capability is disabled. The candidate model ercot-delta-quantile-v1.4 failed its predeclared calibration gate and is not authorized for production inference.",
        model_version: "ercot-delta-quantile-v1.4",
        historical_lab: "/history",
      },
      { status: 503, headers: { "cache-control": "no-store" } },
    );
  }

  return Response.json(
    {
      status: "unavailable",
      error: "operating_context_unavailable",
      message:
        "Official ERCOT operating context is not connected on this deployment. No estimated load, capacity, or weather value is substituted.",
      official_ercot_data: false,
    },
    { status: 503, headers: { "cache-control": "no-store" } },
  );
}
