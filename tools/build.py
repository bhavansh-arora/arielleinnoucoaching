#!/usr/bin/env python3
"""
Static site generator for Arielle Innou Coaching.

Layout lives here; copy and lists live in tools/content.py. Run
`python3 tools/build.py` to regenerate every page. The output is plain HTML in the
repository root with no runtime dependencies. Pages saved from the visual editor
(/admin) are the source of truth and are skipped unless you pass --force.
"""
import json
import sys
from html import escape
from pathlib import Path

from content import *  # noqa: F401,F403  (copy and lists)

ROOT = Path(__file__).resolve().parent.parent
EDITED_MARK = "<!-- editor:edited -->"
FORCE = "--force" in sys.argv
META = json.loads((Path(__file__).parent / "image-meta.json").read_text())

# --------------------------------------------------------------------------- #
# Icons
# --------------------------------------------------------------------------- #
def svg(paths, cls="", sw="1.6", fill="none"):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="{fill}" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'


ARROW = svg('<path d="M5 12h14M13 6l6 6-6 6"/>')
ARROW_UR = svg('<path d="M7 17L17 7M8 7h9v9"/>')
CHEV = svg('<path d="M6 9l6 6 6-6"/>', "chev")
PREV = svg('<path d="M15 6l-6 6 6 6"/>')
NEXT = svg('<path d="M9 6l6 6-6 6"/>')
CLOSE = svg('<path d="M6 6l12 12M18 6L6 18"/>')
CHECK = svg('<path d="M5 12.5l4.5 4.5L19 7.5"/>', sw="1.8")
CROSS = svg('<path d="M7 7l10 10M17 7L7 17"/>', sw="1.8")
MAIL = svg('<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M4 7l8 6 8-6"/>')
PIN = svg('<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>')
IG = svg('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r=".9" fill="currentColor" stroke="none"/>', sw="1.5")
QUOTE = '<svg class="qmark" viewBox="0 0 40 28" fill="currentColor" aria-hidden="true"><path d="M0 28V17.2C0 7.6 4.6 1.9 13.8 0l1.6 3.3C10.3 5 7.8 8.3 7.5 13.2H15V28H0zm22.6 0V17.2C22.6 7.6 27.2 1.9 36.4 0L38 3.3c-5.1 1.7-7.6 5-7.9 9.9h7.5V28h-15z"/></svg>'

FEATURE_ICONS = {
    "video": '<rect x="3" y="6" width="13" height="12" rx="3"/><path d="M16 10.5l5-3v9l-5-3"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "hand": '<path d="M7 11V6.5a1.5 1.5 0 0 1 3 0V11M10 10V4.5a1.5 1.5 0 0 1 3 0V10M13 10V5.5a1.5 1.5 0 0 1 3 0V12M16 9.5a1.5 1.5 0 0 1 3 0V14a7 7 0 0 1-7 7h-1a6 6 0 0 1-5-2.7L3.6 15a1.6 1.6 0 0 1 2.6-1.8L7 14.5"/>',
    "leaf": '<path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15"/><path d="M5 19c3-4 6-6.5 10-8.5"/>',
    "door": '<path d="M5 21V4.5A1.5 1.5 0 0 1 6.5 3h8A1.5 1.5 0 0 1 16 4.5V21M3 21h18"/><path d="M13 12h.01M16 7h3.5a.5.5 0 0 1 .5.5V21"/>',
    "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 16l.7 1.8 1.8.7-1.8.7L19 21l-.7-1.8-1.8-.7 1.8-.7z"/>',
    "heart": '<path d="M12 20s-7.5-4.6-7.5-10A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 7.5 3c0 5.4-7.5 10-7.5 10z"/>',
    "bowl": '<path d="M3 12h18a9 9 0 0 1-18 0z"/><path d="M8 8c0-1.5 1-2 1-3.5M12 8c0-1.5 1-2 1-3.5M16 8c0-1.5 1-2 1-3.5"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    "lotus": '<path d="M12 20c-2.8-2.5-3.6-6.7-.1-11.5 3.6 4.8 2.9 9 .1 11.5z"/><path d="M11.4 19.6C8 19 4.7 16.4 4.6 12c3.3.3 5.8 2.3 6.8 4.7M12.6 19.6C16 19 19.3 16.4 19.4 12c-3.3.3-5.8 2.3-6.8 4.7"/><path d="M10.6 20c-3 .6-6.3-.6-8.1-3.3M13.4 20c3 .6 6.3-.6 8.1-3.3"/>',
}


def ficon(name):
    return f'<span class="ficon">{svg(FEATURE_ICONS[name], sw="1.4")}</span>'


# The lotus from Arielle's logo (same petals as tools/images.py), drawn back to front.
LOTUS_PATHS = [
    "M30 36C18 38 6 32 1 22C14 19 25 24 30 36Z",
    "M34 36C46 38 58 32 63 22C50 19 39 24 34 36Z",
    "M31 35C19 32 13 21 15 8C26 12 31.5 22 31 35Z",
    "M33 35C45 32 51 21 49 8C38 12 32.5 22 33 35Z",
    "M32 35C23 26 24 12 32 2C40 12 41 26 32 35Z",
]


def lotus(cls="lotus", draw=False):
    extra = ' pathLength="1"' if draw else ""
    paths = "".join(f'<path d="{d}"{extra}/>' for d in LOTUS_PATHS)
    cls = "lotus" if cls == "lotus" else f"lotus {cls}"
    return f'<svg class="{cls}" viewBox="0 0 64 40" aria-hidden="true">{paths}</svg>'


# --------------------------------------------------------------------------- #
# Image helpers
# --------------------------------------------------------------------------- #
def focus(name):
    m = META[name]
    return f'{m["fx"]}% {m["fy"]}%'


def img(name, alt, sizes="100vw", lazy=True, priority=False):
    m = META[name]
    w = min(1600, m["w"])
    h = round(m["h"] * w / m["w"])
    srcset = (f"assets/img/{name}-800.webp 800w, assets/img/{name}-1600.webp {w}w" if m["w"] > 800
              else f"assets/img/{name}-1600.webp {w}w")
    load = 'loading="lazy" decoding="async"' if lazy else 'decoding="async"'
    if priority:
        load += ' fetchpriority="high"'
    role = ' role="presentation"' if not alt else ""  # decorative photos
    return (f'<img src="assets/img/{name}-1600.webp" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" '
            f'alt="{alt}"{role} {load} style="object-position:{focus(name)}">')


def media(name, alt, cls="", sizes="100vw", lazy=True, priority=False, reveal=True):
    c = " ".join(x for x in ["media", cls, "reveal-img" if reveal else ""] if x)
    return f'<div class="{c}" style="background-color:{META[name]["c"]}">{img(name, alt, sizes, lazy, priority)}</div>'


def bg(name):
    return f"background-image:url(assets/img/{name}-800.webp);background-position:{focus(name)}" if META[name]["w"] > 800 \
        else f"background-image:url(assets/img/{name}-1600.webp);background-position:{focus(name)}"


# --------------------------------------------------------------------------- #
# Small building blocks
# --------------------------------------------------------------------------- #
def btn(text, href, kind="primary", icon=True, ext=False, extra=""):
    target = ' target="_blank" rel="noopener"' if ext else ""
    ic = f'<span class="btn__icon">{ARROW_UR if ext else ARROW}</span>' if icon else ""
    return f'<a class="btn btn--{kind}{(" " + extra) if extra else ""}" href="{href}"{target}><span class="btn__text">{text}</span>{ic}</a>'


def link(text, href, ext=False):
    target = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="link" href="{href}"{target}>{text} {ARROW_UR if ext else ARROW}</a>'


def label(text, dot=False, cls=""):
    return f'<span class="label{" label--dot" if dot else ""}{(" " + cls) if cls else ""}">{text}</span>'


