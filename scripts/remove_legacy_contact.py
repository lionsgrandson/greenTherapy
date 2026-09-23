#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
PAGES=["index.html","spa.html","ice-bath.html","workshops.html","healthy-bar.html","about.html","contact.html","privacy.html","accessibility.html","terms.html"]

def remove_section_for(el):
    sec=el
    while sec and getattr(sec,"name",None)!="section":
        sec=sec.parent
    if sec: sec.decompose()
    else: el.decompose()

for page in PAGES:
    p=ROOT/page
    if not p.exists(): continue
    soup=BeautifulSoup(p.read_text(encoding="utf-8"),"html.parser")

    if page=="index.html":
        # Keep the original dark CTA section, but strip the old embedded mini-contact UI.
        quick=soup.find(id="quick-inquiry-modal")
        if quick: quick.decompose()
        # Reduce the CTA buttons to one clean action into the shared form.
        sec=soup.find("section",id="contact")
        if sec:
            buttons=sec.find("div",class_=lambda c:c and "flex" in c and "gap-4" in c if isinstance(c,str) else False)
            # Find the specific button row by links/buttons.
            for d in sec.find_all("div"):
                if d.find("button") and d.find("a"):
                    buttons=d
                    break
            if buttons:
                buttons.clear()
                a=soup.new_tag("a",href="#contact-form")
                a["class"]="inline-flex items-center justify-center bg-surface-bright text-forest-deep font-label-md text-label-md px-7 py-3.5 rounded-full hover:bg-primary-container shadow-md transition-all duration-200 font-bold".split()
                a.string="לתכנון אירוע"
                buttons.append(a)
    else:
        # Remove all legacy page-specific contact blocks. The shared component below is the only form/contact block.
        legacy=[]
        for cls in ["gt-service-contact-cta","gt-direct-contact"]:
            legacy.extend(soup.find_all(class_=lambda c,cls=cls: c and cls in (c if isinstance(c,list) else str(c)).split()))
        for el in legacy:
            if el and el.parent: remove_section_for(el)

    # Ice-bath hero: keep one CTA and point it to the shared form; remove quick contact duplication.
    if page=="ice-bath.html":
        for a in list(soup.find_all("a")):
            txt=a.get_text(" ",strip=True)
            if "יצירת קשר מהירה" in txt:
                a.decompose()
            elif a.get("href") in {"#quote-form","#booking-form","#contact-form"}:
                a["href"]="#contact-form"

    # Any stale in-page contact anchors now target the shared component.
    for a in soup.find_all("a"):
        if a.get("href") in {"#quote-form","#booking-form","#contact-form"}:
            a["href"]="#contact-form"

    # Give React contact root a stable scroll anchor without changing its component styling.
    root=soup.find(id="gt-contact-root")
    if root: root["data-contact-anchor"]="true"

    p.write_text(str(soup),encoding="utf-8")

# Shared component already renders <section id="contact">; use a non-conflicting anchor name for old CTAs.
js=ROOT/"shared-components.js"
c=js.read_text(encoding="utf-8")
c=c.replace('return h("section",{className:"gt-shared-contact",id:"contact"},','return h("section",{className:"gt-shared-contact",id:"contact-form"},')
js.write_text(c,encoding="utf-8")

print("Legacy contact blocks removed; one shared contact form remains per page.")
