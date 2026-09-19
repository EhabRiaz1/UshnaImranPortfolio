#!/usr/bin/env python3
"""Emit index.html. Keeps the 48-tile social grid in markup (works without JS)."""
import json, os
ROOT='/Users/ehabriaz/Desktop/uWebsite'
BLURB = "I’m Ushna, part architect, part storyteller, and a full-time creative designer. My work spans brand, strategy,"
LONG  = ("I’m Ushna, part architect, part storyteller, and a full-time creative designer. "
         "My work spans brand, strategy, and narrative-driven design across multiple mediums, "
         "exploring how ideas take shape across space, structure, and story.")

BRANDING=[('lark','Lark Creatives','brand-lark'),
          ('quiksnap','QuikSnap','brand-quiksnap'),
          ('zayriba','Zayriba','brand-zayriba')]
UIUX=[('squint-cognition','Squint Cognition'),('aaron-rodricks','Aaron Rodricks'),('frame','Frame'),
      ('rend-stephan','Rend Stephan'),('atoofy','Atoofy (concept)'),('animal-conservatory','Animal Conservatory'),
      ('syncquik','SyncQuik'),('keke','KEKE (concept)'),('cio1','CIO1')]
# case-study frames that actually exist in Figma
HAS_CASE={'lark','quiksnap','zayriba','aaron-rodricks','frame','rend-stephan','animal-conservatory','keke','cio1'}
ANIM=[('reimagined-music-cover','Reimagined Music Cover'),
      ('bashir-mirza','Bashir Mirza'),
      ('magnetic-marketing','Magnetic Marketing')]

def tile(slug,label,img,cls='tile'):
    link = slug in HAS_CASE
    tag  = 'button' if link else 'div'
    attr = (f' type="button" class="tile tile--link" data-case="{slug}"'
            f' aria-haspopup="dialog"' if link else ' class="tile tile--static"')
    return (f'        <{tag}{attr}>\n'
            f'          <span class="tile__art"><img src="assets/img/{img}.webp" alt="{label}" loading="lazy" width="694" height="476"></span>\n'
            f'          <span class="tile__label">{label}</span>\n'
            f'        </{tag}>')

def anim_tile(slug,label):
    return (f'        <div class="tile tile--static">\n'
            f'          <span class="tile__art"><span class="anim__media" data-hover-video>\n'
            f'            <img src="assets/video/{slug}-poster.jpg" alt="{label}" loading="lazy" width="720" height="494">\n'
            f'            <video muted loop playsinline preload="none" width="720" height="494">\n'
            f'              <source src="assets/video/{slug}.webm" type="video/webm">\n'
            f'              <source src="assets/video/{slug}.mp4" type="video/mp4">\n'
            f'            </video>\n'
            f'          </span></span>\n'
            f'          <span class="tile__label">{label}</span>\n'
            f'        </div>')

def ver(rel):
    """?v=<mtime> so a deploy can never serve a stale css/js from cache."""
    try: return f'{rel}?v={int(os.path.getmtime(f"{ROOT}/{rel}"))}'
    except OSError: return rel

n_social = len([f for f in os.listdir(f'{ROOT}/assets/img') if f.startswith('social-')])
social = '\n'.join(
    f'            <figure class="social__item"><img src="assets/img/social-{i:02d}.webp" '
    f'alt="Social media design {i}" loading="lazy" width="694" height="756"></figure>'
    for i in range(1, n_social+1))

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ushna Imran — Crafting Ideas That Matter</title>
<meta name="description" content="Ushna Imran — creative designer working across branding, UI/UX, social media and 2d animation.">
<meta property="og:title" content="Ushna Imran — Crafting Ideas That Matter">
<meta property="og:description" content="Creative designer working across branding, UI/UX, social media and 2d animation.">
<meta property="og:type" content="website">
<link rel="preload" href="assets/fonts/Satoshi-Black.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/Satoshi-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{ver('css/style.css')}">
</head>
<body>

<header class="nav">
  <div class="wrap nav__in">
    <a class="nav__logo" href="#top">Ushna Imran</a>
    <nav class="nav__links" aria-label="Primary">
      <a href="#branding">Portfolio</a>
      <a href="https://www.linkedin.com/" target="_blank" rel="noopener">LinkedIn</a>
      <a href="mailto:hello@example.com">Email</a>
    </nav>
  </div>
</header>

