import React, {useEffect, useMemo, useRef, useState} from "react";
import {createRoot} from "react-dom/client";
import {
  ArrowLeft, ArrowRight, CalendarDays, Check, ChevronDown, ExternalLink, IceCreamBowl,
  Leaf, Mail, MapPin, Menu, Phone, Send, Sparkles, X
} from "lucide-react";
import "./styles.css";

const PHONE_DISPLAY = "+972 53-532-4962";
const PHONE_TEL = "+972535324962";
const WA = "https://wa.me/972535324962";
const EMAIL = "alongreentherapy@gmail.com";
const GOOGLE_BUSINESS = "https://share.google/hEvKhs5USb65ZEgi7";

const IMG = {
  spa: "/assets/client/887e1d9b-94c2-49aa-b3b9-258f57aacf3c.webp",
  ice: "/assets/client/1c3d140a-38a4-4aff-8196-9fea60c15ae3.webp",
  workshops: "/assets/client/827ed1a7-ce8f-428f-91c1-20ac014453bf.webp",
  healthy: "/assets/client/95941eaf-fc13-49b4-a515-c9d66f1fdb6e.webp",
  atmosphere: "/assets/client/fe5e6cfc-8689-4287-8189-7286edf4bb30.webp",
  logo: "/assets/green-therapy-logo.webp"
};

