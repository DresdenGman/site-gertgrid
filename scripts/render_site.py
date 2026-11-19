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
    ("/monitor", "Live Monitor"),
    ("/history", "Historical Lab"),
    ("/review", "Review"),
    ("/benchmark", "Benchmarks"),
    ("/events/polar-vortex", "Event Replay"),
    ("/scenario", "Scenario"),
    ("/briefs", "Briefs"),
    ("/community", "Community"),
    ("/research", "Research"),
    ("/about", "About"),
    ("/changelog", "Version"),
]

REPO = "https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-"


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
      <li>Community record: a few organizer-relayed sessions and hands-on runs, and 0 independent replications. <a href="/community">Community evidence ledger</a>. Participant and survey totals are not used here.</li>
      <li><a href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-">Source repository</a> · <a href="/api/gert/model/evidence">Evidence JSON</a> · <a href="/history">Historical Lab</a></li>
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


V15 = [
    ("Q50", "0.50", "0.508929", "+0.008929", "0.4712 – 0.5466", "+0.930441"),
    ("Q90", "0.90", "0.918155", "+0.018155", "0.8950 – 0.9366", "+0.931548"),
    ("Q95", "0.95", "0.956845", "+0.006845", "0.9387 – 0.9698", "+0.932996"),
    ("Q99", "0.99", "0.988095", "−0.001905", "0.9767 – 0.9940", "+0.944255"),
]


def v15_table() -> str:
    rows = []
    for quantile, target, empirical, error, ci, skill in V15:
        rows.append(
            f"<tr><td>{quantile}</td><td>{target}</td><td>{empirical}</td><td>{error}</td><td>{ci}</td><td>{skill}</td></tr>"
        )
    return """
<div class="scroll" tabindex="0">
<table>
<caption class="note">Evaluation window 2026-10-05 through 2026-11-01, 672 hourly observations. Point estimates and Wilson 95% intervals from the PR #23 evidence snapshot (<code>evidence/snapshots/pr-23/ercot_v1_5_validation.json</code>, published 2026-11-08). The published scores use realized ERA5 weather and are an optimistic upper bound, not a production forecast.</caption>
<thead><tr><th>Quantile</th><th>Target coverage</th><th>Empirical coverage</th><th>Signed error</th><th>Wilson 95% CI</th><th>Pinball skill</th></tr></thead>
<tbody>
""" + "\n".join(rows) + """
</tbody>
</table>
</div>
"""


