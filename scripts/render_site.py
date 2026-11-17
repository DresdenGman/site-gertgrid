#!/usr/bin/env python3
"""Render the static pages and the labeled polar-vortex playback function."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "data" / "historical-cases.json").read_text())
PLAYBACK = json.loads((ROOT / "data" / "playback-polar-vortex.json").read_text())

GATES = [
    ("Q50 calibration error", "0.020833", "absolute error ≤ 0.03", True),
    ("Q90 calibration error", "0.035417", "absolute error ≤ 0.03", False),
    ("Q95 calibration error", "0.04375", "absolute error ≤ 0.03", False),
    ("Q99 calibration error", "0.031667", "absolute error ≤ 0.03", False),
    ("Positive pinball skill", "+0.757824", "skill > 0 at every quantile", True),
    ("Quantile monotonicity", "0 crossings", "crossings = 0", True),
]

SKILL = [
    ("P50", "0.50", "0.520833", "0.020833", "+0.841492", True),
    ("P90", "0.90", "0.864583", "0.035417", "+0.757824", False),
    ("P95", "0.95", "0.90625", "0.04375", "+0.78482", False),
    ("P99", "0.99", "0.958333", "0.031667", "+0.768279", False),
]

NAV = [
    ("/", "Record"),
    ("/history", "Historical Lab"),
    ("/review", "Review"),
    ("/benchmark", "Benchmarks"),
    ("/events/polar-vortex", "Event Replay"),
    ("/scenario", "Scenario"),
    ("/research", "Research"),
    ("/about", "About"),
]


def nav(current: str) -> str:
    links = []
    for href, label in NAV:
        current_attr = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{current_attr}>{label}</a>')
    return "\n".join(links)


def footer() -> str:
    return """
<footer class="site">
  <div class="wrap">
    <p><strong>Grid Extreme Risk Toolkit (GERT)</strong> is decision-support research. It is not an autonomous grid controller, and this deployment does not show live ERCOT load.</p>
    <ul>
      <li>Software concept DOI <a href="https://doi.org/10.5281/zenodo.23982226">10.5281/zenodo.23982226</a> (resolves to v1.2.0, published 2026-11-05; version DOI 10.5281/zenodo.23982227).</li>
      <li>Dataset DOI <a href="https://doi.org/10.5281/zenodo.22975251">10.5281/zenodo.22975251</a> (Historical Lab, 216 public ERCOT hours, published 2026-09-26).</li>
      <li>Sister benchmark DOI <a href="https://doi.org/10.5281/zenodo.24010850">10.5281/zenodo.24010850</a> (PJM Cold-Spell Calibration Benchmark v1.0.0, published 2026-11-06).</li>
      <li>Tests: 141 backend and 50 frontend passed in CI on 2026-11-05 (main, commit 796e7683, the v1.2.0 archive). No main-branch run dated 2026-11-09 was found.</li>
      <li>Community record: a few organizer-relayed sessions and hands-on runs, and 0 independent replications. <a href="https://gert-d.vercel.app/community">Companion ledger</a>. Participant and survey totals are not used here.</li>
      <li><a href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-">Source repository</a> · <a href="/api/gert/model/evidence">Evidence JSON</a> · <a href="https://gert-d.vercel.app/history">Companion Historical Lab</a></li>
    </ul>
  </div>
</footer>
"""


def page(title: str, description: str, current: str, body: str, scripts: str = "") -> str:
    script_tags = "\n".join(f'<script src="{src}" defer></script>' for src in scripts.split() if src)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="Dresden Goehner">
<link rel="canonical" href="https://gertgrid.space{current if current != "/" else ""}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://gertgrid.space/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Grid Extreme Risk Toolkit (GERT): the v1.4 candidate failed its predeclared calibration gate.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://gertgrid.space/og.png">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Grid Extreme Risk Toolkit (GERT)","applicationCategory":"ScientificApplication","operatingSystem":"Web","url":"https://gertgrid.space","codeRepository":"https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-","identifier":"https://doi.org/10.5281/zenodo.23982226","description":"Evidence-first research software for ERCOT tail-risk questions. The v1.4 candidate is rejected for production inference.","author":{{"@type":"Person","name":"Dresden Goehner"}}}}</script>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<div class="frame">
<header class="site"><div class="wrap">
  <div class="brand">
    <a class="name" href="/">Grid Extreme Risk Toolkit (GERT)</a>
    <small>Research record, not a live dispatch tool</small>
  </div>
  <nav class="primary" aria-label="Primary">{nav(current)}</nav>
</div></header>
<main id="content" class="wrap">
{body}
</main>
{footer()}
</div>
{script_tags}
</body>
</html>
"""


