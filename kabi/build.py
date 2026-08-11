# -*- coding: utf-8 -*-
"""
Generator statycznej strony KABI CHEMIE (kondycjonowanie-wody.pl).
Wczytuje dane SEO z _seo.json + treści sekcji z content.py i renderuje
czyste pliki HTML do katalogu www/. Bez zależności runtime - wynik to
zwykły HTML+CSS, który otworzysz/wyhostujesz gdziekolwiek.

Uruchomienie:  py -X utf8 build.py
"""
import os, re, sys, json, html, shutil
from datetime import date
import content as C
import knowledge_pages

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'www')
DOMAIN = 'https://kondycjonowanie-wody.pl'
ASSET_VERSION = '20260806-mobile-v276'

# Panel redakcyjny (Ctrl+Alt+A) — NARZĘDZIE LOKALNE, domyślnie WYŁĄCZONE.
# Wchodzi do stron tylko przy jawnym KABI_ADMIN=1, więc produkcyjny build
# nie zawiera nawet odwołania do skryptu. Sam panel dodatkowo odmawia
# uruchomienia poza localhost.
ADMIN_PANEL = os.environ.get('KABI_ADMIN') == '1'


def _admin_panel_tag():
    """Znacznik <script> panelu z tokenem opartym o mtime pliku.

    Wspólny ASSET_VERSION zmienia się rzadko, więc po edycji panelu przeglądarka
    serwowała starą wersję z cache. Token z czasu modyfikacji zmienia adres
    dokładnie wtedy, gdy zmienia się plik — i nigdy w produkcji, bo tam
    tego znacznika w ogóle nie ma.
    """
    if not ADMIN_PANEL:
        return ''
    zrodlo = os.path.join(ROOT, 'src', 'assets', 'admin-panel.js')
    token = int(os.path.getmtime(zrodlo)) if os.path.exists(zrodlo) else 0
    return f'\n<script src="/assets/admin-panel.js?v={token}" defer></script>'


ADMIN_PANEL_TAG = _admin_panel_tag()
BUILD_DATE = os.environ.get('KABI_BUILD_DATE') or date.today().isoformat()
CANONICAL_HOST = 'kondycjonowanie-wody.pl'
CANONICAL_SCHEME = 'https'

CORE_EXPERTISE = [
    "kondycjonowanie wody przemysłowej",
    "chemia przemysłowa KCAQUA",
    "uzdatnianie wody dla kotłów parowych",
    "odkamienianie instalacji przemysłowych",
    "ochrona antykorozyjna instalacji",
    "ochrona wież chłodniczych i skraplaczy wyparnych",
    "antyskalanty do membran odwróconej osmozy",
    "analiza wody przemysłowej",
    "audyt techniczny instalacji wodnych",
    "redukcja zużycia wody, energii i ścieków",
]

SERVICE_CATALOG = [
    ("Kondycjonowanie wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/",
     "Dobór programu chemicznego KCAQUA do kotłów parowych, stabilizacja parametrów wody i ograniczenie kamienia."),
    ("Odkamienianie kotłów i instalacji", "/odkamienianie-instalacji/",
     "Kontrolowane usuwanie kamienia z wymienników, rurociągów, kotłów i obiegów przemysłowych."),
    ("Ochrona układów chłodniczych", "/uklady-chlodnicze/",
     "Programy dla wież chłodniczych, skraplaczy wyparnych i obiegów chłodzących: kamień, korozja, biofilm."),
    ("Ochrona membran RO", "/membrany-ro/",
     "Antyskalanty, analiza wody i rekomendacje eksploatacyjne dla systemów odwróconej osmozy."),
    ("Ochrona antykorozyjna i pasywacja", "/ochrona-antykorozyjna/",
     "Inhibitory korozji, pasywacja stali i chemiczne czyszczenie instalacji przemysłowych."),
    ("Audyt techniczny i analiza wody", "/uslugi/",
     "Wizyta inżyniera, badanie parametrów wody, raport ryzyk i rekomendacje dla zakładu."),
]

BLOG_IMAGE_BY_CATEGORY = {
    'Kotły parowe': '/assets/blog/blog-boiler-scale.png',
    'Wieże chłodnicze': '/assets/blog/blog-biofilm-cleaning.png',
    'Korozja': '/assets/blog/blog-corrosion-pipes.png',
    'Parametry wody': '/assets/blog/blog-water-reduction.png',
    'Membrany RO': '/assets/blog/blog-ro-antiscalant.png',
}

BLOG_IMAGE_BY_HREF = {
    '/baza-wiedzy/kamien-kotlowy/': '/assets/blog/blog-boiler-scale.png',
    '/baza-wiedzy/biofilm-w-ukladzie-chlodniczym/': '/assets/blog/blog-biofilm-cleaning.png',
    '/baza-wiedzy/antyskalant-ro/': '/assets/blog/blog-ro-antiscalant.png',
    '/baza-wiedzy/kotly-parowe/': '/assets/blog/blog-boiler-scale.png',
    '/baza-wiedzy/wieze-chlodnicze/': '/assets/blog/blog-cooling-towers.png',
    '/baza-wiedzy/korozja/': '/assets/blog/blog-corrosion-pipes.png',
    '/baza-wiedzy/parametry-wody/': '/assets/blog/blog-water-reduction.png',
    '/baza-wiedzy/membrany-ro/': '/assets/blog/blog-ro-antiscalant.png',
}

PAGE_ART_BY_PATH = {
    '/autor/': '/assets/people/lukasz-kumor.jpg',
    '/baza-wiedzy/korozja/': '/assets/blog/blog-corrosion-pipes.png',
    '/baza-wiedzy/kotly-parowe/': '/assets/blog/blog-boiler-scale.png',
    '/baza-wiedzy/membrany-ro/': '/assets/blog/blog-ro-antiscalant.png',
    '/baza-wiedzy/parametry-wody/': '/assets/blog/blog-water-reduction.png',
    '/baza-wiedzy/kamien-kotlowy/': '/assets/blog/blog-boiler-scale.png',
    '/baza-wiedzy/biofilm-w-ukladzie-chlodniczym/': '/assets/blog/blog-biofilm-cleaning.png',
    '/baza-wiedzy/antyskalant-ro/': '/assets/blog/blog-ro-antiscalant.png',
    '/baza-wiedzy/wieze-chlodnicze/': '/assets/blog/blog-cooling-towers.png',
    '/branze/': '/assets/industries/industry-branches-collage.jpg',
    '/case-study/': '/assets/case/case-fako-boiler-generated.png',
    '/case-study/warsztaty-amoniakalne-2024/': '/assets/case/case-ammonia-workshop-hero.png',
    '/kalkulator-oszczednosci/': '/assets/impact/impact-05-operational-costs.png',
    '/kotly-parowe/ochrona-antykorozyjna/': '/assets/blog/blog-corrosion-pipes.png',
    '/kotly-parowe/odkamienianie/': '/assets/blog/blog-boiler-scale.png',
    '/ochrona-antykorozyjna/chemiczne-czyszczenie/': '/assets/impact/impact-04-installation-protection.png',
    '/ochrona-antykorozyjna/pasywacja-stali/': '/assets/impact/impact-04-installation-protection.png',
    '/polityka-prywatnosci/': '/assets/visuals-v2/hero-privacy-control-v1.webp',
    '/uklady-chlodnicze/ochrona-wiez-chlodniczych/': '/assets/blog/blog-cooling-towers.png',
    '/uklady-chlodnicze/odkamienianie/': '/assets/impact/impact-03-energy-reduction.jpeg',
    '/uklady-chlodnicze/skraplacze-amoniakalne/': '/assets/case/case-skraplacz.png',
    '/uslugi/': '/assets/impact/impact-04-installation-protection.png',
    '/404/': '/assets/impact/impact-01-water-reduction.jpeg',
}

