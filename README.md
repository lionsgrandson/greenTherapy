# Green Therapy — Corporate Wellness static site

Pure HTML/CSS/vanilla JS implementation of the Green Therapy B2B website, based on the Stitch design direction and the `Nature's Warmth` design system.

## Pages
- `index.html` — corporate homepage
- `spa.html` — Corporate Pop-Up Spa
- `ice-bath.html` — Peak Energy / ice baths
- `workshops.html` — mind-body workshops & keynotes
- `healthy-bar.html` — healthy bar & superfood
- `about.html` — about Green Therapy
- `gallery.html` — filterable editorial gallery
- `contact.html` — multi-step event brief

## Shared files
- `styles.css` — full responsive design system and page styles
- `script.js` — mobile navigation, reveal animation, gallery filters, WhatsApp routing and the static multi-step form interaction

## Before production launch
1. Set `WHATSAPP_NUMBER` at the top of `script.js` to the verified business number in international digits-only format.
2. Connect the event brief form to the CRM/email endpoint. It intentionally does not transmit data yet because this repository is currently the static design layer.
3. Confirm public contact details before replacing the current email address.
4. Replace any Stitch-hosted image URL with final compressed WebP assets when the approved original media set is ready.
5. Reconfirm marketing proof points (500+ events, 15,000+ participants, 99% HR satisfaction) before production publication.

## Local preview
Open `index.html` directly or run any static server, for example:

```bash
python -m http.server 8080
```