def v15_section() -> str:
    return f"""
<section>
  <p class="kicker">Next candidate · evidence only</p>
  <h2>The v1.5 candidate met the numeric gate. It is still not packaged.</h2>
  <p><code>ercot-lag-residual-gbt-v1.5-candidate</code> was scored on a preregistered 672-hour window. Its point estimates sit inside the same ±0.03 gate that v1.4 missed, pinball skill is +0.93 to +0.94, and quantile crossings are 0. Two things keep it out of production: the Wilson 95% intervals for Q50 and Q90 extend past the gate, and the evidence-bundle and feature-availability gates are not passed. The v1.4 rejection is unchanged, and the prediction endpoints stay gated.</p>
  {v15_table()}
  <div class="grid stats">
    <article class="card"><h3>Production</h3><p class="stat-value">None.</p><p class="note">No validated model is in production. Prediction endpoints stay gated.</p></article>
    <article class="card fail"><h3>v1.4</h3><p class="stat-value bad">Rejected.</p><p class="note">Q90, Q95, and Q99 missed the ≤ 0.03 gate on the frozen 96-hour window.</p></article>
    <article class="card"><h3>v1.5</h3><p class="stat-value">Evidence only.</p><p class="note">Point estimates inside the gate on 672 hours. Not packaged; PR #23 unmerged.</p></article>
  </div>
</section>
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
    <p class="row">
      <button type="button" data-dl-json>Download the JSON report</button>
      <button type="button" data-dl-csv>Download the hourly CSV</button>
    </p>
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
<p class="banner">Official ERCOT load is not connected on gertgrid.space. No estimated megawatt value is shown in its place. Prediction and scenario endpoints stay closed. The one live reading on this site is external weather on the <a href="/monitor">Live Monitor</a>, labeled with its source.</p>
<div class="grid stats">
  <article class="card fail"><h3>Q90 absolute error</h3><p class="stat-value bad">0.035417</p><p class="note">Gate was ≤ 0.03. Fail.</p></article>
  <article class="card fail"><h3>Q95 absolute error</h3><p class="stat-value bad">0.04375</p><p class="note">Gate was ≤ 0.03. Fail.</p></article>
  <article class="card fail"><h3>Q99 absolute error</h3><p class="stat-value bad">0.031667</p><p class="note">Gate was ≤ 0.03. Fail.</p></article>
</div>
<p>Pinball skill was positive at every reported quantile, about +0.76 to +0.84 against the frozen baseline. Skill did not override the calibration gate. Q50 error was 0.020833 and passed. Quantile crossings were 0. The window has 96 hourly observations and is not, by itself, enough to promote a model.</p>
{gate_table()}
<p><a class="button primary" href="/review">Read the full rejection</a> <a class="button" href="/api/gert/model/evidence">Evidence JSON</a></p>
{v15_section()}
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
<section>
  <p class="kicker">Review &amp; reproduce</p>
  <h2>How to critique the evidence.</h2>
  <p>A review is a check you can repeat: open a historical case, recompute one row, and say what you found. It is not a model validation and it does not authorize a forecast.</p>
  <p class="note">Criticism is recorded only if you submit it. The structured GitHub form and the public discussion are the record. The <a href="/community">community page</a> lists what people have published and which notes are still open. Private replies stay off that page. A comment is not an endorsement.</p>
  <div class="card">
    <h3>Start with a five-minute counterexample.</h3>
    <p>Not ready for a full technical review? Make two invented worlds produce identical meter readings and inspect why their unserved energy differs. Includes a short facilitator guide; no account or installation needed.</p>
    <p><a href="/briefs/same-meter">Open Same meter, two worlds →</a></p>
    <p class="note">An introductory teaching activity, not a completed review of the historical dataset.</p>
  </div>
  <div class="banner">
    <h3>One complete review, about 10 minutes.</h3>
    <ol>
      <li><a href="/history?case=summer-2023&amp;capacity=80000&amp;reduction=0">Open the summer case at 80,000 MW and 0% reduction.</a> Note the hours above assumed capacity and the gap energy.</li>
      <li>Switch to 5% reduction. Explain why the hours and energy change. Can you distinguish the actual observations from the two assumptions?</li>
      <li>Download the JSON report and hourly CSV. Recompute one row as max(0, adjusted load − capacity). Sum the hourly gaps to check the total in MWh.</li>
      <li>Inspect the winter case. Why would measured load during outages be insufficient to reconstruct unmet demand?</li>
      <li>Share one result you checked and one change you would make. A negative finding is useful.</li>
    </ol>
    <p><a class="button primary" href="/history?case=summer-2023&amp;capacity=80000&amp;reduction=0">Start the review</a></p>
  </div>
  <div class="grid duo">
    <article class="card">
      <h3>Reproduce without the website</h3>
      <p>The archive extractor and independent report checker use Python's standard library. The source files, data version, checksums, formulas and limits are documented in the repository.</p>
      <p><a href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-/blob/main/docs/HISTORICAL_LAB.md">Reproduction instructions</a></p>
    </article>
    <article class="card">
      <h3>Use it in a small workshop</h3>
      <p>A ready-to-use 20-minute exercise covers load, power versus energy, counterfactual assumptions, and the difference between arithmetic and a reliable operational decision.</p>
      <p><a href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-/blob/main/docs/WORKSHOP.md">Open the facilitator guide</a></p>
    </article>
  </div>
  <h2>Leave an inspectable review.</h2>
  <p>Use the structured GitHub form for a reproducible review, or add one concise field note to the public discussion. You choose whether to submit. GitHub posts are public: do not include personal contact information, private datasets, credentials, or another person's words without permission.</p>
  <p class="row"><a class="button" href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-/issues/new?template=historical_review.yml">Write a structured review</a> <a class="button primary" href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-/discussions/3">Add one public field note</a></p>
  <p><a href="/community">See the community evidence ledger →</a></p>
  <p class="note">A review records what you actually completed. Feedback is not automatically an endorsement; hosting a session, contributing a critique, and adopting software are different outcomes.</p>
  <h2>What this release establishes</h2>
  <p>Three public-data cases, reproducible deterministic calculations, downloadable reports, and an open review process. User-defined capacity is not historical capacity; counterfactual gap energy is not expected unserved energy. The probabilistic research candidate remains gated until its validation requirements pass.</p>
</section>
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
<p>A few organizer-relayed sessions and hands-on runs are on the community ledger, with 0 independent replications. Availability is not a completed trial. This site does not use participant totals or survey totals as evidence. <a href="/community">Read the ledger</a>.</p>
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


def monitor() -> str:
    body = """