PAGE_ART_FALLBACKS = (
    ('kotly-parowe', '/assets/case/case-kociol-parowy.png'),
    ('uklady-chlodnicze', '/assets/blog/blog-cooling-towers.png'),
    ('membrany-ro', '/assets/blog/blog-ro-antiscalant.png'),
    ('ochrona-antykorozyjna', '/assets/blog/blog-corrosion-pipes.png'),
    ('odkamienianie', '/assets/blog/blog-boiler-scale.png'),
    ('analiza-wody', '/assets/impact/impact-02-effluent-control.jpeg'),
    ('audyt', '/assets/impact/impact-04-installation-protection.png'),
    ('case-study', '/assets/case/case-fako-boiler-generated.png'),
    ('baza-wiedzy', '/assets/blog/blog-water-reduction.png'),
    ('branze', '/assets/industries/industry-branches-collage.jpg'),
)

EXCLUDED_PATHS = {
    '/branze/zaklady-miesne-i-drobiarskie/',
}

# Publiczne podglady techniczne zostaja dostepne pod URL-em, ale nie powinny
# konkurowac w indeksie z gotowymi stronami eksperckimi.
NOINDEX_PATHS = {
    '/404/',
    '/autor/',
    *(f'/baza-wiedzy/artykul-testowy-{index:02d}/' for index in range(1, 21)),
}

# Adresy, które prowadzą do innej strony (ta sama usługa pod inną nazwą).
# Serwer robi 301 (.htaccess), a plik HTML przekierowuje lokalnie i u hostingów bez mod_rewrite.
REDIRECTS = {
    '/uslugi/audyt-techniczny/': '/bezplatna-konsultacja/',
    # Baza wiedzy: artykuły mają płaskie adresy, więc stare zagnieżdżone
    # (z warstwą kategorii w ścieżce) przekierowujemy na nowe.
    # Same kategorie mają z powrotem własne strony — generuje je
    # knowledge_pages.install_knowledge_pages na podstawie tabeli kabi.categories.
    '/baza-wiedzy/kotly-parowe/kamien-kotlowy/': '/baza-wiedzy/kamien-kotlowy/',
    '/baza-wiedzy/wieze-chlodnicze/biofilm-w-ukladzie-chlodniczym/': '/baza-wiedzy/biofilm-w-ukladzie-chlodniczym/',
    '/baza-wiedzy/membrany-ro/antyskalant-ro/': '/baza-wiedzy/antyskalant-ro/',
}

# Kategorie bazy wiedzy, które nie mają ani jednego artykułu, przekierowujemy
# na hub zamiast publikować pustą stronę. Lista wylicza się z danych, więc
# reaguje sama na dodanie i usunięcie artykułu — nie trzeba jej pilnować ręcznie.
REDIRECTS.update(knowledge_pages.empty_category_redirects())

# ---------------------------------------------------------------- utilities
def esc(s):
    return html.escape(str(s or ''), quote=True)

def xml_esc(s):
    return html.escape(str(s or ''), quote=True)

def clean_text(value):
    text = re.sub(r'<[^>]+>', ' ', str(value or ''))
    text = html.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def absolute_url(path):
    if not path:
        return DOMAIN + '/'
    if str(path).startswith(('http://', 'https://')):
        return str(path)
    return DOMAIN + ('' if str(path).startswith('/') else '/') + str(path)

def local_asset_path(src):
    if not src or src.startswith(('http://', 'https://', 'data:')):
        return None
    clean = src.split('?', 1)[0].split('#', 1)[0]
    if not clean.startswith('/assets/'):
        return None
    return os.path.join(OUT, clean.lstrip('/').replace('/', os.sep))

def png_dimensions(data):
    if len(data) >= 24 and data[:8] == b'\x89PNG\r\n\x1a\n':
        return int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')
    return None

def jpeg_dimensions(data):
    if len(data) < 4 or data[:2] != b'\xff\xd8':
        return None
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        i += 2
        if marker in (0xD8, 0xD9):
            continue
        if i + 2 > len(data):
            break
        size = int.from_bytes(data[i:i + 2], 'big')
        if size < 2 or i + size > len(data):
            break
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            if i + 7 <= len(data):
                h = int.from_bytes(data[i + 3:i + 5], 'big')
                w = int.from_bytes(data[i + 5:i + 7], 'big')
                return w, h
        i += size
    return None

def svg_dimensions(text):
    width = re.search(r'\bwidth=["\']([0-9.]+)', text)
    height = re.search(r'\bheight=["\']([0-9.]+)', text)
    if width and height:
        return int(float(width.group(1))), int(float(height.group(1)))
    viewbox = re.search(r'\bviewBox=["\']\s*[-0-9.]+\s+[-0-9.]+\s+([0-9.]+)\s+([0-9.]+)', text)
    if viewbox:
        return int(float(viewbox.group(1))), int(float(viewbox.group(2)))
    return None

def gif_dimensions(data):
    if len(data) >= 10 and data[:6] in (b'GIF87a', b'GIF89a'):
        return int.from_bytes(data[6:8], 'little'), int.from_bytes(data[8:10], 'little')
    return None

def webp_dimensions(data):
    if len(data) < 20 or data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        return None
    offset = 12
    while offset + 8 <= len(data):
        kind = data[offset:offset + 4]
        size = int.from_bytes(data[offset + 4:offset + 8], 'little')
        chunk = data[offset + 8:offset + 8 + size]
        if kind == b'VP8X' and len(chunk) >= 10:
            width = 1 + int.from_bytes(chunk[4:7], 'little')
            height = 1 + int.from_bytes(chunk[7:10], 'little')
            return width, height
        if kind == b'VP8L' and len(chunk) >= 5 and chunk[0] == 0x2f:
            width = 1 + chunk[1] + ((chunk[2] & 0x3f) << 8)
            height = 1 + (chunk[2] >> 6) + (chunk[3] << 2) + ((chunk[4] & 0x0f) << 10)
            return width, height
        if kind == b'VP8 ' and len(chunk) >= 10:
            marker = chunk.find(b'\x9d\x01\x2a')
            if marker >= 0 and marker + 7 <= len(chunk):
                width = int.from_bytes(chunk[marker + 3:marker + 5], 'little') & 0x3fff
                height = int.from_bytes(chunk[marker + 5:marker + 7], 'little') & 0x3fff
                return width, height
        offset += 8 + size + (size % 2)
    return None

IMAGE_DIM_CACHE = {}
def image_dimensions(src):
    fp = local_asset_path(src)
    if not fp:
        return None
    if fp in IMAGE_DIM_CACHE:
        return IMAGE_DIM_CACHE[fp]
    dims = None
    try:
        ext = os.path.splitext(fp)[1].lower()
        with open(fp, 'rb') as f:
            data = f.read() if ext in ('.jpg', '.jpeg') else f.read(65536 if ext == '.webp' else (8192 if ext == '.svg' else 4096))
        if ext == '.png':
            dims = png_dimensions(data)
        elif ext in ('.jpg', '.jpeg'):
            dims = jpeg_dimensions(data)
        elif ext == '.svg':
            dims = svg_dimensions(data.decode('utf-8', errors='ignore'))
        elif ext == '.webp':
            dims = webp_dimensions(data)
        elif ext == '.gif':
            dims = gif_dimensions(data)
    except OSError:
        dims = None
    IMAGE_DIM_CACHE[fp] = dims
    return dims

