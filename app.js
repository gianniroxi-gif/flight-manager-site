(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('.lang-toggle');
  const translatable = [...document.querySelectorAll('[data-it][data-en]')];
  let language = 'it';

  function updateToday() {
    const target = document.querySelector('[data-today]');
    if (!target) return;
    const locale = language === 'it' ? 'it-IT' : 'en-GB';
    target.textContent = new Intl.DateTimeFormat(locale, {
      weekday: 'long', day: '2-digit', month: 'long',
    }).format(new Date());
  }

  function applyLanguage(next) {
    language = next;
    root.lang = language;
    translatable.forEach((node) => {
      node.innerHTML = node.dataset[language];
    });
    updateToday();
    if (toggle) {
      toggle.querySelector('span').style.color = language === 'it' ? 'var(--cyan)' : 'var(--muted)';
      toggle.querySelector('b').style.color = language === 'en' ? 'var(--cyan)' : 'var(--muted)';
      toggle.setAttribute('aria-label', language === 'it' ? 'Switch to English' : 'Passa all\'italiano');
    }
  }

  toggle?.addEventListener('click', () => applyLanguage(language === 'it' ? 'en' : 'it'));
  updateToday();

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
})();