<p class="kicker">Live Monitor</p>
<h1>What is live, and what is not.</h1>
<p class="lede">This page reads the deployment's own status endpoints and one external weather reading. ERCOT system load and capacity are not connected, so those fields stay unavailable instead of showing a substitute number. The prediction layer is gated: the v1.4 candidate was rejected, and v1.5 is evidence only.</p>
<p class="banner" data-m="banner" role="status">Checking the status endpoints…</p>
<div class="grid stats auto">
  <article class="card"><h3>Model status</h3><p class="stat-value" data-m="model">—</p><p class="note">From GET /api/gert/status.</p></article>
  <article class="card"><h3>API health</h3><p class="stat-value" data-m="health">—</p><p class="note" data-m="health-note">From GET /api/gert/health.</p></article>
  <article class="card fail"><h3>Prediction</h3><p class="stat-value bad">UNAVAILABLE</p><p class="note">No validated model is in production. The endpoint stays gated and no simulated forecast is shown.</p></article>
  <article class="card"><h3>System load</h3><p class="stat-value">UNAVAILABLE</p><p class="note">Official ERCOT load is not connected to this deployment. No substitute number is shown.</p></article>
  <article class="card"><h3>Available capacity</h3><p class="stat-value">UNAVAILABLE</p><p class="note">No official adequacy feed is connected.</p></article>
  <article class="card"><h3>Weather · Open-Meteo, Austin, TX</h3><p class="stat-value" data-m="temp">—</p><p class="note">Wind <span data-m="wind">—</span> · Solar <span data-m="solar">—</span> · Reading time <span data-m="weather-time">—</span></p></article>
</div>
<p class="row"><button type="button" class="primary" data-m-refresh>Refresh</button></p>
<p class="note">Weather is an external Open-Meteo reading for the ERCOT region. It is context, not a GERT forecast, and it is never used to fill in load. When a source does not answer, its field says UNAVAILABLE.</p>
<p><a class="button primary" href="/review">Read why prediction is gated</a> <a class="button" href="/history">Open the Historical Lab</a></p>
"""
    return page(
        "Live Monitor — Grid Extreme Risk Toolkit (GERT)",
        "Live status for the GERT deployment: gated prediction, unconnected ERCOT load, and one labeled external weather reading.",
        "/monitor",
        body,
        "/assets/monitor.js",
    )


def briefs_index() -> str:
    body = """
<p class="kicker">Grid notes</p>
<h1>Two short readings.</h1>
<p class="lede">These notes sit beside the Historical Lab. They do not add a forecast, and they do not count a reader as a participant.</p>
<div class="grid duo">
  <article class="card">
    <p class="kicker">Grid notes 01</p>
    <h2><a href="/briefs/winter-load">Why can electricity use fall during a blackout?</a></h2>
    <p>A source-linked reading of 72 ERCOT native-load hours from February 14–16, 2021. Recorded load is not unmet demand.</p>
    <p><a href="/briefs/winter-load">Open this note</a></p>
  </article>
  <article class="card">
    <p class="kicker">Five-minute counterexample</p>
    <h2><a href="/briefs/same-meter">Same meter. Two worlds.</a></h2>
    <p>An invented teaching model: identical electricity readings can hide different unmet demand. It is not a historical measurement.</p>
    <p><a href="/briefs/same-meter">Open this note</a></p>
  </article>
