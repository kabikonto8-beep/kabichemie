# -*- coding: utf-8 -*-
"""Walidacja wygenerowanego serwisu: linki wewnętrzne + kompletność SEO."""
import os, re

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

broken, missing_seo = [], []
href_re = re.compile(r'href="(/[^"#]*?)"')
total_links = 0

for url, fp in sorted(PAGES.items()):
    html = open(fp, encoding='utf-8').read()
    # SEO completeness
    for tag, pat in [('title', r'<title>[^<]+</title>'),
                     ('description', r'<meta name="description" content="[^"]+">'),
                     ('canonical', r'<link rel="canonical"'),
                     ('h1', r'<h1>')]:
        if not re.search(pat, html):
            missing_seo.append(f'{url} -> brak {tag}')
    # internal links
    for href in href_re.findall(html):
        if href.startswith('/assets/'):
            continue
        total_links += 1
        norm = href if href.endswith('/') else href + '/'
        if not href.endswith('/') and '.' in href.rsplit('/', 1)[-1]:
            norm = href  # plik z rozszerzeniem
        if norm not in existing and href not in existing:
            broken.append(f'{url}  ->  {href}')

print(f'Stron: {len(PAGES)}')
print(f'Sprawdzonych linków wewnętrznych: {total_links}')
print(f'Zepsutych linków: {len(broken)}')
for b in broken[:40]:
    print('  ✗', b)
print(f'Braki SEO: {len(missing_seo)}')
for m in missing_seo[:40]:
    print('  ✗', m)
# FAQ schema
faq_pages = [u for u, fp in PAGES.items()
             if '"@type": "FAQPage"' in open(fp, encoding='utf-8').read()]
print(f'Stron z FAQPage schema: {len(faq_pages)} -> {faq_pages}')
print('WYNIK:', 'OK ✅' if not broken and not missing_seo else 'WYMAGA POPRAWEK ❌')
