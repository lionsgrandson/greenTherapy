# Green Therapy

Static bilingual Green Therapy website deployed to Cloudflare Workers and mirrored on Netlify.

## Current site structure

- `index.html` — Corporate events homepage
- `retreat.html` — Event venue / event venue in Beit Dagan, with optional spa add-ons
- `treatments.html` — Personal massage and treatment menu + practitioner booking
- `spa.html` — Corporate Pop-Up Massage
- `ice-bath.html` — Guided corporate ice-bath experience
- `workshops.html` — Mind-body workshops and talks
- `healthy-bar.html` — Smoothie / healthy bar for events
- `about.html` — About Green Therapy
- `contact.html` — Contact for events, event venue availability and treatments
- `privacy.html`, `terms.html`, `accessibility.html` — Legal/accessibility pages

## Languages

Hebrew is the canonical page content. English uses `?lang=en` and is applied client-side through:

- `i18n-data.js` — existing translated strings
- `copy-overrides.js` — curated bilingual copy for the October 2026 restructure
- `shared-components.js` — language switching, shared header/footer/contact UI and SEO synchronization

## Important

The site is published directly from the static files in the repository; `netlify.toml` has no build command.

The Python scripts under `scripts/` are legacy migration/release utilities from the earlier Stitch-based version. They are **not part of the Netlify build** and should not be run against the restructured pages without reviewing/updating them first, because several of them rewrite page markup and navigation.

## Supplied photography

Website copies of selected photos and public review screenshots from `images/` live in `assets/gallery/`. Originals remain untouched. `assets/gallery/manifest.json` records each source and its output dimensions. Run `python scripts/prepare_site_images.py` (requires Pillow) to regenerate these WebP copies; this utility does not rewrite pages.

Photos are placed by subject across the homepage, spa, workshops, personal treatments, retreat workshop, about, and contact pages. Reviews remain in their original Hebrew in expandable sections. Private WhatsApp conversations are not used in these sections.

## October 2026 restructure

The primary hierarchy is now:

1. Corporate events
2. Private retreat
3. Personal treatments

Existing corporate service URLs were retained so current links and search visibility are not unnecessarily discarded. New retreat and treatments URLs are included in `sitemap.xml`, with extensionless Netlify rewrites in `_redirects`.

## Contact form (EmailJS)

The shared bilingual contact form in `shared-components.js` sends directly from the browser to the EmailJS REST API. The configured public key is `dh2O2Nh2z42DJGLUB`, template is `template_suj8dvg`, and service alias is `primary_service` (the default connected service in EmailJS). No private API key is stored in the repository. This integration replaces the earlier homepage POST used for Netlify Forms, which Cloudflare Workers did not handle.

**Before accepting leads:** configure a connected email service as the **default** in the EmailJS dashboard, set the Contact Us template recipient (Green Therapy's inbox), and verify that the template variables `{{name}}`, `{{phone}}`, `{{email}}`, `{{message}}` match the EmailJS template. The form also provides `from_name`, `from_email`, `reply_to`, `page_url`, and `language`. If the default-service alias is unavailable, replace `primary_service` with the exact EmailJS `service_...` ID. Add `greentherapy.co.il` to the allowed origins/domains in EmailJS and enable appropriate spam controls. Do not put a private key into frontend files.

Test with a real browser submission after deployment. Only an HTTP success response from EmailJS produces the success message; it confirms the API accepted the request, not that a message necessarily arrived in the recipient inbox. Network/HTTP errors, rate limiting and a 20-second timeout show localized feedback, keep form data intact, and offer a user-initiated WhatsApp link prefilled with the inquiry. A timeout has uncertain delivery status, so the UI warns that the email may already have been sent. The Cloudflare Worker remains GET/HEAD-only and is not used for form delivery.

## Customer review screenshots

The homepage review grid includes verbatim text from the three public review screenshots in `assets/gallery/`. The original images remain accessible in a collapsed disclosure below the text reviews. A cropped testimonial has no invented author or rating; testimonial text is not to be treated as independent proof of health outcomes.