</div>
"""
    return page(
        "Grid Notes — Grid Extreme Risk Toolkit (GERT)",
        "Short teaching notes on recorded ERCOT load and a same-meter counterexample.",
        "/briefs",
        body,
    )


def brief_winter() -> str:
    winter = next(case for case in CASES["cases"] if case["id"] == "winter-2021")
    rows = "\n".join(
        f'<tr><td>{hour["timestamp"]}</td><td>{hour["load_mw"]:.3f}</td></tr>' for hour in winter["hours"]
    )
    body = f"""
<p class="kicker">Grid notes 01 / About 90 seconds to read</p>
<h1>Why can electricity use fall during a blackout?</h1>
<p class="lede">A lower reading can mean less electricity was delivered—not that people needed less. That distinction changes what you can conclude about a grid.</p>
<p class="note">GERT · Dresden Goehner · September 13, 2026 · Historical educational example</p>
<figure>
  <img src="/briefs/winter-load.png" width="1600" height="1200" alt="72 hourly ERCOT native-load observations, February 14–16, 2021, on a zero-to-80-GW scale. A dashed reference marks the reported onset of rotating outages at 01:25 CST on February 15. The curve falls but does not measure unmet demand or reliability.">
  <figcaption class="note">Recorded load only. The vertical reference is an externally reported event time, not a measurement of lost load. <a href="#sources">Sources and all 72 values below.</a> <a href="/briefs/winter-load.png">Open full-size graphic</a></figcaption>
</figure>
<section>
  <p class="kicker">01 / Read the boundary</p>
  <h2>A measurement is not the whole system.</h2>
  <p>ERCOT reported that rotating outages began at 01:25 a.m. on February 15, 2021, after generating units became unavailable. When customers are disconnected, some intended electricity use cannot appear in the recorded load. <a href="https://www.ercot.com/news/release?id=9c552983-008a-3906-8066-8b76315ed3e7">Read the contemporaneous report.</a></p>
  <div class="card">
    <h3>What this curve cannot establish</h3>
    <ul>
      <li>Demand in the absence of interruptions.</li>
      <li>The amount of electricity not supplied.</li>
      <li>Whether reliability improved, or an intervention worked.</li>
    </ul>
    <p class="note">We do not attribute every change to outages. Weather, behavior, and other system conditions also matter.</p>
  </div>
</section>
<section class="card">
  <p class="kicker">Try a five-minute counterexample</p>
  <h2>Same meter. Two worlds.</h2>
  <p>Build two invented situations with identical electricity readings but different unmet demand. Change an assumption and inspect the arithmetic yourself.</p>
  <p><a href="/briefs/same-meter">Try the interactive explanation →</a></p>