def head(kicker, title, lede="", center=False, cls=""):
    lede_html = f'<p class="lede reveal">{lede}</p>' if lede else ""
    c = "head" + (" head--center" if center else "") + (" head--split" if lede and not center else "") + (f" {cls}" if cls else "")
    return f"""
    <div class="{c}">
      <div class="head__title">{label(kicker, dot=True)}
      <h2 class="h-xl" data-lines>{title}</h2></div>
      {lede_html}
    </div>"""


def checklist(items, kind="check"):
    ic = CHECK if kind == "check" else CROSS
    return f'<ul class="ticks ticks--{kind}">' + "".join(f'<li><span class="ticks__ic">{ic}</span><span>{i}</span></li>' for i in items) + "</ul>"


def marquee(words, cls=""):
    row = "".join(f"<span>{w}</span>{lotus('marquee__mark')}" for w in words)
    return f'<div class="marquee {cls}" aria-hidden="true"><div class="marquee__track">{row}{row}</div></div>'


def steps_section(steps, kicker, title, lede):
    cards = ""
    for i, (t, d, image) in enumerate(steps):
        cards += f"""
        <article class="step-card" style="--i:{i}">
          <div class="step-card__text">
            <div class="step-card__top"><span class="step-card__num">0{i + 1}</span><span class="label">Step {i + 1} of {len(steps)}</span></div>
            <div><h3 class="h-lg">{t}</h3><p class="body mt-s">{d}</p></div>
            {btn(CTA, "contact.html") if i == 0 else ""}
          </div>
          {media(image, "", "step-card__media", "(min-width: 900px) 45vw, 100vw", reveal=False)}
          <span class="step-card__shade" aria-hidden="true"></span>
        </article>"""
    return f"""
<section class="section section--sand" id="process">
  <div class="container">
    {head(kicker, title, lede)}
    <div class="steps" data-stack>{cards}
    </div>
  </div>
</section>"""


def testimonials_section(kicker="Kind words", title="What clients <em>say.</em>", dark=False):
    slides = ""
    for i, (name, q, prog) in enumerate(TESTIMONIALS):
        slides += f"""
        <figure class="t-slide" aria-roledescription="slide" aria-label="{i + 1} of {len(TESTIMONIALS)}">
          <blockquote><p>“{q}”</p></blockquote>
          <figcaption><span class="t-avatar" aria-hidden="true">{name[0]}</span><span><strong>{name}</strong><small>{prog}</small></span></figcaption>
        </figure>"""
    dots = "".join(f'<button class="t-dot" type="button" aria-label="Show testimonial {i + 1}"></button>' for i in range(len(TESTIMONIALS)))
    return f"""
<section class="section testimonials{' section--night' if dark else ''}">
  <div class="container">
    <div class="testimonials__grid">
      <div class="testimonials__aside">
        {label(kicker, dot=True)}
        <h2 class="h-xl" data-lines>{title}</h2>
        <div class="t-controls">
          <button class="t-arrow" type="button" data-t-prev aria-label="Previous testimonial">{PREV}</button>
          <button class="t-arrow" type="button" data-t-next aria-label="Next testimonial">{NEXT}</button>
        </div>
      </div>
      <div class="t-slider" data-slider aria-roledescription="carousel" aria-label="Client testimonials">
        {QUOTE}
        <div class="t-track">{slides}
        </div>
        <div class="t-dots">{dots}</div>
      </div>
    </div>
  </div>
</section>"""


def contrast(cost_label, cost_items, power_label, power_items, tab_cost, tab_power, footnote=""):
    note = f'<p class="contrast__note reveal">{footnote}</p>' if footnote else ""
    return f"""
    <div class="contrast" data-contrast>
      <div class="contrast__switch" role="tablist" aria-label="Compare">
        <button type="button" role="tab" aria-selected="false" data-side="cost">{tab_cost}</button>
        <button type="button" role="tab" aria-selected="true" data-side="power">{tab_power}</button>
        <span class="contrast__pill" aria-hidden="true"></span>
      </div>
      <div class="contrast__panels" data-active="power">
        <div class="contrast__panel contrast__panel--cost" role="tabpanel" data-panel="cost">
          <span class="contrast__tag">{tab_cost}</span>
          <h3 class="h-md">{cost_label}</h3>
          {checklist(cost_items, "cross")}
        </div>
        <div class="contrast__panel contrast__panel--power" role="tabpanel" data-panel="power">
          <span class="contrast__tag">{tab_power}</span>
          <h3 class="h-md">{power_label}</h3>
          {checklist(power_items, "check")}
          {lotus("contrast__lotus")}
        </div>
      </div>
      {note}
    </div>"""


def statement(text, kicker=None, cls=""):
    k = f'<div class="statement__kicker">{label(kicker, dot=True)}</div>' if kicker else ""
    return f"""
<section class="section section--tight {cls}">
  <div class="container">{k}
    <p class="statement" data-scrub-words>{text}</p>
  </div>
</section>"""


def inline_img(name):
    return f'<span class="inline-img" style="{bg(name)}" aria-hidden="true"></span>'


def page_hero(kicker, title, lede, image, alt, actions="", cls="", shape="arch", aside=""):
    return f"""
<section class="page-hero {cls}">
  <div class="container page-hero__grid">
    <div class="page-hero__copy">
      {label(kicker, dot=True, cls="reveal")}
      <h1 class="display page-hero__title" data-lines>{title}</h1>
      <p class="lede reveal">{lede}</p>
      <div class="actions reveal">{actions}</div>
    </div>
    <div class="page-hero__visual">
      {media(image, alt, shape, "(min-width: 900px) 42vw, 92vw", lazy=False, priority=True)}
      {aside}
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------- #
# Shared chrome
# --------------------------------------------------------------------------- #
COACHING = [
    ("life-relationship-coaching.html", "Life & Relationship", "1:1 coaching for women in transition", "new-chapter"),
    ("corporate-coaching.html", "Corporate Coaching", "Healthier, high-performing teams", "leaders"),
    ("retreats.html", "Retreats", "Restorative stays in the Ontario countryside", "sisterhood"),
]
MOBILE_NAV = [
    ("index.html", "Home"), ("about.html", "About"),
    ("life-relationship-coaching.html", "Life &amp; Relationship"), ("corporate-coaching.html", "Corporate"),
    ("retreats.html", "Retreats"), ("contact.html", "Contact"),
]


def cur(h, active):
    return ' aria-current="page"' if h == active else ""


def header(active):
    drop = "".join(
        f'<li><a class="dropdown__item" href="{h}"{cur(h, active)}><span class="dropdown__img" style="{bg(im)}"></span>'
        f'<span class="dropdown__text"><strong>{t}</strong><small>{d}</small></span></a></li>'
        for h, t, d, im in COACHING)
    mobile = "".join(
        f'<li><a href="{h}"{cur(h, active)}><small>0{i + 1}</small><span>{t}</span></a></li>'
        for i, (h, t) in enumerate(MOBILE_NAV))
    return f"""
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="site-header__inner">
    <a class="brand" href="index.html" aria-label="Arielle Innou Coaching, home">{lotus("brand__mark")}<span class="brand__name">Arielle Innou<em>Coaching</em></span></a>
    <nav class="nav" aria-label="Primary">
      <ul class="nav__list">
        <li><a class="nav__link" href="about.html"{cur("about.html", active)}>About</a></li>
        <li class="nav__drop">
          <button class="nav__link nav__drop-toggle" type="button" aria-expanded="false" aria-controls="nav-services">Services {CHEV}</button>
          <div class="dropdown" id="nav-services"><ul class="dropdown__list">{drop}</ul>
            <a class="dropdown__cta" href="contact.html"><span>Not sure where to start? <strong>Book a free 30-minute call</strong></span>{ARROW}</a>
          </div>
        </li>
        <li><a class="nav__link" href="retreats.html"{cur("retreats.html", active)}>Retreats</a></li>
        <li><a class="nav__link" href="contact.html"{cur("contact.html", active)}>Contact</a></li>
      </ul>
    </nav>
    <a class="btn btn--primary btn--sm header-cta" href="contact.html"><span class="btn__text">Book a call</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu">
      <span class="menu-toggle__label">Menu</span><span class="menu-toggle__bars" aria-hidden="true"><span></span><span></span></span>
    </button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
  {lotus("mobile-menu__lotus")}
  <nav aria-label="Mobile"><ul class="mobile-menu__list">{mobile}</ul></nav>
  <div class="mobile-menu__foot">
    <a class="btn btn--light btn--block" href="contact.html"><span class="btn__text">{CTA}</span><span class="btn__icon">{ARROW}</span></a>
    <p class="mobile-menu__meta"><a href="mailto:{EMAIL}">{EMAIL}</a><span>{LOCATION}</span></p>
  </div>
