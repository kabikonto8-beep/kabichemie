# -*- coding: utf-8 -*-
"""
Generator statycznej strony Kabi-Chemie (kondycjonowanie-wody.pl).
Wczytuje dane SEO z _seo.json + treści sekcji z content.py i renderuje
czyste pliki HTML do katalogu www/. Bez zależności runtime - wynik to
zwykły HTML+CSS, który otworzysz/wyhostujesz gdziekolwiek.

Uruchomienie:  py -X utf8 build.py
"""
import os, re, json, html, shutil
import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'www')
DOMAIN = 'https://kondycjonowanie-wody.pl'
ASSET_VERSION = '20260622-flat-dark-v124'

BLOG_IMAGE_BY_CATEGORY = {
    'Kotły parowe': '/assets/blog/blog-boiler-scale.png',
    'Wieże chłodnicze': '/assets/blog/blog-biofilm-cleaning.png',
    'Korozja': '/assets/blog/blog-corrosion-pipes.png',
    'Parametry wody': '/assets/blog/blog-water-reduction.png',
    'Membrany RO': '/assets/blog/blog-ro-antiscalant.png',
}

BLOG_IMAGE_BY_HREF = {
    '/baza-wiedzy/pojedynczy-wpis-blogowy-1/': '/assets/blog/blog-boiler-scale.png',
    '/baza-wiedzy/pojedynczy-wpis-blogowy-2/': '/assets/blog/blog-biofilm-cleaning.png',
    '/baza-wiedzy/pojedynczy-wpis-blogowy-3/': '/assets/blog/blog-ro-antiscalant.png',
    '/baza-wiedzy/kotly-parowe/': '/assets/blog/blog-boiler-scale.png',
    '/baza-wiedzy/wieze-chlodnicze/': '/assets/blog/blog-cooling-towers.png',
    '/baza-wiedzy/korozja/': '/assets/blog/blog-corrosion-pipes.png',
    '/baza-wiedzy/parametry-wody/': '/assets/blog/blog-water-reduction.png',
    '/baza-wiedzy/membrany-ro/': '/assets/blog/blog-ro-antiscalant.png',
}

# ---------------------------------------------------------------- utilities
def esc(s):
    return html.escape(str(s or ''), quote=True)

def blog_image_for(item):
    return (item.get('img') or BLOG_IMAGE_BY_CATEGORY.get(item.get('cat', '')) or
            BLOG_IMAGE_BY_HREF.get(item.get('href', ''), '/assets/blog/blog-water-reduction.png'))

def path_of(url):
    """Z pełnego URL -> ścieżka zaczynająca się od / i kończąca / (lub /404/)."""
    p = url.replace(DOMAIN, '')
    if not p.startswith('/'):
        p = '/' + p
    return p

def out_file(path):
    if path == '/':
        return os.path.join(OUT, 'index.html')
    return os.path.join(OUT, path.strip('/'), 'index.html')

