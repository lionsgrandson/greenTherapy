from pathlib import Path
from bs4 import BeautifulSoup, Tag
import re, html

ROOT=Path('.')
ROOT_PAGES=['index.html','spa.html','ice-bath.html','workshops.html','healthy-bar.html','about.html','gallery.html','contact.html']

COLORS={
'"primary-container": "#f2e8d5"':'"primary-container": "#dfe9e1"',
'"primary-fixed": "#ebe1cf"':'"primary-fixed": "#dbe8dd"',
'"primary-fixed-dim": "#cfc6b3"':'"primary-fixed-dim": "#bfd2c3"',
'"secondary": "#705a4c"':'"secondary": "#506b58"',
'"secondary-container": "#f8dac8"':'"secondary-container": "#e3ece5"',
'"on-secondary-container": "#755e50"':'"on-secondary-container": "#355140"',
'"surface-tint": "#645e4f"':'"surface-tint": "#4e6b58"',
'"inverse-primary": "#cfc6b3"':'"inverse-primary": "#bfd2c3"',
}

def clean_root(name):
    p=ROOT/name
    s=p.read_text(encoding='utf-8')
    for a,b in COLORS.items(): s=s.replace(a,b)
    soup=BeautifulSoup(s,'html.parser')

    # Remove the micro-headline / eyebrow style the client explicitly rejected.
    exact={'אודות Green Therapy • הפקת מתחמי Wellness לאירועי חברה','הסטנדרט שמבדיל אותנו','צוות Green Therapy'}
    for node in list(soup.find_all(string=lambda x:isinstance(x,str) and x.strip() in exact)):
        el=node.parent; par=el.parent if el.parent else None
        if par and isinstance(par,Tag) and ('inline-flex' in (par.get('class') or []) or 'w-fit' in (par.get('class') or [])): par.decompose()
        else: el.decompose()
    for sp in list(soup.find_all('span')):
        if sp.find_parent('header') or sp.find_parent('footer'): continue
        cl=' '.join(sp.get('class') or []); txt=sp.get_text(' ',strip=True)
        if len(txt)<=90 and (('font-label-caps' in cl) or ('font-label-sm' in cl and any(x in cl for x in ['tracking-wider','tracking-widest','tracking-wide','uppercase']))):
            sp.decompose()

    # Remove the unwanted floating micro-copy card in About.
    if name=='about.html':
        for phrase in ['מקצועיות ושירות','צוות מנוסה, מוסמך ושירותי ברמה הגבוהה ביותר']:
            node=soup.find(string=lambda x:isinstance(x,str) and x.strip()==phrase)
            if node:
                card=node.find_parent('div',class_=lambda c:c and 'absolute' in c and 'bottom' in c)
                if card: card.decompose()
        for el in list(soup.find_all(['h4','span'],string=lambda x:isinstance(x,str) and x.strip()=='צוות Green Therapy')):
            card=el.find_parent('div',class_=lambda c:c and ('p-5' in c or 'inline-flex' in c))
            if card: card.decompose()

    if name in ['spa.html','workshops.html']:
        for phrase in ['צוות מטפלים מנוסה ושירותי','מקצועיות ושירות']:
            for node in list(soup.find_all(string=lambda x:isinstance(x,str) and x.strip()==phrase)):
                par=node.parent.parent if node.parent and node.parent.parent else None
                if par and isinstance(par,Tag) and 'inline-flex' in (par.get('class') or []): par.decompose()
                else: node.parent.decompose()
        for node in list(soup.find_all(string=lambda x:isinstance(x,str) and x.strip()=='מקצועיות ושירות ברמה הגבוהה ביותר')):
            row=node.find_parent('div',class_=lambda c:c and 'flex' in c and 'items-center' in c)
            if row: row.decompose()

    # Consistent internal navigation.
    header=soup.find('header')
    if header:
        brand=header.find('a',href=True)
        if brand: brand['href']='index.html'
        nav=header.find('nav')
        if nav:
            old=nav.find('a'); cls=old.get('class') if old else ['text-on-surface-variant','font-medium','transition-colors']
            nav.clear()
            for href,label in [('index.html','דף הבית'),('index.html#experiences','מתחמים'),('about.html','אודות'),('gallery.html','גלריה'),('contact.html','צור קשר')]:
                a=soup.new_tag('a',href=href); a['class']=cls; a.string=label; nav.append(a)
    hash_map={'#popup-spa':'spa.html','#spa':'spa.html','#ice-baths':'ice-bath.html','#ice-bath':'ice-bath.html','#workshops':'workshops.html','#healthy-bar':'healthy-bar.html','#about':'about.html','#gallery':'gallery.html','#contact':'contact.html','#contact-b2b':'contact.html','#services':'index.html#experiences','#atmosphere':'gallery.html','#pricing':'contact.html'}
    for a in soup.find_all('a',href=True):
        if a['href'] in hash_map: a['href']=hash_map[a['href']]
        if a['href']=='#' and a.find_parent('header'): a['href']='index.html'
    if name=='workshops.html':
        for a in soup.find_all('a',href=True):
            if 'עיון בקטלוג הסדנאות' in a.get_text(' ',strip=True): a['href']='#workshops-catalog'

    # Shared motion layer + language switch.
    if soup.head and not soup.find('link',href='enhancements.css'):
        soup.head.append(soup.new_tag('link',rel='stylesheet',href='enhancements.css'))
    if soup.body and not soup.find('script',src='enhancements.js'):
        soup.body.append(soup.new_tag('script',src='enhancements.js',defer=True))
    if header and not header.find('a',attrs={'data-lang-switch':True}):
        area=header.find('div',class_=lambda c:c and 'flex' in c and 'items-center' in c)
        if area:
            a=soup.new_tag('a',href='en/index.html'); a['data-lang-switch']='en'; a['class']='inline-flex items-center justify-center min-w-10 h-10 px-3 rounded-full bg-primary-container text-forest-deep border border-outline-variant/40 font-label-sm text-label-sm font-bold'; a.string='EN'; area.append(a)

    p.write_text(str(soup),encoding='utf-8')

