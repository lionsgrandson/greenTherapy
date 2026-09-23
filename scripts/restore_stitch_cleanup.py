#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import re

ROOT=Path(__file__).resolve().parents[1]
HE=["index.html","spa.html","ice-bath.html","workshops.html","healthy-bar.html","about.html","contact.html"]
EN=[f"en/{p}" for p in HE]
ALL=HE+EN
PHONE="+972 53-532-4962"
TEL="+972535324962"
WA="https://wa.me/972535324962"
EMAIL="alongreentherapy@gmail.com"
GOOGLE="https://share.google/hEvKhs5USb65ZEgi7"

def en(path): return path.startswith("en/")
def prefix(path): return "../" if en(path) else ""

def unified_header(soup,path):
    is_en=en(path); page=Path(path).name
    links_en=[("index.html","Home"),("spa.html","Pop-Up Spa"),("ice-bath.html","Ice Baths"),("workshops.html","Mind & Body"),("healthy-bar.html","Healthy Bar"),("about.html","About"),("contact.html","Contact")]
    links_he=[("index.html","דף הבית"),("spa.html","ספא פופ-אפ"),("ice-bath.html","אמבטיות קרח"),("workshops.html","סדנאות גוף ונפש"),("healthy-bar.html","בר בריאות"),("about.html","אודות"),("contact.html","צור קשר")]
    nav="".join(f'<a class="text-on-surface-variant font-medium hover:text-primary transition-colors duration-300 font-label-md text-label-md" href="{h}">{t}</a>' for h,t in (links_en if is_en else links_he))
    switch_href=("../"+page) if is_en else ("en/"+page)
    switch_label="HE" if is_en else "EN"
    cta="Plan an Event" if is_en else "לתכנון אירוע"
    title="WhatsApp" if is_en else "וואטסאפ"
    home="Home" if is_en else "דף הבית"
    p=prefix(path)
    html=f'''<header class="gt-unified-header docked full-width top-0 sticky z-50 bg-surface-bright/95 backdrop-blur-md border-b border-outline-variant/30 transition-all duration-300">
      <div class="gt-header-inner flex justify-between items-center w-full px-margin-mobile md:px-margin-desktop py-3 max-w-container-max mx-auto">
        <a aria-label="Green Therapy — {home}" class="gt-brand-link" href="index.html"><img alt="Green Therapy" class="gt-header-logo" height="106" src="{p}assets/green-therapy-logo.webp" width="170"/></a>
        <nav class="gt-main-nav hidden lg:flex items-center gap-5 font-label-md text-label-md text-on-surface-variant">{nav}</nav>
        <div class="gt-header-actions flex items-center gap-2">
          <a class="gt-header-phone hidden xl:inline-flex items-center gap-2 px-3 h-10 rounded-full border border-outline-variant/40 bg-surface-container-lowest text-forest-deep font-label-sm font-bold" dir="ltr" href="tel:{TEL}">{PHONE}</a>
          <a class="inline-flex items-center justify-center min-w-10 h-10 px-3 rounded-full bg-surface-container text-forest-deep border border-outline-variant/40 hover:bg-primary-container transition-all font-label-sm text-label-sm font-bold" data-lang-switch href="{switch_href}">{switch_label}</a>
          <a class="gt-plan-event hidden sm:inline-flex items-center justify-center gap-2 bg-primary text-on-primary font-label-md text-label-md px-4 py-2.5 rounded-full hover:bg-forest-deep transition-all duration-200 shadow-sm" href="contact.html">{cta}</a>
          <a class="inline-flex items-center justify-center w-10 h-10 rounded-full bg-primary-container text-terracotta border border-outline-variant/40 hover:bg-secondary-container transition-all" href="{WA}" rel="noopener noreferrer" target="_blank" title="{title}"><span class="material-symbols-outlined text-[20px]">chat</span></a>
        </div>
      </div>
      <a class="gt-mobile-phone-strip" dir="ltr" href="tel:{TEL}">{PHONE}</a>
    </header>'''
    old=soup.find("header")
    if old: old.replace_with(BeautifulSoup(html,"html.parser"))