def write(path, htmltext):
    fp = out_file(path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(htmltext)

# ---------------------------------------------------------------- SEO data
with open(os.path.join(ROOT, '_seo.json'), encoding='utf-8') as f:
    SEO_RAW = json.load(f)

SEO = {}
for row in SEO_RAW:
    p = path_of(row['url'])
    if '/...' in p:          # pomijamy placeholder "..." z arkusza
        continue
    SEO[p] = row

# krótkie etykiety (nawigacja + breadcrumbs) - z content.SHORT, fallback ze slugu
def short_title(path):
    if path in C.SHORT:
        return C.SHORT[path]
    if path == '/':
        return 'Strona główna'
    seg = path.strip('/').split('/')[-1]
    return seg.replace('-', ' ').capitalize()

def breadcrumb_trail(path):
    """Lista (label, href) przodków: Strona główna + nadrzędne (BEZ bieżącej strony)."""
    if path == '/':
        return []
    trail = [('Strona główna', '/')]
    segs = path.strip('/').split('/')
    acc = ''
    for s in segs[:-1]:          # bez ostatniego segmentu (to bieżąca strona)
        acc += '/' + s
        cur = acc + '/'
        trail.append((short_title(cur), cur))
    return trail

# ---------------------------------------------------------------- HEAD / SEO
def render_head(path, page):
    title = page['title'] or page.get('h1') or C.SITE['name']
    desc = page.get('meta', '')
    canonical = DOMAIN + path
    og_path = page.get('og_image') or page.get('image')
    og_img = (DOMAIN + og_path) if og_path else DOMAIN + '/assets/og-default.svg'
    jsonld = list(page.get('jsonld', []))

    # BreadcrumbList
    trail = breadcrumb_trail(path)
    if trail:
        full = trail + [(short_title(path), path)]
        jsonld.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": lbl,
                 "item": DOMAIN + href} for i, (lbl, href) in enumerate(full)
            ],
        })

    ld_html = ''
    for obj in jsonld:
        ld_html += ('<script type="application/ld+json">'
                    + json.dumps(obj, ensure_ascii=False) + '</script>\n')

    og_type = page.get('og_type', 'website')
    return f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#0b3d5c">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="{esc(C.SITE['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_img)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="stylesheet" href="/assets/style.css?v={ASSET_VERSION}">
{ld_html}</head>
<body{(' class="' + page['body_class'] + '"') if page.get('body_class') else ''}>
"""

# ---------------------------------------------------------------- HEADER / NAV
def render_header(path):
    top = path.strip('/').split('/')[0] if path != '/' else ''
    items = ''
    for it in C.NAV:
        href = it['href']
        active = ' aria-current="page"' if (href != '/' and path.startswith(href)) else ''
        if it.get('children'):
            sub = ''.join(
                f'<li><a href="{c["href"]}"><img class="nav-panel__item-logo" '
                'src="/assets/logo-mark.png" alt="" width="22" height="22" aria-hidden="true">'
                f'<span class="nav-panel__link-label">{esc(c["label"])}</span>'
                '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/>'
                '<path d="m13 6 6 6-6 6"/></svg></a></li>'
                for c in it['children'])
            promo = it.get('promo')
            if promo:
                p_h, p_cta, p_href = promo
            else:
                p_h, p_cta, p_href = ('Mierzalny wynik instalacji z technologią KCAQUA.',
                                      'Umów bezpłatny audyt', '/bezplatna-konsultacja/')
            panel_id = 'nav-panel-' + ''.join(ch.lower() if ch.isalnum() else '-'
                                               for ch in it['label']).strip('-')
            items += (
                f'<li class="has-sub"><a href="{href}"{active} aria-haspopup="true" '
                f'aria-expanded="false" aria-controls="{panel_id}">{esc(it["label"])}'
                '<span class="caret" aria-hidden="true"></span></a>'
                f'<div class="nav-panel" id="{panel_id}">'
                '<div class="nav-panel__main">'
                '<div class="nav-panel__identity">'
                '<div class="nav-panel__lockup" aria-hidden="true">'
                '<img src="/assets/logo-mark.png" alt="" width="52" height="51">'
                '<img src="/assets/logo-word-white.png" alt="" width="149" height="30">'
                '</div>'
                '<div class="nav-panel__identity-copy">'
                '<span>Water Performance System</span>'
                '<strong>Woda pod kontrolą. Wynik w liczbach.</strong>'
                '</div>'
                '</div>'
                '<div class="nav-panel__services">'
                '<div class="nav-panel__services-head">'
                f'<span class="nav-panel__section-title">{esc(it["label"])}</span>'
                '</div>'
                f'<ul class="nav-panel__links">{sub}</ul>'
                '<div class="nav-panel__action">'
                f'<strong class="nav-panel__action-title">{esc(p_h)}</strong>'
                '<span class="nav-panel__action-note">Porozmawiaj z inżynierem KABI-CHEMIE.</span>'
                f'<a class="nav-panel__cta" href="{p_href}">{esc(p_cta)}'
                '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/>'
                '<path d="m13 6 6 6-6 6"/></svg></a>'
                '</div>'
                '</div>'
                '</div></div></li>')
        else:
            items += f'<li><a href="{href}"{active}>{esc(it["label"])}</a></li>'
    return f"""<a class="skip" href="#main">Przejdź do treści</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="Kabichemie — strona główna">
      <img class="brand-mark" src="/assets/logo-mark.png" alt="" width="43" height="42" aria-hidden="true">
      <img class="brand-word brand-word-dark" src="/assets/logo-word.png" alt="Kabichemie — Water Treatment" width="149" height="30">
      <img class="brand-word brand-word-light" src="/assets/logo-word-white.png" alt="" width="149" height="30" aria-hidden="true">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    <nav class="primary" id="primary-nav" aria-label="Menu główne">
      <ul class="menu">{items}</ul>
      <div class="nav-cta">
        <a class="btn btn-primary nav-savings-btn" href="/bezplatna-konsultacja/">
          <span>Umów darmowy audyt</span>
        </a>
      </div>
    </nav>
  </div>
