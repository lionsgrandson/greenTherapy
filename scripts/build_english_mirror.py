from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import html
import json
import re
import time
import urllib.parse
import urllib.request

PAGES = [
    'index.html','spa.html','ice-bath.html','workshops.html',
    'healthy-bar.html','about.html','gallery.html','contact.html'
]
HEBREW = re.compile(r'[\u0590-\u05FF]')
CACHE_PATH = Path('translations-he-en.json')

# Brand-sensitive copy gets deliberate wording; everything else is translated and baked at build time.
OVERRIDES = {
    'דף הבית': 'Home',
    'מתחמים': 'Experiences',
    'אודות': 'About',
    'גלריה': 'Gallery',
    'צור קשר': 'Contact',
    'בואו נבנה חוויה': 'Build Your Experience',
    'בואו נבנה את החוויה שלכם': 'Build Your Experience',
    'מתחמי Wellness ו-Wellbeing פרימיום לאירועי חברה': 'Premium Wellness & Wellbeing Experiences for Corporate Events',
    'מתחמי Wellness ו-Wellbeing פרימיום לאירועי חברה.': 'Premium Wellness & Wellbeing Experiences for Corporate Events.',
    'הפקה מקצה לקצה 360°': 'End-to-End 360° Production',
    '5 סוגי עיסוי לבחירה': '5 Massage Styles to Choose From',
    'ניהול תורים דיגיטלי': 'Digital Appointment Management',
    'במשרד, בטבע או באירוע החברה': 'At the Office, Outdoors, or at Your Company Event',
    'הפקה מקצה לקצה': 'End-to-End Production',
    'חוויה בהתאמה אישית': 'A Fully Tailored Experience',
    'ניהול חלק ללא עומסים': 'Smooth, Queue-Free Management',
    'מתחם עיסויים יוקרתי (Pop-Up Spa)': 'Luxury Massage Experience (Pop-Up Spa)',
    'עיסוי שוודי קלאסי ומרגיע': 'Classic Relaxing Swedish Massage',
    'עיסוי תאילנדי משחרר ומתיחות': 'Thai Massage, Release & Stretching',
    'שיאצו': 'Shiatsu',
    'עיסוי קרקפת ופנים + עיסוי כפות רגליים תאילנדי': 'Scalp & Facial Massage + Thai Foot Massage',
    'מתחם אמבטיות קרח – Peak Energy Experience': 'Ice Bath Experience – Peak Energy Experience',
    'סדנאות גוף-נפש, מיינדפולנס והרצאות': 'Mind-Body Workshops, Mindfulness & Talks',
    'יוגה ומדיטציה': 'Yoga & Meditation',
    'מיינדפולנס ונשימה': 'Mindfulness & Breathwork',
    'הרצאות העשרה': 'Enrichment Talks',
    'דוכני בריאות, שייקים וסופר-פוד מעוצבים': 'Styled Healthy Bar, Smoothies & Superfoods',
    'פירות העונה וסופר-פודס': 'Seasonal Fruit & Superfoods',
    'חוויה קולינרית רעננה ואסתטית': 'A Fresh, Beautiful Culinary Experience',
    'ראש שקט (אנחנו מטפלים בהכל)': 'Peace of Mind — We Handle Everything',
    'סטנדרט שירות גבוה': 'High Service Standards',
    'גמישות מלאה': 'Complete Flexibility',
    'חוויה אחת, שפע אפשרויות': 'One Experience, Endless Possibilities',
    'תהליך העבודה איתנו ב-3 שלבים': 'How We Work — 3 Simple Steps',
    'מדברים ומאפיינים': 'Talk & Define the Brief',
    'תופרים את החוויה': 'Tailor the Experience',
    'מגיעים ומפעילים': 'We Arrive & Run It',
    'תכנון אירוע': 'Plan Your Event',
    'פרטי האירוע': 'Event Details',
    'טופס אפיון והזמנת אירוע': 'Event Brief & Booking Form',
    'שם מלא *': 'Full Name *',
    'שם חברה / ארגון *': 'Company / Organization *',
    'תפקיד בארגון *': 'Role in the Organization *',
    'טלפון נייד *': 'Mobile Phone *',
    'מייל עסקי *': 'Business Email *',
    'כמות משתתפים משוערת': 'Estimated Number of Participants',
    'תאריך משוער של האירוע *': 'Estimated Event Date *',
    'מיקום האירוע המתוכנן *': 'Planned Event Location *',
    'שלחו בקשה לקבלת הצעה מפורטת': 'Send a Request for a Detailed Proposal',
    'שליחת פנייה דרך הטופס': 'Send an Inquiry Through the Form',
    'יצירת קשר': 'Contact',
    'מייל': 'Email',
    'אירוע חברה / Offsite': 'Company Event / Offsite',
    'תודה! פנייתך התקבלה בהצלחה, נחזור אליך בהקדם.': 'Thank you! Your inquiry was received successfully. We will get back to you shortly.',
    'תודה! פנייתך התקבלה בהצלחה, צוות Green Therapy יצור עמך קשר בהקדם.': 'Thank you! Your inquiry was received successfully. The Green Therapy team will contact you shortly.',
    'תודה! פרטי הפנייה התקבלו. ניצור איתכם קשר בהקדם עם הצעה מותאמת אישית.': 'Thank you! We received your inquiry and will contact you shortly with a tailored proposal.',
    'תודה! פרטי הבקשה התקבלו ונחזור אליך בהקדם.': 'Thank you! We received your request and will get back to you shortly.',
    'תודה על פנייתך! צוות Green Therapy ייצור איתך קשר בהקדם לתכנון האירוע.': 'Thank you for reaching out! The Green Therapy team will contact you shortly to plan your event.',
    'שלום, אשמח לקבל הצעת מחיר למתחם עיסויים לאירוע חברה': 'Hello, I would like to receive a quote for a corporate event massage experience',
    'היי, נשמח לייעוץ לגבי מתחם ספא לאירוע החברה': 'Hi, we would love advice about a spa experience for our company event',
    'היי, יש לנו אירוע דחוף ונשמח לבדוק זמינות למתחם עיסויים': 'Hi, we have an upcoming event and would like to check availability for a massage experience',
}