for n in ROOT_PAGES: clean_root(n)

# Replace generated/fake testimonials with the real WhatsApp recommendation screenshots from the approved original design.
p=ROOT/'index.html'; s=p.read_text(encoding='utf-8')
start=s.find('<!-- 8. Social Proof / Corporate Testimonials -->'); end=s.find('<!-- 9. Final Full-Width CTA Section -->')
if start!=-1 and end>start:
    real='''<!-- 8. Authentic Client Recommendations -->
<section class="py-16 md:py-24 bg-forest-deep text-white" id="recommendations"><div class="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop"><div class="max-w-2xl mx-auto text-center mb-12"><h2 class="font-display text-headline-lg md:text-[36px] font-bold">הודעות אמיתיות מלקוחות אחרי אירועים</h2><p class="font-body-md text-white/75 mt-3">פידבקים אמיתיים שנשלחו ל-Green Therapy אחרי הפעילויות.</p></div><div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-3xl mx-auto items-start"><figure class="rounded-3xl bg-white/10 border border-white/15 p-5 md:p-7"><img src="assets/client-message-1.jpg" alt="הודעת המלצה אמיתית מלקוח Green Therapy" class="w-full max-w-[330px] mx-auto rounded-2xl shadow-2xl" loading="lazy"/></figure><figure class="rounded-3xl bg-white/10 border border-white/15 p-5 md:p-7"><img src="assets/client-message-2.jpg" alt="פידבק אמיתי נוסף מלקוח Green Therapy" class="w-full max-w-[330px] mx-auto rounded-2xl shadow-2xl" loading="lazy"/></figure></div></div></section>\n'''
    s=s[:start]+real+s[end:]
p.write_text(s,encoding='utf-8')

