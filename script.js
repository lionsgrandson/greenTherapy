const WHATSAPP_NUMBER = ""; // Add verified international number, digits only, before launch.

const menuButton = document.querySelector('.menu-btn');
const navLinks = document.querySelector('.nav-links');
if (menuButton && navLinks) {
  menuButton.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
  });
  navLinks.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
  }));
}

document.querySelectorAll('[data-whatsapp]').forEach(link => {
  if (WHATSAPP_NUMBER) {
    const text = encodeURIComponent(link.dataset.message || 'היי, אשמח לקבל פרטים על אירוע Wellness לארגון.');
    link.href = `https://wa.me/${WHATSAPP_NUMBER}?text=${text}`;
    link.target = '_blank';
    link.rel = 'noopener';
  } else {
    link.href = 'contact.html#event-form';
    link.title = 'מספר WhatsApp יעודכן לפני ההשקה';
  }
});

const observer = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 }) : null;

document.querySelectorAll('.reveal').forEach(el => observer ? observer.observe(el) : el.classList.add('visible'));

document.querySelectorAll('.filter-btn').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    button.classList.add('active');
    const filter = button.dataset.filter;
    document.querySelectorAll('.gallery-card').forEach(card => {
      card.hidden = filter !== 'all' && card.dataset.category !== filter;
    });
  });
});

const briefForm = document.querySelector('[data-multistep-form]');
if (briefForm) {
  const steps = [...briefForm.querySelectorAll('.form-step')];
  const progress = [...briefForm.querySelectorAll('.form-progress span')];
  let current = 0;
  const show = index => {
    current = Math.max(0, Math.min(index, steps.length - 1));
    steps.forEach((step, i) => step.classList.toggle('active', i === current));
    progress.forEach((bar, i) => bar.classList.toggle('active', i <= current));
    briefForm.querySelector('.form-card').scrollIntoView({behavior:'smooth', block:'start'});
  };
  briefForm.querySelectorAll('[data-next]').forEach(btn => btn.addEventListener('click', () => {
    const active = steps[current];
    const required = [...active.querySelectorAll('[required]')];
    if (required.some(field => !field.reportValidity())) return;
    show(current + 1);
  }));
  briefForm.querySelectorAll('[data-prev]').forEach(btn => btn.addEventListener('click', () => show(current - 1)));
  briefForm.addEventListener('submit', event => {
    event.preventDefault();
    steps[current].innerHTML = `
      <div style="padding:32px 0;text-align:center">
        <div class="card-icon" style="margin:0 auto 18px">✓</div>
        <h3 style="font-size:28px;margin:0 0 10px">תודה, הפרטים מוכנים לשליחה</h3>
        <p style="color:var(--on-surface-variant);max-width:560px;margin:0 auto">זהו אתר סטטי בשלב העיצוב. חיבור הטופס ל-CRM או למייל יבוצע בשלב האינטגרציה.</p>
      </div>`;
  });
}
