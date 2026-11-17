const PAGES = new Set([
  "/",
  "/index.html",
  "/about",
  "/about.html",
  "/benchmark",
  "/benchmark.html",
  "/research",
  "/research.html",
  "/scenario",
  "/scenario.html",
  "/history",
  "/history.html",
  "/review",
  "/review.html",
  "/events/polar-vortex",
  "/events/polar-vortex.html",
  "/404.html",
  "/robots.txt",
  "/sitemap.xml",
  "/favicon.ico",
  "/favicon.svg",
  "/og.png",
]);

const NOT_FOUND = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found — Grid Extreme Risk Toolkit (GERT)</title>
<link rel="stylesheet" href="/assets/site.css">
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
</html>`;

export async function onRequest(context) {
  const url = new URL(context.request.url);
  let path = url.pathname;
  if (path.length > 1 && path.endsWith("/")) path = path.slice(0, -1);

  if (path === "/lab" || path === "/lab.html") {
    return Response.redirect(new URL("/history", url.origin), 302);
  }

  if (
    path.startsWith("/api/")
    || path.startsWith("/assets/")
    || path.startsWith("/data/")
    || PAGES.has(path)
  ) {
    return context.next();
  }

  return new Response(NOT_FOUND, {
    status: 404,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
      "x-robots-tag": "noindex",
    },
  });
}
