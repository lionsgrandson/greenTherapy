#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from PIL import Image
import json, re, html as htmlmod

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://green-therapy.netlify.app"
HE_PAGES = ["index.html","spa.html","ice-bath.html","workshops.html","healthy-bar.html","about.html","gallery.html","contact.html"]
EN_PAGES = [f"en/{p}" for p in HE_PAGES]

# ---------- image preparation ----------
raw_dir = ROOT / "assets" / "client_raw"
client_dir = ROOT / "assets" / "client"
client_dir.mkdir(parents=True, exist_ok=True)
if raw_dir.exists():
    for src in raw_dir.glob("*"):
        if src.suffix.lower() not in {".jpg",".jpeg",".png",".webp"}: continue
        try:
            im = Image.open(src).convert("RGB")
            im.thumbnail((1600,1600), Image.Resampling.LANCZOS)
            out = client_dir / (src.stem + ".webp")
            im.save(out, "WEBP", quality=78, method=6)
        except Exception as exc:
            print("image skip", src, exc)
    for src in raw_dir.glob("*"):
        try: src.unlink()
        except: pass
    try: raw_dir.rmdir()
    except: pass

# Convert the first client batch already committed as JPEG.
for src in list(client_dir.glob("*.jpeg")) + list(client_dir.glob("*.jpg")):
    try:
        im = Image.open(src).convert("RGB")
        im.thumbnail((1600,1600), Image.Resampling.LANCZOS)
        out = src.with_suffix(".webp")
        im.save(out, "WEBP", quality=78, method=6)
    except Exception as exc:
        print("image conversion skip", src, exc)

PHOTO_SETS = {
    "index.html": ["887e1d9b-94c2-49aa-b3b9-258f57aacf3c.webp","1c3d140a-38a4-4aff-8196-9fea60c15ae3.webp","827ed1a7-ce8f-428f-91c1-20ac014453bf.webp","95941eaf-fc13-49b4-a515-c9d66f1fdb6e.webp","fe5e6cfc-8689-4287-8189-7286edf4bb30.webp"],
    "spa.html": ["887e1d9b-94c2-49aa-b3b9-258f57aacf3c.webp","1c3d140a-38a4-4aff-8196-9fea60c15ae3.webp","827ed1a7-ce8f-428f-91c1-20ac014453bf.webp","95941eaf-fc13-49b4-a515-c9d66f1fdb6e.webp","fe5e6cfc-8689-4287-8189-7286edf4bb30.webp"],
    "ice-bath.html": ["887e1d9b-94c2-49aa-b3b9-258f57aacf3c.webp","1c3d140a-38a4-4aff-8196-9fea60c15ae3.webp","827ed1a7-ce8f-428f-91c1-20ac014453bf.webp"],
    "workshops.html": ["1c3d140a-38a4-4aff-8196-9fea60c15ae3.webp","827ed1a7-ce8f-428f-91c1-20ac014453bf.webp","95941eaf-fc13-49b4-a515-c9d66f1fdb6e.webp"],
    "healthy-bar.html": ["95941eaf-fc13-49b4-a515-c9d66f1fdb6e.webp","fe5e6cfc-8689-4287-8189-7286edf4bb30.webp"],
    "about.html": ["887e1d9b-94c2-49aa-b3b9-258f57aacf3c.webp","1c3d140a-38a4-4aff-8196-9fea60c15ae3.webp"],
    "gallery.html": ["887e1d9b-94c2-49aa-b3b9-258f57aacf3c.webp","1c3d140a-38a4-4aff-8196-9fea60c15ae3.webp","827ed1a7-ce8f-428f-91c1-20ac014453bf.webp","95941eaf-fc13-49b4-a515-c9d66f1fdb6e.webp","fe5e6cfc-8689-4287-8189-7286edf4bb30.webp"],
    "contact.html": ["887e1d9b-94c2-49aa-b3b9-258f57aacf3c.webp","1c3d140a-38a4-4aff-8196-9fea60c15ae3.webp"],
}
TESTIMONIALS = []

HE_REPL = {
    "במשרדים, בטבע או בסיור החברה": "במשרד, בטבע או באתר האירוע",
    "במשרד, בטבע וב-Offsite": "במשרד, בטבע או באתר האירוע",
    "אירוע חברה / Offsite": "אירוע חברה / אתר אירוע",
    "שקט נפשי מלא למנהלות רווחה": "שקט נפשי לצוותי Wellbeing ו-HR",
    "מדוע מנהלות רווחה ומשאבי אנוש בוחרות בנו?": "למה צוותי Wellbeing ו-HR בוחרים בנו?",
    "מתחמי תוכן ורווחה בהתאמה אישית": "מתחמי Wellness & Wellbeing בהתאמה אישית",
    "ימי רווחה מותאמים אישית": "ימי Wellbeing מותאמים אישית",
    "שאלות נפוצות של מנהלות רווחה ומפיקים": "שאלות נפוצות לצוותי Wellbeing, HR והפקה",
    "מנהל/ת רווחה ו-HR": "Wellbeing / HR / Employee Experience",
    "Turnkey Solution": "מעטפת הפקה מלאה",
    "Turnkey": "מעטפת מלאה",
    "Restoring balance through nature.": "",
    "Green Therapy Beit Dagan": "Green Therapy",
    "ניהול חלק ללא עומסים": "תיאום טיפולים מסודר",
    "איך מתבצע ניהול התורים?": "איך מתאמים את זמני הטיפולים?",
}
EN_REPL = {
    "company tour": "company event",
    "Company Event / Offsite": "Company Event / Event Venue",
    "In the office, in nature and offsite": "In the office, outdoors or at your event venue",
    "Turnkey Solution": "Full-service production",
    "turnkey solution": "full-service production",
    "Turnkey": "Full-service production",
    "Restoring balance through nature.": "",
    "Green Therapy Beit Dagan": "Green Therapy",
    "How is queue management carried out?": "How are treatment times coordinated?",
    "Professional training": "Professional guidance",
}

