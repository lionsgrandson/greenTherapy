(()=>{
const ready=()=>{
 document.body.classList.add('gt-page-ready');
 const isEn=document.documentElement.lang==='en'||location.pathname.includes('/en/');
 // Reveal animations
 const sections=[...document.querySelectorAll('main > section')];
 sections.forEach((s,i)=>s.classList.add(i===0?'gt-visible':'gt-reveal'));
 if('IntersectionObserver'in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('gt-visible');io.unobserve(e.target)}}),{rootMargin:'0px 0px -6% 0px',threshold:.06});sections.slice(1).forEach(s=>io.observe(s))}else sections.forEach(s=>s.classList.add('gt-visible'));
 // Mobile navigation from the real desktop nav.
 const header=document.querySelector('header'); const nav=header?.querySelector('nav');
 if(header&&nav&&!header.querySelector('.gt-mobile-menu-toggle')){
   const actions=header.querySelector('[data-lang-switch]')?.parentElement;
   const btn=document.createElement('button');btn.type='button';btn.className='gt-mobile-menu-toggle';btn.setAttribute('aria-label',isEn?'Open menu':'פתיחת תפריט');btn.setAttribute('aria-expanded','false');
   actions?.appendChild(btn);
   const panel=document.createElement('nav');panel.className='gt-mobile-panel';panel.setAttribute('aria-label',isEn?'Mobile navigation':'ניווט במובייל');
   panel.innerHTML=nav.innerHTML;document.body.appendChild(panel);
   btn.addEventListener('click',()=>{const open=panel.classList.toggle('is-open');btn.setAttribute('aria-expanded',String(open))});
   panel.addEventListener('click',e=>{if(e.target.closest('a')){panel.classList.remove('is-open');btn.setAttribute('aria-expanded','false')}})
 }
 // Broken-image safety net.
 const fallback=(isEn?'../':'')+'assets/client/887e1d9b-94c2-49aa-b3b9-258f57aacf3c.webp';
 document.querySelectorAll('img').forEach(img=>img.addEventListener('error',()=>{if(img.src.endsWith(fallback))return;img.src=fallback},{once:true}));
 // Honest backend-ready forms: never show a false success.
 document.querySelectorAll('form[data-contact-form]').forEach(form=>{
   form.addEventListener('submit',async e=>{
     e.preventDefault(); const status=form.querySelector('.gt-form-status'); if(status){status.className='gt-form-status';status.textContent=isEn?'Sending…':'שולחים…'}
     try{
       const fd=new FormData(form); const payload=Object.fromEntries(fd.entries());
       const res=await fetch('/api/contact',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(payload)});
       const data=await res.json().catch(()=>({}));
       if(res.ok){if(status){status.classList.add('is-success');status.textContent=isEn?'Thank you. Your inquiry was sent.':'תודה, הפנייה נשלחה בהצלחה.'}form.reset();return}
       if(status){status.classList.add('is-error');status.innerHTML=isEn?'Online form delivery is not connected yet. Please email <a href="mailto:alongreentherapy@gmail.com">alongreentherapy@gmail.com</a>.':'שליחת הטופס עדיין אינה מחוברת. אפשר לפנות ישירות במייל: <a href="mailto:alongreentherapy@gmail.com">alongreentherapy@gmail.com</a>.'}
     }catch(err){if(status){status.classList.add('is-error');status.textContent=isEn?'Unable to send right now. Please use the email address on this page.':'לא ניתן לשלוח כרגע. אפשר לפנות באמצעות כתובת המייל שבעמוד.'}}
   })
 });

 // Floating WhatsApp button.
 if(!document.querySelector('.gt-floating-wa')){
   const a=document.createElement('a');a.className='gt-floating-wa';a.href='https://wa.me/972535324962';a.target='_blank';a.rel='noopener noreferrer';a.setAttribute('aria-label',isEn?'Chat on WhatsApp':'שיחה ב-WhatsApp');a.textContent='WA';document.body.appendChild(a);
 }
 // Native details FAQ: one open at a time, without hiding siblings.
 document.querySelectorAll('details').forEach(d=>{
   d.addEventListener('toggle',()=>{
     if(!d.open)return;
     const scope=d.closest('section')||document;
     scope.querySelectorAll('details[open]').forEach(other=>{if(other!==d)other.open=false});
   });
 });
 // If Material Symbols fails to load, replace critical raw icon names instead of showing implementation words.
 if(document.fonts){document.fonts.ready.then(()=>{if(document.fonts.check('16px "Material Symbols Outlined"'))return;const map={chat:'💬',call:'☎',phone:'☎',mail:'✉',location_on:'⌖',calendar_today:'▣',spa:'✦',send:'➜',north_east:'↗',arrow_back:'←',arrow_forward:'→',check_circle:'✓',verified:'✓'};document.querySelectorAll('.material-symbols-outlined').forEach(el=>{const k=el.textContent.trim();if(map[k])el.textContent=map[k];else el.textContent=''})})}
\n // Analytics is dormant until an ID is configured AND the visitor consents.
 const cfg=window.GREEN_THERAPY_CONFIG||{}; const key='gt-analytics-consent';
 const loadGA=()=>{if(!cfg.googleAnalyticsId||window.gtag)return;const s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(cfg.googleAnalyticsId);document.head.appendChild(s);window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('js',new Date());gtag('config',cfg.googleAnalyticsId,{anonymize_ip:true})};
 if(cfg.googleAnalyticsId){
   const consent=localStorage.getItem(key); if(consent==='granted')loadGA();
   if(!consent){const bar=document.createElement('div');bar.className='gt-cookie-banner';bar.innerHTML='<p>'+(isEn?'We use optional analytics only with your consent.':'אנו משתמשים בניתוח נתוני שימוש אופציונלי רק בהסכמתכם.')+'</p><div><button data-c="deny">'+(isEn?'Essential only':'חיוני בלבד')+'</button><button data-c="allow">'+(isEn?'Allow analytics':'אישור אנליטיקה')+'</button></div>';document.body.appendChild(bar);bar.addEventListener('click',e=>{const b=e.target.closest('button[data-c]');if(!b)return;const v=b.dataset.c==='allow'?'granted':'denied';localStorage.setItem(key,v);bar.remove();if(v==='granted')loadGA()})}
 }
};
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',ready):ready();
})();