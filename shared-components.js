import React, {useMemo, useState} from "https://esm.sh/react@19.1.1";
import {createRoot} from "https://esm.sh/react-dom@19.1.1/client";

const h=React.createElement;
const PHONE="+972 53-532-4962";
const TEL="+972535324962";
const WA="https://wa.me/972535324962";
const EMAIL="alongreentherapy@gmail.com";
const MAP="https://share.google/hEvKhs5USb65ZEgi7";

const STRINGS={
  he:{
    nav:[
      ["index.html","דף הבית"],["spa.html","ספא פופ-אפ"],["ice-bath.html","אמבטיות קרח"],
      ["workshops.html","סדנאות גוף ונפש"],["healthy-bar.html","בר בריאות"],["about.html","אודות"],["contact.html","צור קשר"]
    ],
    plan:"לתכנון אירוע", links:"קישורים", legal:"משפטי", contact:"צור קשר",
    privacy:"מדיניות פרטיות", terms:"תנאי שימוש", accessibility:"הצהרת נגישות",
    phone:"טלפון", email:"מייל", address:"כתובת", map:"לצפייה במפה",
    formTitle:"יצירת קשר", formIntro:"השאירו כמה פרטים ונחזור אליכם כדי להתאים את החוויה לאירוע.",
    name:"שם מלא", emailField:"מייל", phoneField:"טלפון", message:"ספרו לנו בקצרה על האירוע", send:"שלח",
    sent:"תודה, הפנייה נשלחה.", notConnected:"שליחת הטופס עדיין אינה מחוברת. אפשר להתקשר או לשלוח הודעה בוואטסאפ.",
    sending:"שולחים…", menu:"פתיחת תפריט", close:"סגירת תפריט", language:"Switch to English", wa:"שיחה בוואטסאפ"
  },
  en:{
    nav:[
      ["index.html","Home"],["spa.html","Pop-Up Spa"],["ice-bath.html","Ice Baths"],
      ["workshops.html","Mind & Body"],["healthy-bar.html","Healthy Bar"],["about.html","About"],["contact.html","Contact"]
    ],
    plan:"Plan an Event", links:"Links", legal:"Legal", contact:"Contact",
    privacy:"Privacy Policy", terms:"Terms of Use", accessibility:"Accessibility Statement",
    phone:"Phone", email:"Email", address:"Address", map:"View on map",
    formTitle:"Contact Us", formIntro:"Leave a few details and we’ll get back to tailor the experience to your event.",
    name:"Full name", emailField:"Email", phoneField:"Phone", message:"Tell us briefly about the event", send:"Send",
    sent:"Thank you. Your inquiry was sent.", notConnected:"Form delivery is not connected yet. Please call or message us on WhatsApp.",
    sending:"Sending…", menu:"Open menu", close:"Close menu", language:"עבור לעברית", wa:"Chat on WhatsApp"
  }
};

function pageName(){
  let p=location.pathname.split("/").filter(Boolean).pop()||"index.html";
  if(!p.includes(".")) p=p+".html";
  return p;
}
function currentLang(){
  const q=new URLSearchParams(location.search).get("lang");
  if(q==="en"||q==="he") localStorage.setItem("gt-lang",q);
  return q==="en" ? "en" : (q==="he" ? "he" : (localStorage.getItem("gt-lang")==="en"?"en":"he"));
}
const LANG=currentLang();
const T=STRINGS[LANG];
const PAGE=pageName();

function withLang(path){
  if(LANG!=="en") return path;
  return path+"?lang=en";
}
function switchHref(){
  const u=new URL(location.href);
  if(LANG==="he") u.searchParams.set("lang","en");
  else u.searchParams.delete("lang");
  return u.pathname+(u.search?u.search:"");
}

function applyStaticTranslation(){
  document.documentElement.lang=LANG;
  document.documentElement.dir=LANG==="he"?"rtl":"ltr";
  document.body.classList.toggle("gt-lang-en",LANG==="en");
  document.body.classList.toggle("gt-lang-he",LANG==="he");
  if(LANG!=="en") return;
  const data=(window.GT_I18N&&window.GT_I18N[PAGE])||{};
  document.querySelectorAll("[data-i18n]").forEach(el=>{
    const v=data.text&&data.text[el.dataset.i18n];
    if(typeof v==="string") el.textContent=v;
  });
  document.querySelectorAll("[data-i18n-alt]").forEach(el=>{
    const v=data.alt&&data.alt[el.dataset.i18nAlt];
    if(typeof v==="string") el.alt=v;
  });
  if(data.title) document.title=data.title;
  const desc=document.querySelector('meta[name="description"]');
  if(desc&&data.description) desc.content=data.description;
}