def replace_text_nodes(soup, mapping):
    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString): continue
        if node.parent and node.parent.name in {"script","style"}: continue
        old = str(node)
        new = old
        for a,b in mapping.items():
            new = new.replace(a,b)
        if new != old:
            node.replace_with(new)

def nearest_card(tag):
    cur = tag
    while cur and getattr(cur, "name", None):
        cls = " ".join(cur.get("class", []))
        if cur.name == "div" and any(x in cls for x in ["rounded-2xl","rounded-3xl","rounded-xl"]):
            return cur
        cur = cur.parent
    return None

def remove_card_by_text(soup, phrases):
    for phrase in phrases:
        node = soup.find(string=lambda s: s and phrase in s)
        if node:
            card = nearest_card(node.parent)
            if card:
                card.decompose()

def insert_after_heading_section(soup, heading_text, new_html):
    node = soup.find(string=lambda s: s and heading_text in s)
    if not node: return False
    sec = node.parent
    while sec and sec.name != "section": sec = sec.parent
    if not sec: return False
    sec.insert_after(BeautifulSoup(new_html, "html.parser"))
    return True

def add_head_meta(soup, page, en=False):
    head = soup.head
    if not head: return
    # cleanup existing SEO tags we own
    for tag in list(head.find_all(["meta","link"])):
        if tag.name == "meta" and (tag.get("name") in {"description","robots","google-site-verification"} or tag.get("property","").startswith("og:") or tag.get("name","").startswith("twitter:")):
            tag.decompose()
        elif tag.name == "link" and tag.get("rel") and any(r in ["canonical","alternate"] for r in tag.get("rel",[])):
            tag.decompose()
    slug = page.replace("en/","")
    path = "/" if slug == "index.html" else "/" + slug
    en_path = "/en/" if slug == "index.html" else "/en/" + slug
    title_map_he = {
        "index.html":"Green Therapy | Wellness & Wellbeing לאירועי חברה",
        "spa.html":"Pop-Up Spa לאירועי חברה | Green Therapy",
        "ice-bath.html":"אמבטיות קרח לאירועי חברה | Green Therapy",
        "workshops.html":"סדנאות Wellness & Wellbeing | Green Therapy",
        "healthy-bar.html":"בר בריאות לאירועים | Green Therapy",
        "about.html":"אודות Green Therapy | Wellness לאירועי חברה",
        "gallery.html":"גלריית אירועים | Green Therapy",
        "contact.html":"תכנון אירוע Wellness | Green Therapy",
    }
    title_map_en = {
        "index.html":"Green Therapy | Corporate Wellness & Wellbeing",
        "spa.html":"Pop-Up Spa for Corporate Events | Green Therapy",
        "ice-bath.html":"Corporate Ice Bath Experience | Green Therapy",
        "workshops.html":"Wellness & Wellbeing Workshops | Green Therapy",
        "healthy-bar.html":"Healthy Bar for Events | Green Therapy",
        "about.html":"About Green Therapy | Corporate Wellness",
        "gallery.html":"Event Gallery | Green Therapy",
        "contact.html":"Plan a Wellness Event | Green Therapy",
    }
    desc_he = "Green Therapy מפיקה מתחמי Wellness ו-Wellbeing לאירועי חברה: Pop-Up Spa, אמבטיות קרח, סדנאות גוף-נפש ובר בריאות, בהתאמה לאופי האירוע."
    desc_en = "Green Therapy creates corporate Wellness & Wellbeing experiences including Pop-Up Spa, ice baths, mind-body workshops and healthy bars, tailored to each event."
    title = (title_map_en if en else title_map_he)[slug]
    if soup.title: soup.title.string = title
    else:
        t=soup.new_tag("title"); t.string=title; head.append(t)
    def meta(**attrs):
        tag=soup.new_tag("meta")
        for k,v in attrs.items(): tag[k.replace("_","-")]=v
        head.append(tag)
    meta(name="description", content=desc_en if en else desc_he)
    meta(name="robots", content="index,follow,max-image-preview:large")
    meta(name="google-site-verification", content="GT_SEARCH_CONSOLE_VERIFICATION")
    canon = soup.new_tag("link", rel="canonical", href=BASE_URL + (en_path if en else path)); head.append(canon)
    for lang,href in [("he",BASE_URL+path),("en",BASE_URL+en_path),("x-default",BASE_URL+path)]:
        head.append(soup.new_tag("link", rel="alternate", hreflang=lang, href=href))
    meta(property="og:type", content="website"); meta(property="og:site_name", content="Green Therapy")
    meta(property="og:title", content=title); meta(property="og:description", content=desc_en if en else desc_he)
    meta(property="og:url", content=BASE_URL + (en_path if en else path))
    meta(name="twitter:card", content="summary_large_image")
    # JSON-LD
    schema = {
      "@context":"https://schema.org","@type":"Organization","name":"Green Therapy",
      "url":BASE_URL,"email":"alongreentherapy@gmail.com",
      "description": desc_en if en else desc_he,
      "areaServed":{"@type":"Country","name":"Israel"},
      "knowsAbout":["Corporate wellness","Wellbeing","Pop-Up Spa","Ice baths","Mindfulness","Yoga","Healthy bar"]
    }
    ld=soup.new_tag("script", type="application/ld+json"); ld.string=json.dumps(schema,ensure_ascii=False); head.append(ld)
    # Site config before enhancements
    prefix = "../" if en else ""
    if not head.find("script", src=re.compile(r"site-config\.js")):
        head.append(soup.new_tag("script", src=prefix+"site-config.js"))