def norm(s):
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def google_translate(text):
    if text in OVERRIDES:
        return OVERRIDES[text]
    params = urllib.parse.urlencode({
        'client': 'gtx', 'sl': 'he', 'tl': 'en', 'dt': 't', 'q': text
    })
    url = 'https://translate.googleapis.com/translate_a/single?' + params
    last = None
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read().decode('utf-8'))
            translated = ''.join(part[0] for part in data[0] if part and part[0])
            if translated:
                return translated
        except Exception as e:
            last = e
            time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f'Translation failed for {text!r}: {last}')


def collect_strings(source):
    strings = set()
    protected = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', source, flags=re.I|re.S)
    for m in re.finditer(r'>([^<>]+)<', protected, flags=re.S):
        s = norm(m.group(1))
        if s and HEBREW.search(s): strings.add(s)
    for attr in ('alt','title','placeholder','aria-label','content'):
        for m in re.finditer(rf'{attr}="([^"]+)"', protected, flags=re.I):
            s = norm(m.group(1))
            if s and HEBREW.search(s): strings.add(s)
    for m in re.finditer(r"alert\(\s*['\"]([^'\"]*[\u0590-\u05FF][^'\"]*)['\"]\s*\)", source, flags=re.I):
        strings.add(norm(m.group(1)))
    for m in re.finditer(r'https://wa\.me/\?text=([^"&]+)', source, flags=re.I):
        decoded = urllib.parse.unquote(m.group(1))
        if HEBREW.search(decoded): strings.add(norm(decoded))
    return strings


cache = {}
if CACHE_PATH.exists():
    try: cache = json.loads(CACHE_PATH.read_text(encoding='utf-8'))
    except Exception: cache = {}
cache.update(OVERRIDES)

all_sources = {p: Path(p).read_text(encoding='utf-8') for p in PAGES}
needed = set()
for src in all_sources.values(): needed.update(collect_strings(src))
missing = sorted(s for s in needed if s not in cache)
print(f'{len(needed)} unique Hebrew strings; {len(missing)} need translation')

if missing:
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(google_translate, s): s for s in missing}
        done = 0
        for f in as_completed(futures):
            s = futures[f]
            cache[s] = f.result()
            done += 1
            if done % 50 == 0: print(f'Translated {done}/{len(missing)}')

CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True), encoding='utf-8')
Path('en').mkdir(exist_ok=True)