def image_mime_type(src):
    ext = os.path.splitext(str(src or '').split('?', 1)[0])[1].lower()
    return {
        '.avif': 'image/avif',
        '.gif': 'image/gif',
        '.jpeg': 'image/jpeg',
        '.jpg': 'image/jpeg',
        '.png': 'image/png',
        '.svg': 'image/svg+xml',
        '.webp': 'image/webp',
    }.get(ext)

def parse_attrs(tag):
    return {m.group(1).lower(): m.group(2) for m in re.finditer(r'([:\w-]+)\s*=\s*"([^"]*)"', tag)}

def add_img_attr(tag, name, value):
    if re.search(r'\s' + re.escape(name) + r'\s*=', tag, re.I):
        return tag
    return tag[:-1] + f' {name}="{esc(value)}">'

def set_img_attr(tag, name, value):
    if re.search(r'\s' + re.escape(name) + r'\s*=', tag, re.I):
        return re.sub(r'(\s' + re.escape(name) + r'\s*=\s*")[^"]*(")', r'\1' + esc(value) + r'\2', tag, count=1, flags=re.I)
    return add_img_attr(tag, name, value)

def enhance_media_attributes(htmltext):
    main_pos = htmltext.find('<main')
    first_main_priority_done = False

    def repl(match):
        nonlocal first_main_priority_done
        tag = match.group(0)
        attrs = parse_attrs(tag)
        src = attrs.get('src', '')

        tag = add_img_attr(tag, 'decoding', 'async')

        dims = image_dimensions(src)
        if dims:
            tag = add_img_attr(tag, 'width', str(dims[0]))
            tag = add_img_attr(tag, 'height', str(dims[1]))

        is_main = main_pos >= 0 and match.start() > main_pos
        is_eager = attrs.get('loading') == 'eager'
        if is_main and is_eager and not first_main_priority_done:
            tag = add_img_attr(tag, 'fetchpriority', 'high')
            first_main_priority_done = True
        elif is_main:
            if is_eager:
                tag = set_img_attr(tag, 'loading', 'lazy')
                tag = add_img_attr(tag, 'fetchpriority', 'low')
            elif 'loading' not in attrs and 'hero' not in attrs.get('class', ''):
                tag = add_img_attr(tag, 'loading', 'lazy')

        return tag

    return re.sub(r'<img\b[^>]*>', repl, htmltext)


UI_ARROW_NAMES = {
    '↗': 'up-right',
    '→': 'right',
    '↘': 'down-right',
    '↓': 'down',
}


def enhance_ui_arrows(htmltext):
    """Oznacza glify kierunkowe używane przez stabilizację wyłącznie na mobile."""
    arrow_pattern = re.compile(
        r'<(?P<tag>span|i)(?P<attrs>[^>]*\baria-hidden="true"[^>]*)>'
        r'(?P<glyph>[↗→↘↓])</(?P=tag)>'
    )

    def add_arrow_class(match):
        tag = match.group('tag')
        attrs = match.group('attrs')
        glyph = match.group('glyph')
        arrow_class = f'ui-arrow ui-arrow--{UI_ARROW_NAMES[glyph]}'
        if re.search(r'\bclass="', attrs):
            attrs = re.sub(
                r'\bclass="([^"]*)"',
                lambda item: f'class="{item.group(1)} {arrow_class}"',
                attrs,
                count=1,
            )
        else:
            attrs = f' class="{arrow_class}"{attrs}'
        return f'<{tag}{attrs}>{glyph}</{tag}>'

    return arrow_pattern.sub(add_arrow_class, htmltext)

def org_id():
    return DOMAIN + '/#organization'

def website_id():
    return DOMAIN + '/#website'

def page_id(path):
    return DOMAIN + path + '#webpage'

def article_id(path):
    return DOMAIN + path + '#article'

def service_id(path):
    return DOMAIN + path + '#service'

def breadcrumb_id(path):
    return DOMAIN + path + '#breadcrumb'

def topic_entities(path):
    topics = [
        {"@type": "Thing", "name": "KABI CHEMIE"},
        {"@type": "Thing", "name": "KCAQUA"},
        {"@type": "Thing", "name": "kondycjonowanie wody przemysłowej"},
    ]
    checks = [
        ('kotly-parowe', ["kotły parowe", "woda kotłowa", "kamień kotłowy", "para technologiczna"]),
        ('uklady-chlodnicze', ["wieże chłodnicze", "skraplacze wyparne", "biofilm", "chłodnictwo przemysłowe"]),
        ('membrany-ro', ["membrany RO", "odwrócona osmoza", "antyskalant", "fouling membran"]),
        ('ochrona-antykorozyjna', ["ochrona antykorozyjna", "pasywacja stali", "inhibitory korozji"]),
        ('odkamienianie', ["odkamienianie instalacji", "chemiczne czyszczenie", "usuwanie osadów"]),
        ('analiza-wody', ["analiza wody", "parametry wody", "diagnostyka laboratoryjna"]),
        ('audyt', ["audyt techniczny", "redukcja kosztów mediów", "raport techniczny"]),
        ('case-study', ["case study", "wdrożenie przemysłowe", "oszczędność wody i energii"]),
        ('baza-wiedzy', ["baza wiedzy", "utrzymanie ruchu", "eksploatacja instalacji wodnych"]),
        ('branze', ["branże przemysłowe", "zakłady produkcyjne", "utrzymanie ruchu"]),
    ]
    for needle, names in checks:
        if needle in path:
            topics.extend({"@type": "Thing", "name": name} for name in names)
    seen, unique = set(), []
    for topic in topics:
        name = topic["name"]
        if name not in seen:
            seen.add(name)
            unique.append(topic)
    return unique

def page_kind(path, page):
    if path == '/':
        return 'WebPage'
    if path == '/kontakt/':
        return 'ContactPage'
    if path == '/o-firmie/':
        return 'AboutPage'
    if path == '/baza-wiedzy/':
        return 'CollectionPage'
    if path.startswith('/baza-wiedzy/') and path != '/baza-wiedzy/':
        # /baza-wiedzy/{kategoria}/{wpis}/ -> wpis; /baza-wiedzy/{kategoria}/ -> kategoria
        return 'BlogPosting' if len(path.strip('/').split('/')) == 3 else 'CollectionPage'
    if path.startswith('/baza-wiedzy/'):
        return 'CollectionPage'
    if path.startswith('/case-study/') and path != '/case-study/':
        return 'Article'
    if path in ('/case-study/', '/referencje/'):
        return 'CollectionPage'
    return 'WebPage'

def is_service_page(path):
    service_prefixes = (
        '/kotly-parowe/', '/uklady-chlodnicze/', '/membrany-ro/',
        '/odkamienianie-instalacji/', '/ochrona-antykorozyjna/',
        '/uslugi/', '/bezplatna-konsultacja/', '/kalkulator-oszczednosci/',
    )
    return path == '/uslugi/' or path.startswith(service_prefixes)

def service_category(path):
    if 'kotly-parowe' in path:
        return 'Kotły parowe i woda kotłowa'
    if 'uklady-chlodnicze' in path:
        return 'Układy chłodnicze i skraplacze wyparne'
    if 'membrany-ro' in path:
        return 'Membrany RO i odwrócona osmoza'
    if 'ochrona-antykorozyjna' in path:
        return 'Ochrona antykorozyjna i pasywacja'
    if 'odkamienianie' in path:
        return 'Odkamienianie i chemiczne czyszczenie'
    if 'analiza-wody' in path:
        return 'Analiza wody przemysłowej'
    if 'audyt' in path or 'konsultacja' in path:
        return 'Audyt techniczny i konsultacje'
    if 'serwis' in path:
        return 'Serwis urządzeń uzdatniania wody'
    return 'Kondycjonowanie wody przemysłowej'

