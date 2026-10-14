// LAYRS logo: exactly as tall as the capital letters of the city's name, standing on the same baseline.
// Runs on its own, before the map loads; the logo stays hidden until the fonts are in and it is measured.
(function () {
  function fit() {
    var h1 = document.querySelector('h1'), logo = h1 && h1.querySelector('.layrs'), probe = h1 && h1.querySelector('.baseline');
    if (!logo || !probe) return;
    var cs = getComputedStyle(h1), ctx = document.createElement('canvas').getContext('2d');
    ctx.font = cs.fontStyle + ' ' + cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
    var name = h1.textContent.replace('LAYRS', '').trim();
    var cap = ctx.measureText(name.charAt(0) || 'H').actualBoundingBoxAscent;
    var base = probe.getBoundingClientRect().top - h1.getBoundingClientRect().top;
    logo.style.height = cap + 'px';
    logo.style.top = (base - cap) + 'px';
    logo.style.fontSize = (cap / 4.6) + 'px';
    h1.style.paddingLeft = (logo.getBoundingClientRect().width + cap * 0.22) + 'px';
    logo.classList.add('fitted');
  }
  function ready() { (document.fonts ? document.fonts.ready : Promise.resolve()).then(fit); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready); else ready();
  addEventListener('resize', fit);
})();