const copy = {
  he: {
    dir:"rtl",
    nav:[
      ["","בית"],["spa","ספא פופ-אפ"],["ice-bath","אמבטיות קרח"],["workshops","סדנאות גוף ונפש"],
      ["healthy-bar","בר בריאות"],["gallery","גלריה"],["about","אודות"],["contact","צור קשר"]
    ],
    plan:"לתכנון אירוע",
    phone:"טלפון",
    email:"מייל",
    address:"כתובת",
    viewAddress:"לצפייה בכתובת",
    links:"קישורים",
    legal:"משפטי",
    contact:"צור קשר",
    privacy:"מדיניות פרטיות",
    accessibility:"הצהרת נגישות",
    send:"שלח",
    formTitle:"שליחת פרטים וקבלת הצעה",
    formIntro:"השאירו כמה פרטים ונחזור אליכם כדי להתאים את החוויה לאירוע.",
    fields:{name:"שם מלא",company:"חברה / ארגון",phone:"טלפון",email:"מייל",message:"ספרו לנו בקצרה על האירוע"},
    required:"שדה חובה",
    more:"צריכים פרטים נוספים?",
    callUs:"דברו איתנו",
    services:"החוויות שלנו",
    home:{
      title:"Wellness שמגיע עד האירוע שלכם",
      intro:"Green Therapy יוצרת מתחמי בריאות, רוגע ואנרגיה לאירועי חברה — במשרד, בטבע או באתר האירוע. אנחנו מתאימים את החוויה לקהל, ללוח הזמנים ולתקציב.",
      cta:"לתכנון אירוע",
      secondary:"לכל החוויות",
      whyTitle:"מעטפת הפקה מלאה – אנחנו דואגים לפרטים",
      why:[
        ["הקמה ותפעול","ציוד, עיצוב, לוגיסטיקה ותפעול מלא במקום."],
        ["צוות מקצועי","מטפלים ומנחים מנוסים, שירותיים ומקצועיים."],
        ["התאמה לאירוע","התאמה לכמות המשתתפים, למיקום וללוח הזמנים."]
      ],
      workshopTitle:"סדנאות מעשיות ומרתקות",
      workshopText:"יוגה, מדיטציה מודרכת, מיינדפולנס, Sound Healing והרצאות העשרה כחלק מאירוע Wellbeing מדויק ונעים.",
      healthyTitle:"קולינריה בריאה ומעוצבת",
      healthyText:"שייקים טבעיים, קערות פירות וסופרפוד, פירות עונתיים, אגוזים וזרעים — בהגשה אסתטית שמתאימה לאירוע.",
      wellnessTitle:"הצימר ומתחם הבריאות של Green Therapy",
      wellnessText:"לצד מתחמי ה-Wellness שמגיעים לאירועי חברה, Green Therapy מפעילה גם מתחם בריאות ואירוח פרטי. לפרטים על אירוח, זמינות והחוויות במתחם — דברו איתנו.",
      reviewsTitle:"מה לקוחות כתבו אחרי האירוע"
    },
    spa:{
      title:"ספא פופ-אפ לאירועי חברה",
      intro:"מתחם טיפולים מוקפד שמגיע אליכם עם מיטות טיפול, מצעים נקיים, שמנים איכותיים, עיצוב נעים וצוות מקצועי.",
      section:"טיפולים שמתאימים לקצב של האירוע",
      items:["עיסוי שוודי","מתיחות ועיסוי תאילנדי","שיאצו","עיסוי ראש ופנים","רפלקסולוגיה ועיסוי כפות רגליים"],
      opsTitle:"איך זה עובד",
      ops:["מתאימים את היקף הצוות והעמדות לכמות המשתתפים.","מקימים מתחם נקי, נעים ומסודר במקום האירוע.","מתאמים זמני טיפול מראש לפי לוח הזמנים והזרימה באירוע."]
    },
    ice:{
      title:"חוויית שיא שמחברת אנרגיה, חוסן וגיבוש",
      intro:"חוויית חשיפה לקור ואמבטיות קרח בהנחיה מקצועית, עם ציוד ייעודי, אספקת קרח, מוזיקה ואווירה שמחברת את הקבוצה.",
      benefitsTitle:"מה החוויה נותנת לקבוצה",
      benefits:[
        ["אנרגיה ופוקוס","חוויה עוצמתית שמכניסה אנרגיה וקשב לאירוע."],
        ["חוסן אישי","התנסות מודרכת שמזמינה לצאת מאזור הנוחות בקצב אישי."],
        ["חיבור קבוצתי","חוויה משותפת שיוצרת רגע משמעותי וזכיר."]
      ],
      guidedTitle:"חוויה מודרכת, מקצועית ומעצימה",
      guided:[
        ["תדרוך ברור","הסבר קצר על מהלך החוויה והדגשים החשובים לפני הכניסה."],
        ["כניסה מודרכת","ליווי אישי ומקצועי לאורך ההתנסות, ללא לחץ על מי שלא רוצה להשתתף."],
        ["סיום משותף","חזרה רגועה לאירוע וסגירה קצרה שמחזירה את הקבוצה יחד."]
      ]
    },
    workshops:{
      title:"סדנאות גוף ונפש לאירועי חברה",
      intro:"תוכן שמוסיף לאירוע רגע של נשימה, נוכחות וחיבור — בפורמט שמתאים לארגון, לקבוצה ולמקום.",
      items:[
        ["יוגה","תרגול נגיש שמתאים לרמות שונות ומייצר תנועה, נשימה ורוגע."],
        ["מדיטציה ומיינדפולנס","תרגול מודרך שמאפשר לעצור, להתמקד ולהוריד עומס."],
        ["Sound Healing","חוויה מבוססת צליל שמייצרת מרחב שקט ומרגיע."],
        ["הרצאות העשרה","תוכן מקצועי על אורח חיים בריא, בריאות פיזית, Wellbeing והתמודדות עם סטרס."]
      ]
    },
    healthy:{
      title:"בר בריאות לאירועים",
      intro:"בר טרי, צבעוני ואסתטי שמוסיף אנרגיה לאירוע בלי להעמיס.",
      items:["שייקים טבעיים שמוכנים במקום","קערות פירות וסופרפוד","פירות עונתיים טריים","אגוזים, זרעים וסופרפוד"],
      noteTitle:"קולינריה בריאה ומעוצבת",
      note:"הבר נבנה בהתאם לאופי האירוע, לכמות המשתתפים ולמיקום, עם דגש על חומרי גלם טריים והגשה שמצטלמת מצוין."
    },
    about:{
      title:"Green Therapy",
      intro:"אנחנו יוצרים חוויות Wellness & Wellbeing לארגונים עם דגש על שירות אנושי, מקצועיות, אסתטיקה והתאמה מדויקת לאירוע.",
      body:"מהתכנון ועד ההקמה בשטח, אנחנו מרכזים את הציוד, הצוות, העיצוב והתפעול כך שלארגון נשארת כתובת אחת ברורה לכל החוויה."
    },
    gallery:{title:"גלריה",intro:"רגעים ממתחמי Green Therapy באירועי חברה."},
    contactPage:{
      title:"בואו נתכנן את החוויה הבאה",
      intro:"ספרו לנו בקצרה על האירוע ונחזור אליכם עם כיוון מתאים.",
      extra:"צריכים פרטים נוספים?"
    },
    faqTitle:"שאלות נפוצות לצוותי Wellbeing, HR והפקה",
    faqs:[
      ["לאילו אירועים זה מתאים?","לאירועי חברה, ימי Wellbeing, אירועי עובדים, כנסים ופעילויות ארגוניות במשרד, בטבע או באתר אירוע."],
      ["איך מתאימים את החוויה לכמות המשתתפים?","מתאימים את מספר העמדות, אנשי הצוות, משך הפעילות והזרימה לפי כמות המשתתפים ולוח הזמנים."],
      ["האם אפשר לשלב כמה מתחמים באותו אירוע?","כן. אפשר לשלב בין ספא פופ-אפ, אמבטיות קרח, סדנאות גוף ונפש ובר בריאות בהתאם לאופי האירוע ולתקציב."],
      ["כמה זמן מראש כדאי לפנות?","ככל שפונים מוקדם יותר קל יותר לשריין צוות וציוד, אבל אפשר לפנות גם לאירועים קרובים ונבדוק זמינות."]
    ]
  },
  en: {
    dir:"ltr",
    nav:[
      ["","Home"],["spa","Pop-Up Spa"],["ice-bath","Ice Baths"],["workshops","Mind & Body"],
      ["healthy-bar","Healthy Bar"],["gallery","Gallery"],["about","About"],["contact","Contact"]
    ],
    plan:"Plan an Event",
    phone:"Phone",
    email:"Email",
    address:"Address",
    viewAddress:"View on Google",
    links:"Links",
    legal:"Legal",
    contact:"Contact",
    privacy:"Privacy Policy",
    accessibility:"Accessibility",
    send:"Send",
    formTitle:"Send Details & Get a Proposal",
    formIntro:"Leave a few details and we’ll get back to tailor the experience to your event.",
    fields:{name:"Full name",company:"Company / Organization",phone:"Phone",email:"Email",message:"Tell us briefly about the event"},
    required:"Required",
    more:"Need more details?",
    callUs:"Call us",
    services:"Our Experiences",
    home:{
      title:"Wellness that comes to your event",
      intro:"Green Therapy creates corporate Wellness & Wellbeing experiences at the office, outdoors or at your event venue. Each experience is tailored to the audience, schedule and budget.",
      cta:"Plan an Event",
      secondary:"Explore Experiences",
      whyTitle:"Full-service production — we handle the details",
      why:[
        ["Setup & Operations","Equipment, styling, logistics and on-site operation."],
        ["Professional Team","Experienced, service-oriented practitioners and facilitators."],
        ["Tailored to the Event","Adapted to participant count, venue and schedule."]
      ],
      workshopTitle:"Practical, Engaging Workshops",
      workshopText:"Yoga, guided meditation, mindfulness, Sound Healing and expert talks as part of a considered Wellbeing experience.",
      healthyTitle:"Healthy, Beautiful Catering",
      healthyText:"Fresh smoothies, fruit and superfood bowls, seasonal fruit, nuts and seeds — presented in a clean, event-ready setup.",
      wellnessTitle:"Green Therapy Wellness & Hospitality Space",
      wellnessText:"Alongside our mobile corporate experiences, Green Therapy also operates a private wellness and hospitality space. Contact us for availability and current on-site experiences.",
      reviewsTitle:"What Clients Said After Their Events"
    },
    spa:{
      title:"Pop-Up Spa for Corporate Events",
      intro:"A polished treatment space brought to your event with treatment tables, fresh linens, quality oils, thoughtful styling and a professional team.",
      section:"Treatments that fit the flow of your event",
      items:["Swedish Massage","Thai Stretch & Massage","Shiatsu","Head & Facial Relaxation","Foot Massage & Reflexology"],
      opsTitle:"How It Works",
      ops:["We size the team and treatment stations to the participant count.","We build a clean, comfortable treatment area at the venue.","Treatment times are coordinated in advance around the event schedule and flow."]
    },
    ice:{
      title:"A Peak Experience Built Around Energy, Resilience & Connection",
      intro:"A professionally guided cold-exposure and ice-bath experience with dedicated equipment, continuous ice supply, music and a setup designed for the group.",
      benefitsTitle:"What the Experience Brings to the Group",
      benefits:[
        ["Energy & Focus","A strong shared moment that adds energy and attention to the event."],
        ["Personal Resilience","A guided challenge that invites people out of their comfort zone at their own pace."],
        ["Team Connection","A memorable shared experience that brings the group together."]
      ],
      guidedTitle:"Guided, Professional & Empowering",
      guided:[
        ["Clear Briefing","A concise explanation of the experience and key points before entering."],
        ["Guided Entry","Individual professional guidance throughout, with no pressure on anyone who prefers not to participate."],
        ["Shared Close","A calm return to the event and a short group close-out."]
      ]
    },
    workshops:{
      title:"Mind & Body Workshops for Corporate Events",
      intro:"Content that adds a moment of breathing room, presence and connection in a format tailored to the organization, group and venue.",
      items:[
        ["Yoga","Accessible movement and breathwork suitable for different levels."],
        ["Guided Meditation & Mindfulness","A guided practice for focus, calm and stress reduction."],
        ["Sound Healing","A sound-based experience that creates a calm, restorative space."],
        ["Expert Talks","Professional content on healthy living, physical health, Wellbeing and stress management."]
      ]
    },
    healthy:{
      title:"Healthy Bar for Events",
      intro:"A fresh, colorful and visually polished bar that adds energy to the event without feeling heavy.",
      items:["Fresh smoothies made on site","Fruit and superfood bowls","Fresh seasonal fruit","Nuts, seeds and superfoods"],
      noteTitle:"Healthy, Beautiful Catering",
      note:"The bar is tailored to the event, participant count and venue, with an emphasis on fresh ingredients and presentation."
    },
    about:{
      title:"Green Therapy",
      intro:"We create corporate Wellness & Wellbeing experiences with a focus on human service, professionalism, aesthetics and precise event fit.",
      body:"From planning through on-site setup, we coordinate equipment, team, styling and operations so the organization has one clear point of contact."
    },
    gallery:{title:"Gallery",intro:"Moments from Green Therapy corporate wellness experiences."},
    contactPage:{
      title:"Let’s Plan Your Next Wellness Experience",
      intro:"Tell us briefly about your event and we’ll get back with a suitable direction.",
      extra:"Need more details?"
    },
    faqTitle:"Frequently Asked Questions for Wellbeing, HR & Production Teams",
    faqs:[
      ["What events are a good fit?","Corporate events, Wellbeing days, employee events, conferences and company activities at the office, outdoors or at an event venue."],
      ["How do you adapt the experience to participant count?","We adjust the number of stations, team size, activity duration and flow to the participant count and schedule."],
      ["Can we combine several experiences?","Yes. Pop-Up Spa, ice baths, Mind & Body workshops and a Healthy Bar can be combined based on the event and budget."],
      ["How far in advance should we contact you?","Earlier gives more flexibility for team and equipment availability, but you can also contact us about upcoming events and we’ll check availability."]
    ]
  }
};

