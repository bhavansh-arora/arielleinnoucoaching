# Arielle Innou Coaching

A hand-built, multi-page website for **Arielle Innou Nahmias**, a certified life and relationship coach in Toronto who also runs corporate coaching programmes and restorative retreats at Bella Estate Gardens.

All copy, testimonials, photos and links come from arielleinnoucoaching.com.

## Pages

| Page | File | Highlights |
| --- | --- | --- |
| Home | `index.html` | Arch portrait hero with a rotating "book a call" badge, scrolling word band, the "Who am I now?" moment, service cards, Meet Arielle, stacking 3-step process, testimonial slider, a before/after switch (cost of staying the same vs transformation) |
| About | `about.html` | Her story told in six chapters (Fez → France → Canada → fashion & real estate → 25 years in healthcare → coaching) that scroll sideways on desktop, five beliefs, who she works with, why people choose her |
| Life & Relationship Coaching | `life-relationship-coaching.html` | Roles that cross themselves out ("mother, wife, daughter…"), what's included, "say yes to you" switch, application link |
| Corporate Coaching | `corporate-coaching.html` | Drifting "High turnover. Low engagement. Missed goals." headline, count-up 300% / 25+ stats, past results, two programmes, ROI, application link |
| Retreats | `retreats.html` | Full-screen photo hero, what's included, a breathing quote, a packed photo grid with a swipeable lightbox, retreat details and registration |
| Contact | `contact.html` | Inquiry form (with "I'm interested in" choices), direct links to the three applications, FAQ |
| 404 | `404.html` | Branded not-found page |

## Look & feel

- **Palette** (from the lotus logo): warm ivory paper, deep plum, purple, lilac and mint. Every colour is a CSS variable at the top of `assets/css/styles.css`.
- **Type:** Fraunces (a soft editorial serif, italics for accent words) and Manrope.
- **Signature details:** arch-shaped photo frames, the lotus drawn as SVG (it draws itself on the intro screen), a fine paper grain, pill buttons with sliding arrows.
- **Motion** (`assets/js/motion.js`, GSAP + ScrollTrigger stored locally): intro screen on the first visit, plum curtain between pages, masked headline reveals, text that lights up word by word as you read, gentle photo parallax centred on faces, pinned sideways story on About, stacking step cards, velocity marquee, magnetic buttons and a custom cursor on mouse/trackpad. Everything turns off under `prefers-reduced-motion`, and no scrolling is hijacked.

## Built for phones and tablets

- Fluid type and spacing (`clamp()`), tested with no sideways scroll from 320px to 1920px.
- Full-screen animated phone menu, a "Book your free call" bar that appears while scrolling on phones, swipeable testimonials, story and lightbox, 44px+ touch targets, 16px form inputs (no iOS zoom).
- Responsive WebP images (800w / 1600w) with set dimensions and colour placeholders, lazy-loaded below the fold.
- SEO: unique titles and descriptions, canonical URLs, share cards for every page (`assets/img/og/`), `ProfessionalService`, `Person`, `Service`, `Event` and `FAQPage` structured data, `sitemap.xml`, `robots.txt`.

## Before going live

1. **Inquiry form:** create a free form at [formspree.io](https://formspree.io), put its ID in `FORMSPREE_ID` in `tools/content.py`, and run the build (or change `YOUR_FORM_ID` in `contact.html`'s form `action` in the editor's code view). Until then the form runs in demo mode: it validates and shows the thank-you message, but nothing is sent.
2. **Applications:** the buttons link to the JotForm forms used on the current site. The current corporate page embeds the same form as the retreat registration (`251906297424058`); swap `APPLY_CORPORATE` in `tools/content.py` if there is a separate corporate form.
3. **Retreat dates:** the current site still says "Summer 2025", so the details card says "Next dates announced soon". Update it in the editor when dates are set.
4. **Domain:** `SITE_URL` in `tools/content.py` (and `origin` in `admin/site-config.js`) sets canonical, share-card and sitemap URLs. It is currently `https://arielleinnoucoaching.codebunny.net`.

## Visual editor (`/admin`)

The same visual editor as our other sites. Open **`/admin/`** on the live site to edit any page without code: click text to type, double-click photos to swap them, drag in ready-made sections (page header, statement, photo + text, service cards, testimonial, three steps, before/after, checklists, features, FAQ, photo grid, call to action…), change colours site-wide, manage photos, check SEO, and publish. Each publish is one GitHub commit, so every version can be restored.

- **First-time setup** (repository owner, once): open `/admin/?setup`, paste a fine-grained GitHub token with **Contents: Read and write** on this repository only, and choose a username and strong password. This creates `admin/auth.json` (the token stored encrypted). After that, people just sign in.
- `/admin/?preview` opens the editor without signing in (publishing disabled).
- Everything specific to this site is in `admin/site-config.js`; the engine files are shared with our other sites.
- Pages mark their editable areas with `<!-- editor:main -->`, `<!-- editor:header -->` and `<!-- editor:footer -->`. Pages saved from the editor become the source of truth: `tools/build.py` skips them unless run with `--force`.

## Editing in code

Layout is in `tools/build.py`; copy and lists (testimonials, steps, beliefs, results, gallery, FAQs, links) are in `tools/content.py`.

```bash
python3 tools/build.py        # regenerate every page
python3 -m http.server 8000   # preview at http://localhost:8000
```

Photos were prepared once with `tools/images.py` (it crops, makes the WebP sizes, the share cards and favicons, and records each photo's size, placeholder colour and focal point in `tools/image-meta.json`).

## Deploying

The site is fully static: GitHub Pages, Netlify, Vercel or Cloudflare Pages all work with no configuration. Pretty URLs (`/about`) are used for canonical links; GitHub Pages and Netlify serve `about.html` for them automatically.
