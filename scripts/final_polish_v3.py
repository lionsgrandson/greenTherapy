#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment
import json, re

ROOT=Path(__file__).resolve().parents[1]
HE=["index.html","spa.html","ice-bath.html","workshops.html","healthy-bar.html","about.html","gallery.html","contact.html"]
ALL=HE+[f"en/{p}" for p in HE]
PHONE_DISPLAY="+972 53-532-4962"
PHONE_TEL="+972535324962"
WA="https://wa.me/972535324962"
GOOGLE_BUSINESS="https://share.google/hEvKhs5USb65ZEgi7"
EMAIL="alongreentherapy@gmail.com"

TECH_LABELS=[
    "Content & Email","Direct Email Option","Links Column","Brand & Mission","Corporate Services Column",
    "Shared Component","JSON Conformance","Form (7 cols)","Image Area (5 cols)","B2B CONTACT",
    "Service links","Corporate Services","FOOTER COMPONENT","TOP APP BAR"
]

HE_REPL={
 "Book Now":"לתכנון אירוע",
 "מעדיפים ליצור קשר ישי":"מעדיפים ליצור קשר ישירות",
}
EN_REPL={
 "Receiving an offer adapted to the organization":"Get a Tailored Proposal",
 "Sending a request for a quote":"Request a Proposal",
 "Direct contact":"Contact us directly",
 "quiet head":"Peace of mind",
 "Superfood and smoothie stands":"Healthy Bar",
 "Book Now":"Plan an Event",
}

REVIEWS_HE=[
 "מבסוטים לאללה, היו תגובות חמות. תודה רבה על הכל. נדבר עוד באירוע הבא 😉",
 "כולן הספיקו וכולן נהנו. תודה לך אלון על הכל! למרות הבלת״ם, קיבלתי הרבה מחמאות.",
 "היה מעולה ממש. פידבקים מעולים על המטפלות והיחס. תודה רבה 🙏",
 "וואו, היה לנו פשוט מושלם באמת. עפנו עליה בטירוף — יצאנו מבסוטיות ממש, ויש לה סבלנות מדהימה ❤️",
]
REVIEWS_EN=[
 "Everyone was really happy and the feedback was warm. Thank you for everything — we'll talk again for the next event.",
 "Everyone got a treatment and everyone enjoyed it. Thank you, Alon, for everything. I received so many compliments.",
 "It was excellent. We received great feedback about the therapists and the way everyone was treated. Thank you.",
 "It was genuinely perfect. We absolutely loved it, left very happy, and the therapist had incredible patience.",
]

def prefix(path): return "../" if path.startswith("en/") else ""
def is_en(path): return path.startswith("en/")

def text_replace(soup,mapping):
    for node in list(soup.find_all(string=True)):
        if isinstance(node,Comment) or not isinstance(node,NavigableString): continue
        if node.parent and node.parent.name in {"script","style"}: continue
        old=str(node); new=old
        for a,b in mapping.items(): new=new.replace(a,b)
        if new!=old: node.replace_with(new)

def remove_tech_labels(soup):
    for node in list(soup.find_all(string=True)):
        if isinstance(node,Comment) or not isinstance(node,NavigableString): continue
        s=" ".join(str(node).split())
        if not s: continue
        if any(x.lower() in s.lower() for x in TECH_LABELS):
            # Only remove short implementation labels, never substantive paragraphs.
            if len(s)<120:
                node.extract()

def replace_brand(soup,path):
    header=soup.find("header")
    if not header:return
    candidates=[]
    for a in header.find_all("a"):
        href=a.get("href","")
        txt=a.get_text(" ",strip=True)
        if href.endswith("index.html") and ("Green Therapy" in txt or not candidates):
            candidates.append(a)
    if not candidates:return
    a=candidates[0]
    a.clear()
    a["class"]=["gt-brand-link"]
    a["aria-label"]="Green Therapy — Home" if is_en(path) else "Green Therapy — דף הבית"
    img=soup.new_tag("img",src=prefix(path)+"assets/green-therapy-logo.webp",alt="Green Therapy")
    img["class"]=["gt-header-logo"]
    img["width"]="170"; img["height"]="106"
    a.append(img)