def organization_schema():
    offers = []
    for name, href, desc in SERVICE_CATALOG:
        offers.append({
            "@type": "Offer",
            "url": absolute_url(href),
            "itemOffered": {
                "@type": "Service",
                "name": name,
                "description": desc,
                "provider": {"@id": org_id()},
                "areaServed": {"@type": "Country", "name": "Polska"},
                "audience": {"@type": "BusinessAudience", "name": "Zakłady przemysłowe i utrzymanie ruchu"},
            },
        })
    return {
        "@context": "https://schema.org",
        "@type": ["Organization", "ProfessionalService"],
        "@id": org_id(),
        "name": C.SITE['name'],
        "url": DOMAIN + "/",
        "legalName": C.SITE['company'],
        "taxID": C.SITE['nip'],
        "vatID": "PL" + C.SITE['nip'],
        "email": C.SITE['email'],
        "telephone": C.SITE['phone_raw'],
        "foundingDate": "2022",
        "logo": {
            "@type": "ImageObject",
            "url": DOMAIN + "/assets/kabi-logo-old-color.png",
            "width": 456,
            "height": 90,
        },
        "image": DOMAIN + "/assets/og-default.svg",
        "description": C.SITE['tagline'],
        "slogan": "Woda pod kontrolą. Wynik w liczbach.",
        "knowsAbout": CORE_EXPERTISE,
        "areaServed": {"@type": "Country", "name": "Polska"},
        "address": {"@type": "PostalAddress", "postalCode": C.SITE['postal_code'],
                    "addressLocality": C.SITE['city'], "addressRegion": "mazowieckie",
                    "streetAddress": C.SITE['street'],
                    "addressCountry": "PL"},
        "contactPoint": [
            {"@type": "ContactPoint", "contactType": "sales",
             "email": C.SITE['email'], "telephone": C.SITE['phone_raw'],
             "availableLanguage": ["pl"]},
            {"@type": "ContactPoint", "contactType": "Oddział w Toruniu",
             "name": C.SITE['branch']['contact'], "email": C.SITE['branch']['email'],
             "telephone": C.SITE['branch']['phone_raw'], "availableLanguage": ["pl"]},
        ],
        "makesOffer": offers,
    }

def website_schema():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": website_id(),
        "name": C.SITE['name'],
        "url": DOMAIN + "/",
        "inLanguage": ["pl-PL", "en", "de", "ar"],
        "publisher": {"@id": org_id()},
    }

def webpage_schema(path, title, meta, page, image_url):
    kind = page_kind(path, page)
    obj = {
        "@context": "https://schema.org",
        "@type": kind,
        "@id": page_id(path),
        "url": DOMAIN + path,
        "name": clean_text(title),
        "description": clean_text(meta),
        "inLanguage": "pl-PL",
        "isPartOf": {"@id": website_id()},
        "publisher": {"@id": org_id()},
        "about": topic_entities(path),
        "mainContentOfPage": {"@type": "WebPageElement", "cssSelector": "#main"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": image_url},
        "dateModified": BUILD_DATE,
    }
    if path != '/':
        obj["breadcrumb"] = {"@id": breadcrumb_id(path)}
    if kind in ('BlogPosting', 'Article'):
        page_node = {
            "@type": "WebPage",
            "@id": page_id(path),
            "url": DOMAIN + path,
            "name": clean_text(title),
            "description": clean_text(meta),
            "inLanguage": "pl-PL",
            "isPartOf": {"@id": website_id()},
            "publisher": {"@id": org_id()},
            "mainContentOfPage": obj.pop("mainContentOfPage"),
            "primaryImageOfPage": obj.pop("primaryImageOfPage"),
        }
        if "breadcrumb" in obj:
            page_node["breadcrumb"] = obj.pop("breadcrumb")
        obj["@id"] = article_id(path)
        obj.update({
            "headline": clean_text(title),
            "image": image_url,
            "author": {"@id": org_id()},
            "mainEntityOfPage": page_node,
        })
        if path.startswith('/case-study/'):
            obj["articleSection"] = "Case study KABI CHEMIE"
        elif path.startswith('/baza-wiedzy/'):
            obj["articleSection"] = "Baza wiedzy KABI CHEMIE"
    return obj

def service_schema(path, title, meta):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": service_id(path),
        "name": clean_text(title),
        "serviceType": service_category(path),
        "category": "Chemia i technologie kondycjonowania wody przemysłowej",
        "description": clean_text(meta),
        "url": DOMAIN + path,
        "provider": {"@id": org_id()},
        "areaServed": {"@type": "Country", "name": "Polska"},
        "audience": {"@type": "BusinessAudience", "name": "Zakłady przemysłowe, utrzymanie ruchu, energetyka i chłodnictwo"},
        "potentialAction": {"@type": "ContactAction", "target": DOMAIN + "/kontakt/"},
        "termsOfService": DOMAIN + "/warunki-wspolpracy/",
    }

def blog_image_for(item):
    return (item.get('img') or BLOG_IMAGE_BY_CATEGORY.get(item.get('cat', '')) or
            BLOG_IMAGE_BY_HREF.get(item.get('href', ''), '/assets/blog/blog-water-reduction.png'))

def page_art_for(path):
    if path in PAGE_ART_BY_PATH:
        return PAGE_ART_BY_PATH[path]
    for needle, asset in PAGE_ART_FALLBACKS:
        if needle in path:
            return asset
    return '/assets/impact/impact-04-installation-protection.png'

def page_art_caption(path):
    if 'baza-wiedzy' in path:
        return 'praktyczna wiedza dla utrzymania ruchu i technologii'
    if 'case-study' in path:
        return 'wdrożenie KCAQUA pokazane na danych i pracy instalacji'
    if 'kotly-parowe' in path:
        return 'kotły parowe, para technologiczna i stabilna woda kotłowa'
    if 'uklady-chlodnicze' in path:
        return 'skraplacze, wieże chłodnicze i kontrola obiegu'
    if 'ochrona-antykorozyjna' in path:
        return 'ochrona metalu, pasywacja i kontrola korozji'
    if 'uslugi' in path:
        return 'audyt, analiza i serwis prowadzone przez inżyniera'
    return 'kondycjonowanie wody przemysłowej KABI CHEMIE'