</div>"""


def footer():
    return f"""
<footer class="site-footer">
  <div class="footer-card">
    {lotus("footer-card__lotus")}
    <div class="footer-cta">
      <div class="footer-cta__copy">
        {label("Take the first step towards your empowered future", dot=True, cls="label--light")}
        <p class="h-xl mt-m" data-lines>Let’s start your<br><em>next chapter.</em></p>
        <p class="lede mt-m">Whether you’re looking to heal relationships, shift your workplace culture, or simply breathe again—you’re in the right place.</p>
      </div>
      <a class="footer-cta__btn" href="contact.html" data-magnetic-strong><span>Book your<br>free call{ARROW_UR}</span></a>
    </div>
    <div class="footer-grid">
      <div class="footer-col footer-col--brand">
        <img class="footer-logo" src="assets/brand/logo-white.png" alt="Arielle Innou Coaching" width="900" height="320" loading="lazy">
        <p>Arielle Innou Nahmias, Life &amp; Relationship Coach. Clarity, confidence, and unapologetic living.</p>
      </div>
      <div class="footer-col"><h3>Explore</h3><ul>
        <li><a href="index.html">Home</a></li><li><a href="about.html">About Arielle</a></li><li><a href="contact.html">Contact</a></li>
      </ul></div>
      <div class="footer-col"><h3>Services</h3><ul>
        <li><a href="life-relationship-coaching.html">Life &amp; Relationship Coaching</a></li>
        <li><a href="corporate-coaching.html">Corporate Coaching</a></li>
        <li><a href="retreats.html">Retreats</a></li>
      </ul></div>
      <div class="footer-col"><h3>Get in touch</h3><ul>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>{LOCATION}</li>
        <li>Sessions via Zoom or in person</li>
      </ul></div>
    </div>
    <p class="footer-wordmark" aria-hidden="true">Clarity · Confidence · Connection</p>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> Arielle Innou Coaching. All rights reserved.</span>
      <span>Resources: coming soon</span>
      <a href="#main">Back to top ↑</a>
    </div>
  </div>
</footer>"""


CHROME = f"""
<div class="preloader" aria-hidden="true">
  <div class="preloader__inner">
    {lotus("preloader__lotus", draw=True)}
    <p class="preloader__name"><span>Arielle Innou</span></p>
    <p class="preloader__words"><span>Clarity</span><span>Confidence</span><span>Connection</span></p>
  </div>
  <div class="preloader__bar"><span></span></div>
</div>
<div class="curtain" aria-hidden="true">
  <span class="curtain__layer curtain__layer--a"></span>
  <span class="curtain__layer curtain__layer--b"></span>
  <div class="curtain__inner">
    {lotus("curtain__lotus", draw=True)}
    <p class="curtain__brand"><span>Arielle Innou</span></p>
    <p class="curtain__to"><span class="curtain__rule"></span><span class="curtain__title" data-curtain-title>Coaching</span><span class="curtain__rule"></span></p>
  </div>
</div>
<script>try{{var t=sessionStorage.getItem("ai-nav-title");if(t)document.querySelector("[data-curtain-title]").textContent=t}}catch(e){{}}</script>
<div class="scroll-progress" aria-hidden="true"><span></span></div>
<div class="cursor" aria-hidden="true"><span class="cursor__ring"><span class="cursor__label"></span></span><span class="cursor__dot"></span></div>"""

STICKY = f"""
<div class="sticky-cta" aria-label="Quick actions">
  <a class="btn btn--primary btn--block" href="contact.html"><span class="btn__text">Book your free call</span><span class="btn__icon">{ARROW}</span></a>
</div>"""

FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..600,0..100;"
         "1,9..144,300..600,0..100&family=Manrope:wght@400;500;600;700&display=swap")


def page(filename, title, description, body, og="home", jsonld=None, active=None):
    active = filename if active is None else active
    canonical = f"{SITE_URL}/" if filename == "index.html" else f"{SITE_URL}/{filename.replace('.html', '')}"
    ld = "".join(f'\n<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    noindex = '\n<meta name="robots" content="noindex, follow">' if filename == "404.html" else ""
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">{noindex}
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#f7f2ec">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/assets/img/og/{og}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE_URL}/assets/img/og/{og}.jpg">
<link rel="icon" href="assets/brand/favicon-48.png" sizes="48x48" type="image/png">
<link rel="icon" href="assets/brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/brand/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/css/styles.css">
<link rel="stylesheet" href="assets/css/editor-global.css">
<style id="page-styles"></style>
<script>try{{var d=document.documentElement;d.classList.add("js");if(sessionStorage.getItem("ai-nav")){{d.classList.add("is-entering");sessionStorage.removeItem("ai-nav")}}else if(!sessionStorage.getItem("ai-seen")&&!matchMedia("(prefers-reduced-motion: reduce)").matches){{d.classList.add("is-loading")}}setTimeout(function(){{d.classList.remove("is-loading","is-entering")}},5000)}}catch(e){{}}</script>{ld}
</head>
<body>
{CHROME}
<!-- editor:header -->{header(active)}
<!-- /editor:header -->
<main id="main">
<!-- editor:main -->
{body}
<!-- /editor:main -->
</main>
<!-- editor:footer -->{footer()}
<!-- /editor:footer -->
{STICKY}
<script src="assets/vendor/gsap.min.js" defer></script>
<script src="assets/vendor/ScrollTrigger.min.js" defer></script>
<script src="assets/js/main.js" defer></script>
<script src="assets/js/motion.js" defer></script>
</body>
</html>
"""
    out = ROOT / filename
    if out.exists() and EDITED_MARK in out.read_text() and not FORCE:
        # Keep everything saved from the editor; only refresh the shared intro screen / page curtain
        # that sits between <body> and the editable header.
        cur = out.read_text()
        a, b = cur.find("<body>"), cur.find("<!-- editor:header -->")
        if a >= 0 and b > a:
            fresh = cur[:a] + "<body>\n" + CHROME.strip("\n") + "\n" + cur[b:]
            if fresh != cur:
                out.write_text(fresh)
                print(f"  refreshed the page transition in {filename} (editor content kept)")
                return
        print(f"  skipped {filename} (edited in the visual editor; use --force to overwrite)")
        return
    out.write_text(html)
    print(f"  wrote {filename}")


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
PERSON = {"@type": "Person", "name": "Arielle Innou Nahmias", "jobTitle": "Certified Life & Relationship Coach",
          "email": f"mailto:{EMAIL}", "image": f"{SITE_URL}/assets/img/arielle-portrait-1600.webp",
          "address": {"@type": "PostalAddress", "addressLocality": "Toronto", "addressRegion": "ON", "addressCountry": "CA"}}
BUSINESS = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": SITE_NAME, "url": f"{SITE_URL}/",
            "image": f"{SITE_URL}/assets/img/og/home.jpg", "logo": f"{SITE_URL}/assets/brand/icon-512.png",
            "description": "Life, relationship and corporate coaching, plus restorative retreats, with Arielle Innou Nahmias in Toronto.",
            "email": EMAIL, "areaServed": ["Toronto", "Ontario", "Canada"],
            "address": {"@type": "PostalAddress", "addressLocality": "Toronto", "addressRegion": "ON", "addressCountry": "CA"},
            "founder": PERSON}