function normalizePath(){
  let p=window.location.pathname.replace(/^\/+|\/+$/g,"");
  p=p.replace(/\.html$/,"");
  if(p==="index") p="";
  return p;
}
function getRoute(){
  const p=normalizePath();
  const en=p==="en"||p.startsWith("en/");
  let slug=en?p.replace(/^en\/?/,""):p;
  if(slug==="index") slug="";
  return {lang:en?"en":"he",slug};
}
function href(lang,slug){
  const base=lang==="en"?"/en": "";
  return slug?base+"/"+slug:base+"/";
}

function useReveal(){
  useEffect(()=>{
    const nodes=[...document.querySelectorAll("[data-reveal]")];
    const io=new IntersectionObserver((entries)=>entries.forEach(e=>{
      if(e.isIntersecting){e.target.classList.add("is-visible");io.unobserve(e.target)}
    }),{threshold:.08,rootMargin:"0px 0px -5% 0px"});
    nodes.forEach(n=>io.observe(n));
    return()=>io.disconnect();
  },[]);
}

function Seo({lang,slug,title,description}){
  useEffect(()=>{
    document.documentElement.lang=lang;
    document.documentElement.dir=copy[lang].dir;
    document.title=title;
    const ensure=(selector,create)=>{
      let el=document.head.querySelector(selector);
      if(!el){el=create();document.head.appendChild(el)} return el;
    };
    const desc=ensure('meta[name="description"]',()=>Object.assign(document.createElement("meta"),{name:"description"}));
    desc.content=description;
    const canonical=ensure('link[rel="canonical"]',()=>{const l=document.createElement("link");l.rel="canonical";return l});
    canonical.href="https://green-therapy.netlify.app"+href(lang,slug);
    document.head.querySelectorAll('link[data-hreflang]').forEach(e=>e.remove());
    [["he",href("he",slug)],["en",href("en",slug)],["x-default",href("he",slug)]].forEach(([l,h])=>{
      const a=document.createElement("link");a.rel="alternate";a.hreflang=l;a.href="https://green-therapy.netlify.app"+h;a.dataset.hreflang="1";document.head.appendChild(a);
    });
  },[lang,slug,title,description]);
  return null;
}

