#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
import json, re, shutil

ROOT=Path(__file__).resolve().parents[1]
PAGES=["index.html","spa.html","ice-bath.html","workshops.html","healthy-bar.html","about.html","contact.html","privacy.html","accessibility.html"]
EMAIL="alongreentherapy@gmail.com"
PHONE="+972 53-532-4962"

HE_REPL={
 "Green Therapy":"גרין תרפי",
 "Wellness & Wellbeing":"וולנס ווולביינג",
 "Wellness":"וולנס",
 "Wellbeing":"וולביינג",
 "Pop-Up Spa":"ספא פופ-אפ",
 "Pop Up Spa":"ספא פופ-אפ",
 "Mind & Body":"גוף ונפש",
 "Sound Healing":"סאונד הילינג",
 "Peak Energy Experience":"חוויית אנרגיה",
 "Safety First":"בטיחות לפני הכול",
 "HR":"משאבי אנוש",
 "WhatsApp":"וואטסאפ",
 "Google Business":"כתובת",
 "Email":"מייל",
 "Book Now":"לתכנון אירוע",
 "Direct Email Option":"",
 "Content & Email":"",
}
EN_REPL={
 "Frequently asked questions of welfare administrations and producers":"Frequently Asked Questions for Wellbeing, HR & Production Teams",
 "Sewing specifications and pre-registration":"Planning and Treatment Scheduling",
 "Construction, operation and full dismantling":"Setup, Operation and Pack-Down",
 "full 360° shell":"full-service production",
 "full 360° envelope":"full-service production",
 "zero worries and maximum wow":"a smooth, polished experience",
 "in offices, in nature or on a company event":"at the office, outdoors or at your event venue",
 "in the office, in nature or on the event site":"at the office, outdoors or at your event venue",
 "the nature of the event":"the event",
 "welfare administrations":"Wellbeing teams",
 "formation":"team connection",
 "Who handles the event?":"Who provides the treatments?",
 "Classic Swedish massage, relaxing Thai, Shiatsu":"Classic Swedish massage, Thai massage and stretching, Shiatsu",
 "receiving a personalized offer":"getting a tailored proposal",
 "Receiving a personalized offer":"Get a Tailored Proposal",
 "Book Now":"Plan an Event",
}

def visible_direct_text_nodes(el):
    if not isinstance(el,Tag) or el.name in {"script","style","noscript","svg"}: return []
    return [c for c in list(el.children) if isinstance(c,NavigableString) and not isinstance(c,Comment) and str(c).strip()]

def replace_visible_text(soup,mapping):
    for node in list(soup.find_all(string=True)):
        if isinstance(node,Comment) or not isinstance(node,NavigableString): continue
        if node.parent and node.parent.name in {"script","style","noscript","svg"}: continue
        old=str(node); new=old
        for a,b in mapping.items(): new=new.replace(a,b)
        if new!=old: node.replace_with(new)

def remove_section_by_phrase(soup,phrase):
    node=soup.find(string=lambda x:x and phrase in str(x))
    if not node:return
    sec=node.parent
    while sec and getattr(sec,"name",None)!="section": sec=sec.parent
    if sec: sec.decompose()