</header>
"""

def render_breadcrumbs(path):
    trail = breadcrumb_trail(path)
    if not trail:
        return ''
    links = ''.join(
        f'<li><a href="{href}">{esc(lbl)}</a></li>' for lbl, href in trail)
    links += f'<li aria-current="page">{esc(short_title(path))}</li>'
    return (f'<nav class="breadcrumbs" aria-label="Okruszki"><div class="wrap">'
            f'<ol>{links}</ol></div></nav>')

# ---------------------------------------------------------------- FOOTER
def render_footer():
    cols = ''
    for col in C.FOOTER:
        links = ''.join(
            f'<li><a href="{l["href"]}">{esc(l["label"])}</a></li>' for l in col['links'])
        cols += f'<div class="fcol"><h3>{esc(col["title"])}</h3><ul>{links}</ul></div>'
    s = C.SITE
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="fcol fbrand">
      <span class="fbrand-logo">
        <img src="/assets/logo-mark.png" alt="" width="38" height="37" aria-hidden="true">
        <img src="/assets/logo-word-white.png" alt="Kabichemie — Water Treatment" width="129" height="26">
      </span>
      <div class="footer-partner">
        <span>Oficjalny Partner w Polsce</span>
        <img src="/assets/weld.png" alt="WELD" width="303" height="71" loading="lazy">
      </div>
      <div class="footer-socials" aria-label="Media społecznościowe">
        <span class="footer-social-icon footer-social-icon--text" role="img" aria-label="LinkedIn"><span aria-hidden="true">in</span></span>
        <span class="footer-social-icon footer-social-icon--text" role="img" aria-label="Facebook"><span aria-hidden="true">f</span></span>
        <span class="footer-social-icon" role="img" aria-label="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6" width="18" height="12" rx="4"></rect><path d="m10 9 5 3-5 3Z"></path></svg></span>
        <span class="footer-social-icon" role="img" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="5"></rect><circle cx="12" cy="12" r="3.5"></circle><circle cx="17.3" cy="6.8" r=".8" class="footer-social-dot"></circle></svg></span>
        <span class="footer-social-icon" role="img" aria-label="X"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4 19 20M19 4 5 20"></path></svg></span>
      </div>
    </div>
    {cols}
    <div class="footer-offices" aria-label="Dane kontaktowe oddziałów">
      <address class="footer-location">
        <strong>Siedziba główna</strong>
        <span class="footer-company">{esc(s['company'])}</span>
        <span>{esc(s['postal_code'])} {esc(s['city'])}</span>
        <span>{esc(s['street'])}</span>
        <span>NIP: {esc(s['nip'])}</span>
        <a href="tel:{s['phone_raw']}">{esc(s['phone'])}</a>
        <a href="mailto:{s['email']}">{esc(s['email'])}</a>
      </address>
      <address class="footer-location">
        <strong>{esc(s['branch']['name'])}</strong>
        <span class="footer-company">{esc(s['branch']['contact'])}</span>
        <a href="tel:{s['branch']['phone_raw']}">{esc(s['branch']['phone'])}</a>
        <a href="mailto:{s['branch']['email']}">{esc(s['branch']['email'])}</a>
      </address>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>© 2026 {esc(s['legal'])}. Wszelkie prawa zastrzeżone.</p>
    <p class="footer-credit">Created with passion by <a href="https://www.handybiz.pl/" target="_blank" rel="noopener noreferrer">Handybiz</a>.</p>
  </div>
</footer>
<script src="/assets/main.js?v={ASSET_VERSION}" defer></script>
</body>
</html>"""


def finalize_homepage_html(htmltext):
    """Naprawia tekst wyłącznie na stronie głównej, bez zmian na podstronach."""
    replacements = {
        'Przejdź do treści': 'Przejdź do treści',
        'Kabichemie — strona główna': 'Kabichemie, strona główna',
        'Kabichemie — Water Treatment': 'Kabichemie Water Treatment',
        'Menu główne': 'Menu główne',
        'Umów darmowy audyt': 'Umów darmowy audyt',
        'KCAQUA · WATER PERFORMANCE SYSTEM': 'KCAQUA · WATER PERFORMANCE SYSTEM',
        'Mierzalne efekty wdrożeń': 'Mierzalne efekty wdrożeń',
        '* potencjał potwierdzamy audytem': '* potencjał potwierdzamy audytem',
        'Media społecznościowe': 'Media społecznościowe',
        'Dane kontaktowe oddziałów': 'Dane kontaktowe oddziałów',
        'Siedziba główna': 'Siedziba główna',
        'Oddział w Toruniu': 'Oddział w Toruniu',
        '©': '©',
        'zastrzeżone': 'zastrzeżone',
        'Evapco — przetwórstwo rybne': 'Evapco: przetwórstwo rybne',
        'konkretny proces — parę, chłód i wodę technologiczną':
            'konkretny proces: parę, chłód i wodę technologiczną',
        'wody kotłowej — mniej kamienia i niższe zużycie pary':
            'wody kotłowej, co oznacza mniej kamienia i niższe zużycie pary',
        'woda technologiczna do mycia — powtarzalna higiena procesu':
            'woda technologiczna do mycia zapewnia powtarzalną higienę procesu',
        'Inhibitory korozji i antyskalanty — stabilna wymiana ciepła':
            'Inhibitory korozji i antyskalanty zapewniają stabilną wymianę ciepła',
        'Mniej wody, energii i ścieków — niższe koszty operacyjne':
            'Mniej wody, energii i ścieków oznacza niższe koszty operacyjne',
        'Zacznij oszczędzać — umów bezpłatny audyt':
            'Zacznij oszczędzać, umów bezpłatny audyt',
        'energii — gotowy do przedstawienia zarządowi':
            'energii. Materiał jest gotowy do przedstawienia zarządowi',
        'Biofilm w układzie chłodniczym — jak go kontrolować?':
            'Biofilm w układzie chłodniczym: jak go kontrolować?',
        'Antyskalant do membran RO — kiedy naprawdę działa?':
            'Antyskalant do membran RO: kiedy naprawdę działa?',
        'Białe certyfikaty i oszczędność energii — od czego zacząć?':
            'Białe certyfikaty i oszczędność energii: od czego zacząć?',
        'Nie wiem — potrzebuję diagnozy': 'Nie wiem, potrzebuję diagnozy',
    }
    for broken, correct in replacements.items():
        htmltext = htmltext.replace(broken, correct)

    # Awaryjne czyszczenie pozostałych pauz użytych jako przerywniki.
    return htmltext.replace(' — ', ', ').replace(' – ', ', ')

