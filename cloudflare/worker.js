// Cloudflare Workers entry point for the static Green Therapy website.
const SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
  "X-Frame-Options": "SAMEORIGIN",
};

// Diagnostic-only User-Agent classification; never trust the claim for access control.
const CRAWLER_USER_AGENTS = [
  ["OAI-SearchBot", /\bOAI-SearchBot(?:\/[\d.]+)?\b/i],
  ["ChatGPT-User", /\bChatGPT-User(?:\/[\d.]+)?\b/i],
  ["Claude-SearchBot", /\bClaude-SearchBot(?:\/[\d.]+)?\b/i],
  ["Claude-User", /\bClaude-User(?:\/[\d.]+)?\b/i],
  ["Googlebot", /\bGooglebot(?:\/[\d.]+)?\b/i],
  ["Bingbot", /\bBingbot(?:\/[\d.]+)?\b/i]
];
function logCrawlerCandidate(request, path, status) {
  const ua = request.headers.get("user-agent") || "";
  const match = CRAWLER_USER_AGENTS.find(([, pattern]) => pattern.test(ua));
  if (!match || !(/\.html$/.test(path) || path === "/" || path === "/robots.txt")) return;
  // The Cloudflare verified-bot flag is plan-dependent and does not verify claimed vendor identity.
  const verified = request.cf?.botManagement?.verifiedBot;
  console.info("green_therapy_crawler", JSON.stringify({
    claimedCrawler: match[0], path, status,
    cloudflareVerifiedBot: typeof verified === "boolean" ? verified : null,
    claimedProviderVerified: false
  }));
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method Not Allowed", { status: 405, headers: { Allow: "GET, HEAD" } });
    }

    // Preserve Netlify language and legacy URL redirects.
    if (path === "/en" || path === "/en/" || path.startsWith("/en/")) {
      const destination = new URL(path.replace(/^\/en\/?/, "/") || "/", url.origin);
      destination.search = url.search;
      destination.searchParams.set("lang", "en");
      return Response.redirect(destination, 301);
    }
    if (path === "/couple" || path === "/couple/") {
      return Response.redirect(new URL("/couple.html", url.origin), 301);
    }
    if (path === "/gallery" || path === "/gallery.html") {
      return Response.redirect(new URL("/", url.origin), 301);
    }

    const rewrites = { "/retreat": "/retreat.html", "/treatments": "/treatments.html" };
    const target = new URL(request.url);
    // Wrangler's html_handling is "none", so explicitly map the domain root.
    // Without this, /index.html works but / can return an asset 404.
    if (path === "/") target.pathname = "/index.html";
    else if (rewrites[path]) target.pathname = rewrites[path];
    const response = await env.ASSETS.fetch(new Request(target, request));
    const headers = new Headers(response.headers);
    for (const [name, value] of Object.entries(SECURITY_HEADERS)) headers.set(name, value);
    logCrawlerCandidate(request, path, response.status);
    return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
  },
};
