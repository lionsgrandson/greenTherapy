# Green Therapy SEO implementation — 20 November 2026

## VERIFIED
- KNP Marketing's public keyword-focused /digital-expert/ page has prominent headings, detailed copy, testimonials, examples and consultation CTAs. Its claimed top-ranking positions and their causes are **not independently verified**.
- Green Therapy's code used green-therapy.netlify.app in canonical metadata, robots, sitemap and runtime SEO code.
- Event service pages had blank initial HTML headings and body copy filled by JS; the indexed /couple route returned 404.
- Corporate event services, private treatments, a couples' massage workshop and a Beit Dagan venue are described by Green Therapy.

## INFERRED / UNKNOWN
Intent-specific pages, crawler-readable explanations, real internal links and strong contact paths may improve discovery and qualified leads, but cannot guarantee rankings. Keyword search volume, competitors' backlinks, true positions, AI answers, Cloudflare bot blocking and actual GSC/GA4/Bing traffic are **unknown**.

## Target audiences
B2B: HR, office managers, event producers, welfare teams and company retreat organizers. B2C: adults seeking private massage, couples' workshops, wellness experiences and venue visits. Do not market specifically to families.

## Keyword intent -> canonical page
| Page | Primary intent |
| --- | --- |
| / | Green Therapy brand; corporate/private wellness overview |
| /spa.html | עמדות עיסוי לאירועים / עיסוי לעובדים |
| /ice-bath.html | אמבטיות קרח לאירועים |
| /workshops.html | סדנאות יוגה וגוף־נפש לאירועי חברה |
| /healthy-bar.html | בר שייקים לאירועים |
| /treatments.html | עיסוי בבית דגן, עיסוי שוודי |
| /retreat.html | מתחם אירועים וספא בבית דגן |
| /couple.html | סדנת עיסוי זוגי בבית דגן |

These are hypotheses based on service fit, not validated keyword volumes or rankings.

## Implemented
- Fixed source HTML and runtime canonical/OG domain and rebuilt canonical-only XML sitemap and robots.txt.
- Restored visible Hebrew text in previously empty static page elements.
- Added an original couples' workshop page and permanent /couple redirects.
- Added factual service FAQ sections, translated interface text, internal links and clearer intent-focused headings and titles.
- Added matching Organization, WebSite, WebPage and Service schema where relevant (no fabricated reviews, medical efficacy or credentials).
- Added social sharing images where available and WhatsApp paths for event-service CTAs.
- Tracked WhatsApp/phone/email **click intent** only with an existing configured gtag instance; no third-party service was installed.
- Added dependency-free static SEO check and GitHub Actions workflow. The original homepage hero, image overlay, styling and existing forms were not redesigned.

## Unresolved and client confirmation
1. The shared contact form is marked under construction and the Cloudflare Worker has no POST handler; WhatsApp and telephone are functioning alternatives, but form submission is not verified.
2. Confirm service-area boundaries, addresses, professional qualifications, venue details, schedules and treatment suitability before adding claims or location-specific pages.
3. Check HTTP redirects, live deployment, Core Web Vitals, mobile accessibility and Cloudflare bot defenses externally.
4. Connect verified GSC/Bing Webmaster/GA4 data for indexing, search queries, leads and conversions.
5. English is UI-translated by JavaScript, not server-rendered. The ?lang=en variant is no longer declared indexable/hreflang until genuine HTML locales are built.
6. Verify alternative domain / www redirects and whether Cloudflare exposes robots.txt as intended.

## Authority opportunities (not undertaken)
Request genuine links from event-production partners, actual client case studies with permissions, valid local directories, verified venue/practitioner profiles and relevant wellness editorial sources. Never purchase spam backlinks, invent endorsements or alter third-party listings without permission.

## 30/60/90-day measurements
**30 days:** Capture indexed URL coverage, impressions, clicks, queries, CTR, qualified B2B/B2C leads and click-intent data. Inspect canonical/301 status and sitemap submissions.
**60 days:** Review query-to-page matches, cannibalization, conversion quality and geographic landing-page demand based on verified first-party data.
**90 days:** Compare trends against baseline, optimize titles/CTAs, evaluate legitimate referral links and track measurable AI-search referrals if visible in analytics.

Technical tests prove only source checks. They do not prove actual rankings, rich results, or lead growth.

Official references: https://developers.google.com/search/docs/appearance/ai-features ; https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls ; https://developers.openai.com/api/docs/bots ; https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
