(()=>{
const ready=()=>{
 const isEn=document.documentElement.lang==="en"||location.pathname.includes("/en/");
 // Mobile menu
 document.querySelectorAll(".gt-menu-toggle").forEach(btn=>btn.addEventListener("click",()=>{
   const nav=document.querySelector(".gt-mobile-nav");if(!nav)return;
   const open=nav.classList.toggle("is-open");btn.setAttribute("aria-expanded",String(open));
 }));
 // Accordion: only one answer open. No reveal classes are toggled here.
 const items=[...document.querySelectorAll(".gt-faq-item")];
 items.forEach(item=>{
   const btn=item.querySelector(".gt-faq-question");if(!btn)return;
   btn.addEventListener("click",()=>{
     const opening=!item.classList.contains("is-open");
     items.forEach(other=>{if(other!==item){other.classList.remove("is-open");other.querySelector(".gt-faq-question")?.setAttribute("aria-expanded","false")}});
     item.classList.toggle("is-open",opening);btn.setAttribute("aria-expanded",String(opening));
   });
 });
 // Restrained reveal animation.
 const reveal=[...document.querySelectorAll("[data-gt-reveal]")];
 if("IntersectionObserver" in window){
   const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("gt-visible");io.unobserve(e.target)}}),{threshold:.05,rootMargin:"0px 0px -4% 0px"});
   reveal.forEach(el=>io.observe(el));
 } else reveal.forEach(el=>el.classList.add("gt-visible"));
 // Floating WhatsApp button.
 if(!document.querySelector(".gt-wa-floating")){
   const a=document.createElement("a");a.className="gt-wa-floating";a.href="https://wa.me/972535324962";a.target="_blank";a.rel="noopener noreferrer";a.textContent="WA";a.setAttribute("aria-label",isEn?"Chat on WhatsApp":"שיחה ב-WhatsApp");document.body.appendChild(a);
 }
 // Contact forms: honest status only.
 document.querySelectorAll("form[data-contact-form]").forEach(form=>form.addEventListener("submit",async e=>{
   e.preventDefault();const status=form.querySelector(".gt-form-status");if(status)status.textContent=isEn?"Sending…":"שולחים…";
   try{
     const payload=Object.fromEntries(new FormData(form));
     const r=await fetch("/api/contact",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify(payload)});
     if(r.ok){if(status)status.textContent=isEn?"Thank you. Your inquiry was sent.":"תודה, הפנייה נשלחה.";form.reset()}
     else if(status)status.innerHTML=isEn?'The form is not connected yet. Please call <a href="tel:+972535324962">+972 53-532-4962</a>.':'הטופס עדיין לא מחובר. אפשר להתקשר ל-<a dir="ltr" href="tel:+972535324962">+972 53-532-4962</a>.';
   }catch{if(status)status.textContent=isEn?"Unable to send right now. Please call us.":"לא ניתן לשלוח כרגע. אפשר להתקשר אלינו."}
 }));
 // If external icon font fails, avoid raw icon words.
 if(document.fonts)document.fonts.ready.then(()=>{if(document.fonts.check('16px "Material Symbols Outlined"'))return;const map={call:"☎",menu:"☰",send:"➜",expand_more:"⌄",calendar_today:"▣",north_east:"↗",chat:"💬",location_on:"⌖",check_circle:"✓",arrow_back:"←",arrow_forward:"→"};document.querySelectorAll(".material-symbols-outlined").forEach(el=>{const k=el.textContent.trim();el.textContent=map[k]||""})});
};
document.readyState==="loading"?document.addEventListener("DOMContentLoaded",ready):ready();
})();