def unified_footer(soup,path):
    is_en=en(path); p=prefix(path)
    if is_en:
        links_title,legal_title,contact_title="Links","Legal","Contact"
        links=[("index.html","Home"),("spa.html","Pop-Up Spa"),("ice-bath.html","Ice Baths"),("workshops.html","Mind & Body"),("healthy-bar.html","Healthy Bar"),("about.html","About"),("contact.html","Contact")]
        legal=[("privacy.html","Privacy Policy"),("accessibility.html","Accessibility")]
        phone_label,email_label,address_label="Phone","Email","Address"
        address_text="View on Google"
    else:
        links_title,legal_title,contact_title="קישורים","משפטי","צור קשר"
        links=[("index.html","דף הבית"),("spa.html","ספא פופ-אפ"),("ice-bath.html","אמבטיות קרח"),("workshops.html","סדנאות גוף ונפש"),("healthy-bar.html","בר בריאות"),("about.html","אודות"),("contact.html","צור קשר")]
        legal=[("privacy.html","מדיניות פרטיות"),("accessibility.html","הצהרת נגישות")]
        phone_label,email_label,address_label="טלפון","מייל","כתובת"
        address_text="לצפייה ב-Google"
    li="".join(f'<li><a href="{h}">{t}</a></li>' for h,t in links)
    le="".join(f'<li><a href="{h}">{t}</a></li>' for h,t in legal)
    html=f'''<footer class="gt-footer">
      <div class="gt-footer-grid">
        <div class="gt-footer-brand"><a aria-label="Green Therapy" href="index.html"><img alt="Green Therapy" loading="lazy" src="{p}assets/green-therapy-logo.webp"/></a></div>
        <div><h2>{links_title}</h2><ul>{li}</ul></div>
        <div><h2>{legal_title}</h2><ul>{le}</ul></div>
        <div><h2>{contact_title}</h2><ul class="gt-contact-list">
          <li><span>{phone_label}:</span> <a class="gt-phone-number" dir="ltr" href="tel:{TEL}">{PHONE}</a></li>
          <li><span>{email_label}:</span> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><span>{address_label}:</span> <a href="{GOOGLE}" rel="noopener noreferrer" target="_blank">{address_text}</a></li>
        </ul></div>
      </div>
    </footer>'''
    old=soup.find("footer")
    if old: old.replace_with(BeautifulSoup(html,"html.parser"))

def fix_phone(soup):
    for a in soup.find_all("a",href=lambda h:h and h.startswith("tel:")):
        a["dir"]="ltr"
        cls=a.get("class",[])
        if "gt-phone-number" not in cls: cls.append("gt-phone-number")
        a["class"]=cls
    for node in list(soup.find_all(string=True)):
        if node and PHONE in str(node) and node.parent and node.parent.name not in {"script","style"}:
            node.parent["dir"]="ltr"

def simplify_forms(soup,path):
    is_en=en(path)
    forms=list(soup.find_all("form"))
    if Path(path).name!="contact.html":
        for form in forms:
            cta="Plan an Event" if is_en else "לתכנון אירוע"
            call="Call" if is_en else "התקשרו"
            block=BeautifulSoup(f'''<div class="gt-service-contact-cta">
              <a class="gt-service-contact-primary" href="contact.html">{cta}</a>
              <a class="gt-service-contact-phone gt-phone-number" dir="ltr" href="tel:{TEL}">{PHONE}</a>
            </div>''',"html.parser")
            form.replace_with(block)
    else:
        for form in forms:
            html=f'''<form action="/api/contact" class="gt-simple-form" data-contact-form="true" method="post">
              <input aria-hidden="true" autocomplete="off" class="gt-honeypot" name="company_website" tabindex="-1" type="text"/>
              <div class="gt-simple-form-grid">
                <label><span>{"Full name" if is_en else "שם מלא"}</span><input autocomplete="name" name="name" required type="text"/></label>
                <label><span>{"Phone" if is_en else "טלפון"}</span><input autocomplete="tel" dir="ltr" name="phone" required type="tel"/></label>
                <label><span>{"Email" if is_en else "מייל"}</span><input autocomplete="email" dir="ltr" name="email" type="email"/></label>
                <label><span>{"Company / Organization" if is_en else "חברה / ארגון"}</span><input autocomplete="organization" name="company" type="text"/></label>
              </div>
              <label><span>{"Tell us briefly about the event" if is_en else "ספרו לנו בקצרה על האירוע"}</span><textarea name="message" rows="3"></textarea></label>
              <button class="gt-simple-submit" type="submit">{"Send" if is_en else "שלח"}</button>
              <div aria-live="polite" class="gt-form-status" role="status"></div>
            </form>'''
            form.replace_with(BeautifulSoup(html,"html.parser"))

