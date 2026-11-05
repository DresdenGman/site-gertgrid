// GET /api/gert/health
// Replicated from the response measured on the previous platform.
// The timestamp is generated per request; everything else is the
// recorded payload.
const PAYLOAD = {
  "status": "ok",
  "timestamp": "2026-11-05T10:09:30.839Z",
  "backend": "gert-sites-native-v1",
  "api_version": "1.2.0",
  "release_sha": "sites",
  "deployment_platform": "sites",
  "ai_enabled": false,
  "env": "production"
};

export function onRequestGet() {
  const body = { ...PAYLOAD, timestamp: new Date().toISOString() };
  return Response.json(body);
}
