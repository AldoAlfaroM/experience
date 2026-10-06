// Animación de aparición al hacer scroll (en archivo externo para permitir una CSP sin 'unsafe-inline').
(() => {
  const els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    els.forEach(el => el.classList.add('in'));
    return;
  }
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: 0.12 });
  els.forEach(el => io.observe(el));
})();


// Cambio de tema claro/oscuro.
(() => {
  const btn = document.getElementById('theme-toggle');
  const meta = document.querySelector('meta[name="theme-color"]');
  const root = document.documentElement;
  const sync = () => {
    const light = root.dataset.theme === 'light';
    btn.setAttribute('aria-label', light ? 'Switch to dark theme' : 'Switch to light theme');
    if (meta) meta.content = light ? '#f7f7f5' : '#0f1115';
  };
  btn.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light';
    try { localStorage.setItem('theme', root.dataset.theme); } catch (_) {}
    sync();
  });
  sync();
})();