def set_logo_meta(soup,path):
    head=soup.head
    if not head:return
    # remove invalid placeholder Search Console token; deployment guide remains.
    for m in list(head.find_all("meta",attrs={"name":"google-site-verification"})): m.decompose()
    # favicon / touch icon
    if not head.find("link",rel=lambda v:v and "icon" in v):
        head.append(soup.new_tag("link",rel="icon",href=prefix(path)+"assets/green-therapy-logo.webp",type="image/webp"))
    # structured data update
    for tag in head.find_all("script",attrs={"type":"application/ld+json"}):
        try:
            data=json.loads(tag.string or "{}")
            if isinstance(data,dict) and data.get("@type")=="Organization":
                data["telephone"]=PHONE_DISPLAY
                data["logo"]="https://green-therapy.netlify.app/assets/green-therapy-logo.webp"
                data["sameAs"]=[GOOGLE_BUSINESS]
                tag.string=json.dumps(data,ensure_ascii=False)
        except Exception: pass

def fix_critical_links(soup,path):
    en=is_en(path)
    for a in soup.find_all("a"):
        txt=" ".join(a.get_text(" ",strip=True).split())
        href=a.get("href","")
        title=a.get("title","")
        if not en and "Book Now" in txt:
            for n in a.find_all(string=True):
                if "Book Now" in str(n): n.replace_with(str(n).replace("Book Now","לתכנון אירוע"))
        if en and txt=="Book Now":
            a.string="Plan an Event"
        if "וואטסאפ" in title.lower() or "whatsapp" in title.lower():
            a["href"]=WA; a["target"]="_blank"; a["rel"]="noopener noreferrer"
        # mailto links with a phone icon were implementation mistakes.
        icon=a.find(class_=lambda c:c and "material-symbols-outlined" in c if isinstance(c,str) else False)
        if href.startswith("mailto:") and icon and icon.get_text(strip=True) in {"phone","call","chat"}:
            if icon.get_text(strip=True) in {"phone","call"}:
                a["href"]="tel:"+PHONE_TEL
        if href=="#":
            a["href"]="contact.html" if txt else "index.html"
        if href.startswith("#") and href!="#":
            target=href[1:]
            if not soup.find(id=target):
                a["href"]="contact.html"

def fix_call_rows(soup):
    for icon in soup.find_all("span",class_=lambda c:c and "material-symbols-outlined" in c if isinstance(c,str) else False):
        if icon.get_text(strip=True) not in {"call","phone"}: continue
        parent=icon.parent
        if not parent: continue
        if EMAIL in parent.get_text(" ",strip=True):
            for node in list(parent.find_all(string=True)):
                if EMAIL in str(node): node.replace_with(str(node).replace(EMAIL,PHONE_DISPLAY))

def polish_workshops(soup,path):
    en=is_en(path)
    # Remove stray technical labels already handled; rebuild the left contact column cleanly.
    section=soup.find(id="b2b-contact")
    if not section:return
    grid=section.find("div",class_=lambda c:c and "lg:grid-cols-12" in c if isinstance(c,str) else False)
    if not grid:return
    left=None
    for d in grid.find_all("div",recursive=False):
        cls=" ".join(d.get("class",[]))
        if "lg:col-span-5" in cls: left=d; break
    if not left:return
    title="Get a Tailored Proposal" if en else "קבלת הצעה מותאמת לארגון"
    copy=("Tell us about your event, budget and number of participants, and we'll build the right mix of workshops and experiences."
          if en else "שתפו אותנו באופי האירוע, התקציב וכמות המשתתפים ונבנה יחד את תפריט הסדנאות והחוויות המתאים.")
    email_label="Email" if en else "מייל"
    phone_label="Phone" if en else "טלפון"
    wa_label="WhatsApp" if en else "WhatsApp"
    left.clear()
    frag=BeautifulSoup(f"""
      <h2 class="font-headline-lg text-headline-lg font-bold text-on-surface">{title}</h2>
      <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">{copy}</p>
      <div class="gt-direct-contact">
        <a href="tel:{PHONE_TEL}"><strong>{phone_label}</strong><span dir="ltr">{PHONE_DISPLAY}</span></a>
        <a href="{WA}" target="_blank" rel="noopener noreferrer"><strong>{wa_label}</strong><span>{'Message us' if en else 'שליחת הודעה'}</span></a>
        <a href="mailto:{EMAIL}"><strong>{email_label}</strong><span>{EMAIL}</span></a>
      </div>
    ""","html.parser")
    for ch in list(frag.contents): left.append(ch)

