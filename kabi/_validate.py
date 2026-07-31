# -*- coding: utf-8 -*-
"""Walidacja wygenerowanego serwisu: linki, SEO, JSON-LD i pliki crawlerów."""
import os, re, json

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'www')

def page_paths():
    res = {}
    for root, _, files in os.walk(OUT):
        for fn in files:
            if fn == 'index.html':
                fp = os.path.join(root, fn)
                url = '/' + os.path.relpath(root, OUT).replace('\\', '/').strip('.').strip('/')
                url = (url + '/').replace('//', '/')
                res[url] = fp
    return res

PAGES = page_paths()
existing = set(PAGES.keys())
existing.add('/404/')

broken, missing_seo, jsonld_errors = [], [], []
href_re = re.compile(r'href="(/[^"#]*?)"')
jsonld_re = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
img_re = re.compile(r'<img\b[^>]*>', re.I)
attr_re = re.compile(r'([:\w-]+)\s*=\s*"([^"]*)"')
total_links = 0

def attrs(tag):
    return {m.group(1).lower(): m.group(2) for m in attr_re.finditer(tag)}

for url, fp in sorted(PAGES.items()):
    html = open(fp, encoding='utf-8').read()
    # Strony przekierowujące są celowo poza indeksem: sprawdzamy tylko cel przekierowania.
    if 'http-equiv="refresh"' in html and 'noindex' in html:
        target = re.search(r'<link rel="canonical" href="(?:https?://[^/"]+)?(/[^"]*)"', html)
        if not target:
            missing_seo.append(f'{url} -> przekierowanie bez canonical')
        elif target.group(1) not in existing:
            broken.append(f'{url} -> przekierowanie do nieistniejącej strony {target.group(1)}')
        continue
    # SEO completeness
    for tag, pat in [('title', r'<title>[^<]+</title>'),
                     ('description', r'<meta name="description" content="[^"]+">'),
                     ('canonical', r'<link rel="canonical"'),
                     ('h1', r'<h1>')]:
        if not re.search(pat, html):
            missing_seo.append(f'{url} -> brak {tag}')
    if '<meta name="robots" content="index, follow' not in html:
        missing_seo.append(f'{url} -> brak rozszerzonego meta robots')
    if '<script type="application/ld+json">' not in html:
        missing_seo.append(f'{url} -> brak JSON-LD')
    if 'hreflang="pl-PL"' not in html or 'hreflang="x-default"' not in html:
        missing_seo.append(f'{url} -> brak hreflang pl-PL/x-default')
    if 'rel="preload" href="/assets/style.css' not in html:
        missing_seo.append(f'{url} -> brak preload CSS')
    for tag in img_re.findall(html):
        a = attrs(tag)
        if a.get('src', '').startswith('/assets/'):
            for required in ('width', 'height', 'decoding'):
                if required not in a:
                    missing_seo.append(f'{url} -> obraz bez {required}: {a.get("src")}')
            if a.get('loading') == 'eager' and 'fetchpriority' not in a:
                missing_seo.append(f'{url} -> obraz eager bez fetchpriority: {a.get("src")}')
    for i, raw in enumerate(jsonld_re.findall(html), 1):
        try:
            json.loads(raw)
        except json.JSONDecodeError as exc:
            jsonld_errors.append(f'{url} -> JSON-LD #{i}: {exc}')
    # internal links
    for href in href_re.findall(html):
        if href.startswith('/assets/'):
            continue
        total_links += 1
        if '.' in href.rsplit('/', 1)[-1]:
            public_file = os.path.join(OUT, href.lstrip('/').replace('/', os.sep))
            if os.path.exists(public_file):
                continue
        norm = href if href.endswith('/') else href + '/'
        if not href.endswith('/') and '.' in href.rsplit('/', 1)[-1]:
            norm = href  # plik z rozszerzeniem
        if norm not in existing and href not in existing:
            broken.append(f'{url}  ->  {href}')

required_files = ['robots.txt', 'sitemap.xml', 'llms.txt', 'llms-full.txt', '.htaccess', '_headers']
missing_files = [fn for fn in required_files if not os.path.exists(os.path.join(OUT, fn))]
if os.path.exists(os.path.join(OUT, 'sitemap.xml')):
    sitemap = open(os.path.join(OUT, 'sitemap.xml'), encoding='utf-8').read()
    for tag in ('<lastmod>', '<changefreq>', '<priority>', '<image:image>'):
        if tag not in sitemap:
            missing_seo.append(f'sitemap.xml -> brak {tag}')

print(f'Stron: {len(PAGES)}')
print(f'Sprawdzonych linków wewnętrznych: {total_links}')
print(f'Zepsutych linków: {len(broken)}')
for b in broken[:40]:
    print('  ✗', b)
print(f'Braki SEO: {len(missing_seo)}')
for m in missing_seo[:40]:
    print('  ✗', m)
print(f'Błędy JSON-LD: {len(jsonld_errors)}')
for e in jsonld_errors[:40]:
    print('  ✗', e)
# FAQ schema
faq_pages = [u for u, fp in PAGES.items()
             if '"@type": "FAQPage"' in open(fp, encoding='utf-8').read()]
print(f'Stron z FAQPage schema: {len(faq_pages)} -> {faq_pages}')
print(f'Pliki crawlerów: {"OK" if not missing_files else "braki: " + ", ".join(missing_files)}')
print('WYNIK:', 'OK ✅' if not broken and not missing_seo and not jsonld_errors and not missing_files else 'WYMAGA POPRAWEK ❌')
