from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
email = 'alongreentherapy@gmail.com'

# Contact page cleanup
p = root / 'contact.html'
s = p.read_text(encoding='utf-8')

s = re.sub(
    r'<a class="hidden sm:inline-flex items-center gap-1\.5 text-secondary[^>]*" href="mailto:alongreentherapy@gmail\.com">\s*<span class="material-symbols-outlined text-tertiary">call</span>\s*<span>alongreentherapy@gmail\.com</span>\s*</a>',
    '<a class="hidden sm:inline-flex items-center gap-1.5 text-secondary hover:text-on-surface text-label-md font-label-md px-3 py-2 rounded-lg transition-colors" href="#booking-form"><span class="material-symbols-outlined text-tertiary">edit_calendar</span><span>פרטי האירוע</span></a>',
    s,
    flags=re.S,
)
s = s.replace('<span>Book Now</span>', '<span>תכנון אירוע</span>')
s = s.replace(
    'href="https://wa.me/97239604422" rel="noopener" target="_blank">\n                    alongreentherapy@gmail.com\n                  </a>',
    'href="#booking-form">\n                    שליחת פנייה דרך הטופס\n                  </a>',
)

dup_row = '''<li class="flex items-start gap-3.5 group">
<div class="p-2.5 rounded-lg bg-surface-container text-tertiary shrink-0">
<span class="material-symbols-outlined">mail</span>
</div>
<div>
<span class="block font-label-sm text-label-sm text-secondary">מייל ליצירת קשר</span>
<a class="font-label-md text-label-md text-on-surface hover:text-tertiary dir-ltr block text-right" href="mailto:alongreentherapy@gmail.com">alongreentherapy@gmail.com</a>
</div>
</li>
'''
s = s.replace(dup_row, '')
s = s.replace(
    '<span class="font-semibold text-on-surface">alongreentherapy@gmail.com</span>',
    '<span class="font-semibold text-on-surface">דרך הטופס או המייל</span>',
    1,
)
s = s.replace(
    '''<p class="dir-ltr text-right">alongreentherapy@gmail.com</p>
<p class="dir-ltr text-right">alongreentherapy@gmail.com</p>
<div class="pt-2 flex items-center gap-3 text-surface-bone">
<span class="inline-flex items-center gap-1 text-label-sm bg-surface-bone/10 px-2.5 py-1 rounded">
<span class="w-2 h-2 rounded-full bg-tertiary-fixed"></span>
              alongreentherapy@gmail.com
            </span>
</div>''',
    '''<a class="dir-ltr text-right hover:text-primary-fixed transition-colors" href="mailto:alongreentherapy@gmail.com">alongreentherapy@gmail.com</a>''',
)
p.write_text(s, encoding='utf-8')

# Site-wide internal links and stale Stitch placeholders
html_files = list(root.glob('*.html')) + list((root / 'en').glob('*.html'))
for p in html_files:
    s = p.read_text(encoding='utf-8')
    link_map = {
        'Pop-Up Spa': 'spa.html',
        'Mind &amp; Body Workshops': 'workshops.html',
        'Ice Bath Experience': 'ice-bath.html',
        'דוכני סופר-פוד ושייקים': 'healthy-bar.html',
        'צור קשר': 'contact.html',
        'בית': 'index.html',
    }
    for label, href in link_map.items():
        pattern = rf'<a(?P<attrs>[^>]*)href="#"(?P<attrs2>[^>]*)>{re.escape(label)}</a>'
        s = re.sub(pattern, lambda m: f'<a{m.group("attrs")}href="{href}"{m.group("attrs2")}>{label}</a>', s)

    s = re.sub(
        r'<a(?P<attrs>[^>]*)href="#"(?P<attrs2>[^>]*)>\s*Green Therapy\s*</a>',
        lambda m: f'<a{m.group("attrs")}href="index.html"{m.group("attrs2")}>Green Therapy</a>',
        s,
    )
    s = re.sub(
        r'<a(?P<attrs>[^>]*)href="#"(?P<attrs2>[^>]*)>Privacy Policy</a>',
        lambda m: f'<span{m.group("attrs")}{m.group("attrs2")}>Privacy Policy</span>',
        s,
    )
    s = re.sub(
        r'<a(?P<attrs>[^>]*)href="#"(?P<attrs2>[^>]*)>(?P<body><span[^>]*>photo_camera</span>)</a>',
        lambda m: f'<a{m.group("attrs")}href="gallery.html"{m.group("attrs2")}>{m.group("body")}</a>',
        s,
    )
    s = re.sub(
        r'<a(?P<attrs>[^>]*)href="#"(?P<attrs2>[^>]*)>(?P<body><span[^>]*>call</span>)</a>',
        lambda m: f'<a{m.group("attrs")}href="contact.html"{m.group("attrs2")}>{m.group("body")}</a>',
        s,
    )
    s = re.sub(
        r'<a(?P<attrs>[^>]*)href="#"(?P<attrs2>[^>]*)>(?P<body><span[^>]*>mail</span>)</a>',
        lambda m: f'<a{m.group("attrs")}href="mailto:{email}"{m.group("attrs2")}>{m.group("body")}</a>',
        s,
    )
    s = s.replace('050-000-0000 / alongreentherapy@gmail.com', 'alongreentherapy@gmail.com')
    s = s.replace('טלפון: alongreentherapy@gmail.com', 'מייל: alongreentherapy@gmail.com')
    p.write_text(s, encoding='utf-8')

# Animation/screenshot stability: keep the reveal subtle enough that captures never look dark/unloaded.
p = root / 'enhancements.css'
css = p.read_text(encoding='utf-8')
css = css.replace(
    '.gt-reveal{position:relative;opacity:.2;transform:translateY(24px);filter:blur(2px);',
    '.gt-reveal{position:relative;opacity:.72;transform:translateY(14px);filter:none;',
)
css = css.replace('.gt-transition-cover.is-active{opacity:.16}', '.gt-transition-cover.is-active{opacity:.06}')
p.write_text(css, encoding='utf-8')