def translate_html(source, filename):
    # The Hebrew page is the visual master. Preserve its exact DOM, classes and RTL layout;
    # change only user-visible copy, language metadata, local paths and the language switch.
    blocks = []
    def protect(m):
        key = f'__GT_PROTECTED_BLOCK_{len(blocks)}__'
        blocks.append(m.group(0))
        return key
    out = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', protect, source, flags=re.I|re.S)

    def text_cb(m):
        raw = m.group(1)
        s = norm(raw)
        if not s or not HEBREW.search(s): return m.group(0)
        tr = cache.get(s)
        if not tr: raise KeyError(f'Missing translation: {s}')
        lead = raw[:len(raw)-len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):] if raw.rstrip() != raw else ''
        return '>' + lead + html.escape(tr, quote=False) + trail + '<'
    out = re.sub(r'>([^<>]+)<', text_cb, out, flags=re.S)

    def attr_cb(m):
        prefix, raw = m.group(1), m.group(2)
        s = norm(raw)
        if not s or not HEBREW.search(s): return m.group(0)
        tr = cache.get(s)
        if not tr: raise KeyError(f'Missing attribute translation: {s}')
        return prefix + html.escape(tr, quote=True) + '"'
    out = re.sub(r'((?:alt|title|placeholder|aria-label|content)=")([^"]+)"', attr_cb, out, flags=re.I)

    for i, block in enumerate(blocks): out = out.replace(f'__GT_PROTECTED_BLOCK_{i}__', block)

    def alert_cb(m):
        quote, raw = m.group(1), m.group(2)
        s = norm(raw)
        tr = cache.get(s, raw)
        return 'alert(' + quote + tr.replace('\\', '\\\\').replace(quote, '\\' + quote) + quote + ')'
    out = re.sub(r"alert\(\s*(['\"])([^'\"]*[\u0590-\u05FF][^'\"]*)\1\s*\)", alert_cb, out)

    def wa_cb(m):
        raw = m.group(1)
        decoded = norm(urllib.parse.unquote(raw))
        tr = cache.get(decoded, decoded)
        return 'https://wa.me/?text=' + urllib.parse.quote(tr, safe=',.!?')
    out = re.sub(r'https://wa\.me/\?text=([^"&]+)', wa_cb, out, flags=re.I)

    # English keeps the same Stitch components, spacing and imagery, but uses natural LTR flow.
    # Fine-grained English-only CSS handles longer copy without changing the Hebrew master.
    def html_tag_cb(m):
        tag = m.group(0)
        if re.search(r'\blang="[^"]*"', tag, re.I):
            tag = re.sub(r'\blang="[^"]*"', 'lang="en"', tag, count=1, flags=re.I)
        else:
            tag = tag[:-1] + ' lang="en">'
        if re.search(r'\bdir="[^"]*"', tag, re.I):
            tag = re.sub(r'\bdir="[^"]*"', 'dir="ltr"', tag, count=1, flags=re.I)
        else:
            tag = tag[:-1] + ' dir="ltr">'
        return tag
    out = re.sub(r'<html\b[^>]*>', html_tag_cb, out, count=1, flags=re.I)
    out = out.replace('data-lang-switch="en"', 'data-lang-switch="he"')
    out = re.sub(r'href="en/([^"]+\.html)"', r'href="../\1"', out)
    out = re.sub(r'(<a[^>]*data-lang-switch="he"[^>]*>)(\s*)EN(\s*</a>)', r'\1\2HE\3', out, flags=re.I)

    out = out.replace('href="enhancements.css"', 'href="../enhancements.css"')
    out = out.replace('src="enhancements.js"', 'src="../enhancements.js"')
    out = out.replace('src="assets/', 'src="../assets/')
    out = out.replace('href="assets/', 'href="../assets/')

    # English-specific layout polish: preserve the design system while giving English natural LTR flow.
    out = out.replace('href="../enhancements.css" rel="stylesheet"/>', 'href="../enhancements.css" rel="stylesheet"/>\n<link href="../english.css" rel="stylesheet"/>')
    out = out.replace('<body class="', '<body class="gt-en-page ', 1)
    out = out.replace('text-right', 'text-left')

    # The homepage hero and trust badges need a little more room for English copy.
    if filename == 'index.html':
        out = out.replace('max-w-3xl text-white">', 'max-w-4xl text-white gt-en-hero-copy">', 1)
        out = out.replace('grid grid-cols-2 sm:grid-cols-4 gap-4 text-white/90', 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-white/90', 1)
        out = out.replace('>arrow_back<', '>arrow_forward<', 1)

    return out

for page, source in all_sources.items():
    built = translate_html(source, page)
    Path('en', page).write_text(built, encoding='utf-8')
    print(f'Built en/{page}: {len(source)} -> {len(built)} bytes')

leftovers = []
for page in PAGES:
    text = Path('en', page).read_text(encoding='utf-8')
    visible = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    visible = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', visible, flags=re.I|re.S)
    if HEBREW.search(visible):
        snippets = [norm(m.group(0)) for m in re.finditer(r'.{0,60}[\u0590-\u05FF].{0,100}', visible)]
        leftovers.append((page, snippets[:10]))
if leftovers:
    raise SystemExit('Visible Hebrew remains in English mirror: ' + repr(leftovers))
