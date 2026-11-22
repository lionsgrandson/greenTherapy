import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";

const files=readdirSync(".").filter(name=>name.endsWith(".html"));
const reviewPages=new Set(["index.html","treatments.html","workshops.html"]);
for(const file of files){
  const html=readFileSync(file,"utf8");
  assert(!/<(?:details|summary)\b/i.test(html),file+" still includes an accordion");
  assert(!/gt-photo-reviews|gt-review-sources|gt-review-photo-grid|gt-faq-item/.test(html),file+" contains an old review or FAQ panel");
  assert(!/assets\/gallery\/(?:workshop-review|corporate-event-review|garden-workshop-review)\.webp/.test(html),file+" still embeds review screenshots");
  assert(!/data-i18n="(?:faq-|couple-faq|couple-q\d+|couple-a\d+)/.test(html),file+" still includes Q&A content");
  assert(!/"FAQPage"/.test(html),file+" advertises an absent FAQ");
  if(!reviewPages.has(file)){
    assert(!html.includes("gt-testimonials-track"),file+" has an unexpected testimonial carousel");
    continue;
  }
  const start=html.indexOf('gt-testimonials-section');
  const end=html.indexOf("</section>",start);
  assert(start>=0 && end>start,file+" missing testimonial carousel");
  const section=html.slice(start,end);
  const cards=[...section.matchAll(/<article\b[^>]*>[\s\S]*?<\/article>/g)].map(m=>m[0]);
  assert.equal(cards.length,16,file+" must have eight cards duplicated for the endless loop");
  assert.deepEqual(cards.slice(0,8),cards.slice(8),file+" repeating cards must match exactly");
  assert(section.includes('class="gt-testimonials-set" aria-hidden="true"'),file+" duplicate must be hidden from assistive technology");
  assert(section.includes('data-i18n="index.html-t240"'),file+" missing translated review heading");
}
const css=readFileSync("production.css","utf8");
assert(css.includes("@keyframes gt-testimonials-right-to-left"),"missing marquee keyframes");
assert(css.includes("translate3d(-50%,0,0)"),"marquee must move from right to left");
assert(css.includes("@media(prefers-reduced-motion:reduce)"),"marquee must respect reduced motion");
const shared=readFileSync("shared-components.js","utf8");
assert(shared.includes("sharedReviews[key]"),"shared reviews must support English and Hebrew on all pages");
assert(!shared.includes("initFaq()"),"obsolete FAQ JS was not removed");
console.log("Green Therapy UX audit passed:",files.length,"pages,",reviewPages.size,"continuous testimonial carousels");