def fix_logo(soup):
    header = soup.find("header")
    if not header: return
    for img in header.find_all("img"):
        src=img.get("src","")
        if "googleusercontent" in src or "Mascot" in img.get("alt",""):
            mark = soup.new_tag("span")
            mark["class"] = ["gt-brand-mark"]
            mark["aria-hidden"] = "true"
            mark.string = "✦"
            img.replace_with(mark)

def fix_images(soup, page, en=False):
    prefix = "../" if en else ""
    photos = PHOTO_SETS.get(page, PHOTO_SETS["index.html"])
    idx=0
    # testimonial screenshots first
    t_idx=0
    for img in soup.find_all("img"):
        src=img.get("src","")
        if "client-message-" in src:
            img["loading"]="lazy"; img["decoding"]="async"
            continue
        if "googleusercontent.com" in src:
            img["src"]=prefix+"assets/client/"+photos[idx % len(photos)]
            idx += 1
            if en:
                img["alt"]="Green Therapy wellness experience at a corporate event"
            else:
                img["alt"]="מתחם Wellness של Green Therapy באירוע חברה"
        if img.get("src","").startswith(prefix+"assets/client/"):
            img["loading"]="lazy"
            img["decoding"]="async"
    # first substantial image should load eagerly
    main=soup.find("main")
    if main:
        first=main.find("img")
        if first:
            first["loading"]="eager"; first["fetchpriority"]="high"

def fix_forms(soup, en=False):
    for fi,form in enumerate(soup.find_all("form"),1):
        form.attrs.pop("onsubmit",None)
        form["method"]="post"
        form["action"]="/api/contact"
        form["data-contact-form"]="true"
        # Remove implicit selections.
        for inp in form.find_all("input"):
            inp.attrs.pop("checked",None)
        for sel in form.find_all("select"):
            for opt in sel.find_all("option"): opt.attrs.pop("selected",None)
            placeholder = next((o for o in sel.find_all("option") if not o.get("value")), None)
            if not placeholder:
                placeholder=soup.new_tag("option", value="")
                placeholder.string="Choose an option" if en else "בחרו אפשרות"
                sel.insert(0,placeholder)
            placeholder["selected"]=""; placeholder["disabled"]=""
        # Ensure fields have names/autocomplete where possible.
        n=0
        for field in form.find_all(["input","select","textarea"]):
            if field.get("type") in {"submit","button","hidden"}: continue
            if not field.get("name"):
                n+=1
                fid=field.get("id","").lower()
                typ=field.get("type","")
                if "mail" in fid or typ=="email": name="email"
                elif "phone" in fid or "tel" in fid or typ=="tel": name="phone"
                elif "name" in fid: name="name"
                elif "company" in fid: name="company"
                else: name=f"field_{fi}_{n}"
                field["name"]=name
        hp=soup.new_tag("input", type="text", name="company_website", tabindex="-1", autocomplete="off")
        hp["class"]=["gt-honeypot"]; hp["aria-hidden"]="true"
        form.insert(0,hp)
        status=soup.new_tag("div")
        status["class"]=["gt-form-status"]; status["role"]="status"; status["aria-live"]="polite"
        form.append(status)