function Header({lang,slug}){
  const t=copy[lang]; const [open,setOpen]=useState(false);
  return <header className="site-header">
    <div className="header-inner">
      <a className="brand" href={href(lang,"")} aria-label="Green Therapy">
        <img src={IMG.logo} alt="Green Therapy" width="170" height="106" />
      </a>
      <nav className="desktop-nav" aria-label={lang==="he"?"ניווט ראשי":"Primary navigation"}>
        {t.nav.map(([s,label])=><a key={s} className={slug===s?"active":""} href={href(lang,s)}>{label}</a>)}
      </nav>
      <div className="header-actions">
        <a className="phone-pill" href={"tel:"+PHONE_TEL}><Phone size={17}/><span>{PHONE_DISPLAY}</span></a>
        <a className="lang-pill" href={href(lang==="he"?"en":"he",slug)}>{lang==="he"?"EN":"HE"}</a>
        <button className="menu-btn" aria-label={open?(lang==="he"?"סגירת תפריט":"Close menu"):(lang==="he"?"פתיחת תפריט":"Open menu")} aria-expanded={open} onClick={()=>setOpen(!open)}>{open?<X/>:<Menu/>}</button>
      </div>
    </div>
    <a className="mobile-phone-bar" href={"tel:"+PHONE_TEL}><Phone size={16}/><span>{t.phone}:</span><strong dir="ltr">{PHONE_DISPLAY}</strong></a>
    <div className={"mobile-menu "+(open?"open":"")}>
      {t.nav.map(([s,label])=><a key={s} href={href(lang,s)}>{label}</a>)}
      <a className="mobile-phone" href={"tel:"+PHONE_TEL}><Phone size={18}/>{PHONE_DISPLAY}</a>
    </div>
  </header>
}