def prepare_page(soup,lang,page):
    replace_visible_text(soup, HE_REPL if lang=="he" else EN_REPL)

    body=soup.body
    if not body:return soup

    # Remove legacy shared UI. React now owns these pieces so they remain identical everywhere.
    old_header=soup.find("header")
    if old_header: old_header.decompose()
    old_footer=soup.find("footer")
    if old_footer: old_footer.decompose()

    # Remove old form sections; every page gets the exact same shared contact component.
    for form in list(soup.find_all("form")):
        sec=form
        while sec and getattr(sec,"name",None)!="section": sec=sec.parent
        if sec: sec.decompose()
        else: form.decompose()

    if page=="contact.html":
        phrases = ([
          "יצירת קשר מהירה","תיאום אירוע:","סוגי מיקום:","לפני שסוגרים אירוע – הכל שקוף וברור",
          "לפני שסוגרים אירוע - הכל שקוף וברור"
        ] if lang=="he" else [
          "Quick contact","Event coordination:","Location types:","Before closing an event - everything is transparent and clear",
          "Before booking an event"
        ])
        for phrase in phrases: remove_section_by_phrase(soup,phrase)

    # Remove any old floating/custom UI scripts. Keep Tailwind and page-level inline scripts.
    for s in list(soup.find_all("script",src=True)):
        src=s.get("src","")
        if any(x in src for x in ["enhancements.js","shared-components.js","i18n-data.js","accessibility-widgets"]):
            s.decompose()

    # Remove old accessibility config snippets to avoid duplicate widgets.
    for s in list(soup.find_all("script",src=False)):
        txt=s.string or ""
        if "ACCESSIBILITY_WIDGET_CONFIG" in txt: s.decompose()

    # Consistent component roots.
    header_root=soup.new_tag("div",id="gt-header-root")
    skip=soup.find("a",class_=lambda c:c and "gt-skip-link" in c if isinstance(c,str) else False)
    if skip: skip.insert_after(header_root)
    else: body.insert(0,header_root)

    footer_root=soup.new_tag("div",id="gt-footer-root")
    body.append(footer_root)
    contact_root=soup.new_tag("div",id="gt-contact-root")
    footer_root.insert_before(contact_root)

    # Use the same React components in both languages; English is a translation mode on the Hebrew page.
    i18n=soup.new_tag("script",src="i18n-data.js")
    shared=soup.new_tag("script",src="shared-components.js",type="module")
    body.append(i18n); body.append(shared)

    # External accessibility widget (supplementary to semantic accessibility).
    cfg=soup.new_tag("script")
    if lang=="he":
        cfg.string='window.ACCESSIBILITY_WIDGET_CONFIG={enableVoiceControl:false,enableScreenReader:true,enableHighContrast:true,enableBiggerText:true,enableTextSpacing:true,enablePauseAnimations:true,enableHideImages:true,enableDyslexiaFont:true,enableBiggerCursor:true,enableLineHeight:true,widgetPosition:{side:"left",left:"16px",bottom:"16px"},lang:{accessibilityMenu:"תפריט נגישות",closeAccessibilityMenu:"סגירת תפריט נגישות",accessibilityTools:"כלי נגישות",resetAllSettings:"איפוס הגדרות",screenReader:"קורא מסך",highContrast:"ניגודיות גבוהה",biggerText:"טקסט גדול",textSpacing:"ריווח טקסט",pauseAnimations:"עצירת אנימציות",hideImages:"הסתרת תמונות",dyslexiaFriendly:"גופן ידידותי לדיסלקציה",biggerCursor:"סמן גדול",lineHeight:"גובה שורה"}};'
    else:
        cfg.string='window.ACCESSIBILITY_WIDGET_CONFIG={enableVoiceControl:false,enableScreenReader:true,enableHighContrast:true,enableBiggerText:true,enableTextSpacing:true,enablePauseAnimations:true,enableHideImages:true,enableDyslexiaFont:true,enableBiggerCursor:true,enableLineHeight:true,widgetPosition:{side:"left",left:"16px",bottom:"16px"}};'
    ext=soup.new_tag("script",src="https://cdn.jsdelivr.net/npm/accessibility-widgets@latest/widget.js",defer=True)
    body.append(cfg); body.append(ext)

    # Remove gallery links if any survived older versions.
    for a in list(soup.find_all("a",href=lambda h:h and "gallery" in h.lower())): a.decompose()

    # Same page-root metadata.
    body["data-page"]=page
    main=soup.find("main")
    if main: main["id"]="main-content"

    # Phone direction anywhere static.
    for a in soup.find_all("a",href=lambda h:h and h.startswith("tel:")):
        a["dir"]="ltr"; a["class"]=a.get("class",[])+["gt-phone-isolate"]

    # Lazy-load all non-hero images; runtime repeats this safely.
    seen=False
    for img in soup.find_all("img"):
        if "green-therapy-logo" in img.get("src",""): continue
        if not seen and (img.get("loading")=="eager" or img.get("fetchpriority")=="high"):
            seen=True; continue
        img["loading"]="lazy"; img["decoding"]="async"

    return soup

