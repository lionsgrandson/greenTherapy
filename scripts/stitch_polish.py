#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment
import re, json

ROOT=Path(__file__).resolve().parents[1]
HE=["index.html","spa.html","ice-bath.html","workshops.html","healthy-bar.html","about.html","contact.html"]
EN=[f"en/{p}" for p in HE]
ALL=HE+EN
PHONE_DISPLAY="+972 53-532-4962"
PHONE_TEL="+972535324962"
WA="https://wa.me/972535324962"
EMAIL="alongreentherapy@gmail.com"
MAP="https://share.google/hEvKhs5USb65ZEgi7"

IMG={
 "hero":"assets/client/887e1d9b-94c2-49aa-b3b9-258f57aacf3c.webp",
 "spa":"assets/client/fe5e6cfc-8689-4287-8189-7286edf4bb30.webp",
 "ice":"assets/client/1c3d140a-38a4-4aff-8196-9fea60c15ae3.webp",
 "workshops":"assets/client/827ed1a7-ce8f-428f-91c1-20ac014453bf.webp",
 "healthy":"assets/client/95941eaf-fc13-49b4-a515-c9d66f1fdb6e.webp",
}
def pref(en): return "../" if en else ""
def page_name(path): return Path(path).name

NAV_HE=[
 ("index.html","בית"),("spa.html","ספא פופ-אפ"),("ice-bath.html","אמבטיות קרח"),
 ("workshops.html","סדנאות גוף ונפש"),("healthy-bar.html","בר בריאות"),
 ("about.html","אודות"),("contact.html","צור קשר")
]
NAV_EN=[
 ("index.html","Home"),("spa.html","Pop-Up Spa"),("ice-bath.html","Ice Baths"),
 ("workshops.html","Mind & Body"),("healthy-bar.html","Healthy Bar"),
 ("about.html","About"),("contact.html","Contact")
]

HE_REPL={
 "שליחת פרטים וקבלת הצעה מיידית":"שליחת פרטים וקבלת הצעה",
 "קבלת הצעה מיידית":"קבלת הצעה",
 "Mind & Body":"סדנאות גוף ונפש",
 "Pop-Up Spa":"ספא פופ-אפ",
 "בואו נבנה חוויה":"לתכנון אירוע",
 "בואו נבנה את החוויה שלכם":"לתכנון אירוע",
}
EN_REPL={
 "immediate proposal":"proposal",
 "Get an immediate proposal":"Get a Proposal",
 "Build Your Experience":"Plan an Event",
 "For all experiences and complexes":"Explore Experiences",
 "full 360° shell":"complete production setup",
 "zero worries and maximum wow":"a smooth, polished experience",
}
HERO_BADGES_HE=["יוגה, מדיטציה ומיינדפולנס","Sound Healing והרצאות העשרה","באירוע החברה שלכם","באירוע שלכם","מתחם עיסויים","דף הבית","מתחם טיפולים"]
HERO_BADGES_EN=["Yoga, Meditation and Mindfulness","Sound Healing and enrichment lectures","At your company event","At your event","Massage complex"]

def replace_text_nodes(soup,mapping):
    for n in list(soup.find_all(string=True)):
        if isinstance(n,Comment) or not isinstance(n,NavigableString): continue
        if n.parent and n.parent.name in {"script","style"}: continue
        s=str(n); t=s
        for a,b in mapping.items(): t=t.replace(a,b)
        if t!=s: n.replace_with(t)