function Footer({lang}){
  const t=copy[lang];
  return <footer className="site-footer">
    <div className="footer-grid">
      <div className="footer-brand"><img src={IMG.logo} alt="Green Therapy" loading="lazy"/></div>
      <div><h2>{t.links}</h2><ul>{t.nav.map(([s,l])=><li key={s}><a href={href(lang,s)}>{l}</a></li>)}</ul></div>
      <div><h2>{t.legal}</h2><ul><li><a href={href(lang,"privacy")}>{t.privacy}</a></li><li><a href={href(lang,"accessibility")}>{t.accessibility}</a></li></ul></div>
      <div><h2>{t.contact}</h2><ul className="contact-list">
        <li><strong>{t.phone}:</strong> <a dir="ltr" href={"tel:"+PHONE_TEL}>{PHONE_DISPLAY}</a></li>
        <li><strong>{t.email}:</strong> <a href={"mailto:"+EMAIL}>{EMAIL}</a></li>
        <li><strong>{t.address}:</strong> <a href={GOOGLE_BUSINESS} target="_blank" rel="noreferrer">{t.viewAddress} <ExternalLink size={14}/></a></li>
      </ul></div>
    </div>
  </footer>
}

function Layout({lang,slug,children,title,description}){
  useReveal();
  return <>
    <Seo lang={lang} slug={slug} title={title} description={description}/>
    <a className="skip-link" href="#main-content">{lang==="he"?"דלגו לתוכן":"Skip to content"}</a>
    <Header lang={lang} slug={slug}/>
    <main id="main-content">{children}</main>
    <Footer lang={lang}/>
    <a className="floating-wa" href={WA} target="_blank" rel="noreferrer" aria-label={lang==="he"?"שיחה ב-WhatsApp":"Chat on WhatsApp"}>WA</a>
  </>
}

function Hero({lang,title,intro,image,primary=true}){
  const t=copy[lang];
  return <section className={"hero "+(!image?"hero-simple":"")} data-reveal>
    <div className="hero-copy">
      <h1>{title}</h1>
      <p>{intro}</p>
      <div className="hero-actions">
        <a className="btn primary" href={href(lang,"contact")}>{t.plan}{lang==="he"?<ArrowLeft/>:<ArrowRight/>}</a>
        <a className="btn ghost" href={"tel:"+PHONE_TEL}><Phone size={18}/>{PHONE_DISPLAY}</a>
      </div>
    </div>
    {image&&<div className="hero-media"><img src={image} alt="" fetchPriority="high"/></div>}
  </section>
}

function SectionTitle({children,lead}){return <div className="section-title" data-reveal><h2>{children}</h2>{lead&&<p>{lead}</p>}</div>}

function ExperienceCard({lang,title,text,img,hrefTo,imgClass=""}){
  return <article className="experience-card" data-reveal>
    <img className={imgClass} src={img} alt="" loading="lazy" decoding="async"/>
    <div><h3>{title}</h3><p>{text}</p><a href={href(lang,hrefTo)}>{lang==="he"?"לפרטים":"Learn more"} {lang==="he"?<ArrowLeft size={17}/>:<ArrowRight size={17}/>}</a></div>
  </article>
}

function ThreeGrid({items}){
  return <div className="three-grid">{items.map(([title,text],i)=><article className="feature-card" data-reveal key={i}><Sparkles size={24}/><h3>{title}</h3><p>{text}</p></article>)}</div>
}
function ItemGrid({items}){
  return <div className="item-grid">{items.map((item,i)=>{
    const [title,text]=Array.isArray(item)?item:[item,""];
    return <article className="item-card" data-reveal key={i}><Check size={20}/><div><h3>{title}</h3>{text&&<p>{text}</p>}</div></article>
  })}</div>
}