def page_kicker(path):
    if 'baza-wiedzy' in path:
        return 'Baza wiedzy · SEO i GEO'
    if 'case-study' in path:
        return 'Case study · wynik w liczbach'
    if 'kotly-parowe' in path:
        return 'Rozwiązania · kotły parowe'
    if 'uklady-chlodnicze' in path:
        return 'Rozwiązania · chłodnictwo'
    if 'membrany-ro' in path:
        return 'Rozwiązania · membrany RO'
    if 'ochrona-antykorozyjna' in path:
        return 'Rozwiązania · antykorozja'
    if 'uslugi' in path:
        return 'Usługi · diagnostyka i serwis'
    if 'branze' in path:
        return 'Branże · przemysł i produkcja'
    return 'KABI CHEMIE · water treatment'

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
    if p in EXCLUDED_PATHS:
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
    og_path = page.get('og_image') or page.get('image') or page_art_for(path)
    og_img = (DOMAIN + og_path) if og_path else DOMAIN + '/assets/og-default.svg'
    og_alt = page_art_caption(path)
    og_dims = image_dimensions(og_path)
    og_type = image_mime_type(og_path)
    og_details = ''
    if og_type:
        og_details += f'<meta property="og:image:type" content="{esc(og_type)}">\n'
    if og_dims:
        og_details += f'<meta property="og:image:width" content="{og_dims[0]}">\n'
        og_details += f'<meta property="og:image:height" content="{og_dims[1]}">\n'
    preload_image = page.get('preload_image')
    jsonld = list(page.get('jsonld', []))
    robots = ('noindex, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1'
              if path in NOINDEX_PATHS else
              'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1')

    # BreadcrumbList
    trail = breadcrumb_trail(path)
    if trail:
        full = trail + [(short_title(path), path)]
        jsonld.append({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "@id": breadcrumb_id(path),
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
<meta name="robots" content="{esc(robots)}">
<meta name="googlebot" content="{esc(robots)}">
<meta name="author" content="{esc(C.SITE['name'])}">
<meta name="publisher" content="{esc(C.SITE['name'])}">
<meta name="application-name" content="{esc(C.SITE['name'])}">
<meta name="geo.region" content="PL-14">
<meta name="geo.placename" content="{esc(C.SITE['city'])}">
<meta name="theme-color" content="#0b3d5c">
<meta property="og:type" content="{esc(og_type)}">
<meta property="og:locale" content="pl_PL">
<meta property="og:site_name" content="{esc(C.SITE['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_img)}">
<meta property="og:image:alt" content="{esc(og_alt)}">
{og_details}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(og_img)}">
<meta name="twitter:image:alt" content="{esc(og_alt)}">
<link rel="alternate" hreflang="pl-PL" href="{esc(canonical)}">
<link rel="alternate" hreflang="en" href="{esc(DOMAIN + '/en' + path)}">
<link rel="alternate" hreflang="de" href="{esc(DOMAIN + '/de' + path)}">
<link rel="alternate" hreflang="ar" href="{esc(DOMAIN + '/ar' + path)}">
<link rel="alternate" hreflang="x-default" href="{esc(canonical)}">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="alternate" type="text/markdown" href="/llms.txt" title="KABI CHEMIE dla agentów AI">
<link rel="preload" href="/assets/style.css?v={ASSET_VERSION}" as="style">
{('<link rel="preload" href="' + esc(preload_image) + '" as="image" fetchpriority="high">') if preload_image else ''}
<link rel="stylesheet" href="/assets/style.css?v={ASSET_VERSION}">
<link rel="stylesheet" href="/assets/solution-pages.css?v={ASSET_VERSION}">
<link rel="stylesheet" href="/assets/company-case-pages.css?v={ASSET_VERSION}">
{ld_html}</head>
<body{(' class="' + page['body_class'] + '"') if page.get('body_class') else ''}>
"""

# ---------------------------------------------------------------- HEADER / NAV
def render_header(path):
    top = path.strip('/').split('/')[0] if path != '/' else ''
    items = ''
    for it in C.NAV:
        href = it['href']
        active = ' aria-current="page"' if (path == href or (href != '/' and path.startswith(href))) else ''
        item_class = it.get('class', '')
        if it.get('children') or it.get('groups'):
            def nav_links(entries):
                return ''.join(
                    f'<li><a href="{c["href"]}"><img class="nav-panel__item-logo" '
                    'src="/assets/logo-mark.png" alt="" aria-hidden="true" decoding="async" width="279" height="276">'
                    f'<span class="nav-panel__link-label">{esc(c["label"])}</span>'
                    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/>'
                    '<path d="m13 6 6 6-6 6"/></svg></a></li>'
                    for c in entries)

            if it.get('groups'):
                sub = '<div class="nav-panel__groups">' + ''.join(
                    '<div class="nav-panel__group">'
                    f'<span class="nav-panel__group-title">{esc(g["title"])}</span>'
                    f'<ul class="nav-panel__links nav-panel__links--stack">{nav_links(g["links"])}</ul>'
                    '</div>'
                    for g in it['groups']) + '</div>'
            else:
                sub = f'<ul class="nav-panel__links">{nav_links(it["children"])}</ul>'
            promo = it.get('promo')
            if promo:
                p_h, p_cta, p_href = promo
            else:
                p_h, p_cta, p_href = ('Mierzalny wynik instalacji z technologią KCAQUA.',
                                      'Umów bezpłatny audyt', '/bezplatna-konsultacja/')
            panel_id = 'nav-panel-' + ''.join(ch.lower() if ch.isalnum() else '-'
                                               for ch in it['label']).strip('-')
            # Panele z grupami mają własne nagłówki kolumn, więc tytuł sekcji jest zbędny.
            head = '' if it.get('groups') else (
                '<div class="nav-panel__services-head">'
                f'<span class="nav-panel__section-title">{esc(it["label"])}</span>'
                '</div>')
            submenu_class = f'has-sub {item_class}'.strip()
            items += (
                f'<li class="{submenu_class}"><a href="{href}"{active} aria-haspopup="true" '
                f'aria-expanded="false" aria-controls="{panel_id}">{esc(it["label"])}'
                '<span class="caret" aria-hidden="true"></span></a>'
                f'<div class="nav-panel" id="{panel_id}">'
                '<div class="nav-panel__main">'
                '<div class="nav-panel__identity">'
                '<div class="nav-panel__lockup" aria-hidden="true">'
                '<img class="nav-panel__lockup-logo" src="/assets/kabi-logo-old-light.png" width="456" height="90" alt="" decoding="async">'
                '</div>'
                '</div>'
                '<div class="nav-panel__services">'
                f'{head}'
                f'{sub}'
                '</div>'
                '</div></div></li>')
        else:
            class_attr = f' class="{item_class}"' if item_class else ''
            label_html = esc(it["label"])
            if item_class == 'nav-calculator-item':
                label_html = (
                    '<svg class="nav-calculator-icon" viewBox="0 0 24 24" aria-hidden="true">'
                    '<rect width="16" height="20" x="4" y="2" rx="2"/>'
                    '<path d="M8 6h8"/><path d="M8 14h.01M12 14h.01M16 14h.01"/>'
                    '<path d="M8 18h.01M12 18h.01M16 18h.01"/></svg>'
                    f'<span>{label_html}</span>'
                )
            items += f'<li{class_attr}><a href="{href}"{active}>{label_html}</a></li>'
    language_switch = f'''<details class="language-switch">
        <summary class="language-switch__summary" aria-label="Wybierz język">
          <svg class="language-switch__icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/></svg>
          <span class="language-switch__code">PL</span>
          <span class="language-switch__caret" aria-hidden="true"></span>
        </summary>
        <ul class="language-switch__menu" aria-label="Dostępne języki">
          <li><a href="{path}" lang="pl" hreflang="pl" aria-current="page"><span>PL</span><strong>Polski</strong></a></li>
          <li><a href="/en{path}" lang="en" hreflang="en"><span>EN</span><strong>English</strong></a></li>
          <li><a href="/de{path}" lang="de" hreflang="de"><span>DE</span><strong>Deutsch</strong></a></li>
          <li><a href="/ar{path}" lang="ar" dir="rtl" hreflang="ar"><span>AR</span><strong>العربية</strong></a></li>
        </ul>
      </details>'''
    return f"""<a class="skip" href="#main">Przejdź do treści</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="KABI CHEMIE - Water Treatment">
      <img class="brand-logo" src="/assets/kabi-logo-old-light.png" width="456" height="90" alt="" aria-hidden="true" decoding="async">
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
      {language_switch}
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
      <span class="fbrand-logo" role="img" aria-label="KABI CHEMIE - Water Treatment">
        <img class="fbrand-logo__image" src="/assets/kabi-logo-old-light.png" width="456" height="90" alt="" aria-hidden="true">
      </span>
      <div class="footer-socials" aria-label="Media społecznościowe">
        <span class="footer-social-icon" role="img" aria-label="LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="6.2" cy="6.3" r="1.65"></circle><path d="M4.7 9.7h3v9.6h-3zM10.4 9.7h2.9V11c.8-1.1 1.9-1.7 3.3-1.7 2.4 0 3.7 1.5 3.7 4.5v5.5h-3v-5.1c0-1.5-.5-2.4-1.8-2.4-1.4 0-2.1 1-2.1 2.8v4.7h-3z"></path></svg></span>
        <span class="footer-social-icon" role="img" aria-label="YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 8.2a2.8 2.8 0 0 0-2-2C17.2 5.7 12 5.7 12 5.7s-5.2 0-7 .5a2.8 2.8 0 0 0-2 2A28 28 0 0 0 2.6 12 28 28 0 0 0 3 15.8a2.8 2.8 0 0 0 2 2c1.8.5 7 .5 7 .5s5.2 0 7-.5a2.8 2.8 0 0 0 2-2 28 28 0 0 0 .4-3.8 28 28 0 0 0-.4-3.8ZM10 15.1V8.9l5.4 3.1z"></path></svg></span>
      </div>
    </div>
    <div class="footer-links">
      {cols}
    </div>
    <div class="footer-offices" aria-label="Dane kontaktowe KABI CHEMIE">
      <address class="footer-location">
        <strong>KABI CHEMIE</strong>
        <span>{esc(s['postal_code'])} {esc(s['city'])}</span>
        <span>{esc(s['street'])}</span>
        <span>NIP: {esc(s['nip'])}</span>
        <a href="tel:{s['phone_raw']}">{esc(s['phone'])}</a>
        <a href="mailto:{s['email']}">{esc(s['email'])}</a>
      </address>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>© 2026 {esc(s['legal'])}. Wszelkie prawa zastrzeżone.</p>
    <p class="footer-credit">Created with passion by <a href="https://www.handybiz.pl/" target="_blank" rel="noopener noreferrer">Handybiz</a>.</p>
  </div>
</footer>
<script src="/assets/main.js?v={ASSET_VERSION}" defer></script>{ADMIN_PANEL_TAG}
</body>
</html>"""


def finalize_homepage_html(htmltext):
    """Naprawia tekst wyłącznie na stronie głównej, bez zmian na podstronach."""
    replacements = {
        'Przejdź do treści': 'Przejdź do treści',
        'KABI CHEMIE — strona główna': 'KABI CHEMIE, strona główna',
        'KABI CHEMIE — Water Treatment': 'KABI CHEMIE Water Treatment',
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
    <source src="{esc(d['video'])}?v={ASSET_VERSION}" type="video/mp4">
  </video>
  <div class="hero-overlay" aria-hidden="true"></div>
  <div class="wrap hero-inner-v">
    <div class="hero-editorial__stage">
      <div class="hero-editorial__brand" aria-label="KABI CHEMIE">
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

    path = d.get('_path', '')
    art = page_art_for(path)
    caption = page_art_caption(path)
    kicker = eyebrow or f'<p class="eyebrow">{esc(page_kicker(path))}</p>'
    return f"""<section class="hero hero-basic" style="--page-art:url('{esc(art)}')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      {kicker}<h1>{h1}</h1>{lead}
      {_ctas(d.get('ctas'))}
      {copy_stats}
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="{esc(art)}" alt="{esc(caption)}" loading="eager" decoding="async" fetchpriority="high">
      <figcaption>{esc(caption)}</figcaption>
    </figure>
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
    <p>{d.get('text','Wpisz firmę i osobę kontaktową, obowiązkowy telefon oraz opcjonalny e-mail. Formularz przygotuje gotową wiadomość do inżyniera.')}</p>
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
  <form class="contact-form contact-form--smart" data-email="{esc(C.SITE['email'])}" novalidate>
    <div class="field field--identity">
      <label for="cf-identity">Firma / imię i nazwisko <span class="field-meta">wymagane</span></label>
      <input id="cf-identity" name="identity" autocomplete="name organization" required placeholder="np. ABC Sp. z o.o. - Jan Kowalski">
      <p class="field-hint">Wpisz nazwę firmy i osobę, do której mamy oddzwonić.</p>
    </div>
      <div class="contact-form__row">
      <div class="field field--phone">
        <label for="cf-phone">Telefon <span class="field-meta">wymagane</span></label>
        <input id="cf-phone" name="phone" type="tel" autocomplete="tel" required placeholder="np. 600 000 000">
      </div>
      <div class="field field--email">
        <label for="cf-email">Adres e-mail <span class="field-meta">opcjonalne</span></label>
        <input id="cf-email" name="email" type="email" autocomplete="email" placeholder="np. biuro@firma.pl">
      </div>
    </div>
    <div class="field field--message">
      <label for="cf-message">Wiadomość <span class="field-meta">opcjonalne</span></label>
      <textarea id="cf-message" name="message" rows="4" aria-describedby="cf-message-hint" placeholder="Napisz krótko, czego dotyczy sprawa lub jaki typ instalacji mamy omówić."></textarea>
      <p id="cf-message-hint" class="field-hint">Możesz dopisać typ instalacji, problem, preferowany termin kontaktu albo dodatkowy kontekst techniczny.</p>
    </div>
    <div class="form-consents" aria-label="Zgody i informacje prawne">
      <label class="form-consent form-consent--required" for="cf-privacy-consent">
        <input id="cf-privacy-consent" name="privacyConsent" type="checkbox" required>
        <span>Zgadzam się na kontakt w sprawie zapytania zgodnie z <a href="/polityka-prywatnosci/">polityką prywatności</a>. <span class="form-consent__tag">wymagane</span></span>
      </label>
    </div>
    <button type="submit" class="btn btn-primary">Wyślij zapytanie</button>
    <p class="form-note" role="status" aria-live="polite" hidden></p>
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
                         'text': 'Bezpłatna konsultacja techniczna z inżynierem KABI CHEMIE.',
                         'button': ('Umów konsultację', '/bezplatna-konsultacja/')})

    # zapewnij H1 w pierwszym hero
    for sec in sections:
        sec.setdefault('_path', path)
        sec.setdefault('_page_title', title)
        if sec['type'] == 'hero' and 'h1' not in sec:
            sec['h1'] = h1
        if sec['type'] == 'faq':
            jsonld.append(faq_schema(sec))

    jsonld += page.get('jsonld', [])

    image_url = absolute_url(page.get('og_image') or page.get('image') or page_art_for(path))
    page_schema = webpage_schema(path, title, meta, page, image_url)
    if is_service_page(path):
        page_schema["mainEntity"] = {"@id": service_id(path)}
    elif path in ('/', '/o-firmie/', '/kontakt/'):
        page_schema["mainEntity"] = {"@id": org_id()}

    # Stały graf wiedzy: kim jest firma, co robi i jak dana podstrona łączy się z ofertą.
    jsonld = [organization_schema(), website_schema(), page_schema] + jsonld
    if is_service_page(path):
        jsonld.append(service_schema(path, title, meta))

    body = ''.join(RENDERERS[s['type']](s) for s in sections)

    has_video = any(s.get('type') == 'hero' and s.get('video') for s in sections)
    body_classes = []
    if has_video:
        body_classes.append('has-video-hero')
    if page.get('body_class'):
        body_classes.append(page['body_class'])
    preload_image = page.get('preload_image')
    if not preload_image and sections and sections[0].get('type') == 'hero' and not sections[0].get('video'):
        preload_image = page_art_for(path)
    pmeta = {'title': title, 'h1': h1, 'meta': meta,
             'jsonld': jsonld, 'og_type': page.get('og_type', 'website'),
             'og_image': page.get('og_image'),
             'preload_image': preload_image,
             'body_class': ' '.join(body_classes)}

    htmltext = (render_head(path, pmeta) + render_header(path)
                + ('' if page.get('no_breadcrumbs') else render_breadcrumbs(path))
                + f'<main id="main">{body}</main>'
                + render_footer())
    htmltext = htmltext.replace(' — ', ', ').replace(' – ', ', ')
    if path == '/':
        htmltext = finalize_homepage_html(htmltext)
    htmltext = enhance_media_attributes(htmltext)
    htmltext = enhance_ui_arrows(htmltext)
    write(path, htmltext)
    return title