# Shared animation and stronger green finishing layer.
(ROOT/'enhancements.css').write_text('''
:root{--gt-forest:#1d3326;--gt-green:#2d5a43;--gt-sage:#6f8f78;--gt-mist:#dfe9e1}html{scroll-behavior:smooth}body{overflow-x:hidden}.bg-primary-container{background-color:#dfe9e1!important}.bg-secondary-container{background-color:#e3ece5!important}.text-secondary{color:#506b58!important}.border-secondary{border-color:#6f8f78!important}.gt-card-hover{transition:transform .35s ease,border-color .35s ease,box-shadow .35s ease}.gt-card-hover:hover{transform:translateY(-4px);box-shadow:0 18px 45px rgba(29,51,38,.08);border-color:rgba(45,90,67,.35)!important}.gt-reveal{position:relative;opacity:.2;transform:translateY(24px);filter:blur(2px);transition:opacity .7s ease,transform .7s cubic-bezier(.22,.8,.2,1),filter .55s ease}.gt-reveal:before{content:"";position:absolute;z-index:50;top:12px;left:50%;width:48px;height:3px;border-radius:999px;transform:translateX(-50%);background:linear-gradient(90deg,transparent,#2d5a43,transparent);background-size:200% 100%;animation:gtLoad 1.15s linear infinite;opacity:.8;pointer-events:none}.gt-reveal.gt-visible{opacity:1;transform:none;filter:none}.gt-reveal.gt-visible:before{opacity:0;transition:opacity .2s ease}@keyframes gtLoad{from{background-position:200% 0}to{background-position:-200% 0}}body.gt-page-ready main{animation:gtPageIn .45s ease both}@keyframes gtPageIn{from{opacity:.72;transform:translateY(6px)}to{opacity:1;transform:none}}.gt-transition-cover{position:fixed;inset:0;z-index:9999;background:#1d3326;opacity:0;pointer-events:none;transition:opacity .22s ease}.gt-transition-cover.is-active{opacity:.16}@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}.gt-reveal{opacity:1!important;transform:none!important;filter:none!important}.gt-reveal:before{display:none!important}}
''',encoding='utf-8')
(ROOT/'enhancements.js').write_text('''
(()=>{const ready=()=>{document.body.classList.add('gt-page-ready');document.querySelectorAll('main .rounded-2xl,main .rounded-3xl,main .rounded-xl').forEach(el=>{if(!el.closest('form'))el.classList.add('gt-card-hover')});const sections=[...document.querySelectorAll('main > section,body > section')].filter(s=>!s.closest('footer'));sections.forEach((s,i)=>{if(i===0)s.classList.add('gt-visible');else s.classList.add('gt-reveal')});if('IntersectionObserver'in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('gt-visible');io.unobserve(e.target)}}),{rootMargin:'0px 0px -8% 0px',threshold:.08});sections.slice(1).forEach(s=>io.observe(s))}else sections.forEach(s=>s.classList.add('gt-visible'));const cover=document.createElement('div');cover.className='gt-transition-cover';document.body.appendChild(cover);document.querySelectorAll('a[href]').forEach(a=>{const h=a.getAttribute('href')||'';if(!h||h.startsWith('#')||/^(https?:|mailto:|tel:|javascript:)/i.test(h)||!/\\.html(?:[#?].*)?$/i.test(h))return;a.addEventListener('click',e=>{if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||a.target==='_blank')return;e.preventDefault();cover.classList.add('is-active');setTimeout(()=>location.href=h,150)})})};document.readyState==='loading'?document.addEventListener('DOMContentLoaded',ready):ready()})();
''',encoding='utf-8')

# ---------- English multi-page site ----------
def sources(page):
    sp=BeautifulSoup((ROOT/page).read_text(encoding='utf-8'),'html.parser')
    return [i.get('src') for i in sp.find_all('img',src=True) if i.get('src')]
imgs={p:sources(p) for p in ROOT_PAGES}

