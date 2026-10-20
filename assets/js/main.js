/* Arielle Innou Coaching — site interactions. No dependencies. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Light header over photo heroes ---------- */
  if ($("main .retreat-hero")) doc.classList.add("hero-dark");

  /* ---------- Header: scrolled / hide on scroll down; sticky phone CTA ---------- */
  var header = $(".site-header");
  var sticky = $(".sticky-cta");
  var lastY = window.scrollY, ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (header) {
      header.classList.toggle("is-scrolled", y > 24);
      var hide = y > 520 && y > lastY + 4 && !document.body.classList.contains("menu-open");
      if (hide) { header.classList.add("is-hidden"); closeDrops(); }
      else if (y < lastY - 4 || y < 520) header.classList.remove("is-hidden");
    }
    if (sticky) {
      var nearBottom = window.innerHeight + y > document.body.scrollHeight - 640;
      sticky.classList.toggle("is-visible", y > window.innerHeight * 0.75 && !nearBottom);
    }
    lastY = y; ticking = false;
  }
  window.addEventListener("scroll", function () { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });

  /* ---------- Services dropdown (click / keyboard; hover handled in CSS) ---------- */
  var drops = $$(".nav__drop");
  function closeDrops(except) {
    drops.forEach(function (d) {
      if (d === except) return;
      d.classList.remove("is-open");
      var b = d.querySelector(".nav__drop-toggle"); if (b) b.setAttribute("aria-expanded", "false");
    });
  }
  drops.forEach(function (d) {
    var b = d.querySelector(".nav__drop-toggle");
    if (!b) return;
    b.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !d.classList.contains("is-open");
      closeDrops(d);
      d.classList.toggle("is-open", open);
      b.setAttribute("aria-expanded", String(open));
    });
    d.addEventListener("mouseleave", function () { if (d.classList.contains("is-open") && !d.contains(document.activeElement)) closeDrops(); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".nav__drop")) closeDrops(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeDrops(); });

  /* ---------- Mobile menu ---------- */
  var toggle = $(".menu-toggle"), menu = $("#mobile-menu");
  function setMenu(open) {
    document.body.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    var lab = toggle.querySelector(".menu-toggle__label"); if (lab) lab.textContent = open ? "Close" : "Menu";
    menu.setAttribute("aria-hidden", String(!open));
    if (open) { header.classList.remove("is-hidden"); var first = menu.querySelector("a"); if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 350); }
  }
  if (toggle && menu) {
    toggle.addEventListener("click", function () { setMenu(!document.body.classList.contains("menu-open")); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && document.body.classList.contains("menu-open")) { setMenu(false); toggle.focus(); } });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    window.addEventListener("resize", function () { if (window.innerWidth >= 1024 && document.body.classList.contains("menu-open")) setMenu(false); });
  }

  /* ---------- Split headlines into masked lines and words ---------- */
  var wordIndex = 0;
  function splitWords(node) {
    Array.prototype.slice.call(node.childNodes).forEach(function (child) {
      if (child.nodeType === 3) {
        var frag = document.createDocumentFragment();
        child.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(" ")); return; }
          var w = document.createElement("span"); w.className = "word";
          var inner = document.createElement("span"); inner.textContent = part; inner.style.setProperty("--i", wordIndex++);
          w.appendChild(inner); frag.appendChild(w);
        });
        child.parentNode.replaceChild(frag, child);
      } else if (child.nodeType === 1) splitWords(child);
    });
  }
  $$("[data-lines]").forEach(function (el) {
    wordIndex = 0;
    var parts = el.innerHTML.split(/<br\s*\/?>/i);
    el.innerHTML = parts.map(function (p) { return '<span class="line">' + p.trim() + "</span>"; }).join("");
    $$(".line", el).forEach(splitWords);
    el.classList.add("lines");
  });

  /* ---------- Reveal on scroll (starts once the intro screen has lifted) ---------- */
  function startReveals() {
    if (startReveals.done) return; startReveals.done = true;
    var els = $$(".reveal, .reveal-img, .lines");
    if (!("IntersectionObserver" in window) || reduceMotion) { els.forEach(function (el) { el.classList.add("is-in"); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    els.forEach(function (el) { io.observe(el); });
  }
  window.__startReveals = startReveals;
  if (doc.classList.contains("is-loading") || doc.classList.contains("is-entering")) {
    document.addEventListener("site:intro", startReveals, { once: true });
    setTimeout(startReveals, 4200);
  } else startReveals();
  onScroll();

  /* ---------- Roles get crossed out ("mother, wife, daughter…") ---------- */
  $$("[data-roles]").forEach(function (el) {
    if (!("IntersectionObserver" in window) || reduceMotion) { el.classList.add("is-struck"); return; }
    var o = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { setTimeout(function () { el.classList.add("is-struck"); }, 500); o.disconnect(); } }, { threshold: 0.8 });
    o.observe(el);
  });

  /* ---------- Testimonials slider ---------- */
  $$("[data-slider]").forEach(function (root) {
    var track = $(".t-track", root), slides = Array.prototype.slice.call(track.children);
    var dots = $$(".t-dot", root), host = root.closest("section") || root, idx = 0, timer;
    function go(i, user) {
      idx = (i + slides.length) % slides.length;
      track.scrollTo({ left: slides[idx].offsetLeft - track.offsetLeft, behavior: reduceMotion ? "auto" : "smooth" });
      mark(); if (user) restart();
    }
    function mark() { dots.forEach(function (d, n) { d.setAttribute("aria-current", n === idx ? "true" : "false"); }); }
    var st;
    track.addEventListener("scroll", function () {
      clearTimeout(st);
      st = setTimeout(function () { var i = Math.round(track.scrollLeft / track.clientWidth); if (i !== idx) { idx = i; mark(); } }, 80);
    }, { passive: true });
    dots.forEach(function (d, n) { d.addEventListener("click", function () { go(n, true); }); });
    var prev = $("[data-t-prev]", host), next = $("[data-t-next]", host);
    if (prev) prev.addEventListener("click", function () { go(idx - 1, true); });
    if (next) next.addEventListener("click", function () { go(idx + 1, true); });
    function restart() { clearInterval(timer); if (!reduceMotion) timer = setInterval(function () { if (!document.hidden && isNear(root)) go(idx + 1); }, 7000); }
    root.addEventListener("pointerenter", function () { clearInterval(timer); });
    root.addEventListener("pointerleave", restart);
    mark(); restart();
  });
  function isNear(el) { var r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < window.innerHeight; }

  /* ---------- Cost vs transformation switch ---------- */
  $$("[data-contrast]").forEach(function (root) {
    var panels = $(".contrast__panels", root), tabs = $$("[data-side]", root);
    function set(side) {
      root.setAttribute("data-side", side);
      panels.setAttribute("data-active", side);
      tabs.forEach(function (t) { t.setAttribute("aria-selected", String(t.getAttribute("data-side") === side)); });
    }
    tabs.forEach(function (t) { t.addEventListener("click", function () { set(t.getAttribute("data-side")); }); });
    // Show the cost first, then turn to the transformation as the section comes into view.
    set("cost");
    if ("IntersectionObserver" in window && !reduceMotion) {
      var o = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { setTimeout(function () { if (root.getAttribute("data-side") === "cost" && !root.dataset.touched) set("power"); }, 1800); o.disconnect(); } }, { threshold: 0.6 });
      o.observe(root);
      tabs.forEach(function (t) { t.addEventListener("click", function () { root.dataset.touched = "1"; }); });
    } else set("power");
  });

  /* ---------- Retreat gallery lightbox ---------- */
  var lb = $(".lightbox");
  var items = $$("[data-gallery] .gallery__item");
  if (lb && items.length) {
    var lbImg = $("img", lb), lbCap = $("figcaption", lb), cur = 0, lastFocus = null;
    function show(i) {
      cur = (i + items.length) % items.length;
      var it = items[cur], im = it.querySelector("img");
      lbImg.src = it.getAttribute("data-full"); lbImg.alt = im ? im.alt : "";
      lbCap.textContent = (im ? im.alt : "") + "  ·  " + (cur + 1) + " / " + items.length;
    }
    function open(i) { lastFocus = document.activeElement; show(i); lb.hidden = false; document.body.style.overflow = "hidden"; $(".lightbox__close", lb).focus(); }
    function close() { lb.hidden = true; document.body.style.overflow = ""; if (lastFocus) lastFocus.focus(); }
    items.forEach(function (it, i) { it.addEventListener("click", function () { open(i); }); });
    $(".lightbox__close", lb).addEventListener("click", close);
    $(".lightbox__nav--prev", lb).addEventListener("click", function () { show(cur - 1); });
    $(".lightbox__nav--next", lb).addEventListener("click", function () { show(cur + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(cur - 1);
      if (e.key === "ArrowRight") show(cur + 1);
    });
    var sx = null;
    lb.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) { if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); sx = null; });
  }

  /* ---------- Contact form ---------- */
  $$("[data-form]").forEach(function (form) {
    var success = $(".form-success", form), error = $(".form-error", form);
    function check(field) {
      var input = field.querySelector("input, textarea");
      if (!input || !input.required) return true;
      var ok = input.type === "email" ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim()) : input.value.trim().length > 0;
      field.classList.toggle("is-invalid", !ok);
      return ok;
    }
    $$(".field", form).forEach(function (f) {
      var input = f.querySelector("input, textarea");
      if (input) input.addEventListener("blur", function () { if (input.value) check(f); });
      if (input) input.addEventListener("input", function () { if (f.classList.contains("is-invalid")) check(f); });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = $$(".field", form).map(check).every(Boolean);
      if (!ok) { var bad = $(".is-invalid input, .is-invalid textarea", form); if (bad) bad.focus(); return; }
      if (error) error.hidden = true;
      var done = function () { form.classList.add("is-sent"); if (success) { success.hidden = false; success.setAttribute("tabindex", "-1"); success.focus(); } };
      // Demo mode until a Formspree form ID is added (see README).
      if (/YOUR_FORM_ID/.test(form.action)) { form.classList.add("is-busy"); setTimeout(function () { form.classList.remove("is-busy"); done(); }, 700); return; }
      form.classList.add("is-busy");
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error(r.status); done(); })
        .catch(function () { if (error) error.hidden = false; })
        .then(function () { form.classList.remove("is-busy"); });
    });
  });

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