<main id="top">

  <section class="hero">
    <h1 class="hero__title">
      <img class="hero__rose" src="assets/img/hero-rose.webp" alt="" width="344" height="264">
      Crafting ideas that matter
    </h1>
    <img class="hero__art" src="assets/img/hero-illustration.webp" alt="Illustration of a figure standing before a row of robed figures" width="1539" height="1455">
    <nav class="hero__jump" aria-label="Sections">
      <a href="#branding" data-jump="branding">Branding</a>
      <span class="hero__dot" aria-hidden="true"></span>
      <a href="#uiux" data-jump="uiux">UI/UX Design</a>
      <span class="hero__dot" aria-hidden="true"></span>
      <a href="#social" data-jump="social">Social Media</a>
      <span class="hero__dot" aria-hidden="true"></span>
      <a href="#animation" data-jump="animation">(2d) Animation</a>
    </nav>
  </section>

  <div class="band band--plain">
    <p class="band__text">{LONG}</p>
  </div>

  <section class="sec" id="branding">
    <div class="wrap">
      <div class="sec__head">
        <h2 class="sec__title">Branding</h2>
        <p class="sec__blurb">{BLURB}</p>
      </div>
      <div class="grid">
{chr(10).join(tile(s,l,i) for s,l,i in BRANDING)}
      </div>
    </div>
  </section>

  <div class="band">
    <img class="band__art" src="assets/img/break-2.webp" alt="" width="2880" height="486">
    <p class="band__text">{LONG}</p>
  </div>

  <section class="sec" id="uiux">
    <div class="wrap">
      <div class="sec__head">
        <h2 class="sec__title">UI/UX</h2>
        <p class="sec__blurb">{BLURB}</p>
      </div>
      <div class="grid">
{chr(10).join(tile(s,l,'uiux-'+s) for s,l in UIUX)}
      </div>
    </div>
  </section>

  <section class="social" id="social">
    <div class="wrap">
      <div class="social__head">
        <img class="social__rose" src="assets/img/hero-rose.webp" alt="" width="344" height="264">
        <h2 class="social__title">Social Media</h2>
      </div>
      <p class="social__blurb">{BLURB}</p>
      <div class="social__gridwrap" id="socialWrap">
        <div class="social__grid" id="socialGrid">
{social}
        </div>
        <div class="social__fade" aria-hidden="true"></div>
      </div>
      <button class="social__toggle" id="socialToggle" type="button" aria-expanded="false" aria-controls="socialGrid">
        <span data-label>View all {n_social}</span>
        <svg width="13" height="8" viewBox="0 0 13 8" fill="none" aria-hidden="true"><path d="M1 1l5.5 5.5L12 1" stroke="currentColor" stroke-width="1.5"/></svg>
      </button>
    </div>
  </section>

  <section class="sec" id="animation">
    <div class="wrap">
      <div class="sec__head">
        <h2 class="sec__title">Animation</h2>
        <p class="sec__blurb">{BLURB}</p>
      </div>

      <figure class="aliph" data-autoplay-video>
        <img src="assets/video/aliph-poster.jpg" alt="Aliph animation" width="1440" height="720">
        <video muted loop playsinline preload="none" width="1440" height="720">
          <source src="assets/video/aliph.webm" type="video/webm">
          <source src="assets/video/aliph.mp4" type="video/mp4">
        </video>
      </figure>
      <p class="tile__label">Aliph</p>

      <div class="grid anim-grid">
{chr(10).join(anim_tile(s,l) for s,l in ANIM)}
      </div>

      <div class="covers">
        <p class="covers__label">Covers</p>
        <div class="covers__row">
          <img src="assets/img/cover-1.webp" alt="World Rhino Day cover" loading="lazy" width="616" height="872">
          <img src="assets/img/cover-2.webp" alt="Thailand cover" loading="lazy" width="616" height="872">
          <img src="assets/img/cover-3.webp" alt="World Rhino Day cover" loading="lazy" width="616" height="872">
          <img src="assets/img/cover-4.webp" alt="Build your brand cover" loading="lazy" width="616" height="872">
        </div>
      </div>
    </div>
  </section>

</main>

<footer class="foot">
  <div class="wrap">
    <div class="foot__links">
      <a href="#top">//Ushna Imran//</a>
      <a href="tel:+10000000000">+1 000 000 0000</a>
      <a href="mailto:hello@example.com">Email</a>
      <a href="https://www.linkedin.com/" target="_blank" rel="noopener">LinkedIn</a>
    </div>
    <p class="foot__big">Let’s Connect</p>
  </div>
</footer>

<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle" hidden>
  <div class="modal__scrim" data-close></div>
  <div class="modal__panel" id="modalPanel">
    <div class="modal__bar">
      <span id="modalTitle">Case study</span>
      <button class="modal__close" type="button" data-close>Close</button>
    </div>
    <div class="modal__body" id="modalBody"></div>
    <p class="modal__end">Scroll to close</p>
  </div>
</div>

<script src="{ver('js/main.js')}"></script>
</body>
</html>
'''
open(f'{ROOT}/index.html','w').write(HTML)
print(f'index.html written — {n_social} social tiles, {len(HAS_CASE)} clickable case studies')