def gate_table() -> str:
    rows = []
    for name, observed, requirement, passed in GATES:
        mark = '<span class="pass-text">Pass</span>' if passed else '<span class="fail-text">Fail</span>'
        rows.append(f"<tr><td>{name}</td><td>{observed}</td><td>{requirement}</td><td>{mark}</td></tr>")
    return """
<div class="scroll" tabindex="0">
<table>
<caption class="note">Predeclared gates for ercot-delta-quantile-v1.4. Exact values from evidence/ercot_v1_4_validation.json and GET /api/gert/model/evidence. Pinball skill is a unitless score against a frozen baseline, not a percent accuracy.</caption>
<thead><tr><th>Gate</th><th>Observed</th><th>Requirement, set beforehand</th><th>Result</th></tr></thead>
<tbody>
""" + "\n".join(rows) + """
</tbody>
</table>
</div>
"""


def skill_table() -> str:
    rows = []
    for quantile, target, empirical, error, skill, passed in SKILL:
        mark = '<span class="pass-text">Pass</span>' if passed else '<span class="fail-text">Fail</span>'
        rows.append(
            f"<tr><td>{quantile}</td><td>{target}</td><td>{empirical}</td><td>{error}</td><td>{skill}</td><td>{mark}</td></tr>"
        )
    return """
<div class="scroll" tabindex="0">
<table>
<caption class="note">Frozen 96-hour window, 2026-08-21 through 2026-08-24. Q50 mean absolute error 404.535 MW. Quantile crossings: 0. Published 2026-08-30.</caption>
<thead><tr><th>Quantile</th><th>Target coverage</th><th>Empirical coverage</th><th>Absolute error</th><th>Pinball skill</th><th>Calibration gate</th></tr></thead>
<tbody>
""" + "\n".join(rows) + """
</tbody>
</table>
</div>
"""


def lab_block() -> str:
    summer = next(case for case in CASES["cases"] if case["id"] == "summer-2023")
    buttons = []
    for case in CASES["cases"]:
        pressed = "true" if case["id"] == "summer-2023" else "false"
        buttons.append(
            f'<button type="button" data-case="{case["id"]}" aria-pressed="{pressed}">{case["title"]}</button>'
        )
    return f"""
<section class="lab" data-lab
  data-reference-case="summer-2023"
  data-reference-capacity="80000"
  data-reference-reduction="5"
  data-reference-hours-before="21"
  data-reference-hours-after="7"
  data-reference-energy-before="66683"
  data-reference-energy-after="4458"
  data-reference-min-reduction="6.393">
  <p class="kicker">Reproducible Historical Lab</p>
  <h2>216 published hours. Your assumptions. No forecast.</h2>
  <p>Three 72-hour windows of ERCOT hourly native load, from dataset DOI 10.5281/zenodo.22975251. Capacity and the uniform reduction are assumptions. Gap energy is the sum of hourly shortfalls against that assumption. It is not expected unserved energy, and it is not the rejected probabilistic model.</p>
  <p class="note" data-lab-status>Reference figures below are for summer 2023 at 80,000 MW and a 5% reduction. The archive checksum is checked before any figure is replaced.</p>
  <div class="cases" role="group" aria-label="Historical window">{"".join(buttons)}</div>
  <div class="controls card">
    <label><span class="key">Assumed available capacity</span>
      <input data-capacity type="number" min="1" step="1" value="{summer["default_capacity_mw"]}" inputmode="numeric">
    </label>
    <label><span class="key">Uniform load reduction <span data-reduction-out>5.0%</span></span>
      <input data-reduction type="range" min="0" max="20" step="0.1" value="5" aria-valuemin="0" aria-valuemax="20">
    </label>
    <p data-field="case-note">{summer["note"]}</p>
  </div>
  <div class="results" aria-live="polite">
    <div class="grid stats">
      <article class="card"><h3>Hours above the assumption</h3><p class="stat-value" data-field="hours">21 → 7</p><p class="note" data-field="hours-detail">Before → after a 5% reduction, out of 72 hours.</p></article>
      <article class="card"><h3>Gap energy after reduction</h3><p class="stat-value" data-field="energy">4,458 MWh</p><p class="note" data-field="energy-detail">Before reduction: 66,683 MWh. Rounded sum of hourly gaps.</p></article>
      <article class="card"><h3>Reduction to clear the peak</h3><p class="stat-value" data-field="min">6.393%</p><p class="note">Algebraic minimum at this capacity. Peak recorded load <span data-field="peak">85,464.116 MW</span>. Feasibility is not evaluated.</p></article>
    </div>
    <svg class="chart" data-chart role="img" aria-label="Recorded hourly load for the selected window. Orange bars are hours still above the assumed capacity after the reduction. The green line is the assumed capacity."></svg>
    <div class="card">
      <h3>One hour, from the archive</h3>
      <p>Summer 2023, <span data-field="sample-time">2023-08-10T15:00:00-05:00</span> (interval start, America/Chicago), at 80,000 MW and 5% until you change the controls.</p>
      <p>Recorded load <strong data-field="sample-recorded">84,660.62 MW</strong>.</p>
      <p class="formula" data-field="sample-math">84,660.62 × (1 − 5 / 100) = 80,427.59 MW</p>
      <p class="formula" data-field="sample-gap">max(0, 80,427.59 − 80,000) = 427.59 MW</p>
      <p class="note">Gap before the reduction at this hour: <span data-field="sample-before">4,660.62 MW</span>. Equality would be a gap of zero.</p>
    </div>
    <details>
      <summary>Inspect all 72 hourly calculations</summary>
      <div class="scroll" tabindex="0">
        <table data-hours>
          <caption>Interval starts in America/Chicago. Adjusted and gap columns follow the controls.</caption>
          <thead><tr><th>Interval start</th><th>Recorded MW</th><th>Adjusted MW</th><th>Capacity MW</th><th>Gap MW</th></tr></thead>
          <tbody><tr><td colspan="5">The hourly rows load from the checksummed archive.</td></tr></tbody>
        </table>
      </div>
    </details>
    <p class="note">Source archive SHA-256 <span data-field="sha">{summer["source_archive_sha256"]}</span>. <a data-field="source" href="{summer["source_url"]}">ERCOT native-load archive</a>. Bundled file SHA-256 f403890ad50a654f85584e03642267d1a06bafb25bf4799346bbf87c4999181b. Winter 2021 load includes outages and load shedding and is not unconstrained demand. Native load is not the forecast-zone series used by the probabilistic candidate.</p>
  </div>
</section>
"""