def simplify_content(soup, en=False):
    # Digital queue system claim -> honest coordination wording.
    for node in list(soup.find_all(string=lambda s: s and (("מערכת דיגיטלית" in s) if not en else ("digital system" in s.lower())))):
        p=node.parent
        while p and p.name not in {"p","span","div"}: p=p.parent
        if p:
            p.string = ("Treatment times are coordinated in advance according to the event schedule and participant flow."
                        if en else "זמני הטיפולים מתואמים מראש בהתאם ללוח הזמנים של האירוע ולזרימת המשתתפים.")
    # Remove duplicated ice-bath cards called out by client.
    remove_card_by_text(soup, ["fitbit","אנרגיה ומסוגלות"] if not en else ["fitbit","energy and abilities","Energy and capability"])
    # Consolidate ice-bath step 4 into guided immersion.
    node=soup.find(string=lambda s: s and ("סיום וחיבור קבוצתי" in s if not en else "Conclusion and group connection" in s))
    if node:
        card=nearest_card(node.parent)
        if card: card.decompose()
    guided=soup.find(string=lambda s: s and ("טבילה מודרכת" in s if not en else "Guided immersion" in s))
    if guided:
        card=nearest_card(guided.parent)
        if card:
            p=card.find("p")
            if p: p.string=("Guided immersion with professional support, followed by a short group close-out."
                            if en else "טבילה מודרכת בליווי מקצועי, ולאחריה סיום קצר שמחזיר את הקבוצה יחד לאירוע.")
    # Contact-page repeated info cards -> one concise card.
    if soup.find(string=lambda s:s and ("איך מתבצעת ההפקה?" in s if not en else "How is the production carried out?" in s)):
        targets=[]
        for phrase in (["איך מתבצעת ההפקה?","איך מתאמים את זמני הטיפולים?"] if not en else ["How is the production carried out?","How are treatment times coordinated?"]):
            n=soup.find(string=lambda s:s and phrase in s)
            if n:
                c=nearest_card(n.parent)
                if c and c not in targets: targets.append(c)
        if targets:
            first=targets[0]
            first.clear()
            icon=soup.new_tag("div"); icon["class"]=["w-10","h-10","rounded-lg","bg-surface-container","text-tertiary","flex","items-center","justify-center","mb-4"]
            sp=soup.new_tag("span"); sp["class"]=["material-symbols-outlined"]; sp.string="event_available"; icon.append(sp); first.append(icon)
            h=soup.new_tag("h3"); h["class"]=["font-headline-md","text-headline-md","text-on-surface","mb-2.5"]; h.string="How do we run the experience?" if en else "איך אנחנו עובדים?"; first.append(h)
            p=soup.new_tag("p"); p["class"]=["font-body-md","text-body-md","text-secondary","leading-relaxed"]
            p.string=("We coordinate the equipment, setup, staffing and treatment timing around the event schedule, participant count and venue."
                      if en else "אנחנו מתאמים את הציוד, ההקמה, הצוות וזמני הטיפולים לפי לוח הזמנים של האירוע, כמות המשתתפים והמיקום.")
            first.append(p)
            for c in targets[1:]: c.decompose()

def add_wellness_space(soup, en=False):
    if soup.find(id="wellness-space"): return
    page_main=soup.find("main")
    if not page_main: return
    prefix="../" if en else ""
    if en:
        title="The Green Therapy Wellness & Hospitality Space"
        copy="Alongside the mobile corporate experiences, Green Therapy also operates a private wellness and hospitality space. Contact us for availability, hosting details and the experiences currently offered on site."
        cta="Ask about the wellness space"
    else:
        title="הצימר ומתחם הבריאות של Green Therapy"
        copy="לצד מתחמי ה-Wellness שמגיעים לאירועי חברה, Green Therapy מפעילה גם צימר ומתחם בריאות פרטי. לפרטים על אירוח, זמינות והחוויות המתקיימות במקום – דברו איתנו."
        cta="לפרטים על המתחם"
    section_html=f"""
<section id="wellness-space" class="gt-wellness-space py-16 md:py-24 bg-primary-container/45 border-y border-outline-variant/20">
  <div class="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop">
    <div class="grid lg:grid-cols-2 gap-10 lg:gap-14 items-center">
      <div class="grid grid-cols-2 gap-3">
        <img class="rounded-2xl w-full h-56 md:h-72 object-cover col-span-2" src="{prefix}assets/client/887e1d9b-94c2-49aa-b3b9-258f57aacf3c.webp" alt="{htmlmod.escape(title)}" loading="lazy" decoding="async">
        <img class="rounded-2xl w-full h-40 md:h-52 object-cover" src="{prefix}assets/client/1c3d140a-38a4-4aff-8196-9fea60c15ae3.webp" alt="{htmlmod.escape(title)}" loading="lazy" decoding="async">
        <img class="rounded-2xl w-full h-40 md:h-52 object-cover" src="{prefix}assets/client/827ed1a7-ce8f-428f-91c1-20ac014453bf.webp" alt="{htmlmod.escape(title)}" loading="lazy" decoding="async">
      </div>
      <div>
        <h2 class="font-display text-headline-lg md:text-[40px] md:leading-[48px] text-forest-deep font-bold mb-5">{title}</h2>
        <p class="font-body-lg text-body-lg text-on-surface-variant leading-relaxed mb-7">{copy}</p>
        <a href="contact.html" class="inline-flex items-center gap-2 bg-primary text-white px-6 py-3 rounded-full font-bold hover:bg-forest-deep transition-colors">{cta}<span class="material-symbols-outlined">arrow_back</span></a>
      </div>
    </div>
  </div>
</section>"""
    # Insert before the final CTA/footer area when possible.
    footer=soup.find("footer")
    if footer: footer.insert_before(BeautifulSoup(section_html,"html.parser"))
    else: page_main.append(BeautifulSoup(section_html,"html.parser"))

