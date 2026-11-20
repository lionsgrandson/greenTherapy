import {readdirSync,readFileSync,existsSync} from "node:fs";
import assert from "node:assert/strict";
const site="https://greentherapy.co.il";
const pages=readdirSync(".").filter(f=>f.endsWith(".html"));
const sitemap=[...readFileSync("sitemap.xml","utf8").matchAll(/<loc>([^<]+)<\/loc>/g)].map(m=>m[1]);
assert.equal(sitemap.length,pages.length);
assert.equal(new Set(sitemap).size,pages.length);
for(const p of pages){
 const html=readFileSync(p,"utf8"),url=site+"/"+(p==="index.html"?"":p);
 assert(html.includes(url),p+" missing canonical URL");
 assert(!html.includes("green-therapy.netlify.app"),p+" old host");
 assert.equal((html.match(/<h1\b/g)||[]).length,1,p+" has incorrect H1 count");
 assert(html.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/)?.[1].replace(/<[^>]*>/g,"").trim(),p+" blank static H1");
 assert(/<title>[^<]+<\/title>/.test(html),p+" missing title");
 assert(/name="description"/.test(html),p+" missing description");
 for(const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g))assert.equal(JSON.parse(m[1])["@context"],"https://schema.org");
 for(const m of html.matchAll(/\bhref="([^"]+)"/g)){
   const link=m[1];
   if(/^(https?:|tel:|mailto:|#|javascript:|\/)/.test(link))continue;
   assert(existsSync(link.split(/[?#]/)[0]),p+" missing local target "+link);
 }
 assert(sitemap.includes(url),p+" omitted from sitemap");
}
assert(!sitemap.some(v=>v.includes("?lang=en")),"Client-rendered English variants must not be in sitemap");
assert(readFileSync("robots.txt","utf8").includes("Sitemap: "+site+"/sitemap.xml"));
console.log("Green Therapy static SEO audit passed:",pages.length,"pages");