# ---------------------------------------------------------------- SECTIONS
CTA_ICONS = {
    'phone': '<svg class="btn-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.4 19.4 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.7.6 2.5a2 2 0 0 1-.4 2.1L8 9.6a16 16 0 0 0 6.4 6.4l1.3-1.3a2 2 0 0 1 2.1-.4c.8.3 1.6.5 2.5.6A2 2 0 0 1 22 16.9z"/><path d="M14 3a7 7 0 0 1 7 7"/><path d="M14 7a3 3 0 0 1 3 3"/></svg>',
    'arrow': '<svg class="btn-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg>',
}

def _btn(cta, kind='btn-primary'):
    if not cta:
        return ''
    label, href = cta[0], cta[1]
    note = cta[2] if len(cta) > 2 else ''
    icon = CTA_ICONS.get(cta[3], '') if len(cta) > 3 else ''
    if note:
        return (f'<a class="btn {kind} btn-tile" href="{href}">'
                f'<span class="btn-copy"><span>{esc(label)}</span><small>{esc(note)}</small></span>{icon}</a>')
    return f'<a class="btn {kind}" href="{href}">{icon}{esc(label)}</a>'

def _ctas(ctas):
    if not ctas:
        return ''
    out = _btn(ctas[0], 'btn-primary')
    for c in ctas[1:]:
        out += _btn(c, 'btn-ghost')
    return f'<div class="cta-row">{out}</div>'