def pjm_block() -> str:
    return """
<section>
  <p class="kicker">Sister benchmark · negative result</p>
  <h2>PJM cold-spell calibration did not transfer.</h2>
  <p>PJM-Cold-Calibration-Benchmark (<a href="https://doi.org/10.5281/zenodo.24010850">10.5281/zenodo.24010850</a>, v1.0.0, published 2026-11-06; repository DresdenGman/PJM-Cold-Calibration-Benchmark) froze its protocol before computing results. The headline is a failure, not a tuning success.</p>
  <div class="grid stats">
    <article class="card fail"><h3>Polar-vortex coverage</h3><p class="stat-value bad">12.5%</p><p class="note">Uncalibrated day-ahead QR-GBT 90% intervals, January 2014 polar-vortex hours.</p></article>
    <article class="card"><h3>Full 2014 evaluation period</h3><p class="stat-value">65.7%</p><p class="note">Same model and interval, outside the claim that every cold event printed 12.5%.</p></article>
    <article class="card fail"><h3>Repairs that passed</h3><p class="stat-value bad">0 of 18</p><p class="note">Horizon × learner cells. No calibrator selected without the target event restored event-window coverage to nominal.</p></article>
  </div>
  <p class="note">The repository also records coverage gaps of +14.3 percentage points for the 2017–18 snap and +9.2 percentage points for Winter Storm Elliott on that same day-ahead QR-GBT arm. Those are separate events. The strict pre-registered form of the collapse judgement narrowly missed on Elliott.</p>
</section>
"""