def build_home():
    services = ""
    svc = [
        ("life-relationship-coaching.html", "new-chapter", "A woman laughing as she reads a message on her phone", "Life &amp; Relationship <em>Coaching</em>",
         "1:1 coaching for women in transition: reclaim your identity, rewrite old stories, and build boundaries that protect your peace.", "For individuals"),
        ("corporate-coaching.html", "leaders", "Three smiling professional women at a meeting table", "Corporate <em>Coaching</em>",
         "Empowered teams. Clear communication. A workplace that works, for dental offices, healthcare providers and growing businesses.", "For leaders &amp; teams"),
        ("retreats.html", "sisterhood", "Women in flowing dresses with arms around each other, facing the landscape", "Transformative <em>Retreats</em>",
         "Step away from the demands of daily life into a safe, nurturing sanctuary in the Ontario countryside.", "For individuals &amp; groups"),
    ]
    for i, (h, im, alt, t, d, who) in enumerate(svc):
        services += f"""
        <a class="svc-card reveal" href="{h}" data-cursor="Explore" style="--d:{i}">
          {media(im, alt, "svc-card__media", "(min-width: 1024px) 31vw, (min-width: 700px) 50vw, 92vw", reveal=False)}
          <div class="svc-card__body">
            <div class="svc-card__top"><span class="svc-card__num">0{i + 1}</span><span class="pill">{who}</span></div>
            <h3 class="h-lg">{t}</h3>
            <p>{d}</p>
            <span class="svc-card__go">Explore {ARROW}</span>
          </div>
        </a>"""

    body = f"""
<section class="hero">
  <div class="hero__bg" aria-hidden="true">{lotus("hero__lotus")}</div>
  <div class="container hero__grid">
    <div class="hero__copy">
      {label("Life &amp; Relationship Coach · Toronto", dot=True, cls="reveal")}
      <h1 class="display hero__title" data-lines>Clear, confident,<br>and <em>in control</em><br>again.</h1>
      <p class="lede reveal">Life and relationship coaching for individuals and groups who feel emotionally drained, overwhelmed by life transitions.</p>
      <div class="actions reveal">{btn(CTA, "contact.html")}{link("Ways to work together", "#services")}</div>
    </div>
    <div class="hero__visual">
      <div class="hero__halo" aria-hidden="true"></div>
      {media("arielle-seated", "Arielle Innou Nahmias, smiling, seated in a red silk blouse", "arch hero__photo", "(min-width: 900px) 40vw, 86vw", lazy=False, priority=True)}
      <a class="badge" href="contact.html" aria-label="{CTA}" data-cursor="Book">
        <svg class="badge__ring" viewBox="0 0 120 120" aria-hidden="true"><defs><path id="badge-path" d="M60 60m-47 0a47 47 0 1 1 94 0a47 47 0 1 1-94 0"/></defs><text><textPath href="#badge-path" textLength="290" lengthAdjust="spacing">Free 30-minute call · Book yours today ·</textPath></text></svg>
        <span class="badge__core">{ARROW_UR}</span>
      </a>
      <figure class="hero__note reveal">
        <blockquote>“We were taught to stay small. I help you unlearn that story—and write a new one.”</blockquote>
        <figcaption>Arielle Innou Nahmias</figcaption>
      </figure>
    </div>
  </div>
  <div class="container">
    <ul class="pillars reveal" aria-label="Clarity, confidence, connection">
      <li><small>01</small>Clarity</li><li><small>02</small>Confidence</li><li><small>03</small>Connection</li>
    </ul>
  </div>
</section>
{marquee(["Clarity", "Confidence", "Connection", "Healthy boundaries", "Self-trust", "Peace", "Unapologetic living"])}

<section class="section" id="story">
  <div class="container">
    {head("Sound familiar?", "It’s not too late to find out<br>who you <em>really</em> are.", "And learn to live life on your terms.")}
    <p class="statement mt-xl" data-scrub-words>You’ve raised your family, supported your partner, handled workplace drama gracefully… but inside, you’re <em>exhausted.</em></p>
    <div class="cols-2 mt-xl">
      <p class="body reveal">You’ve been in a routine, but you’re feeling a void. And despite your best efforts—self-help books, late-night journaling—you still feel unheard, unfulfilled, and unsure how to move forward.</p>
      <p class="body reveal">The relationships around you—at home, with friends, at work, and even with yourself—feel strained or confusing. Toxic relationships take a toll and drain you of all your energy.</p>
    </div>
  </div>
</section>

<section class="section section--night question">
  <div class="question__float question__float--a" aria-hidden="true">{media("women-joy", "", "arch", "20vw", reveal=False)}</div>
  <div class="question__float question__float--b" aria-hidden="true">{media("meditation", "", "arch", "18vw", reveal=False)}</div>
  <div class="container question__inner">
    <p class="label label--light reveal">And maybe the hardest question of all is quietly echoing in the back of your mind</p>
    <p class="question__q" data-lines>“Who am<br><em>I now?”</em></p>
    <p class="lede reveal">You’ve given so much to others. And all that negative energy is pulling you down.</p>
    <div class="question__nots">
      <p class="question__not reveal">You’re not broken.</p>
      <p class="question__not reveal">You’re not lost.</p>
    </div>
    <p class="h-md question__chapter reveal">You’re just in a new chapter, and you haven’t had the tools, space, or support to rediscover <em>you.</em></p>
    <div class="actions actions--center reveal">{btn(CTA, "contact.html", "light")}</div>
  </div>
</section>

<section class="section" id="services">
  <div class="container">
    {head("Ways to work together", "It’s time to make yourself<br>a priority, <em>without the guilt.</em>", "Private coaching, team coaching and restorative retreats, each grounded in the same belief: transformative change begins within.")}
    <div class="svc-grid">{services}
    </div>
  </div>
</section>

<section class="section section--plum meet">
  <div class="container meet__grid">
    <div class="meet__visual">
      {media("arielle-portrait", "Arielle Innou Nahmias with her arms crossed, smiling", "arch", "(min-width: 900px) 38vw, 90vw")}
      <div class="meet__seal" aria-hidden="true">{lotus("meet__seal-lotus")}<span>Certified<br>Life &amp; Relationship<br>Coach</span></div>
    </div>
    <div class="meet__copy">
      {label("Meet your coach", dot=True, cls="label--light")}
      <h2 class="h-xl" data-lines>Meet Arielle<br><em>Innou Nahmias.</em></h2>
      <ul class="chips reveal"><li>Certified Life &amp; Relationship Coach</li><li>Empath</li><li>Multilingual</li><li>Woman who’s walked your path</li></ul>
      <p class="lede reveal">I know what feeling invisible, stuck, and misunderstood is like. I’ve been there—navigating identity, expectations, and survival in a world that didn’t always make space for me.</p>
      <div class="hats reveal">
        <p class="label label--light">I’ve worn many hats</p>
        <ol class="hats__list"><li>Fashion designer</li><li>Real estate agent</li><li>Corporate leader</li><li>25 years in dental: manager, marketing expert &amp; HR coordinator</li></ol>
      </div>
      <p class="body reveal">Along the way, I’ve worked with people from all walks of life. That diversity has deepened my empathy, sharpened my intuition, and reinforced one truth again and again:</p>
      <p class="meet__truth reveal">We were not taught to put our needs first. <em>But we can learn.</em></p>
      <p class="body reveal">I learned the language of people—the unspoken conflicts, the cultural nuances, the unhealed patterns that shape how we show up in the world. I became a certified life and relationship coach—not because I had all the answers, but because I had finally found the clarity to guide others toward their own.</p>
      <div class="actions reveal">{btn("Read Arielle’s story", "about.html", "light")}</div>
    </div>
  </div>
</section>

{statement("“We were taught to stay small. I help you unlearn that story—and <em>write a new one.</em>”", "In her words", "statement--quote")}
{steps_section(HOME_STEPS, "Our collaborative process", "Your path to clarity<br>and confidence <em>starts here.</em>", "Three simple steps, at your pace. The first one is free.")}
{testimonials_section()}

<section class="section section--sand">
  <div class="container">
    {head("The cost of staying the same", "Or the power<br>of <em>transformation.</em>", "Tap between the two. Only one of them is a future you have to accept.")}
    {contrast("If you continue to experience:", COST, "By reclaiming your life, you can:", POWER, "Staying the same", "Transformation")}
  </div>
</section>

<section class="section envision">
  <div class="container envision__inner">
    {lotus("envision__lotus")}
    {label("Envision the empowering realization", dot=True, cls="reveal")}
    <p class="lede reveal">Imagine how it will feel to say:</p>
    <p class="envision__quote" data-scrub-words>“Now I know who I am. I now have more clarity and the ability to create my <em>dream life.</em>”</p>
    <div class="actions actions--center reveal">{btn(CTA, "contact.html")}</div>
  </div>
</section>"""
    page("index.html", "Arielle Innou Coaching — Life & Relationship Coach, Toronto",
         "Clear, confident, and in control again. Life, relationship and corporate coaching, plus restorative retreats, with certified coach Arielle Innou Nahmias.",
         body, "home", [BUSINESS])