def s_hero(d):
    eyebrow_content = d.get('eyebrow_html') or (esc(d["eyebrow"]) if d.get('eyebrow') else '')
    eyebrow = f'<p class="eyebrow">{eyebrow_content}</p>' if eyebrow_content else ''
    lead = f'<p class="lead">{d["lead"]}</p>' if d.get('lead') else ''
    h1 = d.get('h1_html') or esc(d['h1'])
    stats = ''
    if d.get('stats'):
        items = ''.join(f'<div><strong>{esc(b)}</strong><span>{esc(l)}</span></div>'
                        for b, l in d['stats'])
        stats = f'<div class="hero-stats">{items}</div>'
    copy_stats = stats
    if d.get('video'):
        copy_stats = ''
    copy = f"""<div class="hero-copy">
      {eyebrow}<h1>{h1}</h1>{lead}
      {_ctas(d.get('ctas'))}
      {copy_stats}
    </div>"""

    # wariant z wideo w tle (główny motyw landing page)
    if d.get('video'):
        # opis: odslanianie slowo po slowie (jak czytanie)
        _lead_txt = d.get('lead') or ''
        if _lead_txt and '<' not in _lead_txt:
            _words = esc(_lead_txt).split(' ')
            _inner = ' '.join(f'<span class="hero-word" style="--wd:{i}">{w}</span>'
                              for i, w in enumerate(_words))
            lead_block = f'<p class="lead hero-lead-reveal">{_inner}</p>'
            pill_delay = 0.95 + len(_words) * 0.032 + 0.2
        else:
            lead_block = lead
            pill_delay = 1.5
        # CTA: wjazd z calkowicie lewej, po odsloniciu opisu
        pills = ''
        if d.get('ctas'):
            arrow = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
                     '<path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg>')
            parts = []
            for i, c in enumerate(d['ctas']):
                cls = ('hero-pill hero-pill--solid' if i == 0
                       else 'hero-pill hero-pill--ghost')
                parts.append(f'<a class="{cls}" href="{esc(c[1])}">{esc(c[0])}{arrow}</a>')
            pills = f'<div class="hero-pills" style="--pd:{pill_delay:.2f}s">{"".join(parts)}</div>'
        scroll_cue = ''
        if d.get('scroll_cue'):
            scroll_href = esc(d.get('scroll_href', '#nasze-branze'))
            scroll_label = esc(d.get('scroll_cue'))
            scroll_cue = (
                f'<a class="hero-scroll-cue" href="{scroll_href}" aria-label="{scroll_label}">'
                f'<span>{scroll_label}</span><i aria-hidden="true"></i></a>'
            )
        benefits = [
            'Mniej wody i niższe koszty ścieków',
            'Niższe zużycie energii i paliwa',
            'Mniej osadów, korozji i awarii',
            'Dłuższe cykle między czyszczeniami',
        ]
        benefit_slides = ''.join(
            f'<span class="hero-sentence{" is-active" if i == 0 else ""}">{esc(text)}</span>'
            for i, text in enumerate(benefits)
        )
        return f"""<section class="hero hero-video hero-editorial">
  <video class="hero-bg" autoplay muted loop playsinline preload="auto" aria-hidden="true" tabindex="-1">
    <source src="{esc(d['video'])}" type="video/mp4">
  </video>
  <div class="hero-overlay" aria-hidden="true"></div>
  <div class="wrap hero-inner-v">
    <div class="hero-editorial__stage">
      <div class="hero-editorial__brand" aria-label="Kabi-Chemie">
        <strong>KABI</strong><span>CHEMIE</span>
      </div>
      <div class="hero-editorial__lower">
        <div class="hero-copy hero-editorial__copy">
          <p class="hero-editorial__eyebrow">Technologia KCAQUA · chemia, automatyka i monitoring</p>
          <h1>{esc(d['h1'])}</h1>{lead_block}
          {pills}
        </div>
        <div class="hero-benefit hero-editorial__benefit" data-hero-rotator aria-label="Korzyści technologii KCAQUA">
          <span class="hero-benefit__label">Co zyskuje Twój zakład</span>
          <div class="hero-benefit__slider">{benefit_slides}</div>
        </div>
      </div>
    </div>
  </div>
</section>"""

    return f"""<section class="hero">
  <div class="wrap hero-inner">
    {copy}
    <div class="hero-media" aria-hidden="true">{d.get('media', _hero_svg())}</div>
  </div>
</section>"""

def s_bluf(d):
    return f"""<section class="section bluf reveal"><div class="wrap narrow">
      <p class="bluf-text">{d['text']}</p></div></section>"""

def s_richtext(d):
    inner = ''
    if d.get('title'):
        inner += f'<h2>{esc(d["title"])}</h2>'
    for kind, val in d['blocks']:
        if kind == 'h2':
            inner += f'<h2>{esc(val)}</h2>'
        elif kind == 'h3':
            inner += f'<h3>{esc(val)}</h3>'
        elif kind == 'p':
            inner += f'<p>{val}</p>'
        elif kind == 'ul':
            inner += '<ul>' + ''.join(f'<li>{x}</li>' for x in val) + '</ul>'
        elif kind == 'note':
            inner += f'<p class="note">{val}</p>'
    return f'<section class="section reveal"><div class="wrap narrow prose">{inner}</div></section>'

def s_features(d):
    cards = ''
    for ic, h, desc in d['items']:
        cards += (f'<div class="feature"><div class="ficon">{ic}</div>'
                  f'<h3>{esc(h)}</h3><p>{esc(desc)}</p></div>')
    head = f'<div class="section-head"><h2>{esc(d["title"])}</h2>' + \
           (f'<p>{esc(d["intro"])}</p>' if d.get('intro') else '') + '</div>'
    return f'<section class="section reveal"><div class="wrap">{head}<div class="feature-grid">{cards}</div></div></section>'

def s_steps(d):
    items = ''
    for i, (h, desc) in enumerate(d['items'], 1):
        items += (f'<li><div class="step-num">{i}</div>'
                  f'<div><h3>{esc(h)}</h3><p>{esc(desc)}</p></div></li>')
    head = f'<div class="section-head"><h2>{esc(d["title"])}</h2>' + \
           (f'<p>{esc(d["intro"])}</p>' if d.get('intro') else '') + '</div>'
    return f'<section class="section alt reveal"><div class="wrap">{head}<ol class="steps">{items}</ol></div></section>'