const reviewsHE=[
  "מבסוטים לאללה, היו תגובות חמות. תודה רבה על הכל. נדבר עוד באירוע הבא 😉",
  "כולן הספיקו וכולן נהנו. תודה לך אלון על הכל! למרות הבלת״ם, קיבלתי הרבה מחמאות.",
  "היה מעולה ממש. פידבקים מעולים על המטפלות והיחס. תודה רבה 🙏",
  "וואו, היה לנו פשוט מושלם באמת. יצאנו מבסוטיות ממש, ויש לה סבלנות מדהימה ❤️"
];
const reviewsEN=[
  "Everyone was really happy and the feedback was warm. Thank you for everything — we’ll talk again for the next event.",
  "Everyone got a treatment and everyone enjoyed it. Thank you, Alon. I received so many compliments.",
  "It was excellent. We received great feedback about the therapists and the way everyone was treated. Thank you.",
  "It was genuinely perfect. We left very happy, and the therapist had incredible patience."
];
function Reviews({lang}){
  const arr=lang==="he"?reviewsHE:reviewsEN;
  return <section className="reviews-section">
    <SectionTitle>{copy[lang].home.reviewsTitle}</SectionTitle>
    <div className="reviews-grid">{arr.map((r,i)=><blockquote className="review" data-reveal key={i}><div className="stars" aria-label="5 stars">★★★★★</div><p>{r}</p></blockquote>)}</div>
  </section>
}

function FAQ({lang}){
  const t=copy[lang]; const [open,setOpen]=useState(0);
  return <section className="faq-section">
    <SectionTitle>{t.faqTitle}</SectionTitle>
    <div className="faq-list">
      {t.faqs.map(([q,a],i)=><div className={"faq "+(open===i?"open":"")} key={q} data-reveal>
        <button aria-expanded={open===i} onClick={()=>setOpen(open===i?-1:i)}><span>{q}</span><ChevronDown/></button>
        <div className="faq-answer"><div><p>{a}</p></div></div>
      </div>)}
    </div>
  </section>
}

function ContactStrip({lang}){
  const t=copy[lang];
  return <section className="contact-strip" data-reveal><div><h2>{t.more}</h2><p>{lang==="he"?"אפשר לדבר איתנו ישירות ולבדוק התאמה וזמינות.":"Call us directly to discuss fit and availability."}</p></div><a className="btn light" href={"tel:"+PHONE_TEL}><Phone size={20}/>{PHONE_DISPLAY}</a></section>
}

function ContactForm({lang}){
  const t=copy[lang]; const [status,setStatus]=useState("");
  async function submit(e){
    e.preventDefault(); setStatus(lang==="he"?"שולחים...":"Sending...");
    const data=Object.fromEntries(new FormData(e.currentTarget));
    try{
      const r=await fetch("/api/contact",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(data)});
      if(r.ok){setStatus(lang==="he"?"תודה, הפנייה נשלחה.":"Thank you, your inquiry was sent.");e.currentTarget.reset()}
      else setStatus(lang==="he"?"הטופס עדיין לא מחובר למערכת שליחה. אפשר להתקשר או לשלוח WhatsApp.":"The form delivery service is not connected yet. Please call or use WhatsApp.");
    }catch{setStatus(lang==="he"?"לא ניתן לשלוח כרגע. אפשר להתקשר או לשלוח WhatsApp.":"Unable to send right now. Please call or use WhatsApp.")}
  }
  return <form className="contact-form" onSubmit={submit}>
    <div className="form-grid">
      <label>{t.fields.name}<input name="name" required autoComplete="name"/></label>
      <label>{t.fields.company}<input name="company" autoComplete="organization"/></label>
      <label>{t.fields.phone}<input name="phone" required type="tel" dir="ltr" autoComplete="tel"/></label>
      <label>{t.fields.email}<input name="email" type="email" dir="ltr" autoComplete="email"/></label>
    </div>
    <label>{t.fields.message}<textarea name="message" rows="4"/></label>
    <input className="honeypot" name="company_website" tabIndex="-1" autoComplete="off"/>
    <button className="btn primary submit" type="submit"><Send size={18}/>{t.send}</button>
    <div className="form-status" role="status" aria-live="polite">{status}</div>
  </form>
}

function Home({lang}){
  const t=copy[lang],h=t.home;
  return <Layout lang={lang} slug="" title={lang==="he"?"Green Therapy | Wellness & Wellbeing לאירועי חברה":"Green Therapy | Corporate Wellness & Wellbeing"} description={h.intro}>
    <Hero lang={lang} title={h.title} intro={h.intro}/>
    <section className="section">
      <SectionTitle>{t.services}</SectionTitle>
      <div className="experiences">
        <ExperienceCard lang={lang} title={lang==="he"?"ספא פופ-אפ":"Pop-Up Spa"} text={lang==="he"?"טיפולי מגע באווירה נעימה ומוקפדת, אצלכם באירוע.":"Professional treatments in a calm, polished setup at your event."} img={IMG.spa} hrefTo="spa"/>
        <ExperienceCard lang={lang} title={lang==="he"?"אמבטיות קרח":"Ice Baths"} text={lang==="he"?"חשיפה לקור בהנחיה מקצועית כחוויה קבוצתית עוצמתית.":"Professionally guided cold exposure as a powerful group experience."} img={IMG.ice} hrefTo="ice-bath"/>
        <ExperienceCard lang={lang} title={h.workshopTitle} text={h.workshopText} img={IMG.workshops} hrefTo="workshops"/>
        <ExperienceCard lang={lang} title={h.healthyTitle} text={h.healthyText} img={IMG.healthy} hrefTo="healthy-bar" imgClass="face-focus"/>
      </div>
    </section>
    <section className="section soft"><SectionTitle>{h.whyTitle}</SectionTitle><ThreeGrid items={h.why}/></section>
    <Reviews lang={lang}/>
    <section className="section wellness-space" data-reveal>
      <div className="wellness-copy"><h2>{h.wellnessTitle}</h2><p>{h.wellnessText}</p><a className="btn primary" href={href(lang,"contact")}>{t.plan}</a></div>
      <img src={IMG.atmosphere} alt="" loading="lazy"/>
    </section>
    <FAQ lang={lang}/>
    <ContactStrip lang={lang}/>
  </Layout>
}