def make_header(soup,en,page):
    old=soup.find("header")
    if not old:return
    nav=NAV_EN if en else NAV_HE
    p=pref(en)
    lang_href=("../"+page if en else "en/"+page)
    html=f"""
<header class="gt-uniform-header sticky top-0 z-50 bg-surface-bright/95 backdrop-blur-md border-b border-outline-variant/30">
  <div class="gt-header-inner max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop">
    <a class="gt-brand-link" href="index.html" aria-label="Green Therapy"><img class="gt-header-logo" src="{p}assets/green-therapy-logo.webp" alt="Green Therapy"></a>
    <nav class="gt-desktop-nav" aria-label="{'Primary navigation' if en else 'ניווט ראשי'}">
      {''.join(f'<a href="{h}">{l}</a>' for h,l in nav)}
    </nav>
    <div class="gt-header-actions">
      <a class="gt-header-phone" href="tel:{PHONE_TEL}" aria-label="{'Call Green Therapy' if en else 'חיוג ל-Green Therapy'}"><span class="material-symbols-outlined">call</span><bdi dir="ltr">{PHONE_DISPLAY}</bdi></a>
      <a class="gt-lang" data-lang-switch href="{lang_href}">{'HE' if en else 'EN'}</a>
      <a class="gt-plan" href="contact.html">{'Plan an Event' if en else 'לתכנון אירוע'}</a>
      <button class="gt-menu-toggle" type="button" aria-expanded="false" aria-label="{'Open menu' if en else 'פתיחת תפריט'}"><span class="material-symbols-outlined">menu</span></button>
    </div>
  </div>
  <a class="gt-mobile-phone" href="tel:{PHONE_TEL}"><span>{'Phone:' if en else 'טלפון:'}</span><bdi dir="ltr">{PHONE_DISPLAY}</bdi></a>
  <nav class="gt-mobile-nav" aria-label="{'Mobile navigation' if en else 'ניווט במובייל'}">{''.join(f'<a href="{h}">{l}</a>' for h,l in nav)}</nav>
</header>"""
    old.replace_with(BeautifulSoup(html,"html.parser"))

def make_footer(soup,en):
    old=soup.find("footer")
    if not old:return
    nav=NAV_EN if en else NAV_HE
    p=pref(en)
    html=f"""
<footer class="gt-footer">
 <div class="gt-footer-grid">
   <div class="gt-footer-brand"><a href="index.html" aria-label="Green Therapy"><img src="{p}assets/green-therapy-logo.webp" alt="Green Therapy" loading="lazy"></a></div>
   <div><h2>{'Links' if en else 'קישורים'}</h2><ul>{''.join(f'<li><a href="{h}">{l}</a></li>' for h,l in nav)}</ul></div>
   <div><h2>{'Legal' if en else 'משפטי'}</h2><ul><li><a href="privacy.html">{'Privacy Policy' if en else 'מדיניות פרטיות'}</a></li><li><a href="accessibility.html">{'Accessibility' if en else 'הצהרת נגישות'}</a></li></ul></div>
   <div><h2>{'Contact' if en else 'צור קשר'}</h2><ul class="gt-footer-contact">
     <li><strong>{'Phone' if en else 'טלפון'}:</strong> <a href="tel:{PHONE_TEL}"><bdi dir="ltr">{PHONE_DISPLAY}</bdi></a></li>
     <li><strong>{'Email' if en else 'מייל'}:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
     <li><strong>{'Address' if en else 'כתובת'}:</strong> <a href="{MAP}" target="_blank" rel="noopener noreferrer">{'View on Google' if en else 'לצפייה במפה'}</a></li>
   </ul></div>
 </div>
</footer>"""
    old.replace_with(BeautifulSoup(html,"html.parser"))

def set_image_near_text(soup,texts,src,en):
    for txt in texts:
        n=soup.find(string=lambda s:s and txt.lower() in str(s).lower())
        if not n: continue
        cur=n.parent
        for _ in range(7):
            if not cur:break
            img=cur.find("img")
            if img:
                img["src"]=pref(en)+src
                img["loading"]="lazy";img["decoding"]="async"
                return True
            cur=cur.parent
    return False