def shell(title,desc,back,hero,body,hero_img,content):
    nav=''.join(f'<a class="text-sm font-semibold text-on-surface-variant hover:text-primary transition-colors" href="{h}">{t}</a>' for h,t in [('index.html','Home'),('spa.html','Pop-Up Spa'),('ice-bath.html','Ice Baths'),('workshops.html','Workshops'),('healthy-bar.html','Healthy Bar'),('about.html','About'),('gallery.html','Gallery'),('contact.html','Contact')])
    return f'''<!DOCTYPE html><html lang="en" dir="ltr"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"/><link rel="preconnect" href="https://fonts.googleapis.com"/><link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/><link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet"/><script src="https://cdn.tailwindcss.com?plugins=forms"></script><script>tailwind.config={{theme:{{extend:{{colors:{{surface:'#fff8f5','surface-container-low':'#fff1e7','surface-container':'#faebe1','on-surface':'#211a14','on-surface-variant':'#4a463e','outline-variant':'#c6d0c8',primary:'#2d5a43','on-primary':'#fff','primary-container':'#dfe9e1',secondary:'#506b58','secondary-container':'#e3ece5','forest-deep':'#1d3326','terracotta':'#7c5639'}},fontFamily:{{sans:['Manrope','sans-serif']}},maxWidth:{{'container-max':'1280px'}}}}}}}};</script><link rel="stylesheet" href="../enhancements.css"/><style>body{{font-family:Manrope,sans-serif;background:#fff8f5;color:#211a14}}</style></head><body><header class="sticky top-0 z-50 bg-surface/95 backdrop-blur border-b border-outline-variant/40"><div class="max-w-container-max mx-auto px-5 md:px-12 h-20 flex items-center justify-between gap-6"><a href="index.html" class="font-extrabold text-forest-deep">Green Therapy</a><nav class="hidden xl:flex items-center gap-5">{nav}</nav><div class="flex gap-2"><a href="../{back}" class="px-3 py-2 rounded-full bg-primary-container font-bold">HE</a><a href="contact.html" class="bg-forest-deep text-white px-5 py-2.5 rounded-lg font-semibold">Plan Your Event</a></div></div></header><main><section class="relative min-h-[520px] flex items-center overflow-hidden"><img src="{hero_img}" alt="Green Therapy corporate wellness" class="absolute inset-0 w-full h-full object-cover"/><div class="absolute inset-0 bg-gradient-to-r from-forest-deep/95 via-forest-deep/75 to-transparent"></div><div class="relative z-10 max-w-container-max mx-auto px-5 md:px-12 py-20 w-full"><div class="max-w-3xl text-white"><h1 class="text-4xl md:text-6xl leading-tight font-extrabold">{hero}</h1><p class="mt-6 text-lg md:text-xl leading-relaxed text-white/90">{body}</p><div class="mt-8 flex gap-3"><a href="contact.html" class="bg-white text-forest-deep px-6 py-3 rounded-lg font-bold">Plan Your Event</a><a href="index.html" class="border border-white/60 px-6 py-3 rounded-lg font-semibold">Home</a></div></div></div></section>{content}</main><footer class="bg-forest-deep text-white/80"><div class="max-w-container-max mx-auto px-5 md:px-12 py-12 grid md:grid-cols-3 gap-8"><div><b class="text-white">Green Therapy</b><p class="mt-2 text-sm">Premium corporate wellness experiences for offices, outdoor events, and offsites.</p></div><div class="grid gap-2 text-sm"><a href="spa.html">Pop-Up Spa</a><a href="ice-bath.html">Ice Baths</a><a href="workshops.html">Workshops</a><a href="healthy-bar.html">Healthy Bar</a></div><a href="mailto:alongreentherapy@gmail.com">alongreentherapy@gmail.com</a></div></footer><script src="../enhancements.js" defer></script></body></html>'''

def cards(items):
    return '<div class="grid grid-cols-1 md:grid-cols-3 gap-6">'+''.join(f'<div class="bg-white p-7 rounded-2xl border border-outline-variant/50"><span class="material-symbols-outlined text-primary text-3xl">{i}</span><h3 class="text-xl font-bold text-forest-deep mt-4">{t}</h3><p class="mt-3 leading-relaxed text-on-surface-variant">{b}</p></div>' for i,t,b in items)+'</div>'
def sec(title,body,inner='',green=False):
    bg='bg-primary-container/50' if green else 'bg-surface'
    return f'<section class="py-16 md:py-24 {bg}"><div class="max-w-container-max mx-auto px-5 md:px-12"><div class="max-w-3xl mb-10"><h2 class="text-3xl md:text-4xl font-bold text-forest-deep">{title}</h2><p class="mt-4 text-lg leading-relaxed text-on-surface-variant">{body}</p></div>{inner}</div></section>'