</section>
<section data-brief>
  <p class="kicker">Self-check</p>
  <h2>Two questions, answered on this device.</h2>
  <fieldset data-q data-correct="2" data-explain="A fall in the observed series is not a measurement of the electricity people would have used without interruptions. Reliability needs additional evidence.">
    <legend>The recorded load falls. What can this curve alone establish?</legend>
    <label><input type="radio" name="q1" value="0"> The grid became safer.</label>
    <label><input type="radio" name="q1" value="1"> Electricity demand disappeared.</label>
    <label><input type="radio" name="q1" value="2"> Recorded load fell; unmet demand and reliability remain unresolved.</label>
    <p class="note" data-q-feedback hidden></p>
  </fieldset>
  <fieldset data-q data-correct="0" data-explain="max(0, 65,000 − 60,000) MW × 1 hour = 5,000 MWh. It is a hypothetical calculation, not a measured outage or a probability-weighted reliability metric.">
    <legend>In a separate hypothetical one-hour example, load is 65,000 MW and assumed capacity is 60,000 MW. What is the arithmetic gap energy?</legend>
    <label><input type="radio" name="q2" value="0"> 5,000 MWh, under those assumptions.</label>
    <label><input type="radio" name="q2" value="1"> 5,000 MW of proven outage savings.</label>
    <label><input type="radio" name="q2" value="2"> 65,000 MWh of expected unserved energy.</label>
    <p class="note" data-q-feedback hidden></p>
  </fieldset>
  <p class="row"><button type="button" class="primary" data-brief-check>Check answers</button> <button type="button" data-brief-download disabled>Download the receipt</button></p>
  <p class="note" data-brief-status>Nothing is sent anywhere. The receipt is a JSON file on your device; downloading it does not count you as a participant.</p>
</section>
<section>
  <h2>Now change an assumption.</h2>
  <p>Open the winter case with an explicitly assumed 60,000 MW capacity and no load reduction. The arithmetic gap is a counterfactual exercise—not historical outage losses. Try other assumptions and export the calculation.</p>
  <p class="row"><a class="button primary" href="/history?case=winter-2021&amp;capacity=60000&amp;reduction=0">Explore the winter case</a> <a class="button" href="/review">Leave a substantive review</a></p>
</section>
<section id="sources">
  <h2>Sources, exact values, and reuse</h2>
  <ol>
    <li><a href="https://www.ercot.com/files/docs/2021/11/12/Native_Load_2021.zip">ERCOT Native Load 2021 archive</a> — the source of the 72 hourly observations. Interval starts, America/Chicago (CST here); MW in the data, GW on the chart.</li>
    <li><a href="https://www.ercot.com/news/release?id=9c552983-008a-3906-8066-8b76315ed3e7">ERCOT news release, February 15, 2021</a> — the source of the rotating-outage start time. The release is contemporaneous, not a complete retrospective loss estimate.</li>
    <li><a href="/briefs/winter-load-figure-data.json">Exact plotted data and metadata</a> · <a href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-/blob/main/scripts/build_winter_brief.mjs">Figure generator</a> · <a href="https://www.ercot.com/help/terms">ERCOT data-use terms, section 5</a>.</li>
  </ol>
  <p class="note">GERT is independent of ERCOT. No affiliation or endorsement is implied. The original graphic and explanation follow the repository MIT license; underlying data remains attributed to its source.</p>
  <details>
    <summary>Inspect all 72 hourly source values</summary>
    <div class="scroll" tabindex="0">
      <table>
        <caption>Hourly interval starts (CST), February 14–16, 2021</caption>
        <thead><tr><th>Interval start</th><th>Recorded load (MW)</th></tr></thead>
        <tbody>
{rows}
        </tbody>
      </table>
    </div>
  </details>
</section>
"""
    return page(
        "Why can electricity use fall during a blackout? — Grid Extreme Risk Toolkit (GERT)",
        "A short source-linked exercise about observed load, unmet demand, and the February 2021 Texas winter storm.",
        "/briefs/winter-load",
        body,
        "/assets/brief.js",
    )


def brief_same_meter() -> str:
    body = """
