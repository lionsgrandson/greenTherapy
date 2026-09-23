#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import re, json

ROOT=Path(__file__).resolve().parents[1]
HE=["index.html","spa.html","ice-bath.html","workshops.html","healthy-bar.html","about.html","contact.html"]
EN=[f"en/{p}" for p in HE]
ALL=HE+EN
PHONE="+972 53-532-4962"
TEL="+972535324962"

EN_REPL={
 "Opening and explanation of the course of the experience and the important highlights before baptism.":"A clear briefing on the experience and the key points before entering the ice bath.",
 "Guided preparation for baptism, depending on the structure of the activity and the group.":"Guided preparation before entering the ice bath, adapted to the group and activity format.",
 "Full 360° production envelope - we take care of all the details":"Complete 360° production — we take care of the details",
 "Peace of mind (full production envelope): we take care of all the equipment, the setting, the logistics and the operation.":"Peace of mind: we take care of the equipment, setup, logistics and on-site operation.",
 "Full production envelope":"Complete production",
 "quiet head":"Peace of Mind",
 "Equipment, decor and meticulous visibility as part of a professional and inviting experience.":"Equipment, styling and a polished presentation as part of a professional and welcoming experience.",
 "High service standard: human relations, representativeness, meticulous visibility and uncompromising professionalism.":"High service standards: warm interpersonal service, polished presentation and professional delivery.",
 "Receiving a personalized offer for your event":"Get a Tailored Proposal",
 "Receiving an offer adapted to the organization":"Get a Tailored Proposal",
 "Share with us the nature of the event, the budget and the number of participants and we will build together the appropriate menu of workshops and experiences.":"Tell us about your event, budget and participant count, and we’ll build the right mix of workshops and experiences.",
 "The compound production process in 3 simple steps":"How the Pop-Up Spa Comes Together",
 "complete envelope":"complete service",
}
def text_replace(soup,m):
  for n in list(soup.find_all(string=True)):
    if not isinstance(n,NavigableString) or (n.parent and n.parent.name in {"script","style"}):continue
    s=str(n);t=s
    for a,b in m.items():t=t.replace(a,b)
    if t!=s:n.replace_with(t)

def first_hero(soup):
  main=soup.find("main")
  if main:
    sec=main.find("section")
    if sec:return sec
  h=soup.find("header")
  if h:
    n=h.find_next("section")
    if n:return n
  return soup.find("section")

def simplify_hero(soup,en,page):
  hero=first_hero(soup)
  if not hero:return
  # Simple page-specific headlines while preserving the Stitch hero composition.
  h1=hero.find("h1")
  if h1:
    if page=="spa.html": h1.string="Pop-Up Spa for Corporate Events" if en else "מתחם ספא פופ-אפ לאירועי חברה"
    elif page=="ice-bath.html": h1.string="Ice Bath Experience for Corporate Events" if en else "חוויית אמבטיות קרח לאירועי חברה"
  # Remove metric/trust micro-badges and icon rows from service heroes.
  for d in list(hero.find_all("div")):
    if not d.parent:continue
    cls=" ".join(d.get("class",[]))
    txt=" ".join(d.get_text(" ",strip=True).split())
    if not txt:continue
    in_link=bool(d.find_parent(["a","button"]))
    if in_link:continue
    remove=False
    if "grid-cols-3" in cls and len(txt)<220: remove=True
    if "border-t" in cls and ("flex" in cls or "grid" in cls) and len(txt)<220: remove=True
    if ("items-center" in cls and "gap-2" in cls) and len(txt)<95 and d.find("span",class_=lambda c:c and "material-symbols-outlined" in c if isinstance(c,str) else False): remove=True
    if "absolute bottom-" in cls and len(txt)<180: remove=True
    if remove:d.decompose()
  # Also remove standalone small trust line under CTAs.
  for d in list(hero.find_all("div")):
    if not d.parent:continue
    cls=" ".join(d.get("class",[]));txt=d.get_text(" ",strip=True)
    if "font-label-sm" in str(d) and len(txt)<100 and d.find("span",class_=lambda c:c and "material-symbols-outlined" in c if isinstance(c,str) else False):
      if not d.find("a") and d.name=="div": d.decompose()