def ensure_internal_nav(soup, en=False):
    header=soup.find("header")
    if not header: return
    nav=header.find("nav")
    if not nav: return
    links_en=[("index.html","Home"),("spa.html","Pop-Up Spa"),("ice-bath.html","Ice Baths"),("workshops.html","Mind & Body"),("healthy-bar.html","Healthy Bar"),("index.html#wellness-space","Our Space"),("gallery.html","Gallery"),("contact.html","Contact")]
    links_he=[("index.html","דף הבית"),("spa.html","Pop-Up Spa"),("ice-bath.html","אמבטיות קרח"),("workshops.html","Mind & Body"),("healthy-bar.html","בר בריאות"),("index.html#wellness-space","המתחם שלנו"),("gallery.html","גלריה"),("contact.html","צור קשר")]
    nav.clear()
    for href,label in (links_en if en else links_he):
        a=soup.new_tag("a", href=href)
        a["class"]=["text-on-surface-variant","font-medium","hover:text-primary","transition-colors","duration-300","font-label-md","text-label-md"]
        a.string=label; nav.append(a)

def add_footer_links(soup,en=False):
    footer=soup.find("footer")
    if not footer: return
    txt=str(footer)
    # remove unsupported copy and odd business categories
    for bad in ["Restoring balance through nature.","Offsite Experiences","Team Building Workshops"]:
        for node in footer.find_all(string=lambda s:s and bad in s):
            node.replace_with(node.replace(bad,""))
    # add legal links once
    if not footer.find("a",href=re.compile("privacy\.html")):
        box=soup.new_tag("div")
        box["class"]=["gt-legal-links"]
        for href,label in ([("privacy.html","Privacy"),("accessibility.html","Accessibility")] if en else [("privacy.html","פרטיות"),("accessibility.html","נגישות")]):
            a=soup.new_tag("a",href=href); a.string=label; box.append(a)
        footer.append(box)

def add_accessibility(soup):
    body=soup.body
    if not body: return
    main=soup.find("main")
    if main: main["id"]="main-content"
    if not body.find("a",class_="gt-skip-link"):
        a=soup.new_tag("a",href="#main-content"); a["class"]=["gt-skip-link"]; a.string="דלגו לתוכן" if soup.html.get("lang")!="en" else "Skip to content"; body.insert(0,a)
    # Buttons and controls need labels.
    for a in soup.find_all("a"):
        if not a.get_text(" ",strip=True) and not a.get("aria-label"):
            a["aria-label"]="Link" if soup.html.get("lang")=="en" else "קישור"
    for img in soup.find_all("img"):
        if not img.has_attr("alt"): img["alt"]=""

def process(path):
    full=ROOT/path
    soup=BeautifulSoup(full.read_text(encoding="utf-8"),"html.parser")
    en=path.startswith("en/")
    page=Path(path).name
    replace_text_nodes(soup, EN_REPL if en else HE_REPL)
    fix_logo(soup)
    fix_images(soup,page,en)
    fix_forms(soup,en)
    simplify_content(soup,en)
    ensure_internal_nav(soup,en)
    if page=="index.html": add_wellness_space(soup,en)
    add_head_meta(soup,path,en)
    add_footer_links(soup,en)
    add_accessibility(soup)
    # Correct language switch targets.
    for a in soup.find_all("a",attrs={"data-lang-switch":True}):
        if en:
            a["href"]="../"+page; a.string="HE"
        else:
            a["href"]="en/"+page; a.string="EN"
    full.write_text(str(soup),encoding="utf-8")

for path in HE_PAGES+EN_PAGES:
    if (ROOT/path).exists(): process(path)

