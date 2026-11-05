// Catch-all for every other /api/gert/* route (predict, scenario,
// analyze, weather/live, backtest, events/playback, current load).
//
// On the previous platform these capabilities were gated off: the
// candidate model failed its calibration gate and was never
// authorized for production inference (see /api/gert/status, where
// every inference capability is false). This handler preserves that
// state honestly instead of returning invented data.
export function onRequest() {
  return Response.json(
    {
      status: "unavailable",
      error: "capability_disabled",
      message:
        "This capability is disabled. The candidate model did not pass its calibration gate and is not authorized for production inference.",
    },
    { status: 503 },
  );
}