def build_redirect_page(path, target):
    """Strona-przekierowanie: meta refresh + canonical na docelowy adres, poza indeksem."""
    label = short_title(target)
    title = f'{label} | {C.SITE["name"]}'
    htmltext = f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="Ta strona została połączona z sekcją {esc(label)}. Przenosimy Cię pod właściwy adres.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{DOMAIN}{target}">
<meta http-equiv="refresh" content="0; url={target}">
<link rel="stylesheet" href="/assets/style.css?v={ASSET_VERSION}">
</head>
<body class="redirect-page">
<main id="main">
  <h1>{esc(label)}</h1>
  <p>Ta usługa jest opisana na stronie <a href="{target}">{esc(label)}</a>. Za chwilę nastąpi przekierowanie.</p>
</main>
<script>window.location.replace({json.dumps(target)});</script>
</body>
</html>
"""
    write(path, htmltext)
    return title


# ---------------------------------------------------------------- SITEMAP / ROBOTS
def sitemap_priority(path):
    if path == '/':
        return '1.0'
    if path in ('/uslugi/', '/kotly-parowe/', '/uklady-chlodnicze/', '/membrany-ro/',
                '/odkamienianie-instalacji/', '/ochrona-antykorozyjna/', '/kontakt/', '/bezplatna-konsultacja/'):
        return '0.9'
    if path.startswith(('/case-study/', '/baza-wiedzy/')):
        return '0.8'
    if path.count('/') <= 2:
        return '0.7'
    return '0.6'

def sitemap_changefreq(path):
    if path == '/':
        return 'weekly'
    if path.startswith('/baza-wiedzy/') or path.startswith('/case-study/'):
        return 'monthly'
    if path in ('/kontakt/', '/polityka-prywatnosci/', '/warunki-wspolpracy/'):
        return 'yearly'
    return 'monthly'

def write_llms(paths):
    key_sections = [
        ("Najważniejsze strony", [
            ("/", "Kim jest KABI CHEMIE i w czym specjalizuje się firma."),
            ("/uslugi/", "Zakres usług: audyt, analiza wody, serwis i dobór programu chemicznego."),
            ("/kotly-parowe/", "Rozwiązania dla kotłów parowych i wody kotłowej."),
            ("/uklady-chlodnicze/", "Rozwiązania dla wież chłodniczych, skraplaczy i obiegów chłodzenia."),
            ("/membrany-ro/", "Ochrona membran RO, antyskalanty i diagnostyka stacji odwróconej osmozy."),
            ("/odkamienianie-instalacji/", "Odkamienianie wymienników, rurociągów i obiegów przemysłowych."),
            ("/ochrona-antykorozyjna/", "Ochrona antykorozyjna, pasywacja i chemiczne czyszczenie instalacji."),
            ("/case-study/", "Realizacje pokazujące efekty wdrożeń KCAQUA."),
            ("/baza-wiedzy/", "Artykuły eksperckie o wodzie przemysłowej, korozji, kamieniu i biofilmie."),
            ("/kontakt/", "Dane kontaktowe i szybka ścieżka rozmowy z inżynierem."),
        ]),
        ("Usługi i technologie", [
            (href, desc) for _, href, desc in SERVICE_CATALOG
        ]),
    ]
    lines = [
        "# KABI CHEMIE",
        "",
        "> KABI CHEMIE to polski producent autorskiej chemii KCAQUA do kondycjonowania wody przemysłowej. Firma pomaga zakładom produkcyjnym ograniczać kamień, korozję, biofilm, zużycie wody, energii i ścieków w kotłach parowych, układach chłodniczych, skraplaczach wyparnych oraz systemach RO.",
        "",
        "KABI CHEMIE pracuje dla przemysłu, utrzymania ruchu, energetyki zakładowej, chłodnictwa przemysłowego, przetwórstwa spożywczego i firm produkcyjnych. Kluczowe korzyści dla klienta to niższe koszty mediów, stabilniejsza praca instalacji, mniej awarii, dłuższe cykle między czyszczeniami i czytelny raport techniczny dla decyzji zakupowej.",
        "",
        "Firma działa w Polsce. Główna lokalizacja: Siedlce, oddział techniczny: Toruń.",
        "",
    ]
    for title, items in key_sections:
        lines.extend([f"## {title}", ""])
        for href, desc in items:
            lines.append(f"- [{short_title(href)}]({absolute_url(href)}): {desc}")
        lines.append("")
    lines.extend([
        "## Obszary specjalizacji",
        "",
        *[f"- {item}" for item in CORE_EXPERTISE],
        "",
        "## Kontakt",
        "",
        f"- Telefon: {C.SITE['phone']}",
        f"- E-mail: {C.SITE['email']}",
        f"- Siedziba: {C.SITE['address']}",
        f"- Oddział w Toruniu: {C.SITE['branch']['contact']}, {C.SITE['branch']['phone']}, {C.SITE['branch']['email']}",
        "",
        "## Pełniejszy indeks",
        "",
        f"- [llms-full.txt]({DOMAIN}/llms-full.txt): pełniejszy indeks podstron z tytułami i opisami.",
        f"- [sitemap.xml]({DOMAIN}/sitemap.xml): komplet adresów URL do indeksowania.",
        "",
    ])
    with open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    full = [
        "# KABI CHEMIE, pełny indeks dla agentów AI",
        "",
        "Poniżej znajduje się lista publicznych podstron serwisu z krótkim opisem semantycznym. Nie zawiera danych poufnych ani wewnętrznych.",
        "",
        "## Wszystkie podstrony",
        "",
    ]
    for p in paths:
        if p == '/404/':
            continue
        page = C.PAGES.get(p, {})
        seo = SEO.get(p, {})
        title = clean_text(seo.get('title') or page.get('title') or short_title(p))
        meta = clean_text(seo.get('meta') or page.get('meta') or '')
        full.append(f"- [{title}]({absolute_url(p)}): {meta}")
    full.extend([
        "",
        "## Firma i oferta w jednym zdaniu",
        "",
        "KABI CHEMIE projektuje, wdraża i serwisuje programy chemiczne KCAQUA dla przemysłowych instalacji wodnych, aby ograniczać kamień, korozję, biofilm oraz koszty wody, energii i ścieków.",
        "",
    ])
    with open(os.path.join(OUT, 'llms-full.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(full))

def write_sitemap(paths):
    urls = ''
    for p in paths:
        if p == '/404/':
            continue
        img = absolute_url(page_art_for(p))
        caption = page_art_caption(p)
        urls += (
            '  <url>\n'
            f'    <loc>{xml_esc(DOMAIN + p)}</loc>\n'
            f'    <lastmod>{xml_esc(BUILD_DATE)}</lastmod>\n'
            f'    <changefreq>{xml_esc(sitemap_changefreq(p))}</changefreq>\n'
            f'    <priority>{xml_esc(sitemap_priority(p))}</priority>\n'
            '    <image:image>\n'
            f'      <image:loc>{xml_esc(img)}</image:loc>\n'
            f'      <image:caption>{xml_esc(caption)}</image:caption>\n'
            '    </image:image>\n'
            '  </url>\n'
        )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemap.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
           .replace('sitemap.org/schemas', 'sitemaps.org/schemas')
           + urls + '</urlset>\n')
    with open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(xml)
    with open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(
            '# KABI CHEMIE, publiczny serwis ofertowy i ekspercki.\n'
            '# Strona ma być widoczna dla wyszukiwarek oraz agentów AI korzystających z publicznie dostępnych treści.\n'
            'User-agent: *\n'
            'Allow: /\n\n'
            'User-agent: Googlebot\n'
            'Allow: /\n\n'
            'User-agent: Googlebot-Image\n'
            'Allow: /\n\n'
            'User-agent: Google-Extended\n'
            'Allow: /\n\n'
            'User-agent: GPTBot\n'
            'Allow: /\n\n'
            'User-agent: OAI-SearchBot\n'
            'Allow: /\n\n'
            'User-agent: ChatGPT-User\n'
            'Allow: /\n\n'
            'User-agent: ClaudeBot\n'
            'Allow: /\n\n'
            'User-agent: PerplexityBot\n'
            'Allow: /\n\n'
            f'Sitemap: {DOMAIN}/sitemap.xml\n'
            f'# AI summary: {DOMAIN}/llms.txt\n'
        )

def write_server_hints():
    redirect_rules = ''.join(
        f'RewriteRule ^{src.strip("/")}/?$ {dst} [R=301,L]\n'
        for src, dst in sorted(REDIRECTS.items())
    )
    htaccess = f"""# KABI CHEMIE, SEO technical layer.