def text_cleanup(soup,path):
    repl={
      "שליחת פרטים וקבלת הצעה מיידית":"שליחת פרטים וקבלת הצעה",
      "Send details and receive an immediate quote":"Send Details & Get a Proposal",
      "Get an instant quote":"Get a Proposal",
      "מעדיפים ליצור קשר ישי":"מעדיפים ליצור קשר ישירות",
    }
    for n in list(soup.find_all(string=True)):
        if not isinstance(n,NavigableString) or (n.parent and n.parent.name in {"script","style"}): continue
        s=str(n); t=s
        for a,b in repl.items(): t=t.replace(a,b)
        if t!=s: n.replace_with(t)
    # "Need more details?" / "צריכים פרטים נוספים?" must call, not email.
    targets=["צריכים פרטים נוספים?","Need more details?"]
    for target in targets:
        n=soup.find(string=lambda x:x and target in x)
        if n:
            sec=n.parent
            for _ in range(5):
                if not sec: break
                if getattr(sec,"name",None)=="section": break
                sec=sec.parent
            if sec:
                for a in sec.find_all("a"):
                    if a.get("href","").startswith("mailto:"):
                        a["href"]="tel:"+TEL; a["dir"]="ltr"; a["class"]=a.get("class",[])+["gt-phone-number"]
                        # keep icon but replace textual email if present
                        for txt in list(a.find_all(string=True)):
                            if EMAIL in str(txt): txt.replace_with(str(txt).replace(EMAIL,PHONE))

def remove_hero_chips(soup,path):
    phrases=(["יוגה, מדיטציה ומיינדפולנס","Sound Healing והרצאות העשרה","באירוע החברה שלכם"]
             if not en(path) else
             ["Yoga, Meditation & Mindfulness","Sound Healing and Enrichment Lectures","At Your Corporate Event","At your corporate event"])
    for phrase in phrases:
        for n in list(soup.find_all(string=lambda x:x and phrase.lower() in str(x).lower())):
            cur=n.parent
            chosen=None
            for _ in range(4):
                if not cur or not getattr(cur,"name",None): break
                if cur.name in {"div","span"} and not cur.find(["h1","h2"]) and len(cur.get_text(" ",strip=True))<140:
                    chosen=cur
                    classes=" ".join(cur.get("class",[]))
                    if any(k in classes for k in ["inline-flex","rounded-full","gap-2","badge"]): break
                cur=cur.parent
            if chosen: chosen.decompose()

def fix_home_images(soup,path):
    if Path(path).name!="index.html": return
    p=prefix(path)
    mapping=[
      (["Pop-Up Spa","ספא פופ-אפ"],"1c3d140a-38a4-4aff-8196-9fea60c15ae3.webp","center"),
      (["סדנאות מעשיות ומרתקות","Practical","Workshops"],"fe5e6cfc-8689-4287-8189-7286edf4bb30.webp","center"),
      (["קולינריה בריאה ומעוצבת","Healthy","Culinary"],"95941eaf-fc13-49b4-a515-c9d66f1fdb6e.webp","center 22%"),
    ]
    for phrases,imgname,pos in mapping:
        n=None
        for ph in phrases:
            n=soup.find(string=lambda x:x and ph.lower() in str(x).lower())
            if n: break
        if not n: continue
        cur=n.parent
        found=None
        for _ in range(7):
            if not cur: break
            found=cur.find("img") if hasattr(cur,"find") else None
            if found: break
            cur=cur.parent
        if found:
            found["src"]=p+"assets/client/"+imgname
            found["loading"]="lazy"; found["decoding"]="async"
            found["style"]="object-position:"+pos+";"

def polish_ice(soup,path):
    if Path(path).name!="ice-bath.html": return
    is_en=en(path)
    headings=[
      ("A Peak Experience Built Around Energy, Resilience & Connection" if is_en else "חוויית שיא שמחברת אנרגיה, חוסן וגיבוש","benefits"),
      ("Full 360° Production" if is_en else "מעטפת הפקה מלאה 360°","production"),
      ("Guided, Professional" if is_en else "חוויה מודרכת, מקצועית ומעצימה","guided")
    ]
    # Find sections via partial heading text.
    for phrase,kind in headings:
        n=soup.find(string=lambda x:x and phrase.lower() in str(x).lower())
        if not n: continue
        sec=n.parent
        while sec and sec.name!="section": sec=sec.parent
        if not sec: continue
        grids=sec.find_all("div",class_=lambda c:c and "grid" in " ".join(c) if isinstance(c,list) else (c and "grid" in c))
        grid=None
        for g in grids:
            # choose a grid with direct card div children
            kids=[x for x in g.find_all("div",recursive=False)]
            if len(kids)>=3:
                grid=g; break
        if not grid: continue
        cls=" ".join(grid.get("class",[]))
        if kind=="benefits":
            grid["class"]="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto".split()
            for card in grid.find_all("div",recursive=False):
                card["class"]=[c for c in card.get("class",[]) if "col-span" not in c]
        elif kind=="production":
            grid["class"]="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-5".split()
        else:
            grid["class"]="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto".split()
            for card in grid.find_all("div",recursive=False):
                # remove number circles only
                for d in list(card.find_all("div",recursive=False)):
                    txt=d.get_text(" ",strip=True)
                    if txt in {"1","2","3","4"}:
                        d.decompose()
                card["class"]=[c for c in card.get("class",[]) if "items-start" not in c]+["text-center","items-center"]