def s_table(d):
    th = ''.join(f'<th>{esc(x)}</th>' for x in d['headers'])
    rows = ''
    for r in d['rows']:
        rows += '<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>'
    head = f'<div class="section-head"><h2>{esc(d["title"])}</h2>' + \
           (f'<p>{esc(d["intro"])}</p>' if d.get('intro') else '') + '</div>'
    note = f'<p class="note">{d["note"]}</p>' if d.get('note') else ''
    return (f'<section class="section reveal"><div class="wrap narrow">{head}'
            f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div>{note}</div></section>')

def s_faq(d):
    items = ''
    for q, a in d['items']:
        items += (f'<details><summary>{esc(q)}</summary><div class="faq-a"><p>{a}</p></div></details>')
    head = f'<div class="section-head"><h2>{esc(d.get("title","Najczęstsze pytania"))}</h2></div>'
    return f'<section class="section alt reveal"><div class="wrap narrow faq">{head}{items}</div></section>'

def faq_schema(d):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}}
            for q, a in d['items']]
    }

def s_cards(d):
    cards = ''
    for it in d['items']:
        cta = f'<span class="card-link">{esc(it.get("cta","Dowiedz się więcej"))} →</span>'
        cards += (f'<a class="card" href="{it["href"]}"><h3>{esc(it["h"])}</h3>'
                  f'<p>{esc(it["desc"])}</p>{cta}</a>')
    head = f'<div class="section-head"><h2>{esc(d["title"])}</h2>' + \
           (f'<p>{esc(d["intro"])}</p>' if d.get('intro') else '') + '</div>'
    return f'<section class="section reveal"><div class="wrap">{head}<div class="card-grid">{cards}</div></div></section>'

def s_cta(d):
    sec = _btn(d['secondary'], 'btn-ghost-light') if d.get('secondary') else ''
    return f"""<section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>{esc(d['title'])}</h2><p>{esc(d.get('text',''))}</p></div>
      <div class="cta-actions">{_btn(d['button'],'btn-primary')}{sec}</div>
    </div></section>"""

def s_logos(d):
    items = ''.join(f'<div class="logo-chip">{esc(x)}</div>' for x in d['items'])
    t = f'<p class="logos-title">{esc(d["title"])}</p>' if d.get('title') else ''
    return f'<section class="section logos reveal"><div class="wrap">{t}<div class="logo-row">{items}</div></div></section>'

def s_stats(d):
    items = ''.join(f'<div><strong>{esc(b)}</strong><span>{esc(l)}</span></div>'
                    for b, l in d['items'])
    return f'<section class="stat-band reveal"><div class="wrap stat-row">{items}</div></section>'

def s_compare(d):
    th = ''.join(f'<th>{esc(x)}</th>' for x in d['headers'])
    rows = ''
    for r in d['rows']:
        cells = ''.join(f'<td>{x}</td>' for x in r)
        rows += f'<tr>{cells}</tr>'
    head = f'<div class="section-head"><h2>{esc(d["title"])}</h2>' + \
           (f'<p>{esc(d["intro"])}</p>' if d.get('intro') else '') + '</div>'
    return (f'<section class="section alt reveal"><div class="wrap narrow">{head}'
            f'<div class="table-wrap compare"><table><thead><tr>{th}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div></div></section>')

def s_related(d):
    items = ''.join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in d['items'])
    return (f'<section class="section related reveal"><div class="wrap">'
            f'<h2>{esc(d.get("title","Powiązane strony"))}</h2>'
            f'<ul class="related-list">{items}</ul></div></section>')

def s_bloglist(d):
    cards = ''
    for it in d['items']:
        cat = f'<span class="post-cat">{esc(it.get("cat",""))}</span>' if it.get('cat') else ''
        img = blog_image_for(it)
        thumb = f'<div class="post-thumb" aria-hidden="true" style="--post-img:url(\'{esc(img)}\')"></div>'
        cards += (f'<a class="post-card" href="{it["href"]}">'
                  f'{thumb}'
                  f'<div class="post-body">{cat}<h3>{esc(it["h"])}</h3>'
                  f'<p>{esc(it.get("desc",""))}</p>'
                  f'<span class="post-meta">{esc(it.get("meta",""))}</span></div></a>')
    head = f'<div class="section-head"><h2>{esc(d["title"])}</h2>' + \
           (f'<p>{esc(d["intro"])}</p>' if d.get('intro') else '') + '</div>'
    return f'<section class="section reveal"><div class="wrap">{head}<div class="post-grid">{cards}</div></div></section>'

def s_author(d):
    return f"""<section class="section reveal"><div class="wrap narrow author">
      <div class="author-avatar" aria-hidden="true">{d.get('initials','KC')}</div>
      <div><h2>{esc(d['name'])}</h2><p class="author-role">{esc(d['role'])}</p>
      <p>{d['bio']}</p></div></div></section>"""