def page_images(soup,en,page):
    # Keep the original Stitch composition, only diversify repeated photography.
    if page=="index.html":
        set_image_near_text(soup,["Pop-Up Spa","ספא פופ-אפ"],IMG["spa"],en)
        set_image_near_text(soup,["סדנאות מעשיות ומרתקות","Practical","workshops"],IMG["workshops"],en)
        set_image_near_text(soup,["קולינריה בריאה ומעוצבת","Healthy and","Healthy,","culinary"],IMG["healthy"],en)
    elif page=="spa.html":
        for img in soup.find_all("img"):
            if "887e1d9b" in img.get("src",""): img["src"]=pref(en)+IMG["spa"]
    elif page=="ice-bath.html":
        main=soup.find("main") or soup
        first=main.find("img")
        if first:first["src"]=pref(en)+IMG["ice"]
    elif page=="workshops.html":
        main=soup.find("main") or soup
        first=main.find("img")
        if first:first["src"]=pref(en)+IMG["workshops"]
    elif page=="healthy-bar.html":
        main=soup.find("main") or soup
        first=main.find("img")
        if first:
            first["src"]=pref(en)+IMG["healthy"];first["class"]=list(dict.fromkeys(first.get("class",[])+["gt-face-focus"]))
    # Replace any broken remote content image with a page-appropriate local photo.
    fallback={"index.html":IMG["hero"],"spa.html":IMG["spa"],"ice-bath.html":IMG["ice"],"workshops.html":IMG["workshops"],"healthy-bar.html":IMG["healthy"],"about.html":IMG["spa"],"contact.html":IMG["workshops"]}.get(page,IMG["hero"])
    for img in soup.find_all("img"):
        src=img.get("src","")
        if "googleusercontent.com" in src: img["src"]=pref(en)+fallback
    imgs=(soup.find("main") or soup).find_all("img")
    for i,img in enumerate(imgs):
        if i==0:
            img["loading"]="eager";img["fetchpriority"]="high"
        else:
            img["loading"]="lazy";img["decoding"]="async"

def remove_hero_badges(soup,en):
    main=soup.find("main")
    if not main:return
    hero=main.find("section")
    if not hero:return
    phrases=HERO_BADGES_EN if en else HERO_BADGES_HE
    for phrase in phrases:
        for n in list(hero.find_all(string=lambda s:s and phrase.lower() in str(s).lower())):
            cur=n.parent
            while cur and cur!=hero:
                if cur.name in {"a","button"}: break
                cls=" ".join(cur.get("class",[]))
                if ("inline-flex" in cls or "items-center" in cls or "rounded-full" in cls) and len(cur.get_text(" ",strip=True))<100:
                    cur.decompose();break
                cur=cur.parent

def balance_ice(soup,en):
    phrases=["חוויית שיא שמחברת","Peak Experience","מעטפת הפקה מלאה","360°","חוויה מודרכת, מקצועית ומעצימה","Guided","Professional"]
    for phrase in phrases:
        n=soup.find(string=lambda s:s and phrase.lower() in str(s).lower())
        if not n: continue
        sec=n.parent
        while sec and sec.name!="section": sec=sec.parent
        if not sec: continue
        grids=sec.find_all("div",class_=lambda c:c and "grid" in c if isinstance(c,str) else False)
        if grids:
            grid=grids[-1] if "מודרכת" in phrase or "Guided" in phrase else grids[0]
            cls=[x for x in grid.get("class",[]) if not re.match(r"(md:|lg:)?grid-cols-",x) and x not in {"relative"}]
            grid["class"]=cls+["grid-cols-1","md:grid-cols-3","gap-6","max-w-5xl","mx-auto"]
        if "מודרכת" in phrase or "Guided" in phrase:
            for d in list(sec.find_all("div")):
                if d.get_text(strip=True) in {"1","2","3","4"}:
                    cls=" ".join(d.get("class",[]))
                    if "rounded-full" in cls: d.decompose()

def convert_faqs(soup):
    for details in list(soup.find_all("details")):
        summary=details.find("summary")
        if not summary:continue
        q=summary.get_text(" ",strip=True)
        answer=[]
        for child in list(details.contents):
            if child is summary:continue
            answer.append(str(child))
        html=f'<div class="gt-faq-item"><button class="gt-faq-question" type="button" aria-expanded="false"><span>{q}</span><span class="material-symbols-outlined gt-faq-chevron">expand_more</span></button><div class="gt-faq-answer"><div class="gt-faq-answer-inner">{"".join(answer)}</div></div></div>'
        details.replace_with(BeautifulSoup(html,"html.parser"))