function Header(){
  const [open,setOpen]=useState(false);
  return h("header",{className:"gt-react-header"},
    h("div",{className:"gt-react-header-inner"},
      h("a",{className:"gt-react-brand",href:withLang("index.html"),"aria-label":"Green Therapy"},
        h("img",{src:"assets/green-therapy-logo.webp",alt:"Green Therapy",width:170,height:106})
      ),
      h("nav",{className:"gt-react-nav","aria-label":LANG==="he"?"ניווט ראשי":"Primary navigation"},
        ...T.nav.map(([path,label])=>h("a",{key:path,href:withLang(path),className:"gt-react-nav-link "+(PAGE===path?"active":"")},label))
      ),
      h("div",{className:"gt-react-actions"},
        h("a",{className:"gt-react-phone",dir:"ltr",href:"tel:"+TEL},PHONE),
        h("a",{className:"gt-react-flag",href:switchHref(),"aria-label":T.language,title:T.language},LANG==="he"?"🇺🇸":"🇮🇱"),
        h("a",{className:"gt-react-cta",href:withLang("contact.html")},T.plan),
        h("button",{className:"gt-react-menu-btn",type:"button","aria-expanded":open,"aria-label":open?T.close:T.menu,onClick:()=>setOpen(!open)},open?"×":"☰")
      )
    ),
    h("a",{className:"gt-react-mobile-phone",dir:"ltr",href:"tel:"+TEL},PHONE),
    h("nav",{className:"gt-react-mobile-menu "+(open?"open":""),"aria-label":LANG==="he"?"ניווט במובייל":"Mobile navigation"},
      ...T.nav.map(([path,label])=>h("a",{key:path,href:withLang(path),className:PAGE===path?"active":""},label))
    )
  );
}

function Footer(){
  return h("footer",{className:"gt-react-footer"},
    h("div",{className:"gt-react-footer-grid"},
      h("div",{className:"gt-react-footer-brand"},
        h("a",{href:withLang("index.html")},h("img",{src:"assets/green-therapy-logo.webp",alt:"Green Therapy",loading:"lazy"}))
      ),
      h("div",null,h("h2",null,T.links),h("ul",null,...T.nav.map(([path,label])=>h("li",{key:path},h("a",{href:withLang(path)},label))))),
      h("div",null,h("h2",null,T.legal),h("ul",null,
        h("li",null,h("a",{href:withLang("privacy.html")},T.privacy)),
        h("li",null,h("a",{href:withLang("terms.html")},T.terms)),
        h("li",null,h("a",{href:withLang("accessibility.html")},T.accessibility))
      )),
      h("div",null,h("h2",null,T.contact),h("ul",{className:"gt-react-contact-list"},
        h("li",null,h("strong",null,T.phone+":")," ",h("a",{dir:"ltr",href:"tel:"+TEL,className:"gt-phone-isolate"},PHONE)),
        h("li",null,h("strong",null,T.email+":")," ",h("a",{href:"mailto:"+EMAIL},EMAIL)),
        h("li",null,h("strong",null,T.address+":")," ",h("a",{href:MAP,target:"_blank",rel:"noopener noreferrer"},T.map))
      ))
    )
  );
}

function ContactSection(){
  const [status,setStatus]=useState("");
  async function submit(e){
    e.preventDefault();
    setStatus(T.sending);
    const payload=Object.fromEntries(new FormData(e.currentTarget));
    try{
      const res=await fetch("/api/contact",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(payload)});
      if(res.ok){setStatus(T.sent);e.currentTarget.reset();}
      else setStatus(T.notConnected);
    }catch{setStatus(T.notConnected);}
  }
  return h("section",{className:"gt-shared-contact",id:"contact-form"},
    h("div",{className:"gt-shared-contact-inner"},
      h("div",{className:"gt-shared-contact-copy"},
        h("h2",null,T.formTitle),
        h("p",null,T.formIntro),
        h("div",{className:"gt-shared-contact-links"},
          h("a",{href:"tel:"+TEL},h("span",null,T.phone),h("strong",{dir:"ltr",className:"gt-phone-isolate"},PHONE)),
          h("a",{href:"mailto:"+EMAIL},h("span",null,T.email),h("strong",null,EMAIL)),
          h("a",{href:MAP,target:"_blank",rel:"noopener noreferrer"},h("span",null,T.address),h("strong",null,T.map))
        )
      ),
      h("form",{className:"gt-shared-contact-form",onSubmit:submit},
        h("input",{className:"gt-honeypot",name:"company_website",tabIndex:-1,autoComplete:"off","aria-hidden":"true"}),
        h("div",{className:"gt-shared-form-grid"},
          h("label",null,h("span",null,T.name),h("input",{name:"name",required:true,autoComplete:"name"})),
          h("label",null,h("span",null,T.phoneField),h("input",{name:"phone",required:true,type:"tel",dir:"ltr",autoComplete:"tel"})),
          h("label",null,h("span",null,T.emailField),h("input",{name:"email",type:"email",dir:"ltr",autoComplete:"email"}))
        ),
        h("label",null,h("span",null,T.message),h("textarea",{name:"message",rows:3})),
        h("button",{type:"submit"},T.send),
        h("div",{className:"gt-shared-form-status",role:"status","aria-live":"polite"},status)
      )
    )
  );
}