def img(page,n=0):
    arr=imgs.get(page) or imgs.get('index.html') or ['']; return arr[min(n,len(arr)-1)]

def write_en(name,title,desc,hero,hero_body,hero_img,content):
    d=ROOT/'en'; d.mkdir(exist_ok=True); (d/name).write_text(shell(title,desc,name,hero,hero_body,hero_img,content),encoding='utf-8')

home=sec('A Complete 360° Corporate Wellness Experience','Green Therapy brings spa, health, and energy directly to your event—at the office, outdoors, or at an offsite venue.',cards([('inventory_2','Turnkey Production','Equipment, styling, logistics, and on-site operation in one coordinated solution.'),('verified_user','Experienced, Certified Team','Highly experienced, certified practitioners with uncompromising service standards.'),('event_available','Smooth Scheduling','An organized appointment booking system keeps treatment flow smooth with zero unnecessary wait times.')]),True)+sec('Four Ways to Build the Experience','Choose one activity or combine several into one event.',cards([('spa','Luxury Pop-Up Spa','Swedish massage, Thai stretch, Shiatsu, head & facial relaxation, and authentic foot reflexology.'),('ac_unit','Ice Bath Experience','Guided cold exposure for focus, resilience, energy, and team bonding.'),('self_improvement','Mind & Body Workshops','Yoga, guided meditation, mindfulness, Sound Healing, and wellbeing keynotes.'),('nutrition','Healthy Bar','Made-to-order natural smoothies and fruit & superfood bowls with fresh fruit, seeds, and nuts.')] ))+sec('Real Client Messages','Authentic feedback sent to Green Therapy after events.','<div class="grid md:grid-cols-2 gap-8 max-w-3xl mx-auto"><img src="../assets/client-message-1.jpg" class="rounded-3xl shadow-xl mx-auto" alt="Real client message"/><img src="../assets/client-message-2.jpg" class="rounded-3xl shadow-xl mx-auto" alt="Real client message"/></div>',True)
write_en('index.html','Green Therapy | Premium Corporate Wellness Events','Corporate wellness pop-ups for company events.','Premium Corporate Wellness & Wellbeing Experiences for Company Events','Green Therapy brings a luxury retreat directly to your event with a tailored, end-to-end 360° solution.',img('index.html'),home)

spa=sec('Complete Professional Setup','A tranquil sanctuary brought directly to your event.',cards([('bed','Professional Setup','High-end massage tables, fresh linens, premium essential oils, elegant pop-up tents, and ambient decor.'),('groups','Top-Tier Therapists','Highly experienced, certified practitioners with uncompromising service standards.'),('event_available','Queue-Free Booking','Organized appointment booking keeps scheduling smooth and avoids unnecessary waiting.')]),True)+sec('Massage Menu','A varied menu allows the station to fit the audience and event.',cards([('spa','Swedish Massage','Classic relaxation massage.'),('self_improvement','Thai Stretch & Shiatsu','Release, stretching, and pressure-based bodywork.'),('face','Head, Face & Foot','Head & facial relaxation plus authentic foot reflexology.')]))
write_en('spa.html','Green Therapy | Luxury Corporate Pop-Up Spa','Luxury corporate massage stations.','Luxury Pop-Up Spa & Massage Station','A complete professional spa setup delivered directly to your company event.',img('spa.html'),spa)

ice=sec('Safety First','Guided by certified, fully insured instructors trained in cold exposure protocols.',cards([('verified_user','Certified Guidance','Professional facilitation with safety at the center.'),('ac_unit','Full Setup','Ice tubs and continuous ice supply are included.'),('music_note','Atmosphere','Curated background music and aesthetic event styling.')]),True)+sec('Peak Energy Experience','A high-energy activity designed to boost focus, resilience, and team bonding.')
write_en('ice-bath.html','Green Therapy | Ice Bath & Cold Exposure','Corporate ice bath experiences.','Ice Bath & Cold Exposure Experience','The ultimate high-energy attraction to boost focus, resilience, and team bonding.',img('ice-bath.html'),ice)