RewriteEngine On

# Canonical host and HTTPS. Keep one indexable version of every URL.
RewriteCond %{{HTTPS}} !=on [OR]
RewriteCond %{{HTTP_HOST}} ^www\\.{CANONICAL_HOST}$ [NC]
RewriteRule ^ {CANONICAL_SCHEME}://{CANONICAL_HOST}%{{REQUEST_URI}} [R=301,L]

# Zduplikowane adresy tej samej usługi.
{redirect_rules}
AddType image/svg+xml .svg
AddType text/plain .txt
AddType application/xml .xml

# Bez tego Apache pokazuje własną stronę błędu zamiast naszej.
ErrorDocument 404 /404.html

# Czyste adresy katalogowe: /kotly-parowe/ → /kotly-parowe/index.html
DirectoryIndex index.html
# Katalogi bez index.html nie mają wystawiać listy plików.
Options -Indexes

<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
  Header set Strict-Transport-Security "max-age=31536000; includeSubDomains"
  Header set Content-Security-Policy "default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self'; form-action 'self' mailto:; img-src 'self' data:; media-src 'self'; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'; upgrade-insecure-requests"

  <FilesMatch "\\.(css|js|png|jpg|jpeg|svg|webp|mp4)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>

  <FilesMatch "\\.(html|xml|txt)$">
    Header set Cache-Control "public, max-age=3600"
  </FilesMatch>
