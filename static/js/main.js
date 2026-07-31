// Mobile nav (simple show/hide via body class, styled in CSS media query fallback)
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const isOpen = links.style.display === 'flex';
      links.style.cssText = isOpen
        ? ''
        : 'display:flex; flex-direction:column; position:absolute; top:100%; left:0; right:0; background:#FBF8F2; padding:20px 28px; border-bottom:1px solid #E4DCC8;';
    });
  }
});
