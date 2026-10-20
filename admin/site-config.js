/* Site settings for the visual editor (admin/).
   The editor engine (editor.js, inspector.js, media.js, seo.js, auth.js) is the same on every site;
   everything specific to Arielle Innou Coaching lives here. */
window.SITE_EDITOR_CONFIG = {
  name: "Arielle Innou",                      // sign-in screen and browser tab
  initials: "AI",                             // little logo on the sign-in screen and top bar
  signInImage: "assets/img/arielle-portrait-1600.webp",
  signInImageSet: "assets/img/arielle-portrait-800.webp 800w, assets/img/arielle-portrait-1600.webp 922w",
  siteName: "Arielle Innou Coaching",         // Google preview
  storageKey: "ai-site-editor",
  sessionKey: "ai-auth-session",
  repo: { owner: "bhavansh-arora", repo: "arielleinnoucoaching", branch: "main" },
  origin: "https://arielleinnoucoaching.codebunny.net",
  titleSuffix: " — Arielle Innou Coaching",
  altSuffix: " — Arielle Innou Coaching",
  altDefault: "Photo from Arielle Innou Coaching",
  videoAltSuffix: " (video thumbnail)",
  altText: function (words, fileName) {
    if (/^arielle/i.test(fileName)) return "Arielle Innou Nahmias, life and relationship coach";
    if (/^retreat/i.test(fileName)) return "Bella Estate Gardens, home of Arielle Innou's retreats";
    return null;
  },

  pages: { "index.html": "Home", "about.html": "About", "life-relationship-coaching.html": "Life & Relationship Coaching",
    "corporate-coaching.html": "Corporate Coaching", "retreats.html": "Retreats", "contact.html": "Contact", "404.html": "404 page" },

  stylesheets: [
    "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..600,0..100;1,9..144,300..600,0..100&family=Manrope:wght@400;500;600;700&display=swap",
    "assets/css/styles.css"
  ],
  globalCss: "assets/css/editor-global.css",
  uploadsDir: "assets/uploads/",
  brandDir: "assets/brand/",
  pageTemplate: "about.html",

  fonts: [
    { id: '"Fraunces", "Times New Roman", serif', label: "Fraunces (site serif)" },
    { id: '"Manrope", "Helvetica Neue", Arial, sans-serif', label: "Manrope (site sans)" }
  ],

  // Quick colour swatches: [name, CSS value, preview hex].
  swatches: [["Plum", "var(--accent-deep)", "#4b2a6b"], ["Purple", "var(--accent)", "#6f439b"], ["Lilac", "var(--lilac)", "#c9b3e6"],
    ["Lilac wash", "var(--accent-soft)", "#e9e0f4"], ["Mint", "var(--mint)", "#bce3de"], ["Mint wash", "var(--mint-soft)", "#dcefeb"],
    ["Ivory", "var(--paper)", "#f7f2ec"], ["Sand", "var(--paper-2)", "#efe6dc"], ["Night", "var(--night)", "#1c1226"], ["Ink", "var(--ink)", "#221833"], ["White", "#ffffff", "#ffffff"]],

  theme: {
    vars: [["--accent", "Purple accent (italic words, highlights)", "#6f439b"], ["--accent-deep", "Buttons", "#4b2a6b"], ["--accent-soft", "Lilac wash (icons, cards)", "#e9e0f4"],
      ["--lilac", "Lilac on dark sections", "#c9b3e6"], ["--mint", "Mint (badges, ticks)", "#bce3de"], ["--mint-soft", "Mint wash (cards)", "#dcefeb"],
      ["--paper", "Page background", "#f7f2ec"], ["--paper-2", "Sand sections", "#efe6dc"], ["--card", "Cards", "#fffaf5"],
      ["--plum", "Plum sections", "#2b1a3d"], ["--night", "Darkest sections & footer", "#1c1226"],
      ["--ink", "Headings & main text", "#221833"], ["--ink-2", "Body text", "#4d4359"], ["--muted", "Small labels", "#8a7e94"]],
    groups: [["Background", [["--paper", "Page background"], ["--paper-2", "Sand sections"], ["--card", "Cards"], ["--plum", "Plum sections"], ["--night", "Darkest sections & footer"]]],
      ["Text", [["--ink", "Headings & main text"], ["--ink-2", "Body text"], ["--muted", "Small labels"]]],
      ["Brand", [["--accent", "Purple (italic words, highlights)"], ["--accent-deep", "Buttons"], ["--accent-soft", "Lilac wash"], ["--lilac", "Lilac on dark"], ["--mint", "Mint"], ["--mint-soft", "Mint wash"]]]]
  },

  // Editor-only CSS: show everything the live site animates, hides or scrolls sideways.
  canvasBackground: "var(--paper,#f7f2ec)",
  editModeCss: [
    ".marquee__track{animation:none!important;flex-wrap:wrap;width:auto!important}",
    ".contrast__panels .contrast__panel{display:grid!important;opacity:1!important;transform:none!important}",
    ".t-track{display:grid!important;gap:36px;overflow:visible!important}.t-slide{padding-bottom:28px;border-bottom:1px dashed rgba(111,67,155,.35)}",
    ".story__track{flex-wrap:wrap!important;overflow:visible!important;width:auto!important}",
    ".roles .role::after{display:none}",
    ".form-success{display:grid!important;margin-top:24px;padding:20px;border:1px dashed #6f439b;border-radius:16px}",
    ".form-success::before{content:'Shown after the form is sent';font:12px ui-monospace,monospace;color:#6f439b}",
    ".form-error{display:block!important}",
    ".section>.container:empty::before{content:'Drop elements here';display:grid;place-items:center;min-height:78px;font:12px ui-monospace,monospace;color:rgba(111,67,155,.8)}",
    ".section>.container{min-height:96px}",
    ".stack:empty,.container:empty{min-height:96px}"
  ],
  // While editing the shared header, the Services dropdown and the phone menu are shown so they can be changed too.
  headerEditCss: ".site-header{position:relative!important;transform:none!important;pointer-events:auto!important;padding-bottom:400px}" +
    ".dropdown{opacity:1!important;visibility:visible!important;transform:translate(-50%,0)!important}" +
    ".mobile-menu{position:relative!important;inset:auto!important;clip-path:none!important;visibility:visible!important;min-height:640px}" +
    ".mobile-menu__list li{opacity:1!important;transform:none!important}.skip-link{position:static!important;display:inline-block;margin:8px}",
  eagerImages: ".story img[loading=lazy], .marquee img[loading=lazy]",

  newPage: function (name, esc) {
    return '<section class="page-hero"><div class="container page-hero__grid"><div class="page-hero__copy"><span class="label label--dot">' + esc(name) + '</span>' +
      '<h1 class="display page-hero__title">' + esc(name) + '</h1><p class="lede">Introduce this page here. Drag ready-made sections in from the Add panel.</p></div></div></section>';
  },

  // The Add panel: [id, category ("Layout" | "Elements" | "Sections"), label, icon, HTML].
  blocks: function (H) {
    var SITE = H.SITE, ico = H.ico;
    var IMG = function (name) { return SITE + "assets/img/" + name + "-1600.webp"; };
    var ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
    var ARROW_UR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>';
    var CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
    var CROSS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 7l10 10M17 7L7 17"/></svg>';
    var LOTUS = '<svg class="lotus" viewBox="0 0 64 40" aria-hidden="true"><path d="M30 36C18 38 6 32 1 22C14 19 25 24 30 36Z"/><path d="M34 36C46 38 58 32 63 22C50 19 39 24 34 36Z"/><path d="M31 35C19 32 13 21 15 8C26 12 31.5 22 31 35Z"/><path d="M33 35C45 32 51 21 49 8C38 12 32.5 22 33 35Z"/><path d="M32 35C23 26 24 12 32 2C40 12 41 26 32 35Z"/></svg>';
    var media = function (name, alt, cls) { return '<div class="media ' + (cls || "") + '"><img src="' + IMG(name) + '" alt="' + alt + '" loading="lazy"></div>'; };
    var btn = function (text, href, kind) { return '<a class="btn btn--' + (kind || "primary") + '" href="' + href + '"><span class="btn__text">' + text + '</span><span class="btn__icon">' + ARROW + "</span></a>"; };
    var head = function (label, title, lede) {
      return '<div class="head' + (lede ? " head--split" : "") + '"><div class="head__title"><span class="label label--dot">' + label + '</span><h2 class="h-xl">' + title + "</h2></div>" +
        (lede ? '<p class="lede">' + lede + "</p>" : "") + "</div>";
    };
    var ticks = function (items, kind) {
      return '<ul class="ticks ticks--' + (kind || "check") + '">' + items.map(function (t) { return '<li><span class="ticks__ic">' + (kind === "cross" ? CROSS : CHECK) + "</span><span>" + t + "</span></li>"; }).join("") + "</ul>";
    };
    var wrap = function (inner, extra) { return '<section class="section' + (extra ? " " + extra : "") + '"><div class="container">' + inner + "</div></section>"; };

    return [
      // ---- Sections
      ["sec-page-hero", "Sections", "Page header with photo", ico('<path d="M4 6h9M4 10h7M4 14h5"/><path d="M15 20V11a3 3 0 0 1 6 0v9z"/>'),
        '<section class="page-hero"><div class="container page-hero__grid"><div class="page-hero__copy"><span class="label label--dot">Page label</span>' +
        '<h1 class="display page-hero__title">A warm, clear<br><em>headline.</em></h1><p class="lede">A short introduction to this page. Click any text to edit it.</p>' +
        '<div class="actions">' + btn("Book your free 30-minute call", "contact.html") + "</div></div>" +
        '<div class="page-hero__visual">' + media("arielle-portrait", "Arielle Innou Nahmias", "arch") + "</div></div></section>"],
      ["sec-heading", "Sections", "Section heading", ico('<path d="M5 6h14M5 11h9"/><path d="M5 17h6"/>'),
        wrap(head("Section label", "Two lines of<br><em>headline.</em>", "A sentence that supports the headline."))],
      ["sec-statement", "Sections", "Big statement", ico('<path d="M4 8h16M4 13h16M4 18h11"/>'),
        '<section class="section section--tight"><div class="container"><div class="statement__kicker"><span class="label label--dot">Label</span></div>' +
        '<p class="statement">A big, confident sentence<span class="inline-img" style="background-image:url(' + IMG("women-joy") + ')"></span> with a little photo set right <em>inside the words.</em></p></div></section>'],
      ["sec-split", "Sections", "Photo + text", ico('<path d="M3 20V11a5 5 0 0 1 10 0v9z"/><path d="M15 8h6M15 12h6M15 16h4"/>'),
        wrap('<div class="split">' + media("arielle-seated", "Describe this photo", "arch split__media") +
        '<div class="split__copy"><span class="label label--dot">Label</span><h2 class="h-xl">Headline with an <em>accent.</em></h2><p class="lede">An introductory sentence.</p>' +
        '<p class="body">Write a paragraph here. Click to edit text, double-click the photo to replace it.</p>' + btn("Book your free 30-minute call", "contact.html") + "</div></div>")],
      ["sec-services", "Sections", "Service cards", ico('<rect x="3" y="5" width="5" height="14" rx="1.5"/><rect x="9.5" y="5" width="5" height="14" rx="1.5"/><rect x="16" y="5" width="5" height="14" rx="1.5"/>'),
        wrap(head("Ways to work together", "Choose your<br><em>next step.</em>") + '<div class="svc-grid">' +
        [["life-relationship-coaching.html", "new-chapter", "Life &amp; Relationship <em>Coaching</em>"], ["corporate-coaching.html", "leaders", "Corporate <em>Coaching</em>"], ["retreats.html", "sisterhood", "Transformative <em>Retreats</em>"]].map(function (s, i) {
          return '<a class="svc-card" href="' + s[0] + '">' + media(s[1], "", "svc-card__media") + '<div class="svc-card__body"><div class="svc-card__top"><span class="svc-card__num">0' + (i + 1) +
            '</span><span class="pill">Who it’s for</span></div><h3 class="h-lg">' + s[2] + '</h3><p>A short description of this service.</p><span class="svc-card__go">Explore ' + ARROW + "</span></div></a>";
        }).join("") + "</div>")],
      ["sec-quote", "Sections", "Testimonial", ico('<path d="M5 9h5v6H5zM14 9h5v6h-5z"/>'),
        wrap('<div class="testimonials__grid"><div class="testimonials__aside"><span class="label label--dot">Kind words</span><h2 class="h-xl">What clients <em>say.</em></h2></div>' +
        '<div class="t-slider"><div class="t-track"><figure class="t-slide"><blockquote><p>“Paste a kind review from a client here.”</p></blockquote>' +
        '<figcaption><span class="t-avatar" aria-hidden="true">A</span><span><strong>Client name</strong><small>Programme</small></span></figcaption></figure></div></div></div>')],
      ["sec-steps", "Sections", "Three steps", ico('<rect x="4" y="4" width="16" height="6" rx="2"/><rect x="4" y="12" width="16" height="8" rx="2"/>'),
        wrap(head("Your path", "Three simple<br><em>steps.</em>") + '<div class="steps">' +
        [["Schedule your complimentary 30-minute call.", "arielle-garden"], ["Create a custom Clarity Plan.", "meditation"], ["Live life on your terms.", "women-joy"]].map(function (s, i) {
          return '<article class="step-card" style="--i:' + i + '"><div class="step-card__text"><div class="step-card__top"><span class="step-card__num">0' + (i + 1) + '</span><span class="label">Step ' + (i + 1) + ' of 3</span></div>' +
            '<div><h3 class="h-lg">' + s[0] + '</h3><p class="body mt-s">Describe this step.</p></div></div>' + media(s[1], "", "step-card__media") + "</article>";
        }).join("") + "</div>", "section--sand")],
      ["sec-pair", "Sections", "Two checklists", ico('<path d="M4 7l2 2 3-3M4 14l2 2 3-3M12 8h8M12 15h8"/>'),
        '<section class="section section--tight"><div class="container pair"><div class="pair__card pair__card--lilac"><span class="label">Left list title</span>' + ticks(["First point", "Second point", "Third point"]) +
        '</div><div class="pair__card pair__card--mint"><span class="label">Right list title</span>' + ticks(["First point", "Second point", "Third point"]) + "</div></div></section>"],
      ["sec-features", "Sections", "Feature grid", ico('<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="3" y="13" width="8" height="8" rx="2"/><rect x="13" y="13" width="8" height="8" rx="2"/>'),
        wrap(head("What’s included", "Everything you<br><em>need.</em>") + '<div class="features">' + [1, 2, 3, 4].map(function () {
          return '<article class="feature"><span class="ficon">' + LOTUS + '</span><h3 class="h-sm">Feature title</h3><p>One or two lines describing it.</p></article>';
        }).join("") + "</div>")],
      ["sec-compare", "Sections", "Before / after", ico('<rect x="3" y="5" width="8" height="14" rx="2"/><rect x="13" y="5" width="8" height="14" rx="2" fill="currentColor" opacity=".25"/>'),
        wrap(head("Your choice", "Or the power<br>of <em>transformation.</em>") +
        '<div class="contrast" data-contrast><div class="contrast__switch" role="tablist"><button type="button" role="tab" aria-selected="false" data-side="cost">Staying the same</button>' +
        '<button type="button" role="tab" aria-selected="true" data-side="power">Transformation</button><span class="contrast__pill" aria-hidden="true"></span></div>' +
        '<div class="contrast__panels" data-active="power"><div class="contrast__panel contrast__panel--cost" data-panel="cost"><span class="contrast__tag">Staying the same</span><h3 class="h-md">If nothing changes:</h3>' + ticks(["A cost of staying the same", "Another cost"], "cross") +
        '</div><div class="contrast__panel contrast__panel--power" data-panel="power"><span class="contrast__tag">Transformation</span><h3 class="h-md">When you say yes:</h3>' + ticks(["A benefit of changing", "Another benefit"]) + "</div></div></div>", "section--sand")],
      ["sec-faq", "Sections", "FAQ", ico('<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .8-1 1.5V14M12 17h.01"/>'),
        wrap('<div class="faq-layout"><div class="faq-layout__aside"><span class="label label--dot">Questions</span><h2 class="h-xl">Good to<br><em>know.</em></h2></div><div class="faq">' +
        [1, 2, 3].map(function () { return '<details class="faq__item"><summary>A common question?<span class="faq__icon" aria-hidden="true"></span></summary><div class="faq__body"><div><p>The answer goes here.</p></div></div></details>'; }).join("") + "</div></div>")],
      ["sec-gallery", "Sections", "Photo grid", ico('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>'),
        wrap('<div class="gallery">' + ["retreat-gardens", "retreat-statue", "retreat-pool", "retreat-chapel", "retreat-firepit", "retreat-path"].map(function (n, i) {
          return '<div class="gallery__item' + (i === 0 ? " gallery__item--wide" : i % 2 ? " gallery__item--tall" : "") + '"><img src="' + IMG(n) + '" alt="Bella Estate Gardens" loading="lazy"></div>';
        }).join("") + "</div>")],
      ["sec-dark", "Sections", "Dark statement", ico('<rect x="2" y="5" width="20" height="14" rx="2" fill="currentColor" opacity=".2"/><path d="M6 11h12M8 14h8"/>'),
        '<section class="section section--plum principle"><div class="container principle__inner"><span class="label label--dot">A small label</span><p class="principle__text">Transformative change<br>begins <em>within.</em></p></div></section>'],
      ["sec-cta", "Sections", "Call to action", ico('<rect x="3" y="6" width="18" height="12" rx="3"/><path d="M8 12h8"/>'),
        '<section class="section"><div class="container"><div class="cta-panel">' + media("women-together", "", "cta-panel__media") + '<div class="cta-panel__body"><span class="label label--dot">It’s your turn</span>' +
        '<h2 class="h-xl">You’ve given so much.<br>It’s time to give <em>to yourself.</em></h2><p class="lede">A supporting sentence.</p><div class="actions">' + btn("Book your free 30-minute call", "contact.html", "light") + "</div></div></div></div></section>"],
      ["sec-marquee", "Sections", "Scrolling words", ico('<path d="M3 12h18M7 8l-4 4 4 4M17 8l4 4-4 4"/>'),
        '<div class="marquee" aria-hidden="true"><div class="marquee__track">' + ["Clarity", "Confidence", "Connection", "Clarity", "Confidence", "Connection"].map(function (w) { return "<span>" + w + "</span>" + LOTUS.replace('class="lotus"', 'class="lotus marquee__mark"'); }).join("") + "</div></div>"],
      // ---- Layout
      ["lay-2", "Layout", "2 columns", ico('<rect x="3" y="4" width="8" height="16" rx="1.5"/><rect x="13" y="4" width="8" height="16" rx="1.5"/>'),
        '<div class="ed-cols ed-cols--2"><div class="stack"><p class="body">Column one. Drag elements in here.</p></div><div class="stack"><p class="body">Column two.</p></div></div>'],
      ["lay-3", "Layout", "3 columns", ico('<rect x="2" y="4" width="6" height="16" rx="1.5"/><rect x="9" y="4" width="6" height="16" rx="1.5"/><rect x="16" y="4" width="6" height="16" rx="1.5"/>'),
        '<div class="ed-cols ed-cols--3"><div class="stack"><p class="body">Column one.</p></div><div class="stack"><p class="body">Column two.</p></div><div class="stack"><p class="body">Column three.</p></div></div>'],
      ["lay-section", "Layout", "Section", ico('<rect x="3" y="5" width="18" height="14" rx="2" stroke-dasharray="3 3"/>'),
        '<section class="section"><div class="container"><p class="body">New section. Drag headings, text, photos and buttons in here.</p></div></section>'],
      ["lay-section-sand", "Layout", "Sand section", ico('<rect x="3" y="5" width="18" height="14" rx="2" fill="currentColor" opacity=".15"/>'),
        '<section class="section section--sand"><div class="container stack"><span class="label label--dot">Small label</span><h2 class="h-xl">Section title</h2><p class="lede">A sentence or two introducing this section.</p></div></section>'],
      ["lay-html", "Layout", "Custom HTML", ico('<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M13.5 5l-3 14"/>'),
        '<div class="custom-html"><p class="body">Custom HTML: select this block and paste your code (a booking widget, a video…) in the panel on the left.</p></div>'],
      ["lay-spacer", "Layout", "Spacer", ico('<path d="M12 4v16M8 8l4-4 4 4M8 16l4 4 4-4"/>'), '<div class="spacer"></div>'],
      ["lay-divider", "Layout", "Divider", ico('<path d="M3 12h18"/>'), '<hr class="divider">'],
      // ---- Elements
      ["el-heading", "Elements", "Heading", ico('<path d="M6 5v14M18 5v14M6 12h12"/>'), '<h2 class="h-lg">A heading with an <em>accent</em></h2>'],
      ["el-text", "Elements", "Paragraph", ico('<path d="M4 7h16M4 12h16M4 17h10"/>'), '<p class="body">Write something here. Select text to make it bold, italic or a link.</p>'],
      ["el-label", "Elements", "Small label", ico('<path d="M4 12h3M10 12h10"/>'), '<span class="label label--dot">Small label</span>'],
      ["el-button", "Elements", "Plum button", ico('<rect x="3" y="8" width="18" height="8" rx="4"/>'), btn("Book your free 30-minute call", "contact.html")],
      ["el-button2", "Elements", "Outline button", ico('<rect x="3" y="8" width="18" height="8" rx="4" stroke-dasharray="2 2"/>'), btn("Learn more", "about.html", "ghost")],
      ["el-link", "Elements", "Text link", ico('<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>'), '<a class="link" href="about.html">Read more ' + ARROW + "</a>"],
      ["el-image", "Elements", "Photo", ico('<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="1.5"/><path d="M3 17l5-4 4 3 3-2 6 4"/>'), media("arielle-garden", "Describe this photo", "rounded")],
      ["el-arch", "Elements", "Arch photo", ico('<path d="M6 20V10a6 6 0 0 1 12 0v10z"/>'), media("arielle-portrait", "Describe this photo", "arch")],
      ["el-videofile", "Elements", "Video file", ico('<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/>'),
        { tagName: "div", classes: ["media", "rounded"], components: [{ type: "video", src: "", autoplay: true, loop: true, controls: false, attributes: { muted: "", playsinline: "", preload: "metadata" } }] }],
      ["el-quote", "Elements", "Quote", ico('<path d="M6 9h4v5H6zM14 9h4v5h-4z"/>'), '<blockquote class="statement" style="font-size:clamp(1.4rem,1rem + 2vw,2.6rem);font-style:italic">“A memorable quote goes here.”</blockquote>'],
      ["el-pill", "Elements", "Pill", ico('<rect x="4" y="9" width="16" height="6" rx="3"/>'), '<span class="pill">Pill text</span>'],
      ["el-list", "Elements", "Checklist", ico('<path d="M4 7l2 2 3-3M4 14l2 2 3-3M12 8h8M12 15h8"/>'), ticks(["First item", "Second item", "Third item"])],
      ["el-lotus", "Elements", "Lotus mark", ico('<path d="M12 19c-3-3-3-8 0-13 3 5 3 10 0 13zM11 19c-4-1-7-4-7-8 3 .5 5.5 3 7 8zM13 19c4-1 7-4 7-8-3 .5-5.5 3-7 8z"/>'),
        LOTUS.replace('class="lotus"', 'class="lotus" style="width:72px;color:var(--accent)"')]
    ];
  }
};