def fix_healthy_image(soup,path):
    if Path(path).name!="index.html": return
    node=soup.find(string=lambda s:s and (("קולינריה בריאה ומעוצבת" in s) if not is_en(path) else ("Healthy and designed cuisine" in s)))
    if not node:return
    box=node.parent
    while box and not box.find("img"): box=box.parent
    if box:
        img=box.find("img")
        img["src"]=prefix(path)+"assets/client/95941eaf-fc13-49b4-a515-c9d66f1fdb6e.webp"
        img["alt"]="Smiling Green Therapy practitioner at a wellness event" if is_en(path) else "מטפלת Green Therapy באירוע Wellness"
        img["style"]="object-position:center 24%;"

def replace_reviews(soup,path):
    if Path(path).name!="index.html": return
    old=soup.find(id="recommendations")
    if not old:return
    en=is_en(path)
    reviews=REVIEWS_EN if en else REVIEWS_HE
    title="What clients said after their events" if en else "מה לקוחות כתבו אחרי האירוע"
    sub="Feedback taken from client messages after Green Therapy events." if en else "פידבקים מתוך הודעות שנשלחו ל-Green Therapy אחרי אירועים."
    cards=[]
    for r in reviews:
        cards.append(f"""<article class="gt-review-card">
          <div class="gt-stars" aria-label="5 out of 5 stars">★★★★★</div>
          <blockquote>{r}</blockquote>
          <p>{'Client feedback after an event' if en else 'פידבק מלקוח/ה לאחר אירוע'}</p>
        </article>""")
    html=f"""<section class="py-16 md:py-24 bg-forest-deep text-white" id="recommendations">
      <div class="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop">
        <div class="max-w-2xl mx-auto text-center mb-10">
          <h2 class="font-display text-headline-lg md:text-[36px] font-bold">{title}</h2>
          <p class="font-body-md text-white/75 mt-3">{sub}</p>
        </div>
        <div class="gt-review-grid">{''.join(cards)}</div>
      </div>
    </section>"""
    old.replace_with(BeautifulSoup(html,"html.parser"))

def unified_footer(soup,path):
    old=soup.find("footer")
    if not old:return
    en=is_en(path); p=prefix(path)
    if en:
        link_title,legal_title,contact_title="Links","Legal","Contact"
        links=[("index.html","Home"),("spa.html","Pop-Up Spa"),("ice-bath.html","Ice Baths"),("workshops.html","Mind & Body"),("healthy-bar.html","Healthy Bar"),("gallery.html","Gallery")]
        legal=[("privacy.html","Privacy Policy"),("accessibility.html","Accessibility")]
        gb="Google Business"
    else:
        link_title,legal_title,contact_title="קישורים","משפטי","צור קשר"
        links=[("index.html","דף הבית"),("spa.html","Pop-Up Spa"),("ice-bath.html","אמבטיות קרח"),("workshops.html","Mind & Body"),("healthy-bar.html","בר בריאות"),("gallery.html","גלריה")]
        legal=[("privacy.html","מדיניות פרטיות"),("accessibility.html","הצהרת נגישות")]
        gb="Google Business"
    link_html="".join(f'<li><a href="{h}">{t}</a></li>' for h,t in links)
    legal_html="".join(f'<li><a href="{h}">{t}</a></li>' for h,t in legal)
    html=f"""<footer class="gt-footer">
      <div class="gt-footer-grid">
        <div class="gt-footer-brand">
          <a href="index.html" aria-label="Green Therapy"><img src="{p}assets/green-therapy-logo.webp" alt="Green Therapy" loading="lazy"></a>
        </div>
        <div><h2>{link_title}</h2><ul>{link_html}</ul></div>
        <div><h2>{legal_title}</h2><ul>{legal_html}</ul></div>
        <div><h2>{contact_title}</h2><ul>
          <li><a href="tel:{PHONE_TEL}" dir="ltr">{PHONE_DISPLAY}</a></li>
          <li><a href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{GOOGLE_BUSINESS}" target="_blank" rel="noopener noreferrer">{gb}</a></li>
        </ul></div>
      </div>
    </footer>"""
    old.replace_with(BeautifulSoup(html,"html.parser"))