def s_contact(d):
    branch = C.SITE['branch']
    return f"""<section class="section alt reveal"><div class="wrap contact-grid">
  <div class="contact-info">
    <h2>{esc(d.get('title','Skontaktuj się z inżynierem'))}</h2>
    <p>{d.get('text','Napisz, z czym się mierzysz — dobierzemy rozwiązanie do Twojej instalacji.')}</p>
    <div class="contact-locations">
      <div class="contact-location">
        <h3>Siedziba główna</h3>
        <p class="contact-location__name">{esc(C.SITE['company'])}</p>
        <ul class="contact-list">
          <li><span class="ci">☎</span> <a href="tel:{C.SITE['phone_raw']}">{esc(C.SITE['phone'])}</a></li>
          <li><span class="ci">✉</span> <a href="mailto:{C.SITE['email']}">{esc(C.SITE['email'])}</a></li>
          <li><span class="ci">📍</span> {esc(C.SITE['address'])}</li>
          <li><span class="ci">NIP</span> {esc(C.SITE['nip'])}</li>
          <li><span class="ci">🕑</span> Inżynier dostępny pn–pt 7:00–16:00</li>
        </ul>
      </div>
      <div class="contact-location">
        <h3>{esc(branch['name'])}</h3>
        <p class="contact-location__name">{esc(branch['contact'])}</p>
        <ul class="contact-list">
          <li><span class="ci">☎</span> <a href="tel:{branch['phone_raw']}">{esc(branch['phone'])}</a></li>
          <li><span class="ci">✉</span> <a href="mailto:{branch['email']}">{esc(branch['email'])}</a></li>
        </ul>
      </div>
    </div>
  </div>
  <form class="contact-form" data-email="{esc(C.SITE['email'])}" novalidate>
    <div class="field"><label for="cf-name">Imię i nazwisko</label><input id="cf-name" name="name" required></div>
    <div class="field"><label for="cf-company">Firma / Zakład</label><input id="cf-company" name="company"></div>
    <div class="row2">
      <div class="field"><label for="cf-phone">Telefon</label><input id="cf-phone" name="phone" type="tel"></div>
      <div class="field"><label for="cf-email">E-mail</label><input id="cf-email" name="email" type="email" required></div>
    </div>
    <div class="field"><label for="cf-type">Typ instalacji</label>
      <select id="cf-type" name="type">
        <option>Kotły parowe</option><option>Układy chłodnicze</option>
        <option>Membrany RO</option><option>Inne / nie wiem</option>
      </select></div>
    <div class="field"><label for="cf-msg">Opis problemu</label><textarea id="cf-msg" name="message" rows="4"></textarea></div>
    <button type="submit" class="btn btn-primary">Wyślij zapytanie</button>
    <p class="form-note" hidden></p>
  </form>
</div></section>"""

def s_custom(d):
    return d.get('html', '')

RENDERERS = {
    'hero': s_hero, 'bluf': s_bluf, 'richtext': s_richtext, 'features': s_features,
    'steps': s_steps, 'table': s_table, 'faq': s_faq, 'cards': s_cards, 'cta': s_cta,
    'logos': s_logos, 'stats': s_stats, 'compare': s_compare, 'related': s_related,
    'bloglist': s_bloglist, 'author': s_author, 'contact': s_contact, 'custom': s_custom,
}

def _hero_svg():
    return ('<svg viewBox="0 0 480 360" xmlns="http://www.w3.org/2000/svg" role="img">'
            '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#0b3d5c"/><stop offset="1" stop-color="#1789b6"/>'
            '</linearGradient></defs>'
            '<rect width="480" height="360" rx="18" fill="url(#g)"/>'
            '<g fill="none" stroke="#7fd4ef" stroke-width="3" opacity="0.85">'
            '<path d="M60 250 q40 -40 80 0 t80 0 t80 0 t80 0"/>'
            '<path d="M60 210 q40 -40 80 0 t80 0 t80 0 t80 0" opacity="0.6"/>'
            '<path d="M60 290 q40 -40 80 0 t80 0 t80 0 t80 0" opacity="0.4"/></g>'
            '<g fill="#eaf6fb"><circle cx="150" cy="120" r="7"/><circle cx="240" cy="95" r="5"/>'
            '<circle cx="330" cy="130" r="6"/><circle cx="300" cy="80" r="4"/></g>'
            '<text x="240" y="330" fill="#bfe6f3" font-family="sans-serif" font-size="15" '
            'text-anchor="middle">KCAQUA — chemia do kondycjonowania wody</text></svg>')

