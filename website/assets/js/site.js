const toggle = document.querySelector('[data-nav-toggle]');
const nav = document.querySelector('[data-nav]');

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    nav.classList.toggle('is-open', !open);
  });

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    });
  });
}

const copyButton = document.querySelector('[data-copy-citation]');
const citation = document.querySelector('#bibtex');

if (copyButton && citation) {
  copyButton.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(citation.textContent.trim());
      const original = copyButton.textContent;
      copyButton.textContent = 'Copied';
      window.setTimeout(() => { copyButton.textContent = original; }, 1600);
    } catch (_error) {
      copyButton.textContent = 'Select and copy';
    }
  });
}