def build_about():
    chapters = ""
    for i, (place, role, text, image) in enumerate(STORY):
        pic = media(image, "", "chapter__media", "320px", reveal=False) if image else f'<div class="chapter__mark" aria-hidden="true">{lotus()}</div>'
        chapters += f"""
          <article class="chapter" style="--i:{i}">
            <div class="chapter__top"><span class="chapter__num">0{i + 1}</span><span class="label">{role}</span></div>
            {pic}
            <div><h3 class="h-md">{place}</h3><p class="body mt-s">{text}</p></div>
          </article>"""
    beliefs = "".join(
        f'<li class="belief reveal"><span class="belief__num">0{i + 1}</span><p class="belief__text"><strong>{a}</strong> <em>{b}</em></p>{lotus("belief__lotus")}</li>'
        for i, (a, b) in enumerate(BELIEFS))
    why = "".join(f'<li class="reveal"><span>0{i + 1}</span><p>{w}</p></li>' for i, w in enumerate(WHY))

    body = f"""
{page_hero("About Arielle", "Welcome, I am<br><em>Arielle Innou</em><br><em>Nahmias.</em>",
           "I am a dedicated life coach who empowers individuals and leaders to navigate significant personal and professional transitions with clarity, compassion, and courage to embrace change.",
           "arielle-portrait", "Portrait of Arielle Innou Nahmias", btn(CTA, "contact.html") + link("My story", "#story"),
           aside='<div class="page-hero__chip reveal"><strong>25+</strong><span>years leading teams<br>and people</span></div>')}

{statement(f"I specialize in supporting women in midlife {inline_img('women-together')} seeking to rediscover their identity, and leaders {inline_img('leaders')} striving to cultivate a more harmonious and <em>productive workplace.</em>", "Who I help")}

<section class="section section--tight">
  <div class="container cols-2 cols-2--wide">
    <p class="body reveal">If you’ve landed here, it’s possible that life feels particularly demanding right now, a little heavier than usual. Perhaps years of prioritizing the needs of others, your family, your work, and your relationships have led to a feeling of disconnection from your own essential needs.</p>
    <div>
      <p class="body reveal">Whether the desire for change stems from within your inner world or your professional environment, you are seeking more than superficial adjustments. You desire genuine peace, clear direction, and a profound sense of self, achieved without the weight of guilt, the disruption of chaos, or the hindrance of self-doubt.</p>
      <p class="h-md mt-m reveal">I understand this journey intimately, having walked this path <em>myself.</em></p>
    </div>
  </div>
</section>

<section class="section section--sand story" id="story" data-hscroll>
  <div class="story__pin">
    <div class="container story__head">
      {label("My story", dot=True)}
      <h2 class="h-xl" data-lines>My story is one<br>of <em>resilience.</em></h2>
      <div class="story__progress" aria-hidden="true"><span></span></div>
    </div>
    <div class="story__track">{chapters}
      <article class="chapter chapter--end">
        <p class="h-md">Grounded in the belief that prioritizing emotional well-being and self-care are <em>learned skills</em>, crucial for both personal fulfillment and thriving workplaces.</p>
        {btn(CTA, "contact.html", "light")}
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="container beliefs">
    <div class="beliefs__aside">
      {label("What I believe", dot=True)}
      <h2 class="h-xl" data-lines>Five truths<br>I <em>coach by.</em></h2>
      {media("meditation", "Hands resting in a meditation pose by the sea", "beliefs__media", "(min-width: 900px) 30vw, 90vw")}
    </div>
    <ol class="beliefs__list">{beliefs}</ol>
  </div>
</section>

<section class="section section--plum principle">
  <div class="container principle__inner">
    {lotus("principle__lotus", draw=True)}
    {label("My coaching practice is rooted in a fundamental principle", dot=True, cls="label--light reveal")}
    <p class="principle__text" data-lines>Transformative change<br>begins <em>within.</em></p>
  </div>
</section>

<section class="section">
  <div class="container">
    {head("Who I work with", "Two kinds of<br><em>new chapters.</em>")}
    <div class="who-grid">
      <a class="who-card reveal" href="life-relationship-coaching.html" data-cursor="Explore">
        {media("women-joy", "Five joyful women holding hands, arms raised", "who-card__media", "(min-width: 900px) 45vw, 92vw", reveal=False)}
        <div class="who-card__body">
          <span class="pill">Women in transition</span>
          <h3 class="h-lg">Empowering women <em>in transition.</em></h3>
          <p>You’ve supported everyone else—your children, your spouse, your coworkers. Now it’s time to reconnect with who you are. I help women 50+ reclaim their identity, rewrite old stories, and build boundaries that protect their peace.</p>
          <span class="svc-card__go">Life &amp; Relationship Coaching {ARROW}</span>
        </div>
      </a>
      <a class="who-card reveal" href="corporate-coaching.html" data-cursor="Explore">
        {media("leaders", "Three professional women smiling at a meeting table", "who-card__media", "(min-width: 900px) 45vw, 92vw", reveal=False)}
        <div class="who-card__body">
          <span class="pill">Leaders &amp; teams</span>
          <h3 class="h-lg">High-performing leaders <em>&amp; teams.</em></h3>
          <p>Whether it’s low morale, employee conflict, or high turnover—I support organizations in building workplaces that work. I specialize in coaching for dental offices, healthcare providers, and small-to-mid-size businesses.</p>
          <span class="svc-card__go">Corporate Coaching {ARROW}</span>
        </div>
      </a>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="container why">
    <div class="why__copy">
      {label("Why people work with me", dot=True)}
      <h2 class="h-xl" data-lines>Real-life experience.<br><em>Deep emotional insight.</em></h2>
      <ol class="why__list">{why}</ol>
    </div>
    {media("arielle-estate", "Arielle walking across the lawn at Bella Estate Gardens", "arch why__media", "(min-width: 900px) 34vw, 80vw")}
  </div>
</section>"""
    page("about.html", "About Arielle Innou Nahmias — Life & Relationship Coach",
         "From Fez to France to Toronto: meet Arielle Innou Nahmias, a certified life and relationship coach helping women in midlife and leaders navigate change.",
         body, "about", [{"@context": "https://schema.org", **PERSON, "worksFor": {"@type": "Organization", "name": SITE_NAME}}])