def add_external_accessibility(soup,path):
    # External widget replaces the custom accessibility menu; WhatsApp remains ours.
    if soup.find("script",src=re.compile("accessibility-widgets")): return
    cfg=soup.new_tag("script")
    if en(path):
        cfg.string='window.ACCESSIBILITY_WIDGET_CONFIG={enableVoiceControl:false,enableScreenReader:true,enableHighContrast:true,enableBiggerText:true,enableTextSpacing:true,enablePauseAnimations:true,enableHideImages:true,enableDyslexiaFont:true,enableBiggerCursor:true,enableLineHeight:true,widgetPosition:{side:"left",left:"16px",bottom:"16px"}};'
    else:
        cfg.string='window.ACCESSIBILITY_WIDGET_CONFIG={enableVoiceControl:false,enableScreenReader:true,enableHighContrast:true,enableBiggerText:true,enableTextSpacing:true,enablePauseAnimations:true,enableHideImages:true,enableDyslexiaFont:true,enableBiggerCursor:true,enableLineHeight:true,widgetPosition:{side:"left",left:"16px",bottom:"16px"},lang:{accessibilityMenu:"תפריט נגישות",closeAccessibilityMenu:"סגירת תפריט נגישות",accessibilityTools:"כלי נגישות",resetAllSettings:"איפוס הגדרות",screenReader:"קורא מסך",highContrast:"ניגודיות גבוהה",biggerText:"טקסט גדול",textSpacing:"ריווח טקסט",pauseAnimations:"עצירת אנימציות",hideImages:"הסתרת תמונות",dyslexiaFriendly:"גופן ידידותי לדיסלקציה",biggerCursor:"סמן גדול",lineHeight:"גובה שורה"}};'
    ext=soup.new_tag("script",src="https://cdn.jsdelivr.net/npm/accessibility-widgets@latest/widget.js",defer=True)
    if soup.body:
        soup.body.append(cfg); soup.body.append(ext)

def image_loading(soup):
    imgs=soup.find_all("img")
    first_content=False
    for img in imgs:
        if "green-therapy-logo" in img.get("src",""): continue
        if not first_content:
            # keep an explicitly eager hero eager
            if img.get("loading")=="eager" or img.get("fetchpriority")=="high":
                first_content=True; continue
        img["loading"]="lazy"; img["decoding"]="async"

for path in ALL:
    f=ROOT/path
    soup=BeautifulSoup(f.read_text(encoding="utf-8"),"html.parser")
    unified_header(soup,path)
    unified_footer(soup,path)
    fix_phone(soup)
    simplify_forms(soup,path)
    text_cleanup(soup,path)
    remove_hero_chips(soup,path)
    fix_home_images(soup,path)
    polish_ice(soup,path)
    add_external_accessibility(soup,path)
    image_loading(soup)
    f.write_text(str(soup),encoding="utf-8")

# Gallery is intentionally removed because the available local client set repeats the same images across the site.
for p in [ROOT/"gallery.html",ROOT/"en"/"gallery.html"]:
    if p.exists(): p.unlink()

# Redirect old gallery links cleanly.
(ROOT/"_redirects").write_text("/gallery.html / 301\n/en/gallery.html /en/ 301\n/gallery / 301\n/en/gallery /en/ 301\n",encoding="utf-8")

# Runtime enhancements: keep original gentle reveal, add proper details accordion, keep only floating WhatsApp.
js=ROOT/"enhancements.js"
txt=js.read_text(encoding="utf-8")
# Remove old custom floating tools block entirely.
start=txt.find(" // Floating WhatsApp + accessibility controls.")
end=txt.find(" // If Material Symbols fails",start)
if start!=-1 and end!=-1:
    txt=txt[:start]+""" // Floating WhatsApp button.
 if(!document.querySelector('.gt-floating-wa')){
   const a=document.createElement('a');a.className='gt-floating-wa';a.href='https://wa.me/972535324962';a.target='_blank';a.rel='noopener noreferrer';a.setAttribute('aria-label',isEn?'Chat on WhatsApp':'שיחה ב-WhatsApp');a.textContent='WA';document.body.appendChild(a);
 }
 // Native details FAQ: one open at a time, without hiding siblings.
 document.querySelectorAll('details').forEach(d=>{
   d.addEventListener('toggle',()=>{
     if(!d.open)return;
     const scope=d.closest('section')||document;
     scope.querySelectorAll('details[open]').forEach(other=>{if(other!==d)other.open=false});
   });
 });
""" + txt[end:]
js.write_text(txt,encoding="utf-8")