def legal_markup(lang,kind):
    if lang=="he":
        if kind=="privacy":
            title="מדיניות פרטיות"
            body=f"""
            <p>עודכן: ספטמבר 2026.</p>
            <h2>מי מפעיל את האתר</h2><p>האתר מופעל עבור גרין תרפי. לשאלות בנושא פרטיות ניתן לפנות בטלפון {PHONE} או במייל {EMAIL}.</p>
            <h2>מידע שנאסף</h2><p>כאשר אתם פונים דרך האתר, ניתן למסור שם, מספר טלפון, כתובת מייל ופרטים שתבחרו לכתוב על האירוע. בנוסף עשוי להיאסף מידע טכני בסיסי הנדרש לאבטחה ולתפעול האתר.</p>
            <h2>למה המידע משמש</h2><p>המידע משמש למענה לפנייה, התאמת שירות לאירוע, יצירת קשר ותפעול ואבטחת האתר.</p>
            <h2>עוגיות וניתוח שימוש</h2><p>כלי ניתוח אופציונליים, אם יחוברו בעתיד, יופעלו בהתאם להגדרות ההסכמה באתר. אין להפעיל כלי ניתוח אופציונלי לפני הגדרתו ועדכון מדיניות זו בהתאם.</p>
            <h2>שירותים חיצוניים</h2><p>האתר מתארח בשירות חיצוני. לחיצה על קישור לוואטסאפ או למפה מעבירה את המשתמש לשירות של צד שלישי, הכפוף למדיניות הפרטיות שלו.</p>
            <h2>שמירת מידע ואבטחה</h2><p>מידע יישמר רק למשך הזמן הנדרש לצורך הטיפול בפנייה, ניהול הקשר והתחייבויות החלות לפי דין. ננקטים אמצעים סבירים לצמצום גישה בלתי מורשית.</p>
            <h2>פניות בנושא פרטיות</h2><p>ניתן לפנות אלינו כדי לבקש מידע, תיקון או בירור בנוגע למידע שמסרתם, בכפוף לדין החל.</p>
            """
        elif kind=="terms":
            title="תנאי שימוש"
            body=f"""
            <p>עודכן: ספטמבר 2026.</p>
            <h2>השימוש באתר</h2><p>האתר מציג מידע כללי על שירותי גרין תרפי. השימוש באתר מהווה הסכמה לתנאים אלה.</p>
            <h2>מידע, זמינות והצעות</h2><p>המידע באתר אינו הצעה מחייבת. היקף השירות, המחיר, הזמינות, המיקום, הצוות ולוח הזמנים נקבעים רק לאחר תיאום ואישור בכתב מול הלקוח.</p>
            <h2>בריאות ובטיחות</h2><p>פעילויות וולנס עשויות לדרוש התאמה אישית. המשתתפים אחראים למסור מידע רלוונטי ולפעול לפי הנחיות הצוות. אין לראות בתוכן האתר ייעוץ רפואי.</p>
            <h2>קניין רוחני</h2><p>התוכן, העיצוב, התמונות והמיתוג באתר מוגנים בזכויות המתאימות ואין להעתיקם או לעשות בהם שימוש מסחרי ללא אישור.</p>
            <h2>קישורים לשירותים חיצוניים</h2><p>קישורים למפה, וואטסאפ ושירותים חיצוניים ניתנים לנוחות בלבד. השימוש בהם כפוף לתנאים של אותם שירותים.</p>
            <h2>שינויים ואחריות</h2><p>ניתן לעדכן את תוכן האתר והתנאים מעת לעת. האחריות לשירות בפועל נקבעת לפי ההסכמות בכתב מול הלקוח ובכפוף לדין החל.</p>
            <h2>יצירת קשר</h2><p>טלפון: {PHONE}<br/>מייל: {EMAIL}</p>
            """
        else:
            title="הצהרת נגישות"
            body=f"""
            <p>גרין תרפי פועלת לשפר את נגישות האתר ולאפשר שימוש נוח ככל האפשר במקלדת, במסכי קורא ובתצוגות שונות.</p>
            <h2>התאמות באתר</h2><p>האתר כולל מבנה סמנטי, קישור דילוג לתוכן, ניגודיות, טקסט חלופי לתמונות, תמיכה בהפחתת תנועה וכלי נגישות חיצוני. כלי הנגישות הוא אמצעי משלים ואינו מחליף את עבודת ההנגשה בקוד ובתוכן.</p>
            <h2>נתקלתם בבעיה?</h2><p>אם מצאתם קושי בשימוש באתר, כתבו לנו באיזה עמוד נתקלתם בבעיה ומה ניסיתם לבצע. טלפון: {PHONE}. מייל: {EMAIL}.</p>
            """
    else:
        if kind=="privacy":
            title="Privacy Policy"
            body=f"""
            <p>Updated: September 2026.</p>
            <h2>Who operates this site</h2><p>This site is operated for Green Therapy. Privacy questions can be sent to {EMAIL} or raised by phone at {PHONE}.</p>
            <h2>Information we collect</h2><p>When you contact us, you may provide your name, phone number, email address and event details. Basic technical data may also be processed where needed for site operation and security.</p>
            <h2>How information is used</h2><p>Information is used to respond to inquiries, tailor services, communicate with you, and operate and secure the site.</p>
            <h2>Cookies and analytics</h2><p>Optional analytics, if enabled in the future, should operate according to the consent settings on the site. This policy should be updated when additional analytics or marketing services are connected.</p>
            <h2>External services</h2><p>The site is hosted by a third-party hosting provider. Links to WhatsApp and map services take you to third-party services governed by their own privacy terms.</p>
            <h2>Retention and security</h2><p>Information is kept only as long as reasonably required for the inquiry, business relationship and applicable legal obligations. Reasonable measures are used to reduce unauthorized access.</p>
            <h2>Privacy requests</h2><p>You may contact us regarding access, correction or questions about information you provided, subject to applicable law.</p>
            """
        elif kind=="terms":
            title="Terms of Use"
            body=f"""
            <p>Updated: September 2026.</p>
            <h2>Using the site</h2><p>This site provides general information about Green Therapy services. By using the site, you agree to these terms.</p>
            <h2>Information, availability and proposals</h2><p>Website content is not a binding offer. Scope, pricing, availability, venue, staffing and timing are agreed only through direct written confirmation with the client.</p>
            <h2>Health and safety</h2><p>Wellness activities may require individual suitability. Participants are responsible for providing relevant information and following staff guidance. Website content is not medical advice.</p>
            <h2>Intellectual property</h2><p>Site content, design, images and branding are protected by applicable rights and may not be copied or used commercially without permission.</p>
            <h2>Third-party links</h2><p>Links to maps, WhatsApp and other external services are provided for convenience and are governed by those services’ own terms.</p>
            <h2>Changes and responsibility</h2><p>The website and these terms may be updated from time to time. Responsibility for services actually supplied is governed by the written agreement with the client and applicable law.</p>
            <h2>Contact</h2><p>Phone: {PHONE}<br/>Email: {EMAIL}</p>
            """
        else:
            title="Accessibility Statement"
            body=f"""
            <p>Green Therapy works to improve site accessibility and support comfortable use with keyboards, screen readers and different display settings.</p>
            <h2>Accessibility features</h2><p>The site includes semantic structure, a skip link, contrast support, image alternatives, reduced-motion support and an external accessibility tool. The tool supplements — rather than replaces — accessibility work in the code and content.</p>
            <h2>Found a problem?</h2><p>If you encounter an accessibility issue, tell us which page you were using and what you were trying to do. Phone: {PHONE}. Email: {EMAIL}.</p>
            """
    return title,body