def home() -> str:
    body = f"""
<p class="kicker">Grid Extreme Risk Toolkit (GERT)</p>
<h1>Thresholds were set first. Then the model failed them.</h1>
<p class="lede">Dresden Goehner froze the promotion gates for <code>ercot-delta-quantile-v1.4</code> before the evaluation window was opened. On the untouched 96-hour window the candidate missed Q90, Q95, and Q99. That rejection, published 2026-08-30, is the front of this site. The Historical Lab below can be recomputed from a public archive.</p>
<p class="banner">Official ERCOT load and live weather are not connected on gertgrid.space. No estimated megawatt or weather value is shown in their place. Prediction and scenario endpoints stay closed.</p>
<div class="grid stats">
  <article class="card fail"><h3>Q90 absolute error</h3><p class="stat-value bad">0.035417</p><p class="note">Gate was ≤ 0.03. Fail.</p></article>
  <article class="card fail"><h3>Q95 absolute error</h3><p class="stat-value bad">0.04375</p><p class="note">Gate was ≤ 0.03. Fail.</p></article>
  <article class="card fail"><h3>Q99 absolute error</h3><p class="stat-value bad">0.031667</p><p class="note">Gate was ≤ 0.03. Fail.</p></article>
</div>
<p>Pinball skill was positive at every reported quantile, about +0.76 to +0.84 against the frozen baseline. Skill did not override the calibration gate. Q50 error was 0.020833 and passed. Quantile crossings were 0. The window has 96 hourly observations and is not, by itself, enough to promote a model.</p>
{gate_table()}
<p><a class="button primary" href="/review">Read the full rejection</a> <a class="button" href="/api/gert/model/evidence">Evidence JSON</a></p>
{lab_block()}
"""
    return page(
        "Grid Extreme Risk Toolkit (GERT)",
        "The v1.4 ERCOT candidate failed predeclared calibration gates. The Historical Lab recomputes published hourly load against assumptions you set.",
        "/",
        body,
        "/assets/lab.js",
    )


def history() -> str:
    body = f"""
<p class="kicker">Historical Lab</p>
<h1>Recompute the hours yourself.</h1>
<p class="lede">Observed ERCOT native load, a capacity you type, and a uniform reduction you choose. The reference row is summer 2023, 80,000 MW, 5%: 21 hours above capacity become 7, gap energy goes from 66,683 MWh to 4,458 MWh, and the peak needs a 6.393% reduction to clear.</p>
{lab_block()}
"""
    return page(
        "Historical Lab — Grid Extreme Risk Toolkit (GERT)",
        "Checksummed Historical Lab for 216 hours of public ERCOT native load. Assumptions stay labeled as assumptions.",
        "/history",
        body,
        "/assets/lab.js",
    )


def review() -> str:
    body = f"""
<p class="kicker">Rejection record</p>
<h1>ercot-delta-quantile-v1.4 is not authorized.</h1>
<p class="lede">The candidate is a one-hour-ahead load-change quantile model. Parameters were frozen before the final window, 2026-08-21T00:00:00Z through 2026-08-24T23:00:00Z. Three calibration gates failed. The threshold was not relaxed after the miss.</p>
{skill_table()}
{gate_table()}
<h2>What stayed gated</h2>
<p>Production prediction, scenario analysis, and validated backtest stay unavailable. This site returns 503 for those routes and does not invent a forecast. The same evidence file is served at <a href="/api/gert/model/evidence">/api/gert/model/evidence</a> and stored in the main repository as <code>evidence/ercot_v1_4_validation.json</code>.</p>
<h2>Limits of this record</h2>
<ul>
  <li>96 hourly observations are a small sample for tail quantiles.</li>
  <li>Positive pinball skill is not calibration.</li>
  <li>GERT is decision-support research and must not be used for autonomous grid control.</li>
  <li>Data provenance for the candidate: official ERCOT system-load archives joined with ERA5 weather. That is the evaluation record, not a live feed on this website.</li>
</ul>
<p><a class="button primary" href="/history">Use the Historical Lab instead</a></p>
"""
    return page(
        "Review — Grid Extreme Risk Toolkit (GERT)",
        "Frozen evaluation of ercot-delta-quantile-v1.4. Q90, Q95, and Q99 missed a predeclared 0.03 absolute coverage error.",
        "/review",
        body,
    )


def benchmark() -> str:
    body = f"""
<p class="kicker">Benchmarks</p>
<h1>Two public failures, with the numbers attached.</h1>
<p class="lede">Neither result is a production forecast. Both were scored against rules written down first.</p>
<h2>ERCOT candidate v1.4</h2>
<p>Minimum reported pinball skill on the frozen window is +0.757824 (about +0.76), not a percent. The calibration gate still failed.</p>
{skill_table()}
{pjm_block()}
"""
    return page(
        "Benchmarks — Grid Extreme Risk Toolkit (GERT)",
        "ERCOT v1.4 pinball skill and calibration gates, plus the PJM cold-spell benchmark's negative coverage result.",
        "/benchmark",
        body,
    )