<p class="kicker">Grid notes / A five-minute counterexample</p>
<h1>Same meter. Two worlds.</h1>
<p class="lede">Can the same falling electricity readings mean two different things? Build a counterexample, then see why a real blackout curve needs careful interpretation.</p>
<p class="note">No account required · Calculator optional · Invented teaching model, not historical data</p>
<section data-same-meter>
  <div class="card">
    <p class="kicker">01 / What both meters show</p>
    <h2>The same fall. A different story.</h2>
    <p class="big-reading">60 GW → 45 GW</p>
    <p>Each reading is constant over one hour in this invented example. Before looking below: does the fall tell you how much electricity people wanted but did not receive?</p>
  </div>
  <div class="grid duo">
    <article class="card pass">
      <p class="kicker">World A / Less wanted</p>
      <h3>Demand falls to 45 GW.</h3>
      <p>The assumed delivery ceiling stays at 90 GW. All demand in both hours is served.</p>
      <p class="note">Model unserved energy, two hours</p>
      <p class="stat-value">0 MWh</p>
    </article>
    <article class="card fail">
      <p class="kicker">World B / Delivery constrained</p>
      <h3>The ceiling falls to 45 GW.</h3>
      <p>Change the assumed second-hour demand. The meter cannot show electricity that is not delivered.</p>
      <label><span class="key">World B: second-hour demand — <span data-sm-out>65 GW</span></span>
        <input data-sm-demand type="range" min="45000" max="90000" step="5000" value="65000" aria-valuemin="45000" aria-valuemax="90000">
      </label>
      <p class="note">45 GW — 90 GW</p>
      <p class="banner" data-sm-applied role="status">Applied input: 65 GW. The model outputs below have been recalculated.</p>
      <p class="note">Hour-two meter</p>
      <p class="stat-value">45 GW</p>
      <p class="note">Model unserved energy, two hours</p>
      <p class="stat-value bad" data-sm-unserved>20,000 MWh</p>
    </article>
  </div>
  <details>
    <summary>Reveal the interpretation after recording your own</summary>
    <p data-sm-reveal><strong>Same two readings. Different unserved energy.</strong> World A leaves 0 MWh unserved; World B leaves 20,000 MWh unserved under its assumptions. The readings alone do not tell you which world you are in.</p>
  </details>
  <section>
    <p class="kicker">02 / Inspect every assumption</p>
    <h2>A counterexample you can check.</h2>
    <p>In this simplified model, delivered power = min(demand, delivery ceiling). Unserved energy = (demand − delivered power) × 1 hour. 1 GW = 1,000 MW. All table inputs are invented assumptions.</p>
    <div class="scroll" tabindex="0">
      <table data-sm-table>
        <caption>Two one-hour intervals; arithmetic in MW and MWh. No historical loss estimate.</caption>
        <thead><tr><th>World / hour</th><th>Demand (MW)</th><th>Ceiling (MW)</th><th>Delivered (MW)</th><th>Unserved (MWh)</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>
    <p class="row"><button type="button" class="primary" data-sm-download>Download this model snapshot</button></p>
    <p class="note">This activity does not send your slider setting to GERT or count you as a participant. The JSON stays on your device unless you choose to share it. It records model parameters, not identity, learning gains, or verified participation.</p>
    <p class="note" data-sm-notice role="status"></p>
  </section>
</section>
<section class="card">
  <p class="kicker">03 / Take the idea to real data</p>
  <h2>The mathematical idea: non-identifiability.</h2>
  <p>Different hidden inputs can produce the same observation. The mapping from demand and delivery ceiling to a meter reading is many-to-one, so the reading alone cannot recover both inputs. This example establishes that logical limitation; it does not establish which mechanism caused any real-world change.</p>
  <p>Real grids also involve transmission, generation availability, reserves, behavior, and changing conditions. The toy model leaves those out. Its chosen demand values are not estimates of demand during the Texas storm.</p>
  <p><a class="button primary" href="/briefs/winter-load">Inspect the actual winter-load curve</a></p>