def replace_legal_main(soup,lang,kind):
    title,body=legal_markup(lang,kind)
    main=soup.find("main")
    if not main:
        main=soup.new_tag("main",id="main-content"); soup.body.append(main)
    main.clear()
    sec=BeautifulSoup(f'''<section class="gt-legal-page py-16 md:py-24"><div class="max-w-3xl mx-auto px-margin-mobile md:px-margin-desktop"><h1 class="font-display text-display text-forest-deep mb-8">{title}</h1><div class="gt-legal-copy">{body}</div></div></section>''',"html.parser")
    main.append(sec)

def pair_translation(he_soup,en_soup,page):
    data={"text":{},"alt":{}}
    counter=[0]
    altcounter=[0]
    pairs=[]; altpairs=[]
    def walk(a,b):
        if not isinstance(a,Tag) or not isinstance(b,Tag): return
        if a.name!=b.name: return
        if a.name in {"script","style","noscript","svg"}: return
        at=visible_direct_text_nodes(a); bt=visible_direct_text_nodes(b)
        for i in range(min(len(at),len(bt))):
            pairs.append((at[i],str(bt[i])))
        if a.name=="img" and a.has_attr("alt") and b.has_attr("alt"):
            altpairs.append((a,b.get("alt","")))
        ac=[x for x in a.children if isinstance(x,Tag)]
        bc=[x for x in b.children if isinstance(x,Tag)]
        for x,y in zip(ac,bc):
            if x.name==y.name: walk(x,y)
    walk(he_soup.body,en_soup.body)
    for node,en_text in pairs:
        he_text=str(node)
        if not he_text.strip() or not en_text.strip(): continue
        key=f"{page}-t{counter[0]}";counter[0]+=1
        span=he_soup.new_tag("span");span["data-i18n"]=key;span.string=he_text
        node.replace_with(span);data["text"][key]=en_text
    for img,en_alt in altpairs:
        key=f"{page}-a{altcounter[0]}";altcounter[0]+=1
        img["data-i18n-alt"]=key;data["alt"][key]=en_alt
    title=en_soup.title.string.strip() if en_soup.title and en_soup.title.string else ""
    desc=en_soup.find("meta",attrs={"name":"description"})
    data["title"]=title
    data["description"]=desc.get("content","") if desc else ""
    return data