# ---------------------------------------------------------------- PAGE BUILD
def build_page(path):
    seo = SEO.get(path, {})
    page = C.PAGES.get(path, {})
    # scal SEO + treść
    title = seo.get('title') or page.get('title') or C.SITE['name']
    h1 = page.get('h1') or seo.get('h1') or short_title(path)
    meta = seo.get('meta') or page.get('meta', '')

    sections = page.get('sections')
    jsonld = []
    # auto: jeśli brak zdefiniowanych sekcji - złóż sensowny default
    if not sections:
        sections = [
            {'type': 'hero', 'h1': h1, 'lead': meta,
             'ctas': [('Bezpłatna konsultacja', '/bezplatna-konsultacja/'), ('Kontakt', '/kontakt/')]},
            {'type': 'bluf', 'text': meta},
        ]
        rel = page.get('related')
        if rel:
            sections.append({'type': 'related', 'items': rel})
        sections.append({'type': 'cta', 'title': 'Porozmawiajmy o Twojej instalacji',
                         'text': 'Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie.',
                         'button': ('Umów konsultację', '/bezplatna-konsultacja/')})

    # zapewnij H1 w pierwszym hero
    for sec in sections:
        if sec['type'] == 'hero' and 'h1' not in sec:
            sec['h1'] = h1
        if sec['type'] == 'faq':
            jsonld.append(faq_schema(sec))

    jsonld += page.get('jsonld', [])

    # dane organizacji na stronie głównej
    if path == '/':
        jsonld.append({
            "@context": "https://schema.org", "@type": "Organization",
            "name": C.SITE['name'], "url": DOMAIN + "/",
            "legalName": C.SITE['company'], "taxID": C.SITE['nip'],
            "logo": DOMAIN + "/assets/logo.png",
            "description": C.SITE['tagline'],
            "areaServed": "PL",
            "address": {"@type": "PostalAddress", "postalCode": C.SITE['postal_code'],
                        "addressLocality": C.SITE['city'], "streetAddress": C.SITE['street'],
                        "addressCountry": "PL"},
            "contactPoint": [
                {"@type": "ContactPoint", "contactType": "sales",
                 "email": C.SITE['email'], "telephone": C.SITE['phone_raw']},
                {"@type": "ContactPoint", "contactType": "Oddział w Toruniu",
                 "name": C.SITE['branch']['contact'], "email": C.SITE['branch']['email'],
                 "telephone": C.SITE['branch']['phone_raw']},
            ],
        })
        jsonld.append({
            "@context": "https://schema.org", "@type": "WebSite",
            "name": C.SITE['name'], "url": DOMAIN + "/", "inLanguage": "pl-PL",
        })

    body = ''.join(RENDERERS[s['type']](s) for s in sections)

    has_video = any(s.get('type') == 'hero' and s.get('video') for s in sections)
    pmeta = {'title': title, 'h1': h1, 'meta': meta,
             'jsonld': jsonld, 'og_type': page.get('og_type', 'website'),
             'og_image': page.get('og_image'),
             'body_class': 'has-video-hero' if has_video else ''}

    htmltext = (render_head(path, pmeta) + render_header(path)
                + render_breadcrumbs(path)
                + f'<main id="main">{body}</main>'
                + render_footer())
    if path == '/':
        htmltext = finalize_homepage_html(htmltext)
    write(path, htmltext)
    return title

# ---------------------------------------------------------------- SITEMAP / ROBOTS
def write_sitemap(paths):
    urls = ''
    for p in paths:
        if p == '/404/':
            continue
        urls += f'  <url><loc>{DOMAIN}{p}</loc></url>\n'
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9">\n'
           .replace('sitemap.org/schemas', 'sitemaps.org/schemas')
           + urls + '</urlset>\n')
    with open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(xml)
    with open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write('User-agent: *\nAllow: /\n\nSitemap: ' + DOMAIN + '/sitemap.xml\n')

# ---------------------------------------------------------------- MAIN
def main():
    # czyszczenie odporne na blokady plików (Windows / otwarty podgląd)
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)
    # assets
    shutil.copytree(os.path.join(ROOT, 'src', 'assets'),
                    os.path.join(OUT, 'assets'), dirs_exist_ok=True)

    paths = list(SEO.keys())
    # dodatkowe strony zdefiniowane tylko w content (gdyby były)
    for p in C.PAGES:
        if p not in paths:
            paths.append(p)

    count = 0
    for p in paths:
        build_page(p)
        count += 1

    # 404 -> także kopia w korzeniu (dla hostingów)
    if os.path.exists(out_file('/404/')):
        shutil.copyfile(out_file('/404/'), os.path.join(OUT, '404.html'))

    write_sitemap(paths)
    print(f'OK: wygenerowano {count} stron -> {OUT}')

if __name__ == '__main__':
    main()