def build_life():
    roles = "".join(f'<li class="role" style="--i:{i}">{r}</li>' for i, r in enumerate(ROLES))
    included = "".join(
        f'<article class="feature reveal" style="--d:{i}">{ficon(ic)}<h3 class="h-sm">{t}</h3><p>{d}</p></article>'
        for i, (ic, t, d) in enumerate(LIFE_INCLUDED))
    actions = btn(CTA, "contact.html") + btn("Apply now", APPLY_LIFE, "ghost", ext=True)
    body = f"""
{page_hero("1:1 Life &amp; Relationship Coaching", "Because it’s not<br>too late to feel<br>like <em>you again.</em>",
           "Private coaching for women ready to reconnect with who they are—and create lives that reflect their values, voice, and vision.",
           "new-chapter", "A woman laughing as she reads a message on her phone", actions,
           aside='<div class="page-hero__chip reveal"><strong>1:1</strong><span>via Zoom<br>or in person</span></div>')}

<section class="section roles-section">
  <div class="container">
    {head("You’ve spent a lifetime holding it all together", "You’ve raised kids, kept the peace,<br>supported a partner, and probably<br>held it down <em>at work, too.</em>")}
    <div class="roles-wrap">
      <p class="body reveal">You’ve played so many roles for so long—</p>
      <ul class="roles" data-roles>{roles}</ul>
      <p class="body reveal">—that now, with a little space to breathe… you’re asking:</p>
      <p class="roles__q" data-lines>“Who am <em>I now?”</em></p>
    </div>
  </div>
</section>

<section class="section section--night feelings">
  <div class="container feelings__grid">
    <div class="feelings__lines">
      <p class="feelings__line reveal">You feel emotionally <em>drained.</em></p>
      <p class="feelings__line reveal">Pulled in a million <em>directions.</em></p>
      <p class="feelings__line reveal">Your relationships—at home, work, even with yourself—feel strained or <em>unbalanced.</em></p>
    </div>
    <div class="feelings__aside">
      <p class="lede reveal">And while everyone around you may think you’re “doing fine,” inside you feel lost, unfulfilled, and unsure how to move forward.</p>
      <div class="callout reveal">
        {lotus("callout__lotus")}
        <p class="h-md">You’re not broken. You’re not behind. You’re just at a turning point—and you deserve the support to meet it with <em>clarity and confidence.</em></p>
        {btn(CTA, "contact.html", "light")}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split">
    {media("arielle-seated", "Arielle Innou Nahmias seated, smiling warmly", "arch split__media", "(min-width: 900px) 40vw, 90vw")}
    <div class="split__copy">
      {label("Hi, I’m Arielle", dot=True)}
      <h2 class="h-xl" data-lines>A woman who’s<br><em>been there.</em></h2>
      <p class="pill-row reveal"><span class="pill">Certified Life &amp; Relationship Coach</span><span class="pill">Empath</span></p>
      <p class="lede reveal">I help women 50+ reconnect with who they are—and create lives that reflect their values, voice, and vision.</p>
      <p class="body reveal">I know what it’s like to feel invisible. To spend so long supporting others that you forget how to support yourself. I’ve navigated identity shifts, cultural expectations, and burnout from giving too much without enough return.</p>
      <p class="h-md reveal">That’s why I became a coach—not to hand out advice, but to create space for <em>your truth to rise.</em></p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container pair">
    <div class="pair__card pair__card--lilac reveal">
      {label("This is a space where you’ll feel")}
      {checklist(LIFE_FEEL)}
    </div>
    <div class="pair__card pair__card--mint reveal">
      {label("We’ll work together to")}
      {checklist(LIFE_TOGETHER)}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {head("What’s included", "Everything you need<br>to <em>shift for good.</em>")}
    <div class="features">{included}</div>
  </div>
</section>

{testimonials_section(dark=True)}

<section class="section section--sand">
  <div class="container">
    {head("Your choice", "What happens when<br>you say <em>yes to you?</em>", "But it doesn’t have to be this way.")}
    {contrast("What happens if nothing changes?", LIFE_NO, "What happens when you say yes to you:", LIFE_YES, "If nothing changes", "Say yes to you")}
  </div>
</section>

{steps_section(LIFE_STEPS, "Your path", "Your path to feeling<br>like <em>you again.</em>", "Begin with a complimentary 30-minute consultation.")}

<section class="section">
  <div class="container">
    <div class="cta-panel reveal">
      {media("women-together", "", "cta-panel__media", "100vw", reveal=False)}
      <div class="cta-panel__body">
        {label("It’s your turn", dot=True, cls="label--light")}
        <h2 class="h-xl" data-lines>You’ve given so much.<br>It’s time to give <em>to yourself.</em></h2>
        <p class="lede">Let’s find out who you really are—and help you start living like her.</p>
        <div class="actions">{btn(CTA, "contact.html", "light")}{btn("Apply now", APPLY_LIFE, "ghost-light", ext=True)}</div>
      </div>
    </div>
  </div>
</section>"""
    page("life-relationship-coaching.html", "Life & Relationship Coaching for Women — Arielle Innou",
         "1:1 coaching for women in transition: set boundaries without guilt, heal relationship wounds and feel like you again. Via Zoom or in person in Toronto.",
         body, "life", [{"@context": "https://schema.org", "@type": "Service", "name": "Life & Relationship Coaching", "provider": {"@type": "ProfessionalService", "name": SITE_NAME}, "areaServed": "Toronto, Ontario", "description": "Private 1:1 sessions via Zoom or in person, customized Clarity Plans, ongoing support and tools for emotional strength."}])


def build_corporate():
    results = "".join(f'<li class="reveal"><span>{CHECK}</span>{r}</li>' for r in CORP_RESULTS)
    programs = ""
    for i, (t, d, items, image) in enumerate(CORP_PROGRAMS):
        programs += f"""
        <article class="program reveal" style="--d:{i}">
          {media(image, "", "program__media", "(min-width: 900px) 45vw, 92vw", reveal=False)}
          <div class="program__body">
            <span class="program__num">0{i + 1}</span>
            <h3 class="h-lg">{t}</h3>
            <p class="body">{d}</p>
            {checklist(items)}
          </div>
        </article>"""
    roi = "".join(
        f'<article class="roi reveal" style="--d:{i}">{ficon(ic)}<span class="roi__num">0{i + 1}</span><h3 class="h-md">{t}</h3><p>{d}</p></article>'
        for i, (ic, t, d) in enumerate(CORP_ROI))
    actions = btn(CTA, "contact.html") + btn("Apply for corporate coaching", APPLY_CORPORATE, "ghost", ext=True)
    body = f"""
{page_hero("Corporate Coaching with Arielle Innou", "Empowered teams.<br>Clear communication.<br>A workplace <em>that works.</em>",
           "Customized coaching for dental offices, healthcare providers, and small-to-mid-size businesses that gets to the root of dysfunction.",
           "leaders", "Three professional women smiling around a laptop", actions, cls="page-hero--wide", shape="rounded",
           aside='<div class="page-hero__chip reveal"><strong>300%</strong><span>team growth, with<br>culture intact</span></div>')}

<section class="section">
  <div class="container">
    {head("The real cost", "What’s really going on when you<br>notice tension between <em>team members?</em>")}
    <div class="cols-2 mt-l">
      <p class="lede reveal">You’ve got staff burnout, interpersonal conflict, or unspoken resentment that’s hurting morale.</p>
      <p class="body reveal">And maybe, as a business owner or manager, you’re feeling stuck in the middle—unsure how to fix it without making it worse. <strong>You’re not imagining it.</strong> Toxic dynamics and miscommunication don’t just hurt feelings—they hurt your business.</p>
    </div>
  </div>
</section>

<section class="kinetic" aria-label="High turnover. Low engagement. Missed goals.">
  <p class="kinetic__row" data-drift="-1"><span>High turnover.</span><span>Low engagement.</span><span>Missed goals.</span><span>High turnover.</span></p>
  <p class="kinetic__row kinetic__row--alt" data-drift="1"><span>When your team isn’t aligned,</span><em>everything suffers.</em><span>When your team isn’t aligned,</span></p>
</section>

<section class="section section--plum">
  <div class="container corp-bio">
    <div class="corp-bio__copy">
      {label("Hi, I’m Arielle Innou", dot=True, cls="label--light")}
      <h2 class="h-xl" data-lines>Corporate coach.<br>25+ years in operations.<br><em>Conflict whisperer.</em></h2>
      <p class="lede reveal">With a background that spans business ownership, team leadership, and HR operations in healthcare, I know what it’s like to juggle logistics and emotions in the workplace.</p>
      <p class="body reveal">I spent 25 years transforming a small dental practice into a thriving multi-doctor, multi-staff clinic—handling conflict resolution, onboarding, training, marketing, and mentorship.</p>
      <div class="stats reveal">
        <div class="stat"><span class="stat__num"><span data-count="300">300</span>%</span><span class="stat__label">team growth, with a strong, collaborative culture</span></div>
        <div class="stat"><span class="stat__num"><span data-count="25">25</span>+</span><span class="stat__label">years in healthcare operations and HR</span></div>
      </div>
    </div>
    <div class="corp-bio__results">
      {media("arielle-portrait", "Arielle Innou with her arms crossed", "arch corp-bio__media", "(min-width: 900px) 30vw, 80vw")}
      <div class="results reveal">
        <p class="label label--light">Past results</p>
        <ul class="results__list">{results}</ul>
      </div>
    </div>
  </div>
</section>

{statement("Now, I help other leaders and teams do the same—with customized coaching that gets to the root of dysfunction and builds a culture of <em>trust, clarity, and collaboration.</em>", "Today")}

<section class="section section--sand">
  <div class="container">
    {head("From burnout to buy-in", "Coaching that creates<br><em>real change.</em>")}
    <div class="programs">{programs}</div>
  </div>
</section>

<section class="section section--night">
  <div class="container">
    {head("The ROI you can expect", "A healthier workplace<br>is a <em>better business.</em>")}
    <div class="roi-grid">{roi}</div>
  </div>
</section>

{steps_section(CORP_STEPS, "Your path to a healthy workplace", "Three steps to a<br>team that <em>works.</em>", "It starts with a complimentary 30-minute call.")}

<section class="section">
  <div class="container">
    <div class="cta-panel reveal">
      {media("leaders", "", "cta-panel__media", "100vw", reveal=False)}
      <div class="cta-panel__body">
        {label("Ready to build a better workplace?", dot=True, cls="label--light")}
        <h2 class="h-xl" data-lines>Let’s shift the dynamic—<br><em>for good.</em></h2>
        <p class="lede">Let’s talk about your team, your goals, and how we can shift the dynamic—for good.</p>
        <div class="actions">{btn(CTA, "contact.html", "light")}{btn("Apply now", APPLY_CORPORATE, "ghost-light", ext=True)}</div>
      </div>
    </div>
  </div>
</section>"""
    page("corporate-coaching.html", "Corporate Coaching for Healthier Teams — Arielle Innou",
         "Team coaching and culture transformation for dental offices, healthcare providers and growing businesses. Reduce turnover, resolve conflict, build trust.",
         body, "corporate", [{"@context": "https://schema.org", "@type": "Service", "name": "Corporate Coaching", "provider": {"@type": "ProfessionalService", "name": SITE_NAME}, "areaServed": "Ontario", "description": "Team coaching and group dynamics, staff wellness and culture transformation."}])


