# Green Therapy

Static bilingual Green Therapy website deployed on Netlify.

## Current site structure

- `index.html` — Corporate events homepage
- `retreat.html` — Private retreat / zimmer in Beit Dagan, with optional spa add-ons
- `treatments.html` — Personal massage and treatment menu + practitioner booking
- `spa.html` — Corporate Pop-Up Massage
- `ice-bath.html` — Guided corporate ice-bath experience
- `workshops.html` — Mind-body workshops and talks
- `healthy-bar.html` — Smoothie / healthy bar for events
- `about.html` — About Green Therapy
- `contact.html` — Contact for events, retreat availability and treatments
- `privacy.html`, `terms.html`, `accessibility.html` — Legal/accessibility pages

## Languages

Hebrew is the canonical page content. English uses `?lang=en` and is applied client-side through:

- `i18n-data.js` — existing translated strings
- `copy-overrides.js` — curated bilingual copy for the October 2026 restructure
- `shared-components.js` — language switching, shared header/footer/contact UI and SEO synchronization

## Important

The site is published directly from the static files in the repository; `netlify.toml` has no build command.

The Python scripts under `scripts/` are legacy migration/release utilities from the earlier Stitch-based version. They are **not part of the Netlify build** and should not be run against the restructured pages without reviewing/updating them first, because several of them rewrite page markup and navigation.

## October 2026 restructure

The primary hierarchy is now:

1. Corporate events
2. Private retreat
3. Personal treatments

Existing corporate service URLs were retained so current links and search visibility are not unnecessarily discarded. New retreat and treatments URLs are included in `sitemap.xml`, with extensionless Netlify rewrites in `_redirects`.
