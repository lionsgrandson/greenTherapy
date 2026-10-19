// Cloudflare Workers entry point for the static Green Therapy website.
const SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
  "X-Frame-Options": "SAMEORIGIN",
};

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
    return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
  },
};