def simplify_forms(soup,en,page):
    forms=list(soup.find_all("form"))
    for form in forms:
        if page!="contact.html":
            html=f'''<div class="gt-simple-contact-cta"><h3>{"Let’s plan your event" if en else "בואו נתכנן את האירוע"}</h3><p>{"Call us directly or leave details on the contact page." if en else "אפשר לדבר איתנו ישירות או להשאיר פרטים בעמוד יצירת הקשר."}</p><div><a class="gt-phone-button" href="tel:{PHONE_TEL}"><span class="material-symbols-outlined">call</span><bdi dir="ltr">{PHONE_DISPLAY}</bdi></a><a class="gt-contact-button" href="contact.html">{"Contact" if en else "צור קשר"}</a></div></div>'''
            form.replace_with(BeautifulSoup(html,"html.parser"))
        else:
            html=f'''<form class="gt-simple-form" action="/api/contact" method="post" data-contact-form="true">
<input class="gt-honeypot" type="text" name="company_website" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="gt-form-grid">
<label>{"Full name" if en else "שם מלא"}<input name="name" autocomplete="name" required></label>
<label>{"Company / Organization" if en else "חברה / ארגון"}<input name="company" autocomplete="organization"></label>
<label>{"Phone" if en else "טלפון"}<input name="phone" type="tel" dir="ltr" autocomplete="tel" required></label>
<label>{"Email" if en else "מייל"}<input name="email" type="email" dir="ltr" autocomplete="email"></label>
</div>
<label>{"Tell us briefly about the event" if en else "ספרו לנו בקצרה על האירוע"}<textarea name="message" rows="4"></textarea></label>
<button type="submit" class="gt-form-submit"><span class="material-symbols-outlined">send</span>{"Send" if en else "שלח"}</button>
<div class="gt-form-status" role="status" aria-live="polite"></div>
</form>'''
            form.replace_with(BeautifulSoup(html,"html.parser"))
    # Remove false instant wording anywhere.
    replace_text_nodes(soup,{"מיידית":"","מיידי":"","Immediately":"","immediately":""})
    # "Need more details?" must call, not email.
    needles=["צריכים פרטים נוספים?","Need more details?"]
    for needle in needles:
        n=soup.find(string=lambda s:s and needle.lower() in str(s).lower())
        if n:
            sec=n.parent
            while sec and sec.name!="section":sec=sec.parent
            if sec:
                links=sec.find_all("a")
                if links:
                    a=links[0];a["href"]="tel:"+PHONE_TEL
                    # Replace obvious email icon with phone icon.
                    icon=a.find("span",class_=lambda c:c and "material-symbols-outlined" in c if isinstance(c,str) else False)
                    if icon:icon.string="call"

def clean_comments(soup):
    for c in list(soup.find_all(string=lambda x:isinstance(x,Comment))):
        txt=str(c)
        if any(k in txt for k in ["JSON","Shared Component","cols","Column","B2B","TOP APP BAR","FOOTER COMPONENT"]): c.extract()

def add_common_assets(soup,en):
    if soup.head:
        # External accessibility widget configuration + script, shared site CSS.
        if not soup.head.find("script",src=re.compile("accessibility-widgets")):
            cfg=soup.new_tag("script")
            cfg.string='''window.ACCESSIBILITY_WIDGET_CONFIG={enableVoiceControl:false,enableScreenReader:true,enableHighContrast:true,enableBiggerText:true,enableTextSpacing:true,enablePauseAnimations:true,enableHideImages:true,enableDyslexiaFont:true,enableBiggerCursor:true,enableLineHeight:true,widgetPosition:{side:"left",left:"16px",bottom:"16px"}};'''
            soup.head.append(cfg)
            ext=soup.new_tag("script",src="https://cdn.jsdelivr.net/npm/accessibility-widgets@latest/widget.js",defer=True)
            soup.head.append(ext)

def process(path):
    en=path.startswith("en/")
    page=page_name(path)
    f=ROOT/path
    soup=BeautifulSoup(f.read_text(encoding="utf-8"),"html.parser")
    replace_text_nodes(soup,EN_REPL if en else HE_REPL)
    clean_comments(soup)
    make_header(soup,en,page)
    make_footer(soup,en)
    page_images(soup,en,page)
    remove_hero_badges(soup,en)
    if page=="ice-bath.html": balance_ice(soup,en)
    convert_faqs(soup)
    simplify_forms(soup,en,page)
    add_common_assets(soup,en)
    # Mark sections for restrained reveal animation.
    for sec in soup.find_all("section"): sec["data-gt-reveal"]=""
    f.write_text(str(soup),encoding="utf-8")

for path in ALL:
    process(path)