# ---------- global production CSS ----------
css = r"""
/* Production hardening: accessibility, mobile, consistent brand */
:root{--gt-green:#1d3326;--gt-green-2:#2d5a43;--gt-mint:#e3ece5}
html{scroll-padding-top:92px}
body{overflow-x:hidden}
.gt-skip-link{position:fixed;z-index:9999;top:8px;left:8px;transform:translateY(-150%);background:#fff;color:#1d3326;padding:.75rem 1rem;border:2px solid #1d3326;border-radius:.5rem;font-weight:700}
.gt-skip-link:focus{transform:none}
:focus-visible{outline:3px solid #2d5a43!important;outline-offset:3px!important}
.gt-brand-mark{font-size:1.8rem;line-height:1;color:#1d3326;display:flex;align-items:center;justify-content:center;width:100%;height:100%}
footer{background:#1d3326!important;color:#fff!important}
footer a{color:inherit}
.gt-legal-links{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;padding:1rem 1rem 1.5rem;color:rgba(255,255,255,.78);font-size:.875rem}
.gt-legal-links a{text-decoration:underline;text-underline-offset:3px}
a[href^="mailto:"]{overflow-wrap:anywhere;word-break:break-word;max-width:100%}
.gt-honeypot{position:absolute!important;left:-9999px!important;width:1px!important;height:1px!important;opacity:0!important}
.gt-form-status{margin-top:.75rem;font-weight:600;line-height:1.5}
.gt-form-status.is-error{color:#8b1e1e}.gt-form-status.is-success{color:#1d5a38}
.gt-mobile-menu-toggle{display:none}
.gt-mobile-panel{display:none}
@media(max-width:767px){
  header>div{padding:10px 14px!important;gap:10px!important;min-height:72px}
  header a[aria-label="Green Therapy"]{flex:1;min-width:0;gap:8px!important}
  header a[aria-label="Green Therapy"] .w-12{width:40px!important;height:40px!important;min-width:40px}
  header a[aria-label="Green Therapy"] span.font-headline-md{font-size:1.2rem!important;line-height:1.1!important;white-space:normal}
  header a[aria-label="Green Therapy"] span.font-label-sm{font-size:.7rem!important;line-height:1.2!important}
  header a[href^="mailto:"]{display:none!important}
  header [data-lang-switch]{width:44px!important;min-width:44px!important;padding:0!important}
  .gt-mobile-menu-toggle{display:inline-flex!important;width:44px;height:44px;border-radius:999px;align-items:center;justify-content:center;background:#e3ece5;color:#1d3326;border:1px solid #ccc6bb;font-size:0}
  .gt-mobile-menu-toggle:after{content:"☰";font-size:1.35rem}
  .gt-mobile-panel{position:fixed;top:72px;left:12px;right:12px;z-index:80;background:#fff8f5;border:1px solid #ccc6bb;border-radius:18px;box-shadow:0 18px 45px rgba(29,51,38,.18);padding:10px}
  .gt-mobile-panel.is-open{display:grid;grid-template-columns:1fr 1fr;gap:6px}
  .gt-mobile-panel a{padding:12px;border-radius:12px;color:#1d3326;font-weight:700;text-decoration:none;background:#e3ece5}
  main h1{font-size:clamp(2rem,10vw,3.1rem)!important;line-height:1.05!important}
  main h2{overflow-wrap:anywhere}
  main .text-display{font-size:clamp(2rem,10vw,3.1rem)!important;line-height:1.08!important}
  main .px-margin-mobile{padding-left:18px!important;padding-right:18px!important}
  .gt-wellness-space .grid-cols-2{gap:8px}
  .gt-wellness-space img{min-height:0}
  a[href^="mailto:"]{font-size:clamp(.84rem,3.7vw,1rem)!important}
  input,select,textarea{font-size:16px!important}
}
@media(max-width:380px){
 header a[aria-label="Green Therapy"] span.font-label-sm{display:none}
 .gt-mobile-panel.is-open{grid-template-columns:1fr}
}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
"""
(ROOT/"production.css").write_text(css,encoding="utf-8")

# Append production stylesheet to every page.
for path in HE_PAGES+EN_PAGES+["privacy.html","accessibility.html","en/privacy.html","en/accessibility.html"]:
    full=ROOT/path
    if not full.exists(): continue
    soup=BeautifulSoup(full.read_text(encoding="utf-8"),"html.parser")
    prefix="../" if path.startswith("en/") else ""
    if soup.head and not soup.head.find("link",href=re.compile("production\.css")):
        soup.head.append(soup.new_tag("link",rel="stylesheet",href=prefix+"production.css"))
    full.write_text(str(soup),encoding="utf-8")

