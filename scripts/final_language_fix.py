#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup, Comment, NavigableString
import re

ROOT=Path(__file__).resolve().parents[1]
HE=["index.html","spa.html","ice-bath.html","workshops.html","healthy-bar.html","about.html","gallery.html","contact.html"]
ALL=HE+[f"en/{p}" for p in HE]

EN_REPL={
"Opening and explanation of the course of the experience and the important highlights before baptism.":"We start with a clear briefing on the experience and the key points before entering the ice bath.",
"How do you turn an idea into a pampering and sweet health complex in the field?":"How do we turn an idea into a polished wellness experience at your event?",
"Equipment, decor and meticulous visibility as part of a professional and inviting experience.":"Equipment, styling and a polished presentation as part of a professional, welcoming experience.",
"Human relations and meticulous visibility":"Warm service and a polished presentation",
"Strong emphasis on human relations, representativeness, meticulous visibility and service at the highest level.":"Strong emphasis on warm interpersonal service, a polished presentation and professional delivery.",
"High service standard: human relations, representativeness, meticulous visibility and uncompromising professionalism.":"High service standards: warm interpersonal service, a polished presentation and professional delivery.",
"Name of the company / organization *":"Company / Organization *",
"High-tech company Ltd":"Company name",
"Email at work *":"Work Email *",
"A major issue":"Main Interest",
"small group":"Small group",
"A large company event":"Large company event",
"quiet head":"Peace of Mind",
"Customized content and well-being complexes":"Tailored Wellness & Wellbeing Experiences",
"What does the complex that comes to you in the field include?":"What’s included in the Pop-Up Spa setup?",
"We take care of all the equipment, decor, logistics and operation - you just have to come and enjoy.":"We handle the equipment, styling, logistics and on-site operation so your team can focus on the event.",
"Understand the nature of the event, the budget, the number of participants and the location - in the office, in nature or on the event site.":"We start by understanding the event format, budget, participant count and venue.",
"Understand the nature of the event, the budget, the number of participants and the location.":"We start by understanding the event format, budget, participant count and venue.",
"Adjustment to the nature of the event and the audience":"Tailored to the event and audience",
"Full customization to the nature of the event, the budget and the number of participants":"Tailored to the event format, budget and participant count",
"Content adapted to the nature of the event":"Content tailored to the event",
"Sending a request for a quote":"Request a Proposal",
"Share with us the nature of the event, the budget and the number of participants and we will build together the appropriate menu of workshops and experiences.":"Tell us about your event, budget and participant count, and we’ll build the right mix of workshops and experiences.",
"Days of formation and recovery":"Wellbeing Days",
"Pop-up massage in the office":"Pop-Up Spa at the Office",
"Ice bath workshops":"Ice Bath Experiences",
"Customized wellness packages":"Tailored Wellness Experiences",
}

def replace_text(soup,mapping):
    for n in list(soup.find_all(string=True)):
        if isinstance(n,Comment) or not isinstance(n,NavigableString): continue
        if n.parent and n.parent.name in {"script","style"}: continue
        s=str(n); t=s
        for a,b in mapping.items(): t=t.replace(a,b)
        if t!=s: n.replace_with(t)

for p in ALL:
    f=ROOT/p
    soup=BeautifulSoup(f.read_text(encoding="utf-8"),"html.parser")
    # ensure skip link target always valid
    main=soup.find("main")
    if main: main["id"]="main-content"
    skip=soup.find("a",class_=lambda c: c and "gt-skip-link" in c if isinstance(c,str) else False)
    if skip: skip["href"]="#main-content"
    # remove fake Search Console placeholder
    for m in list(soup.find_all("meta",attrs={"name":"google-site-verification"})):
        if m.get("content")=="GT_SEARCH_CONSOLE_VERIFICATION": m.decompose()
    # remove implementation-only HTML comments from output
    for c in list(soup.find_all(string=lambda x:isinstance(x,Comment))):
        txt=str(c)
        if any(k in txt for k in ["JSON Conformance","Shared Component","Column","cols","B2B CONTACT","TOP APP BAR","FOOTER COMPONENT","Form (","Image Area"]):
            c.extract()
    if p.startswith("en/"): replace_text(soup,EN_REPL)
    f.write_text(str(soup),encoding="utf-8")

print("language/accessibility cleanup complete")
