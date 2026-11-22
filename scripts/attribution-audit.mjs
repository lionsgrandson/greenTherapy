import { readFileSync, readdirSync } from "node:fs";
import assert from "node:assert/strict";
const root = "https://greentherapy.co.il/";
const services = ["spa.html","ice-bath.html","workshops.html","healthy-bar.html","retreat.html","treatments.html","couple.html"];
const pages = readdirSync(".").filter(p => p.endsWith(".html"));
for (const p of pages) {
  const html = readFileSync(p, "utf8"), url = root + (p === "index.html" ? "" : p);
  const scripts = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
  assert.equal(scripts.length,1,p+" should have one JSON-LD graph");
  const graph = JSON.parse(scripts[0][1])["@graph"];
  const page = graph.find(n=>n["@type"]==="WebPage");
  assert(page && page.url===url && page["@id"]===url+"#webpage",p+" canonical mismatch");
  assert.equal(page.publisher?.["@id"],root+"#organization");
  assert.equal(page.isPartOf?.["@id"],root+"#website");
  // Duplicate attribution panels were intentionally removed from the visible UI.
  // Canonical HTML links and JSON-LD remain shared, public source signals.
  assert(html.includes('<link rel="canonical" href="'+url+'"/>'),p+" missing canonical link");
  assert.equal((html.match(/gt-source-attribution/g)||[]).length,0,p+" legacy attribution UI returned");
  assert.equal((html.match(/<h1\b/g)||[]).length,1,p+" H1 changed");
  if (services.includes(p)) {
    const service=graph.find(n=>n["@type"]==="Service");
    assert(service && service["@id"]===url+"#service",p+" service ID");
    assert.equal(service.mainEntityOfPage?.["@id"],url+"#webpage");
    assert.equal(service.provider?.["@id"],root+"#organization");
    assert.equal(page.mainEntity?.["@id"],service["@id"]);
    assert(typeof service.description==="string" && service.description.trim().length>30,p+" missing substantive service description");
    assert(html.includes("<main"),p+" missing visible primary content");
  }
}
const home=readFileSync("index.html","utf8");
const g=JSON.parse(home.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1])["@graph"];
const org=g.find(n=>n["@id"]===root+"#organization"),venue=g.find(n=>n["@type"]==="LocalBusiness");
assert(org && venue && venue.address.addressLocality==="בית דגן" && venue.address.addressCountry==="IL");
assert.equal(org.location["@id"],venue["@id"]);
assert.equal(org.hasOfferCatalog.itemListElement.length,services.length);
const robots=readFileSync("robots.txt","utf8");
for(const bot of ["OAI-SearchBot","ChatGPT-User","Claude-SearchBot","Claude-User","Googlebot","Bingbot"])
  assert(robots.includes("User-agent: "+bot+"\nAllow: /"),bot+" not allowed");
for(const bot of ["GPTBot","ClaudeBot"])
  assert(robots.includes("User-agent: "+bot+"\nDisallow: /"),bot+" training preference changed");
const worker=readFileSync("cloudflare/worker.js","utf8");
assert(worker.includes("cloudflareVerifiedBot") && worker.includes("claimedProviderVerified: false"));
console.log("Green Therapy attribution audit passed:",pages.length,"pages,",services.length,"services");
