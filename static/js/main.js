document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const backdrop = document.querySelector('.nav-backdrop');

  function closeMenu() {
    document.body.classList.remove('menu-open');
    document.querySelectorAll('.has-dropdown.open').forEach(el => el.classList.remove('open'));
    if (toggle) {
      toggle.textContent = '☰';
      toggle.setAttribute('aria-label', 'Open menu');
    }
  }

  function openMenu() {
    document.body.classList.add('menu-open');
    if (toggle) {
      toggle.textContent = '✕';
      toggle.setAttribute('aria-label', 'Close menu');
    }
  }

  if (toggle) {
    toggle.addEventListener('click', () => {
      document.body.classList.contains('menu-open') ? closeMenu() : openMenu();
    });
  }
  if (backdrop) {
    backdrop.addEventListener('click', closeMenu);
  }

  // On mobile, dropdown parents (Programs/People/Media) need a tap to expand,
  // since hover doesn't exist on touch devices. Only the caret/label toggles
  // the submenu; the link itself still navigates normally on larger screens.
  document.querySelectorAll('.has-dropdown > a').forEach(link => {
    link.addEventListener('click', (e) => {
      if (window.innerWidth <= 900) {
        const parent = link.closest('.has-dropdown');
        const alreadyOpen = parent.classList.contains('open');
        e.preventDefault();
        document.querySelectorAll('.has-dropdown.open').forEach(el => {
          if (el !== parent) el.classList.remove('open');
        });
        parent.classList.toggle('open', !alreadyOpen);
      }
    });
  });

  // Close mobile menu on resize past the breakpoint (e.g. orientation change to tablet+)
  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) closeMenu();
  });
});