def process(path):
    f=ROOT/path
    soup=BeautifulSoup(f.read_text(encoding="utf-8"),"html.parser")
    text_replace(soup, EN_REPL if is_en(path) else HE_REPL)
    remove_tech_labels(soup)
    replace_brand(soup,path)
    set_logo_meta(soup,path)
    fix_critical_links(soup,path)
    fix_call_rows(soup)
    polish_workshops(soup,path)
    fix_healthy_image(soup,path)
    replace_reviews(soup,path)
    unified_footer(soup,path)
    f.write_text(str(soup),encoding="utf-8")

for p in ALL: process(p)

# Shared CSS append/override.
css_path=ROOT/"production.css"
css=css_path.read_text(encoding="utf-8")
css += r"""
/* Final production polish */
.gt-brand-link{display:flex;align-items:center;flex:0 0 auto;max-width:190px}
.gt-header-logo{display:block;width:150px;height:58px;object-fit:contain;background:#fff;border-radius:10px}
.gt-footer{background:#1d3326!important;color:#fff!important;padding:46px 20px!important}
.gt-footer-grid{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1.1fr 1fr 1fr 1.25fr;gap:38px;align-items:start}
.gt-footer h2{font-size:1rem!important;font-weight:800!important;color:#dce9df!important;margin:0 0 14px!important}
.gt-footer ul{list-style:none!important;margin:0!important;padding:0!important;display:grid;gap:9px}
.gt-footer a{color:rgba(255,255,255,.84)!important;text-decoration:none!important;overflow-wrap:anywhere}
.gt-footer a:hover{text-decoration:underline!important;text-underline-offset:4px;color:#fff!important}
.gt-footer-brand img{width:min(220px,100%);height:auto;background:white;border-radius:14px;display:block}
.gt-review-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;max-width:980px;margin:0 auto}
.gt-review-card{background:#fff;color:#211a14;border-radius:20px;padding:26px;box-shadow:0 10px 30px rgba(0,0,0,.12);min-width:0}
.gt-review-card blockquote{font-size:1.05rem;line-height:1.75;margin:8px 0 16px}
.gt-review-card p{font-size:.82rem;color:#625c54;margin:0}
.gt-stars{color:#9a6b35;letter-spacing:.12em;font-size:1.15rem}
.gt-direct-contact{display:grid;gap:10px;padding-top:8px}
.gt-direct-contact a{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;padding:13px 15px;border:1px solid rgba(29,51,38,.16);background:#fff;border-radius:14px;text-decoration:none;color:#1d3326}
.gt-direct-contact a span{overflow-wrap:anywhere;word-break:break-word}
.gt-floating-tools{position:fixed;z-index:90;right:18px;bottom:calc(20px + env(safe-area-inset-bottom));display:flex;flex-direction:column;gap:10px}
.gt-float-btn{width:54px;height:54px;border-radius:999px;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(0,0,0,.2);border:2px solid rgba(255,255,255,.85);font-weight:900;text-decoration:none!important;cursor:pointer}
.gt-wa-btn{background:#25D366;color:white!important;font-size:.88rem}
.gt-a11y-btn{background:#1d3326;color:#fff;font-size:1.45rem}
.gt-a11y-panel{position:fixed;z-index:95;right:18px;bottom:calc(146px + env(safe-area-inset-bottom));width:min(330px,calc(100vw - 36px));background:#fff;color:#211a14;border:1px solid #c8d5cb;border-radius:18px;box-shadow:0 18px 50px rgba(0,0,0,.22);padding:16px;display:none}
.gt-a11y-panel.is-open{display:block}
.gt-a11y-panel h2{font-size:1.05rem;margin:0 0 12px;color:#1d3326}
.gt-a11y-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.gt-a11y-actions button,.gt-a11y-panel a{border:1px solid #c8d5cb;border-radius:10px;background:#f7fbf8;color:#1d3326;padding:10px;font:inherit;font-weight:700;text-align:center;text-decoration:none;cursor:pointer}
html.gt-large-text{font-size:112%}
html.gt-high-contrast body{filter:contrast(1.22)}
html.gt-no-motion *,html.gt-no-motion *::before,html.gt-no-motion *::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}
@media(max-width:900px){.gt-footer-grid{grid-template-columns:1fr 1fr}.gt-footer-brand{grid-column:1/-1}.gt-review-grid{grid-template-columns:1fr}}
@media(max-width:767px){
 .gt-brand-link{max-width:128px;flex:1}
 .gt-header-logo{width:122px;height:48px;border-radius:8px}
 header>div{min-height:68px!important}
 .gt-footer{padding:36px 18px!important}
 .gt-footer-grid{grid-template-columns:1fr;gap:28px}
 .gt-footer-brand{grid-column:auto}
 .gt-footer-brand img{width:180px}
 .gt-floating-tools{right:12px;bottom:calc(14px + env(safe-area-inset-bottom))}
 .gt-float-btn{width:50px;height:50px}
 .gt-a11y-panel{right:12px;bottom:calc(128px + env(safe-area-inset-bottom))}
}
"""
css_path.write_text(css,encoding="utf-8")