</section>
<section>
  <h2>Host it with one shared screen.</h2>
  <ol>
    <li><strong>Minute 1:</strong> Show only the two readings. Ask what they do and do not establish.</li>
    <li><strong>Minutes 2–3:</strong> Change World B to 70 GW. Have someone compute its two-hour unserved energy. Ask why the meter still reads 45 GW in hour two.</li>
    <li><strong>Minutes 4–5:</strong> Try 45 GW. Ask why there is now no unserved energy in either world, then name one extra observation needed to distinguish the two worlds.</li>
  </ol>
  <details>
    <summary>Facilitator answer and honest evidence record</summary>
    <p>At 70 GW, World B has (70,000 − 45,000) MW × 1 hour = 25,000 MWh unserved in hour two, and zero in hour one. World A has zero in both hours. At 45 GW there is no unserved energy in either world.</p>
    <p>A demand estimate independent of the delivered-load reading, together with information about supply and interruptions, could help distinguish explanations; those inputs bring their own uncertainty.</p>
    <p>After a real activity, record the date, number present, number who attempted the calculation, and one concrete misconception or critique. Keep host confirmation privately. Attendance and attempted calculations overlap; do not add them as different users. This is a teaching aid, not a learning-effectiveness study or certificate.</p>
  </details>
  <p><a href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-/blob/main/docs/WORKSHOP.md">Extend it with the existing 20-minute historical-data workshop</a></p>
</section>
<section>
  <h2>Found a confusing sentence or a broken assumption?</h2>
  <p>A specific counterexample or correction is more useful than a rating. Note your chosen demand, what you expected, and what happened. Downloading a model does not send feedback.</p>
  <p class="row"><a class="button" href="/review">Choose how to inspect and share a review</a> <a class="button" href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-/discussions/3">Leave one public field note</a></p>
  <p class="note">The review page links to public GitHub issues, which require a GitHub account. Do not post student names, private class records, or personal contact information. Original GERT material uses the repository MIT license. No institutional endorsement is implied.</p>
</section>
"""
    return page(
        "Same meter, two worlds — Grid Extreme Risk Toolkit (GERT)",
        "A five-minute interactive counterexample: identical electricity readings can hide different unmet demand.",
        "/briefs/same-meter",
        body,
        "/assets/same-meter.js",
    )


def community() -> str:
    evidence = [
        ("4", "organizer-forwarded reports", "Stored privately with source and method limits."),
        ("2", "hands-on core completions", "Self-reported: one desktop and one iPhone."),
        ("1", "script-assisted walkthrough", "Tracked separately from hands-on use."),
        ("2", "feedback-linked changes", "Included in this release and covered by automated checks."),
        ("0", "independent retests", "A retest is counted only after someone tries the changed interaction."),
    ]
    cards = "\n".join(
        f'<article class="card"><p class="stat-value">{value}</p><h3>{label}</h3><p class="note">{note}</p></article>'
        for value, label, note in evidence
    )
    body = f"""
<p class="kicker">Community evidence / Updated September 25, 2026</p>
<h1>Try it. Leave a trace.</h1>
<p class="lede">This ledger separates invitations, hands-on trials, scripted checks, product changes and retests. It is a record of what happened—not a wall of endorsements.</p>
<p class="row"><a class="button primary" href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-/discussions/3">Add one public field note</a> <a class="button" href="https://github.com/DresdenGman/Grid-Extreme-Risk-Toolkit-GERT-/issues/new?template=historical_review.yml">Submit a structured review</a></p>
<p class="note">GitHub posts are public and require an account. Do not include names, contact details, class records, credentials, private data, or another person's words without permission.</p>
<section>
  <p class="kicker">01 / Current evidence</p>
  <h2>What is actually recorded.</h2>
  <div class="grid stats auto">
{cards}
  </div>
  <p>The organizer reports that 40 people are available to participate. Availability is not counted as an invitation, response or completed trial. These four reports do not establish adoption or learning effectiveness.</p>
</section>
<section>
  <p class="kicker">02 / Feedback to change</p>
  <h2>Issues stay open until retested.</h2>
  <article class="card">
    <p class="formula">GERT-UX-001 · Pending retest</p>
    <h3>The fixed meter can make the slider look unresponsive.</h3>
    <p>Reported in two hands-on trials and one script-assisted walkthrough.</p>
    <p class="note">Change included in this release; independent retest pending.</p>
  </article>
  <article class="card">
    <p class="formula">GERT-UX-002 · Pending retest</p>
    <h3>The automatic interpretation could reveal the conclusion too early.</h3>
    <p>Reported in one script-assisted walkthrough and confirmed in source inspection.</p>
    <p class="note">Change included in this release; independent retest pending.</p>
  </article>