# ---------- site configuration + runtime ----------
(ROOT/"site-config.js").write_text("""window.GREEN_THERAPY_CONFIG={googleAnalyticsId:"",googleSearchConsoleVerification:"",contactBackendEnabled:false};""",encoding="utf-8")
(ROOT/"enhancements.js").write_text(r"""(()=>{
const ready=()=>{
 document.body.classList.add('gt-page-ready');
 const isEn=document.documentElement.lang==='en'||location.pathname.includes('/en/');
 // Reveal animations
 const sections=[...document.querySelectorAll('main > section')];
 sections.forEach((s,i)=>s.classList.add(i===0?'gt-visible':'gt-reveal'));
 if('IntersectionObserver'in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('gt-visible');io.unobserve(e.target)}}),{rootMargin:'0px 0px -6% 0px',threshold:.06});sections.slice(1).forEach(s=>io.observe(s))}else sections.forEach(s=>s.classList.add('gt-visible'));
 // Mobile navigation from the real desktop nav.
 const header=document.querySelector('header'); const nav=header?.querySelector('nav');
 if(header&&nav&&!header.querySelector('.gt-mobile-menu-toggle')){
   const actions=header.querySelector('[data-lang-switch]')?.parentElement;
   const btn=document.createElement('button');btn.type='button';btn.className='gt-mobile-menu-toggle';btn.setAttribute('aria-label',isEn?'Open menu':'פתיחת תפריט');btn.setAttribute('aria-expanded','false');
   actions?.appendChild(btn);
   const panel=document.createElement('nav');panel.className='gt-mobile-panel';panel.setAttribute('aria-label',isEn?'Mobile navigation':'ניווט במובייל');
   panel.innerHTML=nav.innerHTML;document.body.appendChild(panel);
   btn.addEventListener('click',()=>{const open=panel.classList.toggle('is-open');btn.setAttribute('aria-expanded',String(open))});
   panel.addEventListener('click',e=>{if(e.target.closest('a')){panel.classList.remove('is-open');btn.setAttribute('aria-expanded','false')}})
 }
 // Broken-image safety net.
 const fallback=(isEn?'../':'')+'assets/client/887e1d9b-94c2-49aa-b3b9-258f57aacf3c.webp';
 document.querySelectorAll('img').forEach(img=>img.addEventListener('error',()=>{if(img.src.endsWith(fallback))return;img.src=fallback},{once:true}));
 // Honest backend-ready forms: never show a false success.
 document.querySelectorAll('form[data-contact-form]').forEach(form=>{
   form.addEventListener('submit',async e=>{
     e.preventDefault(); const status=form.querySelector('.gt-form-status'); if(status){status.className='gt-form-status';status.textContent=isEn?'Sending…':'שולחים…'}
     try{
       const fd=new FormData(form); const payload=Object.fromEntries(fd.entries());
       const res=await fetch('/api/contact',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(payload)});
       const data=await res.json().catch(()=>({}));
       if(res.ok){if(status){status.classList.add('is-success');status.textContent=isEn?'Thank you. Your inquiry was sent.':'תודה, הפנייה נשלחה בהצלחה.'}form.reset();return}
       if(status){status.classList.add('is-error');status.innerHTML=isEn?'Online form delivery is not connected yet. Please email <a href="mailto:alongreentherapy@gmail.com">alongreentherapy@gmail.com</a>.':'שליחת הטופס עדיין אינה מחוברת. אפשר לפנות ישירות במייל: <a href="mailto:alongreentherapy@gmail.com">alongreentherapy@gmail.com</a>.'}
     }catch(err){if(status){status.classList.add('is-error');status.textContent=isEn?'Unable to send right now. Please use the email address on this page.':'לא ניתן לשלוח כרגע. אפשר לפנות באמצעות כתובת המייל שבעמוד.'}}
   })
 });
 // Analytics is dormant until an ID is configured AND the visitor consents.
 const cfg=window.GREEN_THERAPY_CONFIG||{}; const key='gt-analytics-consent';
 const loadGA=()=>{if(!cfg.googleAnalyticsId||window.gtag)return;const s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(cfg.googleAnalyticsId);document.head.appendChild(s);window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('js',new Date());gtag('config',cfg.googleAnalyticsId,{anonymize_ip:true})};
 if(cfg.googleAnalyticsId){
   const consent=localStorage.getItem(key); if(consent==='granted')loadGA();
   if(!consent){const bar=document.createElement('div');bar.className='gt-cookie-banner';bar.innerHTML='<p>'+(isEn?'We use optional analytics only with your consent.':'אנו משתמשים בניתוח נתוני שימוש אופציונלי רק בהסכמתכם.')+'</p><div><button data-c="deny">'+(isEn?'Essential only':'חיוני בלבד')+'</button><button data-c="allow">'+(isEn?'Allow analytics':'אישור אנליטיקה')+'</button></div>';document.body.appendChild(bar);bar.addEventListener('click',e=>{const b=e.target.closest('button[data-c]');if(!b)return;const v=b.dataset.c==='allow'?'granted':'denied';localStorage.setItem(key,v);bar.remove();if(v==='granted')loadGA()})}
 }
};
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',ready):ready();
})();""",encoding="utf-8")

# ---------- legal/accessibility pages ----------
def simple_page(lang,title,body_html):
    rtl=lang=="he"; prefix="../" if lang=="en" else ""
    return f"""<!doctype html><html lang="{lang}" dir="{'rtl' if rtl else 'ltr'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | Green Therapy</title><meta name="robots" content="index,follow"><link rel="stylesheet" href="{prefix}production.css"><style>body{{font-family:Arial,sans-serif;background:#fff8f5;color:#211a14;margin:0}}main{{max-width:860px;margin:auto;padding:48px 20px 80px}}a{{color:#2d5a43}}h1,h2{{color:#1d3326;line-height:1.2}}p,li{{line-height:1.8}}.back{{display:inline-block;margin-bottom:28px;font-weight:700}}</style></head><body><main id="main-content"><a class="back" href="index.html">{'Back to site' if lang=='en' else 'חזרה לאתר'}</a><h1>{title}</h1>{body_html}</main></body></html>"""