# Gallery is removed because the currently available approved local photos are too repetitive.
(ROOT/"_redirects").write_text("/gallery.html / 301!\n/gallery / 301!\n/en/gallery.html /en/ 301!\n/en/gallery /en/ 301!\n",encoding="utf-8")

# Remove gallery from sitemap if present.
sm=ROOT/"sitemap.xml"
if sm.exists():
    txt=sm.read_text(encoding="utf-8")
    txt=re.sub(r'\s*<url><loc>[^<]*gallery(?:\.html)?</loc></url>','',txt)
    sm.write_text(txt,encoding="utf-8")

# Shared production CSS appended to the original Stitch styling.
css=ROOT/"production.css"
base=css.read_text(encoding="utf-8") if css.exists() else ""
base += r'''
/* Original Stitch design: uniform shell and production polish */
.gt-uniform-header{font-family:inherit}
.gt-header-inner{min-height:76px;display:flex;align-items:center;gap:18px}
.gt-brand-link{display:flex;align-items:center;flex:0 0 145px}
.gt-header-logo{width:142px;height:58px;object-fit:contain;border-radius:10px;background:#fff}
.gt-desktop-nav{display:flex;align-items:center;justify-content:center;gap:18px;flex:1;min-width:0}
.gt-desktop-nav a{font-size:14px;line-height:1.2;font-weight:700;color:#4a463e;text-decoration:none;white-space:nowrap;padding:8px 2px;border-bottom:2px solid transparent}
.gt-desktop-nav a:hover{color:#1d4b34;border-color:#6f957d}
.gt-header-actions{display:flex;align-items:center;gap:8px}
.gt-header-phone,.gt-lang,.gt-plan{height:40px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;gap:6px;text-decoration:none;font-weight:800;white-space:nowrap}
.gt-header-phone{padding:0 12px;background:#e4eee7;color:#1d4b34;border:1px solid #c7d4ca}.gt-header-phone .material-symbols-outlined{font-size:18px}
.gt-lang{min-width:42px;padding:0 10px;background:#fff;border:1px solid #c7d4ca;color:#1d4b34}
.gt-plan{padding:0 16px;background:#1d4b34;color:#fff}.gt-menu-toggle{display:none;width:42px;height:42px;border-radius:999px;border:1px solid #c7d4ca;background:#e4eee7;color:#1d4b34;align-items:center;justify-content:center}
.gt-mobile-phone,.gt-mobile-nav{display:none}
.gt-phone-number,bdi[dir="ltr"]{unicode-bidi:isolate;direction:ltr}
.gt-footer{background:#1d3326!important;color:#fff!important;padding:46px 20px!important}
.gt-footer-grid{max-width:1180px;margin:auto;display:grid;grid-template-columns:1.05fr 1fr .8fr 1.25fr;gap:36px;align-items:start}
.gt-footer-brand img{width:205px;height:auto;background:#fff;border-radius:14px}
.gt-footer h2{font-size:1rem!important;color:#dce9df!important;font-weight:800!important;margin:0 0 13px!important}
.gt-footer ul{list-style:none!important;margin:0!important;padding:0!important;display:grid;gap:9px}
.gt-footer a{color:rgba(255,255,255,.84)!important;text-decoration:none!important;overflow-wrap:anywhere}.gt-footer a:hover{text-decoration:underline!important}
.gt-footer-contact strong{color:#fff;margin-inline-end:5px}
.gt-simple-contact-cta{background:#fff;border:1px solid rgba(40,88,64,.2);border-radius:20px;padding:26px;text-align:center}
.gt-simple-contact-cta h3{font-size:1.5rem;color:#1d4b34;margin:0 0 7px}.gt-simple-contact-cta p{color:#5c685f;line-height:1.6;margin:0 0 18px}.gt-simple-contact-cta>div{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.gt-phone-button,.gt-contact-button{min-height:44px;padding:0 17px;border-radius:999px;display:inline-flex;align-items:center;gap:7px;text-decoration:none;font-weight:800}.gt-phone-button{background:#e4eee7;color:#1d4b34}.gt-contact-button{background:#1d4b34;color:#fff}
.gt-simple-form{display:grid;gap:15px}.gt-form-grid{display:grid;grid-template-columns:1fr 1fr;gap:13px}.gt-simple-form label{display:grid;gap:6px;font-weight:700;color:#294936}.gt-simple-form input,.gt-simple-form textarea{width:100%;border:1px solid #c8d5cb;background:#fff;border-radius:11px;padding:11px 12px;color:#211a14;font-size:16px}.gt-simple-form input:focus,.gt-simple-form textarea:focus{outline:3px solid rgba(45,90,67,.16);border-color:#2d5a43}.gt-form-submit{justify-self:start;border:0;border-radius:999px;background:#1d4b34;color:#fff;min-height:44px;padding:0 19px;display:inline-flex;gap:7px;align-items:center;font-weight:800;cursor:pointer}.gt-honeypot{position:absolute!important;left:-9999px!important;width:1px!important;height:1px!important;opacity:0!important}.gt-form-status{min-height:22px;font-weight:600;color:#4f5d53}
.gt-faq-item{background:#fff;border:1px solid rgba(40,88,64,.2);border-radius:16px;overflow:hidden;margin-bottom:10px}.gt-faq-question{width:100%;display:flex;align-items:center;justify-content:space-between;gap:16px;text-align:inherit;background:transparent;border:0;padding:18px 20px;font-weight:800;color:#1d4b34;cursor:pointer;font-size:1.05rem}.gt-faq-chevron{transition:transform .28s ease}.gt-faq-item.is-open .gt-faq-chevron{transform:rotate(180deg)}.gt-faq-answer{display:grid;grid-template-rows:0fr;transition:grid-template-rows .34s ease}.gt-faq-answer-inner{overflow:hidden;padding:0 20px;color:#5c685f}.gt-faq-item.is-open .gt-faq-answer{grid-template-rows:1fr}.gt-faq-item.is-open .gt-faq-answer-inner{padding-bottom:18px}
.gt-face-focus{object-position:center 20%!important}
[data-gt-reveal]{opacity:0;transform:translateY(16px);transition:opacity .52s ease,transform .52s cubic-bezier(.2,.8,.2,1)}[data-gt-reveal].gt-visible{opacity:1;transform:none}
main h1{max-width:100%;text-wrap:balance;overflow-wrap:normal}main h2{max-width:100%;text-wrap:balance}.gt-three-balanced{max-width:1050px;margin-inline:auto}
.gt-wa-floating{position:fixed;right:18px;bottom:18px;z-index:999;width:56px;height:56px;border-radius:999px;background:#25D366;color:#fff!important;border:2px solid #fff;box-shadow:0 10px 28px rgba(0,0,0,.2);display:flex;align-items:center;justify-content:center;text-decoration:none;font-weight:900}
@media(max-width:1180px){.gt-desktop-nav{gap:11px}.gt-desktop-nav a{font-size:13px}.gt-header-phone bdi{display:none}.gt-header-phone{width:40px;padding:0}}
@media(max-width:1023px){.gt-desktop-nav,.gt-plan,.gt-header-phone{display:none}.gt-menu-toggle{display:inline-flex}.gt-header-inner{min-height:68px;padding-top:7px!important;padding-bottom:7px!important}.gt-mobile-phone{display:flex;align-items:center;justify-content:center;gap:7px;padding:6px 12px;background:#e4eee7;color:#1d4b34;text-decoration:none;font-size:14px;border-top:1px solid #c7d4ca}.gt-mobile-nav.is-open{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:10px 14px 14px;background:#fff8f5;border-top:1px solid #d6d1c8}.gt-mobile-nav a{padding:11px 12px;border-radius:11px;background:#fff;text-decoration:none;font-weight:800;color:#1d4b34}.gt-header-logo{width:122px;height:50px}.gt-brand-link{flex-basis:125px}}
@media(max-width:767px){main h1{font-size:clamp(2.05rem,10.5vw,3rem)!important;line-height:1.06!important}main h2{font-size:clamp(1.7rem,8vw,2.3rem)!important;line-height:1.12!important}.gt-footer-grid{grid-template-columns:1fr;gap:28px}.gt-footer-brand img{width:175px}.gt-form-grid{grid-template-columns:1fr}.gt-wa-floating{width:52px;height:52px;right:12px;bottom:12px}.gt-simple-contact-cta{padding:22px}.gt-mobile-nav.is-open{grid-template-columns:1fr}.gt-faq-question{font-size:1rem;padding:16px 17px}.gt-faq-answer-inner{padding-inline:17px}}
@media(prefers-reduced-motion:reduce){[data-gt-reveal]{opacity:1;transform:none;transition:none}.gt-faq-answer,.gt-faq-chevron{transition:none!important}}
'''
css.write_text(base,encoding="utf-8")