function ServicePage({lang,type}){
  const t=copy[lang]; const d=t[type];
  const images={spa:IMG.atmosphere,ice:IMG.ice,workshops:IMG.workshops,healthy:IMG.healthy};
  const titles={spa:"spa",ice:"ice-bath",workshops:"workshops",healthy:"healthy-bar"};
  const seoTitle={
    spa:lang==="he"?"ספא פופ-אפ לאירועי חברה | Green Therapy":"Pop-Up Spa for Corporate Events | Green Therapy",
    ice:lang==="he"?"אמבטיות קרח לאירועי חברה | Green Therapy":"Ice Bath Experience | Green Therapy",
    workshops:lang==="he"?"סדנאות גוף ונפש לאירועי חברה | Green Therapy":"Mind & Body Workshops | Green Therapy",
    healthy:lang==="he"?"בר בריאות לאירועים | Green Therapy":"Healthy Bar for Events | Green Therapy"
  }[type];
  if(type==="spa") return <Layout lang={lang} slug="spa" title={seoTitle} description={d.intro}>
    <Hero lang={lang} title={d.title} intro={d.intro} image={images[type]}/>
    <section className="section"><SectionTitle>{d.section}</SectionTitle><ItemGrid items={d.items}/></section>
    <section className="section soft"><SectionTitle>{d.opsTitle}</SectionTitle><ThreeGrid items={d.ops.map((x,i)=>[lang==="he"?["התאמה","הקמה","תיאום"][i]:["Planning","Setup","Coordination"][i],x])}/></section>
    <FAQ lang={lang}/><ContactStrip lang={lang}/>
  </Layout>;
  if(type==="ice") return <Layout lang={lang} slug="ice-bath" title={seoTitle} description={d.intro}>
    <Hero lang={lang} title={d.title} intro={d.intro} image={images[type]}/>
    <section className="section"><SectionTitle>{d.benefitsTitle}</SectionTitle><ThreeGrid items={d.benefits}/></section>
    <section className="section soft"><SectionTitle>{d.guidedTitle}</SectionTitle><ThreeGrid items={d.guided}/></section>
    <FAQ lang={lang}/><ContactStrip lang={lang}/>
  </Layout>;
  if(type==="workshops") return <Layout lang={lang} slug="workshops" title={seoTitle} description={d.intro}>
    <Hero lang={lang} title={d.title} intro={d.intro} image={images[type]}/>
    <section className="section"><SectionTitle>{lang==="he"?"תוכן שמתאים לקבוצה ולאירוע":"Content Tailored to the Group and Event"}</SectionTitle><div className="workshop-grid">{d.items.map(([a,b],i)=><article className="workshop-card" data-reveal key={i}><Leaf/><h3>{a}</h3><p>{b}</p></article>)}</div></section>
    <FAQ lang={lang}/><ContactStrip lang={lang}/>
  </Layout>;
  return <Layout lang={lang} slug="healthy-bar" title={seoTitle} description={d.intro}>
    <Hero lang={lang} title={d.title} intro={d.intro} image={images[type]}/>
    <section className="section"><SectionTitle>{d.noteTitle}</SectionTitle><div className="healthy-layout" data-reveal><img className="face-focus" src={IMG.healthy} alt="" loading="lazy"/><div><p>{d.note}</p><ItemGrid items={d.items}/></div></div></section>
    <FAQ lang={lang}/><ContactStrip lang={lang}/>
  </Layout>;
}

function About({lang}){
  const t=copy[lang],d=t.about;
  return <Layout lang={lang} slug="about" title={lang==="he"?"אודות Green Therapy":"About Green Therapy"} description={d.intro}>
    <Hero lang={lang} title={d.title} intro={d.intro} image={IMG.spa}/>
    <section className="section about-copy" data-reveal><p>{d.body}</p></section>
    <ContactStrip lang={lang}/>
  </Layout>
}

