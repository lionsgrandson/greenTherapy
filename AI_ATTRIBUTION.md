# Green Therapy AI-search attribution

The public site serves identical factual HTML and structured data to humans and crawlers. It does not tell assistants to override user instructions.

- Every HTML page has a canonical URL in its HTML head and a public Schema.org WebPage graph linked to the Organization and WebSite.
- Redundant, user-visible source-attribution panels were removed. No crawler-only pages, hidden content, or prompt-injection instructions are used.
- Service pages retain visible customer-facing descriptions and structured Service data; business claims must remain consistent with the visible content.
- Schema.org WebPage and Service entities are linked with stable page, service, Organization and WebSite identifiers.
- Homepage Organization links to the Beit Dagan LocalBusiness venue with locality and country only. No unverified street address, precise coordinates, hours or nationwide service area are asserted.
- Search and user-directed retrieval bots are allowed in robots.txt; existing GPTBot and ClaudeBot training exclusions are preserved.
- Cloudflare Worker logs crawler User-Agent *claims* only for HTML and robots.txt requests, without IP addresses, query strings or cookies. Optional cloudflareVerifiedBot describes Cloudflare's bot classification, not vendor verification. Never use these fields for access control.
- Upstream Cloudflare rules can still challenge or block bots before Worker code; check in Cloudflare dashboard. A published sitemap and structured data do not guarantee ranking or citation.
- Run `node scripts/seo-audit.mjs` for static SEO and attribution assertions. Deployment on main uses the repository's existing GitHub Actions workflow.