def build_retreats():
    included = "".join(
        f'<article class="feature feature--line reveal" style="--d:{i}">{ficon(ic)}<h3 class="h-sm">{t}</h3><p>{d}</p></article>'
        for i, (ic, t, d) in enumerate(RETREAT_INCLUDED))
    def gshape(n):
        m = META[n]
        return " gallery__item--wide" if n == "retreat-gardens" else (" gallery__item--tall" if m["h"] > m["w"] else "")
    gallery = "".join(
        f'<button class="gallery__item{gshape(n)} reveal" type="button" data-full="assets/img/{n}-1600.webp" data-cursor="View" aria-label="View photo: {a}">'
        f'{img(n, a, "(min-width: 1024px) 30vw, (min-width: 600px) 45vw, 92vw")}</button>'
        for n, a in RETREAT_GALLERY)
    body = f"""
<section class="retreat-hero">
  <div class="retreat-hero__media" data-parallax-hero>{img("sisterhood", "Women in flowing dresses standing together, arms around each other, looking out over the land", "100vw", lazy=False, priority=True)}</div>
  <div class="retreat-hero__shade" aria-hidden="true"></div>
  <div class="container retreat-hero__inner">
    {label("Retreats with Arielle Innou", dot=True, cls="label--light reveal")}
    <h1 class="display retreat-hero__title" data-lines>The Sanctuary<br><em>Navigator.</em></h1>
    <p class="lede reveal">Guiding you to transformative retreats.</p>
    <div class="actions reveal">{btn("Register for the retreat", REGISTER_RETREAT, "light", ext=True)}{btn("Retreat details", "#details", "ghost-light")}</div>
  </div>
  <div class="container retreat-hero__words">
    <ol class="aaa reveal"><li><small>01</small>Absorb</li><li><small>02</small>Accept</li><li><small>03</small>Apply</li></ol>
  </div>
</section>

{statement("Complementing my coaching services, I offer a unique opportunity for individuals and groups to step away from the demands of daily life and immerse themselves in a <em>safe, nurturing, and supportive</em> environment.", "The retreat")}

<section class="section section--tight">
  <div class="container split split--rev">
    <div class="collage">
      {media("retreat-statue", "A garden statue in front of the white estate chapel", "collage__a arch", "(min-width: 900px) 26vw, 60vw")}
      {media("retreat-pool", "The pool terrace at Bella Estate Gardens", "collage__b", "(min-width: 900px) 22vw, 50vw")}
    </div>
    <div class="split__copy">
      {label("Bella Estate Gardens", dot=True)}
      <h2 class="h-xl" data-lines>The healing<br>power of <em>nature.</em></h2>
      <p class="lede reveal">Experience the healing power of nature in a beautiful retreat sanctuary surrounded by lush gardens and the inspiring presence of the natural world, nestled in magnificent tranquility away from the busy city.</p>
      <p class="body reveal">Guests will feel truly nurtured by our dedicated and supportive team, thoughtfully prepared healthy and delicious meals with diverse options, and a range of restorative activities such as yoga, meditation, nature immersion, individualized coaching sessions, insightful workshops, and activities designed to support personal growth and well-being.</p>
      <div class="actions reveal">{link("Visit Bella Estate Gardens on Instagram", RETREAT_INSTAGRAM, ext=True)}</div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    {head("What’s included", "Nurtured, <em>every moment.</em>")}
    <div class="features features--3">{included}</div>
  </div>
</section>

<section class="section section--night breathe">
  <div class="container breathe__inner">
    <div class="breathe__orb" aria-hidden="true"><span></span><span></span><span></span></div>
    <p class="breathe__text" data-scrub-words>Nestled in nature and curated with intention, every moment is a time to breathe and remember who you are <em>beneath the noise.</em></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="gallery-head">
      {head("Inside the sanctuary", "A glimpse of<br><em>the estate.</em>")}
      {link("@bellaestategardens", RETREAT_INSTAGRAM, ext=True)}
    </div>
    <div class="gallery" data-gallery>{gallery}</div>
  </div>
</section>

<section class="section section--plum" id="details">
  <div class="container details">
    <div class="details__copy">
      {label("Upcoming retreat details", dot=True, cls="label--light")}
      <h2 class="h-xl" data-lines>A 3-day restorative<br>retreat with <em>Arielle Innou.</em></h2>
      <p class="lede reveal">Absorb. Accept. Apply. Three days to step away, breathe, and remember who you are.</p>
      <div class="actions reveal">{btn("Register for the retreat", REGISTER_RETREAT, "light", ext=True)}{btn("Ask a question", "contact.html", "ghost-light")}</div>
    </div>
    <dl class="details__card reveal">
      <div><dt>Length</dt><dd>3 days, restorative</dd></div>
      <div><dt>Where</dt><dd>Ontario countryside<br>Bella Estate Gardens</dd></div>
      <div><dt>When</dt><dd>Next dates announced soon</dd></div>
      <div><dt>Who</dt><dd>Individuals &amp; groups</dd></div>
      <div><dt>Includes</dt><dd>Meals, yoga, meditation, coaching &amp; workshops</dd></div>
      <div><dt>Status</dt><dd><span class="status-dot"></span>Now accepting registrations</dd></div>
    </dl>
  </div>
</section>

<div class="lightbox" hidden aria-modal="true" role="dialog" aria-label="Photo viewer">
  <button class="lightbox__close" type="button" aria-label="Close">{CLOSE}</button>
  <button class="lightbox__nav lightbox__nav--prev" type="button" aria-label="Previous photo">{PREV}</button>
  <figure class="lightbox__figure"><img alt="Retreat photo"><figcaption></figcaption></figure>
  <button class="lightbox__nav lightbox__nav--next" type="button" aria-label="Next photo">{NEXT}</button>
</div>"""
    page("retreats.html", "Transformative Retreats in Ontario — Arielle Innou Coaching",
         "A 3-day restorative retreat with Arielle Innou at Bella Estate Gardens in the Ontario countryside: yoga, meditation, nature immersion, coaching and workshops.",
         body, "retreats", [{"@context": "https://schema.org", "@type": "Event", "name": "A 3-day restorative retreat with Arielle Innou",
                             "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                             "location": {"@type": "Place", "name": "Bella Estate Gardens", "address": {"@type": "PostalAddress", "addressRegion": "ON", "addressCountry": "CA"}},
                             "organizer": {"@type": "Organization", "name": SITE_NAME, "url": f"{SITE_URL}/"},
                             "image": f"{SITE_URL}/assets/img/og/retreats.jpg"}])


