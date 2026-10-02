(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('.lang-toggle');
  const translatable = [...document.querySelectorAll('[data-it][data-en]')];
  // La lingua di partenza e' quella della PAGINA, non sempre l'italiano: da
  // /en/ l'HTML servito e' gia' inglese. Prima era fissa a 'it' e il primo
  // tocco del selettore su /en/ non cambiava niente.
  let language = root.lang === 'en' ? 'en' : 'it';

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

  // Il selettore porta all'ALTRO INDIRIZZO, non scambia il testo sul posto.
  // Due ragioni: la scelta diventa un link condivisibile, e Google trova due
  // pagine invece di una — che e' il motivo per cui /en/ esiste. Se la pagina
  // di destinazione non ci fosse, si ripiega sullo scambio di prima.
  toggle?.addEventListener('click', (e) => {
    e.preventDefault();
    const dove = language === 'it' ? '/en/' : '/';
    if (location.pathname !== dove) { location.href = dove; return; }
    applyLanguage(language === 'it' ? 'en' : 'it');
  });
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