# Robust shared behavior, deliberately independent of FAQ state.
js=ROOT/"enhancements.js"
js.write_text(r'''(()=>{
const ready=()=>{
 const isEn=document.documentElement.lang==="en"||location.pathname.includes("/en/");
 // Mobile menu
 document.querySelectorAll(".gt-menu-toggle").forEach(btn=>btn.addEventListener("click",()=>{
   const nav=document.querySelector(".gt-mobile-nav");if(!nav)return;
   const open=nav.classList.toggle("is-open");btn.setAttribute("aria-expanded",String(open));
 }));
 // Accordion: only one answer open. No reveal classes are toggled here.
 const items=[...document.querySelectorAll(".gt-faq-item")];
 items.forEach(item=>{
   const btn=item.querySelector(".gt-faq-question");if(!btn)return;
   btn.addEventListener("click",()=>{
     const opening=!item.classList.contains("is-open");
     items.forEach(other=>{if(other!==item){other.classList.remove("is-open");other.querySelector(".gt-faq-question")?.setAttribute("aria-expanded","false")}});
     item.classList.toggle("is-open",opening);btn.setAttribute("aria-expanded",String(opening));
   });
 });
 // Restrained reveal animation.
 const reveal=[...document.querySelectorAll("[data-gt-reveal]")];
 if("IntersectionObserver" in window){
   const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("gt-visible");io.unobserve(e.target)}}),{threshold:.05,rootMargin:"0px 0px -4% 0px"});
   reveal.forEach(el=>io.observe(el));
 } else reveal.forEach(el=>el.classList.add("gt-visible"));
 // Floating WhatsApp button.
 if(!document.querySelector(".gt-wa-floating")){
   const a=document.createElement("a");a.className="gt-wa-floating";a.href="https://wa.me/972535324962";a.target="_blank";a.rel="noopener noreferrer";a.textContent="WA";a.setAttribute("aria-label",isEn?"Chat on WhatsApp":"שיחה ב-WhatsApp");document.body.appendChild(a);
 }
 // Contact forms: honest status only.
 document.querySelectorAll("form[data-contact-form]").forEach(form=>form.addEventListener("submit",async e=>{
   e.preventDefault();const status=form.querySelector(".gt-form-status");if(status)status.textContent=isEn?"Sending…":"שולחים…";
   try{
     const payload=Object.fromEntries(new FormData(form));
     const r=await fetch("/api/contact",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(payload)});
     if(r.ok){if(status)status.textContent=isEn?"Thank you. Your inquiry was sent.":"תודה, הפנייה נשלחה.";form.reset()}
     else if(status)status.innerHTML=isEn?'The form is not connected yet. Please call <a href="tel:+972535324962">+972 53-532-4962</a>.':'הטופס עדיין לא מחובר. אפשר להתקשר ל-<a dir="ltr" href="tel:+972535324962">+972 53-532-4962</a>.';
   }catch{if(status)status.textContent=isEn?"Unable to send right now. Please call us.":"לא ניתן לשלוח כרגע. אפשר להתקשר אלינו."}
 }));
 // If external icon font fails, avoid raw icon words.
 if(document.fonts)document.fonts.ready.then(()=>{if(document.fonts.check('16px "Material Symbols Outlined"'))return;const map={call:"☎",menu:"☰",send:"➜",expand_more:"⌄",calendar_today:"▣",north_east:"↗",chat:"💬",location_on:"⌖",check_circle:"✓",arrow_back:"←",arrow_forward:"→"};document.querySelectorAll(".material-symbols-outlined").forEach(el=>{const k=el.textContent.trim();el.textContent=map[k]||""})});
};
document.readyState==="loading"?document.addEventListener("DOMContentLoaded",ready):ready();
})();''',encoding="utf-8")

print("Original Stitch polish applied")