work=sec('Sessions Employees Can Take Back to Everyday Life','Engaging sessions designed to help employees recharge and build everyday resilience.',cards([('fitness_center','Yoga','Movement and recovery.'),('self_improvement','Guided Meditation & Mindfulness','Practical tools for calm, balance, and reducing burnout.'),('graphic_eq','Sound Healing','Immersive sound journeys for deep stress relief.'),('record_voice_over','Expert Keynotes','Lectures on physical health, mental wellbeing, and stress management.')]),True)
write_en('workshops.html','Green Therapy | Mind & Body Workshops','Corporate yoga, meditation, mindfulness, Sound Healing and keynotes.','Mind & Body Workshops & Keynotes','Engaging sessions to help employees recharge and build everyday resilience.',img('workshops.html'),work)

bar=sec('Fresh, Healthy & Visually Stunning','A premium food experience designed for company events.',cards([('local_bar','Made-to-Order Smoothies','Refreshing natural smoothies prepared fresh at the event.'),('nutrition','Fruit & Superfood Bowls','Fresh fruit, seeds, nuts, and superfoods.'),('photo_camera','Beautiful Presentation','Colorful, fresh, and designed to look great at the event.')]),True)
write_en('healthy-bar.html','Green Therapy | Nutritional Bar & Superfood Bowls','Healthy smoothie and superfood catering.','Nutritional Bar & Superfood Bowls','Refreshing made-to-order natural smoothies and rich fruit bowls topped with fresh fruits, seeds, and nuts.',img('healthy-bar.html'),bar)

about=sec('Why HR Teams & Event Producers Choose Green Therapy','The service is built around reducing operational friction while delivering a premium employee experience.',cards([('inventory_2','Turnkey Solution','We handle equipment, decor, logistics, and operation.'),('workspace_premium','High Service Standard','Strong emphasis on human interaction, representation, polished appearance, and professional execution.'),('tune','Flexible & Tailored','We build the experience around the event style, budget, and number of participants.')]),True)
write_en('about.html','Green Therapy | About','About Green Therapy corporate wellness events.','Green Therapy — Premium Corporate Wellness Events','We bring spa, wellness, and energy directly to your event with a complete, tailored 360° solution.',img('about.html'),about)

galimgs=(imgs.get('gallery.html') or imgs.get('index.html') or [])[:9]; grid='<div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">'+''.join(f'<img src="{x}" class="w-full h-72 object-cover rounded-3xl border border-outline-variant/50" loading="lazy" alt="Green Therapy event"/>' for x in galimgs)+'</div>'
write_en('gallery.html','Green Therapy | Events Gallery','Corporate wellness event gallery.','Corporate Wellness Event Gallery','A visual look at Green Therapy experiences across company events and wellness settings.',img('gallery.html'),sec('Real Event Atmosphere','Massage, ice baths, workshops, and healthy experiences.',grid,True))

form='''<form class="max-w-3xl grid md:grid-cols-2 gap-5 bg-white p-8 rounded-3xl border border-outline-variant/50" onsubmit="event.preventDefault();alert('Thank you! Your inquiry was received.');"><label>Full name *<input required class="mt-2 w-full rounded-lg"/></label><label>Company *<input required class="mt-2 w-full rounded-lg"/></label><label>Phone *<input required type="tel" class="mt-2 w-full rounded-lg"/></label><label>Business email *<input required type="email" class="mt-2 w-full rounded-lg"/></label><label>Estimated participants<select class="mt-2 w-full rounded-lg"><option>10–30</option><option>30–70</option><option>70–150</option><option>150–500</option><option>500+</option></select></label><label>Planned date<input type="date" class="mt-2 w-full rounded-lg"/></label><textarea class="md:col-span-2 rounded-lg" rows="4" placeholder="Tell us about the event"></textarea><button class="md:col-span-2 bg-forest-deep text-white py-3.5 rounded-lg font-bold">Send Event Brief</button></form>'''
write_en('contact.html','Green Therapy | Contact & Event Brief','Plan a corporate wellness event.','Plan Your Corporate Wellness Event','Tell us about the event and we will help shape the right mix of wellness experiences.',img('index.html',-1),sec('Tell Us About Your Event','Share the basic details and Green Therapy can build a tailored experience around your event, budget, and number of participants.',form,True))
