# Green Therapy deployment checklist

## Google Analytics
Set window.GREEN_THERAPY_CONFIG.googleAnalyticsId in site-config.js. Analytics remains dormant until an ID exists and the visitor grants consent.

## Google Search Console
Replace GT_SEARCH_CONSOLE_VERIFICATION in the generated meta tag with the verification token and redeploy. Submit /sitemap.xml after verification.

## Contact backend
Set CONTACT_WEBHOOK_URL in Netlify environment variables to the approved CRM/email automation endpoint. Until then, forms clearly direct visitors to email instead of showing a false success.

## Custom domain
When a custom domain is connected, update BASE_URL in scripts/production_release.py and regenerate canonical, hreflang, sitemap and robots values.