def research() -> str:
    body = f"""
<p class="kicker">Open research</p>
<h1>The claim is that the miss stays inspectable.</h1>
<p class="lede">Grid Extreme Risk Toolkit (GERT) is public research software. A candidate with positive pinball skill was rejected because it missed gates that were fixed in advance. That is the result this site leads with.</p>
<p>Probabilistic prediction stays closed. This page is the rejection record, the Historical Lab, and the PJM benchmark.</p>
{pjm_block()}
<h2>What was checked, and when</h2>
<p>On 2026-11-05, CI for main commit 796e7683 reported 141 backend tests passed and 50 frontend tests passed. That commit is the v1.2.0 archive behind concept DOI <a href="https://doi.org/10.5281/zenodo.23982226">10.5281/zenodo.23982226</a>. A main-branch run dated 2026-11-09 was not found, so this page does not move the date forward.</p>
<p>Dataset DOI <a href="https://doi.org/10.5281/zenodo.22975251">10.5281/zenodo.22975251</a> is the Historical Lab snapshot: 216 hours, a methodology note, and an independent Python checker.</p>
<h2>Community evidence, kept small</h2>
<p>A few organizer-relayed sessions and hands-on runs are on the companion ledger, with 0 independent replications. Availability is not a completed trial. This site does not use participant totals or survey totals as evidence. <a href="https://gert-d.vercel.app/community">Read the ledger</a>.</p>
<p><a class="button primary" href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-">Inspect the repository</a> <a class="button" href="/review">Open the rejection</a></p>
"""
    return page(
        "Research — Grid Extreme Risk Toolkit (GERT)",
        "Public record for GERT: a rejected v1.4 candidate, checksummed historical hours, and a PJM benchmark that failed its repair test.",
        "/research",
        body,
    )


def about() -> str:
    body = """
<p class="kicker">About</p>
<h1>Grid Extreme Risk Toolkit (GERT)</h1>
<p class="lede">GERT asks how close a demand tail sits to a boundary you can name. The software DOI is the concept record 10.5281/zenodo.23982226, version 1.2.0, published 2026-11-05. The dataset DOI is 10.5281/zenodo.22975251.</p>
<h2>What this website will not do</h2>
<ul>
  <li>It will not present estimated fallback load, such as a 45,000 MW / 65,000 MW pair, as ERCOT's current load.</li>
  <li>It will not fill missing weather with placeholder temperatures or wind speeds.</li>
  <li>It will not run scenario analysis while <code>ercot-delta-quantile-v1.4</code> remains rejected. The Historical Lab is the calculation that stays available.</li>
  <li>It will not treat organizer notes as adoption. The public wording is a few organizer-relayed sessions, hands-on runs, and 0 independent replications.</li>
</ul>
<h2>Tests</h2>
<p>141 backend tests and 50 frontend tests passed in CI on 2026-11-05, main commit 796e7683. That is the date this site can verify. GitHub star counts are not evidence.</p>
<p>Author: Dresden Goehner. Repository: <a href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-">DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-</a>. Companion tool: <a href="https://gert-d.vercel.app/">gert-d.vercel.app</a>.</p>
"""
    return page(
        "About — Grid Extreme Risk Toolkit (GERT)",
        "What Grid Extreme Risk Toolkit (GERT) is, which DOIs identify it, and which claims this site refuses.",
        "/about",
        body,
    )


def scenario() -> str:
    body = """
<p class="kicker">Scenario analysis · gated</p>
<h1>Run Analysis will not invent a scenario.</h1>
<p class="lede">Forecast and scenario routes are disabled because <code>ercot-delta-quantile-v1.4</code> failed its predeclared calibration gate at Q90, Q95, and Q99. Absolute coverage error had to be ≤ 0.03. Observed errors were 0.035417, 0.04375, and 0.031667.</p>
<p>
  <button type="button" class="primary" data-run aria-controls="why-gated">Run Analysis</button>
</p>
<section id="why-gated" class="warn" tabindex="-1">
  <h2>Why this button does not run a model</h2>
  <p>There is no validated production artifact on this deployment, and no weather slider is offered as a stand-in. A 503 from <code>/api/gert/scenario</code> means the capability is off. It does not mean a placeholder forecast is waiting behind the control.</p>
  <p>The calculation that does run is the Historical Lab: published hourly load, an assumed capacity, and a uniform reduction, with every hour downloadable from the checksummed archive.</p>
  <p><a class="button primary" href="/history">Open the Historical Lab</a> <a class="button" href="/review">Read the rejection</a></p>
</section>
"""
    return page(
        "Scenario — Grid Extreme Risk Toolkit (GERT)",
        "Scenario analysis stays disabled after the v1.4 calibration failure. The Historical Lab is the available calculation.",
        "/scenario",
        body,
        "/assets/scenario.js",
    )


