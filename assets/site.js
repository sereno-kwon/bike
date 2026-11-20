/* bike.rubiworkshop.com shared behaviour. Every page works without this file;
   it only adds hotspots, gallery arrows, the active model-bar tab and GA4 events. */
(function(){
  /* Hotspots: .hot[data-f][data-x][data-y] inside a plate, paired with .flist button[data-f] */
  document.querySelectorAll('[data-hotspots]').forEach(function(root){
    var hots = root.querySelectorAll('.hot'), btns = root.querySelectorAll('.flist button');
    hots.forEach(function(h){ h.style.left = h.dataset.x + '%'; h.style.top = h.dataset.y + '%'; });
    function set(i){
      hots.forEach(function(h){ h.classList.toggle('on', +h.dataset.f === i); });
      btns.forEach(function(b){ var on = +b.dataset.f === i; b.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on)); });
    }
    hots.forEach(function(h){ h.addEventListener('click', function(){ set(+h.dataset.f); }); });
    btns.forEach(function(b){ b.addEventListener('click', function(){ set(+b.dataset.f); }); });
  });

  /* Galleries: [data-gallery] with .gallery, [data-prev], [data-next], .gcount */
  document.querySelectorAll('[data-gallery]').forEach(function(root){
    var g = root.querySelector('.gallery'), c = root.querySelector('.gcount');
    if (!g) return;
    function step(){ var p = g.querySelector('.plate'); return p ? p.getBoundingClientRect().width + 16 : 300; }
    var prev = root.querySelector('[data-prev]'), next = root.querySelector('[data-next]');
    if (prev) prev.addEventListener('click', function(){ g.scrollBy({ left: -step(), behavior: 'smooth' }); });
    if (next) next.addEventListener('click', function(){ g.scrollBy({ left: step(), behavior: 'smooth' }); });
    if (c) g.addEventListener('scroll', function(){
      var n = g.children.length, i = Math.min(n, Math.round(g.scrollLeft / step()) + 1);
      c.textContent = i + ' / ' + n;
    }, { passive: true });
  });

  /* Model bar: highlight the tab of the section in view */
  var links = document.querySelectorAll('.tabs a[href^="#"]');
  if (links.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if (!e.isIntersecting) return;
        links.forEach(function(a){
          var on = a.getAttribute('href') === '#' + e.target.id;
          a.classList.toggle('on', on);
          if (on && a.parentNode.scrollWidth > a.parentNode.clientWidth) a.parentNode.scrollTo({ left: a.offsetLeft - 16, behavior: 'smooth' });
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    links.forEach(function(a){ var s = document.getElementById(a.getAttribute('href').slice(1)); if (s) io.observe(s); });
  }
})();

/* GA4 events (shared across Rubi Company brand sites). Sends nothing while GA_ID is empty.
   section_view, consulting_click, model_click, dealer_click, social_click, image_view */
(function(){
  function track(name, params){ if (window.GA_ID && typeof gtag === 'function') gtag('event', name, params || {}); }
  function where(a){
    if (a.getAttribute('data-ga')) return a.getAttribute('data-ga');
    if (a.closest('header')) return 'header';
    if (a.closest('.modelbar')) return 'modelbar';
    if (a.closest('footer')) return 'footer';
    var s = a.closest('section[id], [data-sec][id]');
    return s ? s.id : 'other';
  }
  if ('IntersectionObserver' in window) {
    var seen = {};
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){
      var id = e.target.id;
      if (!e.isIntersecting || seen[id] || !window.GA_ID) return;
      seen[id] = 1; track('section_view', { section_name: id });
    }); }, { rootMargin: '-40% 0px -55% 0px' });
    document.querySelectorAll('section[id], [data-sec][id]').forEach(function(s){ io.observe(s); });
  }
  document.addEventListener('click', function(e){
    var t = e.target, a = t.closest && t.closest('a');
    if (a) {
      var href = a.getAttribute('href') || '';
      if (a.hasAttribute('data-consult') || /rubiworkshop\.com\/models/.test(href)) return track('consulting_click', { link_location: where(a), model: document.body.getAttribute('data-model') || '' });
      if (a.closest('.models')) return track('model_click', { model: a.getAttribute('data-model') || href });
      if (/rubisupply\.com/.test(href)) return track('dealer_click', { link_location: where(a) });
      var m = href.match(/instagram|kakao|youtube/);
      if (m) track('social_click', { network: m[0], link_location: where(a) });
      return;
    }
    var g = t.closest && t.closest('[data-gallery]');
    if (g && t.closest('figure')) track('image_view', { gallery: g.getAttribute('data-gallery') || 'gallery' });
  }, true);
})();