function FloatingWhatsApp(){
  return h("a",{className:"gt-floating-wa-react",href:WA,target:"_blank",rel:"noopener noreferrer","aria-label":T.wa,title:T.wa},"WA");
}

function initFaq(){
  document.querySelectorAll("details").forEach(d=>{
    d.classList.add("gt-faq-item");
    d.addEventListener("toggle",()=>{
      if(!d.open)return;
      const scope=d.closest("section")||document;
      scope.querySelectorAll("details[open]").forEach(other=>{if(other!==d) other.open=false;});
    });
  });
}

function initReveal(){
  const els=[...document.querySelectorAll("main > section, main article, main .tactile-card")].filter(el=>!el.closest("#gt-contact-root"));
  els.forEach(el=>el.dataset.gtReveal="");
  document.documentElement.classList.add("gt-animate-ready");
  if(!("IntersectionObserver" in window)){els.forEach(el=>el.classList.add("gt-visible"));return;}
  const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add("gt-visible");io.unobserve(e.target);}}),{threshold:.06,rootMargin:"0px 0px -5% 0px"});
  els.forEach(el=>io.observe(el));
}

function initMaterialIconFallback(){
  if(!document.fonts||!document.fonts.ready)return;
  document.fonts.ready.then(()=>{
    if(document.fonts.check('16px "Material Symbols Outlined"'))return;
    const map={
      chat:"💬",call:"☎",phone:"☎",mail:"✉",location_on:"⌖",calendar_today:"▣",event_available:"▣",
      spa:"✦",send:"➜",north_east:"↗",arrow_back:"←",arrow_forward:"→",chevron_left:"‹",
      check:"✓",check_circle:"✓",verified:"✓",verified_user:"✓",award_star:"★",stars:"★",
      ac_unit:"❄",air:"◌",all_inclusive:"∞",assignment_turned_in:"✓",bed:"▰",celebration:"✦",
      devices:"▣",diversity_3:"●",dry_cleaning:"◇",dynamic_form:"▦",energy_savings_leaf:"❧",
      fitness_center:"◆",forest:"♧",forum:"◌",graphic_eq:"≋",groups:"●",health_and_safety:"✚",
      healing:"✚",humidity_mid:"◌",inventory_2:"□",local_florist:"✿",local_shipping:"▱",
      military_tech:"★",nature_people:"♧",nutrition:"◉",palette:"◐",person_celebrate:"✦",
      photo_camera:"▣",pin_drop:"⌖",potted_plant:"♧",psychology:"◌",psychology_alt:"◌",
      recycling:"♻",restaurant_menu:"≡",rice_bowl:"◉",schedule:"◷",self_improvement:"◌",
      sentiment_satisfied:"☺",sentiment_very_satisfied:"☺",thermostat:"◌",tune:"≡",
      tungsten:"✦",volume_up:"◖",waves:"≈",wb_sunny:"☼",workspace_premium:"★",bolt:"ϟ",
      bathtub:"▰",business_center:"▣",eco:"❧",emoji_food_beverage:"◉",hourglass_empty:"⌛"
    };
    document.querySelectorAll(".material-symbols-outlined").forEach(el=>{
      const key=el.textContent.trim();
      el.textContent=map[key]||"•";
      el.setAttribute("aria-hidden","true");
    });
  });
}

function initLazy(){
  const imgs=[...document.querySelectorAll("main img")];
  imgs.forEach((img,i)=>{
    if(i===0||img.getAttribute("fetchpriority")==="high") return;
    img.loading="lazy";img.decoding="async";
  });
}

function updateSeo(){
  const data=(window.GT_I18N&&window.GT_I18N[PAGE])||{};
  const base="https://green-therapy.netlify.app/"+(PAGE==="index.html"?"":PAGE);
  let canonical=document.querySelector('link[rel="canonical"]');
  if(!canonical){canonical=document.createElement("link");canonical.rel="canonical";document.head.appendChild(canonical);}
  canonical.href=LANG==="en"?base+"?lang=en":base;
  document.querySelectorAll('link[rel="alternate"][hreflang],link[data-gt-hreflang]').forEach(x=>x.remove());
  [["he",base],["en",base+"?lang=en"],["x-default",base]].forEach(([lang,url])=>{
    const l=document.createElement("link");l.rel="alternate";l.hreflang=lang;l.href=url;l.dataset.gtHreflang="1";document.head.appendChild(l);
  });
  if(LANG==="en"&&data.title) document.title=data.title;
}

applyStaticTranslation();
updateSeo();
const headerRoot=document.getElementById("gt-header-root");
const footerRoot=document.getElementById("gt-footer-root");
const contactRoot=document.getElementById("gt-contact-root");
if(headerRoot) createRoot(headerRoot).render(h(Header));
if(footerRoot) createRoot(footerRoot).render(h(Footer));
if(contactRoot) createRoot(contactRoot).render(h(ContactSection));
const waRoot=document.createElement("div");waRoot.id="gt-wa-root";document.body.appendChild(waRoot);createRoot(waRoot).render(h(FloatingWhatsApp));
initFaq();initReveal();initLazy();initMaterialIconFallback();