def replay() -> str:
    body = """
<p class="kicker">Event Replay · educational reconstruction</p>
<h1>Polar vortex, labeled as a reconstruction.</h1>
<p class="lede">This playback is the same payload the companion tool serves at <code>/api/gert/events/playback/polar-vortex</code>. Provenance is <span data-field="provenance">synthetic_reconstruction</span>. It is a deterministic teaching series, not an official ERCOT historical record and not the rejected v1.4 forecast.</p>
<section data-replay>
  <p class="banner" data-replay-status role="status">Loading the labeled playback…</p>
  <div data-replay-body hidden>
    <div class="replay-head">
      <div>
        <h2 data-field="title">ERCOT Polar Vortex · Decision Replay</h2>
        <p data-field="note">Deterministic educational reconstruction; not an official historical event record.</p>
        <p class="note">Event id <span data-field="event">ercot-2021-educational-reconstruction</span></p>
      </div>
      <button type="button" data-play aria-pressed="false">Play</button>
    </div>
    <label><span class="key">Hour</span>
      <input data-hour type="range" min="0" max="35" value="0" step="1">
    </label>
    <p class="hour-readout" data-field="hour">Hour 0</p>
    <div class="grid stats">
      <article class="card"><h3>Reconstructed temperature</h3><p class="stat-value" data-field="temperature">—</p></article>
      <article class="card"><h3>Series field actual_load_mw</h3><p class="stat-value" data-field="load">—</p><p class="note">Name kept from the file. Not an official meter reading.</p></article>
      <article class="card"><h3>Series field capacity_mw</h3><p class="stat-value" data-field="capacity">—</p></article>
      <article class="card"><h3>Series field gert_p99_load_mw</h3><p class="stat-value" data-field="p99">—</p></article>
      <article class="card"><h3>Series field risk_score</h3><p class="stat-value" data-field="risk">—</p></article>
    </div>
    <h2>Notes stored with the playback</h2>
    <div data-logs></div>
  </div>
</section>
<noscript><p class="warn">Event replay needs the playback request. With scripts disabled, the series is not filled in. The route is /api/gert/events/playback/polar-vortex and it is labeled synthetic_reconstruction.</p></noscript>
"""
    return page(
        "Polar vortex replay — Grid Extreme Risk Toolkit (GERT)",
        "Educational reconstruction of a polar-vortex decision replay. Not an official ERCOT historical record.",
        "/events/polar-vortex",
        body,
        "/assets/replay.js",
    )


def not_found() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found — Grid Extreme Risk Toolkit (GERT)</title>
<link rel="stylesheet" href="/assets/site.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="robots" content="noindex">
</head>
<body>
<div class="frame">
<main class="wrap">
<p class="kicker">404</p>
<h1>This page is not on the site.</h1>
<p class="lede">Nothing was substituted for the missing path. The published record starts on the homepage.</p>
<p><a class="button primary" href="/">Back to the record</a> <a class="button" href="/history">Historical Lab</a></p>
</main>
</div>
</body>
</html>
"""


def write_playback_function() -> None:
    payload = json.dumps(PLAYBACK, indent=2)
    text = f"""// GET /api/gert/events/playback/polar-vortex
// Labeled educational reconstruction. The object matches the companion
// tool response captured on 2026-11-17 from
// https://gert-d.vercel.app/api/gert/events/playback/polar-vortex
// provenance: synthetic_reconstruction.
const PAYLOAD = {payload};

export function onRequestGet() {{
  return Response.json(PAYLOAD, {{
    headers: {{ "cache-control": "no-store" }},
  }});
}}
"""
    path = ROOT / "functions" / "api" / "gert" / "events" / "playback" / "polar-vortex.js"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> None:
    outputs = {
        ROOT / "index.html": home(),
        ROOT / "history.html": history(),
        ROOT / "review.html": review(),
        ROOT / "benchmark.html": benchmark(),
        ROOT / "research.html": research(),
        ROOT / "about.html": about(),
        ROOT / "scenario.html": scenario(),
        ROOT / "events" / "polar-vortex.html": replay(),
        ROOT / "404.html": not_found(),
    }
    for path, html in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html)
        print(path.relative_to(ROOT), len(html))
    write_playback_function()


if __name__ == "__main__":
    main()