css=ROOT/"production.css"
c=css.read_text(encoding="utf-8")
c += r"""
/* Original-design cleanup pass */
.gt-unified-header{direction:inherit}
.gt-header-inner{gap:14px}
.gt-main-nav{min-width:0;white-space:nowrap}
.gt-main-nav a{font-size:.875rem}
.gt-header-actions{flex:0 0 auto}
.gt-header-phone,.gt-phone-number{direction:ltr!important;unicode-bidi:isolate!important;white-space:nowrap!important}
.gt-mobile-phone-strip{display:none;direction:ltr;unicode-bidi:isolate;text-align:center;text-decoration:none;background:#e3ece5;color:#1d3326;padding:5px 12px;font-weight:700;font-size:.82rem;border-top:1px solid rgba(29,51,38,.10)}
.gt-contact-list li{display:flex;align-items:baseline;gap:5px;flex-wrap:wrap}
.gt-contact-list li>span{font-weight:700;color:#fff}
.gt-service-contact-cta{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:18px}
.gt-service-contact-primary,.gt-service-contact-phone{display:inline-flex;align-items:center;justify-content:center;min-height:46px;border-radius:999px;padding:0 20px;font-weight:700;text-decoration:none}
.gt-service-contact-primary{background:#2d5a43;color:#fff}.gt-service-contact-phone{border:1px solid #2d5a43;color:#2d5a43;background:#fff}
.gt-simple-form{display:grid;gap:14px}.gt-simple-form-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.gt-simple-form label{display:grid;gap:6px;font-weight:700;color:#1d3326}.gt-simple-form input,.gt-simple-form textarea{width:100%;padding:12px 13px;border-radius:10px;border:1px solid #ccc6bb;background:#fff;color:#211a14;font:inherit}.gt-simple-submit{justify-self:start;min-width:110px;border:0;border-radius:999px;background:#2d5a43;color:#fff;padding:12px 24px;font-weight:800;cursor:pointer}
.gt-floating-wa{position:fixed;z-index:90;right:18px;bottom:calc(18px + env(safe-area-inset-bottom));width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#25D366;color:#fff!important;border:2px solid #fff;box-shadow:0 9px 26px rgba(0,0,0,.22);font-weight:900;text-decoration:none!important}
details>summary{user-select:none}
details[open]>summary{margin-bottom:4px}
details>p,details>div:not(:first-child){animation:gtFaqIn .22s ease both}
@keyframes gtFaqIn{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:none}}
main h1,main h2,main h3{text-wrap:balance}
main p{text-wrap:pretty}
@media(max-width:1100px){
 .gt-main-nav{gap:12px!important}.gt-main-nav a{font-size:.80rem!important}
 .gt-plan-event{display:none!important}
}
@media(max-width:1023px){
 .gt-mobile-menu-toggle{display:inline-flex!important}
 .gt-mobile-phone-strip{display:block}
 .gt-mobile-panel{top:104px}
}
@media(max-width:767px){
 .gt-header-inner{padding:8px 12px!important;min-height:66px!important}
 .gt-brand-link{max-width:118px!important}.gt-header-logo{width:112px!important;height:44px!important}
 .gt-header-actions{gap:6px!important}
 .gt-simple-form-grid{grid-template-columns:1fr}
 .gt-simple-submit{width:100%}
 .gt-service-contact-cta{display:grid}.gt-service-contact-primary,.gt-service-contact-phone{width:100%}
 .gt-footer-grid{gap:24px!important}
 main h1{font-size:clamp(2rem,9.5vw,2.8rem)!important;line-height:1.08!important}
 main h2{font-size:clamp(1.65rem,7.5vw,2.2rem)!important;line-height:1.15!important}
 main h3{line-height:1.22!important}
 .gt-floating-wa{right:12px;bottom:calc(12px + env(safe-area-inset-bottom));width:50px;height:50px}
}
"""
css.write_text(c,encoding="utf-8")
print("Restored Stitch design and applied focused cleanup.")
