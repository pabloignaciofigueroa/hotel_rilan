/* =========================================================
   RILÁN — movimiento e interacción
   Curvas: expo.out (arranque rápido, frenado suave) · power3.inOut (cortinas)
   ========================================================= */
(() => {
  'use strict';

  const root = document.documentElement;
  const loaderSafety = setTimeout(() => { const l = document.querySelector('.loader'); if (l) l.remove(); }, 7000);
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const desktop = window.matchMedia('(min-width: 900px)');
  const fine = window.matchMedia('(hover: hover) and (pointer: fine)');
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* sin almacenamiento */ } }
  };

  /* ---------- idioma ---------- */
  const swapAttr = (attr, key) => {
    $$(`[data-${key}-en]`).forEach(el => {
      if (el.dataset[key + 'Es'] === undefined) el.dataset[key + 'Es'] = el.getAttribute(attr) || '';
      el.setAttribute(attr, root.dataset.lang === 'en' ? el.dataset[key + 'En'] : el.dataset[key + 'Es']);
    });
  };
  const setLang = (l) => {
    root.dataset.lang = l;
    root.lang = l;
    store.set('rilan-lang', l);
    swapAttr('alt', 'alt');
    swapAttr('aria-label', 'aria');
    swapAttr('title', 'title');
    swapAttr('content', 'meta');
    $$('[data-on]').forEach(el => {
      const btn = el.closest('[data-sound]');
      el.textContent = btn && btn.getAttribute('aria-pressed') === 'true' ? el.dataset.on : el.dataset.off;
    });
    document.dispatchEvent(new CustomEvent('rilan:lang'));
  };
  const saved = store.get('rilan-lang');
  const browserEn = !saved && navigator.language && !navigator.language.toLowerCase().startsWith('es');
  setLang(saved || (browserEn ? 'en' : 'es'));
  $('[data-lang-toggle]')?.addEventListener('click', () => setLang(root.dataset.lang === 'es' ? 'en' : 'es'));

  /* ---------- evento con fecha ---------- */
  $$('[data-event-until]').forEach(el => {
    if (Date.now() > Date.parse(el.dataset.eventUntil)) el.hidden = true;
  });

  /* ---------- mapa diferido ---------- */
  const iframe = $('.arrive__map iframe');
  if (iframe && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((en) => {
      if (en[0].isIntersecting) { iframe.src = iframe.dataset.src; io.disconnect(); }
    }, { rootMargin: '600px' });
    io.observe(iframe);
  } else if (iframe) iframe.src = iframe.dataset.src;

  /* ---------- sonido de la ballena ---------- */
  const listenVideo = $('[data-listen-video]');
  const soundBtn = $('[data-sound]');
  const setSound = (on) => {
    if (!listenVideo) return;
    listenVideo.muted = !on;
    if (on) { listenVideo.volume = 0; listenVideo.play().catch(() => {}); fadeVolume(listenVideo, .9, 900); }
    soundBtn.setAttribute('aria-pressed', String(on));
    $$('[data-on]', soundBtn).forEach(el => { el.textContent = on ? el.dataset.on : el.dataset.off; });
  };
  function fadeVolume(v, to, ms) {
    const from = v.volume, t0 = performance.now();
    const step = (t) => { const p = Math.min(1, (t - t0) / ms); v.volume = from + (to - from) * (1 - Math.pow(1 - p, 3)); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  }
  soundBtn?.addEventListener('click', () => setSound(listenVideo.muted));

  /* videos: solo se reproducen en pantalla */
  const playInView = (v, onLeave) => {
    if (!v || !('IntersectionObserver' in window)) return;
    new IntersectionObserver((en) => {
      en.forEach(e => {
        if (e.isIntersecting) { if (v.preload === 'none') v.preload = 'auto'; v.play().catch(() => {}); }
        else { v.pause(); onLeave && onLeave(); }
      });
    }, { threshold: .15 }).observe(v);
  };
  playInView(listenVideo, () => { if (!listenVideo.muted) setSound(false); });
  playInView($('[data-portal-video]'));

  /* ---------- menú ---------- */
  const menu = $('[data-menu]');
  const openBtn = $('[data-menu-open]');
  let menuOpen = false;
  const toggleMenu = (open) => {
    if (open === menuOpen) return;
    menuOpen = open;
    openBtn.setAttribute('aria-expanded', String(open));
    if (open) {
      menu.hidden = false;
      lenis && lenis.stop();
      if (window.gsap && !reduced) {
        gsap.fromTo(menu, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: .9, ease: 'power3.inOut' });
        gsap.fromTo($$('.menu__w', menu), { yPercent: 110 }, { yPercent: 0, duration: .9, stagger: .05, ease: 'expo.out', delay: .35 });
      } else menu.style.clipPath = 'none';
      $('[data-menu-close]').focus();
    } else {
      const done = () => { menu.hidden = true; lenis && lenis.start(); openBtn.focus(); };
      if (window.gsap && !reduced) gsap.to(menu, { clipPath: 'inset(100% 0 0% 0)', duration: .7, ease: 'power3.inOut', onComplete: done });
      else done();
    }
  };
  openBtn?.addEventListener('click', () => toggleMenu(true));
  $('[data-menu-close]')?.addEventListener('click', () => toggleMenu(false));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && menuOpen) toggleMenu(false); });
  $$('[data-menu-key]').forEach(a => {
    const show = () => $$('[data-menu-img]').forEach(i => i.classList.toggle('is-on', i.dataset.menuImg === a.dataset.menuKey));
    a.addEventListener('mouseenter', show);
    a.addEventListener('focus', show);
    a.addEventListener('click', (e) => {
      e.preventDefault();
      const target = $(a.getAttribute('href'));
      toggleMenu(false);
      setTimeout(() => scrollToEl(target), reduced ? 0 : 500);
    });
  });

  /* ---------- scroll suave ---------- */
  let lenis = null;
  const scrollToEl = (el) => {
    if (!el) return;
    if (lenis) lenis.scrollTo(el, { duration: 1.6, easing: t => 1 - Math.pow(1 - t, 4) });
    else el.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
  };
  $$('a[href^="#"]').forEach(a => {
    if (a.hasAttribute('data-menu-key')) return;
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (id.length < 2) return;
      const t = $(id);
      if (!t) return;
      e.preventDefault();
      scrollToEl(t);
    });
  });

  /* ---------- sliders (Swiper) ---------- */
  const pad = (n) => String(n).padStart(2, '0');
  const a11yMsgs = () => root.dataset.lang === 'en'
    ? { prevSlideMessage: 'Previous', nextSlideMessage: 'Next', firstSlideMessage: 'First slide', lastSlideMessage: 'Last slide', slideLabelMessage: '{{index}} / {{slidesLength}}' }
    : { prevSlideMessage: 'Anterior', nextSlideMessage: 'Siguiente', firstSlideMessage: 'Primera imagen', lastSlideMessage: 'Última imagen', slideLabelMessage: '{{index}} / {{slidesLength}}' };
  const makeSlider = (el, opts, prefix) => {
    if (!el || !window.Swiper) return null;
    const total = el.querySelectorAll('.swiper-slide').length;
    const cur = $('[data-count-cur]', el), tot = $('[data-count-tot]', el);
    if (tot) tot.textContent = pad(total);
    const bar = $('[data-rooms-bar]', el);
    const sw = new Swiper(el, Object.assign({
      slidesPerView: 'auto', spaceBetween: 16, speed: 900, grabCursor: true,
      keyboard: { enabled: true, onlyInViewport: true },
      a11y: Object.assign({ enabled: true }, a11yMsgs()),
      navigation: { prevEl: $(`[data-${prefix}-prev]`, el), nextEl: $(`[data-${prefix}-next]`, el) },
      on: {
        slideChange(s) {
          if (cur) {
            const n = pad(s.realIndex + 1);
            if (window.gsap && !reduced) gsap.fromTo(cur, { yPercent: 60, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .5, ease: 'expo.out', onStart: () => { cur.textContent = n; } });
            else cur.textContent = n;
          }
          if (bar) bar.style.transform = `scaleX(${(s.realIndex + 1) / total})`;
        }
      }
    }, opts));
    if (bar) bar.style.transform = `scaleX(${1 / total})`;
    return sw;
  };
  /* Swiper se carga solo cuando los sliders se acercan a la pantalla */
  let swiperLoading = null;
  const loadSwiper = () => swiperLoading || (swiperLoading = new Promise((res, rej) => {
    if (window.Swiper) return res();
    const sc = document.createElement('script');
    sc.src = 'vendor/swiper-bundle.min.js'; sc.onload = res; sc.onerror = rej;
    document.head.appendChild(sc);
  }));
  const sliders = [];
  const lazySlider = (el, opts, prefix) => {
    if (!el) return;
    const init = () => {
      if (el.swiper || el.dataset.pending) return;
      if (!el.offsetParent) return; /* oculto por idioma: se inicia al cambiar */
      el.dataset.pending = '1';
      loadSwiper().then(() => { const sw = makeSlider(el, opts, prefix); if (sw) sliders.push(sw); }).catch(() => {}).finally(() => { delete el.dataset.pending; });
    };
    el._initSlider = init;
    if (!('IntersectionObserver' in window)) return init();
    const io = new IntersectionObserver((en) => { if (en[0].isIntersecting) { io.disconnect(); init(); } }, { rootMargin: '900px 0px' });
    io.observe(el);
  };
  lazySlider($('[data-rooms]'), { spaceBetween: 18 }, 'rooms');
  $$('[data-reviews]').forEach(el => lazySlider(el, { spaceBetween: 0, autoplay: reduced ? false : { delay: 6500, disableOnInteraction: true, pauseOnMouseEnter: true } }, 'reviews'));
  document.addEventListener('rilan:lang', () => {
    $$('[data-rooms], [data-reviews]').forEach(el => {
      if (!el.offsetParent) return;
      if (el.swiper) { Object.assign(el.swiper.params.a11y, a11yMsgs()); el.swiper.update(); }
      else if (el._initSlider && el.getBoundingClientRect().top < window.innerHeight * 3) el._initSlider();
    });
  });

  /* ---------- etiqueta "Arrastrar" que sigue al cursor ---------- */
  const drag = $('[data-drag]');
  if (drag && fine.matches && !reduced) {
    let dx = 0, dy = 0, tx = 0, ty = 0, raf = 0, shown = false;
    const loop = () => { dx += (tx - dx) * .2; dy += (ty - dy) * .2; drag.style.translate = `${dx}px ${dy}px`; raf = requestAnimationFrame(loop); };
    $$('[data-drag-label]').forEach(zone => {
      zone.addEventListener('pointerenter', (e) => {
        tx = dx = e.clientX; ty = dy = e.clientY; shown = true;
        drag.style.background = zone.closest('.hosts') ? 'var(--piedra)' : 'var(--niebla)';
        drag.style.color = zone.closest('.hosts') ? 'var(--niebla)' : 'var(--noche)';
        cancelAnimationFrame(raf); loop();
        window.gsap && gsap.to(drag, { scale: 1, opacity: 1, duration: .5, ease: 'expo.out' });
      });
      zone.addEventListener('pointermove', (e) => { tx = e.clientX; ty = e.clientY; });
      zone.addEventListener('pointerdown', () => shown && window.gsap && gsap.to(drag, { scale: .82, duration: .3, ease: 'expo.out' }));
      zone.addEventListener('pointerup', () => shown && window.gsap && gsap.to(drag, { scale: 1, duration: .4, ease: 'expo.out' }));
      zone.addEventListener('pointerleave', () => {
        shown = false;
        window.gsap && gsap.to(drag, { scale: 0, opacity: 0, duration: .4, ease: 'expo.out', onComplete: () => cancelAnimationFrame(raf) });
      });
      $$('button, a', zone).forEach(b => {
        b.addEventListener('pointerenter', () => window.gsap && gsap.to(drag, { scale: 0, opacity: 0, duration: .3 }));
        b.addEventListener('pointerleave', () => shown && window.gsap && gsap.to(drag, { scale: 1, opacity: 1, duration: .4, ease: 'expo.out' }));
      });
    });
  }

  /* ---------- botones magnéticos ---------- */
  if (fine.matches && !reduced) {
    $$('[data-magnetic]').forEach(btn => {
      const strength = 6;
      btn.addEventListener('pointermove', (e) => {
        const r = btn.getBoundingClientRect();
        const x = ((e.clientX - r.left) / r.width - .5) * 2 * strength;
        const y = ((e.clientY - r.top) / r.height - .5) * 2 * strength;
        window.gsap && gsap.to(btn, { x, y, duration: .45, ease: 'expo.out' });
      });
      btn.addEventListener('pointerleave', () => window.gsap && gsap.to(btn, { x: 0, y: 0, duration: .8, ease: 'elastic.out(1, .45)' }));
    });
  }

  /* ---------- sin movimiento: mostrar todo y salir ---------- */
  if (reduced || !window.gsap || !window.ScrollTrigger) {
    $('.loader')?.remove();
    clearTimeout(loaderSafety);
    $$('[data-clip]').forEach(f => f.classList.add('is-in'));
    $('[data-portal-window]')?.style.setProperty('clip-path', 'none');
    navTheme();
    return;
  }

  gsap.registerPlugin(ScrollTrigger);
  gsap.defaults({ ease: 'expo.out', duration: .9 });

  /* Lenis + ScrollTrigger en el mismo reloj */
  if (window.Lenis) {
    lenis = new Lenis({ lerp: .1, wheelMultiplier: 1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    lenis.stop();
  }

  /* ---------- división en líneas para revelados ---------- */
  const splitLines = (el) => {
    const targets = el.querySelectorAll(':scope > [data-l]').length ? $$(':scope > [data-l]', el) : [el];
    targets.forEach(t => {
      if (!t.dataset.raw) t.dataset.raw = t.innerHTML;
      t.innerHTML = t.dataset.raw;
      if (!t.offsetParent && getComputedStyle(t).display === 'none') return;
      const words = t.textContent.trim().split(/\s+/);
      t.innerHTML = words.map(w => `<span class="w">${w}</span>`).join(' ');
      const lines = []; let top = null;
      $$('.w', t).forEach(w => {
        const y = w.offsetTop;
        if (top === null || Math.abs(y - top) > 4) { lines.push([]); top = y; }
        lines[lines.length - 1].push(w.textContent);
      });
      const esc = (x) => x.replace(/&/g, '&amp;').replace(/</g, '&lt;');
      t.innerHTML = lines.map(l => `<span class="line"><span>${esc(l.join(' '))}</span></span>`).join('');
    });
  };
  const revealTweens = [];
  const buildReveals = (rebuild = false) => {
    revealTweens.forEach(t => { t.scrollTrigger && t.scrollTrigger.kill(); t.kill(); });
    revealTweens.length = 0;
    $$('[data-lines]').forEach(el => {
      splitLines(el);
      const inner = $$('.line > span', el).filter(s => s.offsetParent);
      if (!inner.length) return;
      if (rebuild && el.getBoundingClientRect().top < window.innerHeight * .88) return; /* ya visto: queda quieto */
      const tw = gsap.fromTo(inner, { yPercent: 105 }, {
        yPercent: 0, duration: 1.1, stagger: .07, ease: 'expo.out',
        scrollTrigger: { trigger: el, start: 'top 88%', once: true }
      });
      revealTweens.push(tw);
    });
  };

  /* ---------- precarga + entrada del hero ---------- */
  const loader = $('.loader');
  const heroImg = $('.hero__media img');
  const imgReady = new Promise(res => {
    if (!heroImg || heroImg.complete) return res();
    heroImg.addEventListener('load', res, { once: true });
    heroImg.addEventListener('error', res, { once: true });
    setTimeout(res, 2600);
  });
  const fontsReady = document.fonts
    ? Promise.race([
        Promise.all(['400 1em Marcellus', '300 1em Newsreader', 'italic 300 1em Newsreader', '400 1em Newsreader', 'italic 400 1em Newsreader', '500 1em Newsreader'].map(f => document.fonts.load(f))),
        new Promise(r => setTimeout(r, 2500))
      ]).then(() => document.fonts.ready)
    : Promise.resolve();

  gsap.set('.hero__letters span', { yPercent: 105 });
  gsap.set('[data-hero-fade]', { opacity: 0 });
  const markPath = $('.loader__mark path');
  const len = markPath.getTotalLength();
  gsap.set(markPath, { strokeDasharray: len, strokeDashoffset: len });
  const intro = gsap.timeline();
  intro.to(markPath, { strokeDashoffset: 0, duration: .95, ease: 'power2.inOut' })
       .to('.loader__mark', { fill: '#EAE9E3', duration: .5, ease: 'power1.out' }, '-=.25')
       .to('.loader__mark rect', { opacity: 1, duration: .3 }, '<')
       .fromTo('.loader__coords', { opacity: 0, letterSpacing: '.6em' }, { opacity: .8, letterSpacing: '.28em', duration: .9 }, '-=.7');

  Promise.all([imgReady, fontsReady, new Promise(r => intro.eventCallback('onComplete', r))]).then(() => {
    buildReveals();
    clearTimeout(loaderSafety);
    const tl = gsap.timeline({ onComplete: () => { loader.remove(); lenis && lenis.start(); } });
    tl.to(loader, { clipPath: 'inset(0 0 100% 0)', duration: 1.1, ease: 'power3.inOut' })
      .fromTo('[data-hero-media] img', { scale: 1.18 }, { scale: 1, duration: 2.2, ease: 'expo.out' }, '-=.75')
      .to('.hero__letters span', { yPercent: 0, duration: 1.3, stagger: .07, ease: 'expo.out' }, '-=1.9')
      .to('[data-hero-fade]', { opacity: 1, duration: 1.2, stagger: .1, ease: 'power2.out' }, '-=1');
    ScrollTrigger.refresh();
  });

  /* hero: al salir, la imagen se hunde y el título se separa */
  gsap.timeline({ scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } })
    .to('[data-hero-media]', { yPercent: 18, ease: 'none' }, 0)
    .to('.hero__content', { yPercent: -30, opacity: 0, ease: 'none' }, 0)
    .to('.hero__letters', { letterSpacing: '.3em', ease: 'none' }, 0);

  /* ---------- la ventana Λ (momento principal) ---------- */
  const portal = $('[data-portal]');
  if (portal) {
    const mm = gsap.matchMedia();
    mm.add({ d: '(min-width: 900px)', m: '(max-width: 899px)' }, (ctx) => {
      const start = ctx.conditions.d ? 'polygon(50% 26%, 50% 26%, 63% 76%, 37% 76%)' : 'polygon(50% 30%, 50% 30%, 68% 72%, 32% 72%)';
      const navEl = $('[data-nav]');
      const tl = gsap.timeline({ scrollTrigger: { trigger: portal, start: 'top top', end: 'bottom bottom', scrub: .6,
        /* mientras domina el fondo claro, el menú va oscuro */
        onUpdate: (self) => navEl.classList.toggle('on-light', self.progress < .42),
        onLeave: () => navEl.classList.remove('on-light'),
        onLeaveBack: () => navEl.classList.remove('on-light') } });
      tl.fromTo('[data-portal-window]', { clipPath: start }, { clipPath: 'polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)', ease: 'power2.inOut', duration: 1 }, 0)
        .to('[data-portal-dot]', { scale: 0, opacity: 0, ease: 'power2.in', duration: .25 }, 0)
        .to('[data-portal-intro]', { opacity: 0, x: -40, ease: 'power2.in', duration: .3 }, 0)
        .fromTo('.portal__video', { scale: ctx.conditions.d ? 1.25 : 1.15 }, { scale: 1, ease: 'none', duration: 1 }, 0)
        .to('[data-portal-shade]', { opacity: 1, duration: .3, ease: 'none' }, .75);
      const words = () => $$('[data-word]').filter(w => w.offsetParent);
      const wtl = gsap.timeline({ scrollTrigger: { trigger: portal, start: '62% bottom', end: 'bottom bottom', scrub: .4 } });
      wtl.to(words(), { opacity: 1, y: 0, filter: 'blur(0px)', stagger: .25, duration: .5, ease: 'power2.out' });
      document.addEventListener('rilan:lang', () => {
        gsap.set($$('[data-word]'), { clearProps: 'all' });
        wtl.clear(); wtl.to(words(), { opacity: 1, y: 0, filter: 'blur(0px)', stagger: .25, duration: .5, ease: 'power2.out' });
        ScrollTrigger.refresh();
      });
      return () => {};
    });
  }

  /* ---------- portadas de capítulo: la palabra respira ---------- */
  $$('[data-cover]').forEach(cover => {
    const media = $('[data-cover-media]', cover);
    const word = $('[data-cover-word]', cover);
    const mark = $('.mark', cover);
    gsap.fromTo(media, { yPercent: -6, scale: 1.12 }, { yPercent: 6, scale: 1, ease: 'none', scrollTrigger: { trigger: cover, start: 'top bottom', end: 'bottom top', scrub: true } });
    gsap.fromTo(word, { letterSpacing: '.5em', opacity: 0, filter: 'blur(10px)' }, { letterSpacing: '.12em', opacity: 1, filter: 'blur(0px)', ease: 'none', scrollTrigger: { trigger: cover, start: 'top 75%', end: 'center 55%', scrub: .5 } });
    gsap.fromTo(mark, { yPercent: 60, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 1.2, scrollTrigger: { trigger: cover, start: 'top 60%', once: true } });
  });

  /* ---------- imágenes que entran con cortina ---------- */
  $$('[data-clip]').forEach(fig => {
    const img = $('img', fig);
    gsap.timeline({ scrollTrigger: { trigger: fig, start: 'top 85%', once: true }, onComplete: () => { fig.classList.add('is-in'); gsap.set([fig, img], { clearProps: 'clipPath,transform' }); } })
      .fromTo(fig, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: 1.3, ease: 'expo.out' })
      .fromTo(img, { scale: 1.18 }, { scale: 1, duration: 1.8, ease: 'expo.out' }, 0);
  });
  /* parallax interno sutil (después de la entrada) */
  $$('[data-parallax-in]').forEach(img => {
    const frame = img.closest('.frame');
    gsap.fromTo(frame, { yPercent: -4 }, { yPercent: 4, ease: 'none', scrollTrigger: { trigger: frame, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  $$('[data-parallax-bg]').forEach(m => {
    gsap.fromTo(m, { yPercent: -8 }, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: m.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* ---------- galería horizontal (escritorio) ---------- */
  const hs = $('[data-hscroll]');
  if (hs) {
    const mm = gsap.matchMedia();
    mm.add('(min-width: 900px)', () => {
      /* Sin pin: la sección mide (recorrido + una pantalla) y su interior es sticky.
         Así no hay salto de layout al entrar ni al salir. */
      const track = $('[data-hscroll-track]', hs);
      const dist = () => Math.max(0, track.scrollWidth - window.innerWidth);
      const size = () => { hs.style.height = (dist() + window.innerHeight) + 'px'; };
      size();
      ScrollTrigger.addEventListener('refreshInit', size);
      const move = gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: hs, start: 'top top', end: 'bottom bottom', scrub: .8, invalidateOnRefresh: true } });
      $$('.hs .frame img', track).forEach(img => {
        gsap.fromTo(img, { xPercent: -7 }, { xPercent: 7, ease: 'none', scrollTrigger: { trigger: img.closest('.hs'), containerAnimation: move, start: 'left right', end: 'right left', scrub: true } });
      });
      $$('.hs', track).forEach(fig => {
        gsap.fromTo(fig, { clipPath: 'inset(0 0 0 100%)' }, { clipPath: 'inset(0 0 0 0%)', ease: 'expo.out', duration: 1.4, scrollTrigger: { trigger: fig, containerAnimation: move, start: 'left 92%', toggleActions: 'play none none none' } });
      });
      return () => { ScrollTrigger.removeEventListener('refreshInit', size); hs.style.height = ''; gsap.set(track, { clearProps: 'transform' }); };
    });
  }

  /* ---------- capas del silencio ---------- */
  const layers = () => $$('[data-layer]').filter(l => l.offsetParent);
  const layerTl = () => gsap.fromTo(layers(), { opacity: .12, x: -16 }, { opacity: 1, x: 0, stagger: .18, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: '.silence__layers', start: 'top 80%', once: true } });
  layerTl();
  document.addEventListener('rilan:lang', () => gsap.set($$('[data-layer]'), { opacity: 1, x: 0 }));

  /* ---------- masas de la cocina ---------- */
  const mmMass = gsap.matchMedia();
  mmMass.add('(min-width: 600px)', () => {
    $$('[data-mass] .mass__col').forEach(col => {
      const s = parseFloat(col.dataset.speed || 0);
      gsap.fromTo(col, { yPercent: -s }, { yPercent: s, ease: 'none', scrollTrigger: { trigger: '[data-mass]', start: 'top bottom', end: 'bottom top', scrub: .6 } });
    });
  });
  $$('[data-mass] figure').forEach((f, i) => {
    gsap.fromTo(f, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: 1.3, ease: 'expo.out', delay: (i % 3) * .08, scrollTrigger: { trigger: f, start: 'top 92%', once: true } });
  });

  /* ---------- cava: zoom lento ---------- */
  gsap.fromTo('[data-cava-media] img', { scale: 1.25 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: '.cava', start: 'top bottom', end: 'bottom top', scrub: true } });

  /* ---------- cinta de arquitectura ---------- */
  $$('[data-marquee]').forEach(row => {
    const dir = parseFloat(row.dataset.marquee) || -1;
    gsap.fromTo(row, { xPercent: dir < 0 ? 0 : -30 }, { xPercent: dir < 0 ? -30 : 0, ease: 'none', scrollTrigger: { trigger: row, start: 'top bottom', end: 'bottom top', scrub: .5 } });
  });

  /* ---------- palabra del pie ---------- */
  gsap.fromTo('[data-foot-word]', { yPercent: 40, letterSpacing: '.3em' }, { yPercent: 0, letterSpacing: '.1em', ease: 'none', scrollTrigger: { trigger: '.foot', start: 'top bottom', end: 'bottom bottom', scrub: .5 } });

  /* ---------- barra de progreso ---------- */
  gsap.to('[data-progress]', { scaleX: 1, ease: 'none', scrollTrigger: { start: 0, end: 'max', scrub: .3 } });

  /* ---------- navegación: se esconde al bajar, cambia de tono sobre fondos claros ---------- */
  navTheme();
  const nav = $('[data-nav]');
  ScrollTrigger.create({
    start: 'top -120',
    onUpdate: (self) => nav.classList.toggle('is-hidden', self.direction === 1 && !menuOpen)
  });

  function navTheme() {
    const nav = $('[data-nav]');
    if (!window.ScrollTrigger) return;
    $$('[data-theme="light"]').forEach(sec => {
      ScrollTrigger.create({ trigger: sec, start: 'top 40px', end: 'bottom 40px', onToggle: (s) => nav.classList.toggle('on-light', s.isActive) });
    });
  }

  /* ---------- re-división de líneas al cambiar idioma o tamaño ---------- */
  let rz, lastW = window.innerWidth;
  const rebuild = () => { buildReveals(true); ScrollTrigger.refresh(); };
  document.addEventListener('rilan:lang', () => {
    rebuild();
    $$('.line > span').forEach(s => { if (s.getBoundingClientRect().top < window.innerHeight) gsap.set(s, { yPercent: 0 }); });
  });
  window.addEventListener('resize', () => {
    if (Math.abs(window.innerWidth - lastW) < 2) return;
    lastW = window.innerWidth;
    clearTimeout(rz); rz = setTimeout(rebuild, 250);
  });
})();