function Gallery({lang}){
  const t=copy[lang],d=t.gallery;
  const imgs=[IMG.spa,IMG.ice,IMG.workshops,IMG.healthy,IMG.atmosphere,IMG.ice,IMG.healthy,IMG.spa];
  return <Layout lang={lang} slug="gallery" title={lang==="he"?"גלריה | Green Therapy":"Gallery | Green Therapy"} description={d.intro}>
    <section className="gallery-hero"><h1>{d.title}</h1><p>{d.intro}</p></section>
    <section className="gallery-grid">{imgs.map((src,i)=><figure key={i} data-reveal><img src={src} alt="" loading={i<2?"eager":"lazy"} decoding="async"/></figure>)}</section>
  </Layout>
}

function Contact({lang}){
  const t=copy[lang],d=t.contactPage;
  return <Layout lang={lang} slug="contact" title={lang==="he"?"צור קשר | Green Therapy":"Contact | Green Therapy"} description={d.intro}>
    <section className="contact-page">
      <div className="contact-copy" data-reveal><h1>{d.title}</h1><p>{d.intro}</p>
        <div className="contact-options">
          <a href={"tel:"+PHONE_TEL}><Phone/><div><strong>{t.phone}</strong><span dir="ltr">{PHONE_DISPLAY}</span></div></a>
          <a href={"mailto:"+EMAIL}><Mail/><div><strong>{t.email}</strong><span>{EMAIL}</span></div></a>
          <a href={GOOGLE_BUSINESS} target="_blank" rel="noreferrer"><MapPin/><div><strong>{t.address}</strong><span>{t.viewAddress}</span></div></a>
        </div>
      </div>
      <div className="contact-box" data-reveal><h2>{t.formTitle}</h2><p>{t.formIntro}</p><ContactForm lang={lang}/></div>
    </section>
    <section className="contact-strip" data-reveal><div><h2>{d.extra}</h2><p>{lang==="he"?"אפשר להתקשר ישירות.":"Call us directly."}</p></div><a className="btn light" href={"tel:"+PHONE_TEL}><Phone/>{PHONE_DISPLAY}</a></section>
  </Layout>
}

function Legal({lang,type}){
  const t=copy[lang],isPrivacy=type==="privacy";
  const title=isPrivacy?t.privacy:t.accessibility;
  return <Layout lang={lang} slug={type} title={title+" | Green Therapy"} description={title}>
    <article className="legal-page"><h1>{title}</h1>
      {isPrivacy ? <>
        <h2>{lang==="he"?"מידע שנמסר בטופס":"Information Submitted Through Forms"}</h2>
        <p>{lang==="he"?"פרטי קשר ופרטי אירוע שתבחרו למסור משמשים לצורך מענה לפנייה ותכנון השירות. מערכת השליחה החיצונית אינה מחוברת עד להגדרת יעד מאושר.":"Contact and event details you choose to submit are used to respond to your inquiry and plan the service. The external delivery destination remains disconnected until an approved endpoint is configured."}</p>
        <h2>{lang==="he"?"אנליטיקה וקובצי Cookie":"Analytics & Cookies"}</h2>
        <p>{lang==="he"?"Google Analytics אינו נטען כל עוד לא הוגדר מזהה מדידה ולא ניתנה הסכמה.":"Google Analytics does not load until a measurement ID is configured and consent is given."}</p>
      </>:<>
        <p>{lang==="he"?"האתר נבנה עם ניווט מקלדת, מבנה סמנטי, ניגודיות, טקסט חלופי, תמיכה בהפחתת תנועה וכלי נגישות חיצוני. אם נתקלתם בבעיה, נשמח לקבל פרטים ולתקן.":"The site includes keyboard navigation, semantic structure, contrast, image alternatives, reduced-motion support and an external accessibility tool. If you encounter a problem, contact us so we can address it."}</p>
      </>}
      <p><a href={"mailto:"+EMAIL}>{EMAIL}</a></p>
    </article>
  </Layout>
}

function App(){
  const {lang,slug}=useMemo(getRoute,[]);
  if(slug==="spa") return <ServicePage lang={lang} type="spa"/>;
  if(slug==="ice-bath") return <ServicePage lang={lang} type="ice"/>;
  if(slug==="workshops") return <ServicePage lang={lang} type="workshops"/>;
  if(slug==="healthy-bar") return <ServicePage lang={lang} type="healthy"/>;
  if(slug==="gallery") return <Gallery lang={lang}/>;
  if(slug==="about") return <About lang={lang}/>;
  if(slug==="contact") return <Contact lang={lang}/>;
  if(slug==="privacy") return <Legal lang={lang} type="privacy"/>;
  if(slug==="accessibility") return <Legal lang={lang} type="accessibility"/>;
  return <Home lang={lang}/>;
}

createRoot(document.getElementById("root")).render(<App/>);
