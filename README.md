# gertgrid.space

GERT — Grid Extreme Risk Toolkit. A decision-facing interface for
ERCOT power-grid tail risk: P50–P99 risk view, scenario stress
testing, a polar-vortex event study, and the model-governance record.

The site is static HTML/CSS/JS plus a small set of Cloudflare Pages
Functions under `functions/`:

| Route | Behavior |
|---|---|
| `GET /api/gert/health` | Service health payload |
| `GET /api/gert/status` | Model status and capabilities |
| `GET /api/gert/model/evidence` | Frozen evaluation evidence for the candidate model |
| any other `/api/gert/*` | `503 capability_disabled` |

The candidate model (ercot-delta-quantile-v1.4) failed its
predeclared calibration tolerance at Q90/Q95/Q99 and is **not**
authorized for production inference. That is why every inference
capability reports `false` in `/api/gert/status` and the prediction
endpoints stay disabled — the interface does not substitute or
fabricate a forecast. The front end also ships a demo mode
(`?demo=1`) that runs entirely on built-in sample data.

## Local preview

Static pages only:

```sh
python3 -m http.server 8000
```

Including the API functions (recommended):

```sh
npx wrangler pages dev .
```

## Deployment (Cloudflare Pages)

1. Cloudflare dashboard → Workers & Pages → Create → Pages →
   Connect to Git → select this repository.
2. Framework preset: **None**. Build command: *(leave empty)*.
   Build output directory: `/`. Functions in `functions/` are
   picked up automatically.
3. Add the custom domain `gertgrid.space` under Custom domains,
   then update DNS as prompted.

Every push to `main` redeploys automatically.