</IfModule>
"""
    with open(os.path.join(OUT, '.htaccess'), 'w', encoding='utf-8') as f:
        f.write(htaccess)

    headers = """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self'; form-action 'self' mailto:; img-src 'self' data:; media-src 'self'; font-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'; upgrade-insecure-requests

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/sitemap.xml
  Content-Type: application/xml; charset=utf-8
  Cache-Control: public, max-age=3600

/robots.txt
  Content-Type: text/plain; charset=utf-8
  Cache-Control: public, max-age=3600

/llms.txt
  Content-Type: text/plain; charset=utf-8
  Cache-Control: public, max-age=3600

/llms-full.txt
  Content-Type: text/plain; charset=utf-8
  Cache-Control: public, max-age=3600
"""
    with open(os.path.join(OUT, '_headers'), 'w', encoding='utf-8') as f:
        f.write(headers)

# ---------------------------------------------------------------- SYNCHRONIZACJA WSPÓLNEGO NAGŁÓWKA
def sync_generated_headers():
    """Aktualizuje nagłówek bez przebudowy treści istniejących podstron."""
    header_pattern = re.compile(
        r'<a class="skip" href="#main">.*?</header>', re.DOTALL)
    asset_pattern = re.compile(
        r'(/assets/(?:style|solution-pages|company-case-pages)\.css|/assets/main\.js)\?v=[^"\']+')
    changed = 0
    redirects = 0

    for directory, _, files in os.walk(OUT):
        for filename in files:
            if filename not in ('index.html', '404.html'):
                continue
            filepath = os.path.join(directory, filename)
            relative = os.path.relpath(filepath, OUT).replace(os.sep, '/')
            if relative == 'index.html':
                path = '/'
            elif relative == '404.html':
                path = '/404/'
            elif relative.endswith('/index.html'):
                path = '/' + relative[:-len('index.html')]
            else:
                continue

            with open(filepath, 'r', encoding='utf-8') as source:
                page_html = source.read()
            page_html, replacements = header_pattern.subn(render_header(path).strip(), page_html, count=1)
            page_html = asset_pattern.sub(lambda match: f'{match.group(1)}?v={ASSET_VERSION}', page_html)
            with open(filepath, 'w', encoding='utf-8', newline='') as target:
                target.write(page_html)
            if replacements == 1:
                changed += 1
            else:
                redirects += 1

    print(f'OK: zaktualizowano nagłówek w {changed} plikach HTML; pominięto {redirects} przekierowań')


# ---------------------------------------------------------------- MAIN
def main():
    # czyszczenie odporne na blokady plików (Windows / otwarty podgląd)
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)
    # assets
    # Skrypt panelu redakcyjnego kopiujemy WYŁĄCZNIE przy KABI_ADMIN=1.
    # Bez tego wykluczenia trafiłby do produkcyjnego www/ mimo że żadna
    # strona go nie ładuje — a wtedy „lokalne narzędzie" byłoby publiczne.
    pomin = (lambda katalog, nazwy: [] if ADMIN_PANEL
             else [n for n in nazwy if n == 'admin-panel.js'])
    shutil.copytree(os.path.join(ROOT, 'src', 'assets'),
                    os.path.join(OUT, 'assets'), dirs_exist_ok=True, ignore=pomin)
    if ADMIN_PANEL:
        print('UWAGA: build z panelem redakcyjnym (KABI_ADMIN=1) — '
              'to wydanie DEWELOPERSKIE, nie wgrywaj go na produkcję.')

    paths = list(SEO.keys())
    # dodatkowe strony zdefiniowane tylko w content (gdyby były)
    for p in C.PAGES:
        if p in EXCLUDED_PATHS:
            continue
        if p not in paths:
            paths.append(p)

    count = 0
    for p in paths:
        if p in REDIRECTS:
            build_redirect_page(p, REDIRECTS[p])
        else:
            build_page(p)
        count += 1

    # 404 -> także kopia w korzeniu (dla hostingów)
    if os.path.exists(out_file('/404/')):
        shutil.copyfile(out_file('/404/'), os.path.join(OUT, '404.html'))

    indexable = [p for p in paths if p not in REDIRECTS and p not in NOINDEX_PATHS]
    write_sitemap(indexable)
    write_llms(indexable)
    write_server_hints()
    print(f'OK: wygenerowano {count} stron -> {OUT}')

if __name__ == '__main__':
    if '--headers-only' in sys.argv:
        sync_generated_headers()
    else:
        main()