privacy_he="""<p>עודכן: ספטמבר 2026.</p><h2>איזה מידע נאסף</h2><p>כאשר טופס יצירת הקשר יחובר למערכת שליחה, הוא עשוי להעביר פרטי קשר ופרטי אירוע שתבחרו למסור. בשלב הנוכחי מנגנון השליחה החיצוני אינו מחובר.</p><h2>אנליטיקה וקובצי Cookie</h2><p>Google Analytics אינו פעיל כל עוד לא הוגדר מזהה מדידה. לאחר חיבור עתידי, טעינת האנליטיקה תתבצע רק לאחר הסכמה.</p><h2>שימוש ושמירה</h2><p>מידע שיימסר ישמש לצורך מענה לפנייה ותכנון שירותי Green Therapy. לפני חיבור CRM, דיוור או ספק אנליטיקה יש לעדכן מדיניות זו בהתאם לספקים ולתקופות השמירה בפועל.</p><h2>יצירת קשר</h2><p><a href="mailto:alongreentherapy@gmail.com">alongreentherapy@gmail.com</a></p>"""
privacy_en="""<p>Updated: September 2026.</p><h2>Information collected</h2><p>Once the contact backend is connected, forms may transmit contact and event details that you choose to provide. The external delivery destination is not connected in the current configuration.</p><h2>Analytics and cookies</h2><p>Google Analytics is inactive until a measurement ID is configured. When enabled later, optional analytics loads only after consent.</p><h2>Use and retention</h2><p>Submitted information will be used to respond to inquiries and plan Green Therapy services. This notice should be updated when a CRM, mailing platform or analytics provider is connected.</p><h2>Contact</h2><p><a href="mailto:alongreentherapy@gmail.com">alongreentherapy@gmail.com</a></p>"""
access_he="""<p>Green Therapy פועלת להנגשת האתר בהתאם לעקרונות WCAG: ניווט מקלדת, מבנה כותרות ברור, ניגודיות, טקסט חלופי לתמונות, תמיכה בהפחתת תנועה וטפסים עם תוויות ברורות.</p><p>אם נתקלתם בבעיה, ניתן לפנות אלינו בכתובת <a href="mailto:alongreentherapy@gmail.com">alongreentherapy@gmail.com</a> ולציין את העמוד והבעיה.</p>"""
access_en="""<p>Green Therapy aims to follow WCAG accessibility principles, including keyboard navigation, clear heading structure, contrast, image alternatives, reduced-motion support and clearly labelled forms.</p><p>If you encounter an accessibility issue, email <a href="mailto:alongreentherapy@gmail.com">alongreentherapy@gmail.com</a> with the page and issue.</p>"""
(ROOT/"privacy.html").write_text(simple_page("he","מדיניות פרטיות",privacy_he),encoding="utf-8")
(ROOT/"accessibility.html").write_text(simple_page("he","הצהרת נגישות",access_he),encoding="utf-8")
(ROOT/"en"/"privacy.html").write_text(simple_page("en","Privacy Policy",privacy_en),encoding="utf-8")
(ROOT/"en"/"accessibility.html").write_text(simple_page("en","Accessibility Statement",access_en),encoding="utf-8")

# ---------- Netlify-ready backend (dormant until webhook env var exists) ----------
fn=ROOT/"netlify"/"functions"; fn.mkdir(parents=True,exist_ok=True)
(fn/"contact.mts").write_text(r"""export default async (req: Request) => {
  if (req.method !== "POST") return new Response(JSON.stringify({error:"method_not_allowed"}),{status:405,headers:{"content-type":"application/json"}});
  let data: Record<string, unknown> = {};
  try { data = await req.json(); } catch { return new Response(JSON.stringify({error:"invalid_json"}),{status:400,headers:{"content-type":"application/json"}}); }
  if (data.company_website) return new Response(JSON.stringify({ok:true}),{status:200,headers:{"content-type":"application/json"}});
  const hasContact = Boolean(data.email || data.phone || data.name || data.fullName);
  if (!hasContact) return new Response(JSON.stringify({error:"missing_contact"}),{status:400,headers:{"content-type":"application/json"}});
  const webhook = Netlify.env.get("CONTACT_WEBHOOK_URL");
  if (!webhook) return new Response(JSON.stringify({configured:false,error:"contact_backend_not_connected"}),{status:503,headers:{"content-type":"application/json","cache-control":"no-store"}});
  const upstream = await fetch(webhook,{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({source:"green-therapy-site",submittedAt:new Date().toISOString(),...data})});
  if (!upstream.ok) return new Response(JSON.stringify({error:"delivery_failed"}),{status:502,headers:{"content-type":"application/json"}});
  return new Response(JSON.stringify({ok:true}),{status:200,headers:{"content-type":"application/json","cache-control":"no-store"}});
};
export const config = { path: "/api/contact" };
""",encoding="utf-8")
(ROOT/"netlify.toml").write_text("""[build]
  publish = "."

[functions]
  directory = "netlify/functions"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"
    X-Frame-Options = "SAMEORIGIN"
""",encoding="utf-8")
(ROOT/".gitignore").write_text(".netlify/\nnode_modules/\n",encoding="utf-8")

# ---------- crawl/index files ----------
urls=[]
for p in HE_PAGES:
    path="/" if p=="index.html" else "/"+p; urls.append(BASE_URL+path)
    ep="/en/" if p=="index.html" else "/en/"+p; urls.append(BASE_URL+ep)
urls += [BASE_URL+"/privacy.html",BASE_URL+"/accessibility.html",BASE_URL+"/en/privacy.html",BASE_URL+"/en/accessibility.html"]
(ROOT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)+"\n</urlset>\n",encoding="utf-8")
(ROOT/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+BASE_URL+"/sitemap.xml\n",encoding="utf-8")
(ROOT/"DEPLOYMENT.md").write_text("""# Green Therapy deployment checklist

## Google Analytics
Set window.GREEN_THERAPY_CONFIG.googleAnalyticsId in site-config.js. Analytics remains dormant until an ID exists and the visitor grants consent.

## Google Search Console
Replace GT_SEARCH_CONSOLE_VERIFICATION in the generated meta tag with the verification token and redeploy. Submit /sitemap.xml after verification.

## Contact backend
Set CONTACT_WEBHOOK_URL in Netlify environment variables to the approved CRM/email automation endpoint. Until then, forms clearly direct visitors to email instead of showing a false success.

## Custom domain
When a custom domain is connected, update BASE_URL in scripts/production_release.py and regenerate canonical, hreflang, sitemap and robots values.
""",encoding="utf-8")

print("Production release transformations complete.")