def fix_three_card_sections(soup,en):
  headings=[
    "חוויית שיא שמחברת","מעטפת הפקה מלאה 360","חוויה מודרכת, מקצועית ומעצימה",
    "Peak Experience","Complete 360","Full 360","Guided, professional","Guided, Professional"
  ]
  for needle in headings:
    n=soup.find(string=lambda s:s and needle.lower() in str(s).lower())
    if not n:continue
    sec=n.parent
    while sec and sec.name!="section":sec=sec.parent
    if not sec:continue
    grids=[g for g in sec.find_all("div") if "grid" in g.get("class",[])]
    if not grids:continue
    grid=grids[-1] if ("מודרכת" in needle or "Guided" in needle) else grids[0]
    cls=[]
    for x in grid.get("class",[]):
      if re.match(r"(?:(?:sm|md|lg):)?grid-cols-",x):continue
      if x=="relative":continue
      if x=="gap-8":continue
      cls.append(x)
    grid["class"]=list(dict.fromkeys(cls+["grid-cols-1","md:grid-cols-3","gap-6","max-w-5xl","mx-auto"]))
    for child in grid.find_all("div",recursive=False):
      child["class"]=[x for x in child.get("class",[]) if not re.match(r"(?:(?:sm|md|lg):)?col-span-",x)]
    if "מודרכת" in needle or "Guided" in needle:
      for d in list(grid.find_all("div")):
        if d.get_text(strip=True) in {"1","2","3","4"} and "rounded-full" in " ".join(d.get("class",[])): d.decompose()

def fix_contact_sidebar(soup,en):
  # Direct contact card: phone must be the primary direct channel.
  call=soup.find("span",class_=lambda c:c and "material-symbols-outlined" in c if isinstance(c,str) else False,string=lambda s:s and str(s).strip()=="call")
  if call:
    li=call.find_parent("li")
    if li:
      label=li.find("span",class_=lambda c:c and "font-label-sm" in c if isinstance(c,str) else False)
      a=li.find("a")
      if label:label.string="Phone" if en else "טלפון"
      if a:
        a["href"]="tel:"+TEL;a["dir"]="ltr";a.string=PHONE
  text_replace(soup,{
    "דרך הטופס או המייל":"דרך הטופס או הטלפון",
    "through the form or email":"through the form or phone",
    "To contact Green Therapy directly:":"For direct contact with Green Therapy:",
  })
  # Any visible phone number gets bidi isolation.
  for a in soup.find_all("a",href=re.compile(r"^tel:")):
    a["dir"]="ltr"

def fix_en_meta(soup,page):
  slug="" if page=="index.html" else page
  enurl="https://green-therapy.netlify.app/en/"+slug
  heurl="https://green-therapy.netlify.app/"+slug
  can=soup.find("link",rel="canonical")
  if can:can["href"]=enurl
  for l in soup.find_all("link",rel="alternate"):
    lang=l.get("hreflang")
    if lang=="en":l["href"]=enurl
    elif lang in {"he","x-default"}:l["href"]=heurl
  og=soup.find("meta",attrs={"property":"og:url"})
  if og:og["content"]=enurl
  for sc in soup.find_all("script",attrs={"src":True}):
    if sc.get("src")=="site-config.js":sc["src"]="../site-config.js"
  for l in soup.find_all("link",attrs={"href":True}):
    if l.get("href")=="production.css":l["href"]="../production.css"
  desc="Green Therapy creates corporate Wellness & Wellbeing experiences including Pop-Up Spa, ice baths, Mind & Body workshops and a Healthy Bar, tailored to each event."
  md=soup.find("meta",attrs={"name":"description"})
  if md:md["content"]=desc
  for tag in soup.find_all("script",attrs={"type":"application/ld+json"}):
    try:
      data=json.loads(tag.string or "{}")
      if isinstance(data,dict) and data.get("@type")=="Organization":
        data["description"]=desc;tag.string=json.dumps(data,ensure_ascii=False)
    except:pass

def process(path):
  en=path.startswith("en/");page=Path(path).name
  f=ROOT/path;soup=BeautifulSoup(f.read_text(encoding="utf-8"),"html.parser")
  if en:
    text_replace(soup,EN_REPL);fix_en_meta(soup,page)
  simplify_hero(soup,en,page)
  if page=="ice-bath.html":fix_three_card_sections(soup,en)
  if page=="contact.html":fix_contact_sidebar(soup,en)
  f.write_text(str(soup),encoding="utf-8")

for p in ALL:process(p)

# Stronger text-size constraints without changing the Stitch visual language.
css=ROOT/"production.css"
s=css.read_text(encoding="utf-8")
s += r'''
/* Fine typography pass */
@media(min-width:768px){
  main h1{font-size:clamp(2.45rem,4.4vw,3.55rem)!important;line-height:1.08!important;max-width:100%!important}
  main h2{font-size:clamp(1.9rem,3vw,2.65rem)!important;line-height:1.14!important}
  main h3{line-height:1.2!important}
}
main p{overflow-wrap:break-word}.gt-header-phone bdi,.gt-mobile-phone bdi,.gt-footer-contact bdi{direction:ltr;unicode-bidi:isolate}
'''
css.write_text(s,encoding="utf-8")
print("stitch polish v2 complete")