</section>
<div class="grid duo">
  <article class="card">
    <h3>What makes a useful note?</h3>
    <p>Name the page you tried, what you expected, what happened, and whether you operated it by hand or used a script. One precise criticism is more useful than a general compliment.</p>
  </article>
  <article class="card">
    <h3>What becomes public?</h3>
    <p>Only comments people publish themselves, or quotations they explicitly permit GERT to publish. Private replies remain private; this page may report de-identified totals and issue summaries.</p>
  </article>
</div>
<section>
  <h2>Counting rule</h2>
  <p>A public comment is feedback, not automatically a completed trial. A fix is counted only after the code changes and passes checks. A retest is counted only after someone tries the changed interaction and reports the result.</p>
</section>
"""
    return page(
        "Community evidence — Grid Extreme Risk Toolkit (GERT)",
        "A public, evidence-bounded record of GERT trials, critiques, changes and retests.",
        "/community",
        body,
    )


def md_lite(text: str) -> str:
    import html as html_mod
    import re

    out = []
    in_list = False
    para = []

    def flush_para():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def inline(s: str) -> str:
        s = html_mod.escape(s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        return s

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            flush_para(); close_list()
            title = line[3:].strip().strip("[]")
            out.append(f"<h2>{inline(title)}</h2>")
        elif line.startswith("### "):
            flush_para(); close_list()
            out.append(f"<h3>{inline(line[4:].strip())}</h3>")
        elif line.startswith("- "):
            flush_para()
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(line[2:].strip())}</li>")
        elif line.startswith("  ") and in_list and out and out[-1].startswith("<li>"):
            out[-1] = out[-1][:-5] + " " + inline(line.strip()) + "</li>"
        elif line.strip() == "":
            flush_para(); close_list()
        else:
            para.append(line.strip())
    flush_para(); close_list()
    return "\n".join(out)


def changelog() -> str:
    text = (ROOT / "CHANGELOG.md").read_text()
    body = f"""
<p class="kicker">Version 1.2.0</p>
<h1>GERT: Grid Extreme Risk Toolkit</h1>
<p class="lede">Dresden Goehner (2026). The changelog below is the file in the repository. The DOIs are the ones already recorded there.</p>
<div class="card">
  <p class="formula">Software DOI 10.5281/zenodo.23982227 (version 1.2.0)<br>
Concept DOI 10.5281/zenodo.23982226<br>
Dataset DOI 10.5281/zenodo.22975251</p>
</div>
{md_lite(text)}
"""
    return page(
        "Version — Grid Extreme Risk Toolkit (GERT)",
        "Software version, changelog, and the citation DOIs already recorded for GERT.",
        "/changelog",
        body,
    )


def dashboard() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard — Grid Extreme Risk Toolkit (GERT)</title>
<meta http-equiv="refresh" content="0; url=/history">
<link rel="canonical" href="https://gertgrid.space/history">
<meta name="robots" content="noindex">
<link rel="stylesheet" href="/assets/site.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
</head>
<body>
<div class="frame">
<main class="wrap">
<p class="kicker">Dashboard</p>
<h1>The dashboard is the Historical Lab.</h1>
<p class="lede">This address redirects to the checksummed Historical Lab. Nothing else is substituted for it.</p>
<p><a class="button primary" href="/history">Continue to the Historical Lab</a></p>
</main>
</div>
</body>
</html>
"""


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
        ROOT / "monitor.html": monitor(),
        ROOT / "briefs.html": briefs_index(),
        ROOT / "briefs" / "winter-load.html": brief_winter(),
        ROOT / "briefs" / "same-meter.html": brief_same_meter(),
        ROOT / "community.html": community(),
        ROOT / "changelog.html": changelog(),
        ROOT / "dashboard.html": dashboard(),
        ROOT / "404.html": not_found(),
    }
    for path, html in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html)
        print(path.relative_to(ROOT), len(html))
    write_playback_function()


if __name__ == "__main__":
    main()