# Prepare Hebrew + mirrored English in parallel, then extract translations from the mirrored DOM.
prepared={}
for page in PAGES:
    hp=ROOT/page; ep=ROOT/"en"/page
    if not hp.exists(): continue
    he=BeautifulSoup(hp.read_text(encoding="utf-8"),"html.parser")
    en_soup=BeautifulSoup(ep.read_text(encoding="utf-8"),"html.parser") if ep.exists() else BeautifulSoup(hp.read_text(encoding="utf-8"),"html.parser")
    if page=="privacy.html":
        replace_legal_main(he,"he","privacy"); replace_legal_main(en_soup,"en","privacy")
    elif page=="accessibility.html":
        replace_legal_main(he,"he","accessibility"); replace_legal_main(en_soup,"en","accessibility")
    he=prepare_page(he,"he",page); en_soup=prepare_page(en_soup,"en",page)
    prepared[page]=(he,en_soup)

# Terms page uses the same visual shell as Privacy and participates in the same translation system.
base_he=BeautifulSoup((ROOT/"privacy.html").read_text(encoding="utf-8"),"html.parser")
base_en=BeautifulSoup((ROOT/"en"/"privacy.html").read_text(encoding="utf-8"),"html.parser") if (ROOT/"en"/"privacy.html").exists() else BeautifulSoup((ROOT/"privacy.html").read_text(encoding="utf-8"),"html.parser")
replace_legal_main(base_he,"he","terms");replace_legal_main(base_en,"en","terms")
base_he=prepare_page(base_he,"he","terms.html");base_en=prepare_page(base_en,"en","terms.html")
prepared["terms.html"]=(base_he,base_en)

