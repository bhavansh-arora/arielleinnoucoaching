/* Arielle Innou Coaching — motion layer.
   GSAP + ScrollTrigger drive the scroll effects. Every effect degrades gracefully:
   if a library fails to load, or motion is reduced, content simply stays visible. */
(function () {
  "use strict";
  var html = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var gsap = window.gsap, ST = window.ScrollTrigger;
  var hasGsap = !!(gsap && ST) && !reduce;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  function intro() {
    if (intro.done) return; intro.done = true;
    document.dispatchEvent(new CustomEvent("site:intro"));
    if (window.__startReveals) window.__startReveals();
    if (hasGsap) ST.refresh();
  }
  function finishLoading() {
    html.classList.remove("is-loading");
    try { sessionStorage.setItem("ai-seen", "1"); } catch (e) {}
  }
  if (reduce) { finishLoading(); html.classList.remove("is-entering"); intro(); return; }
  if (hasGsap) { gsap.registerPlugin(ST); html.classList.add("has-gsap"); }

  /* ---------- Scroll progress ---------- */
  var bar = $(".scroll-progress");
  function progress() {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.setProperty("--sp", max > 0 ? (window.scrollY / max).toFixed(4) : 0);
  }
  window.addEventListener("scroll", progress, { passive: true });
  progress();

  /* ---------- Intro screen (first visit) / curtain (between pages) ---------- */
  if (html.classList.contains("is-loading")) {
    var lbar = $(".preloader__bar");
    var heroImg = $("main img");
    var loaded = !heroImg || heroImg.complete;
    if (heroImg && !loaded) { heroImg.addEventListener("load", function () { loaded = true; }); heroImg.addEventListener("error", function () { loaded = true; }); }
    var fontsReady = false;
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () { fontsReady = true; });
    var t0 = performance.now(), shown = 0, MIN = 2000, MAX = 3600;
    (function tick(now) {
      var elapsed = now - t0, ready = (loaded && fontsReady) || elapsed > MAX;
      var target = ready ? 100 : Math.min(88, (elapsed / MIN) * 88);
      shown += (Math.min(target, (elapsed / MIN) * 100) - shown) * 0.1;
      if (ready && elapsed >= MIN && shown > 99.3) shown = 100;
      if (lbar) lbar.style.setProperty("--p", (shown / 100).toFixed(3));
      if (shown < 100) { requestAnimationFrame(tick); return; }
      html.classList.add("is-loaded");
      finishLoading();
      setTimeout(intro, 350);
      setTimeout(function () { html.classList.remove("is-loaded"); }, 1400);
    })(t0);
  } else if (html.classList.contains("is-entering")) {
    // Hold the composed brand for a beat, then lift the curtain.
    try { sessionStorage.removeItem("ai-nav-title"); } catch (e) {}
    setTimeout(function () {
      html.classList.add("is-entered");
      setTimeout(intro, 380);
      setTimeout(function () { html.classList.remove("is-entering", "is-entered"); }, 1500);
    }, 280);
  } else intro();

  // The name shown on the curtain: the page's name from the menu, else the link's own words.
  function pageTitle(a, url) {
    var file = url.pathname.split("/").pop() || "index.html";
    if (!/\.html$/.test(file)) file += ".html";
    if (file === "index.html") return "Home";
    var m = document.querySelector('.mobile-menu__list a[href="' + file + '"] span');
    if (m && m.textContent.trim()) return m.textContent.trim();
    var t = (a.querySelector(".btn__text") || a).textContent.replace(/\s+/g, " ").trim();
    return t && t.length < 40 ? t : "Coaching";
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[href]");
    if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (a.target === "_blank" || a.hasAttribute("download")) return;
    var url = new URL(a.getAttribute("href"), location.href);
    if (url.origin !== location.origin || !/(\.html|\/|\/[^.\/]+)$/.test(url.pathname)) return;
    if (url.pathname === location.pathname) return;
    e.preventDefault();
    var title = pageTitle(a, url), slot = $("[data-curtain-title]");
    if (slot) slot.textContent = title;
    try { sessionStorage.setItem("ai-nav", "1"); sessionStorage.setItem("ai-nav-title", title); } catch (err) {}
    html.classList.add("is-leaving");
    setTimeout(function () { location.href = url.href; }, 900);
  });
  window.addEventListener("pageshow", function (e) { if (e.persisted) html.classList.remove("is-leaving", "is-entering", "is-entered"); });

  /* ---------- Count-up numbers ---------- */
  var counters = $$("[data-count]");
  if ("IntersectionObserver" in window && counters.length) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        var el = en.target, end = parseFloat(el.dataset.count), s = performance.now();
        (function step(now) {
          var p = Math.min(1, (now - s) / 1900);
          el.textContent = Math.round(end * (p === 1 ? 1 : 1 - Math.pow(2, -10 * p)));
          if (p < 1) requestAnimationFrame(step);
        })(s);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { c.textContent = "0"; cio.observe(c); });
  }

  /* ---------- Marquee that speeds up with scroll ---------- */
  var lastY = window.scrollY, velocity = 0, direction = 1;
  (function sample() {
    var y = window.scrollY, d = y - lastY;
    velocity += (d - velocity) * 0.2;
    if (Math.abs(d) > 0.5) direction = d > 0 ? 1 : -1;
    lastY = y;
    requestAnimationFrame(sample);
  })();
  if (hasGsap) $$(".marquee__track").forEach(function (track) {
    var x = 0;
    (function loop() {
      x -= (0.5 + Math.min(Math.abs(velocity) * 0.22, 12)) * direction;
      var half = track.scrollWidth / 2;
      if (x <= -half) x += half;
      if (x > 0) x -= half;
      track.style.transform = "translate3d(" + x.toFixed(2) + "px,0,0)";
      requestAnimationFrame(loop);
    })();
  });

  /* ---------- Cursor and magnetic buttons (mouse/trackpad only) ---------- */
  if (fine) {
    html.classList.add("has-cursor");
    var cursor = $(".cursor"), ring = $(".cursor__ring"), dot = $(".cursor__dot"), label = $(".cursor__label");
    var mx = innerWidth / 2, my = innerHeight / 2, rx = mx, ry = my;
    window.addEventListener("mousemove", function (e) {
      mx = e.clientX; my = e.clientY;
      if (!cursor.classList.contains("is-ready")) { rx = mx; ry = my; cursor.classList.add("is-ready"); }
      cursor.classList.remove("is-hidden");
    }, { passive: true });
    document.addEventListener("mouseleave", function () { cursor.classList.add("is-hidden"); });
    (function follow() {
      rx += (mx - rx) * 0.2; ry += (my - ry) * 0.2;
      dot.style.transform = "translate3d(" + mx + "px," + my + "px,0)";
      ring.style.transform = "translate3d(" + rx + "px," + ry + "px,0)";
      requestAnimationFrame(follow);
    })();
    document.addEventListener("mouseover", function (e) {
      var lab = e.target.closest("[data-cursor]");
      var hov = e.target.closest("a, button, summary, label, input, textarea");
      if (lab) { label.textContent = lab.dataset.cursor; cursor.classList.add("is-label"); cursor.classList.remove("is-hover"); }
      else if (hov) { cursor.classList.add("is-hover"); cursor.classList.remove("is-label"); }
      else cursor.classList.remove("is-hover", "is-label");
    });
    if (hasGsap) {
      $$(".btn, .t-arrow, .badge, .footer-cta__btn, .menu-toggle").forEach(function (el) {
        var k = el.classList.contains("btn") ? 0.22 : 0.38;
        el.addEventListener("mousemove", function (e) {
          var r = el.getBoundingClientRect();
          gsap.to(el, { x: (e.clientX - (r.left + r.width / 2)) * k, y: (e.clientY - (r.top + r.height / 2)) * k, duration: 0.6, ease: "power3.out" });
        });
        el.addEventListener("mouseleave", function () { gsap.to(el, { x: 0, y: 0, duration: 1, ease: "elastic.out(1, 0.35)" }); });
      });
    }
  }

  if (!hasGsap) return;

  /* ====================== Scroll choreography ====================== */
  var mm = gsap.matchMedia();

  // Home hero: portrait drifts, the big lotus turns slowly, the note floats.
  $$(".hero").forEach(function (hero) {
    var trig = { trigger: hero, start: "top top", end: "bottom top", scrub: true };
    var photo = $(".hero__photo", hero), lotus = $(".hero__lotus", hero), note = $(".hero__note", hero), badge = $(".badge", hero);
    if (photo) gsap.to(photo, { yPercent: 10, ease: "none", scrollTrigger: trig });
    if (lotus) gsap.to(lotus, { rotate: 14, yPercent: 12, ease: "none", scrollTrigger: trig });
    if (note) gsap.to(note, { yPercent: -40, ease: "none", scrollTrigger: trig });
    if (badge) gsap.to(badge, { yPercent: -60, ease: "none", scrollTrigger: trig });
  });

  // Photo hero (retreats): slow zoom-out parallax.
  $$("[data-parallax-hero]").forEach(function (m) {
    gsap.fromTo(m, { scale: 1.12 }, { scale: 1, duration: 2.4, ease: "expo.out" });
    gsap.to(m, { yPercent: 14, ease: "none", scrollTrigger: { trigger: m.parentElement, start: "top top", end: "bottom top", scrub: true } });
  });

  // Gentle parallax inside framed photos (anchored on faces).
  $$(".media").forEach(function (m) {
    if (m.closest(".hero, .story, .step-card, .question__float, .cta-panel, .svc-card, .who-card, .program, .gallery")) return;
    var im = m.querySelector("img");
    if (!im) return;
    im.style.transformOrigin = getComputedStyle(im).objectPosition;
    gsap.fromTo(im, { yPercent: -5, scale: 1.12 }, { yPercent: 5, scale: 1.12, ease: "none", scrollTrigger: { trigger: m, start: "top bottom", end: "bottom top", scrub: true } });
  });
  $$(".cta-panel__media img").forEach(function (im) {
    gsap.fromTo(im, { yPercent: -8, scale: 1.18 }, { yPercent: 8, scale: 1.18, ease: "none", scrollTrigger: { trigger: im.closest(".cta-panel"), start: "top bottom", end: "bottom top", scrub: true } });
  });

  // Floating arches beside "Who am I now?"
  $$(".question__float").forEach(function (f, i) {
    gsap.fromTo(f, { y: i ? 80 : -40 }, { y: i ? -120 : 120, ease: "none", scrollTrigger: { trigger: f.parentElement, start: "top bottom", end: "bottom top", scrub: true } });
  });

  // Text that lights up word by word as you read.
  $$("[data-scrub-words]").forEach(function (el) {
    (function wrap(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (c) {
        if (c.nodeType === 3) {
          var f = document.createDocumentFragment();
          c.textContent.split(/(\s+)/).forEach(function (w) {
            if (!w) return;
            if (/^\s+$/.test(w)) { f.appendChild(document.createTextNode(" ")); return; }
            var s = document.createElement("span"); s.className = "sw"; s.textContent = w; f.appendChild(s);
          });
          c.parentNode.replaceChild(f, c);
        } else if (c.nodeType === 1 && !c.classList.contains("inline-img")) wrap(c);
      });
    })(el);
    gsap.to($$(".sw, .inline-img", el), { opacity: 1, stagger: 0.1, ease: "none", scrollTrigger: { trigger: el, start: "top 85%", end: "bottom 45%", scrub: 0.6 } });
  });

  // Big outlined lotuses draw themselves as they arrive.
  $$(".principle__lotus, .notfound__lotus").forEach(function (l) {
    var paths = $$("path", l);
    gsap.set(paths, { strokeDasharray: 1, strokeDashoffset: 1 });
    gsap.to(paths, { strokeDashoffset: 0, duration: 1.8, ease: "power2.inOut", stagger: 0.12, scrollTrigger: { trigger: l, start: "top 85%" } });
  });

  // Corporate: the "High turnover. Low engagement." rows drift in opposite directions.
  $$("[data-drift]").forEach(function (row) {
    var dir = parseFloat(row.getAttribute("data-drift"));
    gsap.fromTo(row, { xPercent: dir > 0 ? -18 : 0 }, { xPercent: dir > 0 ? 0 : -18, ease: "none", scrollTrigger: { trigger: row.parentElement, start: "top bottom", end: "bottom top", scrub: true } });
  });

  // About: pinned, sideways story chapters on desktop.
  mm.add("(min-width: 1024px)", function () {
    var section = $("[data-hscroll]");
    if (!section) return;
    var track = $(".story__track", section), prog = $(".story__progress", section);
    section.classList.add("is-pinned");
    var dist = function () { return Math.max(0, track.scrollWidth - window.innerWidth); };
    gsap.to(track, {
      x: function () { return -dist(); }, ease: "none",
      scrollTrigger: { trigger: section, start: "top top", end: function () { return "+=" + dist(); }, pin: true, scrub: 0.8, invalidateOnRefresh: true, anticipatePin: 1,
        onUpdate: function (self) { if (prog) prog.style.setProperty("--hp", self.progress.toFixed(4)); } }
    });
    return function () { section.classList.remove("is-pinned"); gsap.set(track, { x: 0 }); };
  });

  // Steps stack: each covered card eases back and dims.
  mm.add("(min-width: 900px)", function () {
    var cards = $$("[data-stack] .step-card");
    cards.forEach(function (card, i) {
      var next = cards[i + 1];
      if (!next) return;
      var st = { trigger: next, start: "top bottom", end: "top " + (108 + (i + 1) * 28) + "px", scrub: true };
      gsap.to(card, { scale: 0.94, ease: "none", scrollTrigger: st });
      gsap.to(card.querySelector(".step-card__shade"), { opacity: 0.35, ease: "none", scrollTrigger: st });
    });
    // Headings drift a touch for depth.
    $$(".head--split .h-xl, .page-hero__title").forEach(function (h) {
      gsap.fromTo(h, { y: 16 }, { y: -16, ease: "none", scrollTrigger: { trigger: h, start: "top bottom", end: "bottom top", scrub: true } });
    });
  });

  // Footer: letters of the closing line rise into place.
  var wm = $(".footer-wordmark");
  if (wm) {
    wm.innerHTML = wm.textContent.split("").map(function (ch) { return ch === " " ? " " : '<span class="fw-char">' + ch + "</span>"; }).join("");
    gsap.from($$(".fw-char", wm), { yPercent: 110, opacity: 0, duration: 1.2, ease: "expo.out", stagger: 0.025, scrollTrigger: { trigger: wm, start: "top 98%" } });
  }

  window.addEventListener("load", function () { ST.refresh(); });
  if (document.fonts) document.fonts.ready.then(function () { ST.refresh(); });
})();
