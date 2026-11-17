# gertgrid.space

Source for the Grid Extreme Risk Toolkit (GERT) project site.
The site is static HTML plus Cloudflare Pages Functions.

The homepage leads with two public records:

1. `ercot-delta-quantile-v1.4` missed the calibration gates that were
   fixed before its 96-hour evaluation window. Evidence is served at
   `GET /api/gert/model/evidence`.
2. A Historical Lab over 216 hours of public ERCOT native load
   (dataset DOI `10.5281/zenodo.22975251`). Capacity and reductions
   are assumptions. The lab is not a live forecast.

Official ERCOT operating data is not connected here.
`official_ercot_data` is `false`. Load and weather routes return 503
and do not substitute estimated values. Prediction and scenario routes
return 503 because the candidate failed its calibration gate.
`GET /api/gert/events/playback/polar-vortex` serves a labeled
educational reconstruction (`synthetic_reconstruction`), the same
payload as the companion tool.

Unknown paths return HTTP 404. `/lab` redirects to `/history`.

## Local preview

```sh
python3 scripts/render_site.py
npx wrangler pages dev .
```

## Regenerate pages

`scripts/render_site.py` writes the HTML and the playback function from
`data/historical-cases.json` and `data/playback-polar-vortex.json`.
Run it after either file changes.

## Deployment

Cloudflare Pages, framework preset none, build command empty, output
directory `/`. Do not deploy this repository straight to the production
domain from a feature branch.