i18n={}
for page,(he,en_soup) in prepared.items():
    i18n[page]=pair_translation(he,en_soup,page)
    (ROOT/page).write_text(str(he),encoding="utf-8")

# English is now a translation of the same Hebrew DOM, not a second separately designed site.
if (ROOT/"en").exists():
    shutil.rmtree(ROOT/"en")

# Old /en URLs remain usable through redirects.
(ROOT/"_redirects").write_text("""/en /?lang=en 301
/en/ /?lang=en 301
/en/* /:splat?lang=en 301
/gallery / 301
/gallery.html / 301
""",encoding="utf-8")

(ROOT/"i18n-data.js").write_text("window.GT_I18N="+json.dumps(i18n,ensure_ascii=False,separators=(",",":"))+";\n",encoding="utf-8")

# Remove legacy JS that used to own duplicate navigation/contact behavior.
if (ROOT/"enhancements.js").exists():
    (ROOT/"enhancements.js").unlink()

# Shared component + responsive polish. The underlying Stitch sections remain untouched.
css=ROOT/"production.css"
c=css.read_text(encoding="utf-8")
c += r"""
/* Shared React chrome over the original Stitch design */
#gt-header-root{position:sticky;top:0;z-index:120}
.gt-react-header{background:rgba(255,248,245,.96);backdrop-filter:blur(12px);border-bottom:1px solid rgba(204,198,187,.45);color:#211a14}
.gt-react-header-inner{max-width:1280px;margin:auto;padding:9px 24px;min-height:76px;display:flex;align-items:center;gap:16px}
.gt-react-brand{display:flex;align-items:center;flex:0 0 138px}.gt-react-brand img{width:132px;height:56px;object-fit:contain;border-radius:9px;background:#fff}
.gt-react-nav{flex:1;display:flex;align-items:center;justify-content:center;gap:7px;min-width:0}
.gt-react-nav-link{padding:9px 11px;border-radius:999px;text-decoration:none;color:#4a463e;font-weight:700;font-size:.86rem;white-space:nowrap;transition:.2s ease}
.gt-react-nav-link:hover{background:#eef4ef;color:#1d3326}.gt-react-nav-link.active{background:#dfe9e1;color:#173c2b;box-shadow:inset 0 0 0 1px rgba(45,90,67,.18),0 2px 8px rgba(29,51,38,.08)}
.gt-react-actions{display:flex;align-items:center;gap:7px;flex:0 0 auto}
.gt-react-phone{direction:ltr;unicode-bidi:isolate;white-space:nowrap;text-decoration:none;border:1px solid #d6dfd8;background:#fff;color:#173c2b;border-radius:999px;padding:10px 12px;font-weight:800;font-size:.82rem}
.gt-react-flag{width:42px;height:42px;display:flex;align-items:center;justify-content:center;border:1px solid #d6dfd8;background:#fff;border-radius:999px;text-decoration:none;font-size:1.25rem}
.gt-react-cta{min-height:42px;display:inline-flex;align-items:center;justify-content:center;padding:0 17px;border-radius:999px;background:#2d5a43;color:#fff;text-decoration:none;font-weight:800;white-space:nowrap}
.gt-react-menu-btn{display:none;width:42px;height:42px;border-radius:999px;border:1px solid #d6dfd8;background:#fff;color:#173c2b;font-size:1.45rem;align-items:center;justify-content:center}
.gt-react-mobile-menu{display:none}.gt-react-mobile-phone{display:none}
.gt-phone-isolate{direction:ltr!important;unicode-bidi:isolate!important;white-space:nowrap!important}

.gt-react-footer{background:#1d3326;color:#fff;padding:46px 22px}.gt-react-footer-grid{max-width:1180px;margin:auto;display:grid;grid-template-columns:1.05fr 1fr .9fr 1.35fr;gap:34px}.gt-react-footer-brand img{width:190px;background:#fff;border-radius:14px}.gt-react-footer h2{font-size:1rem;color:#dcebe1;margin:0 0 14px;font-weight:800}.gt-react-footer ul{list-style:none;margin:0;padding:0;display:grid;gap:8px}.gt-react-footer a{color:rgba(255,255,255,.84);text-decoration:none}.gt-react-footer a:hover{text-decoration:underline;text-underline-offset:3px}.gt-react-contact-list li{overflow-wrap:anywhere}.gt-react-contact-list strong{color:#fff}

.gt-shared-contact{background:#eef4ef;border-top:1px solid #d6dfd8;padding:64px 22px}.gt-shared-contact-inner{max-width:1080px;margin:auto;display:grid;grid-template-columns:.85fr 1.15fr;gap:44px;align-items:start}.gt-shared-contact-copy h2{font-size:clamp(2rem,3.5vw,2.8rem);line-height:1.05;color:#1d3326;margin:0 0 14px}.gt-shared-contact-copy>p{font-size:1.05rem;line-height:1.7;color:#5f6c63}.gt-shared-contact-links{display:grid;gap:10px;margin-top:24px}.gt-shared-contact-links a{display:flex;align-items:center;justify-content:space-between;gap:12px;text-decoration:none;background:#fff;border:1px solid #d6dfd8;border-radius:14px;padding:13px 15px;color:#1d3326}.gt-shared-contact-links span{font-weight:700}.gt-shared-contact-links strong{font-weight:600;overflow-wrap:anywhere;text-align:end}
.gt-shared-contact-form{display:grid;gap:13px;background:#fff;border:1px solid #d6dfd8;border-radius:22px;padding:25px;box-shadow:0 10px 30px rgba(29,51,38,.06)}.gt-shared-form-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.gt-shared-contact-form label{display:grid;gap:6px;font-weight:700;color:#1d3326}.gt-shared-contact-form input,.gt-shared-contact-form textarea{width:100%;border:1px solid #cbd7ce;border-radius:11px;background:#fbfdfb;padding:12px 13px;color:#211a14;font:inherit}.gt-shared-contact-form input:focus,.gt-shared-contact-form textarea:focus{outline:3px solid rgba(45,90,67,.14);border-color:#2d5a43}.gt-shared-contact-form button{justify-self:start;min-width:105px;border:0;border-radius:999px;background:#2d5a43;color:#fff;padding:12px 24px;font:inherit;font-weight:800;cursor:pointer}.gt-shared-form-status{min-height:24px;color:#5f6c63;font-weight:600}.gt-honeypot{position:absolute!important;left:-9999px!important;width:1px!important;height:1px!important;opacity:0!important}

.gt-floating-wa-react{position:fixed;right:18px;bottom:18px;z-index:150;width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#25D366;color:#fff!important;border:2px solid #fff;text-decoration:none!important;font-weight:900;box-shadow:0 10px 28px rgba(0,0,0,.24)}

details.gt-faq-item{overflow:hidden}details.gt-faq-item summary{user-select:none}details.gt-faq-item[open]>summary .material-symbols-outlined{transform:rotate(180deg)}details.gt-faq-item>summary .material-symbols-outlined{transition:transform .25s ease}details.gt-faq-item[open]>:not(summary){animation:gtFaqReveal .28s cubic-bezier(.2,.8,.2,1) both}@keyframes gtFaqReveal{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}

.gt-animate-ready [data-gt-reveal]{opacity:0;transform:translateY(14px)}.gt-animate-ready [data-gt-reveal].gt-visible{opacity:1;transform:none;transition:opacity .55s ease,transform .55s cubic-bezier(.2,.8,.2,1)}
.gt-lang-en main{direction:ltr}.gt-lang-en main .text-right{text-align:left!important}.gt-lang-en main .right-4{right:auto!important;left:1rem!important}.gt-lang-en main .right-5{right:auto!important;left:1.25rem!important}
.gt-legal-page{background:#fff8f5}.gt-legal-copy{font-size:1.05rem;line-height:1.8;color:#4a463e}.gt-legal-copy h2{color:#1d3326;font-size:1.35rem;margin:30px 0 8px;font-weight:800}.gt-legal-copy p{margin:0 0 12px}

@media(max-width:1180px){.gt-react-nav-link{padding:8px 8px;font-size:.79rem}.gt-react-phone{display:none}.gt-react-header-inner{padding-left:16px;padding-right:16px}}
@media(max-width:980px){
 .gt-react-nav{display:none}.gt-react-cta{display:none}.gt-react-menu-btn{display:flex}.gt-react-header-inner{min-height:68px}.gt-react-brand{flex-basis:118px}.gt-react-brand img{width:112px;height:48px}
 .gt-react-mobile-phone{display:block;direction:ltr;unicode-bidi:isolate;text-align:center;padding:5px 12px;background:#e3ece5;color:#173c2b;text-decoration:none;font-weight:800;font-size:.82rem;border-top:1px solid rgba(29,51,38,.08)}
 .gt-react-mobile-menu.open{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:10px 14px 14px;background:#fff8f5;border-top:1px solid #d6dfd8}.gt-react-mobile-menu a{padding:11px;border-radius:11px;background:#fff;text-decoration:none;color:#173c2b;font-weight:800}.gt-react-mobile-menu a.active{background:#dfe9e1}
 .gt-shared-contact-inner{grid-template-columns:1fr}.gt-react-footer-grid{grid-template-columns:1fr 1fr}.gt-react-footer-brand{grid-column:1/-1}
}
@media(max-width:640px){
 .gt-react-header-inner{padding:7px 11px;gap:8px}.gt-react-actions{gap:5px}.gt-react-flag,.gt-react-menu-btn{width:40px;height:40px}.gt-react-mobile-menu.open{grid-template-columns:1fr}
 .gt-shared-contact{padding:50px 16px}.gt-shared-contact-inner{gap:26px}.gt-shared-contact-form{padding:20px}.gt-shared-form-grid{grid-template-columns:1fr}.gt-shared-contact-form button{width:100%}
 .gt-shared-contact-links a{display:grid;gap:4px}.gt-shared-contact-links strong{text-align:start}
 .gt-react-footer{padding:38px 17px}.gt-react-footer-grid{grid-template-columns:1fr;gap:26px}.gt-react-footer-brand{grid-column:auto}.gt-react-footer-brand img{width:165px}
 .gt-floating-wa-react{right:12px;bottom:12px;width:52px;height:52px}
 main h1{font-size:clamp(2rem,9.4vw,2.85rem)!important;line-height:1.08!important}main h2{font-size:clamp(1.6rem,7.2vw,2.15rem)!important;line-height:1.16!important}
}
@media(prefers-reduced-motion:reduce){.gt-animate-ready [data-gt-reveal]{opacity:1;transform:none}.gt-animate-ready [data-gt-reveal].gt-visible{transition:none}details.gt-faq-item[open]>:not(summary){animation:none}}
"""
css.write_text(c,encoding="utf-8")

# Validation: report remaining visible Latin words on Hebrew pages (email addresses are expected).
offenders={}
for page in list(prepared.keys()):
    soup=BeautifulSoup((ROOT/page).read_text(encoding="utf-8"),"html.parser")
    vals=[]
    for node in soup.find_all(string=True):
        if isinstance(node,Comment) or not str(node).strip() or (node.parent and node.parent.name in {"script","style","noscript","svg"}): continue
        s=str(node).strip()
        scrub=re.sub(r'\b[\w.+-]+@[\w.-]+\.\w+\b','',s)
        if re.search(r'[A-Za-z]{2,}',scrub): vals.append(s)
    if vals: offenders[page]=sorted(set(vals))[:40]
print("LATIN_VISIBLE_REVIEW="+json.dumps(offenders,ensure_ascii=False))
print("Unified shared components and translation mode complete.")
