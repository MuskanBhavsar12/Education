// Initialize AOS
AOS.init({ duration: 700, once: true, offset: 120, easing: 'ease-out-cubic' });

// Footer year
const yearEl = document.getElementById('year'); if (yearEl) yearEl.textContent = new Date().getFullYear();

// Navbar shrink + back-to-top
const nav = document.getElementById('mainNav');
const backToTop = document.getElementById('backToTop');
function onScroll() {
  if (nav) { if (window.scrollY > 30) nav.classList.add('scrolled'); else nav.classList.remove('scrolled'); }
  if (backToTop) backToTop.style.display = window.scrollY > 400 ? 'inline-flex' : 'none';
}
onScroll(); window.addEventListener('scroll', onScroll);
if (backToTop) backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// Close mobile menu on click
const wrap = document.getElementById('navLinks');
if (wrap) wrap.querySelectorAll('a.nav-link').forEach(a => a.addEventListener('click', () => {
  const c = bootstrap.Collapse.getInstance(wrap);
  if (c && window.innerWidth < 992) c.hide();
}));

// Notice bar with persistence
const notice = document.getElementById('noticeBar');
const closeNotice = document.getElementById('closeNotice');
if (notice) {
  const KEY = 'noticeClosed';
  if (localStorage.getItem(KEY) === '1') notice.style.display = 'none';
  if (closeNotice) closeNotice.addEventListener('click', () => { notice.style.display = 'none'; localStorage.setItem(KEY, '1'); });
}

// Gallery modal image
const galleryModal = document.getElementById('galleryModal');
if (galleryModal) {
  galleryModal.addEventListener('show.bs.modal', (e) => {
    const trigger = e.relatedTarget;
    const src = trigger?.getAttribute('data-bs-image');
    const modalImg = document.getElementById('modalImg');
    if (src && modalImg) modalImg.src = src;
  });
}

// Contact form: validate + send to Flask
const form = document.getElementById('contactForm');
if (form) {
  const formStatus = document.getElementById('formStatus');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    e.stopPropagation();

    if (!form.checkValidity()) {
      form.classList.add('was-validated');
      if (formStatus) formStatus.textContent = '';
      return;
    }

    const payload = {
      name: form.querySelector('[name="name"]').value.trim(),
      email: form.querySelector('[name="email"]').value.trim(),
      phone: form.querySelector('[name="phone"]').value.trim(),
      message: form.querySelector('[name="message"]').value.trim()
    };

    try {
      if (formStatus) { formStatus.classList.remove('text-danger','text-success'); formStatus.textContent = 'Submitting...'; }
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok || !data.ok) throw new Error(data.error || 'Failed');
      form.reset();
      form.classList.remove('was-validated');
      if (formStatus) { formStatus.textContent = 'Thank you! We will contact you soon.'; formStatus.classList.add('text-success'); }
    } catch (err) {
      if (formStatus) { formStatus.textContent = 'Something went wrong. Please try again.'; formStatus.classList.add('text-danger'); }
    }
  });
}