# Runtime: preserve existing functionality and add floating WhatsApp/accessibility + resilient icon fallbacks.
js_path=ROOT/"enhancements.js"
js=js_path.read_text(encoding="utf-8")
insert=r"""
 // Floating WhatsApp + accessibility controls.
 if(!document.querySelector('.gt-floating-tools')){
   const tools=document.createElement('div');tools.className='gt-floating-tools';
   tools.innerHTML='<a class="gt-float-btn gt-wa-btn" href="https://wa.me/972535324962" target="_blank" rel="noopener noreferrer" aria-label="'+(isEn?'Chat on WhatsApp':'שיחה ב-WhatsApp')+'">WA</a><button type="button" class="gt-float-btn gt-a11y-btn" aria-expanded="false" aria-label="'+(isEn?'Accessibility options':'אפשרויות נגישות')+'">♿</button>';
   document.body.appendChild(tools);
   const panel=document.createElement('div');panel.className='gt-a11y-panel';panel.setAttribute('role','dialog');panel.setAttribute('aria-label',isEn?'Accessibility options':'אפשרויות נגישות');
   panel.innerHTML='<h2>'+(isEn?'Accessibility':'נגישות')+'</h2><div class="gt-a11y-actions"><button type="button" data-a="text">'+(isEn?'Larger text':'טקסט גדול')+'</button><button type="button" data-a="contrast">'+(isEn?'High contrast':'ניגודיות גבוהה')+'</button><button type="button" data-a="motion">'+(isEn?'Reduce motion':'הפחתת תנועה')+'</button><button type="button" data-a="reset">'+(isEn?'Reset':'איפוס')+'</button></div><a style="display:block;margin-top:8px" href="'+(isEn?'accessibility.html':'accessibility.html')+'">'+(isEn?'Accessibility statement':'הצהרת נגישות')+'</a>';
   document.body.appendChild(panel);
   const btn=tools.querySelector('.gt-a11y-btn');
   btn.addEventListener('click',()=>{const open=panel.classList.toggle('is-open');btn.setAttribute('aria-expanded',String(open))});
   panel.addEventListener('click',e=>{const b=e.target.closest('button[data-a]');if(!b)return;const root=document.documentElement;const a=b.dataset.a;if(a==='text')root.classList.toggle('gt-large-text');if(a==='contrast')root.classList.toggle('gt-high-contrast');if(a==='motion')root.classList.toggle('gt-no-motion');if(a==='reset')root.classList.remove('gt-large-text','gt-high-contrast','gt-no-motion')});
 }
 // If Material Symbols fails to load, replace critical raw icon names instead of showing implementation words.
 if(document.fonts){document.fonts.ready.then(()=>{if(document.fonts.check('16px "Material Symbols Outlined"'))return;const map={chat:'💬',call:'☎',phone:'☎',mail:'✉',location_on:'⌖',calendar_today:'▣',spa:'✦',send:'➜',north_east:'↗',arrow_back:'←',arrow_forward:'→',check_circle:'✓',verified:'✓'};document.querySelectorAll('.material-symbols-outlined').forEach(el=>{const k=el.textContent.trim();if(map[k])el.textContent=map[k];else el.textContent=''})})}
"""
const marker=" // Analytics is dormant until an ID is configured AND the visitor consents.";
if(!js.includes("Floating WhatsApp + accessibility controls.")) js=js.replace(marker,insert+"\n"+marker);
js_path.write_text(js,encoding="utf-8")

print("Final polish complete")