def build_contact():
    interests = [("life", "Life &amp; Relationship"), ("corporate", "Corporate coaching"), ("retreats", "Retreats"), ("unsure", "Not sure yet")]
    chips = "".join(
        f'<label class="chip-opt"><input type="radio" name="interest" value="{v}"{" checked" if i == 0 else ""}><span>{t}</span></label>'
        for i, (v, t) in enumerate(interests))
    faqs = "".join(
        f'<details class="faq__item"><summary>{q}<span class="faq__icon" aria-hidden="true"></span></summary><div class="faq__body"><div><p>{a}</p></div></div></details>'
        for q, a in FAQS)
    apps = [
        ("Life &amp; Relationship Coaching", "Application", APPLY_LIFE, "new-chapter"),
        ("Corporate Coaching", "Application", APPLY_CORPORATE, "leaders"),
        ("The 3-day retreat", "Registration", REGISTER_RETREAT, "sisterhood"),
    ]
    app_cards = "".join(
        f'<a class="app-card reveal" href="{h}" target="_blank" rel="noopener" style="--d:{i}"><span class="app-card__img" style="{bg(im)}" aria-hidden="true"></span>'
        f'<span class="app-card__text"><small>{k}</small><strong>{t}</strong></span><span class="app-card__go">{ARROW_UR}</span></a>'
        for i, (t, k, h, im) in enumerate(apps))
    body = f"""
<section class="contact-hero">
  <div class="container contact">
    <div class="contact__copy">
      {label("Contact Arielle", dot=True, cls="reveal")}
      <h1 class="display contact__title" data-lines>Let’s talk about<br><em>where you are.</em></h1>
      <p class="lede reveal">Where you want to go, and how we can get there—together. Send a note, or book your complimentary 30-minute call.</p>
      <ul class="info reveal">
        <li><span class="info__ic">{MAIL}</span><span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
        <li><span class="info__ic">{PIN}</span><span><small>Based in</small>{LOCATION}</span></li>
        <li><span class="info__ic">{svg(FEATURE_ICONS["video"])}</span><span><small>Sessions</small>Via Zoom or in person</span></li>
      </ul>
      {media("arielle-garden", "Arielle at a garden luncheon at Bella Estate Gardens", "arch contact__media", "(min-width: 900px) 22vw, 60vw")}
    </div>
    <form class="form reveal" action="https://formspree.io/f/{FORMSPREE_ID}" method="POST" novalidate data-form>
      <div class="form__head">
        <p class="h-md">Book your free <em>30-minute call.</em></p>
        <p class="body">Tell me a little about where you are. I’ll reply personally to find a time that suits your schedule.</p>
      </div>
      <fieldset class="field field--chips">
        <legend>I’m interested in</legend>
        <div class="chip-opts">{chips}</div>
      </fieldset>
      <div class="field-row">
        <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" autocomplete="name" required><span class="field__error">Please enter your name.</span></div>
        <div class="field"><label for="f-email">Your email</label><input id="f-email" name="email" type="email" autocomplete="email" required><span class="field__error">Please enter a valid email.</span></div>
      </div>
      <div class="field"><label for="f-phone">Phone <span class="field__opt">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="f-msg">Your message</label><textarea id="f-msg" name="message" rows="5" required placeholder="Where are you now, and where would you like to be?"></textarea><span class="field__error">Please enter a message.</span></div>
      <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn btn--primary btn--block" type="submit"><span class="btn__text">Send message</span><span class="btn__icon">{ARROW}</span></button>
      <p class="form__fine">Your details stay private and are only used to reply to you.</p>
      <div class="form-success" role="status" hidden>
        {lotus("form-success__lotus")}
        <p class="h-md">Thanks for your message! <em>I’ll be in touch soon.</em></p>
        <p class="body">In the meantime, take a breath. You’ve already taken the first step.</p>
      </div>
      <p class="form-error" role="alert" hidden>Message failed. Please try again, or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </form>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    {head("Ready to apply?", "Applications &amp;<br><em>registration.</em>", "Already know what you need? Go straight to the right form.")}
    <div class="apps">{app_cards}</div>
  </div>
</section>

<section class="section">
  <div class="container faq-layout">
    <div class="faq-layout__aside">
      {label("Questions", dot=True)}
      <h2 class="h-xl" data-lines>Good to<br><em>know.</em></h2>
      <p class="body reveal">Anything else? Email <a class="inline-link" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
    <div class="faq">{faqs}</div>
  </div>
</section>"""
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    page("contact.html", "Contact Arielle Innou — Book Your Free 30-Minute Call",
         "Book a complimentary 30-minute call with certified life and relationship coach Arielle Innou Nahmias in Toronto, or apply for coaching and retreats.",
         body, "contact", [faq_ld])


def build_404():
    body = f"""
<section class="notfound">
  <div class="container notfound__inner">
    {lotus("notfound__lotus", draw=True)}
    {label("Page not found", dot=True)}
    <h1 class="display" data-lines>This path<br><em>wandered off.</em></h1>
    <p class="lede reveal">The page you’re looking for has moved or no longer exists. Let’s find your way back.</p>
    <div class="actions actions--center reveal">{btn("Back to home", "index.html")}{btn("Contact Arielle", "contact.html", "ghost")}</div>
  </div>
</section>"""
    page("404.html", "Page not found — Arielle Innou Coaching", "This page has moved or no longer exists.", body, "home", active="")


def build_meta_files():
    pages = ["", "about", "life-relationship-coaching", "corporate-coaching", "retreats", "contact"]
    urls = "".join(f"  <url><loc>{SITE_URL}/{p}</loc></url>\n" for p in pages)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    css = ROOT / "assets" / "css" / "editor-global.css"
    if not css.exists():
        css.write_text("/* Styles saved from the visual editor for the shared header and footer. */\n/* editor:header */\n/* /editor:header */\n/* editor:footer */\n/* /editor:footer */\n")
    (ROOT / "admin").mkdir(exist_ok=True)
    (ROOT / "admin" / "assets.json").write_text(json.dumps(
        [{"src": f"assets/img/{n}-1600.webp", "name": n} for n in sorted(META)], indent=0) + "\n")
    (ROOT / "site.webmanifest").write_text(json.dumps({
        "name": SITE_NAME, "short_name": "Arielle Innou",
        "icons": [{"src": "assets/brand/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
                  {"src": "assets/brand/icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": "#f7f2ec", "background_color": "#f7f2ec", "display": "standalone", "start_url": "./"}, indent=2) + "\n")
    fav = ROOT / "assets" / "brand" / "favicon.svg"
    if not fav.exists():
        paths = "".join(f'<path d="{d}" fill="#f7f2ec" stroke="#2b1a3d" stroke-width="1.1"/>' for d in LOTUS_PATHS)
        fav.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#2b1a3d"/><g transform="translate(6 13) scale(.8125)">{paths}</g></svg>\n')


if __name__ == "__main__":
    build_home()
    build_about()
    build_life()
    build_corporate()
    build_retreats()
    build_contact()
    build_404()
    build_meta_files()
