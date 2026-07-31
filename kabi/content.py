# -*- coding: utf-8 -*-
"""
Treść i konfiguracja serwisu Kabi-Chemie.
Dane SEO (title/meta/h1/breadcrumbs) pochodzą z _seo.json (arkusz „Optymalizacja”).
Tu definiujemy: SITE, NAV, FOOTER, SHORT (etykiety okruszków) oraz PAGES (sekcje).
"""

from solution_pages import install_solution_pages
from company_case_pages import install_company_case_pages
from knowledge_pages import install_knowledge_pages

# ------------------------------------------------------------------ globalne
SITE = {
    "name": "Kabi-Chemie",
    "legal": "Kabi-Chemie",
    "company": "Kabi-Chemie",
    "tagline": "Producent autorskiej chemii KCAQUA do kondycjonowania wody w przemyśle. Mniej kamienia, mniejsze zużycie wody i energii, ochrona instalacji.",
    "phone": "+48 662 792 875",
    "phone_raw": "+48662792875",
    "email": "info@kondycjonowanie-wody.pl",
    "postal_code": "08-110",
    "city": "Siedlce",
    "street": "Żabokliki-Kolonia ul. Stocka 10",
    "address": "Żabokliki-Kolonia ul. Stocka 10, 08-110 Siedlce",
    "nip": "8212519774",
    "branch": {
        "name": "Oddział w Toruniu",
        "contact": "Przemysław Jesiołkowski",
        "phone": "+48 669 060 022",
        "phone_raw": "+48669060022",
        "email": "PJ@kondycjonowanie-wody.pl",
    },
}

# ------------------------------------------------------------------ ikony (inline SVG, currentColor)
def _ic(p):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + p + '</svg>')

ICON = {
    "flame": _ic('<path d="M12 3c2 3 5 4.5 5 8a5 5 0 0 1-10 0c0-1.5.7-2.7 1.5-3.5C9 9 9.5 7 9 5c2 .5 2.5 1.5 3 2 .3-1.2.2-2.7 0-4Z"/>'),
    "snow": _ic('<path d="M12 2v20M4 6l16 12M20 6 4 18"/><path d="M12 5 9.5 7M12 5l2.5 2M12 19l-2.5-2M12 19l2.5-2"/>'),
    "membrane": _ic('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16M15 4v16M3 9h18M3 15h18"/>'),
    "shield": _ic('<path d="M12 3 5 6v5c0 4 3 7 7 8 4-1 7-4 7-8V6l-7-3Z"/><path d="m9 12 2 2 4-4"/>'),
    "gear": _ic('<circle cx="12" cy="12" r="3.2"/><path d="M19 12a7 7 0 0 0-.1-1.3l2-1.5-2-3.4-2.3 1a7 7 0 0 0-2.3-1.3L13.8 1h-3.6l-.3 2.2a7 7 0 0 0-2.3 1.3l-2.3-1-2 3.4 2 1.5A7 7 0 0 0 5 12c0 .5 0 .9.1 1.3l-2 1.5 2 3.4 2.3-1a7 7 0 0 0 2.3 1.3l.3 2.2h3.6l.3-2.2a7 7 0 0 0 2.3-1.3l2.3 1 2-3.4-2-1.5c.1-.4.1-.8.1-1.3Z"/>'),
    "flask": _ic('<path d="M9 3h6M10 3v6l-5 8a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-8V3"/><path d="M7.5 14h9"/>'),
    "drop": _ic('<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/>'),
    "chart": _ic('<path d="M4 20h16M7 20V10M12 20V5M17 20v-7"/>'),
    "wrench": _ic('<path d="M21 4a5 5 0 0 1-6.5 6.5L6 19a2.1 2.1 0 0 1-3-3l8.5-8.5A5 5 0 0 1 18 3l-3 3 3 3 3-3Z"/>'),
    "doc": _ic('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>'),
    "leaf": _ic('<path d="M5 19c0-8 6-13 14-14 .5 8-4 14-12 14-1 0-2 0-2-3Z"/><path d="M9 15c2-2 4-3 7-4"/>'),
    "factory": _ic('<path d="M3 21h18V10l-6 4V10l-6 4V6H3Z"/><path d="M7 21v-4M11 21v-4M15 21v-4"/>'),
    "check": _ic('<path d="m5 12 4 4L19 7"/>'),
    "bolt": _ic('<path d="M13 2 4 14h7l-1 8 9-12h-7Z"/>'),
    "phone": _ic('<path d="M5 4h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/>'),
}

# ------------------------------------------------------------------ nawigacja
NAV = [
    {"label": "Kotły parowe", "href": "/kotly-parowe/", "children": [
        {"label": "Kondycjonowanie wody kotłowej", "href": "/kotly-parowe/kondycjonowanie-wody-kotlowej/"},
        {"label": "Odkamienianie kotłów", "href": "/kotly-parowe/odkamienianie/"},
        {"label": "Ochrona antykorozyjna", "href": "/kotly-parowe/ochrona-antykorozyjna/"},
    ]},
    {"label": "Układy chłodnicze", "href": "/uklady-chlodnicze/", "children": [
        {"label": "Ochrona wież chłodniczych", "href": "/uklady-chlodnicze/ochrona-wiez-chlodniczych/"},
        {"label": "Odkamienianie układów", "href": "/uklady-chlodnicze/odkamienianie/"},
        {"label": "Skraplacze amoniakalne", "href": "/uklady-chlodnicze/skraplacze-amoniakalne/"},
    ]},
    {"label": "Membrany RO", "href": "/membrany-ro/"},
    {"label": "Antykorozja", "href": "/ochrona-antykorozyjna/", "children": [
        {"label": "Pasywacja stali", "href": "/ochrona-antykorozyjna/pasywacja-stali/"},
        {"label": "Chemiczne czyszczenie", "href": "/ochrona-antykorozyjna/chemiczne-czyszczenie/"},
        {"label": "Odkamienianie instalacji", "href": "/odkamienianie-instalacji/"},
    ]},
    {"label": "Usługi", "href": "/uslugi/", "children": [
        {"label": "Audyt techniczny", "href": "/bezplatna-konsultacja/"},
        {"label": "Analiza wody", "href": "/uslugi/analiza-wody/"},
        {"label": "Serwis urządzeń", "href": "/uslugi/serwis-urzadzen/"},
    ]},
    {"label": "Baza wiedzy", "href": "/baza-wiedzy/", "children": [
        {"label": "Kotły parowe i para", "href": "/baza-wiedzy/kotly-parowe/"},
        {"label": "Wieże chłodnicze", "href": "/baza-wiedzy/wieze-chlodnicze/"},
        {"label": "Korozja i ochrona", "href": "/baza-wiedzy/korozja/"},
        {"label": "Parametry wody", "href": "/baza-wiedzy/parametry-wody/"},
        {"label": "Membrany RO", "href": "/baza-wiedzy/membrany-ro/"},
    ]},
    {"label": "O firmie", "href": "/o-firmie/", "children": [
        {"label": "Branże", "href": "/branze/"},
        {"label": "Case studies", "href": "/case-study/"},
        {"label": "Referencje", "href": "/referencje/"},
        {"label": "FAQ", "href": "/faq/"},
        {"label": "Kontakt", "href": "/kontakt/"},
    ]},
]

FOOTER = [
    {"title": "Oferta", "links": [
        {"label": "Kotły parowe", "href": "/kotly-parowe/"},
        {"label": "Skraplacze wyparne", "href": "/uklady-chlodnicze/"},
        {"label": "Autoklawy i pasteryzatory", "href": "/autoklawy-i-pasteryzatory/"},
        {"label": "Technologia KCAQUA", "href": "/kotly-parowe/kondycjonowanie-wody-kotlowej/"},
        {"label": "Ochrona membran RO", "href": "/membrany-ro/"},
        {"label": "Odkamienianie instalacji", "href": "/odkamienianie-instalacji/"},
        {"label": "Ochrona antykorozyjna", "href": "/ochrona-antykorozyjna/"},
    ]},
    {"title": "Usługi", "links": [
        {"label": "Audyt techniczny", "href": "/bezplatna-konsultacja/"},
        {"label": "Analiza wody", "href": "/uslugi/analiza-wody/"},
        {"label": "Serwis urządzeń", "href": "/uslugi/serwis-urzadzen/"},
        {"label": "Białe certyfikaty", "href": "/biale-certyfikaty/"},
    ]},
    {"title": "Wiedza", "links": [
        {"label": "Baza wiedzy", "href": "/baza-wiedzy/"},
        {"label": "Case studies", "href": "/case-study/"},
        {"label": "FAQ", "href": "/faq/"},
        {"label": "Branże", "href": "/branze/"},
    ]},
    {"title": "Firma", "links": [
        {"label": "O firmie", "href": "/o-firmie/"},
        {"label": "Referencje", "href": "/referencje/"},
        {"label": "Kontakt", "href": "/kontakt/"},
        {"label": "Polityka prywatności", "href": "/polityka-prywatnosci/"},
        {"label": "Model współpracy", "href": "/warunki-wspolpracy/"},
    ]},
]

# Nowa nawigacja zgodna z briefem: mniej pozycji, więcej ścieżek decyzyjnych.
NAV = [
    {"label": "Rozwiązania", "href": "/uslugi/", "promo": ("Dobierzemy program chemiczny pod Twoją instalację.", "Umów bezpłatny audyt", "/bezplatna-konsultacja/"), "groups": [
        {"title": "Oferta", "links": [
            {"label": "Kotły parowe", "href": "/kotly-parowe/"},
            {"label": "Skraplacze wyparne", "href": "/uklady-chlodnicze/"},
            {"label": "Autoklawy i pasteryzatory", "href": "/autoklawy-i-pasteryzatory/"},
            {"label": "Ochrona membran RO", "href": "/membrany-ro/"},
            {"label": "Odkamienianie instalacji", "href": "/odkamienianie-instalacji/"},
            {"label": "Ochrona antykorozyjna", "href": "/ochrona-antykorozyjna/"},
        ]},
        {"title": "Usługi", "links": [
            {"label": "Audyt techniczny", "href": "/bezplatna-konsultacja/"},
            {"label": "Analiza wody", "href": "/uslugi/analiza-wody/"},
            {"label": "Serwis i automatyka", "href": "/uslugi/serwis-urzadzen/"},
            {"label": "Białe certyfikaty", "href": "/biale-certyfikaty/"},
        ]},
    ]},
    {"label": "Technologia KCAQUA", "href": "/kotly-parowe/kondycjonowanie-wody-kotlowej/"},
    {"label": "Case studies", "href": "/case-study/"},
    {"label": "Branże", "href": "/branze/"},
    {"label": "Baza wiedzy", "href": "/baza-wiedzy/"},
    {"label": "Firma", "href": "/o-firmie/", "promo": ("Poznaj Kabi-Chemie i nasz model współpracy.", "Skontaktuj się z nami", "/kontakt/"), "children": [
        {"label": "Misja firmy", "href": "/o-firmie/"},
        {"label": "Model współpracy", "href": "/warunki-wspolpracy/"},
        {"label": "Referencje", "href": "/referencje/"},
        {"label": "FAQ", "href": "/faq/"},
        {"label": "Kontakt", "href": "/kontakt/"},
    ]},
    {"label": "Kontakt", "href": "/kontakt/"},
]

# ------------------------------------------------------------------ etykiety okruszków/nawigacji
SHORT = {
    "/o-firmie/": "O firmie",
    "/bezplatna-konsultacja/": "Bezpłatna konsultacja",
    "/kalkulator-oszczednosci/": "Kalkulator oszczędności",
    "/biale-certyfikaty/": "Białe certyfikaty",
    "/referencje/": "Referencje",
    "/case-study/": "Case studies",
    "/case-study/kociol-parowy-fako/": "Kocioł parowy Fako",
    "/case-study/skraplacz-bac-kcaqua/": "Skraplacz BAC",
    "/case-study/skraplacz-evapco-przetworstwo-rybne/": "Skraplacz Evapco",
    "/case-study/warsztaty-amoniakalne-2024/": "Warsztaty Amoniakalne 2024",
    "/faq/": "FAQ",
    "/kotly-parowe/": "Kotły parowe",
    "/autoklawy-i-pasteryzatory/": "Autoklawy i pasteryzatory",
    "/kotly-parowe/kondycjonowanie-wody-kotlowej/": "Kondycjonowanie wody kotłowej",
    "/kotly-parowe/odkamienianie/": "Odkamienianie kotłów",
    "/kotly-parowe/ochrona-antykorozyjna/": "Ochrona antykorozyjna",
    "/uklady-chlodnicze/": "Układy chłodnicze",
    "/uklady-chlodnicze/ochrona-wiez-chlodniczych/": "Ochrona wież chłodniczych",
    "/uklady-chlodnicze/odkamienianie/": "Odkamienianie układów",
    "/uklady-chlodnicze/skraplacze-amoniakalne/": "Skraplacze amoniakalne",
    "/membrany-ro/": "Membrany RO",
    "/odkamienianie-instalacji/": "Odkamienianie instalacji",
    "/ochrona-antykorozyjna/": "Ochrona antykorozyjna",
    "/ochrona-antykorozyjna/pasywacja-stali/": "Pasywacja stali",
    "/ochrona-antykorozyjna/chemiczne-czyszczenie/": "Chemiczne czyszczenie",
    "/uslugi/": "Usługi",
    "/uslugi/audyt-techniczny/": "Audyt techniczny",
    "/uslugi/analiza-wody/": "Analiza wody",
    "/uslugi/serwis-urzadzen/": "Serwis urządzeń",
    "/branze/": "Branże",
    "/branze/zaklady-miesne-i-drobiarskie/": "Zakłady mięsne i drobiarskie",
    "/baza-wiedzy/": "Baza wiedzy",
    "/autor/": "Zespół ekspertów",
    "/baza-wiedzy/kotly-parowe/": "Kotły parowe i para",
    "/baza-wiedzy/wieze-chlodnicze/": "Wieże chłodnicze",
    "/baza-wiedzy/korozja/": "Korozja i ochrona",
    "/baza-wiedzy/parametry-wody/": "Parametry wody",
    "/baza-wiedzy/membrany-ro/": "Membrany RO",
    "/baza-wiedzy/pojedynczy-wpis-blogowy-1/": "Kamień kotłowy",
    "/baza-wiedzy/pojedynczy-wpis-blogowy-2/": "Biofilm w układzie chłodniczym",
    "/baza-wiedzy/pojedynczy-wpis-blogowy-3/": "Antyskalant do membran RO",
    "/kontakt/": "Kontakt",
    "/polityka-prywatnosci/": "Polityka prywatności",
    "/warunki-wspolpracy/": "Model współpracy",
    "/404/": "Nie znaleziono strony",
}

# ------------------------------------------------------------------ helpery sekcji
def hero(h1=None, eyebrow=None, lead=None, ctas=None, stats=None, video=None, h1_html=None, eyebrow_html=None,
         scroll_cue=None, scroll_href=None):
    d = {"type": "hero"}
    if h1: d["h1"] = h1
    if h1_html: d["h1_html"] = h1_html
    if eyebrow_html: d["eyebrow_html"] = eyebrow_html
    if eyebrow: d["eyebrow"] = eyebrow
    if lead: d["lead"] = lead
    if ctas: d["ctas"] = ctas
    if stats: d["stats"] = stats
    if video: d["video"] = video
    if scroll_cue: d["scroll_cue"] = scroll_cue
    if scroll_href: d["scroll_href"] = scroll_href
    return d

def bluf(text): return {"type": "bluf", "text": text}
def features(title, items, intro=None): return {"type": "features", "title": title, "items": items, "intro": intro}
def steps(title, items, intro=None): return {"type": "steps", "title": title, "items": items, "intro": intro}
def table(title, headers, rows, intro=None, note=None): return {"type": "table", "title": title, "headers": headers, "rows": rows, "intro": intro, "note": note}
def compare(title, headers, rows, intro=None): return {"type": "compare", "title": title, "headers": headers, "rows": rows, "intro": intro}
def faq(items, title="Najczęstsze pytania"): return {"type": "faq", "title": title, "items": items}
def cards(title, items, intro=None): return {"type": "cards", "title": title, "items": items, "intro": intro}
def cta(title, button, text="", secondary=None): return {"type": "cta", "title": title, "text": text, "button": button, "secondary": secondary}
def logos(items, title=None): return {"type": "logos", "title": title, "items": items}
def stats(items): return {"type": "stats", "items": items}
def related(items, title="Powiązane strony"): return {"type": "related", "title": title, "items": items}
def richtext(blocks, title=None): return {"type": "richtext", "title": title, "blocks": blocks}
def bloglist(title, items, intro=None): return {"type": "bloglist", "title": title, "items": items, "intro": intro}
def author(name, role, bio, initials="KC"): return {"type": "author", "name": name, "role": role, "bio": bio, "initials": initials}
def contact(title=None, text=None): return {"type": "contact", "title": title, "text": text}
def custom(html): return {"type": "custom", "html": html}

CONSULT = ("Umów bezpłatną konsultację", "/bezplatna-konsultacja/")
CONTACT = ("Kontakt", "/kontakt/")

def std_cta(title="Sprawdź, ile zaoszczędzi Twój zakład",
            text="Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie — bez zobowiązań."):
    return cta(title, CONSULT, text, secondary=CONTACT)

# ================================================================== STRONY
PAGES = {}

# ---------- STRONA GŁÓWNA -------------------------------------------------
PAGES["/"] = {"sections": [
    hero(
        video="/assets/kabi-hero-latest.mp4",
        eyebrow="Producent chemii KCAQUA",
        lead="<strong>Kabi-Chemie to producent autorskiej chemii do kondycjonowania wody</strong> w kotłach parowych, układach chłodniczych i systemach RO. Rozpuszczamy kamień, chronimy instalacje przed korozją i obniżamy zużycie wody oraz energii.",
        ctas=[CONSULT, ("Zobacz ofertę", "/uslugi/")],
        stats=[("−32%", "zużycia paliwa*"), ("−30–40%", "zużycia wody*"), ("3×", "dłuższy cykl czyszczenia*")],
    ),
    features("Nasze obszary specjalizacji", [
        (ICON["flame"], "Kotły parowe", "Kondycjonowanie wody kotłowej, odkamienianie i ochrona antykorozyjna układów parowych."),
        (ICON["snow"], "Układy chłodnicze", "Ochrona wież i skraplaczy przed kamieniem, korozją i biofilmem."),
        (ICON["membrane"], "Membrany RO", "Antyskalanty chroniące membrany odwróconej osmozy przed foulingiem."),
        (ICON["wrench"], "Odkamienianie instalacji", "Chemiczne usuwanie kamienia i osadów z rurociągów i wymienników."),
        (ICON["shield"], "Ochrona antykorozyjna", "Programy antykorozyjne, pasywacja stali i chemiczne czyszczenie."),
        (ICON["gear"], "Usługi inżynieryjne", "Audyt techniczny, analiza wody i serwis urządzeń uzdatniania."),
    ], intro="Dobieramy chemię i program dozowania do konkretnej instalacji — nie sprzedajemy „z półki”."),
    features("Dlaczego Kabi-Chemie", [
        (ICON["chart"], "Mniej paliwa", "Rozpuszczamy kamień, który izoluje powierzchnie grzewcze. 1 mm kamienia to nawet +10% zużycia paliwa."),
        (ICON["drop"], "Mniej wody", "Wyższa dopuszczalna przewodność = rzadsze odsalanie i odmulanie, czyli realnie mniejsze zużycie wody."),
        (ICON["shield"], "Autorska ochrona", "Preparaty KCAQUA łączą inhibitory korozji, odtlenianie i kontrolę pH w jednym programie."),
    ]),
    steps("Jak z nami pracujesz — 3 etapy", [
        ("Audyt techniczny", "Inżynier przyjeżdża do zakładu, ocenia instalację i pobiera próbki wody."),
        ("Program chemiczny", "Dobieramy preparat KCAQUA i program dozowania dopasowany do Twojego układu."),
        ("Monitoring i serwis", "Kontrolujemy parametry, korygujemy dozowanie i raportujemy efekty."),
    ]),
    cards("Wybrane realizacje", [
        {"h": "Kocioł parowy Fako", "desc": "Chemiczne odkamienianie i kondycjonowanie — niższe zużycie paliwa.", "href": "/case-study/kociol-parowy-fako/", "cta": "Zobacz case study"},
        {"h": "Skraplacz BAC + KCAQUA 305", "desc": "Optymalizacja pracy skraplacza i mniejsze zużycie wody.", "href": "/case-study/skraplacz-bac-kcaqua/", "cta": "Zobacz case study"},
        {"h": "Skraplacz Evapco — przetwórstwo rybne", "desc": "Usunięcie kamienia i przywrócenie wydajności chłodzenia.", "href": "/case-study/skraplacz-evapco-przetworstwo-rybne/", "cta": "Zobacz case study"},
    ], intro="Realne dane przed i po wdrożeniu programu KCAQUA."),
    logos(["Zakład mięsny", "Mleczarnia", "Browar", "Chłodnia amoniakalna", "Przemysł ciężki"],
          title="Zaufały nam zakłady przemysłowe z różnych branż"),
    std_cta(),
]}

# ---------- STRONA GŁÓWNA: NOWY UKŁAD -------------------------------------
PAGES["/"] = {"sections": [
    hero(
        video="/assets/kabi-hero-nowa.mp4",
        h1="Kondycjonowanie wody przemysłowej",
        h1_html=(
            '<span class="hero-title-line hero-title-line--light">Kondycjonowanie wody</span>'
            '<strong><span class="hero-title-line hero-title-line--accent">dla przemysłu</span></strong>'
        ),
        eyebrow_html=(
            '<span class="hero-eyebrow-mark" aria-hidden="true"></span>'
            '<span class="hero-eyebrow-text">KCAQUA · przemysłowe programy uzdatniania wody</span>'
        ),
        lead=(
            "Projektujemy programy uzdatniania i kondycjonowania wody dla kotłów parowych, skraplaczy wyparnych "
            "oraz przemysłowych obiegów chłodniczych. Technologia KCAQUA łączy chemię, automatykę dozowania "
            "i monitoring, aby ograniczać zużycie wody i energii, korozję, osady oraz awarie instalacji."
        ),
        ctas=[
            ("Sprawdź potencjał oszczędności", "/kalkulator-oszczednosci/"),
            ("Skontaktuj się z inżynierem", "/bezplatna-konsultacja/"),
        ],
        scroll_cue="Zobacz więcej",
        scroll_href="#nasze-branze",
    ),
    custom("""
<section class="section branze-svc section-brand-panel" id="nasze-branze" aria-labelledby="branze-svc-title" data-branze-svc>
  <div class="branze-svc__bg" aria-hidden="true"></div>
  <span class="branze-watermark section-bg-word" aria-hidden="true">KABI CHEMIE</span>
  <img class="branze-logo-bg section-bg-logo" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap branze-svc__grid">
    <div class="branze-svc__intro" data-branze-anim>
      <p class="eyebrow">Nasze branże</p>
      <h2 id="branze-svc-title">Branże, które obsługujemy</h2>
      <p class="branze-svc__lead">Programy kondycjonowania wody KCAQUA dobieramy pod konkretny proces — parę, chłód i wodę technologiczną. Wybierz branżę i zobacz, co realnie optymalizujemy.</p>
      <ul class="branze-menu" role="tablist" aria-label="Wybierz branżę">
        <li><button type="button" class="branze-menu__btn is-active" data-branze-tab="0" role="tab" aria-selected="true">Zakłady mięsne i drobiarskie <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg></button></li>
        <li><button type="button" class="branze-menu__btn" data-branze-tab="1" role="tab" aria-selected="false">Mleczarnie i przetwórstwo mleka <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg></button></li>
        <li><button type="button" class="branze-menu__btn" data-branze-tab="2" role="tab" aria-selected="false">Chłodnie i obiegi chłodnicze <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg></button></li>
        <li><button type="button" class="branze-menu__btn" data-branze-tab="3" role="tab" aria-selected="false">Przemysł ciężki <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg></button></li>
        <li><button type="button" class="branze-menu__btn" data-branze-tab="4" role="tab" aria-selected="false">Producenci żywności <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg></button></li>
      </ul>
    </div>

    <div class="branze-svc__panels">
      <div class="branze-svc__media" data-branze-media aria-hidden="true"></div>
      <div class="branze-pane is-active" data-branze-pane="0" style="--pane-img:url('/assets/industries/industry-meat.jpg')">
        <div class="branze-card"><span class="branze-card__num">01</span><h3>Kotły parowe</h3><p>Odkamienianie i kondycjonowanie wody kotłowej — mniej kamienia i niższe zużycie pary.</p></div>
        <div class="branze-card"><span class="branze-card__num">02</span><h3>Chłodnictwo i mycie</h3><p>Stabilne obiegi chłodnicze oraz woda do mycia bez osadów i biofilmu.</p></div>
        <div class="branze-card"><span class="branze-card__num">03</span><h3>Ciągłość produkcji</h3><p>Mniej awaryjnych przestojów, czyszczeń i ryzyka dla harmonogramu.</p></div>
        <a class="branze-pane__cta" href="/branze/">Zobacz branżę <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></a>
      </div>
      <div class="branze-pane" data-branze-pane="1" style="--pane-img:url('/assets/industries/industry-dairy.jpg')">
        <div class="branze-card"><span class="branze-card__num">01</span><h3>Wymienniki i pasteryzacja</h3><p>Ochrona powierzchni wymiany ciepła przed kamieniem i osadami.</p></div>
        <div class="branze-card"><span class="branze-card__num">02</span><h3>Stacje CIP</h3><p>Stabilna woda technologiczna do mycia — powtarzalna higiena procesu.</p></div>
        <div class="branze-card"><span class="branze-card__num">03</span><h3>Kotły parowe</h3><p>Niższe zużycie paliwa i pary dzięki czystym instalacjom.</p></div>
        <a class="branze-pane__cta" href="/branze/">Zobacz branżę <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></a>
      </div>
      <div class="branze-pane" data-branze-pane="2" style="--pane-img:url('/assets/industries/industry-cold-storage.jpg')">
        <div class="branze-card"><span class="branze-card__num">01</span><h3>Skraplacze wyparne</h3><p>Kontrola osadów i biofilmu w układach BAC i EVAPCO (program KCAQUA 305).</p></div>
        <div class="branze-card"><span class="branze-card__num">02</span><h3>Wieże chłodnicze</h3><p>Inhibitory korozji i antyskalanty — stabilna wymiana ciepła.</p></div>
        <div class="branze-card"><span class="branze-card__num">03</span><h3>Obiegi amoniakalne</h3><p>Mniej korozji i osadów w wymagających instalacjach chłodniczych.</p></div>
        <a class="branze-pane__cta" href="/branze/">Zobacz branżę <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></a>
      </div>
      <div class="branze-pane" data-branze-pane="3" style="--pane-img:url('/assets/industries/industry-heavy.jpg')">
        <div class="branze-card"><span class="branze-card__num">01</span><h3>Wysokie obciążenia cieplne</h3><p>Programy dla instalacji pracujących w trudnych, ekstremalnych warunkach.</p></div>
        <div class="branze-card"><span class="branze-card__num">02</span><h3>Korozja i kamień</h3><p>Ograniczenie ubytków, osadów i kosztownych awarii.</p></div>
        <div class="branze-card"><span class="branze-card__num">03</span><h3>Redukcja przestojów</h3><p>Dłuższe cykle między czyszczeniami i większa dyspozycyjność.</p></div>
        <a class="branze-pane__cta" href="/branze/">Zobacz branżę <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></a>
      </div>
      <div class="branze-pane" data-branze-pane="4" style="--pane-img:url('/assets/industries/industry-food-producers.jpg')">
        <div class="branze-card"><span class="branze-card__num">01</span><h3>Para i chłód</h3><p>Niezawodne media procesowe przy stabilnych parametrach pracy.</p></div>
        <div class="branze-card"><span class="branze-card__num">02</span><h3>Woda technologiczna</h3><p>Powtarzalna jakość wody i higiena całego procesu produkcji.</p></div>
        <div class="branze-card"><span class="branze-card__num">03</span><h3>Oszczędności</h3><p>Mniej wody, energii i ścieków — niższe koszty operacyjne.</p></div>
        <a class="branze-pane__cta" href="/branze/">Zobacz branżę <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></a>
      </div>
    </div>
  </div>
</section>

<section class="partner-marquee" aria-label="Logotypy marek partnerów i klientów">
  <h2 class="sr-only">Zaufali nam</h2>
  <div class="partner-trust-panel" data-trust-label aria-hidden="true">
    <div class="partner-trust-label">Zaufali nam</div>
    <p>Współpracujemy z firmami z wielu segmentów przemysłu: producentami żywności, mleczarniami, chłodniami, zakładami mięsnymi i przetwórstwem pracującym na instalacjach parowych, chłodniczych oraz wodnych.</p>
  </div>
  <div class="partner-scale-group" data-partner-scale aria-label="Ponad dwadzieścia sześć firm w bazie doświadczeń">
    <div class="partner-scale-copy">
      <span>Dołącz do firm, które oszczędzają pieniądze</span>
      <svg class="partner-growth-arrow" viewBox="0 0 520 84" aria-hidden="true" focusable="false">
        <path class="partner-growth-line" d="M14 30 C150 82 340 80 478 33" />
        <path class="partner-growth-head" d="M498 26 L476 44 L472 22 Z" />
      </svg>
    </div>
    <div class="partner-scale-badge">
    <strong class="partner-scale-number" data-count-to="26" data-suffix="+">0+</strong>
    <span>firm w bazie doświadczeń</span>
    <em>pokazujemy tylko część z nich</em>
    </div>
  </div>
  <div class="partner-rails">
    <div class="partner-rail" data-logo-rail data-direction="-1" data-repeats="3">
      <div class="partner-track">
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-01-muted.png" alt="Sokołów"><img class="logo-color" src="/assets/partners/partner-01-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-02-muted.png" alt="Farmio"><img class="logo-color" src="/assets/partners/partner-02-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-07-muted.png" alt="SEKO"><img class="logo-color" src="/assets/partners/partner-07-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-18-muted.png" alt="ZPC Bałtyk"><img class="logo-color" src="/assets/partners/partner-18-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-04-muted.png" alt="Bakalland"><img class="logo-color" src="/assets/partners/partner-04-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-05-muted.png" alt="Dolina Noteci"><img class="logo-color" src="/assets/partners/partner-05-color.png" alt="" aria-hidden="true"></span>
      </div>
    </div>
    <div class="partner-rail" data-logo-rail data-direction="1" data-repeats="3">
      <div class="partner-track">
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-06-muted.png" alt="Wipasz"><img class="logo-color" src="/assets/partners/partner-06-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-09-muted.png" alt="Rauch"><img class="logo-color" src="/assets/partners/partner-09-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-10-muted.png" alt="OSM Garwolin"><img class="logo-color" src="/assets/partners/partner-10-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-11-muted.png" alt="Krynicavitamin"><img class="logo-color" src="/assets/partners/partner-11-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-12-muted.png" alt="Komar Group"><img class="logo-color" src="/assets/partners/partner-12-color.png" alt="" aria-hidden="true"></span>
      </div>
    </div>
    <div class="partner-rail" data-logo-rail data-direction="-1" data-repeats="3">
      <div class="partner-track">
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-13-muted.png" alt="Wierzejki"><img class="logo-color" src="/assets/partners/partner-13-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-03-muted.png" alt="Silikaty Szlachta"><img class="logo-color" src="/assets/partners/partner-03-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-15-muted.png" alt="OSM Siedlce"><img class="logo-color" src="/assets/partners/partner-15-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-16-muted.png" alt="Wędzarnia Ostropol"><img class="logo-color" src="/assets/partners/partner-16-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-17-muted.png" alt="Podlaska Chata"><img class="logo-color" src="/assets/partners/partner-17-color.png" alt="" aria-hidden="true"></span>
      </div>
    </div>
  </div>
</section>

<section class="section alt impact-showcase-section" data-scrub>
  <div class="wrap impact-showcase">
    <div class="impact-copy">
      <p class="eyebrow scrub-l">Czym się zajmujemy</p>
      <h2 class="scrub-l">Mniej wody. Mniej energii. Większe&nbsp;zyski.</h2>
      <p class="scrub-l">Porządkujemy obieg wody tam, gdzie wynik techniczny przekłada się na koszty: w poborze wody uzupełniającej, zrzutach z instalacji, wymianie ciepła i trwałości urządzeń.</p>
      <a class="btn btn-primary btn-arrow impact-copy__cta scrub-l" href="/bezplatna-konsultacja/">Umów darmowy audyt</a>
    </div>
    <div class="impact-grid impact-accordion scrub-r" data-impact-accordion aria-label="Animowane obszary wpływu Kabi-Chemie">
      <article class="impact-card impact-card--active" role="button" tabindex="0" aria-expanded="true" data-impact-item style="--card-img:url('/assets/impact/impact-01-process-water-control-v2.webp');--card-pos:center center;--card-a:#062030;--card-b:#0f6f93;--card-accent:#7fd4ef">
        <span class="impact-card__number">01</span>
        <div class="impact-card__visual" aria-hidden="true"></div>
        <div class="impact-card__content">
          <p class="impact-card__kicker">Woda uzupełniająca</p>
          <h3>Zmniejszamy pobór świeżej wody</h3>
          <p>Stabilne parametry pozwalają rzadziej uzupełniać obieg i ograniczyć ilość wody potrzebnej do jego pracy.</p>
        </div>
      </article>
      <article class="impact-card" role="button" tabindex="0" aria-expanded="false" data-impact-item style="--card-img:url('/assets/impact/impact-02-process-water-discharge-v2.webp');--card-pos:center center;--card-a:#062030;--card-b:#0f6f93;--card-accent:#7fd4ef">
        <span class="impact-card__number">02</span>
        <div class="impact-card__visual" aria-hidden="true"></div>
        <div class="impact-card__content">
          <p class="impact-card__kicker">Zrzut wody z instalacji</p>
          <h3>Ograniczamy zrzut wody z instalacji</h3>
          <p>Lepsza kontrola odsalania i wymian pozwala dłużej wykorzystać wodę w obiegu, ograniczając ilość odprowadzanej wody i związane z tym koszty.</p>
        </div>
      </article>
      <article class="impact-card" role="button" tabindex="0" aria-expanded="false" data-impact-item style="--card-img:url('/assets/impact/impact-03-heat-transfer-v2.webp');--card-pos:center center;--card-a:#061a2a;--card-b:#1789b6;--card-accent:#8ee3ff">
        <span class="impact-card__number">03</span>
        <div class="impact-card__visual" aria-hidden="true"></div>
        <div class="impact-card__content">
          <p class="impact-card__kicker">Sprawna wymiana ciepła</p>
          <h3>Ograniczamy straty energii</h3>
          <p>Czyste powierzchnie wymiany ciepła pomagają efektywniej wykorzystać paliwo, parę i chłód.</p>
        </div>
      </article>
      <article class="impact-card" role="button" tabindex="0" aria-expanded="false" data-impact-item style="--card-img:url('/assets/impact/impact-04-installation-protection-v2.webp');--card-pos:center center;--card-a:#061421;--card-b:#0b3d5c;--card-accent:#b8eaff">
        <span class="impact-card__number">04</span>
        <div class="impact-card__visual" aria-hidden="true"></div>
        <div class="impact-card__content">
          <p class="impact-card__kicker">Trwałość urządzeń</p>
          <h3>Chronimy instalację</h3>
          <p>Kontrola kamienia, korozji i biofilmu ogranicza awarie oraz wydłuża czas bezpiecznej pracy urządzeń.</p>
        </div>
      </article>
      <article class="impact-card" role="button" tabindex="0" aria-expanded="false" data-impact-item style="--card-img:url('/assets/impact/impact-05-measured-savings-v2.webp');--card-pos:center center;--card-a:#071824;--card-b:#0a789b;--card-accent:#7fd4ef">
        <span class="impact-card__number">05</span>
        <div class="impact-card__visual" aria-hidden="true"></div>
        <div class="impact-card__content">
          <p class="impact-card__kicker">Wynik w danych</p>
          <h3>Pokazujemy efekt w liczbach</h3>
          <p>Monitoring i raporty łączą parametry techniczne z kosztami, ułatwiając decyzje utrzymania ruchu i zarządu.</p>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section process-loss-section section-brand-panel" id="proces-kcaqua" data-scroll-fly>
  <div class="process-loss-bg" aria-hidden="true"></div>
  <span class="section-bg-word" aria-hidden="true">PROCES</span>
  <img class="section-bg-logo" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="process-loss-inner">
    <div class="process-loss-head" data-fly="left">
      <p class="eyebrow">Proces Kabi-Chemie</p>
      <h2 id="process-loss-title">Od audytu do mierzalnych oszczędności</h2>
      <p>Jedna infrastruktura: audyt, program chemiczny, monitoring i raport kosztów wody, energii oraz ścieków.</p>
    </div>

    <article class="proc-arc" aria-labelledby="process-loss-title" data-proc-arc>
      <svg class="proc-arc__links" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
        <path class="proc-link" pathLength="100" style="--ld:.30s" d="M16 50 L30 9"/>
        <path class="proc-link" pathLength="100" style="--ld:.42s" d="M16 50 L41 25"/>
        <path class="proc-link" pathLength="100" style="--ld:.54s" d="M16 50 L46 41"/>
        <path class="proc-link" pathLength="100" style="--ld:.66s" d="M16 50 L46 57"/>
        <path class="proc-link" pathLength="100" style="--ld:.78s" d="M16 50 L41 73"/>
        <path class="proc-link" pathLength="100" style="--ld:.90s" d="M16 50 L30 89"/>
      </svg>

      <div class="proc-hub" aria-hidden="true">
        <span class="proc-hub__ring proc-hub__ring--1"></span>
        <span class="proc-hub__ring proc-hub__ring--2"></span>
        <span class="proc-hub__core">
          <img class="proc-hub__logo" src="/assets/kabi-logo-old-color.png" alt="Kabi-Chemie Water Treatment" loading="lazy">
          <span class="proc-hub__hint">Kliknij, aby zwinąć</span>
        </span>
      </div>

      <ol class="proc-steps">
        <li class="proc-step" style="--x:30%;--y:9%;--delay:.34s">
          <span class="proc-step__num">01</span>
          <span class="proc-step__ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 12h6M9 16h4"/></svg></span>
          <span class="proc-step__tx"><strong>Audyt techniczny</strong><em>Parametry instalacji, zużycie wody i aktualny program chemiczny.</em></span>
        </li>
        <li class="proc-step" style="--x:41%;--y:25%;--delay:.46s">
          <span class="proc-step__num">02</span>
          <span class="proc-step__ico" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/></svg></span>
          <span class="proc-step__tx"><strong>Potencjał oszczędności</strong><em>Wskazujemy miejsca, w których zakład realnie traci pieniądze.</em></span>
        </li>
        <li class="proc-step" style="--x:46%;--y:41%;--delay:.58s">
          <span class="proc-step__num">03</span>
          <span class="proc-step__ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3s6 6.5 6 10.5a6 6 0 0 1-12 0C6 9.5 12 3 12 3Z"/></svg></span>
          <span class="proc-step__tx"><strong>Wdrożenie KCAQUA</strong><em>Dobór chemii, nastaw i bezpiecznych parametrów pracy instalacji.</em></span>
        </li>
        <li class="proc-step" style="--x:46%;--y:57%;--delay:.70s">
          <span class="proc-step__num">04</span>
          <span class="proc-step__ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M3 12h4l3 8 4-16 3 8h4"/></svg></span>
          <span class="proc-step__tx"><strong>Monitoring i nadzór</strong><em>Stała kontrola wody, energii, osadów i stabilności efektów.</em></span>
        </li>
        <li class="proc-step" style="--x:41%;--y:73%;--delay:.82s">
          <span class="proc-step__num">05</span>
          <span class="proc-step__ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 20V4M4 20h16"/><rect x="8" y="11" width="3" height="6" rx="1"/><rect x="14" y="7" width="3" height="10" rx="1"/></svg></span>
          <span class="proc-step__tx"><strong>Raport efektów</strong><em>Oszczędności pokazane w danych zrozumiałych dla zarządu.</em></span>
        </li>
        <li class="proc-step" style="--x:30%;--y:89%;--delay:.94s">
          <span class="proc-step__num">06</span>
          <span class="proc-step__ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 4v5h-5"/></svg></span>
          <span class="proc-step__tx"><strong>Długofalowa optymalizacja</strong><em>Utrzymanie rezultatów i dalsze obniżanie strat z miesiąca na miesiąc.</em></span>
        </li>
      </ol>
    </article>

    <div class="process-cta reveal">
      <a class="btn btn-primary btn-arrow" href="/kalkulator-oszczednosci/">Uruchom kalkulator oszczędności</a>
      <a class="btn btn-ghost-light btn-arrow" href="/bezplatna-konsultacja/">Umów bezpłatny audyt</a>
    </div>
  </div>
</section>

<section class="mission-band" data-scrub>
  <span class="section-bg-word section-bg-word--dark" aria-hidden="true">MISJA</span>
  <img class="section-bg-logo section-bg-logo--dark" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap mission-grid">
    <div class="mission-visual scrub-l" aria-hidden="true">
      <video class="mission-visual__video" autoplay muted loop playsinline preload="metadata" poster="">
        <source src="/assets/mission.mp4" type="video/mp4">
      </video>
    </div>
    <div class="mission-copy scrub-r">
      <p class="eyebrow">Misja firmy</p>
      <h2>Nasza historia zaczęła się od jednego pytania</h2>
      <p><strong>Dlaczego przemysł zużywa tak dużo wody i energii, skoro nowoczesna chemia pozwala ograniczyć jej wykorzystanie?</strong></p>
      <p>Kabi-Chemie powstało w 2022 roku z przekonania, że przemysł nie musi wybierać pomiędzy rentownością a odpowiedzialnym gospodarowaniem wodą.</p>
      <p>Tak powstała technologia KCAQUA: autorski program kondycjonowania wody, który łączy ochronę instalacji z wymiernymi oszczędnościami zasobów i kosztów.</p>
      <ul class="check-list">
        <li>obniża koszty produkcji</li>
        <li>chroni instalacje</li>
        <li>ogranicza zużycie wody</li>
        <li>zmniejsza zużycie energii</li>
      </ul>
    </div>
  </div>
</section>

<section class="section impact-curve-section" data-scrub>
  <span class="section-bg-word section-bg-word--dark" aria-hidden="true">OSZCZĘDZAJ</span>
  <img class="section-bg-logo section-bg-logo--dark" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap">
    <div class="section-head scrub-l">
      <p class="eyebrow">Nasz wpływ</p>
      <h2>Oszczędność wody to nie tylko ekologia</h2>
      <p>To także niższe koszty produkcji, mniejsze zużycie energii, niższe koszty ścieków, większa niezależność zakładu i bezpieczniejsza produkcja.</p>
    </div>
  </div>

  <div class="impact-curve" data-impact-curve>
    <svg class="impact-curve__svg" viewBox="0 0 1200 520" preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <linearGradient id="curveGrad" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#0f6f93"/>
          <stop offset="0.55" stop-color="#1789b6"/>
          <stop offset="1" stop-color="#7fd4ef"/>
        </linearGradient>
        <linearGradient id="curveArea" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#1789b6" stop-opacity="0.26"/>
          <stop offset="1" stop-color="#1789b6" stop-opacity="0"/>
        </linearGradient>
        <clipPath id="curveClip" clipPathUnits="userSpaceOnUse">
          <rect class="impact-curve__clip" x="0" y="0" width="1200" height="520"/>
        </clipPath>
      </defs>
      <path class="impact-curve__area" clip-path="url(#curveClip)" fill="url(#curveArea)" d="M30,470 L150,432 L230,380 L320,424 L420,360 L520,300 L610,348 L720,272 L820,210 L910,256 L1010,196 L1080,150 L1200,95 L1200,520 L30,520 Z"/>
      <path class="impact-curve__ghost" d="M30,470 L150,432 L230,380 L320,424 L420,360 L520,300 L610,348 L720,272 L820,210 L910,256 L1010,196 L1080,150 L1200,95"/>
      <path class="impact-curve__line" d="M30,470 L150,432 L230,380 L320,424 L420,360 L520,300 L610,348 L720,272 L820,210 L910,256 L1010,196 L1080,150 L1200,95"/>
    </svg>

    <a class="impact-curve__cta" href="/bezplatna-konsultacja/" aria-label="Zacznij oszczędzać. Umów bezpłatny audyt">
      <span>Zacznij<br>oszczędzać</span>
    </a>

    <div class="impact-stat" style="left:19.2%;top:64%">
      <span class="impact-stat__num"><b class="num-counter" data-count-to="12593000">0</b></span>
      <span class="impact-stat__label">litrów wody zaoszczędzonych u jednego klienta w 12 miesięcy</span>
    </div>
    <div class="impact-stat" style="left:43.3%;top:49%">
      <span class="impact-stat__num"><b>68,2</b><i class="impact-stat__unit">%</i></span>
      <span class="impact-stat__label">redukcji zużycia wody po wdrożeniu programu</span>
    </div>
    <div class="impact-stat impact-stat--program" style="left:68.3%;top:31%">
      <span class="impact-stat__num"><b>2 + 2</b></span>
      <span class="impact-stat__label">Zakres programu obejmuje dwa obiegi wodne ze skraplaczami natryskowo-wyparnymi oraz dwa kotły parowe o wydajności 4 t każdy.</span>
    </div>
    <div class="impact-stat" style="left:90%;top:20%">
      <span class="impact-stat__num"><b class="num-counter" data-count-to="418">0</b><i class="impact-stat__unit">tys. zł</i></span>
      <span class="impact-stat__label">oszczędności kosztów operacyjnych dla klienta</span>
    </div>

    <span class="impact-node" style="left:19.17%;top:73.08%"></span>
    <span class="impact-node" style="left:43.33%;top:57.69%"></span>
    <span class="impact-node" style="left:68.33%;top:40.38%"></span>
    <span class="impact-node" style="left:90%;top:28.85%"></span>
    <span class="impact-curve__spark" aria-hidden="true"></span>
  </div>

  <div class="wrap">
    <ul class="impact-stack" aria-hidden="false">
      <li><span class="impact-stat__num"><b>12 593 000</b></span><span class="impact-stat__label">litrów wody zaoszczędzonych u jednego klienta w 12 miesięcy</span></li>
      <li><span class="impact-stat__num"><b>68,2</b><i class="impact-stat__unit">%</i></span><span class="impact-stat__label">redukcji zużycia wody po wdrożeniu programu</span></li>
      <li><span class="impact-stat__num"><b>2 + 2</b></span><span class="impact-stat__label">Zakres programu obejmuje dwa obiegi wodne ze skraplaczami natryskowo-wyparnymi oraz dwa kotły parowe o wydajności 4 t każdy.</span></li>
      <li><span class="impact-stat__num"><b>418</b><i class="impact-stat__unit">tys. zł</i></span><span class="impact-stat__label">oszczędności kosztów operacyjnych dla klienta</span></li>
    </ul>
  </div>
</section>

<section class="expert-section expert-reel-section" id="zespol-kabi-chemie">
  <div class="expert-wide reveal">
    <div class="expert-reel" data-expert-reel>
      <div class="expert-reel__visual" aria-hidden="true">
        <div class="reel-column reel-column--center" aria-hidden="true">
          <span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span>
        </div>
        <div class="reel-column reel-column--side reel-column--far reel-column--far-left" data-reel-side>
          <span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span>
        </div>
        <div class="reel-column reel-column--side reel-column--left" data-reel-side>
          <span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span>
        </div>
        <div class="reel-column reel-column--main" data-reel-track>
          <figure class="reel-portrait is-active" data-reel-image="0">
            <img src="/assets/people/lukasz-mielcarz.png" alt="" loading="lazy">
          </figure>
          <figure class="reel-portrait" data-reel-image="1">
            <img src="/assets/people/przemyslaw-jesiolkowski.png" alt="" loading="lazy">
          </figure>
          <figure class="reel-portrait" data-reel-image="2">
            <img src="/assets/people/lukasz-kumor.jpg" alt="" loading="lazy">
          </figure>
        </div>
        <div class="reel-column reel-column--side reel-column--right" data-reel-side>
          <span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span>
        </div>
        <div class="reel-column reel-column--side reel-column--far reel-column--far-right" data-reel-side>
          <span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span>
        </div>
      </div>

      <div class="expert-reel__content">
        <p class="eyebrow">Twarze Kabi-Chemie</p>
        <div class="expert-quote-stage" aria-live="polite">
          <article class="expert-quote is-active" data-reel-panel="0">
            <p class="expert-quote__mark" aria-hidden="true">“</p>
            <h2 data-quote-text>Najlepsza woda w zakładzie to ta, której nie trzeba pobrać ponownie. Dlatego każdy program zaczynamy od liczb, parametrów i punktów strat.</h2>
            <p class="expert-person"><strong>Łukasz Mielcarz</strong><span>Prezes Kabi-Chemie</span></p>
            <p class="expert-meta">Strategia wdrożeń i kierunek rozwoju technologii KCAQUA dla instalacji przemysłowych.</p>
          </article>

          <article class="expert-quote" data-reel-panel="1">
            <p class="expert-quote__mark" aria-hidden="true">“</p>
            <h2 data-quote-text>Stabilna instalacja nie bierze się z przypadku. Wynika z dobrze dobranej chemii, kontroli parametrów i serwisu, który utrzymuje wynik miesiąc po miesiącu.</h2>
            <p class="expert-person"><strong>Przemysław Jesiołkowski</strong><span>Członek zarządu · Oddział w Toruniu</span></p>
            <p class="expert-meta">Wdrożenia oszczędnościowe, nadzór nad parametrami pracy układów i rozwój klientów przemysłowych w regionie.</p>
          </article>

          <article class="expert-quote" data-reel-panel="2">
            <p class="expert-quote__mark" aria-hidden="true">“</p>
            <h2 data-quote-text>Klient nie potrzebuje kolejnego preparatu na półce. Potrzebuje planu, szybkiego wdrożenia i wyniku, który da się obronić w kosztach oraz w codziennej pracy zakładu.</h2>
            <p class="expert-person"><strong>Łukasz Kumor</strong><span>Business Development Manager</span></p>
            <p class="expert-meta">Koordynacja relacji z klientami, przygotowanie wdrożeń i przekładanie potrzeb technicznych na klarowny plan działania.</p>
          </article>
        </div>

        <div class="expert-controls" aria-label="Przełącz cytat">
          <button type="button" data-reel-prev aria-label="Poprzedni cytat">‹</button>
          <button type="button" data-reel-next aria-label="Następny cytat">›</button>
          <span class="expert-dot is-active" data-reel-dot="0"></span>
          <span class="expert-dot" data-reel-dot="1"></span>
          <span class="expert-dot" data-reel-dot="2"></span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="company-stories" id="baza-wiedzy">
  <span class="section-bg-word section-bg-word--dark" aria-hidden="true">WIEDZA</span>
  <img class="section-bg-logo section-bg-logo--dark" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap company-stories__grid">
    <header class="company-stories__intro reveal-left">
      <p class="company-kicker"><span></span>Baza wiedzy</p>
      <h2><span>Wiedza z prawdziwych</span><span>instalacji.</span></h2>
      <p>Każdy artykuł pokazuje konkretny problem instalacji, jego przyczyny i działania, które realnie obniżają koszty codziennej pracy.</p>
    </header>
    <div class="company-stories__list">
      <a class="reveal" href="/baza-wiedzy/kamien-kotlowy/"><span>Kotły parowe</span><strong>Kamień kotłowy: jak cienki osad podnosi koszty pracy kotła.</strong><i aria-hidden="true">↗</i></a>
      <a class="reveal" href="/baza-wiedzy/biofilm-w-ukladzie-chlodniczym/"><span>Chłodnictwo przemysłowe</span><strong>Biofilm w układzie chłodniczym: jak rozpoznać i usunąć osady.</strong><i aria-hidden="true">↗</i></a>
      <a class="reveal" href="/baza-wiedzy/antyskalant-ro/"><span>Membrany RO</span><strong>Antyskalant RO: kiedy naprawdę chroni membranę.</strong><i aria-hidden="true">↗</i></a>
    </div>
  </div>
</section>

<section class="section home-faq-section section-brand-panel" id="faq" data-faq-scroll>
  <span class="section-bg-word" aria-hidden="true">PYTANIA</span>
  <img class="section-bg-logo" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap home-faq">
    <div class="section-head home-faq__intro">
      <h2>Najczęściej zadawane pytania</h2>
      <p>Zebraliśmy odpowiedzi na najczęstsze pytania dotyczące technologii, wdrożenia i możliwych oszczędności. Wiemy jednak, że każda instalacja pracuje inaczej i nie da się rzetelnie ocenić wszystkich kosztów, ryzyk oraz efektów bez poznania parametrów zakładu.</p>
      <p>Dlatego zachęcamy do bezpośredniego kontaktu lub umówienia bezpłatnego audytu. Wskażemy obszary strat, oszacujemy potencjał oszczędności i zaproponujemy konkretne kolejne kroki.</p>
      <a class="btn home-faq__cta" href="#formularz-audytu">Zapytaj nas o instalację <span aria-hidden="true">↗</span></a>
    </div>
    <div class="faq home-faq__list">
      <details>
        <summary>Czym różni się technologia KCAQUA od standardowej chemii kotłowej?</summary>
        <div class="faq-a"><p>KCAQUA opiera się na autorskiej technologii polimerowej, która pozwala osiągać wyższe parametry pracy instalacji przy jednoczesnym ograniczeniu zużycia wody i energii. W wielu przypadkach umożliwia zmniejszenie częstotliwości odsalania.</p></div>
      </details>
      <details>
        <summary>Czy KCAQUA zastępuje obecnie stosowaną chemię?</summary>
        <div class="faq-a"><p>Tak. Program chemiczny KCAQUA może zastąpić dotychczasowe rozwiązania stosowane w kotłach parowych, układach chłodniczych oraz wybranych instalacjach przemysłowych.</p></div>
      </details>
      <details>
        <summary>Ile można zaoszczędzić dzięki technologii KCAQUA?</summary>
        <div class="faq-a"><p>To zależy od rodzaju instalacji, jakości wody i obecnie stosowanego programu chemicznego. W wybranych przypadkach oszczędności wody i energii sięgają nawet 50%.</p></div>
      </details>
      <details>
        <summary>Dlaczego oszczędność wody oznacza również oszczędność energii?</summary>
        <div class="faq-a"><p>Każdy litr gorącej wody usuniętej z instalacji oznacza utratę energii. Ograniczenie zrzutów i wymian wody zmniejsza również energię potrzebną do podgrzewania lub chłodzenia układu.</p></div>
      </details>
      <details>
        <summary>Czy konsultacja techniczna jest bezpłatna?</summary>
        <div class="faq-a"><p>Tak. Pierwsza konsultacja oraz wstępna analiza potencjału oszczędności są bezpłatne i nie zobowiązują do podjęcia współpracy.</p></div>
      </details>
    </div>
  </div>
</section>

<section class="audit-form-section section-brand-panel" id="formularz-audytu" data-audit-scroll>
  <span class="section-bg-word" aria-hidden="true">KONTAKT</span>
  <img class="section-bg-logo" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap audit-form-grid">
    <div class="audit-benefits">
      <h2>Jesteśmy po to, aby Ci pomóc.</h2>
      <p>Każda instalacja ma swoją specyfikę. Wpisz firmę i imię, obowiązkowy telefon, opcjonalny e-mail oraz wiadomość, a nasz inżynier oddzwoni i doprecyzuje temat rozmowy.</p>
      <div class="audit-flow" aria-label="Jak możemy Ci pomóc">
        <div><span>01</span><strong>Podaj kontakt</strong><p>Podstawowe dane wystarczą, żebyśmy mogli szybko wrócić z odpowiedzią.</p></div>
        <div><span>02</span><strong>Oddzwaniamy i ustalamy temat</strong><p>Inżynier doprecyzuje instalację, objawy i najlepszy kolejny krok.</p></div>
        <div class="audit-flow__phone"><span aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.5 15.5 0 0 0 6.6 6.6l2.2-2.2a1.5 1.5 0 0 1 1.6-.34c1.05.35 2.18.54 3.35.54A1.65 1.65 0 0 1 22 17.05v3.3A1.65 1.65 0 0 1 20.35 22C10.22 22 2 13.78 2 3.65A1.65 1.65 0 0 1 3.65 2h3.3A1.65 1.65 0 0 1 8.6 3.65c0 1.18.19 2.3.54 3.36a1.5 1.5 0 0 1-.34 1.59Z"/></svg></span><strong>Wolisz porozmawiać?</strong><p><a href="tel:+48662792875">+48 662 792 875</a></p></div>
      </div>
    </div>
    <form class="contact-form audit-form-card contact-form--smart" data-email="info@kondycjonowanie-wody.pl" novalidate>
      <div class="audit-form-card__head">
        <strong>Powiedz nam, jak możemy pomóc</strong>
      </div>
      <div class="field field--identity">
        <label for="audit-identity">Firma / imię i nazwisko <span class="field-meta">wymagane</span></label>
        <input id="audit-identity" name="identity" autocomplete="name organization" required placeholder="np. ABC Sp. z o.o. - Jan Kowalski">
        <p class="field-hint">Wpisz nazwę firmy i osobę, do której mamy oddzwonić.</p>
      </div>
      <div class="contact-form__row">
        <div class="field field--phone">
          <label for="audit-phone">Telefon <span class="field-meta">wymagane</span></label>
          <input id="audit-phone" name="phone" type="tel" autocomplete="tel" required placeholder="np. 600 000 000">
        </div>
        <div class="field field--email">
          <label for="audit-email">Adres e-mail <span class="field-meta">opcjonalne</span></label>
          <input id="audit-email" name="email" type="email" autocomplete="email" placeholder="np. biuro@firma.pl">
        </div>
      </div>
      <div class="field field--message">
        <label for="audit-message">Wiadomość <span class="field-meta">opcjonalne</span></label>
        <textarea id="audit-message" name="message" rows="4" aria-describedby="audit-message-hint" placeholder="Napisz krótko, czego dotyczy sprawa lub jaki typ instalacji mamy omówić."></textarea>
        <p id="audit-message-hint" class="field-hint">Możesz dopisać typ instalacji, problem, preferowany termin kontaktu albo dodatkowy kontekst techniczny.</p>
      </div>
      <div class="form-consents" aria-label="Zgody i informacje prawne">
        <label class="form-consent form-consent--required" for="audit-privacy-consent">
          <input id="audit-privacy-consent" name="privacyConsent" type="checkbox" required>
          <span>Zgadzam się na kontakt w sprawie zapytania zgodnie z <a href="/polityka-prywatnosci/">polityką prywatności</a>. <span class="form-consent__tag">wymagane</span></span>
        </label>
      </div>
      <button type="submit" class="btn btn-primary">Poproś o kontakt <span aria-hidden="true">→</span></button>
      <p class="form-note" role="status" aria-live="polite" hidden></p>
    </form>
  </div>
</section>
"""),
]}

# ---------- O FIRMIE ------------------------------------------------------
PAGES["/o-firmie/"] = {"sections": [
    hero(lead="<strong>Kabi-Chemie to producent autorskiej chemii KCAQUA.</strong> Specjalizujemy się w kondycjonowaniu wody dla polskiego przemysłu — od kotłowni parowych, przez układy chłodnicze, po systemy odwróconej osmozy.",
         ctas=[CONSULT, ("Nasze realizacje", "/case-study/")]),
    richtext(title="Nasza historia i misja", blocks=[
        ("p", "Powstaliśmy z przekonania, że kondycjonowanie wody w przemyśle nie musi oznaczać przepłacania za nieskuteczną chemię. Opracowaliśmy własną linię preparatów <strong>KCAQUA</strong> i podejście oparte na pomiarze, edukacji i uczciwym raportowaniu efektów."),
        ("p", "Nie sprzedajemy chemii „na sztuki”. Najpierw rozumiemy instalację i parametry wody, a dopiero potem dobieramy program dozowania, który realnie obniża koszty utrzymania ruchu."),
    ]),
    features("Nasze wartości", [
        (ICON["flask"], "Autorska technologia", "Preparaty KCAQUA projektujemy i rozwijamy sami — odpowiadamy za skład i wynik."),
        (ICON["doc"], "Edukacja klienta", "Tłumaczymy parametry wody i pokazujemy, co i dlaczego robimy."),
        (ICON["check"], "Uczciwość", "Jeśli efekt wymaga czasu, mówimy to wprost. Pokazujemy realne dane, nie obietnice."),
    ]),
    features("Dla kogo pracujemy", [
        (ICON["flame"], "Kotłownie parowe", "Zakłady wykorzystujące parę w procesach produkcyjnych."),
        (ICON["snow"], "Układy chłodnicze", "Wieże chłodnicze, skraplacze wyparne i amoniakalne."),
        (ICON["membrane"], "Systemy RO", "Instalacje odwróconej osmozy i demineralizacji wody."),
    ]),
    cards("Poznaj nas bliżej", [
        {"h": "Nasze usługi", "desc": "Audyt, analiza wody i serwis instalacji.", "href": "/uslugi/"},
        {"h": "Referencje", "desc": "Opinie kierowników technicznych i dyrektorów UR.", "href": "/referencje/"},
        {"h": "Case studies", "desc": "Realne wdrożenia i oszczędności.", "href": "/case-study/"},
    ]),
    std_cta(),
]}

# ---------- BEZPŁATNA KONSULTACJA ----------------------------------------
PAGES["/bezplatna-konsultacja/"] = {
    "body_class": "has-dark-hero consultation-branches-page",
    "title": "Bezpłatna konsultacja techniczna | Kabi-Chemie",
    "h1": "Porozmawiaj z inżynierem przed doborem chemii.",
    "meta": "Bezpłatna konsultacja techniczna Kabi-Chemie: rozmowa z inżynierem, wstępna diagnoza instalacji, analiza objawów i jasny kolejny krok dla kotłów, chłodnictwa, RO i obiegów procesowych.",
    "image": "/assets/industries/industry-branches-collage.jpg",
    "og_image": "/assets/industries/industry-branches-collage.jpg",
    "sections": [custom("""
<section class="consult-branches-hero" id="konsultacja" aria-label="Bezpłatna konsultacja techniczna Kabi-Chemie">
  <div class="consult-branches-hero__media" aria-hidden="true">
    <video autoplay muted loop playsinline preload="metadata" poster="/assets/industries/industry-branches-collage.jpg">
      <source src="/assets/consultation-hero.mp4" type="video/mp4">
    </video>
  </div>
  <div class="consult-branches-hero__shade" aria-hidden="true"></div>
  <div class="wrap consult-branches-hero__inner">
    <p class="branches-kicker">Bezpłatna konsultacja techniczna</p>
    <h1><span>Porozmawiaj z inżynierem</span> <span>przed doborem chemii.</span></h1>
    <p class="consult-branches-hero__lead">Zaczynamy od rozmowy o instalacji, objawach i kosztach, które generuje woda. Bez gotowego schematu i bez presji zakupowej. Najpierw porządkujemy sytuację, potem wskazujemy najrozsądniejszy kolejny krok.</p>
    <div class="branches-hero__actions consult-branches-hero__actions">
      <a class="btn btn-primary" href="#consult-form">Wypełnij krótki formularz</a>
      <a class="branches-link" href="tel:+48662792875">Zadzwoń: +48 662 792 875</a>
    </div>
    <ul class="branches-sector-strip consult-branches-strip" aria-label="Zakres konsultacji">
      <li><a href="/kotly-parowe/kondycjonowanie-wody-kotlowej/">Technologia KCAQUA <span aria-hidden="true">↘</span></a></li>
      <li><a href="/kotly-parowe/">Kotły parowe <span aria-hidden="true">↘</span></a></li>
      <li><a href="/uklady-chlodnicze/">Skraplacze wyparne <span aria-hidden="true">↘</span></a></li>
      <li><a href="/membrany-ro/">Ochrona membran <span aria-hidden="true">↘</span></a></li>
      <li><a href="/biale-certyfikaty/">Białe certyfikaty <span aria-hidden="true">↘</span></a></li>
      <li><a href="/uslugi/serwis-urzadzen/">Serwis i automatyka <span aria-hidden="true">↘</span></a></li>
    </ul>
  </div>
</section>

<section class="branches-method consult-branches-method reveal" id="proces-konsultacji" aria-labelledby="consult-method-title" data-scroll-fly>
  <div class="wrap branches-method__grid">
    <div data-fly="left">
      <p class="branches-kicker">Jak przebiega konsultacja</p>
      <h2 id="consult-method-title"><span>Krótka rozmowa.</span> <span>Jasny kolejny krok.</span></h2>
      <p>Wystarczy numer telefonu i jedno zdanie o instalacji. Potrzebne dane ustalimy wspólnie podczas rozmowy.</p>
    </div>
    <ol class="branches-method__steps">
      <li data-fly="right"><strong>Krótka informacja</strong><span>Podajesz firmę, numer telefonu i temat rozmowy.</span></li>
      <li data-fly="right" data-fly-delay="0.04"><strong>Rozmowa techniczna</strong><span>Inżynier porządkuje objawy, warunki pracy i dostępne dane.</span></li>
      <li data-fly="right" data-fly-delay="0.08"><strong>Ustalenie działania</strong><span>Otrzymujesz konkretną rekomendację dalszego kroku.</span></li>
    </ol>
  </div>
</section>

<section class="branch-chapter consult-branches-chapter reveal" id="rozmowa-techniczna" aria-labelledby="consult-chapter-title" data-scroll-fly>
  <div class="wrap branch-chapter__grid">
    <figure class="branch-chapter__media"><img src="/assets/industries/industry-heavy.jpg" alt="Instalacje przemysłowe, rurociągi i obiegi wody wymagające konsultacji technicznej" loading="lazy"></figure>
    <div class="branch-chapter__copy">
      <p class="branches-kicker" data-fly="right">Rozmowa techniczna</p>
      <h2 id="consult-chapter-title" data-fly="right" data-fly-delay="0.02"><span>Nie zaczynamy od oferty.</span> <span>Zaczynamy od procesu.</span></h2>
      <p data-fly="right" data-fly-delay="0.05">Woda w zakładzie rzadko generuje koszt w jednym miejscu. Dlatego pierwsza rozmowa porządkuje cały kontekst: źródło wody, obieg, automatykę, osady, korozję, odsalanie, energię i wpływ na ciągłość produkcji.</p>
      <div class="branch-matrix" data-fly="right" data-fly-delay="0.08">
        <article><h3>Co omawiamy</h3><p>Typ instalacji, aktualne parametry, częstotliwość czyszczeń, zużycie wody, ścieki, awarie i miejsca, w których proces traci stabilność.</p></article>
        <article><h3>Co filtrujemy</h3><p>Oddzielamy objaw od przyczyny. Kamień, biofilm albo korozja mogą wymagać zupełnie innego działania niż sama zmiana preparatu.</p></article>
        <article><h3>Co dostajesz</h3><p>Praktyczny plan pierwszego kroku: co sprawdzić, co policzyć i kiedy warto przejść do audytu lub programu KCAQUA.</p></article>
      </div>
      <div class="branch-actions"><a class="btn btn-primary" href="#consult-form">Umów rozmowę techniczną</a><a class="branches-link" href="/branze/">Zobacz branże</a></div>
    </div>
  </div>
</section>

<section class="branches-savings consult-branches-form reveal" id="consult-form" aria-labelledby="consult-form-title" data-scroll-fly>
  <div class="wrap branches-savings__grid consult-branches-form__grid">
    <div data-fly="left">
      <p class="branches-kicker">Umów konsultację</p>
      <h2 id="consult-form-title"><span>Porozmawiajmy o</span> <span>Twojej instalacji.</span></h2>
      <p>Wypełnij krótki formularz, a nasz inżynier skontaktuje się z Tobą. Wystarczy numer telefonu i krótka informacja o instalacji. Podczas rozmowy wspólnie ustalimy najlepszy kolejny krok.</p>
      <div class="consult-branches-form__notes" aria-label="Najważniejsze informacje o kontakcie">
        <a class="consult-contact-link" href="tel:+48662792875">
          <span class="consult-contact-link__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/></svg></span>
          <span><small>Telefon</small><strong>+48 662 792 875</strong></span>
        </a>
        <a class="consult-contact-link" href="mailto:info@kondycjonowanie-wody.pl">
          <span class="consult-contact-link__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg></span>
          <span><small>E-mail</small><strong>info@kondycjonowanie-wody.pl</strong></span>
        </a>
      </div>
    </div>
    <div class="consult-branches-form__stage" data-fly="right">
      <span class="consult-branches-form__sigil" aria-hidden="true"></span>
      <form class="contact-form contact-form--smart consult-smart-form consult-branches-form__card" data-email="info@kondycjonowanie-wody.pl" novalidate>
      <div class="field field--identity">
        <label for="consult-identity">Firma / imię i nazwisko <span class="field-meta">wymagane</span></label>
        <input id="consult-identity" name="identity" autocomplete="name organization" required placeholder="np. ABC Sp. z o.o. - Jan Kowalski">
      </div>
      <div class="contact-form__row">
        <div class="field field--phone">
          <label for="consult-phone">Telefon <span class="field-meta">wymagane</span></label>
          <input id="consult-phone" name="phone" type="tel" autocomplete="tel" required placeholder="np. 600 000 000">
        </div>
        <div class="field field--email">
          <label for="consult-email">Adres e-mail <span class="field-meta">opcjonalne</span></label>
          <input id="consult-email" name="email" type="email" autocomplete="email" placeholder="np. biuro@firma.pl">
        </div>
      </div>
      <div class="field field--message">
        <label for="consult-message">Wiadomość <span class="field-meta">opcjonalne</span></label>
        <textarea id="consult-message" name="message" rows="4" placeholder="Napisz krótko, czego dotyczy sprawa lub jaki typ instalacji mamy omówić."></textarea>
      </div>
      <div class="form-consents" aria-label="Zgody i informacje prawne">
        <label class="form-consent form-consent--required" for="consult-privacy-consent">
          <input id="consult-privacy-consent" name="privacyConsent" type="checkbox" required>
          <span>Zgadzam się na kontakt w sprawie zapytania zgodnie z <a href="/polityka-prywatnosci/">polityką prywatności</a>. <span class="form-consent__tag">wymagane</span></span>
        </label>
      </div>
      <button type="submit" class="btn btn-primary">Poproś o kontakt</button>
      <p class="form-note" role="status" aria-live="polite" hidden></p>
      </form>
    </div>
  </div>
</section>

<section class="branches-proof consult-branches-faq reveal" aria-labelledby="consult-faq-title" data-scroll-fly>
  <div class="wrap consult-branches-faq__layout">
    <div class="consult-branches-faq__intro" data-fly="left">
      <p class="branches-proof__eyebrow">FAQ</p>
      <h2 id="consult-faq-title" class="branches-proof__intro"><span>Techniczne pytania</span> <span>przed konsultacją.</span></h2>
      <p class="branches-proof__lead">Jeżeli widzisz kamień, korozję, biofilm, wzrost przewodności, spadek wydajności albo problemy z membranami, nie musisz od razu znać przyczyny. W rozmowie porządkujemy objawy, dane i najrozsądniejszy pierwszy krok.</p>
    </div>
    <div class="consult-branches-faq__list" data-fly="right">
      <details>
        <summary>Czy konsultacja jest naprawdę bezpłatna?</summary>
        <p>Tak. Pierwsza rozmowa techniczna i wstępne rozpoznanie problemu są bezpłatne. Nie zobowiązują do zakupu chemii, audytu ani usługi serwisowej.</p>
      </details>
      <details>
        <summary>Czy muszę mieć wyniki analizy wody?</summary>
        <p>Nie. Jeśli masz wyniki, przeanalizujemy je w kontekście instalacji. Jeśli ich nie masz, wskażemy, które parametry warto sprawdzić: pH, twardość, przewodność, chlorki, żelazo, zasadowość, TDS lub mikrobiologię.</p>
      </details>
      <details>
        <summary>Jakie dane techniczne najbardziej przyspieszają diagnozę?</summary>
        <p>Najbardziej pomagają: typ instalacji, źródło wody, wyniki badań, przewodność, twardość, objawy, zdjęcia osadów, historia czyszczeń, zużycie wody uzupełniającej i informacja o aktualnym dozowaniu.</p>
      </details>
      <details>
        <summary>Co jeśli znam tylko objaw, a nie znam przyczyny?</summary>
        <p>To wystarczy na start. Objaw, taki jak kamień, korozja, śliski osad, spadek wymiany ciepła, wzrost przewodności albo częste alarmy, pozwala zawęzić kierunek diagnozy.</p>
      </details>
      <details>
        <summary>Czy możecie ocenić obecny program chemiczny?</summary>
        <p>Tak. Możemy omówić stosowaną chemię, punkty dozowania, dawki, automatykę, parametry kontrolne i efekty w instalacji. Nie chodzi o samą nazwę preparatu, tylko o to, czy program realnie pasuje do pracy obiegu.</p>
      </details>
      <details>
        <summary>Kiedy rozmowa nie wystarczy i potrzebny jest audyt?</summary>
        <p>Audyt ma sens, gdy problem wraca, instalacja ma kilka obiegów, wyniki są niespójne, pojawia się korozja, szybkie zarastanie osadem albo chcesz policzyć wodę, ścieki, energię i potencjał oszczędności.</p>
      </details>
      <details>
        <summary>Co sprawdzacie przy kotłowni parowej?</summary>
        <p>Patrzymy na twardość, pH, przewodność, odsalanie, odmulanie, zużycie wody, jakość kondensatu, historię kamienia, pracę stacji uzdatniania i ryzyko strat paliwa przez gorszą wymianę ciepła.</p>
      </details>
      <details>
        <summary>Co sprawdzacie przy chłodni albo skraplaczu?</summary>
        <p>Analizujemy cykle koncentracji, przewodność, odsalanie, twardość, pH, mikrobiologię, biofilm, korozję ocynku, jakość wody uzupełniającej i wpływ osadów na wydajność chłodzenia.</p>
      </details>
      <details>
        <summary>Czy konsultacja obejmuje membrany RO?</summary>
        <p>Tak. Przy RO pytamy o jakość wody surowej, odzysk, przepływy, różnicę ciśnień, jakość permeatu, płukania, historię CIP oraz ryzyko osadów mineralnych, żelaza, chloru i zanieczyszczeń organicznych.</p>
      </details>
      <details>
        <summary>Czy pomagacie ocenić potencjał oszczędności?</summary>
        <p>Tak, jeśli są dane do policzenia strat. Najczęściej analizujemy zużycie wody, ścieków, energii, paliwa, częstotliwość czyszczeń, odsalanie i wpływ osadów na wymianę ciepła.</p>
      </details>
      <details>
        <summary>Jak szybko ktoś się ze mną skontaktuje?</summary>
        <p>W dni robocze oddzwaniamy zwykle w ciągu 24 godzin. Przy pilnym spadku wydajności, awarii lub ryzyku zatrzymania procesu najlepiej zadzwonić bezpośrednio.</p>
      </details>
    </div>
  </div>
</section>

<section class="branches-final consult-branches-final reveal" aria-labelledby="consult-final-title">
  <div class="wrap branches-final__inner">
    <span class="branches-final__sigil" aria-hidden="true"></span>
    <h2 id="consult-final-title"><span>Obsługujemy Twoją branżę i znamy objawy.</span> <span>Wskażemy najrozsądniejszy pierwszy krok.</span></h2>
    <p>Opowiedz, jak pracuje instalacja i co się zmieniło. Ustalimy, czy zacząć od analizy wody, audytu technicznego, korekty dozowania, czyszczenia chemicznego czy kalkulacji oszczędności.</p>
    <div class="branches-final__actions">
      <a class="btn btn-primary" href="#consult-form">Umów bezpłatną konsultację</a>
      <a class="branches-link" href="/branze/">Zobacz obsługiwane branże</a>
    </div>
  </div>
</section>
""")],
}

# ---------- REFERENCJE ----------------------------------------------------
PAGES["/referencje/"] = {"sections": [
    hero(lead="Zaufały nam zakłady z przemysłu spożywczego, chłodniczego i produkcyjnego. Zobacz, jak chemia Kabi-Chemie chroni instalacje naszych klientów.",
         ctas=[("Zobacz case studies", "/case-study/"), CONSULT]),
    logos(["Zakład mięsny", "Mleczarnia", "Browar", "Chłodnia amoniakalna", "Przemysł ciężki", "Przetwórstwo rybne"],
          title="Wybrane branże, które obsługujemy"),
    features("Co mówią o współpracy", [
        (ICON["check"], "Kierownik UR, zakład mięsny", "„Po wdrożeniu programu zaobserwowaliśmy wyraźne zmniejszenie kamienia w kotle.” (opinia przykładowa)"),
        (ICON["check"], "Dyrektor techniczny, chłodnia", "„Skraplacz odzyskał wydajność, a zużycie wody spadło.” (opinia przykładowa)"),
        (ICON["check"], "Utrzymanie ruchu, mleczarnia", "„Konkretny raport i jasna rekomendacja — wiedzieliśmy, za co płacimy.” (opinia przykładowa)"),
    ], intro="Opinie poniżej są przykładowe — do zastąpienia autoryzowanymi cytatami klientów."),
    related([
        ("Case studies — realne wdrożenia", "/case-study/"),
        ("Bezpłatna konsultacja", "/bezplatna-konsultacja/"),
        ("Nasze usługi", "/uslugi/"),
    ]),
    std_cta(),
]}

# ---------- KALKULATOR OSZCZĘDNOŚCI --------------------------------------
PAGES["/kalkulator-oszczednosci/"] = {
    "body_class": "has-dark-hero branches-hub-page calculator-experience-page",
    "no_breadcrumbs": True,
    "title": "Kalkulator oszczędności wody i energii dla przemysłu | Kabi-Chemie",
    "h1": "Kalkulator oszczędności wody i energii",
    "meta": "Poznaj potencjał ograniczenia kosztów wody, ścieków i energii w kotle parowym lub skraplaczu wyparnym. Bezpłatny kalkulator Kabi-Chemie dla przemysłu.",
    "image": "/assets/impact/impact-05-operational-costs.png",
    "og_image": "/assets/impact/impact-05-operational-costs.png",
    "jsonld": [
        {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Kalkulator oszczędności wody i energii Kabi-Chemie",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web",
            "description": "Kalkulator potencjału ograniczenia kosztów dla kotłów parowych i skraplaczy wyparnych.",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "PLN"},
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": "Co dokładnie obejmuje wynik rocznych oszczędności?", "acceptedAnswer": {"@type": "Answer", "text": "Wynik sumuje dwa składniki: koszt energii traconej przez kamień lub osad oraz potencjał wynikający z ograniczenia odsalania, czyli zużycia wody, ścieków, a w kotle także strat ciepła. Pokazuje wartość dla podanych godzin pracy i cen mediów, a nie gwarantowaną kwotę oszczędności."}},
                {"@type": "Question", "name": "Które dane mają największy wpływ na wynik dla kotła parowego?", "acceptedAnswer": {"@type": "Answer", "text": "Na część energetyczną najmocniej wpływają moc kotła, czas pracy, cena gazu i grubość kamienia. Potencjał ograniczenia odsalania zależy przede wszystkim od produkcji pary, czasu pracy oraz kosztów gazu, wody i ścieków."}},
                {"@type": "Question", "name": "Które dane mają największy wpływ na wynik dla skraplacza wyparnego?", "acceptedAnswer": {"@type": "Answer", "text": "Kluczowe są moc chłodnicza, roczny czas pracy, cena energii oraz różnica między średnicą czystej wężownicy a średnicą z osadem. Koszty wody i ścieków decydują o wartości potencjalnego ograniczenia odsalania."}},
                {"@type": "Question", "name": "Jak wiarygodnie określić grubość kamienia lub osadu?", "acceptedAnswer": {"@type": "Answer", "text": "Najlepiej wykorzystać pomiar wykonany podczas postoju, dokumentację z ostatniego czyszczenia albo różnicę średnic wężownicy. Gdy nie ma pomiaru, warto policzyć kilka scenariuszy grubości zamiast traktować jedną wartość jako pewną."}},
                {"@type": "Question", "name": "Czy kalkulator uwzględnia zmienne obciążenie instalacji w ciągu roku?", "acceptedAnswer": {"@type": "Answer", "text": "Nie w pełni. Model używa jednej wartości mocy i łącznej liczby godzin pracy, dlatego przy dużych zmianach obciążenia dokładniejszy wynik wymaga danych miesięcznych lub godzinowych z systemu monitoringu."}},
                {"@type": "Question", "name": "Dlaczego wynik może różnić się od audytu?", "acceptedAnswer": {"@type": "Answer", "text": "Audyt uwzględnia rzeczywiste obciążenie, jakość wody, automatykę, stan powierzchni wymiany ciepła i historię pracy instalacji, których model kalkulatora nie opisuje w pełni."}},
                {"@type": "Question", "name": "Kiedy kalkulację należy potwierdzić pomiarem lub audytem?", "acceptedAnswer": {"@type": "Answer", "text": "Zawsze przed zatwierdzeniem budżetu, zmianą programu chemicznego, czyszczeniem instalacji lub przyjęciem oszczędności do planu inwestycyjnego. Pomiar potwierdza stan powierzchni, parametry wody i rzeczywisty profil pracy urządzenia."}},
                {"@type": "Question", "name": "Jakie dane przygotować do weryfikacji wyniku z inżynierem?", "acceptedAnswer": {"@type": "Answer", "text": "Najbardziej użyteczne są dane z ostatnich 12 miesięcy: zużycie paliwa lub energii, godziny pracy, produkcja pary albo obciążenie chłodnicze, zużycie wody, ilość ścieków i wyniki analiz wody. Warto dołączyć także historię czyszczeń, nastawy automatyki i aktualne stawki za media."}},
                {"@type": "Question", "name": "Czy wynik można wykorzystać przy planowaniu białego certyfikatu?", "acceptedAnswer": {"@type": "Answer", "text": "Tak, jako wstępny sygnał, że przedsięwzięcie warto przeanalizować. Do formalnej oceny potrzebne są jednak dane bazowe, metodyka obliczeń, pomiary i audyt efektywności energetycznej."}},
            ],
        },
    ],
    "sections": [
    custom("""
<section class="calc-page-hero" id="kalkulator-top" aria-label="Kalkulator oszczędności wody i energii">
  <div class="calc-page-hero__media" aria-hidden="true">
    <video autoplay muted loop playsinline preload="metadata">
      <source src="/assets/calculator-hero.mp4" type="video/mp4">
    </video>
  </div>
  <div class="calc-page-hero__shade" aria-hidden="true"></div>
  <div class="wrap calc-page-hero__inner">
    <div class="calc-page-hero__copy">
      <p class="branches-kicker">Kalkulator potencjału oszczędności</p>
      <h1><span>Policz potencjał oszczędności</span> <span>wody i energii.</span></h1>
      <p class="calc-page-hero__lead">Uzupełnij dane kotła parowego lub skraplacza wyparnego. Kalkulator pokaże roczną wartość energii, wody i ścieków, którą warto odzyskać w Państwa zakładzie.</p>
      <div class="branches-hero__actions calc-page-hero__actions">
        <a class="btn btn-primary" href="#kalkulator">Przejdź do kalkulatora</a>
        <a class="branches-link" href="/bezplatna-konsultacja/">Porozmawiaj z inżynierem</a>
      </div>
    </div>
  </div>
</section>
"""),
    custom("""
<section class="section calc2-section" id="kalkulator">
  <div class="wrap">
    <div class="section-head calc2-head">
      <p class="eyebrow">Wstępna kalkulacja techniczna</p>
      <h2>Roczny potencjał oszczędności dla Państwa instalacji</h2>
      <p>Wybierz rodzaj instalacji i uzupełnij podstawowe parametry jej pracy. Model pokaże potencjał ograniczenia kosztów energii, wody i ścieków związanych z osadami oraz nadmiernym odsalaniem. Wyliczenie pomaga wybrać obszary warte wspólnej weryfikacji technicznej.</p>
    </div>

    <form class="calc2" data-savings-calculator novalidate>
      <div class="calc2-grid">
        <div class="calc2-panel">
          <header class="calc2-panel__header">
            <span class="calc2-section-brand calc2-section-brand--lockup" aria-hidden="true"><img src="/assets/kabi-logo-horizontal.svg" width="730" height="164" alt=""></span>
            <span><strong>Dane instalacji</strong><small>Wynik aktualizuje się automatycznie</small></span>
          </header>
          <div class="calc2-typebar" role="tablist" aria-label="Typ instalacji" data-active-type="kotly">
            <span class="calc2-typebar__thumb" aria-hidden="true"><span class="calc2-typebar__drop"></span></span>
            <button type="button" class="calc2-type is-active" data-calc-type="kotly" role="tab" aria-selected="true">
              <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7h8M8 11h8"/><path d="M9 15v3M15 15v3"/></svg>
              <span>Kotły parowe</span>
            </button>
            <button type="button" class="calc2-type" data-calc-type="skraplacze" role="tab" aria-selected="false">
              <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 5h16v6a8 8 0 0 1-16 0Z"/><path d="M9 16c0 2-2 2-2 4M15 16c0 2 2 2 2 4M12 16.5c0 2-1.5 2-1.5 3.5"/></svg>
              <span>Skraplacze wyparne</span>
            </button>
          </div>

          <div class="calc2-fields" data-calc-fields="kotly">
            <fieldset class="calc2-group">
              <legend><span class="calc2-ico calc2-ico--scale"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12.83 2.18-9.61 4.37a1 1 0 0 0 0 1.82l7.95 3.62a2 2 0 0 0 1.66 0l7.95-3.62a1 1 0 0 0 0-1.82l-9.61-4.37a2 2 0 0 0-1.66 0Z"/><path d="m22 12.5-9.17 4.17a2 2 0 0 1-1.66 0L2 12.5"/><path d="m22 17.5-9.17 4.17a2 2 0 0 1-1.66 0L2 17.5"/></svg></span> Zakamienienie powierzchni grzewczych</legend>
              <div class="calc2-rows">
                <label class="calc2-field"><span class="calc2-field__label">Moc cieplna kotła <i class="calc2-info" tabindex="0" aria-label="Maksymalna moc cieplna kotła parowego określona przez producenta." data-tip="Maksymalna moc cieplna kotła parowego określona przez producenta.">i</i></span><span class="calc2-input"><input type="number" name="kb_power" value="2500" min="0" step="50" inputmode="decimal"><em>kW</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Godziny pracy / rok <i class="calc2-info" tabindex="0" aria-label="Łączna liczba godzin pracy kotła w ciągu roku (365 dni × 24 h)." data-tip="Łączna liczba godzin pracy kotła w ciągu roku (365 dni × 24 h).">i</i></span><span class="calc2-input"><input type="number" name="kb_hours" value="8760" min="0" max="8760" step="10" inputmode="decimal"><em>h</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Cena gazu ziemnego <i class="calc2-info" tabindex="0" aria-label="Aktualny koszt zakupu gazu wykorzystywanego do produkcji pary." data-tip="Aktualny koszt zakupu gazu wykorzystywanego do produkcji pary.">i</i></span><span class="calc2-input"><input type="number" name="kb_gas" value="425" min="0" step="5" inputmode="decimal"><em>zł/MWh</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Grubość kamienia <i class="calc2-info" tabindex="0" aria-label="Szacowana lub zmierzona grubość osadów na powierzchniach grzewczych kotła." data-tip="Szacowana lub zmierzona grubość osadów na powierzchniach grzewczych kotła.">i</i></span><span class="calc2-input"><input type="number" name="kb_scale" value="0.2" min="0" max="8" step="0.1" inputmode="decimal"><em>mm</em></span></label>
              </div>
            </fieldset>
            <fieldset class="calc2-group">
              <legend><span class="calc2-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.3 6 10.5a6 6 0 0 1-12 0C6 9.3 12 3 12 3Z"/></svg></span> Zasolenie wody kotłowej</legend>
              <div class="calc2-rows">
                <label class="calc2-field"><span class="calc2-field__label">Produkcja pary <i class="calc2-info" tabindex="0" aria-label="Ilość pary produkowanej przez kocioł w ciągu godziny." data-tip="Ilość pary produkowanej przez kocioł w ciągu godziny.">i</i></span><span class="calc2-input"><input type="number" name="kb_steam" value="20" min="0" step="1" inputmode="decimal"><em>t/h</em></span></label>
              </div>
            </fieldset>
          </div>

          <div class="calc2-fields" data-calc-fields="skraplacze" hidden>
            <fieldset class="calc2-group">
              <legend><span class="calc2-ico calc2-ico--scale"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12.83 2.18-9.61 4.37a1 1 0 0 0 0 1.82l7.95 3.62a2 2 0 0 0 1.66 0l7.95-3.62a1 1 0 0 0 0-1.82l-9.61-4.37a2 2 0 0 0-1.66 0Z"/><path d="m22 12.5-9.17 4.17a2 2 0 0 1-1.66 0L2 12.5"/><path d="m22 17.5-9.17 4.17a2 2 0 0 1-1.66 0L2 17.5"/></svg></span> Zakamienienie wężownic / wymiany ciepła</legend>
              <div class="calc2-rows">
                <label class="calc2-field"><span class="calc2-field__label">Moc chłodnicza układu <i class="calc2-info" tabindex="0" aria-label="Moc układu chłodniczego opisana w karcie produktu." data-tip="Moc układu chłodniczego opisana w karcie produktu.">i</i></span><span class="calc2-input"><input type="number" name="sk_power" value="1400" min="0" step="50" inputmode="decimal"><em>kW</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Godziny pracy / rok <i class="calc2-info" tabindex="0" aria-label="Dla instalacji pracujących całorocznie w trybie ciągłym przyjmuje się 8760 h/rok (365 dni × 24 h)." data-tip="Dla instalacji pracujących całorocznie w trybie ciągłym przyjmuje się 8760 h/rok (365 dni × 24 h).">i</i></span><span class="calc2-input"><input type="number" name="sk_hours" value="8760" min="0" max="8760" step="10" inputmode="decimal"><em>h</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Cena energii elektr. <i class="calc2-info" tabindex="0" aria-label="Cena energii elektrycznej netto." data-tip="Cena energii elektrycznej netto.">i</i></span><span class="calc2-input"><input type="number" name="sk_energy" value="425" min="0" step="5" inputmode="decimal"><em>zł/MWh</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Średnica czystej wężownicy <i class="calc2-info" tabindex="0" aria-label="Średnica zewnętrzna czystej wężownicy, zmierzona suwmiarką." data-tip="Średnica zewnętrzna czystej wężownicy, zmierzona suwmiarką.">i</i></span><span class="calc2-input"><input type="number" name="sk_d_clean" value="20" min="0" step="0.5" inputmode="decimal"><em>mm</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Średnica z osadem <i class="calc2-info" tabindex="0" aria-label="Średnica wężownicy z osadem. Osad liczony po obu stronach, dlatego grubość = (z osadem − czysta) / 2." data-tip="Średnica wężownicy z osadem. Osad liczony po obu stronach, dlatego grubość = (z osadem − czysta) / 2.">i</i></span><span class="calc2-input"><input type="number" name="sk_d_scaled" value="22" min="0" step="0.5" inputmode="decimal"><em>mm</em></span></label>
              </div>
            </fieldset>
          </div>

          <section class="calc2-adv" aria-labelledby="calc2-adv-title">
            <header class="calc2-adv__head">
              <span class="calc2-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M4 7h10M18 7h2M4 12h3M11 12h9M4 17h8M16 17h4"/><circle cx="16" cy="7" r="2"/><circle cx="9" cy="12" r="2"/><circle cx="14" cy="17" r="2"/></svg></span>
              <span><h3 id="calc2-adv-title">Założenia i ceny mediów</h3><p>Dopasuj wartości do aktualnych kosztów w swoim zakładzie.</p></span>
            </header>
            <div class="calc2-fields" data-calc-fields="kotly">
              <div class="calc2-rows">
                <label class="calc2-field"><span class="calc2-field__label">Cena gazu - odzysk ciepła <i class="calc2-info" tabindex="0" aria-label="Cena paliwa użyta do wyceny odzysku ciepła z ograniczenia odsalania." data-tip="Cena paliwa użyta do wyceny odzysku ciepła z ograniczenia odsalania.">i</i></span><span class="calc2-input"><input type="number" name="kb_gas2" value="425.4" min="0" step="0.1" inputmode="decimal"><em>zł/MWh</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Koszt wody <i class="calc2-info" tabindex="0" aria-label="Koszt zakupu 1 m³ wody." data-tip="Koszt zakupu 1 m³ wody.">i</i></span><span class="calc2-input"><input type="number" name="kb_water" value="6" min="0" step="0.5" inputmode="decimal"><em>zł/m³</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Koszt ścieków <i class="calc2-info" tabindex="0" aria-label="Koszt odprowadzenia 1 m³ ścieków." data-tip="Koszt odprowadzenia 1 m³ ścieków.">i</i></span><span class="calc2-input"><input type="number" name="kb_sewage" value="6" min="0" step="0.5" inputmode="decimal"><em>zł/m³</em></span></label>
              </div>
            </div>
            <div class="calc2-fields" data-calc-fields="skraplacze" hidden>
              <div class="calc2-rows">
                <label class="calc2-field"><span class="calc2-field__label">Koszt wody <i class="calc2-info" tabindex="0" aria-label="Koszt zakupu 1 m³ wody." data-tip="Koszt zakupu 1 m³ wody.">i</i></span><span class="calc2-input"><input type="number" name="sk_water" value="6" min="0" step="0.5" inputmode="decimal"><em>zł/m³</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Koszt ścieków <i class="calc2-info" tabindex="0" aria-label="Koszt odprowadzenia 1 m³ ścieków." data-tip="Koszt odprowadzenia 1 m³ ścieków.">i</i></span><span class="calc2-input"><input type="number" name="sk_sewage" value="6" min="0" step="0.5" inputmode="decimal"><em>zł/m³</em></span></label>
              </div>
            </div>
          </section>
        </div>

        <aside class="calc2-result" aria-live="polite">
          <header class="calc2-result__header">
            <span class="calc2-section-brand calc2-section-brand--mark" aria-hidden="true"></span>
            <span><strong>Wynik kalkulacji</strong><small>Roczny potencjał ograniczenia kosztów</small></span>
          </header>
          <span class="panel-kicker">Łączny potencjał oszczędności</span>
          <strong data-calc-total>0 zł</strong>
          <span class="calc2-accent" aria-hidden="true"></span>
          <p class="calc2-result-sub" data-calc-message>Uzupełnij dane, aby zobaczyć potencjał oszczędności.</p>
          <div class="calc2-split">
            <div><span class="calc2-split__val" data-calc-scale>0 zł</span><span class="calc2-split__lbl">odkamienienie (energia)</span></div>
            <div><span class="calc2-split__val calc2-split__val--alt" data-calc-salt>0 zł</span><span class="calc2-split__lbl">zatężenie (woda + ścieki)</span></div>
          </div>
          <div class="calc2-bar" role="img" aria-label="Udział oszczędności: odkamienienie i zatężenie">
            <span class="calc2-bar__seg calc2-bar__seg--scale" data-calc-bar-scale style="--segment-scale:.5"></span>
            <span class="calc2-bar__seg calc2-bar__seg--salt" data-calc-bar-salt style="--segment-scale:.5"></span>
          </div>
          <div class="calc2-legend">
            <span class="calc2-legend__item"><i class="calc2-dot calc2-dot--scale"></i>odkamienienie</span>
            <span class="calc2-legend__item"><i class="calc2-dot calc2-dot--salt"></i>zatężenie</span>
          </div>
          <ul class="calc2-mlist">
            <li><span class="calc2-mlist__lbl" data-calc-m1l>—</span><span class="calc2-mlist__val" data-calc-m1>—</span></li>
            <li><span class="calc2-mlist__lbl" data-calc-m2l>—</span><span class="calc2-mlist__val" data-calc-m2>—</span></li>
            <li><span class="calc2-mlist__lbl" data-calc-m3l>—</span><span class="calc2-mlist__val" data-calc-m3>—</span></li>
          </ul>
          <a class="btn calc2-cta btn-arrow" href="/bezplatna-konsultacja/">Zweryfikuj wynik z inżynierem</a>
          <p class="calc2-disclaimer">Wyliczenie modelowe oparte o praktykę eksploatacyjną oraz zależności HVAC/ASHRAE. Konkretne działania i ich efekt potwierdzamy audytem technicznym.</p>
        </aside>
      </div>
    </form>
  </div>
</section>
"""),
    custom("""
<section class="branches-method calc-page-method reveal" id="metoda-obliczen" aria-labelledby="calc-method-title" data-scroll-fly>
  <div class="wrap branches-method__grid">
    <div data-fly="left">
      <p class="branches-kicker">Metoda obliczeń</p>
      <h2 id="calc-method-title"><span>Od danych wejściowych</span> <span>do wyniku, który da się zweryfikować.</span></h2>
      <p>Kalkulator nie zastępuje pomiarów z instalacji. Porządkuje jednak najważniejsze zależności i pokazuje, gdzie mogą powstawać koszty związane z osadem, energią oraz gospodarką wodno-ściekową.</p>
    </div>
    <ol class="branches-method__steps">
      <li data-fly="right"><strong>Dane instalacji</strong><span>Wybierasz kocioł parowy albo skraplacz wyparny i wpisujesz moc, czas pracy oraz parametry osadu.</span></li>
      <li data-fly="right" data-fly-delay="0.04"><strong>Dwa źródła strat</strong><span>Model oddzielnie szacuje koszt gorszej wymiany ciepła oraz potencjał ograniczenia odsalania i zużycia wody.</span></li>
      <li data-fly="right" data-fly-delay="0.08"><strong>Wynik do audytu</strong><span>Otrzymujesz roczny potencjał finansowy i techniczne wskaźniki, które warto potwierdzić na danych eksploatacyjnych.</span></li>
    </ol>
  </div>
</section>

<section class="branch-chapter calc-page-reading reveal" id="interpretacja-wyniku" aria-labelledby="calc-reading-title" data-scroll-fly>
  <div class="wrap branch-chapter__grid">
    <figure class="branch-chapter__media">
      <img src="/assets/industries/industry-cold-storage.jpg" alt="Przemysłowe skraplacze wyparne i instalacja chłodnicza zakładu" loading="lazy">
    </figure>
    <div class="branch-chapter__copy">
      <p class="branches-kicker" data-fly="right">Interpretacja wyniku</p>
      <h2 id="calc-reading-title" data-fly="right" data-fly-delay="0.02"><span>Wynik jest początkiem decyzji.</span> <span>Nie gotową ofertą.</span></h2>
      <p data-fly="right" data-fly-delay="0.05">Wysoki potencjał wskazuje obszar, który warto sprawdzić w pierwszej kolejności. Dopiero pomiary, bilans mediów i stan instalacji pozwalają potwierdzić realny zakres usprawnień.</p>
      <div class="branch-matrix" data-fly="right" data-fly-delay="0.08">
        <article><h3>Co pokazuje kalkulator</h3><p>Potencjał ograniczenia kosztów energii, wody i ścieków w skali roku.</p></article>
        <article><h3>Czego nie zastępuje</h3><p>Pomiaru osadu, analizy wody, bilansu przepływów, oceny automatyki i rzeczywistego profilu obciążenia.</p></article>
        <article><h3>Co potwierdza audyt</h3><p>Stan bazowy, wykonalne działania, realny efekt ekonomiczny, sposób wdrożenia i parametry do monitorowania.</p></article>
      </div>
      <div class="branch-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Zweryfikuj wynik z inżynierem</a><a class="branches-link" href="#faq-kalkulatora">Przejdź do FAQ</a></div>
    </div>
  </div>
</section>

<section class="branches-proof consult-branches-faq calc-page-faq reveal" id="faq-kalkulatora" aria-labelledby="calc-faq-title" data-scroll-fly>
  <div class="wrap consult-branches-faq__layout">
    <div class="consult-branches-faq__intro" data-fly="left">
      <p class="branches-proof__eyebrow">Weryfikacja wyniku</p>
      <h2 id="calc-faq-title" class="branches-proof__intro"><span>Co decyduje</span> <span>o wiarygodności wyniku?</span></h2>
      <p class="branches-proof__lead">Konkretne odpowiedzi o jakości danych, ograniczeniach modelu i momencie, w którym kalkulację trzeba potwierdzić pomiarem lub audytem.</p>
    </div>
    <div class="consult-branches-faq__list" data-fly="right">
      <details>
        <summary>Co dokładnie obejmuje wynik rocznych oszczędności?</summary>
        <p>Wynik sumuje dwa składniki: koszt energii traconej przez kamień lub osad oraz potencjał wynikający z ograniczenia odsalania, czyli zużycia wody, ścieków, a w kotle także strat ciepła. Pokazuje wartość dla podanych godzin pracy i cen mediów, a nie gwarantowaną kwotę oszczędności.</p>
      </details>
      <details>
        <summary>Które dane mają największy wpływ na wynik dla kotła parowego?</summary>
        <p>Na część energetyczną najmocniej wpływają moc kotła, czas pracy, cena gazu i grubość kamienia. Potencjał ograniczenia odsalania zależy przede wszystkim od produkcji pary, czasu pracy oraz kosztów gazu, wody i ścieków.</p>
      </details>
      <details>
        <summary>Które dane mają największy wpływ na wynik dla skraplacza wyparnego?</summary>
        <p>Kluczowe są moc chłodnicza, roczny czas pracy, cena energii oraz różnica między średnicą czystej wężownicy a średnicą z osadem. Koszty wody i ścieków decydują o wartości potencjalnego ograniczenia odsalania.</p>
      </details>
      <details>
        <summary>Jak wiarygodnie określić grubość kamienia lub osadu?</summary>
        <p>Najlepiej wykorzystać pomiar wykonany podczas postoju, dokumentację z ostatniego czyszczenia albo różnicę średnic wężownicy. Gdy nie ma pomiaru, warto policzyć kilka scenariuszy grubości zamiast traktować jedną wartość jako pewną.</p>
      </details>
      <details>
        <summary>Czy kalkulator uwzględnia zmienne obciążenie instalacji w ciągu roku?</summary>
        <p>Nie w pełni. Model używa jednej wartości mocy i łącznej liczby godzin pracy, dlatego przy dużych zmianach obciążenia dokładniejszy wynik wymaga danych miesięcznych lub godzinowych z systemu monitoringu.</p>
      </details>
      <details>
        <summary>Dlaczego wynik może różnić się od audytu?</summary>
        <p>Audyt uwzględnia rzeczywiste obciążenie, jakość wody, automatykę, stan powierzchni wymiany ciepła i historię pracy instalacji, których model kalkulatora nie opisuje w pełni.</p>
      </details>
      <details>
        <summary>Kiedy kalkulację należy potwierdzić pomiarem lub audytem?</summary>
        <p>Zawsze przed zatwierdzeniem budżetu, zmianą programu chemicznego, czyszczeniem instalacji lub przyjęciem oszczędności do planu inwestycyjnego. Pomiar potwierdza stan powierzchni, parametry wody i rzeczywisty profil pracy urządzenia.</p>
      </details>
      <details>
        <summary>Jakie dane przygotować do weryfikacji wyniku z inżynierem?</summary>
        <p>Najbardziej użyteczne są dane z ostatnich 12 miesięcy: zużycie paliwa lub energii, godziny pracy, produkcja pary albo obciążenie chłodnicze, zużycie wody, ilość ścieków i wyniki analiz wody. Warto dołączyć także historię czyszczeń, nastawy automatyki i aktualne stawki za media.</p>
      </details>
      <details>
        <summary>Czy wynik można wykorzystać przy planowaniu białego certyfikatu?</summary>
        <p>Tak, jako wstępny sygnał, że przedsięwzięcie warto przeanalizować. Do formalnej oceny potrzebne są jednak dane bazowe, metodyka obliczeń, pomiary i audyt efektywności energetycznej.</p>
      </details>
    </div>
  </div>
</section>

<section class="branches-final calc-page-final reveal" aria-labelledby="calc-final-title">
  <div class="wrap branches-final__inner">
    <span class="branches-final__sigil" aria-hidden="true"></span>
    <h2 id="calc-final-title"><span>Wspólna weryfikacja</span> <span>potencjału oszczędności w Państwa instalacji.</span></h2>
    <p>Inżynier Kabi-Chemie przeanalizuje przyjęte założenia, wskaże potrzebne pomiary i pomoże ocenić rozwiązania najlepiej dopasowane do warunków pracy Państwa zakładu.</p>
    <div class="branches-final__actions">
      <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację techniczną</a>
      <a class="branches-link" href="/bezplatna-konsultacja/">Poznaj zakres audytu technicznego</a>
    </div>
  </div>
</section>
"""),
]}

_S = SITE
_BR = SITE["branch"]
PAGES["/kontakt/"] = {"body_class": "has-dark-hero firm-page firm-contact-page", "sections": [
    custom(f"""
<section class="firm-hero firm-hero--contact" style="--firm-bg:url('/assets/industries/industry-cold-storage.jpg')" id="kontakt-top">
  <div class="firm-hero__shade" aria-hidden="true"></div>
  <div class="wrap firm-hero__inner">
    <div class="firm-hero__copy reveal-left">
      <p class="firm-kicker">Kontakt z inżynierem Kabi-Chemie</p>
      <h1>Opisz instalację. Wskażemy kolejny krok.</h1>
      <p>Masz problem z kamieniem, korozją, przewodnością, biofilmem albo zbyt wysokim zużyciem wody? Skontaktuj się z nami, a inżynier Kabi-Chemie pomoże szybko uporządkować temat.</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="tel:{_S['phone_raw']}">Zadzwoń: {_S['phone']}</a>
        <a class="btn btn-ghost-light" href="#kontakt-form">Napisz wiadomość</a>
      </div>
    </div>
    <div class="firm-contact-panel reveal-right" aria-label="Bezpośrednie dane kontaktowe">
      <a href="tel:{_S['phone_raw']}"><span>Telefon</span><strong>{_S['phone']}</strong></a>
      <a href="mailto:{_S['email']}"><span>E-mail</span><strong>{_S['email']}</strong></a>
      <p><span>Godziny</span><strong>pn-pt, 7:00-16:00</strong></p>
    </div>
  </div>
</section>

<section class="firm-contact-main" id="kontakt-form">
  <div class="wrap firm-contact-main__grid">
    <div class="firm-contact-main__copy reveal">
      <p class="firm-kicker">Dane i lokalizacje</p>
      <h2>Dwie lokalizacje. Jeden zespół techniczny.</h2>
      <p>Zgłoszenie trafi do osoby, która rozumie instalacje przemysłowe i może od razu zapytać o właściwe parametry.</p>
      <div class="firm-contact-lines">
        <address>
          <span>Siedziba główna</span>
          <strong>{_S['company']}</strong>
          <em>{_S['address']}</em>
          <a href="tel:{_S['phone_raw']}">{_S['phone']}</a>
          <a href="mailto:{_S['email']}">{_S['email']}</a>
        </address>
        <address>
          <span>{_BR['name']}</span>
          <strong>{_BR['contact']}</strong>
          <em>Obsługa północnej Polski</em>
          <a href="tel:{_BR['phone_raw']}">{_BR['phone']}</a>
          <a href="mailto:{_BR['email']}">{_BR['email']}</a>
        </address>
      </div>
    </div>
    <form class="contact-form contact-form--smart kontakt-form firm-contact-form reveal" data-email="{_S['email']}" novalidate>
      <div class="consult-form-head">
        <strong>Krótki formularz kontaktowy</strong>
        <span>około 30 sekund</span>
      </div>
      <div class="field field--identity">
        <label for="kontakt-identity">Firma / imię i nazwisko <span class="field-meta">wymagane</span></label>
        <input id="kontakt-identity" name="identity" autocomplete="name organization" required placeholder="np. ABC Sp. z o.o., Jan Kowalski">
        <p class="field-hint">Wpisz nazwę firmy i osobę, do której mamy oddzwonić.</p>
      </div>
      <div class="contact-form__row">
        <div class="field field--phone">
          <label for="kontakt-phone">Telefon <span class="field-meta">wymagane</span></label>
          <input id="kontakt-phone" name="phone" type="tel" autocomplete="tel" required placeholder="np. 600 000 000">
        </div>
        <div class="field field--email">
          <label for="kontakt-email">Adres e-mail <span class="field-meta">opcjonalne</span></label>
          <input id="kontakt-email" name="email" type="email" autocomplete="email" placeholder="np. biuro@firma.pl">
        </div>
      </div>
      <div class="field field--message">
        <label for="kontakt-message">Wiadomość <span class="field-meta">opcjonalne</span></label>
        <textarea id="kontakt-message" name="message" rows="4" aria-describedby="kontakt-message-hint" placeholder="Napisz krótko, czego dotyczy sprawa lub jaki typ instalacji mamy omówić."></textarea>
        <p id="kontakt-message-hint" class="field-hint">Możesz dopisać typ instalacji, problem, preferowany termin kontaktu albo dodatkowy kontekst techniczny.</p>
      </div>
      <div class="form-consents" aria-label="Zgody i informacje prawne">
        <label class="form-consent form-consent--required" for="kontakt-privacy-consent">
          <input id="kontakt-privacy-consent" name="privacyConsent" type="checkbox" required>
          <span>Zgadzam się na kontakt w sprawie zapytania zgodnie z <a href="/polityka-prywatnosci/">polityką prywatności</a>. <span class="form-consent__tag">wymagane</span></span>
        </label>
      </div>
      <button type="submit" class="btn btn-primary">Wyślij zapytanie</button>
      <p class="form-note" role="status" aria-live="polite" hidden></p>
    </form>
  </div>
</section>

<section class="firm-river firm-river--light" data-scroll-fly>
  <div class="wrap">
    <div class="firm-section-head" data-fly="left">
      <p class="firm-kicker">Jak przebiega kontakt</p>
      <h2>Krótki kontakt techniczny bez presji zakupowej.</h2>
    </div>
    <ol class="firm-river__list">
      <li data-fly="right"><span>01</span><strong>Zostawiasz wiadomość lub dzwonisz</strong><p>Wystarczy jeden objaw albo typ instalacji.</p></li>
      <li data-fly="right" data-fly-delay="0.05"><span>02</span><strong>Oddzwaniamy w 24 h w dni robocze</strong><p>Dopytujemy o parametry i ustalamy, czy potrzebny jest audyt.</p></li>
      <li data-fly="right" data-fly-delay="0.1"><span>03</span><strong>Rekomendujemy kolejny krok</strong><p>Może to być analiza wody, wizyta, dobór programu albo prosta korekta eksploatacji.</p></li>
    </ol>
  </div>
</section>
"""),
]}

# ================================================================== ROZWIAZANIA I USLUGI: PRZEMODELOWANE PODKARTY
PAGES["/ochrona-antykorozyjna/"] = {"body_class": "has-dark-hero firm-page solution-page solution-page--corrosion", "sections": [
    custom("""
<section class="solution-hero solution-hero--corrosion" style="--solution-bg:url('/assets/blog/blog-corrosion-pipes.png')" id="top">
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner">
    <div class="solution-hero__copy reveal-left">
      <p class="firm-kicker">Ochrona antykorozyjna KCAQUA</p>
      <h1>Program antykorozyjny dla instalacji przemysłowych.</h1>
      <p>Diagnozujemy źródło korozji, dobieramy chemię i prowadzimy parametry wody tak, aby instalacja pracowała stabilnie przez cały sezon.</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="/kontakt/">Umów konsultację</a>
        <a class="btn btn-ghost-light" href="/baza-wiedzy/korozja/">Zobacz wiedzę o korozji</a>
      </div>
    </div>
    <aside class="solution-hero__panel reveal-right" aria-label="Najważniejsze efekty programu">
      <div><span>Cel</span><strong>Mniej rdzy, mniej osadów i niższe ryzyko awarii.</strong></div>
      <div><span>Zakres</span><strong>Kotłownie, obiegi chłodnicze, rurociągi i wymienniki.</strong></div>
      <div><span>Efekt</span><strong>Stabilna woda i przewidywalny serwis instalacji.</strong></div>
    </aside>
  </div>
</section>

<section class="solution-scan solution-scan--white" data-scroll-fly>
  <div class="wrap solution-scan__grid">
    <div class="solution-scan__copy" data-fly="left">
      <p class="firm-kicker">Od przyczyny do programu</p>
      <h2>Najpierw rozpoznajemy mechanizm korozji.</h2>
      <p>Korozja w instalacji rzadko ma jedną przyczynę. Sprawdzamy tlen, pH, przewodność, osady, temperaturę i miejsca, w których woda traci stabilność.</p>
      <ul class="solution-scan__list">
        <li><strong>Korozja tlenowa</strong><span>kontrola odtleniania, szczelności i warunków pracy kotłowni.</span></li>
        <li><strong>Korozja podosadowa</strong><span>usuwanie osadów, które blokują chemię i przyspieszają degradację metalu.</span></li>
        <li><strong>Biała korozja</strong><span>ochrona elementów ocynkowanych w skraplaczach i wieżach chłodniczych.</span></li>
        <li><strong>Korozja po montażu</strong><span>pasywacja nowych instalacji przed pełnym obciążeniem produkcyjnym.</span></li>
      </ul>
    </div>
    <figure class="solution-scan__visual" data-fly="right">
      <img src="/assets/impact/impact-04-installation-protection.png" alt="Ochrona instalacji przemysłowej przed korozją">
      <figcaption>Program obejmuje wodę, metal, dozowanie i monitoring parametrów.</figcaption>
    </figure>
  </div>
</section>

<section class="solution-lines solution-lines--dark" data-scroll-fly>
  <div class="wrap solution-lines__grid">
    <div class="firm-section-head" data-fly="left">
      <p class="firm-kicker">Co wdrażamy</p>
      <h2>Program ochrony dobrany do realnej pracy instalacji.</h2>
      <p>Nie sprzedajemy jednej recepty dla każdej wody. Dobieramy zakres prac do typu instalacji, materiału, temperatury i ryzyka przestoju.</p>
    </div>
    <ol class="solution-steps">
      <li data-fly="right"><span>01</span><strong>Pasywacja stali</strong><p>Zabezpieczamy nowe elementy i instalacje po czyszczeniu, zanim korozja zacznie pracować pod osadem.</p></li>
      <li data-fly="right" data-fly-delay="0.05"><span>02</span><strong>Inhibitory korozji</strong><p>Dobieramy preparaty do obiegu, jakości wody i temperatury pracy.</p></li>
      <li data-fly="right" data-fly-delay="0.1"><span>03</span><strong>Czyszczenie chemiczne</strong><p>Usuwamy osady, które ograniczają wymianę ciepła i tworzą ogniska korozji.</p></li>
      <li data-fly="right" data-fly-delay="0.15"><span>04</span><strong>Monitoring parametrów</strong><p>Ustalamy zakres kontroli, aby utrzymać ochronę po wdrożeniu programu.</p></li>
    </ol>
  </div>
</section>

<section class="solution-index">
  <div class="wrap">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Najczęstsze scenariusze</p>
      <h2>Wybierz temat najbliższy Twojej instalacji.</h2>
    </div>
    <div class="solution-link-rows">
      <a class="reveal" href="/ochrona-antykorozyjna/pasywacja-stali/"><span>Pasywacja stali</span><strong>dla nowych instalacji, remontów i uruchomień po czyszczeniu.</strong><em>sprawdź</em></a>
      <a class="reveal" href="/ochrona-antykorozyjna/chemiczne-czyszczenie/"><span>Czyszczenie chemiczne</span><strong>gdy osad zasłania powierzchnię wymiany ciepła i podnosi ryzyko korozji.</strong><em>sprawdź</em></a>
      <a class="reveal" href="/kotly-parowe/ochrona-antykorozyjna/"><span>Kotły parowe</span><strong>ochrona przed korozją w układach parowych i kondensacie.</strong><em>sprawdź</em></a>
    </div>
  </div>
</section>

<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Masz ślady rdzy lub częste awarie?</p>
        <h2>Opisz objawy korozji. Wskażemy pierwszy krok.</h2>
        <p>Wystarczy typ instalacji, miejsce problemu i informacja, kiedy pojawia się korozja.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/kontakt/">Skontaktuj się z nami</a>
        <a class="consult-final__tel" href="tel:+48662792875"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg><span>+48 662 792 875</span></a>
      </div>
    </div>
  </div>
</section>
"""),
]}

PAGES["/odkamienianie-instalacji/"] = {"body_class": "has-dark-hero firm-page solution-page solution-page--descaling", "sections": [
    custom("""
<section class="solution-hero solution-hero--descaling" style="--solution-bg:url('/assets/blog/blog-boiler-scale.png')" id="top">
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner">
    <div class="solution-hero__copy reveal-left">
      <p class="firm-kicker">Odkamienianie instalacji przemysłowych</p>
      <h1>Usuwamy kamień bez zgadywania kosztów.</h1>
      <p>Czyścimy rurociągi, wymienniki, skraplacze, kotły i obiegi technologiczne. Dobieramy chemię do osadu, materiału i ryzyka postoju.</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="/kontakt/">Zgłoś instalację do oceny</a>
        <a class="btn btn-ghost-light" href="/kotly-parowe/odkamienianie/">Odkamienianie kotłów</a>
      </div>
    </div>
    <aside class="solution-hero__panel solution-hero__panel--meter reveal-right">
      <div><span>Sygnał</span><strong>Spadek przepływu lub wydajności wymiany ciepła.</strong></div>
      <div><span>Ryzyko</span><strong>Wyższe zużycie energii, przegrzanie i nieplanowany postój.</strong></div>
      <div><span>Rezultat</span><strong>Czystsza powierzchnia wymiany i łatwiejsza kontrola parametrów.</strong></div>
    </aside>
  </div>
</section>

<section class="solution-scan solution-scan--white" data-scroll-fly>
  <div class="wrap solution-scan__grid solution-scan__grid--reverse">
    <figure class="solution-scan__visual" data-fly="left">
      <img src="/assets/impact/impact-03-energy-reduction.jpeg" alt="Instalacja przemysłowa po optymalizacji wymiany ciepła">
      <figcaption>Każde czyszczenie planujemy pod proces, nie pod sam osad.</figcaption>
    </figure>
    <div class="solution-scan__copy" data-fly="right">
      <p class="firm-kicker">Kiedy warto działać</p>
      <h2>Kamień szybko zmienia koszt pracy instalacji.</h2>
      <p>Wczesna diagnoza pozwala zaplanować czyszczenie bez nerwowego zatrzymania produkcji. Najczęściej zaczynamy od analizy wody i objawów z ruchu.</p>
      <ul class="solution-scan__list">
        <li><strong>Niższy przepływ</strong><span>pompy pracują ciężej, a instalacja reaguje wolniej na obciążenie.</span></li>
        <li><strong>Gorsza wymiana ciepła</strong><span>ten sam efekt wymaga większej ilości energii.</span></li>
        <li><strong>Częste alarmy</strong><span>temperatura, ciśnienie lub przewodność zaczynają wychodzić poza stabilny zakres.</span></li>
        <li><strong>Osad po rozruchu</strong><span>nowa lub remontowana instalacja wnosi zanieczyszczenia do obiegu.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="solution-process">
  <div class="wrap">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Przebieg czyszczenia</p>
      <h2>Instalacja wraca do pracy z jasnym raportem.</h2>
    </div>
    <ol class="solution-process__rail">
      <li class="reveal"><span>01</span><strong>Rozpoznanie osadu</strong><p>Analizujemy wodę, objawy i historię pracy instalacji.</p></li>
      <li class="reveal"><span>02</span><strong>Dobór chemii</strong><p>Dobieramy preparat do materiału, osadu i bezpiecznego zakresu pracy.</p></li>
      <li class="reveal"><span>03</span><strong>Obieg czyszczący</strong><p>Prowadzimy proces z kontrolą parametrów i czasu kontaktu.</p></li>
      <li class="reveal"><span>04</span><strong>Płukanie i neutralizacja</strong><p>Domykamy czyszczenie tak, aby instalacja mogła wrócić do normalnej pracy.</p></li>
      <li class="reveal"><span>05</span><strong>Rekomendacja</strong><p>Wskazujemy, jak ograniczyć powrót kamienia w kolejnym sezonie.</p></li>
    </ol>
  </div>
</section>

<section class="solution-index solution-index--compact">
  <div class="wrap solution-index__grid">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Zakres prac</p>
      <h2>Usuwamy osad podnoszący koszt produkcji.</h2>
    </div>
    <div class="solution-link-rows">
      <a class="reveal" href="/uklady-chlodnicze/odkamienianie/"><span>Układy chłodnicze</span><strong>skraplacze, wieże chłodnicze i obiegi z osadami mineralnymi.</strong><em>zobacz</em></a>
      <a class="reveal" href="/kotly-parowe/odkamienianie/"><span>Kotły parowe</span><strong>czyszczenie powierzchni wymiany ciepła i wsparcie programu wody kotłowej.</strong><em>zobacz</em></a>
      <a class="reveal" href="/uslugi/analiza-wody/"><span>Analiza wody</span><strong>sprawdzenie przyczyn narastania kamienia przed doborem chemii.</strong><em>zobacz</em></a>
    </div>
  </div>
</section>

<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Nie wiesz, czy to już czas na czyszczenie?</p>
        <h2>Prześlij objawy. Ocenimy zakres działania.</h2>
        <p>Najczęściej prosimy o typ instalacji, zdjęcia osadu i ostatnie parametry wody.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/kontakt/">Poproś o ocenę</a>
        <a class="consult-final__tel" href="/bezplatna-konsultacja/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>bezpłatna konsultacja</span></a>
      </div>
    </div>
  </div>
</section>
"""),
]}

PAGES["/uslugi/analiza-wody/"] = {"body_class": "has-dark-hero firm-page solution-page solution-page--boilers service-analysis-page", "sections": [
    custom("""
<section class="solution-hero" id="top" style="--solution-image:url('/assets/impact/impact-02-effluent-control.jpeg'); --solution-position:center center">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner">
    <div class="solution-hero__copy">
      <p class="solution-kicker"><span></span>Usługi / Analiza wody</p>
      <h1>Badamy wodę <span>przed awarią instalacji.</span></h1>
      <p class="solution-hero__lead">Analiza wody przemysłowej pomaga szybko zobaczyć, czy instalacja pracuje stabilnie. Wynik przekładamy na konkretne decyzje dla kotłowni, chłodnictwa i RO.</p>
      <div class="solution-hero__actions">
        <a class="btn btn-primary" href="/kontakt/">Zleć analizę wody</a>
        <a class="solution-text-link" href="/baza-wiedzy/parametry-wody/">Poznaj parametry wody <span aria-hidden="true">↗</span></a>
      </div>
      <ul class="solution-hero__signals" aria-label="Najważniejsze obszary">
        <li class="has-icon"><span class="solution-hero__signal-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/><path d="M12 7.5v5l3.5 2"/></svg></span><span>Utrzymanie ruchu i produkcja</span></li>
        <li class="has-icon"><span class="solution-hero__signal-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4A2 2 0 0 0 19 18l-5-9V3"/><path d="M7.5 16h9"/><path d="m9.4 12.8 1.6 1.2 2.2-2 2 1.3"/></svg></span><span>Diagnoza kamienia i korozji</span></li>
        <li class="has-icon"><span class="solution-hero__signal-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3h10v18H7z"/><path d="M9.5 7h5M9.5 11h5M9.5 15h2.5"/><path d="m13.6 16.1 1.2 1.2 2.3-2.5"/></svg></span><span>Raport z rekomendacją</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="lab-intro">
  <div class="wrap lab-intro__grid">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Co sprawdzamy</p>
      <h2>Parametry dobieramy do instalacji.</h2>
      <p>Inaczej czytamy wodę kotłową, inaczej wodę w skraplaczu, a jeszcze inaczej układ RO. Dlatego wynik zawsze łączymy z kontekstem procesu.</p>
    </div>
    <div class="lab-matrix reveal" aria-label="Najważniejsze parametry badania wody">
      <div><span>pH</span><strong>kontrola kierunku korozji i zasadowości</strong><em>ryzyko agresywnej wody</em></div>
      <div><span>Twardość</span><strong>ocena narastania kamienia</strong><em>spadek wymiany ciepła</em></div>
      <div><span>Przewodność</span><strong>kontrola zasolenia i odsalania</strong><em>niestabilna praca obiegu</em></div>
      <div><span>Żelazo</span><strong>sygnał korozji i transportu osadów</strong><em>zatykanie, rdza, brudny kondensat</em></div>
      <div><span>Chlorki</span><strong>ocena agresywności wody</strong><em>korozja miejscowa</em></div>
      <div><span>TDS</span><strong>kontrola całkowitej ilości substancji rozpuszczonych</strong><em>zrzuty, ścieki i koszty wody</em></div>
    </div>
  </div>
</section>

<section class="solution-lines solution-lines--dark" data-scroll-fly>
  <div class="wrap solution-lines__grid">
    <div class="firm-section-head" data-fly="left">
      <p class="firm-kicker">Od próbki do decyzji</p>
      <h2>Wynik badania prowadzi do działania.</h2>
      <p>Po analizie wskazujemy, czy problem wymaga korekty dozowania, czyszczenia, pasywacji, zmiany prowadzenia wody lub dodatkowego audytu.</p>
    </div>
    <ol class="solution-steps">
      <li data-fly="right"><span>01</span><strong>Pobór próbki</strong><p>Ustalamy miejsce poboru i typ instalacji, aby wynik miał sens techniczny.</p></li>
      <li data-fly="right" data-fly-delay="0.05"><span>02</span><strong>Pomiar parametrów</strong><p>Sprawdzamy najważniejsze wskaźniki dla wody kotłowej, chłodniczej lub technologicznej.</p></li>
      <li data-fly="right" data-fly-delay="0.1"><span>03</span><strong>Interpretacja</strong><p>Łączymy liczby z objawami, pracą instalacji i kosztami eksploatacji.</p></li>
      <li data-fly="right" data-fly-delay="0.15"><span>04</span><strong>Rekomendacja</strong><p>Przekazujemy jasny kolejny krok, bez nadmiaru laboratoryjnego żargonu.</p></li>
    </ol>
  </div>
</section>

<section class="solution-report">
  <div class="wrap solution-report__grid">
    <div class="solution-report__copy reveal">
      <p class="firm-kicker">Co otrzymujesz</p>
      <h2>Raport czytelny dla technika i zarządu.</h2>
      <p>W raporcie pokazujemy parametry, ryzyka i rekomendacje. Dzięki temu łatwiej uzasadnić działania w utrzymaniu ruchu, produkcji i zakupach.</p>
    </div>
    <div class="solution-report__lines">
      <p class="reveal"><strong>Stan wody</strong><span>wyniki pomiarów z krótkim komentarzem technicznym.</span></p>
      <p class="reveal"><strong>Ryzyko dla instalacji</strong><span>kamień, korozja, biofilm, przewodność, zrzuty i strata energii.</span></p>
      <p class="reveal"><strong>Kolejny krok</strong><span>korekta chemii, audyt, czyszczenie lub regularny monitoring.</span></p>
    </div>
  </div>
</section>

<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Masz aktualne wyniki wody?</p>
        <h2>Wyślij parametry. Pomożemy je odczytać.</h2>
        <p>Możesz też zamówić analizę, jeśli nie masz pewnych danych z ostatnich pomiarów.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/kontakt/">Wyślij zapytanie</a>
        <a class="consult-final__tel" href="tel:+48662792875"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg><span>+48 662 792 875</span></a>
      </div>
    </div>
  </div>
</section>
"""),
]}

PAGES["/uslugi/audyt-techniczny/"] = {"body_class": "has-dark-hero firm-page solution-page solution-page--boilers service-audit-page", "sections": [
    custom("""
<section class="solution-hero" id="top" style="--solution-image:url('/assets/industries/industry-heavy.jpg'); --solution-position:center center">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner">
    <div class="solution-hero__copy">
      <p class="solution-kicker"><span></span>Usługi / Audyt techniczny</p>
      <h1>Sprawdzamy instalację <span>i realne miejsca strat.</span></h1>
      <p class="solution-hero__lead">Audyt pokazuje, gdzie zakład traci wodę, energię, stabilność parametrów lub czas serwisu. Po wizycie otrzymujesz jasną rekomendację dalszych działań.</p>
      <div class="solution-hero__actions">
        <a class="btn btn-primary" href="/kontakt/">Umów audyt</a>
        <a class="solution-text-link" href="/kalkulator-oszczednosci/">Policz potencjał oszczędności <span aria-hidden="true">↗</span></a>
      </div>
      <ul class="solution-hero__signals" aria-label="Najważniejsze obszary">
        <li class="has-icon"><span class="solution-hero__signal-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/><path d="M8 10.5h5M10.5 8v5"/></svg></span><span>Rozmowa, oględziny i pomiary</span></li>
        <li class="has-icon"><span class="solution-hero__signal-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h9"/><circle cx="8" cy="6" r="1.6"/><circle cx="15" cy="12" r="1.6"/><circle cx="6.5" cy="18" r="1.6"/></svg></span><span>Kotłownie, chłodnictwo i RO</span></li>
        <li class="has-icon"><span class="solution-hero__signal-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V9M10 20V4M16 20v-7M22 20H2"/><path d="M4 9 10 4l6 9 6-6"/></svg></span><span>Priorytety kosztów i ryzyka</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="solution-flow">
  <div class="wrap solution-flow__grid">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Jak pracujemy</p>
      <h2>Audyt ma dać decyzję.</h2>
      <p>Patrzymy na instalację z perspektywy utrzymania ruchu i kosztów. Łączymy pomiary z pracą urządzeń, aby wskazać działania o największym sensie biznesowym.</p>
    </div>
    <ol class="solution-flow__steps">
      <li class="reveal"><span>01</span><strong>Rozmowa i kontekst</strong><p>Ustalamy typ instalacji, objawy, historię awarii i cele zakładu.</p></li>
      <li class="reveal"><span>02</span><strong>Oględziny instalacji</strong><p>Sprawdzamy punkty dozowania, zrzuty, wymienniki, armaturę i miejsca ryzyka.</p></li>
      <li class="reveal"><span>03</span><strong>Pomiary wody</strong><p>Porównujemy parametry z warunkami pracy i obecnym programem chemicznym.</p></li>
      <li class="reveal"><span>04</span><strong>Ocena strat</strong><p>Szukamy kosztów ukrytych w wodzie, energii, ściekach i częstym serwisie.</p></li>
      <li class="reveal"><span>05</span><strong>Plan działania</strong><p>Przekazujemy priorytety, zakres wdrożenia i sposób kontroli efektów.</p></li>
    </ol>
  </div>
</section>

<section class="solution-scan solution-scan--white" data-scroll-fly>
  <div class="wrap solution-scan__grid">
    <div class="solution-scan__copy" data-fly="left">
      <p class="firm-kicker">Co obejmuje audyt</p>
      <h2>Sprawdzamy elementy decydujące o kosztach.</h2>
      <ul class="solution-scan__list">
        <li><strong>Parametry wody</strong><span>twardość, pH, przewodność, żelazo, TDS i ryzyko kamienia.</span></li>
        <li><strong>Dozowanie chemii</strong><span>miejsce dozowania, dawka, automatyka i powtarzalność pracy.</span></li>
        <li><strong>Stan instalacji</strong><span>ślady korozji, osady, biofilm, zabrudzenia i punkty zastoju.</span></li>
        <li><strong>Koszty eksploatacji</strong><span>woda, ścieki, energia, częstotliwość awarii i czas obsługi.</span></li>
      </ul>
    </div>
    <figure class="solution-scan__visual" data-fly="right">
      <img src="/assets/industries/industry-cold-storage.jpg" alt="Audyt techniczny instalacji chłodniczej i przemysłowej">
      <figcaption>Audyt porządkuje decyzje techniczne przed zmianą chemii lub serwisem.</figcaption>
    </figure>
  </div>
</section>

<section class="solution-report solution-report--blue">
  <div class="wrap solution-report__grid">
    <div class="solution-report__copy reveal">
      <p class="firm-kicker">Po audycie</p>
      <h2>Otrzymujesz priorytety dla utrzymania ruchu.</h2>
      <p>Raport pokazuje, co warto zrobić od razu, co zaplanować przy postoju i które parametry trzeba monitorować cyklicznie.</p>
    </div>
    <div class="solution-report__lines">
      <p class="reveal"><strong>Szybkie korekty</strong><span>ustawienia dozowania, pomiary kontrolne i proste zmiany eksploatacyjne.</span></p>
      <p class="reveal"><strong>Prace planowane</strong><span>czyszczenie, pasywacja, wymiana elementów lub modernizacja punktów dozowania.</span></p>
      <p class="reveal"><strong>Kontrola efektów</strong><span>monitoring wody, raportowanie trendów i porównanie kosztów przed oraz po wdrożeniu.</span></p>
    </div>
  </div>
</section>

<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Chcesz sprawdzić instalację bez zobowiązań?</p>
        <h2>Umów audyt i znajdź źródło strat.</h2>
        <p>W pierwszym kroku wystarczy krótki opis instalacji i problemu.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/kontakt/">Umów audyt</a>
        <a class="consult-final__tel" href="/uslugi/analiza-wody/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>analiza wody</span></a>
      </div>
    </div>
  </div>
</section>
"""),
]}

PAGES["/baza-wiedzy/"] = {"body_class": "has-dark-hero firm-page solution-page knowledge-page", "sections": [
    custom("""
<section class="solution-hero knowledge-hero" style="--solution-image:url('/assets/blog/blog-water-reduction.png'); --solution-position:center center" id="top">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner solution-hero__inner--editorial">
    <div class="solution-hero__copy reveal-left">
      <p class="firm-kicker">Baza wiedzy Kabi-Chemie</p>
      <h1>Praktyczna wiedza o wodzie przemysłowej dla decyzji technicznych.</h1>
      <p>Wyjaśniamy kamień, korozję, biofilm, membrany RO i parametry wody w języku, który pomaga działać w zakładzie produkcyjnym.</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="#artykuly">Czytaj artykuły</a>
        <a class="btn btn-ghost-light" href="/kontakt/">Zapytaj eksperta</a>
      </div>
    </div>
    <aside class="solution-hero__panel knowledge-hero__panel reveal-right">
      <div><span>Tematy</span><strong>Kotły parowe, chłodnictwo, RO, korozja i oszczędność wody.</strong></div>
      <div><span>Dla kogo</span><strong>Inżynierowie, kierownicy utrzymania ruchu i osoby decyzyjne.</strong></div>
      <div><span>Cel</span><strong>Szybciej rozpoznać problem i lepiej zaplanować działanie.</strong></div>
    </aside>
  </div>
</section>

<section class="knowledge-feature" id="artykuly">
  <div class="wrap knowledge-feature__grid">
    <a class="knowledge-feature__media reveal" href="/baza-wiedzy/kamien-kotlowy/" aria-label="Przeczytaj artykuł o kamieniu kotłowym">
      <img src="/assets/blog/blog-boiler-scale.png" alt="Kamień kotłowy i osad na powierzchni wymiany ciepła">
    </a>
    <div class="knowledge-feature__copy reveal">
      <p class="firm-kicker">Polecany temat</p>
      <h2>Dlaczego cienka warstwa kamienia potrafi podnieść koszt pracy kotła.</h2>
      <p>Pokazujemy, jak osad ogranicza wymianę ciepła, zwiększa zużycie paliwa i przyspiesza ryzyko awarii.</p>
      <a class="text-link" href="/baza-wiedzy/kamien-kotlowy/">Przeczytaj artykuł</a>
    </div>
  </div>
</section>

<section class="knowledge-index">
  <div class="wrap">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Kategorie wiedzy</p>
      <h2>Wybierz obszar instalacji do uporządkowania.</h2>
    </div>
    <nav class="knowledge-index__rows" aria-label="Kategorie bazy wiedzy">
      <a class="reveal" href="/baza-wiedzy/kotly-parowe/"><span>01</span><strong>Kotły parowe i para</strong><em>kamień, kondensat, odsalanie i ochrona przed korozją.</em></a>
      <a class="reveal" href="/baza-wiedzy/wieze-chlodnicze/"><span>02</span><strong>Wieże chłodnicze i skraplacze</strong><em>biofilm, biocydy, odkamienianie i zużycie wody.</em></a>
      <a class="reveal" href="/baza-wiedzy/korozja/"><span>03</span><strong>Korozja i ochrona metalu</strong><em>inhibitory, pasywacja, rodzaje korozji i objawy w instalacji.</em></a>
      <a class="reveal" href="/baza-wiedzy/parametry-wody/"><span>04</span><strong>Parametry wody i oszczędności</strong><em>pH, przewodność, twardość, TDS, ścieki i energia.</em></a>
      <a class="reveal" href="/baza-wiedzy/membrany-ro/"><span>05</span><strong>Membrany RO</strong><em>antyskalanty, fouling, płukanie i ochrona wydajności.</em></a>
    </nav>
  </div>
</section>

<section class="knowledge-stream">
  <div class="wrap knowledge-stream__grid">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Ostatnie materiały</p>
      <h2>Artykuły o problemach z prawdziwych instalacji.</h2>
    </div>
    <div class="knowledge-stream__list">
      <a class="reveal" href="/baza-wiedzy/biofilm-w-ukladzie-chlodniczym/"><img src="/assets/blog/blog-biofilm-cleaning.png" alt=""><span>Biofilm w układzie chłodniczym</span><strong>jak rozpoznać problem, zanim spadnie sprawność skraplacza.</strong></a>
      <a class="reveal" href="/baza-wiedzy/antyskalant-ro/"><img src="/assets/blog/blog-ro-antiscalant.png" alt=""><span>Antyskalant do membran RO</span><strong>kiedy pomaga, a kiedy maskuje problem z jakością wody.</strong></a>
      <a class="reveal" href="/baza-wiedzy/korozja/"><img src="/assets/blog/blog-corrosion-pipes.png" alt=""><span>Korozja w instalacji</span><strong>najczęstsze objawy, błędy i kierunek diagnostyki.</strong></a>
    </div>
  </div>
</section>

<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Nie widzisz swojego problemu?</p>
        <h2>Opisz instalację. Podpowiemy pierwszy temat.</h2>
        <p>Możemy wskazać artykuł, zaproponować analizę wody albo umówić krótką rozmowę z inżynierem.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/kontakt/">Zapytaj eksperta</a>
        <a class="consult-final__tel" href="/faq/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>przejdź do FAQ</span></a>
      </div>
    </div>
  </div>
</section>
"""),
]}

# ================================================================== 404
PAGES["/404/"] = {"sections": [
    hero(h1="Nie znaleziono strony (404)",
         lead="Strona nie istnieje lub adres jest nieprawidłowy. Wróć na stronę główną lub sprawdź popularne sekcje.",
         ctas=[("Strona główna", "/"), ("Kontakt", "/kontakt/")]),
    related(title="Popularne strony", items=[
        ("Kotły parowe", "/kotly-parowe/"),
        ("Układy chłodnicze", "/uklady-chlodnicze/"),
        ("Membrany RO", "/membrany-ro/"),
        ("Nasze usługi", "/uslugi/"),
        ("Baza wiedzy", "/baza-wiedzy/"),
        ("Case studies", "/case-study/"),
    ]),
]}


# ==================================================================
# DEFINICJE ODTWORZONE Z RENDERU www (po awarii edycji 2026-07-02)
# Późniejsze przypisanie nadpisuje wcześniejsze definicje tych samych ścieżek.
# ==================================================================

PAGES["/autor/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/people/lukasz-kumor.jpg')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Kabi-Chemie · water treatment</p><h1>Nasi inżynierowie i eksperci techniczni</h1><p class="lead">Za treściami w bazie wiedzy stoją inżynierowie i technolodzy z praktycznym doświadczeniem w kondycjonowaniu wody przemysłowej.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/baza-wiedzy/">Baza wiedzy</a><a class="btn btn-ghost" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/people/lukasz-kumor.jpg" alt="kondycjonowanie wody przemysłowej Kabi-Chemie" loading="eager">
      <figcaption>kondycjonowanie wody przemysłowej Kabi-Chemie</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap narrow author">
      <div class="author-avatar" aria-hidden="true">KC</div>
      <div><h2>Zespół ekspertów Kabi-Chemie</h2><p class="author-role">Inżynierowie i technolodzy kondycjonowania wody</p>
      <p>Tworzymy specjalistyczne treści o uzdatnianiu i kondycjonowaniu wody dla przemysłu. Nasze doświadczenie potwierdza m.in. udział w Warsztatach Amoniakalnych. <em>(Biogram do uzupełnienia o realne dane i zdjęcia autorów.)</em></p></div></div></section><section class="section reveal"><div class="wrap"><div class="section-head"><h2>Artykuły zespołu</h2></div><div class="post-grid"><a class="post-card" href="/baza-wiedzy/kamien-kotlowy/"><div class="post-thumb" aria-hidden="true" style="--post-img:url('/assets/blog/blog-boiler-scale.png')"></div><div class="post-body"><span class="post-cat">Kotły parowe</span><h3>Co to jest kamień kotłowy?</h3><p></p><span class="post-meta"></span></div></a><a class="post-card" href="/baza-wiedzy/biofilm-w-ukladzie-chlodniczym/"><div class="post-thumb" aria-hidden="true" style="--post-img:url('/assets/blog/blog-biofilm-cleaning.png')"></div><div class="post-body"><span class="post-cat">Wieże chłodnicze</span><h3>Biofilm w układzie chłodniczym</h3><p></p><span class="post-meta"></span></div></a><a class="post-card" href="/baza-wiedzy/antyskalant-ro/"><div class="post-thumb" aria-hidden="true" style="--post-img:url('/assets/blog/blog-ro-antiscalant.png')"></div><div class="post-body"><span class="post-cat">Membrany RO</span><h3>Antyskalant do membran RO</h3><p></p><span class="post-meta"></span></div></a></div></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/baza-wiedzy/korozja/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/blog/blog-corrosion-pipes.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Baza wiedzy · SEO i GEO</p><h1>Korozja w instalacjach przemysłowych - Zapobieganie</h1><p class="lead">Jak chronić instalacje przemysłowe przed korozją, inhibitory, pasywacja stali i rodzaje korozji.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/blog/blog-corrosion-pipes.png" alt="praktyczna wiedza dla utrzymania ruchu i technologii" loading="eager">
      <figcaption>praktyczna wiedza dla utrzymania ruchu i technologii</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap"><div class="section-head"><h2>Artykuły w tej kategorii</h2></div><div class="post-grid"><a class="post-card" href="/baza-wiedzy/kamien-kotlowy/"><div class="post-thumb" aria-hidden="true" style="--post-img:url('/assets/blog/blog-corrosion-pipes.png')"></div><div class="post-body"><span class="post-cat">Korozja</span><h3>Korozja w instalacjach przemysłowych, rodzaje i zapobieganie</h3><p>Korozja tlenowa, wżerowa i biała, jak im przeciwdziałać.</p><span class="post-meta">9 min</span></div></a></div></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/ochrona-antykorozyjna/">Ochrona antykorozyjna, oferta</a></li><li><a href="/ochrona-antykorozyjna/pasywacja-stali/">Pasywacja stali</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/baza-wiedzy/kotly-parowe/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/blog/blog-boiler-scale.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Baza wiedzy · SEO i GEO</p><h1>Kotły parowe i para wodna - Artykuły eksperckie</h1><p class="lead">Wszystko o kondycjonowaniu wody w kotłach parowych, jak zapobiegać awariom, usuwać kamień i oszczędzać paliwo.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/blog/blog-boiler-scale.png" alt="praktyczna wiedza dla utrzymania ruchu i technologii" loading="eager">
      <figcaption>praktyczna wiedza dla utrzymania ruchu i technologii</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap"><div class="section-head"><h2>Artykuły w tej kategorii</h2></div><div class="post-grid"><a class="post-card" href="/baza-wiedzy/kamien-kotlowy/"><div class="post-thumb" aria-hidden="true" style="--post-img:url('/assets/blog/blog-boiler-scale.png')"></div><div class="post-body"><span class="post-cat">Kotły parowe</span><h3>Co to jest kamień kotłowy i dlaczego niszczy kotły parowe?</h3><p>Mechanizm powstawania kamienia i jego wpływ na koszty.</p><span class="post-meta">8 min</span></div></a></div></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/kotly-parowe/">Kotły parowe, oferta</a></li><li><a href="/baza-wiedzy/parametry-wody/">Parametry wody</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/baza-wiedzy/membrany-ro/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/blog/blog-ro-antiscalant.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Baza wiedzy · SEO i GEO</p><h1>Membrany RO i systemy demineralizacji - Baza wiedzy</h1><p class="lead">Ochrona membran odwróconej osmozy (RO) przed foulingiem, dobór antyskalantu i dbałość o demineralizację.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/blog/blog-ro-antiscalant.png" alt="praktyczna wiedza dla utrzymania ruchu i technologii" loading="eager">
      <figcaption>praktyczna wiedza dla utrzymania ruchu i technologii</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap"><div class="section-head"><h2>Artykuły w tej kategorii</h2></div><div class="post-grid"><a class="post-card" href="/baza-wiedzy/antyskalant-ro/"><div class="post-thumb" aria-hidden="true" style="--post-img:url('/assets/blog/blog-ro-antiscalant.png')"></div><div class="post-body"><span class="post-cat">Membrany RO</span><h3>Antyskalant i jego rola w ochronie membran RO</h3><p>Jak antyskalant przedłuża żywotność membran.</p><span class="post-meta">6 min</span></div></a></div></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/membrany-ro/">Membrany RO, oferta</a></li><li><a href="/uslugi/analiza-wody/">Analiza wody</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/baza-wiedzy/parametry-wody/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/blog/blog-water-reduction.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Baza wiedzy · SEO i GEO</p><h1>Przewodność i pH wody przemysłowej - Poradniki</h1><p class="lead">Zrozum parametry wody w przemyśle, wpływ pH, twardości i przewodności na pracę kotłów i układów chłodniczych.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/blog/blog-water-reduction.png" alt="praktyczna wiedza dla utrzymania ruchu i technologii" loading="eager">
      <figcaption>praktyczna wiedza dla utrzymania ruchu i technologii</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap"><div class="section-head"><h2>Artykuły w tej kategorii</h2></div><div class="post-grid"><a class="post-card" href="/baza-wiedzy/kamien-kotlowy/"><div class="post-thumb" aria-hidden="true" style="--post-img:url('/assets/blog/blog-water-reduction.png')"></div><div class="post-body"><span class="post-cat">Parametry wody</span><h3>Twardość wody, dlaczego niszczy kotły i instalacje?</h3><p>Stopnie twardości i ich znaczenie dla przemysłu.</p><span class="post-meta">6 min</span></div></a></div></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/uslugi/analiza-wody/">Analiza wody</a></li><li><a href="/kotly-parowe/kondycjonowanie-wody-kotlowej/">Kondycjonowanie wody kotłowej</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/baza-wiedzy/pojedynczy-wpis-blogowy-1/"] = {
    "og_type": 'article',
    "og_image": '/assets/blog/blog-boiler-scale.png',
    "jsonld": [{'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': 'Jak często należy odkamieniać kocioł?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Zależy od jakości wody, obciążenia i historii osadów. Przy prawidłowym kondycjonowaniu potrzeba czyszczeń wyraźnie maleje.'}}, {'@type': 'Question', 'name': 'Czy można kondycjonować wodę bez wyłączania kotła?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak, samo kondycjonowanie prowadzimy w trakcie pracy. Odkamienianie planujemy zależnie od stanu układu.'}}, {'@type': 'Question', 'name': 'Po czym poznać, że w kotle narasta kamień?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Typowe objawy to rosnące zużycie paliwa, gorsza wymiana ciepła, częstsze alarmy, osady w wodzie i problemy z utrzymaniem stabilnych parametrów.'}}, {'@type': 'Question', 'name': 'Czy 1 mm kamienia naprawdę ma znaczenie?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Nawet cienka warstwa osadu działa jak izolacja cieplna. Kocioł musi zużyć więcej paliwa, aby przekazać tę samą ilość energii do wody.'}}, {'@type': 'Question', 'name': 'Jak zapobiec powrotowi kamienia po czyszczeniu?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Po odkamienianiu warto wdrożyć stałą kontrolę twardości, przewodności i pH oraz dobrać program KCAQUA do pracy konkretnej kotłowni.'}}]}],
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/blog/blog-boiler-scale.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Baza wiedzy · SEO i GEO</p><h1>[Tytuł wpisu blogowego 1 - tu wstawisz konkretny temat]</h1><p class="lead">Kamień kotłowy to osad soli twardości na gorących powierzchniach kotła. Działa jak izolator, podnosi zużycie paliwa i grozi przegrzaniem rur.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/blog/blog-boiler-scale.png" alt="praktyczna wiedza dla utrzymania ruchu i technologii" loading="eager">
      <figcaption>praktyczna wiedza dla utrzymania ruchu i technologii</figcaption>
    </figure>
  </div>
</section><section class="section post-cover-section">
  <div class="wrap">
    <figure class="post-cover reveal">
      <img src="/assets/blog/blog-boiler-scale.png" alt="Kotłownia przemysłowa z rurociągami i instalacją parową" loading="eager">
      <figcaption>Kamień kotłowy ogranicza wymianę ciepła i podnosi koszt pracy kotła.</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap narrow prose"><h2>Jak powstaje kamień kotłowy?</h2><p>Podgrzewana woda traci zdolność utrzymania rozpuszczonych soli wapnia i magnezu. Wytrącają się one na najgorętszych powierzchniach, tworząc twardą skorupę.</p><h2>Jak kamień wpływa na rachunki za paliwo?</h2><p>Już <strong>1 mm kamienia</strong> może zwiększyć zużycie paliwa o około 10%, bo ciepło trudniej przenika do wody.</p><h2>Jak usunąć kamień kotłowy?</h2><ul><li>Chemiczne odkamienianie dobranym preparatem</li><li>Płukanie i pasywacja powierzchni</li><li>Wdrożenie kondycjonowania, by kamień nie wracał</li></ul><p class="note">Information gain: w realizacji Fako po wdrożeniu programu KCAQUA cykl czyszczenia wydłużył się z 3 do 12 miesięcy (dane przykładowe).</p></div></section><section class="section alt reveal"><div class="wrap narrow faq"><div class="section-head"><h2>Najczęstsze pytania</h2></div><details><summary>Jak często należy odkamieniać kocioł?</summary><div class="faq-a"><p>Zależy od jakości wody, obciążenia i historii osadów. Przy prawidłowym kondycjonowaniu potrzeba czyszczeń wyraźnie maleje.</p></div></details><details><summary>Czy można kondycjonować wodę bez wyłączania kotła?</summary><div class="faq-a"><p>Tak, samo kondycjonowanie prowadzimy w trakcie pracy. Odkamienianie planujemy zależnie od stanu układu.</p></div></details><details><summary>Po czym poznać, że w kotle narasta kamień?</summary><div class="faq-a"><p>Typowe objawy to rosnące zużycie paliwa, gorsza wymiana ciepła, częstsze alarmy, osady w wodzie i problemy z utrzymaniem stabilnych parametrów.</p></div></details><details><summary>Czy 1 mm kamienia naprawdę ma znaczenie?</summary><div class="faq-a"><p>Tak. Nawet cienka warstwa osadu działa jak izolacja cieplna. Kocioł musi zużyć więcej paliwa, aby przekazać tę samą ilość energii do wody.</p></div></details><details><summary>Jak zapobiec powrotowi kamienia po czyszczeniu?</summary><div class="faq-a"><p>Po odkamienianiu warto wdrożyć stałą kontrolę twardości, przewodności i pH oraz dobrać program KCAQUA do pracy konkretnej kotłowni.</p></div></details></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/kotly-parowe/odkamienianie/">Odkamienianie kotłów parowych</a></li><li><a href="/kotly-parowe/kondycjonowanie-wody-kotlowej/">Kondycjonowanie wody kotłowej</a></li><li><a href="/case-study/kociol-parowy-fako/">Case study: kocioł Fako</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/baza-wiedzy/pojedynczy-wpis-blogowy-2/"] = {
    "og_type": 'article',
    "og_image": '/assets/blog/blog-biofilm-cleaning.png',
    "jsonld": [{'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': 'Jak chronić wieżę przed Legionellą?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Podstawą jest kontrola biofilmu, właściwy biocyd, regularny monitoring wody i utrzymanie czystości powierzchni kontaktu z wodą.'}}, {'@type': 'Question', 'name': 'Czy sam biocyd wystarczy do usunięcia biofilmu?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Nie zawsze. Biofilm może chronić mikroorganizmy przed chemią, dlatego często potrzebna jest korekta programu, czyszczenie i kontrola parametrów obiegu.'}}, {'@type': 'Question', 'name': 'Jakie objawy wskazują na biofilm w układzie chłodniczym?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Najczęściej widać spadek wydajności chłodzenia, śliski osad, wzrost zużycia wody, nieprzyjemny zapach i większą podatność instalacji na korozję.'}}, {'@type': 'Question', 'name': 'Czy biofilm wpływa na koszty energii?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Warstwa biologiczna pogarsza wymianę ciepła, więc układ musi pracować ciężej, aby utrzymać wymaganą temperaturę procesu.'}}, {'@type': 'Question', 'name': 'Jak często trzeba kontrolować wodę w wieży chłodniczej?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Częstotliwość zależy od obciążenia i jakości wody. W praktyce warto kontrolować przewodność, pH, biologię i skuteczność programu chemicznego w stałym harmonogramie.'}}]}],
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/blog/blog-biofilm-cleaning.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Baza wiedzy · SEO i GEO</p><h1>[Tytuł wpisu blogowego 2 - tu wstawisz konkretny temat]</h1><p class="lead">Biofilm to warstwa mikroorganizmów na powierzchniach układu chłodniczego. Pogarsza wymianę ciepła, sprzyja korozji i bywa siedliskiem bakterii.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/blog/blog-biofilm-cleaning.png" alt="praktyczna wiedza dla utrzymania ruchu i technologii" loading="eager">
      <figcaption>praktyczna wiedza dla utrzymania ruchu i technologii</figcaption>
    </figure>
  </div>
</section><section class="section post-cover-section">
  <div class="wrap">
    <figure class="post-cover reveal">
      <img src="/assets/blog/blog-biofilm-cleaning.png" alt="Technik czyszczący wymiennik w przemysłowym układzie chłodniczym" loading="eager">
      <figcaption>Biofilm obniża sprawność wymiany ciepła i wymaga regularnej kontroli programu chemicznego.</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap narrow prose"><h2>Dlaczego biofilm jest groźny?</h2><p>Biofilm izoluje powierzchnie wymiany ciepła i chroni mikroorganizmy przed działaniem chemii. Może też sprzyjać rozwojowi bakterii Legionella.</p><h2>Jak usunąć i kontrolować biofilm?</h2><ul><li>Dozowanie biocydów (np. w ramach programu KCAQUA 305)</li><li>Kontrola parametrów obiegu i przewodności</li><li>Okresowe czyszczenie układu</li></ul></div></section><section class="section alt reveal"><div class="wrap narrow faq"><div class="section-head"><h2>Najczęstsze pytania</h2></div><details><summary>Jak chronić wieżę przed Legionellą?</summary><div class="faq-a"><p>Podstawą jest kontrola biofilmu, właściwy biocyd, regularny monitoring wody i utrzymanie czystości powierzchni kontaktu z wodą.</p></div></details><details><summary>Czy sam biocyd wystarczy do usunięcia biofilmu?</summary><div class="faq-a"><p>Nie zawsze. Biofilm może chronić mikroorganizmy przed chemią, dlatego często potrzebna jest korekta programu, czyszczenie i kontrola parametrów obiegu.</p></div></details><details><summary>Jakie objawy wskazują na biofilm w układzie chłodniczym?</summary><div class="faq-a"><p>Najczęściej widać spadek wydajności chłodzenia, śliski osad, wzrost zużycia wody, nieprzyjemny zapach i większą podatność instalacji na korozję.</p></div></details><details><summary>Czy biofilm wpływa na koszty energii?</summary><div class="faq-a"><p>Tak. Warstwa biologiczna pogarsza wymianę ciepła, więc układ musi pracować ciężej, aby utrzymać wymaganą temperaturę procesu.</p></div></details><details><summary>Jak często trzeba kontrolować wodę w wieży chłodniczej?</summary><div class="faq-a"><p>Częstotliwość zależy od obciążenia i jakości wody. W praktyce warto kontrolować przewodność, pH, biologię i skuteczność programu chemicznego w stałym harmonogramie.</p></div></details></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/uklady-chlodnicze/ochrona-wiez-chlodniczych/">Ochrona wież chłodniczych</a></li><li><a href="/uklady-chlodnicze/odkamienianie/">Odkamienianie układów chłodniczych</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/baza-wiedzy/pojedynczy-wpis-blogowy-3/"] = {
    "og_type": 'article',
    "og_image": '/assets/blog/blog-ro-antiscalant.png',
    "jsonld": [{'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': 'Jak dobrać antyskalant do mojej wody?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Na podstawie analizy wody surowej, odzysku instalacji RO i parametrów pracy membran. Najlepiej zacząć od badania wody.'}}, {'@type': 'Question', 'name': 'Po czym poznać, że membrany RO są zagrożone osadem?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Sygnałem jest spadek wydajności, wzrost różnicy ciśnień, pogorszenie jakości permeatu i częstsza potrzeba płukania chemicznego.'}}, {'@type': 'Question', 'name': 'Czy antyskalant zastępuje prawidłową filtrację wstępną?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Nie. Antyskalant chroni przed wytrącaniem soli, ale filtracja, kontrola żelaza, chloru i zawiesiny nadal są kluczowe dla żywotności membran.'}}, {'@type': 'Question', 'name': 'Jak często trzeba kontrolować dawkę antyskalantu?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Dawkę warto weryfikować przy zmianie jakości wody, odzysku, przepływu lub ciśnienia. Stała kontrola ogranicza ryzyko przewymiarowania i niedozowania.'}}, {'@type': 'Question', 'name': 'Czy pomagacie dobrać chemię do istniejącej stacji RO?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Analizujemy wodę, parametry pracy i historię awarii. Na tej podstawie dobieramy antyskalant oraz zalecenia dla obsługi stacji.'}}]}],
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/blog/blog-ro-antiscalant.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Baza wiedzy · SEO i GEO</p><h1>[Tytuł wpisu blogowego 3 - tu wstawisz konkretny temat]</h1><p class="lead">Antyskalant to preparat zapobiegający wytrącaniu soli na membranach odwróconej osmozy. Chroni membrany przed kamieniem i wydłuża ich żywotność.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/blog/blog-ro-antiscalant.png" alt="praktyczna wiedza dla utrzymania ruchu i technologii" loading="eager">
      <figcaption>praktyczna wiedza dla utrzymania ruchu i technologii</figcaption>
    </figure>
  </div>
</section><section class="section post-cover-section">
  <div class="wrap">
    <figure class="post-cover reveal">
      <img src="/assets/blog/blog-ro-antiscalant.png" alt="Przemysłowa stacja odwróconej osmozy z membranami i armaturą" loading="eager">
      <figcaption>Antyskalant chroni membrany RO przed krystalizacją soli i spadkiem wydajności.</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap narrow prose"><h2>Jak działa antyskalant?</h2><p>Antyskalant utrzymuje sole twardości w roztworze, zapobiegając ich krystalizacji na powierzchni membrany i spadkowi wydajności stacji RO.</p><h2>Dlaczego chlor i chlorki są groźne dla membran?</h2><p>Degradują strukturę membrany. Dlatego ważna jest ich kontrola, nasz preparat potrafi wiązać te gazy.</p></div></section><section class="section alt reveal"><div class="wrap narrow faq"><div class="section-head"><h2>Najczęstsze pytania</h2></div><details><summary>Jak dobrać antyskalant do mojej wody?</summary><div class="faq-a"><p>Na podstawie analizy wody surowej, odzysku instalacji RO i parametrów pracy membran. Najlepiej zacząć od badania wody.</p></div></details><details><summary>Po czym poznać, że membrany RO są zagrożone osadem?</summary><div class="faq-a"><p>Sygnałem jest spadek wydajności, wzrost różnicy ciśnień, pogorszenie jakości permeatu i częstsza potrzeba płukania chemicznego.</p></div></details><details><summary>Czy antyskalant zastępuje prawidłową filtrację wstępną?</summary><div class="faq-a"><p>Nie. Antyskalant chroni przed wytrącaniem soli, ale filtracja, kontrola żelaza, chloru i zawiesiny nadal są kluczowe dla żywotności membran.</p></div></details><details><summary>Jak często trzeba kontrolować dawkę antyskalantu?</summary><div class="faq-a"><p>Dawkę warto weryfikować przy zmianie jakości wody, odzysku, przepływu lub ciśnienia. Stała kontrola ogranicza ryzyko przewymiarowania i niedozowania.</p></div></details><details><summary>Czy pomagacie dobrać chemię do istniejącej stacji RO?</summary><div class="faq-a"><p>Tak. Analizujemy wodę, parametry pracy i historię awarii. Na tej podstawie dobieramy antyskalant oraz zalecenia dla obsługi stacji.</p></div></details></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/membrany-ro/">Membrany RO, oferta</a></li><li><a href="/uslugi/analiza-wody/">Analiza wody</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/baza-wiedzy/wieze-chlodnicze/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/blog/blog-cooling-towers.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Baza wiedzy · SEO i GEO</p><h1>Wieże chłodnicze i obiegi chłodzące - Baza wiedzy</h1><p class="lead">Optymalizacja pracy wież chłodniczych i obiegów, biofilm, biocydy i usuwanie kamienia ze skraplaczy.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/blog/blog-cooling-towers.png" alt="praktyczna wiedza dla utrzymania ruchu i technologii" loading="eager">
      <figcaption>praktyczna wiedza dla utrzymania ruchu i technologii</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap"><div class="section-head"><h2>Artykuły w tej kategorii</h2></div><div class="post-grid"><a class="post-card" href="/baza-wiedzy/biofilm-w-ukladzie-chlodniczym/"><div class="post-thumb" aria-hidden="true" style="--post-img:url('/assets/blog/blog-biofilm-cleaning.png')"></div><div class="post-body"><span class="post-cat">Wieże chłodnicze</span><h3>Biofilm w układzie chłodniczym, jak usunąć osady biologiczne?</h3><p>Kontrola mikroorganizmów w obiegu chłodzącym.</p><span class="post-meta">7 min</span></div></a></div></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/uklady-chlodnicze/">Układy chłodnicze, oferta</a></li><li><a href="/uklady-chlodnicze/skraplacze-amoniakalne/">Skraplacze amoniakalne</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/branze/"] = {
    "body_class": "has-dark-hero branches-hub-page",
    "title": "Kondycjonowanie wody dla branż przemysłowych | Kabi-Chemie",
    "h1": "Znamy procesy. Dobieramy technologię do branży.",
    "meta": "Jedna podstrona branżowa Kabi-Chemie: zakłady mięsne, mleczarnie, chłodnie, przemysł ciężki i producenci żywności. Technologie KCAQUA, analiza wody, oszczędności i kalkulator.",
    "image": "/assets/industries/industry-branches-collage.jpg",
    "og_image": "/assets/industries/industry-branches-collage.jpg",
    "jsonld": [{
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Branże obsługiwane przez Kabi-Chemie",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Zakłady mięsne i drobiarskie", "url": "https://kondycjonowanie-wody.pl/branze/#zaklady-miesne"},
            {"@type": "ListItem", "position": 2, "name": "Mleczarnie i przetwórstwo mleka", "url": "https://kondycjonowanie-wody.pl/branze/#mleczarnie"},
            {"@type": "ListItem", "position": 3, "name": "Chłodnie i obiegi chłodnicze", "url": "https://kondycjonowanie-wody.pl/branze/#chlodnie"},
            {"@type": "ListItem", "position": 4, "name": "Przemysł ciężki", "url": "https://kondycjonowanie-wody.pl/branze/#przemysl-ciezki"},
            {"@type": "ListItem", "position": 5, "name": "Producenci żywności", "url": "https://kondycjonowanie-wody.pl/branze/#producenci-zywnosci"}
        ]
    }],
    "sections": [custom("""
<section class="branches-hero" aria-label="Branże obsługiwane przez Kabi-Chemie">
  <div class="branches-hero__image" aria-hidden="true">
    <video autoplay muted loop playsinline preload="metadata" poster="/assets/industries/industry-branches-collage.jpg">
      <source src="/assets/industries/hero-branze.mp4" type="video/mp4">
    </video>
  </div>
  <div class="branches-hero__shade" aria-hidden="true"></div>
  <div class="wrap branches-hero__inner">
    <p class="branches-kicker">Branże, instalacje, procesy</p>
    <h1><span>Znamy procesy.</span> <span>Dobieramy technologię do branży.</span></h1>
    <p class="branches-hero__lead">Kotły parowe, chłodnictwo, mycie, woda technologiczna i odzysk energii prowadzimy pod kontrolą inżynierów Kabi-Chemie. Dlatego nie sprzedajemy jednego schematu, tylko program dopasowany do tego, jak realnie pracuje zakład.</p>
    <div class="branches-hero__actions">
      <a class="btn btn-primary" href="#zaklady-miesne">Zobacz branże</a>
      <a class="branches-link" href="/kalkulator-oszczednosci/#kalkulator">Policz potencjał oszczędności</a>
    </div>
    <ul class="branches-sector-strip" aria-label="Wybierz branżę">
      <li><a href="#zaklady-miesne">Zakłady mięsne i drobiarskie <span aria-hidden="true">↘</span></a></li>
      <li><a href="#mleczarnie">Mleczarnie <span aria-hidden="true">↘</span></a></li>
      <li><a href="#chlodnie">Chłodnie <span aria-hidden="true">↘</span></a></li>
      <li><a href="#przemysl-ciezki">Przemysł ciężki <span aria-hidden="true">↘</span></a></li>
      <li><a href="#producenci-zywnosci">Producenci żywności <span aria-hidden="true">↘</span></a></li>
    </ul>
  </div>
</section>

<section class="branches-proof reveal" aria-label="Dlaczego zakłady wybierają Kabi-Chemie" data-scroll-fly>
  <div class="wrap branches-proof__inner">
    <div class="branches-proof__head">
      <div data-fly="left">
        <p class="branches-proof__eyebrow">Proces decyzji</p>
        <h2 class="branches-proof__intro"><span>Technologia, pomiar,</span> <span>dane i raport.</span></h2>
      </div>
      <p class="branches-proof__lead" data-fly="right" data-fly-delay="0.04">Cztery obszary, które porządkują rozmowę o wodzie z utrzymaniem ruchu, produkcją i zarządem, bez zgadywania i dobierania chemii w ciemno.</p>
    </div>
    <div class="branches-proof__flow">
      <article>
        <span class="branches-proof__top"><span class="branches-proof__num">01</span></span>
        <strong>Autorska technologia KCAQUA</strong>
        <span>programy dla wody kotłowej, chłodniczej, RO i instalacji procesowych</span>
      </article>
      <article>
        <span class="branches-proof__top"><span class="branches-proof__num">02</span></span>
        <strong>Decyzje na podstawie pomiarów</strong>
        <span>sprawdzamy pH, twardość, przewodność, żelazo, TDS, osady i odsalanie</span>
      </article>
      <article>
        <span class="branches-proof__top"><span class="branches-proof__num">03</span></span>
        <strong>Dane do oszczędności i certyfikatów</strong>
        <span>liczymy wodę, ścieki, energię i dane potrzebne do rozmowy o efekcie energetycznym</span>
      </article>
      <article>
        <span class="branches-proof__top"><span class="branches-proof__num">04</span></span>
        <strong>Raport dla utrzymania ruchu i zarządu</strong>
        <span>pokazujemy problem, rekomendację, ryzyko i możliwy efekt finansowy w liczbach</span>
      </article>
    </div>
  </div>
</section>

<section class="branches-method reveal" aria-labelledby="branches-method-title" data-scroll-fly>
  <div class="wrap branches-method__grid">
    <div data-fly="left">
      <p class="branches-kicker">Jak dobieramy program</p>
      <h2 id="branches-method-title"><span>Najpierw proces,</span> <span>potem chemia.</span></h2>
      <p>Ta sama nazwa preparatu nie rozwiązuje dwóch różnych problemów. Inaczej pracuje kocioł w zakładzie mięsnym, inaczej skraplacz w chłodni, a inaczej obieg w przemyśle ciężkim. Dlatego zaczynamy od technologii zakładu i miejsc, w których woda generuje koszt.</p>
    </div>
    <ol class="branches-method__steps">
      <li data-fly="right"><strong>Rozpoznajemy obieg</strong><span>para, chłód, RO, mycie, CIP, woda uzupełniająca, ścieki technologiczne</span></li>
      <li data-fly="right" data-fly-delay="0.04"><strong>Sprawdzamy parametry</strong><span>analiza wody, osady, korozja, przewodność, odsalanie, dawki i praca automatyki</span></li>
      <li data-fly="right" data-fly-delay="0.08"><strong>Dobieramy KCAQUA</strong><span>preparat, dozowanie, limity pracy i harmonogram kontroli</span></li>
      <li data-fly="right" data-fly-delay="0.12"><strong>Liczymy efekt</strong><span>woda, ścieki, energia, paliwo, czyszczenia, awarie i czas pracy instalacji</span></li>
    </ol>
  </div>
</section>

<section class="branch-chapter branch-chapter--meat reveal" id="zaklady-miesne" aria-labelledby="branch-meat-title" data-scroll-fly>
  <div class="wrap branch-chapter__grid">
    <figure class="branch-chapter__media"><img src="/assets/industries/industry-meat.jpg" alt="Zakład mięsny i drobiarski z instalacją procesową, parą i obiegami wody" loading="lazy"></figure>
    <div class="branch-chapter__copy">
      <p class="branches-kicker" data-fly="right">Zakłady mięsne i drobiarskie</p>
      <h2 id="branch-meat-title" data-fly="right" data-fly-delay="0.02"><span>Higiena procesu</span> <span>i ciągłość produkcji</span> <span>zależą od stabilnej wody.</span></h2>
      <p data-fly="right" data-fly-delay="0.05">W przetwórstwie mięsa i drobiu woda pracuje w kotłowni, chłodzeniu, myciu, płukaniu oraz instalacjach pomocniczych. Kamień, biofilm albo korozja szybko przechodzą z problemu technicznego w przestój, większe zużycie pary i ryzyko dla harmonogramu produkcji.</p>
      <div class="branch-matrix" data-fly="right" data-fly-delay="0.08">
        <article><h3>Co robimy</h3><p>Kondycjonujemy wodę kotłową KCAQUA 303, prowadzimy ochronę skraplaczy i obiegów chłodniczych, dobieramy biocydy, inhibitory korozji i antyskalanty do realnego obciążenia zakładu.</p></article>
        <article><h3>Co sprawdzamy</h3><p>Twardość, pH, przewodność, odsalanie, żelazo, osady, biofilm, jakość wody uzupełniającej, pracę pomp dozujących i historię czyszczeń.</p></article>
        <article><h3>Jaka korzyść</h3><p>Mniej kamienia w kotle, stabilniejsze chłodzenie, mniejsze zużycie wody i ścieków oraz mniej awaryjnych czyszczeń w czasie produkcji.</p></article>
      </div>
      <div class="branch-actions" data-fly="right" data-fly-delay="0.11"><a class="btn btn-primary" href="/kalkulator-oszczednosci/#kalkulator">Policz oszczędności</a><a class="branches-link" href="/bezplatna-konsultacja/">Porozmawiaj z inżynierem</a></div>
    </div>
  </div>
</section>

<section class="branch-chapter reveal" id="mleczarnie" aria-labelledby="branch-dairy-title" data-scroll-fly>
  <div class="wrap branch-chapter__grid branch-chapter__grid--reverse">
    <figure class="branch-chapter__media"><img src="/assets/industries/industry-dairy.jpg" alt="Mleczarnia z instalacjami ze stali nierdzewnej i obiegami technologicznymi" loading="lazy"></figure>
    <div class="branch-chapter__copy">
      <p class="branches-kicker" data-fly="left">Mleczarnie i przetwórstwo mleka</p>
      <h2 id="branch-dairy-title" data-fly="left" data-fly-delay="0.02"><span>Wymiana ciepła musi być</span> <span>czysta, powtarzalna</span> <span>i&nbsp;przewidywalna.</span></h2>
      <p data-fly="left" data-fly-delay="0.05">Mleczarnie pracują na pasteryzacji, wymiennikach, kotłowniach, wodzie lodowej, CIP i wodzie technologicznej. Osad na powierzchniach wymiany ciepła oznacza dłuższe cykle, wyższe koszty energii i trudniejszą stabilizację parametrów procesu.</p>
      <div class="branch-matrix" data-fly="left" data-fly-delay="0.08">
        <article><h3>Co robimy</h3><p>Dobieramy program dla kotłów parowych, wymienników, obiegów chłodniczych, stacji RO i wody do mycia. W razie potrzeby planujemy czyszczenie chemiczne oraz pasywację powierzchni.</p></article>
        <article><h3>Co sprawdzamy</h3><p>Przewodność, twardość, zasadowość, chlorki, żelazo, ryzyko kamienia, pracę odsalania i wpływ jakości wody na CIP oraz wymianę ciepła.</p></article>
        <article><h3>Jaka korzyść</h3><p>Stabilniejsze procesy cieplne, krótsze ryzyko przestojów, mniej osadów w wymiennikach i lepsza kontrola kosztu pary oraz chłodu.</p></article>
      </div>
      <div class="branch-actions" data-fly="left" data-fly-delay="0.11"><a class="btn btn-primary" href="/kalkulator-oszczednosci/#kalkulator">Policz oszczędności</a><a class="branches-link" href="/uslugi/analiza-wody/">Zobacz analizę wody</a></div>
    </div>
  </div>
</section>

<section class="branch-chapter reveal" id="chlodnie" aria-labelledby="branch-cooling-title" data-scroll-fly>
  <div class="wrap branch-chapter__grid">
    <figure class="branch-chapter__media"><img src="/assets/industries/industry-cold-storage.jpg" alt="Chłodnia przemysłowa i skraplacze wyparne z instalacjami wodnymi" loading="lazy"></figure>
    <div class="branch-chapter__copy">
      <p class="branches-kicker" data-fly="right">Chłodnie i obiegi chłodnicze</p>
      <h2 id="branch-cooling-title" data-fly="right" data-fly-delay="0.02"><span>Skraplacz traci wydajność</span> <span>po&nbsp;cichu, a rachunki</span> <span>rosną od razu.</span></h2>
      <p data-fly="right" data-fly-delay="0.05">W chłodniach i skraplaczach wyparnych problemem jest kamień, biofilm, biała korozja i zbyt konserwatywne odsalanie. Każdy z tych czynników pogarsza wymianę ciepła, zwiększa pobór energii i skraca czas między czyszczeniami.</p>
      <div class="branch-matrix" data-fly="right" data-fly-delay="0.08">
        <article><h3>Co robimy</h3><p>Stosujemy KCAQUA 305, biocydy, inhibitory korozji i antyskalanty dla skraplaczy BAC, EVAPCO, wież chłodniczych i obiegów natryskowych.</p></article>
        <article><h3>Co sprawdzamy</h3><p>Cykle koncentracji, przewodność, pH, twardość, osady, mikrobiologię, żelazo, pracę automatyki odsalania i zużycie wody uzupełniającej.</p></article>
        <article><h3>Jaka korzyść</h3><p>Lepsza wymiana ciepła, mniej wody uzupełniającej, mniej ścieków, stabilna temperatura procesu i mniejsze ryzyko korozji ocynku.</p></article>
      </div>
      <div class="branch-actions" data-fly="right" data-fly-delay="0.11"><a class="btn btn-primary" href="/kalkulator-oszczednosci/#kalkulator">Policz oszczędności</a><a class="branches-link" href="/uklady-chlodnicze/skraplacze-amoniakalne/">Skraplacze amoniakalne</a></div>
    </div>
  </div>
</section>

<section class="branch-chapter reveal" id="przemysl-ciezki" aria-labelledby="branch-heavy-title" data-scroll-fly>
  <div class="wrap branch-chapter__grid branch-chapter__grid--reverse">
    <figure class="branch-chapter__media"><img src="/assets/industries/industry-heavy.jpg" alt="Przemysł ciężki z instalacjami wodnymi, kominami i układami chłodzenia" loading="lazy"></figure>
    <div class="branch-chapter__copy">
      <p class="branches-kicker" data-fly="left">Przemysł ciężki</p>
      <h2 id="branch-heavy-title" data-fly="left" data-fly-delay="0.02"><span>W trudnych warunkach</span> <span>program musi być odporny,</span> <span>nie tylko poprawny</span> <span>na papierze.</span></h2>
      <p data-fly="left" data-fly-delay="0.05">Huty, kopalnie, energetyka i zakłady ciężkie pracują na wysokim obciążeniu cieplnym, zapyleniu, zmiennej jakości wody i dużych kosztach przestoju. Tu liczy się stabilność programu, szybka diagnoza i ochrona instalacji przed korozją oraz osadami.</p>
      <div class="branch-matrix" data-fly="left" data-fly-delay="0.08">
        <article><h3>Co robimy</h3><p>Chronimy obiegi chłodnicze, kotły, wymienniki i rurociągi. Dobieramy inhibitory korozji, antyskalanty, czyszczenie chemiczne i pasywację po usunięciu osadów.</p></article>
        <article><h3>Co sprawdzamy</h3><p>pH, przewodność, chlorki, żelazo, zawiesiny, twardość, osady, korozję punktową, ubytki metalu i stabilność parametrów przy zmiennym obciążeniu.</p></article>
        <article><h3>Jaka korzyść</h3><p>Dłuższa żywotność instalacji, mniej awarii, lepsza dyspozycyjność produkcji i większa kontrola nad kosztami mediów.</p></article>
      </div>
      <div class="branch-actions" data-fly="left" data-fly-delay="0.11"><a class="btn btn-primary" href="/kalkulator-oszczednosci/#kalkulator">Policz oszczędności</a><a class="branches-link" href="/ochrona-antykorozyjna/">Ochrona antykorozyjna</a></div>
    </div>
  </div>
</section>

<section class="branch-chapter reveal" id="producenci-zywnosci" aria-labelledby="branch-food-title" data-scroll-fly>
  <div class="wrap branch-chapter__grid">
    <figure class="branch-chapter__media"><img src="/assets/industries/industry-food-producers.jpg" alt="Produkcja żywności z linią technologiczną i instalacjami wodnymi" loading="lazy"></figure>
    <div class="branch-chapter__copy">
      <p class="branches-kicker" data-fly="right">Producenci żywności</p>
      <h2 id="branch-food-title" data-fly="right" data-fly-delay="0.02"><span>Woda technologiczna</span> <span>ma wspierać produkcję,</span> <span>nie wymuszać</span> <span>reakcji awaryjnych.</span></h2>
      <p data-fly="right" data-fly-delay="0.05">Producenci żywności łączą kilka obiegów naraz: parę, chłód, wodę do mycia, wodę procesową, RO i ścieki. Właśnie dlatego program powinien obejmować całą mapę instalacji, a nie tylko jeden punkt dozowania.</p>
      <div class="branch-matrix" data-fly="right" data-fly-delay="0.08">
        <article><h3>Co robimy</h3><p>Łączymy analizę wody, dobór KCAQUA, korektę dozowania, monitoring i rekomendacje dla kotłów, chłodnictwa, RO oraz wody technologicznej.</p></article>
        <article><h3>Co sprawdzamy</h3><p>Jakość wody surowej, filtrację, przewodność, twardość, TDS, chlorki, zużycie wody, ścieków i wpływ parametrów na powtarzalność produkcji.</p></article>
        <article><h3>Jaka korzyść</h3><p>Mniejszy koszt mediów, stabilniejsza produkcja, prostsze raportowanie i mniej decyzji podejmowanych dopiero po awarii.</p></article>
      </div>
      <div class="branch-actions" data-fly="right" data-fly-delay="0.11"><a class="btn btn-primary" href="/kalkulator-oszczednosci/#kalkulator">Policz oszczędności</a><a class="branches-link" href="/bezplatna-konsultacja/">Umów audyt</a></div>
    </div>
  </div>
</section>

<section class="branches-savings reveal" aria-labelledby="branches-savings-title" data-scroll-fly>
  <div class="wrap branches-savings__grid">
    <div data-fly="left">
      <p class="branches-kicker">Oszczędności i certyfikaty</p>
      <h2 id="branches-savings-title"><span>Najpierw liczymy straty</span> <span>potem pokazujemy potencjał.</span></h2>
      <p>Nie obiecujemy tej samej liczby każdemu zakładowi. Weryfikujemy parametry instalacji, koszty mediów i obecny sposób pracy. Jeżeli efekt energetyczny spełnia wymagania, pomagamy zebrać dane potrzebne do rozmowy o białych certyfikatach.</p>
      <div class="branch-actions"><a class="btn btn-primary" href="/kalkulator-oszczednosci/#kalkulator">Uruchom kalkulator</a><a class="branches-link" href="/case-study/">Zobacz case studies</a></div>
    </div>
    <div class="branches-savings__stats" aria-label="Przykładowe efekty wdrożeń">
      <article data-fly="right">
        <span class="branches-savings__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" focusable="false"><path d="M12 3.5s6 6.7 6 11a6 6 0 0 1-12 0c0-4.3 6-11 6-11Z"></path><path d="M9.2 15.3c.5 1.3 1.5 2.1 2.8 2.1"></path></svg>
        </span>
        <strong class="branches-savings__value">12 593 000 l</strong>
        <span class="branches-savings__label">wody zaoszczędzonej u jednego klienta w 12 miesięcy</span>
      </article>
      <article data-fly="right" data-fly-delay="0.05">
        <span class="branches-savings__icon branches-savings__icon--trend" aria-hidden="true">
          <svg viewBox="0 0 24 24" focusable="false"><path d="M4 17l5.4-5.4 4 4L20 9"></path><path class="trend-arrow" d="M15 9h5v5"></path></svg>
        </span>
        <strong class="branches-savings__value">68,2%</strong>
        <span class="branches-savings__label">redukcji zużycia wody po wdrożeniu programu</span>
      </article>
      <article data-fly="right" data-fly-delay="0.1">
        <span class="branches-savings__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" focusable="false"><ellipse cx="12" cy="6.5" rx="6.5" ry="3"></ellipse><path d="M5.5 6.5v8c0 1.7 2.9 3 6.5 3s6.5-1.3 6.5-3v-8"></path><path d="M5.5 10.5c0 1.7 2.9 3 6.5 3s6.5-1.3 6.5-3"></path><path d="M5.5 14.5c0 1.7 2.9 3 6.5 3s6.5-1.3 6.5-3"></path></svg>
        </span>
        <strong class="branches-savings__value">418 tys. zł</strong>
        <span class="branches-savings__label">oszczędności kosztów operacyjnych w analizowanym przypadku</span>
      </article>
    </div>
  </div>
</section>

<section class="branches-final reveal" aria-labelledby="branches-final-title">
  <div class="wrap branches-final__inner">
    <span class="branches-final__sigil" aria-hidden="true"></span>
    <h2 id="branches-final-title"><span>Twoja branża. Nasze doświadczenie.</span> <span>Konkretny plan dla Twojej instalacji.</span></h2>
    <p>Opisz instalację i objaw. Pokażemy, gdzie woda generuje koszt i od czego zacząć: analiza wody, audyt techniczny, korekta dozowania, czyszczenie chemiczne albo kalkulacja oszczędności.</p>
    <div class="branches-final__actions">
      <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>
      <a class="branches-link" href="/kalkulator-oszczednosci/#kalkulator">Policz potencjał oszczędności</a>
    </div>
  </div>
</section>
""")],
}

PAGES["/branze/zaklady-miesne-i-drobiarskie/"] = {
    "body_class": "has-dark-hero industry-detail-page meat-sector-page",
    "title": "Kondycjonowanie wody dla zakładów mięsnych i drobiarskich",
    "h1": "Kondycjonowanie wody dla zakładów mięsnych i drobiarskich",
    "meta": "Programy KCAQUA dla zakładów mięsnych i drobiarskich: kotły parowe, obiegi chłodnicze, woda technologiczna, mycie, biofilm, kamień i korozja.",
    "image": "/assets/industries/industry-meat.jpg",
    "og_image": "/assets/industries/industry-meat.jpg",
    "jsonld": [{
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "Kondycjonowanie wody dla zakładów mięsnych i drobiarskich",
        "serviceType": "Kondycjonowanie wody przemysłowej dla przetwórstwa mięsa i drobiu",
        "provider": {
            "@type": "Organization",
            "name": "Kabi-Chemie",
            "url": "https://kondycjonowanie-wody.pl/"
        },
        "areaServed": "Polska",
        "audience": {
            "@type": "BusinessAudience",
            "audienceType": "Zakłady mięsne, zakłady drobiarskie, przetwórstwo spożywcze"
        },
        "offers": {
            "@type": "Offer",
            "availability": "https://schema.org/InStock",
            "url": "https://kondycjonowanie-wody.pl/bezplatna-konsultacja/"
        }
    }],
    "sections": [custom("""
<section class="meat-hero" aria-label="Kondycjonowanie wody dla zakładów mięsnych i drobiarskich">
  <div class="meat-hero__shade" aria-hidden="true"></div>
  <div class="wrap meat-hero__grid">
    <div class="meat-hero__copy">
      <p class="meat-kicker">Branże: zakłady mięsne i drobiarskie</p>
      <h1>Woda pod kontrolą w zakładach mięsnych i drobiarskich.</h1>
      <p>Dobieramy programy KCAQUA dla kotłowni parowych, skraplaczy, obiegów chłodniczych i wody technologicznej, aby wspierać higienę procesu oraz ciągłość produkcji.</p>
      <div class="meat-hero__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację</a>
        <a class="meat-link" href="/kotly-parowe/">Zobacz rozwiązania dla kotłów</a>
      </div>
    </div>
    <figure class="meat-hero__media">
      <img src="/assets/industries/industry-meat.jpg" alt="Zakład mięsny i drobiarski z instalacjami procesowymi, parą i obiegami wody" loading="eager">
    </figure>
  </div>
</section>

<section class="meat-signal" aria-label="Najważniejsze potrzeby zakładów mięsnych i drobiarskich">
  <div class="wrap meat-signal__grid">
    <article>
      <strong>Higiena procesu</strong>
      <span>Stabilna jakość wody do mycia, płukania i pracy instalacji pomocniczych.</span>
    </article>
    <article>
      <strong>Para technologiczna</strong>
      <span>Mniej kamienia w kotle, lepsza wymiana ciepła i przewidywalna praca kotłowni.</span>
    </article>
    <article>
      <strong>Chłód i skraplacze</strong>
      <span>Kontrola osadów, biofilmu i korozji w obiegach, które pracują pod dużym obciążeniem.</span>
    </article>
  </div>
</section>

<section class="meat-risk reveal" aria-labelledby="meat-risk-title">
  <div class="wrap meat-risk__grid">
    <div class="meat-risk__intro">
      <h2 id="meat-risk-title">Największe koszty zwykle nie zaczynają się od chemii.</h2>
      <p>Zaczynają się od niestabilnej wody: kamienia, biofilmu, korozji, zbyt częstego odsalania i czyszczeń planowanych w złym momencie.</p>
    </div>
    <div class="meat-risk__list" aria-label="Typowe ryzyka w zakładzie">
      <article><h3>Kamień kotłowy</h3><p>Izoluje powierzchnie grzewcze i podnosi zużycie paliwa przy tej samej produkcji pary.</p></article>
      <article><h3>Biofilm w chłodzeniu</h3><p>Obniża wydajność wymiany ciepła i zwiększa ryzyko problemów sanitarnych w obiegu.</p></article>
      <article><h3>Korozja instalacji</h3><p>Skraca żywotność rur, pomp, wymienników i armatury pracującej z wodą procesową.</p></article>
      <article><h3>Nadmierne odsalanie</h3><p>Podnosi zużycie wody, ilość ścieków i koszt utrzymania parametrów w bezpiecznym zakresie.</p></article>
    </div>
  </div>
</section>

<section class="meat-solutions reveal" aria-labelledby="meat-solutions-title">
  <div class="wrap">
    <div class="meat-section-head">
      <h2 id="meat-solutions-title">Program dobieramy do instalacji, nie do nazwy branży.</h2>
      <p>Zakład mięsny może mieć kocioł parowy, chłodnię amoniakalną, skraplacze wyparne, stację RO, CIP i wodę do mycia. Każdy z tych obszarów wymaga innego punktu kontroli.</p>
    </div>
    <div class="meat-bento">
      <article class="meat-bento__item meat-bento__item--wide">
        <span>Kotły parowe</span>
        <h3>KCAQUA 303 dla stabilnej wody kotłowej</h3>
        <p>Kontrolujemy twardość, pH, przewodność, odsalanie i ochronę antykorozyjną, żeby ograniczyć narastanie kamienia oraz straty energii.</p>
      </article>
      <article class="meat-bento__item">
        <span>Chłodnictwo</span>
        <h3>Skraplacze i wieże chłodnicze</h3>
        <p>Program obejmuje antyskalant, biocyd, inhibitory korozji i korektę pracy odsalania.</p>
      </article>
      <article class="meat-bento__item meat-bento__item--image" aria-label="Instalacje wodne w przemyśle spożywczym"></article>
      <article class="meat-bento__item">
        <span>Mycie i proces</span>
        <h3>Woda technologiczna pod kontrolą</h3>
        <p>Pomagamy utrzymać parametry wody tam, gdzie liczy się powtarzalność mycia, płukania i przygotowania procesu.</p>
      </article>
      <article class="meat-bento__item">
        <span>Serwis</span>
        <h3>Monitoring zamiast reakcji po awarii</h3>
        <p>Ustalamy rytm kontroli parametrów, korekt dozowania i raportowania dla utrzymania ruchu.</p>
      </article>
    </div>
  </div>
</section>

<section class="meat-flow reveal" aria-labelledby="meat-flow-title">
  <div class="wrap meat-flow__grid">
    <div class="meat-flow__copy">
      <h2 id="meat-flow-title">Jak wygląda pierwsza rozmowa z inżynierem?</h2>
      <p>Nie musisz mieć kompletnej dokumentacji. Wystarczy krótki opis instalacji, objawy, wyniki wody albo zdjęcia miejsca, w którym pojawia się problem.</p>
      <a class="btn btn-primary" href="/bezplatna-konsultacja/">Przejdź do formularza</a>
    </div>
    <div class="meat-flow__steps">
      <article><h3>Rozpoznajemy proces</h3><p>Ustalamy, czy problem dotyczy kotłowni, chłodnictwa, skraplacza, mycia czy stacji przygotowania wody.</p></article>
      <article><h3>Sprawdzamy parametry</h3><p>Analizujemy dostępne wyniki wody i wskazujemy, jakie dane warto uzupełnić przed doborem programu.</p></article>
      <article><h3>Wskazujemy kolejny krok</h3><p>Może to być audyt techniczny, analiza wody, korekta dozowania albo plan czyszczenia chemicznego.</p></article>
    </div>
  </div>
</section>

<section class="meat-outcome reveal" aria-labelledby="meat-outcome-title">
  <div class="wrap meat-outcome__inner">
    <div>
      <h2 id="meat-outcome-title">Efekt, którego szuka zakład: mniej ryzyka i mniej kosztów ukrytych.</h2>
      <p>Kabi-Chemie łączy chemię KCAQUA, pomiar, serwis i raportowanie. Dzięki temu decyzja o programie nie opiera się na obietnicy, tylko na stanie instalacji i parametrach wody.</p>
    </div>
    <ul class="meat-outcome__list">
      <li>mniej kamienia w kotle i wymiennikach</li>
      <li>stabilniejsza praca chłodzenia i skraplaczy</li>
      <li>mniejsze zużycie wody oraz ścieków technologicznych</li>
      <li>czytelny raport dla utrzymania ruchu i osób decyzyjnych</li>
    </ul>
  </div>
</section>

<section class="meat-related reveal" aria-labelledby="meat-related-title">
  <div class="wrap">
    <h2 id="meat-related-title">Najczęściej łączymy tę branżę z tymi rozwiązaniami</h2>
    <div class="meat-related__grid">
      <a href="/kotly-parowe/kondycjonowanie-wody-kotlowej/"><strong>Kondycjonowanie wody kotłowej</strong><span>program dla kotłów parowych i stabilnej produkcji pary</span></a>
      <a href="/uklady-chlodnicze/skraplacze-amoniakalne/"><strong>Skraplacze amoniakalne</strong><span>ochrona przed kamieniem, biofilmem i korozją</span></a>
      <a href="/uslugi/analiza-wody/"><strong>Analiza wody</strong><span>punkt startowy przed doborem chemii i korektą dozowania</span></a>
    </div>
  </div>
</section>

<section class="meat-cta reveal" aria-labelledby="meat-cta-title">
  <div class="wrap meat-cta__inner">
    <div>
      <h2 id="meat-cta-title">Opisz instalację. Oddzwoni osoba techniczna, nie anonimowa infolinia.</h2>
      <p>Wystarczy nazwa firmy, telefon i krótki opis problemu. Resztę doprecyzujemy w rozmowie.</p>
    </div>
    <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację</a>
  </div>
</section>
""")],
}

PAGES["/case-study/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/case/case-fako-boiler-generated.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Case study · wynik w liczbach</p><h1>Case Studies: Realizacje z zakresu uzdatniania wody</h1><p class="lead">Realne dane przed i po wdrożeniu programu KCAQUA, z kotłowni parowych, chłodni amoniakalnych i zakładów przetwórczych.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/case/case-fako-boiler-generated.png" alt="wdrożenie KCAQUA pokazane na danych i pracy instalacji" loading="eager">
      <figcaption>wdrożenie KCAQUA pokazane na danych i pracy instalacji</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap"><div class="section-head"><h2>Realizacje</h2></div><div class="card-grid"><a class="card" href="/case-study/kociol-parowy-fako/"><h3>Kocioł parowy Fako</h3><p>Chemiczne odkamienianie i kondycjonowanie wody kotłowej.</p><span class="card-link">Zobacz efekty →</span></a><a class="card" href="/case-study/skraplacz-bac-kcaqua/"><h3>Skraplacz BAC, KCAQUA 305</h3><p>Optymalizacja pracy skraplacza wyparnego.</p><span class="card-link">Zobacz efekty →</span></a><a class="card" href="/case-study/skraplacz-evapco-przetworstwo-rybne/"><h3>Skraplacz Evapco, przetwórstwo rybne</h3><p>Czyszczenie chemiczne i odzysk wydajności chłodzenia.</p><span class="card-link">Zobacz efekty →</span></a><a class="card" href="/case-study/warsztaty-amoniakalne-2024/"><h3>Warsztaty Amoniakalne 2024</h3><p>Nasza relacja i prelekcje o kondycjonowaniu wody.</p><span class="card-link">Przeczytaj →</span></a></div></div></section><section class="section bluf reveal"><div class="wrap narrow">
      <p class="bluf-text">Dane liczbowe w poszczególnych realizacjach są przykładowe, do potwierdzenia i autoryzacji przez klientów przed publikacją.</p></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/case-study/kociol-parowy-fako/"] = {
    "og_type": 'article',
    "body_class": 'has-dark-hero',
    "sections": [custom("""
<section class="consult-hero" id="top">
  <div class="consult-hero__bg" aria-hidden="true"></div>
  <div class="wrap consult-hero__inner">
    <div class="consult-hero__copy">
      <p class="consult-kicker">Case study · Kotłownia parowa</p>
      <h1>Efekty chemicznego odkamieniania kotła parowego <em>Fako</em></h1>
      <p class="consult-lead">Zakład zmagał się z kamieniem, stratami energii i częstymi przestojami na czyszczenie. Odkamieniliśmy układ i wdrożyliśmy program KCAQUA 303, a kocioł odzyskał parametry pracy.</p>
      <div class="consult-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/case-study/">Zobacz inne realizacje</a></div>
      <ul class="consult-hero__points" aria-label="Najważniejsze informacje"><li>Kocioł parowy Fako</li><li>Program KCAQUA 303</li><li>Efekty widoczne po 6 tygodniach</li></ul>
    </div>
    <div class="consult-hero__visual">
      <div class="consult-hero__frame">
        <img src="/assets/case/case-fako-boiler-generated.png" alt="Kocioł parowy Fako po chemicznym odkamienianiu" loading="eager">
      </div>
    </div>
  </div>
  <div class="consult-proof" aria-label="Najważniejsze informacje"><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3c2 3 5 4.5 5 8a5 5 0 0 1-10 0c0-1.5.7-2.7 1.5-3.5C9 9 9.5 7 9 5c2 .5 2.5 1.5 3 2 .3-1.2.2-2.7 0-4Z"/></svg></span><strong>Instalacja</strong><span>Kocioł parowy Fako pracujący na twardej wodzie.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6M10 3v6l-5 8a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-8V3"/><path d="M7.5 14h9"/></svg></span><strong>Zakres prac</strong><span>Odkamienianie i kondycjonowanie KCAQUA 303.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h16M7 20V10M12 20V5M17 20v-7"/></svg></span><strong>Kluczowy efekt</strong><span>Mniej paliwa i dłuższe cykle czyszczenia.</span></div></div>
</section>
<section class="consult-section consult-section--light">
  <div class="wrap">
    <div class="consult-section-head">
      <p class="consult-kicker">Wyzwanie</p>
      <h2>Kamień izolował powierzchnie grzewcze i podnosił koszty pary.</h2>
      <p>Kocioł pracował na wodzie o wysokiej twardości i przewodności, a narastający osad wymuszał częste przestoje.</p>
    </div>
    <div class="consult-fit-grid consult-fit-grid--3"><article class="fitcard"><span class="fitcard__no" aria-hidden="true">01</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><h3>Twarda woda zasilająca</h3><p>Twardość 8°n i przewodność 4200 µS sprzyjały szybkiemu narastaniu kamienia.</p><span class="fitcard__tag">Woda · parametry</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">02</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3c2 3 5 4.5 5 8a5 5 0 0 1-10 0c0-1.5.7-2.7 1.5-3.5C9 9 9.5 7 9 5c2 .5 2.5 1.5 3 2 .3-1.2.2-2.7 0-4Z"/></svg></span><h3>Straty paliwa</h3><p>Już 1 mm kamienia potrafi podnieść zużycie paliwa o około 10%.</p><span class="fitcard__tag">Energia · koszty</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">03</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M19 12a7 7 0 0 0-.1-1.3l2-1.5-2-3.4-2.3 1a7 7 0 0 0-2.3-1.3L13.8 1h-3.6l-.3 2.2a7 7 0 0 0-2.3 1.3l-2.3-1-2 3.4 2 1.5A7 7 0 0 0 5 12c0 .5 0 .9.1 1.3l-2 1.5 2 3.4 2.3-1a7 7 0 0 0 2.3 1.3l.3 2.2h3.6l.3-2.2a7 7 0 0 0 2.3-1.3l2.3 1 2-3.4-2-1.5c.1-.4.1-.8.1-1.3Z"/></svg></span><h3>Częste przestoje</h3><p>Czyszczenie kotła było potrzebne średnio co 3 miesiące.</p><span class="fitcard__tag">Utrzymanie ruchu</span></article></div>
  </div>
</section>
<section class="consult-section kontakt-steps">
  <span class="consult-watermark" aria-hidden="true"></span>
  <div class="wrap">
    <div class="consult-section-head kontakt-steps__head">
      <p class="consult-kicker">Co zrobiliśmy</p>
      <h2>Od analizy wody do stałego programu ochrony kotła.</h2>
      <p>Prace prowadziliśmy bez demontażu układu i bez długiego postoju kotłowni.</p>
    </div>
    <ol class="kontakt-steps__list kontakt-steps__list--4"><li class="kontakt-step reveal"><span class="kontakt-step__no">1</span><h3>Analiza wody i oględziny</h3><p>Pomiar twardości, przewodności i pH oraz ocena stanu powierzchni grzewczych.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">2</span><h3>Chemiczne odkamienianie</h3><p>Preparat KCAQUA rozpuścił osad i przywrócił wymianę ciepła.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">3</span><h3>Program KCAQUA 303</h3><p>Wdrożyliśmy kondycjonowanie wody kotłowej z korektą pH i ochroną antykorozyjną.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">4</span><h3>Monitoring i korekta</h3><p>Kontrolujemy parametry wody i dozowanie, a efekty raportujemy.</p></li></ol>
  </div>
</section>
<section class="consult-section consult-section--value case-results-section" id="efekty">
  <span class="consult-watermark consult-watermark--light" aria-hidden="true"></span>
  <div class="wrap">
    <div class="consult-section-head case-results-head">
      <p class="consult-kicker">Efekty wdrożenia</p>
      <h2>Parametry kotłowni przed i po programie KCAQUA.</h2>
      <p>Najważniejsze wskaźniki pracy kotła po 6 tygodniach od wdrożenia.</p>
    </div>
    <div class="case-results"><article class="case-result reveal"><span class="case-result__big"><b class="num-counter" data-count-to="32" data-prefix="−" data-suffix="%">0</b></span><span class="case-result__label">zużycia paliwa</span><span class="case-result__ba"><em>przed: poziom 100%</em><em>po: trwały spadek</em></span></article><article class="case-result reveal"><span class="case-result__big"><b class="num-counter" data-count-to="2800">0</b><i>µS</i></span><span class="case-result__label">przewodność wody</span><span class="case-result__ba"><em>przed: 4200 µS</em><em>po: 2800 µS</em></span></article><article class="case-result reveal"><span class="case-result__big"><b>0,02</b><i>°n</i></span><span class="case-result__label">twardość wody</span><span class="case-result__ba"><em>przed: 8°n</em><em>po: 0,02°n</em></span></article><article class="case-result reveal"><span class="case-result__big"><b class="num-counter" data-count-to="12">0</b><i>mies.</i></span><span class="case-result__label">cykl między czyszczeniami</span><span class="case-result__ba"><em>przed: co 3 miesiące</em><em>po: co 12 miesięcy</em></span></article></div>
    <p class="case-results__note">Dane liczbowe są przykładowe i przed publikacją wymagają autoryzacji klienta.</p>
  </div>
</section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/kotly-parowe/kondycjonowanie-wody-kotlowej/">Kondycjonowanie wody kotłowej</a></li><li><a href="/kotly-parowe/odkamienianie/">Odkamienianie kotłów parowych</a></li><li><a href="/bezplatna-konsultacja/">Audyt techniczny instalacji</a></li></ul></div></section>
<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Podobna instalacja?</p>
        <h2>Sprawdź kondycję swojej kotłowni.</h2>
        <p>Inżynier Kabi-Chemie oceni wodę i instalację, a następnie zaproponuje konkretny plan działania.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>
        <a class="consult-final__tel" href="/case-study/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>Zobacz pozostałe case studies</span></a>
      </div>
    </div>
  </div>
</section>""")],
}

PAGES["/case-study/skraplacz-bac-kcaqua/"] = {
    "og_type": 'article',
    "body_class": 'has-dark-hero',
    "sections": [custom("""
<section class="consult-hero" id="top">
  <div class="consult-hero__bg" aria-hidden="true"></div>
  <div class="wrap consult-hero__inner">
    <div class="consult-hero__copy">
      <p class="consult-kicker">Case study · Chłodnictwo przemysłowe</p>
      <h1>Optymalizacja pracy skraplacza BAC preparatem <em>KCAQUA 305</em></h1>
      <p class="consult-lead">Skraplacz wyparny BAC tracił wydajność przez osady i kamień. Dozowanie KCAQUA 305 ustabilizowało pracę układu i ograniczyło zużycie wody uzupełniającej.</p>
      <div class="consult-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/case-study/">Zobacz inne realizacje</a></div>
      <ul class="consult-hero__points" aria-label="Najważniejsze informacje"><li>Skraplacz wyparny BAC</li><li>Program KCAQUA 305</li><li>Stabilna praca układu</li></ul>
    </div>
    <div class="consult-hero__visual">
      <div class="consult-hero__frame">
        <img src="/assets/case/case-bac-kcaqua-generated.png" alt="Skraplacz wyparny BAC objęty programem KCAQUA 305" loading="eager">
      </div>
    </div>
  </div>
  <div class="consult-proof" aria-label="Najważniejsze informacje"><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v20M4 6l16 12M20 6 4 18"/><path d="M12 5 9.5 7M12 5l2.5 2M12 19l-2.5-2M12 19l2.5-2"/></svg></span><strong>Instalacja</strong><span>Skraplacz wyparny BAC w układzie chłodniczym.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6M10 3v6l-5 8a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-8V3"/><path d="M7.5 14h9"/></svg></span><strong>Zakres prac</strong><span>Biocyd, inhibitor i antyskalant w jednym programie.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><strong>Kluczowy efekt</strong><span>Mniej wody uzupełniającej i osadów.</span></div></div>
</section>
<section class="consult-section consult-section--light">
  <div class="wrap">
    <div class="consult-section-head">
      <p class="consult-kicker">Wyzwanie</p>
      <h2>Osady pogarszały chłodzenie i zwiększały zużycie wody.</h2>
      <p>Układ wymagał coraz częstszych interwencji, a koszty wody uzupełniającej rosły z miesiąca na miesiąc.</p>
    </div>
    <div class="consult-fit-grid consult-fit-grid--3"><article class="fitcard"><span class="fitcard__no" aria-hidden="true">01</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3c2 3 5 4.5 5 8a5 5 0 0 1-10 0c0-1.5.7-2.7 1.5-3.5C9 9 9.5 7 9 5c2 .5 2.5 1.5 3 2 .3-1.2.2-2.7 0-4Z"/></svg></span><h3>Słabsza wymiana ciepła</h3><p>Osady na powierzchniach wymiany ciepła obniżały skuteczność chłodzenia.</p><span class="fitcard__tag">Wydajność</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">02</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><h3>Rosnące zużycie wody</h3><p>Częste odsalanie i uzupełnianie obiegu podnosiło koszty operacyjne.</p><span class="fitcard__tag">Woda · koszty</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">03</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h16M7 20V10M12 20V5M17 20v-7"/></svg></span><h3>Niestabilna praca</h3><p>Wydajność układu wahała się wraz z narastaniem osadów.</p><span class="fitcard__tag">Stabilność</span></article></div>
  </div>
</section>
<section class="consult-section kontakt-steps">
  <span class="consult-watermark" aria-hidden="true"></span>
  <div class="wrap">
    <div class="consult-section-head kontakt-steps__head">
      <p class="consult-kicker">Co zrobiliśmy</p>
      <h2>Jeden program zamiast trzech osobnych preparatów.</h2>
      <p>KCAQUA 305 łączy biocyd, inhibitor korozji i antyskalant, więc prowadzenie układu jest prostsze.</p>
    </div>
    <ol class="kontakt-steps__list"><li class="kontakt-step reveal"><span class="kontakt-step__no">1</span><h3>Dobór preparatu KCAQUA 305</h3><p>Program dobrany do jakości wody i obciążenia skraplacza.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">2</span><h3>Dozowanie i kontrola przewodności</h3><p>Ustawiliśmy pompy dozujące oraz limity odsalania obiegu.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">3</span><h3>Monitoring i korekta</h3><p>W pierwszych tygodniach dostroiliśmy dawki do rzeczywistej pracy układu.</p></li></ol>
  </div>
</section>
<section class="consult-section consult-section--value case-results-section" id="efekty">
  <span class="consult-watermark consult-watermark--light" aria-hidden="true"></span>
  <div class="wrap">
    <div class="consult-section-head case-results-head">
      <p class="consult-kicker">Efekty wdrożenia</p>
      <h2>Mniej wody i stabilna wydajność chłodzenia.</h2>
      <p>Najważniejsze zmiany zaobserwowane po wdrożeniu programu KCAQUA 305.</p>
    </div>
    <div class="case-results"><article class="case-result reveal"><span class="case-result__big"><b class="num-counter" data-count-to="40" data-prefix="−" data-suffix="%">0</b></span><span class="case-result__label">zużycia wody uzupełniającej</span><span class="case-result__ba"><em>przed: poziom 100%</em><em>po: trwały spadek</em></span></article><article class="case-result reveal"><span class="case-result__big case-result__big--text"><b>Pod kontrolą</b></span><span class="case-result__label">osady na wymienniku</span><span class="case-result__ba"><em>przed: narastające</em><em>po: kontrolowane</em></span></article><article class="case-result reveal"><span class="case-result__big case-result__big--text"><b>Stabilna</b></span><span class="case-result__label">praca układu chłodzenia</span><span class="case-result__ba"><em>przed: spadki wydajności</em><em>po: równa praca</em></span></article></div>
    <p class="case-results__note">Dane liczbowe są przykładowe i przed publikacją wymagają autoryzacji klienta.</p>
  </div>
</section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/uklady-chlodnicze/skraplacze-amoniakalne/">Skraplacze amoniakalne</a></li><li><a href="/uklady-chlodnicze/ochrona-wiez-chlodniczych/">Ochrona wież chłodniczych</a></li><li><a href="/uklady-chlodnicze/">Układy chłodnicze</a></li></ul></div></section>
<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Podobna instalacja?</p>
        <h2>Policz, ile wody może oszczędzić Twój skraplacz.</h2>
        <p>Inżynier Kabi-Chemie oceni układ chłodniczy i zaproponuje program dobrany do Twojej wody.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>
        <a class="consult-final__tel" href="/case-study/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>Zobacz pozostałe case studies</span></a>
      </div>
    </div>
  </div>
</section>""")],
}

PAGES["/case-study/skraplacz-evapco-przetworstwo-rybne/"] = {
    "og_type": 'article',
    "body_class": 'has-dark-hero',
    "sections": [custom("""
<section class="consult-hero" id="top">
  <div class="consult-hero__bg" aria-hidden="true"></div>
  <div class="wrap consult-hero__inner">
    <div class="consult-hero__copy">
      <p class="consult-kicker">Case study · Przetwórstwo rybne</p>
      <h1>Chemiczne czyszczenie skraplacza <em>Evapco</em> w przetwórstwie rybnym</h1>
      <p class="consult-lead">Skraplacz pokrył się twardym kamieniem i tracił wydajność chłodzenia. Wykonaliśmy czyszczenie chemiczne i wdrożyliśmy program kondycjonowania, który chroni układ na co dzień.</p>
      <div class="consult-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/case-study/">Zobacz inne realizacje</a></div>
      <ul class="consult-hero__points" aria-label="Najważniejsze informacje"><li>Skraplacz Evapco</li><li>Czyszczenie bez demontażu</li><li>Stały program ochrony</li></ul>
    </div>
    <div class="consult-hero__visual">
      <div class="consult-hero__frame">
        <img src="/assets/case/case-evapco-fish-generated.png" alt="Hala przetwórstwa rybnego chłodzona skraplaczem Evapco" loading="eager">
      </div>
    </div>
  </div>
  <div class="consult-proof" aria-label="Najważniejsze informacje"><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21h18V10l-6 4V10l-6 4V6H3Z"/><path d="M7 21v-4M11 21v-4M15 21v-4"/></svg></span><strong>Zakład</strong><span>Przetwórstwo rybne z ciągłą pracą chłodu.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 4a5 5 0 0 1-6.5 6.5L6 19a2.1 2.1 0 0 1-3-3l8.5-8.5A5 5 0 0 1 18 3l-3 3 3 3 3-3Z"/></svg></span><strong>Zakres prac</strong><span>Czyszczenie chemiczne i program kondycjonowania.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v20M4 6l16 12M20 6 4 18"/><path d="M12 5 9.5 7M12 5l2.5 2M12 19l-2.5-2M12 19l2.5-2"/></svg></span><strong>Kluczowy efekt</strong><span>Odzyskana wydajność chłodzenia.</span></div></div>
</section>
<section class="consult-section consult-section--light">
  <div class="wrap">
    <div class="consult-section-head">
      <p class="consult-kicker">Wyzwanie</p>
      <h2>Twardy kamień na wężownicy ograniczał wymianę ciepła.</h2>
      <p>W zakładzie spożywczym każda utrata chłodu to ryzyko dla produkcji, dlatego liczył się czas reakcji.</p>
    </div>
    <div class="consult-fit-grid consult-fit-grid--3"><article class="fitcard"><span class="fitcard__no" aria-hidden="true">01</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><h3>Kamień na wężownicy</h3><p>Twardy osad ograniczał wymianę ciepła i wydajność skraplacza.</p><span class="fitcard__tag">Osady</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">02</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7Z"/></svg></span><h3>Wyższe koszty energii</h3><p>Układ potrzebował coraz więcej energii, aby utrzymać temperatury.</p><span class="fitcard__tag">Energia</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">03</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21h18V10l-6 4V10l-6 4V6H3Z"/><path d="M7 21v-4M11 21v-4M15 21v-4"/></svg></span><h3>Ryzyko przestojów</h3><p>Spadek wydajności chłodzenia zagrażał ciągłości produkcji.</p><span class="fitcard__tag">Produkcja</span></article></div>
  </div>
</section>
<section class="consult-section kontakt-steps">
  <span class="consult-watermark" aria-hidden="true"></span>
  <div class="wrap">
    <div class="consult-section-head kontakt-steps__head">
      <p class="consult-kicker">Co zrobiliśmy</p>
      <h2>Czyszczenie chemiczne bez demontażu i długiego postoju.</h2>
      <p>Po przywróceniu wydajności zabezpieczyliśmy układ stałym programem kondycjonowania.</p>
    </div>
    <ol class="kontakt-steps__list"><li class="kontakt-step reveal"><span class="kontakt-step__no">1</span><h3>Oględziny i analiza wody</h3><p>Ocena osadu na wężownicy oraz parametrów wody chłodzącej.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">2</span><h3>Czyszczenie chemiczne</h3><p>Preparat rozpuścił kamień i odsłonił czyste powierzchnie wymiany ciepła.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">3</span><h3>Program kondycjonowania</h3><p>Stałe dozowanie i monitoring chronią układ przed nawrotem osadów.</p></li></ol>
  </div>
</section>
<section class="consult-section consult-section--value case-results-section" id="efekty">
  <span class="consult-watermark consult-watermark--light" aria-hidden="true"></span>
  <div class="wrap">
    <div class="consult-section-head case-results-head">
      <p class="consult-kicker">Efekty wdrożenia</p>
      <h2>Skraplacz wrócił do pełnej wydajności chłodzenia.</h2>
      <p>Najważniejsze zmiany po czyszczeniu chemicznym i wdrożeniu programu.</p>
    </div>
    <div class="case-results"><article class="case-result reveal"><span class="case-result__big"><b class="num-counter" data-count-to="100" data-suffix="%">0</b></span><span class="case-result__label">wydajności chłodzenia</span><span class="case-result__ba"><em>przed: ograniczona osadem</em><em>po: przywrócona</em></span></article><article class="case-result reveal"><span class="case-result__big case-result__big--text"><b>Usunięty</b></span><span class="case-result__label">kamień z wężownicy</span><span class="case-result__ba"><em>przed: twardy osad</em><em>po: czyste powierzchnie</em></span></article><article class="case-result reveal"><span class="case-result__big"><b>Stała</b></span><span class="case-result__label">ochrona układu</span><span class="case-result__ba"><em>przed: brak programu</em><em>po: kondycjonowanie i monitoring</em></span></article></div>
    <p class="case-results__note">Dane liczbowe są przykładowe i przed publikacją wymagają autoryzacji klienta.</p>
  </div>
</section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/uklady-chlodnicze/odkamienianie/">Odkamienianie układów chłodniczych</a></li><li><a href="/uklady-chlodnicze/skraplacze-amoniakalne/">Skraplacze amoniakalne</a></li><li><a href="/branze/">Woda w przemyśle spożywczym</a></li></ul></div></section>
<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Podobna instalacja?</p>
        <h2>Odzyskaj wydajność chłodzenia bez wymiany urządzeń.</h2>
        <p>Inżynier Kabi-Chemie oceni skraplacz i dobierze bezpieczny sposób czyszczenia oraz ochrony.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>
        <a class="consult-final__tel" href="/case-study/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>Zobacz pozostałe case studies</span></a>
      </div>
    </div>
  </div>
</section>""")],
}

PAGES["/case-study/warsztaty-amoniakalne-2024/"] = {
    "og_type": 'article',
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/industries/industry-cold-storage.jpg')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Case study · wynik w liczbach</p><h1>Warsztaty Amoniakalne 2024 - Nasza relacja i prelekcje</h1><p class="lead">Uczestniczyliśmy w Warsztatach Amoniakalnych, jednym z najważniejszych wydarzeń branży chłodnictwa amoniakalnego w Polsce. Dzielimy się relacją i wnioskami z prelekcji.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/uklady-chlodnicze/">Zobacz układy chłodnicze</a><a class="btn btn-ghost" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/industries/industry-cold-storage.jpg" alt="wdrożenie KCAQUA pokazane na danych i pracy instalacji" loading="eager">
      <figcaption>wdrożenie KCAQUA pokazane na danych i pracy instalacji</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap narrow prose"><h2>Dlaczego tam jesteśmy</h2><p>Warsztaty Amoniakalne to miejsce wymiany wiedzy między inżynierami i służbami utrzymania ruchu. Prezentujemy tam praktyczne podejście do kondycjonowania wody w skraplaczach natryskowo-wyparnych.</p><p class="note">Element budujący E-E-A-T: potwierdza nasze doświadczenie i obecność w środowisku branżowym.</p></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/uklady-chlodnicze/skraplacze-amoniakalne/">Skraplacze amoniakalne</a></li><li><a href="/baza-wiedzy/korozja/">Biała korozja na ocynku, baza wiedzy</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/faq/"] = {
    "body_class": 'has-dark-hero firm-page firm-faq-page',
    "jsonld": [{'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': 'Czym zajmuje się Kabi-Chemie?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Kabi-Chemie projektuje programy kondycjonowania wody przemysłowej dla kotłów parowych, układów chłodniczych, skraplaczy wyparnych i instalacji RO.'}}, {'@type': 'Question', 'name': 'Czym jest technologia KCAQUA?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'KCAQUA to autorska technologia chemiczna Kabi-Chemie, która łączy preparaty, dozowanie, monitoring i raportowanie efektów w instalacjach przemysłowych.'}}, {'@type': 'Question', 'name': 'Czy pierwsza konsultacja jest bezpłatna?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Pierwsza rozmowa techniczna i wstępne rozpoznanie problemu są bezpłatne i nie zobowiązują do zakupu chemii ani usługi.'}}, {'@type': 'Question', 'name': 'Jak wygląda audyt techniczny?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Inżynier analizuje typ instalacji, parametry wody, koszty mediów, sposób dozowania chemii i miejsca, w których zakład traci wodę, energię lub stabilność pracy.'}}, {'@type': 'Question', 'name': 'Czy Kabi-Chemie obsługuje zakłady w całej Polsce?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Firma działa z Siedlec i oddziału w Toruniu, a wdrożenia realizuje w zakładach przemysłowych w różnych regionach Polski.'}}, {'@type': 'Question', 'name': 'Czy KCAQUA może zastąpić dotychczasową chemię?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'W wielu instalacjach tak, ale decyzję poprzedza analiza wody, warunków pracy i celu technicznego. Nie zmieniamy programu bez diagnozy.'}}, {'@type': 'Question', 'name': 'Kiedy widać efekty wdrożenia?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Część efektów, na przykład stabilizacja parametrów, może być widoczna szybko. Usuwanie osadów, ograniczenie strat i potwierdzenie oszczędności wymaga pomiarów w czasie.'}}, {'@type': 'Question', 'name': 'Czy przygotowujecie raport dla zarządu?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Po audycie i wdrożeniu możemy przygotować podsumowanie techniczne z danymi o wodzie, energii, ściekach, osadach i ryzykach eksploatacyjnych.'}}]}],
    "sections": [custom("""
<section class="firm-hero firm-hero--faq" style="--firm-bg:url('/assets/blog/blog-water-reduction.png')" id="top">
  <div class="firm-hero__shade" aria-hidden="true"></div>
  <div class="wrap firm-hero__inner">
    <div class="firm-hero__copy reveal-left">
      <p class="firm-kicker">FAQ Kabi-Chemie</p>
      <h1>Najczęstsze pytania o kondycjonowanie wody przemysłowej.</h1>
      <p>Odpowiadamy prostym językiem na pytania, które najczęściej pojawiają się przed audytem, zmianą chemii, wdrożeniem KCAQUA lub kontaktem z naszym inżynierem.</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="/kontakt/">Zadaj pytanie techniczne</a>
        <a class="btn btn-ghost-light" href="/baza-wiedzy/">Przejdź do bazy wiedzy</a>
      </div>
    </div>
    <nav class="firm-faq-jump reveal-right" aria-label="Kategorie pytań">
      <a href="#faq-firma">Firma i technologia</a>
      <a href="#faq-audyt">Audyt i wdrożenie</a>
      <a href="#faq-instalacje">Instalacje przemysłowe</a>
      <a href="#faq-kontakt">Kontakt i decyzja</a>
    </nav>
  </div>
</section>

<section class="firm-faq" id="faq-firma">
  <div class="wrap firm-faq__grid">
    <div class="firm-faq__intro reveal">
      <p class="firm-kicker">Firma i technologia</p>
      <h2>KCAQUA, producent chemii i sposób pracy.</h2>
    </div>
    <div class="firm-faq__list">
      <details open class="reveal"><summary>Czym zajmuje się Kabi-Chemie?</summary><div><p>Kabi-Chemie projektuje programy kondycjonowania wody przemysłowej dla kotłów parowych, układów chłodniczych, skraplaczy wyparnych i instalacji RO.</p></div></details>
      <details class="reveal"><summary>Czym jest technologia KCAQUA?</summary><div><p>KCAQUA to autorska technologia chemiczna Kabi-Chemie, która łączy preparaty, dozowanie, monitoring i raportowanie efektów w instalacjach przemysłowych.</p></div></details>
      <details class="reveal"><summary>Czy KCAQUA może zastąpić dotychczasową chemię?</summary><div><p>W wielu instalacjach tak, ale decyzję poprzedza analiza wody, warunków pracy i celu technicznego. Nie zmieniamy programu bez diagnozy.</p></div></details>
    </div>
  </div>
</section>

<section class="firm-faq firm-faq--alt" id="faq-audyt">
  <div class="wrap firm-faq__grid">
    <div class="firm-faq__intro reveal">
      <p class="firm-kicker">Audyt i wdrożenie</p>
      <h2>Jak wygląda pierwszy kontakt i start programu.</h2>
    </div>
    <div class="firm-faq__list">
      <details open class="reveal"><summary>Czy pierwsza konsultacja jest bezpłatna?</summary><div><p>Tak. Pierwsza rozmowa techniczna i wstępne rozpoznanie problemu są bezpłatne i nie zobowiązują do zakupu chemii ani usługi.</p></div></details>
      <details class="reveal"><summary>Jak wygląda audyt techniczny?</summary><div><p>Inżynier analizuje typ instalacji, parametry wody, koszty mediów, sposób dozowania chemii i miejsca, w których zakład traci wodę, energię lub stabilność pracy.</p></div></details>
      <details class="reveal"><summary>Kiedy widać efekty wdrożenia?</summary><div><p>Część efektów, na przykład stabilizacja parametrów, może być widoczna szybko. Usuwanie osadów, ograniczenie strat i potwierdzenie oszczędności wymaga pomiarów w czasie.</p></div></details>
    </div>
  </div>
</section>

<section class="firm-faq" id="faq-instalacje">
  <div class="wrap firm-faq__grid">
    <div class="firm-faq__intro reveal">
      <p class="firm-kicker">Instalacje przemysłowe</p>
      <h2>Kotły parowe, chłodnictwo, skraplacze i RO.</h2>
    </div>
    <div class="firm-faq__list">
      <details open class="reveal"><summary>Jakie instalacje obsługujecie najczęściej?</summary><div><p>Najczęściej pracujemy przy kotłach parowych, skraplaczach wyparnych, wieżach chłodniczych, instalacjach RO, wymiennikach i przemysłowych obiegach technologicznych.</p></div></details>
      <details class="reveal"><summary>Czy 1 mm kamienia naprawdę zwiększa zużycie paliwa?</summary><div><p>Tak. Nawet cienka warstwa osadu izoluje powierzchnię wymiany ciepła. W praktyce oznacza to wyższe zużycie paliwa, większe ryzyko przegrzania i częstsze problemy serwisowe.</p></div></details>
      <details class="reveal"><summary>Czy program chemiczny może ograniczyć zużycie wody?</summary><div><p>Tak, jeżeli instalacja pozwala bezpiecznie utrzymywać korzystniejsze parametry pracy. Wtedy można ograniczać zrzuty, odsalanie lub niepotrzebne wymiany wody.</p></div></details>
    </div>
  </div>
</section>

<section class="firm-faq firm-faq--alt" id="faq-kontakt">
  <div class="wrap firm-faq__grid">
    <div class="firm-faq__intro reveal">
      <p class="firm-kicker">Kontakt i decyzja</p>
      <h2>Co przygotować przed rozmową z inżynierem.</h2>
    </div>
    <div class="firm-faq__list">
      <details open class="reveal"><summary>Czy Kabi-Chemie obsługuje zakłady w całej Polsce?</summary><div><p>Tak. Firma działa z Siedlec i oddziału w Toruniu, a wdrożenia realizuje w zakładach przemysłowych w różnych regionach Polski.</p></div></details>
      <details class="reveal"><summary>Czy przygotowujecie raport dla zarządu?</summary><div><p>Tak. Po audycie i wdrożeniu możemy przygotować podsumowanie techniczne z danymi o wodzie, energii, ściekach, osadach i ryzykach eksploatacyjnych.</p></div></details>
      <details class="reveal"><summary>Co jeśli nie wiem, jaki temat wybrać w formularzu?</summary><div><p>Zostaw domyślne „Zapytanie o darmową konsultację”. Formularz od razu przygotuje profesjonalną wiadomość do osoby technicznej.</p></div></details>
    </div>
  </div>
</section>

<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Nie znalazłeś odpowiedzi?</p>
        <h2>Zadaj pytanie bezpośrednio inżynierowi Kabi-Chemie.</h2>
        <p>Wystarczy jedno zdanie o instalacji. Oddzwonimy i doprecyzujemy szczegóły techniczne.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/kontakt/">Przejdź do kontaktu</a>
        <a class="consult-final__tel" href="tel:+48662792875"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg><span>+48 662 792 875</span></a>
      </div>
    </div>
  </div>
</section>
""")],
}

PAGES["/kotly-parowe/"] = {
    "body_class": 'has-dark-hero',
    "jsonld": [{'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': 'Jak kondycjonowanie wody zmniejsza rachunki za paliwo?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Usuwając warstwę kamienia, która izoluje powierzchnie grzewcze. Czysty kocioł oddaje ciepło wodzie znacznie efektywniej.'}}, {'@type': 'Question', 'name': 'Czy program wymaga wyłączenia kotła?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Kondycjonowanie prowadzimy w trakcie normalnej eksploatacji. Odkamienianie chemiczne planujemy zależnie od stanu układu.'}}, {'@type': 'Question', 'name': 'Co się stanie, jeśli nie będę kondycjonować wody?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Narasta kamień i korozja. Rosną koszty paliwa, częstotliwość czyszczeń i ryzyko awarii.'}}, {'@type': 'Question', 'name': 'Jakie parametry wody kotłowej kontrolujecie?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Najczęściej sprawdzamy pH, twardość, przewodność, żelazo i zasadowość. Na tej podstawie dobieramy program dozowania i limity odsalania.'}}, {'@type': 'Question', 'name': 'Czy obsługujecie kotłownie poza Siedlcami i Toruniem?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Pracujemy z zakładami przemysłowymi w całej Polsce. Zespół techniczny planuje wizyty tak, aby połączyć analizę wody, oględziny i rekomendacje w jednym procesie.'}}]}],
    "sections": [custom("""
<section class="consult-hero" id="top">
  <div class="consult-hero__bg" aria-hidden="true"></div>
  <div class="wrap consult-hero__inner">
    <div class="consult-hero__copy">
      <p class="consult-kicker">Rozwiązania · Kotły parowe</p>
      <h1>Kondycjonowanie wody w przemysłowych <em>kotłach parowych</em></h1>
      <p class="consult-lead">Usuwamy kamień, chronimy przed korozją i obniżamy zużycie paliwa. Autorska chemia KCAQUA 303 jest dobierana pod konkretną kotłownię, a nie z półki.</p>
      <div class="consult-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/case-study/kociol-parowy-fako/">Case study: kocioł Fako</a></div>
      <ul class="consult-hero__points" aria-label="Najważniejsze informacje"><li>Mniej paliwa i przestojów</li><li>Ochrona przed korozją</li><li>Monitoring parametrów wody</li></ul>
    </div>
    <div class="consult-hero__visual">
      <div class="consult-hero__frame">
        <img src="/assets/case/case-kociol-parowy.png" alt="Przemysłowy kocioł parowy objęty programem KCAQUA 303" loading="eager">
      </div>
    </div>
  </div>
  <div class="consult-proof" aria-label="Najważniejsze informacje"><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3c2 3 5 4.5 5 8a5 5 0 0 1-10 0c0-1.5.7-2.7 1.5-3.5C9 9 9.5 7 9 5c2 .5 2.5 1.5 3 2 .3-1.2.2-2.7 0-4Z"/></svg></span><strong>1 mm kamienia</strong><span>To nawet +10% zużycia paliwa.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v5c0 4 3 7 7 8 4-1 7-4 7-8V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg></span><strong>Pełna ochrona</strong><span>Inhibitory korozji, odtlenianie i korekta pH.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg></span><strong>Raporty</strong><span>Efekty pokazujemy w danych, nie w obietnicach.</span></div></div>
</section>
<section class="consult-section consult-section--light">
  <div class="wrap">
    <div class="consult-section-head">
      <p class="consult-kicker">Co niszczy kocioł parowy</p>
      <h2>Kamień i korozja podnoszą koszt pary.</h2>
      <p>Każdy z tych problemów narasta powoli i niezauważalnie, aż zaczyna kosztować naprawdę duże pieniądze.</p>
    </div>
    <div class="consult-fit-grid"><article class="fitcard"><span class="fitcard__no" aria-hidden="true">01</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><h3>Kamień kotłowy</h3><p>Izoluje powierzchnie grzewcze. 1 mm osadu to nawet +10% zużycia paliwa.</p><span class="fitcard__tag">KCAQUA 303 + odkamienianie</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">02</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v5c0 4 3 7 7 8 4-1 7-4 7-8V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg></span><h3>Korozja tlenowa</h3><p>Prowadzi do wżerów, nieszczelności rur i kosztownych awarii.</p><span class="fitcard__tag">Inhibitory + wiązanie tlenu</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">03</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6M10 3v6l-5 8a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-8V3"/><path d="M7.5 14h9"/></svg></span><h3>Złe pH wody</h3><p>Przyspiesza korozję i niszczy ochronną warstwę magnetytu.</p><span class="fitcard__tag">Korekta chemiczna</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">04</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h16M7 20V10M12 20V5M17 20v-7"/></svg></span><h3>Nadmierne odsalanie</h3><p>Zła przewodność wymusza częstsze odsalanie, czyli stratę wody i ciepła.</p><span class="fitcard__tag">Kontrola przewodności</span></article></div>
  </div>
</section>
<section class="consult-section kontakt-steps">
  <span class="consult-watermark" aria-hidden="true"></span>
  <div class="wrap">
    <div class="consult-section-head kontakt-steps__head">
      <p class="consult-kicker">Jak działamy</p>
      <h2>Od analizy wody do stałego programu dozowania.</h2>
      <p>Kondycjonowanie prowadzimy w trakcie normalnej eksploatacji, bez wyłączania kotła.</p>
    </div>
    <ol class="kontakt-steps__list kontakt-steps__list--4"><li class="kontakt-step reveal"><span class="kontakt-step__no">1</span><h3>Analiza wody i instalacji</h3><p>Pomiar twardości, pH, przewodności i żelaza oraz ocena kotłowni.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">2</span><h3>Dobór preparatu KCAQUA 303</h3><p>Inhibitor korozji, odtlenianie i korekta pH w jednym programie.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">3</span><h3>Wdrożenie dozowania</h3><p>Ustawienie programu, pomp dozujących i limitów odsalania.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">4</span><h3>Monitoring i korekta</h3><p>Bieżąca kontrola parametrów wody i raportowanie efektów.</p></li></ol>
  </div>
</section>
<section class="consult-section consult-section--value">
  <span class="consult-watermark consult-watermark--light" aria-hidden="true"></span>
  <div class="wrap consult-value">
    <div class="consult-value__intro">
      <p class="consult-kicker">Co zyskuje kotłownia</p>
      <h2>Czysty kocioł to niższe rachunki i spokojniejsza praca.</h2>
      <p class="consult-value__lead">Program KCAQUA 303 łączy ochronę instalacji z wymiernym efektem energetycznym.</p>
    </div>
    <div class="consult-value__list"><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3c2 3 5 4.5 5 8a5 5 0 0 1-10 0c0-1.5.7-2.7 1.5-3.5C9 9 9.5 7 9 5c2 .5 2.5 1.5 3 2 .3-1.2.2-2.7 0-4Z"/></svg></span><div><strong>Mniej paliwa</strong><span>Czyste powierzchnie grzewcze oddają ciepło efektywniej, więc kocioł zużywa mniej paliwa.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M19 12a7 7 0 0 0-.1-1.3l2-1.5-2-3.4-2.3 1a7 7 0 0 0-2.3-1.3L13.8 1h-3.6l-.3 2.2a7 7 0 0 0-2.3 1.3l-2.3-1-2 3.4 2 1.5A7 7 0 0 0 5 12c0 .5 0 .9.1 1.3l-2 1.5 2 3.4 2.3-1a7 7 0 0 0 2.3 1.3l.3 2.2h3.6l.3-2.2a7 7 0 0 0 2.3-1.3l2.3 1 2-3.4-2-1.5c.1-.4.1-.8.1-1.3Z"/></svg></span><div><strong>Dłuższe cykle czyszczenia</strong><span>Rzadsze przestoje na czyszczenie mechaniczne i chemiczne.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v5c0 4 3 7 7 8 4-1 7-4 7-8V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg></span><div><strong>Ochrona przed awarią</strong><span>Mniej korozji i wżerów, czyli mniejsze ryzyko nieszczelności rur.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg></span><div><strong>Dane dla zarządu</strong><span>Raportujemy parametry i oszczędności w zrozumiałych liczbach.</span></div></article></div>
  </div>
</section><section class="section reveal"><div class="wrap"><div class="section-head"><h2>Nasze rozwiązania dla kotłowni</h2></div><div class="card-grid"><a class="card" href="/kotly-parowe/kondycjonowanie-wody-kotlowej/"><h3>Kondycjonowanie wody kotłowej</h3><p>Program dozowania KCAQUA 303, czyli ochrona i oszczędność.</p><span class="card-link">Dowiedz się więcej →</span></a><a class="card" href="/kotly-parowe/odkamienianie/"><h3>Odkamienianie kotłów</h3><p>Chemiczne usuwanie kamienia w trakcie eksploatacji.</p><span class="card-link">Dowiedz się więcej →</span></a><a class="card" href="/kotly-parowe/ochrona-antykorozyjna/"><h3>Ochrona antykorozyjna</h3><p>Inhibitory korozji i wiązanie tlenu w układzie parowym.</p><span class="card-link">Dowiedz się więcej →</span></a></div></div></section><section class="section alt reveal"><div class="wrap narrow faq"><div class="section-head"><h2>Najczęstsze pytania</h2></div><details><summary>Jak kondycjonowanie wody zmniejsza rachunki za paliwo?</summary><div class="faq-a"><p>Usuwając warstwę kamienia, która izoluje powierzchnie grzewcze. Czysty kocioł oddaje ciepło wodzie znacznie efektywniej.</p></div></details><details><summary>Czy program wymaga wyłączenia kotła?</summary><div class="faq-a"><p>Kondycjonowanie prowadzimy w trakcie normalnej eksploatacji. Odkamienianie chemiczne planujemy zależnie od stanu układu.</p></div></details><details><summary>Co się stanie, jeśli nie będę kondycjonować wody?</summary><div class="faq-a"><p>Narasta kamień i korozja. Rosną koszty paliwa, częstotliwość czyszczeń i ryzyko awarii.</p></div></details><details><summary>Jakie parametry wody kotłowej kontrolujecie?</summary><div class="faq-a"><p>Najczęściej sprawdzamy pH, twardość, przewodność, żelazo i zasadowość. Na tej podstawie dobieramy program dozowania i limity odsalania.</p></div></details><details><summary>Czy obsługujecie kotłownie poza Siedlcami i Toruniem?</summary><div class="faq-a"><p>Tak. Pracujemy z zakładami przemysłowymi w całej Polsce. Zespół techniczny planuje wizyty tak, aby połączyć analizę wody, oględziny i rekomendacje w jednym procesie.</p></div></details></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/kotly-parowe/kondycjonowanie-wody-kotlowej/">Kondycjonowanie wody kotłowej</a></li><li><a href="/kotly-parowe/odkamienianie/">Odkamienianie kotłów parowych</a></li><li><a href="/bezplatna-konsultacja/">Audyt techniczny instalacji</a></li></ul></div></section>
<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Zacznij od diagnozy</p>
        <h2>Sprawdź kondycję swojej kotłowni.</h2>
        <p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>
        <a class="consult-final__tel" href="/case-study/kociol-parowy-fako/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>Zobacz case study kotła Fako</span></a>
      </div>
    </div>
  </div>
</section>""")],
}

PAGES["/kotly-parowe/kondycjonowanie-wody-kotlowej/"] = {
    "body_class": 'has-dark-hero',
    "sections": [custom("""
<section class="consult-hero" id="top">
  <div class="consult-hero__bg" aria-hidden="true"></div>
  <div class="wrap consult-hero__inner">
    <div class="consult-hero__copy">
      <p class="consult-kicker">Rozwiązania · Technologia KCAQUA</p>
      <h1>Technologia KCAQUA do wody kotłowej</h1>
      <p class="consult-lead">Prowadzimy kondycjonowanie wody kotłowej w oparciu o pomiar i program dozowania KCAQUA 303, z realnym efektem energetycznym dla kotłowni.</p>
      <div class="consult-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kotly-parowe/">Zobacz rozwiązania dla kotłów</a></div>
      <ul class="consult-hero__points" aria-label="Najważniejsze informacje"><li>Program oparty na pomiarach</li><li>Korekta pH i odtlenianie</li><li>Raportowane efekty</li></ul>
    </div>
    <div class="consult-hero__visual">
      <div class="consult-hero__frame">
        <img src="/assets/blog/blog-boiler-scale.png" alt="Rurociągi kotłowni objęte technologią KCAQUA" loading="eager">
      </div>
    </div>
  </div>
  <div class="consult-proof" aria-label="Najważniejsze informacje"><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6M10 3v6l-5 8a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-8V3"/><path d="M7.5 14h9"/></svg></span><strong>Autorska receptura</strong><span>Preparaty produkujemy i dobieramy sami.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h16M7 20V10M12 20V5M17 20v-7"/></svg></span><strong>Kontrola parametrów</strong><span>pH, twardość, przewodność i żelazo pod nadzorem.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg></span><strong>Jasne normy</strong><span>Docelowe wartości ustalamy dla konkretnego kotła.</span></div></div>
</section>
<section class="consult-section consult-section--light">
  <div class="wrap">
    <div class="consult-section-head">
      <p class="consult-kicker">Parametry wody kotłowej</p>
      <h2>Cztery parametry decydują o bezpieczeństwie i kosztach pracy kotła.</h2>
      <p>Podane zakresy są punktem odniesienia. Docelowe normy dobieramy do konkretnego kotła i wymagań procesu.</p>
    </div>
    <div class="consult-fit-grid"><article class="fitcard"><span class="fitcard__no" aria-hidden="true">01</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6M10 3v6l-5 8a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-8V3"/><path d="M7.5 14h9"/></svg></span><h3>pH: 9,0-11,0</h3><p>Utrzymuje wodę w zakresie bezpiecznym dla stali i chroni przed korozją.</p><span class="fitcard__tag">Ochrona przed korozją</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">02</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><h3>Twardość: < 0,02°n</h3><p>Woda pozbawiona twardości nie wytrąca kamienia na powierzchniach grzewczych.</p><span class="fitcard__tag">Zapobiega kamieniowi</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">03</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7Z"/></svg></span><h3>Przewodność: < 3000 µS</h3><p>Kontrola zasolenia pozwala ograniczyć odsalanie i stratę ciepła.</p><span class="fitcard__tag">Kontrola odsalania</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">04</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v5c0 4 3 7 7 8 4-1 7-4 7-8V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg></span><h3>Żelazo: < 0,1 mg/l</h3><p>Poziom żelaza w wodzie pokazuje, czy w układzie postępuje korozja.</p><span class="fitcard__tag">Wskaźnik korozji</span></article></div>
  </div>
</section>
<section class="consult-section kontakt-steps">
  <span class="consult-watermark" aria-hidden="true"></span>
  <div class="wrap">
    <div class="consult-section-head kontakt-steps__head">
      <p class="consult-kicker">Jak działamy</p>
      <h2>Technologia oparta na pomiarze.</h2>
      <p>Każdy etap programu KCAQUA kończy się konkretnymi liczbami i zaleceniami.</p>
    </div>
    <ol class="kontakt-steps__list"><li class="kontakt-step reveal"><span class="kontakt-step__no">1</span><h3>Analiza wody</h3><p>Pomiar parametrów wody zasilającej i kotłowej oraz ocena instalacji.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">2</span><h3>Dobór preparatu KCAQUA 303</h3><p>Receptura dopasowana do Twojego układu i jakości wody.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">3</span><h3>Wdrożenie i monitoring</h3><p>Dozowanie, kontrola przewodności i pH oraz bieżąca korekta programu.</p></li></ol>
  </div>
</section>
<section class="consult-section consult-section--value">
  <span class="consult-watermark consult-watermark--light" aria-hidden="true"></span>
  <div class="wrap consult-value">
    <div class="consult-value__intro">
      <p class="consult-kicker">Efekt technologii</p>
      <h2>Stabilna woda kotłowa przekłada się na policzalne oszczędności.</h2>
      <p class="consult-value__lead">Technologia KCAQUA łączy chemię, automatykę dozowania i monitoring w jeden system.</p>
    </div>
    <div class="consult-value__list"><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3c2 3 5 4.5 5 8a5 5 0 0 1-10 0c0-1.5.7-2.7 1.5-3.5C9 9 9.5 7 9 5c2 .5 2.5 1.5 3 2 .3-1.2.2-2.7 0-4Z"/></svg></span><div><strong>Niższe zużycie paliwa</strong><span>Czyste powierzchnie grzewcze oznaczają lepszą wymianę ciepła.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><div><strong>Mniej wody i ścieków</strong><span>Wyższa dopuszczalna przewodność to rzadsze odsalanie i odmulanie.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v5c0 4 3 7 7 8 4-1 7-4 7-8V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg></span><div><strong>Dłuższa żywotność kotła</strong><span>Ochrona przed korozją i kamieniem wydłuża życie instalacji.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h16M7 20V10M12 20V5M17 20v-7"/></svg></span><div><strong>Efekty w liczbach</strong><span>Parametry i oszczędności raportujemy w formie czytelnej dla zarządu.</span></div></article></div>
  </div>
</section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/kotly-parowe/odkamienianie/">Odkamienianie kotłów</a></li><li><a href="/kotly-parowe/ochrona-antykorozyjna/">Ochrona antykorozyjna układów parowych</a></li><li><a href="/baza-wiedzy/parametry-wody/">Parametry wody w bazie wiedzy</a></li></ul></div></section>
<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Technologia KCAQUA</p>
        <h2>Sprawdź potencjał technologii KCAQUA.</h2>
        <p>Zaczynamy od analizy wody i rozmowy z inżynierem, bez żadnych zobowiązań.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>
        <a class="consult-final__tel" href="/case-study/kociol-parowy-fako/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>Zobacz case study kotła Fako</span></a>
      </div>
    </div>
  </div>
</section>""")],
}

PAGES["/kotly-parowe/ochrona-antykorozyjna/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/blog/blog-corrosion-pipes.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Rozwiązania · kotły parowe</p><h1>Ochrona antykorozyjna układów parowych i inhibitory korozji</h1><p class="lead">Chronimy układy parowe przed korozją, inhibitory korozji, chemiczne wiązanie tlenu i korekta pH w jednym programie.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/blog/blog-corrosion-pipes.png" alt="kotły parowe, para technologiczna i stabilna woda kotłowa" loading="eager">
      <figcaption>kotły parowe, para technologiczna i stabilna woda kotłowa</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap"><div class="section-head"><h2>Jak chronimy układ parowy</h2></div><div class="feature-grid"><div class="feature"><div class="ficon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v5c0 4 3 7 7 8 4-1 7-4 7-8V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg></div><h3>Inhibitory korozji</h3><p>Tworzą warstwę ochronną na powierzchniach metalu.</p></div><div class="feature"><div class="ficon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></div><h3>Wiązanie tlenu</h3><p>Usuwamy tlen rozpuszczony, główny sprawca korozji tlenowej.</p></div><div class="feature"><div class="ficon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6M10 3v6l-5 8a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-8V3"/><path d="M7.5 14h9"/></svg></div><h3>Korekta pH</h3><p>Utrzymujemy pH w zakresie bezpiecznym dla stali.</p></div></div></div></section><section class="section reveal"><div class="wrap narrow prose"><h2>Warstwa magnetytowa, naturalna ochrona</h2><p>Prawidłowo prowadzony układ buduje na stali ochronną warstwę magnetytu. Naszym zadaniem jest ją utrzymać, a nie zniszczyć agresywną chemią.</p></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/kotly-parowe/kondycjonowanie-wody-kotlowej/">Kondycjonowanie wody kotłowej</a></li><li><a href="/baza-wiedzy/korozja/">Korozja tlenowa, baza wiedzy</a></li><li><a href="/ochrona-antykorozyjna/pasywacja-stali/">Pasywacja stali</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/kotly-parowe/odkamienianie/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/blog/blog-boiler-scale.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Rozwiązania · kotły parowe</p><h1>Chemiczne odkamienianie kotłów parowych</h1><p class="lead">Chemicznie rozpuszczamy kamień w kotłach parowych, przywracamy wymianę ciepła i chronimy instalację przed awariami, bez kosztownego demontażu.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/blog/blog-boiler-scale.png" alt="kotły parowe, para technologiczna i stabilna woda kotłowa" loading="eager">
      <figcaption>kotły parowe, para technologiczna i stabilna woda kotłowa</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap narrow prose"><h2>Po co odkamieniać kocioł?</h2><p>Kamień działa jak izolator. Im grubsza warstwa, tym więcej paliwa potrzeba do wytworzenia pary i tym większe ryzyko przegrzań i pęknięć.</p></div></section><section class="section alt reveal"><div class="wrap"><div class="section-head"><h2>Przebieg odkamieniania</h2></div><ol class="steps"><li><div class="step-num">1</div><div><h3>Ocena stanu i wody</h3><p>Określamy rodzaj i grubość osadu.</p></div></li><li><div class="step-num">2</div><div><h3>Czyszczenie chemiczne</h3><p>Dobrany preparat rozpuszcza kamień.</p></div></li><li><div class="step-num">3</div><div><h3>Płukanie i pasywacja</h3><p>Zabezpieczamy oczyszczone powierzchnie.</p></div></li><li><div class="step-num">4</div><div><h3>Kondycjonowanie</h3><p>Wdrażamy program, by kamień nie wracał.</p></div></li></ol></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/kotly-parowe/kondycjonowanie-wody-kotlowej/">Kondycjonowanie wody kotłowej</a></li><li><a href="/case-study/kociol-parowy-fako/">Case study: kocioł parowy Fako</a></li><li><a href="/ochrona-antykorozyjna/chemiczne-czyszczenie/">Chemiczne czyszczenie instalacji</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/membrany-ro/"] = {
    "body_class": 'has-dark-hero',
    "sections": [custom("""
<section class="consult-hero" id="top">
  <div class="consult-hero__bg" aria-hidden="true"></div>
  <div class="wrap consult-hero__inner">
    <div class="consult-hero__copy">
      <p class="consult-kicker">Rozwiązania · Ochrona membran RO</p>
      <h1>Ochrona membran RO przed foulingiem <em>(Antyskalanty)</em></h1>
      <p class="consult-lead">Chronimy membrany odwróconej osmozy przed kamieniem, foulingiem oraz chlorem. Dobrany antyskalant wydłuża żywotność membran i utrzymuje wydajność stacji RO.</p>
      <div class="consult-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/baza-wiedzy/membrany-ro/">Baza wiedzy o membranach RO</a></div>
      <ul class="consult-hero__points" aria-label="Najważniejsze informacje"><li>Dłuższa żywotność membran</li><li>Stabilny strumień permeatu</li><li>Kontrola chloru i chlorków</li></ul>
    </div>
    <div class="consult-hero__visual">
      <div class="consult-hero__frame">
        <img src="/assets/blog/blog-ro-antiscalant.png" alt="Przemysłowa stacja odwróconej osmozy chroniona antyskalantem" loading="eager">
      </div>
    </div>
  </div>
  <div class="consult-proof" aria-label="Najważniejsze informacje"><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16M15 4v16M3 9h18M3 15h18"/></svg></span><strong>Antyskalant</strong><span>Zapobiega wytrącaniu soli na powierzchni membran.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-8 6-13 14-14 .5 8-4 14-12 14-1 0-2 0-2-3Z"/><path d="M9 15c2-2 4-3 7-4"/></svg></span><strong>Kontrola foulingu</strong><span>Ograniczamy osady organiczne i biologiczne.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7Z"/></svg></span><strong>Wiązanie chloru</strong><span>Preparat wiąże chlor i chlorki degradujące membrany.</span></div></div>
</section>
<section class="consult-section consult-section--light">
  <div class="wrap">
    <div class="consult-section-head">
      <p class="consult-kicker">Co niszczy membrany RO</p>
      <h2>Membrany tracą wydajność przez cztery cichych przeciwników.</h2>
      <p>Fouling i kamień obniżają strumień permeatu i podnoszą ciśnienie pracy, a chlor niszczy membrany trwale.</p>
    </div>
    <div class="consult-fit-grid"><article class="fitcard"><span class="fitcard__no" aria-hidden="true">01</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><h3>Kamień na membranach</h3><p>Wytrącające się sole blokują pory i obniżają strumień permeatu.</p><span class="fitcard__tag">Antyskalant</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">02</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-8 6-13 14-14 .5 8-4 14-12 14-1 0-2 0-2-3Z"/><path d="M9 15c2-2 4-3 7-4"/></svg></span><h3>Fouling organiczny</h3><p>Osady organiczne i biologiczne zarastają powierzchnię membran.</p><span class="fitcard__tag">Kontrola foulingu</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">03</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7Z"/></svg></span><h3>Chlor i chlorki</h3><p>Utleniają warstwę aktywną membrany i skracają jej życie.</p><span class="fitcard__tag">Wiązanie chloru</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">04</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h16M7 20V10M12 20V5M17 20v-7"/></svg></span><h3>Rosnące ciśnienie pracy</h3><p>Zablokowane membrany wymagają wyższego ciśnienia i większej energii.</p><span class="fitcard__tag">Niższe koszty energii</span></article></div>
  </div>
</section>
<section class="consult-section kontakt-steps">
  <span class="consult-watermark" aria-hidden="true"></span>
  <div class="wrap">
    <div class="consult-section-head kontakt-steps__head">
      <p class="consult-kicker">Jak działamy</p>
      <h2>Ochrona membran zaczyna się od analizy wody zasilającej.</h2>
      <p>Antyskalant dobieramy do składu wody, a nie odwrotnie.</p>
    </div>
    <ol class="kontakt-steps__list kontakt-steps__list--4"><li class="kontakt-step reveal"><span class="kontakt-step__no">1</span><h3>Analiza wody zasilającej</h3><p>Skład chemiczny wody decyduje o doborze preparatu i dawki.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">2</span><h3>Dobór antyskalantu</h3><p>Preparat dopasowany do soli, które realnie zagrażają membranom.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">3</span><h3>Dozowanie i kontrola</h3><p>Ustawienie pomp dozujących i parametrów pracy stacji.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">4</span><h3>Monitoring i raporty</h3><p>Śledzimy ciśnienie, przewodność i strumień permeatu.</p></li></ol>
  </div>
</section>
<section class="consult-section consult-section--value">
  <span class="consult-watermark consult-watermark--light" aria-hidden="true"></span>
  <div class="wrap consult-value">
    <div class="consult-value__intro">
      <p class="consult-kicker">Co zyskuje stacja RO</p>
      <h2>Chronione membrany pracują dłużej i taniej.</h2>
      <p class="consult-value__lead">Program ochrony membran zwraca się w oszczędzonych wymianach i energii.</p>
    </div>
    <div class="consult-value__list"><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16M15 4v16M3 9h18M3 15h18"/></svg></span><div><strong>Dłuższa żywotność membran</strong><span>Rzadsze wymiany modułów RO to bezpośrednia oszczędność.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><div><strong>Stabilny permeat</strong><span>Stała wydajność stacji bez nagłych spadków produkcji wody.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7Z"/></svg></span><div><strong>Niższe ciśnienie i energia</strong><span>Czyste membrany wymagają niższego ciśnienia roboczego.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M19 12a7 7 0 0 0-.1-1.3l2-1.5-2-3.4-2.3 1a7 7 0 0 0-2.3-1.3L13.8 1h-3.6l-.3 2.2a7 7 0 0 0-2.3 1.3l-2.3-1-2 3.4 2 1.5A7 7 0 0 0 5 12c0 .5 0 .9.1 1.3l-2 1.5 2 3.4 2.3-1a7 7 0 0 0 2.3 1.3l.3 2.2h3.6l.3-2.2a7 7 0 0 0 2.3-1.3l2.3 1 2-3.4-2-1.5c.1-.4.1-.8.1-1.3Z"/></svg></span><div><strong>Rzadsze mycia CIP</strong><span>Mniej chemicznych myć, czyli mniej przestojów i chemii.</span></div></article></div>
  </div>
</section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/baza-wiedzy/membrany-ro/">Antyskalanty w bazie wiedzy</a></li><li><a href="/uslugi/analiza-wody/">Analiza wody</a></li><li><a href="/odkamienianie-instalacji/">Odkamienianie instalacji</a></li></ul></div></section>
<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Zacznij od diagnozy</p>
        <h2>Sprawdź ochronę membran RO.</h2>
        <p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>
        <a class="consult-final__tel" href="/baza-wiedzy/membrany-ro/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>Przejdź do bazy wiedzy o RO</span></a>
      </div>
    </div>
  </div>
</section>""")],
}

PAGES["/ochrona-antykorozyjna/chemiczne-czyszczenie/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/impact/impact-04-installation-protection.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Rozwiązania · antykorozja</p><h1>Chemiczne czyszczenie instalacji przemysłowych</h1><p class="lead">Specjalistyczne chemiczne czyszczenie instalacji przemysłowych, usuwamy uporczywe osady i przywracamy przepływy oraz wydajność układu.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/impact/impact-04-installation-protection.png" alt="ochrona metalu, pasywacja i kontrola korozji" loading="eager">
      <figcaption>ochrona metalu, pasywacja i kontrola korozji</figcaption>
    </figure>
  </div>
</section><section class="section alt reveal"><div class="wrap"><div class="section-head"><h2>Przebieg czyszczenia chemicznego</h2></div><ol class="steps"><li><div class="step-num">1</div><div><h3>Diagnoza</h3><p>Identyfikujemy osad i dobieramy bezpieczny preparat.</p></div></li><li><div class="step-num">2</div><div><h3>Czyszczenie</h3><p>Rozpuszczamy osady w obiegu zamkniętym.</p></div></li><li><div class="step-num">3</div><div><h3>Neutralizacja i pasywacja</h3><p>Zabezpieczamy oczyszczone powierzchnie.</p></div></li></ol></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/odkamienianie-instalacji/">Odkamienianie instalacji</a></li><li><a href="/ochrona-antykorozyjna/pasywacja-stali/">Pasywacja stali</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/ochrona-antykorozyjna/pasywacja-stali/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/impact/impact-04-installation-protection.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Rozwiązania · antykorozja</p><h1>Pasywacja chemiczna stali nierdzewnej i węglowej</h1><p class="lead">Pasywujemy stal nierdzewną i węglową, zabezpieczamy nowe instalacje przemysłowe przed korozją, zanim zacznie się problem.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/impact/impact-04-installation-protection.png" alt="ochrona metalu, pasywacja i kontrola korozji" loading="eager">
      <figcaption>ochrona metalu, pasywacja i kontrola korozji</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap narrow prose"><h2>Czym jest pasywacja</h2><p>Pasywacja to chemiczne wytworzenie lub odtworzenie warstwy ochronnej na powierzchni stali. Dla instalacji po montażu lub spawaniu to kluczowy krok wydłużający żywotność.</p></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/ochrona-antykorozyjna/chemiczne-czyszczenie/">Chemiczne czyszczenie instalacji</a></li><li><a href="/baza-wiedzy/korozja/">Pasywacja stali, baza wiedzy</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/polityka-prywatnosci/"] = {
    "body_class": "has-dark-hero privacy-page",
    "og_image": "/assets/visuals-v2/hero-privacy-control-v1.webp",
    "preload_image": "/assets/visuals-v2/hero-privacy-control-v1.webp",
    "sections": [custom("""<section class="solution-hero privacy-hero" id="top" style="--solution-image:url('/assets/visuals-v2/hero-privacy-control-v1.webp'); --solution-position:center center">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner">
    <div class="solution-hero__copy">
      <p class="solution-kicker"><span></span>Kabi-Chemie / ochrona danych</p>
      <h1>Polityka prywatności.</h1>
      <p class="solution-hero__lead">Jasne zasady ochrony danych osobowych, zapytań B2B i informacji technicznych przekazywanych Kabi-Chemie.</p>
    </div>
  </div>
</section><section class="section reveal"><div class="wrap narrow prose">
<p class="note">Wersja obowiązująca od 2 lipca 2026 r. Dokument opisuje, jak Kabi-Chemie przetwarza dane osób korzystających ze strony, wysyłających formularz, dzwoniących, piszących e-mail lub przekazujących informacje techniczne dotyczące instalacji przemysłowej.</p>

<h2>1. Administrator danych</h2>
<p>Administratorem danych osobowych jest Kabi-Chemie, Żabokliki-Kolonia, ul. Stocka 10, 08-110 Siedlce, NIP: 8212519774, dalej jako Administrator lub Kabi-Chemie.</p>
<p>W sprawach dotyczących ochrony danych można skontaktować się z nami mailowo: <a href="mailto:info@kondycjonowanie-wody.pl">info@kondycjonowanie-wody.pl</a>, telefonicznie: <a href="tel:+48662792875">+48 662 792 875</a> albo pisemnie na adres siedziby.</p>

<h2>2. Zakres danych</h2>
<p>Przetwarzamy tylko dane, które są potrzebne do obsługi strony, kontaktu i zapytań biznesowych. Mogą to być w szczególności: imię i nazwisko, nazwa firmy, stanowisko lub dział, numer telefonu, adres e-mail, treść wiadomości, dane przekazane podczas rozmowy, informacje o instalacji, załączone materiały techniczne, adres IP oraz podstawowe logi serwera.</p>
<p>Nie prosimy o przekazywanie danych szczególnych kategorii, danych prywatnych pracowników, numerów dokumentów, danych medycznych ani innych informacji, które nie są potrzebne do rozmowy o instalacji. Jeżeli takie dane zostaną przesłane, możemy je pominąć, ograniczyć ich zakres albo poprosić o przekazanie zapytania bez tych informacji.</p>
<p>Jeżeli osoba kontaktująca się działa w imieniu firmy lub przekazuje dane współpracownika, przyjmujemy, że robi to w ramach spraw zawodowych i ma podstawę do przekazania tych danych Kabi-Chemie.</p>

<h2>3. Cele i podstawy prawne przetwarzania</h2>
<p>Dane przetwarzamy wyłącznie wtedy, gdy mamy do tego podstawę prawną. Najczęściej jest to obsługa zapytania, przygotowanie oferty, realizacja umowy, obowiązek prawny albo prawnie uzasadniony interes Kabi-Chemie.</p>
<div class="table-wrap"><table>
  <thead><tr><th>Cel</th><th>Podstawa prawna</th></tr></thead>
  <tbody>
    <tr><td>Obsługa formularza, oddzwonienie, odpowiedź na e-mail lub przygotowanie pierwszej rekomendacji technicznej.</td><td>Art. 6 ust. 1 lit. b RODO, gdy zapytanie zmierza do zawarcia umowy, albo art. 6 ust. 1 lit. f RODO, czyli prawnie uzasadniony interes polegający na obsłudze zapytań biznesowych.</td></tr>
    <tr><td>Przygotowanie oferty, dobór rozwiązania, ustalenie zakresu audytu, konsultacji, serwisu lub współpracy.</td><td>Art. 6 ust. 1 lit. b RODO lub art. 6 ust. 1 lit. f RODO.</td></tr>
    <tr><td>Kontakt z przedstawicielami klientów, dostawców i partnerów w sprawach zawodowych.</td><td>Art. 6 ust. 1 lit. f RODO, prawnie uzasadniony interes polegający na utrzymaniu relacji B2B.</td></tr>
    <tr><td>Archiwizacja korespondencji, wykazanie przebiegu ustaleń, dochodzenie roszczeń lub obrona przed roszczeniami.</td><td>Art. 6 ust. 1 lit. f RODO.</td></tr>
    <tr><td>Realizacja obowiązków podatkowych, rachunkowych i prawnych.</td><td>Art. 6 ust. 1 lit. c RODO.</td></tr>
    <tr><td>Bezpieczeństwo strony, diagnostyka błędów, ochrona przed nadużyciami i zapewnienie ciągłości działania serwisu.</td><td>Art. 6 ust. 1 lit. f RODO.</td></tr>
  </tbody>
</table></div>

<h2>4. Formularze kontaktowe</h2>
<p>Podanie danych w formularzu jest dobrowolne, ale numer telefonu oraz dane identyfikujące firmę lub osobę kontaktową są wymagane, abyśmy mogli realnie obsłużyć zapytanie i oddzwonić. Adres e-mail oraz treść wiadomości są opcjonalne, chyba że użytkownik chce otrzymać odpowiedź mailowo albo przekazać dodatkowy kontekst techniczny.</p>
<p>Akceptacja polityki prywatności potwierdza, że użytkownik zapoznał się z informacją o przetwarzaniu danych. Nie jest zgodą marketingową i nie oznacza zapisu do newslettera.</p>

<h2>5. Dane techniczne i logi serwera</h2>
<p>Serwis może zapisywać standardowe dane techniczne, takie jak adres IP, data i godzina żądania, adres odwiedzanej podstrony, typ przeglądarki, system operacyjny oraz status odpowiedzi serwera. Dane te służą bezpieczeństwu, diagnostyce błędów i prawidłowemu działaniu strony.</p>
<p>Na dzień publikacji tej polityki strona nie korzysta z opcjonalnego panelu zgód cookies ani z dodatkowych narzędzi analitycznych lub marketingowych wymagających odrębnej zgody użytkownika. Jeżeli takie narzędzia zostaną wdrożone w przyszłości, dokument i wymagane mechanizmy informacyjne zostaną odpowiednio uzupełnione.</p>

<h2>6. Odbiorcy danych</h2>
<p>Dane mogą być udostępniane tylko podmiotom, które pomagają nam prowadzić stronę, obsługiwać zapytania i realizować obowiązki firmy. Mogą to być w szczególności dostawcy hostingu, poczty e-mail, usług IT, narzędzi formularzy, księgowość, doradcy, kancelarie, podmioty serwisowe oraz organy publiczne, gdy wymagają tego przepisy prawa.</p>
<p>Podmioty działające na nasze zlecenie otrzymują dane wyłącznie w zakresie potrzebnym do wykonania swoich usług i na podstawie odpowiednich umów, upoważnień albo innych zabezpieczeń wymaganych przez RODO.</p>

<h2>7. Przekazywanie danych poza EOG</h2>
<p>Co do zasady korzystamy z dostawców działających w Europejskim Obszarze Gospodarczym. Jeżeli w ramach używanych usług dojdzie do przekazania danych poza EOG, odbywa się to tylko na podstawie mechanizmów dopuszczonych przez RODO, takich jak decyzja stwierdzająca odpowiedni stopień ochrony, standardowe klauzule umowne lub inne wymagane zabezpieczenia.</p>

<h2>8. Okres przechowywania danych</h2>
<p>Dane z formularza i korespondencji przechowujemy przez czas potrzebny do obsługi zapytania, przygotowania oferty, prowadzenia rozmów i realizacji współpracy. Po zakończeniu kontaktu dane mogą być przechowywane przez okres potrzebny do zabezpieczenia ewentualnych roszczeń albo wykonania obowiązków prawnych, podatkowych lub rachunkowych.</p>
<p>Logi serwera przechowujemy przez czas potrzebny do zapewnienia bezpieczeństwa, diagnostyki błędów i prawidłowego działania strony, chyba że dłuższy okres jest konieczny z powodu incydentu, nadużycia albo obowiązku prawnego.</p>

<h2>9. Prawa użytkownika</h2>
<p>Osobie, której dane dotyczą, przysługuje prawo dostępu do danych, otrzymania kopii danych, sprostowania danych, usunięcia danych, ograniczenia przetwarzania, przenoszenia danych, wniesienia sprzeciwu wobec przetwarzania opartego na prawnie uzasadnionym interesie oraz wycofania zgody, jeżeli przetwarzanie odbywało się na podstawie zgody.</p>
<p>Niektóre prawa nie mają charakteru bezwzględnego. Możemy odmówić realizacji żądania w zakresie, w którym dalsze przetwarzanie jest wymagane przez przepisy prawa, niezbędne do ustalenia, dochodzenia lub obrony roszczeń albo oparte na nadrzędnym prawnie uzasadnionym interesie Administratora.</p>
<p>Żądanie można przesłać na adres <a href="mailto:info@kondycjonowanie-wody.pl">info@kondycjonowanie-wody.pl</a>. Dla bezpieczeństwa możemy poprosić o informacje pozwalające potwierdzić tożsamość osoby składającej wniosek.</p>

<h2>10. Prawo skargi</h2>
<p>Jeżeli użytkownik uzna, że dane są przetwarzane niezgodnie z prawem, ma prawo wnieść skargę do Prezesa Urzędu Ochrony Danych Osobowych. Aktualne dane kontaktowe organu nadzorczego są dostępne na stronie <a href="https://uodo.gov.pl/" rel="nofollow noopener">uodo.gov.pl</a>.</p>

<h2>11. Automatyczne decyzje i profilowanie</h2>
<p>Nie podejmujemy wobec użytkowników decyzji opartych wyłącznie na zautomatyzowanym przetwarzaniu, które wywoływałyby skutki prawne lub w podobny sposób istotnie wpływały na użytkownika. Nie prowadzimy też profilowania użytkowników strony w celach marketingowych.</p>

<h2>12. Bezpieczeństwo danych</h2>
<p>Stosujemy środki organizacyjne i techniczne odpowiednie do charakteru danych oraz ryzyka związanego z ich przetwarzaniem. Obejmują one w szczególności ograniczenie dostępu do danych, kontrolę uprawnień, zabezpieczenia usług poczty i hostingu oraz korzystanie z dostawców zapewniających odpowiedni poziom ochrony.</p>
<p>Informacje techniczne dotyczące instalacji, procesów produkcyjnych lub warunków pracy zakładu traktujemy jako informacje przekazane w celu obsługi zapytania. Dostęp do nich mają wyłącznie osoby i podmioty, które potrzebują ich do przygotowania odpowiedzi, oferty, audytu, serwisu lub zabezpieczenia interesów Kabi-Chemie.</p>

<h2>13. Zmiany polityki</h2>
<p>Polityka prywatności może być aktualizowana, jeżeli zmienią się przepisy, zakres działania strony, używane narzędzia, sposób obsługi zapytań lub organizacja pracy Kabi-Chemie. Aktualna wersja dokumentu jest zawsze publikowana na tej stronie.</p>
</div></section>""")],
}

PAGES["/uklady-chlodnicze/"] = {
    "body_class": 'has-dark-hero',
    "jsonld": [{'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': 'Jak często odkamieniać układ chłodniczy?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Przy prawidłowym kondycjonowaniu częstotliwość czyszczeń wyraźnie spada. Harmonogram ustalamy na podstawie jakości wody i obciążenia.'}}, {'@type': 'Question', 'name': 'Czy biocydy są bezpieczne dla środowiska?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Dobieramy preparaty i dawki zgodnie z wymaganiami i przepisami. Kontrolujemy stężenia w obiegu.'}}, {'@type': 'Question', 'name': 'Jak rozpoznać, że układ chłodniczy traci wydajność?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Sygnałem jest wzrost temperatury procesu, częstsze odsalanie, większe zużycie wody, osad na powierzchniach i niestabilne wskazania przewodności.'}}, {'@type': 'Question', 'name': 'Czy program KCAQUA działa w skraplaczach BAC i EVAPCO?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Dobieramy program do typu skraplacza, jakości wody i obciążenia cieplnego. Uwzględniamy ochronę przed kamieniem, biofilmem i korozją.'}}, {'@type': 'Question', 'name': 'Czy pomagacie ograniczyć zużycie wody w obiegu chłodniczym?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Analizujemy przewodność, cykle koncentracji i obecny sposób odsalania. Celem jest stabilna praca układu przy mniejszej ilości wody uzupełniającej i ścieków.'}}]}],
    "sections": [custom("""
<section class="consult-hero" id="top">
  <div class="consult-hero__bg" aria-hidden="true"></div>
  <div class="wrap consult-hero__inner">
    <div class="consult-hero__copy">
      <p class="consult-kicker">Rozwiązania · Skraplacze wyparne</p>
      <h1>Kondycjonowanie wody w przemysłowych <em>układach chłodniczych</em></h1>
      <p class="consult-lead">Chronimy wieże i skraplacze przed kamieniem, korozją i biofilmem. Program KCAQUA 305 stabilizuje pracę układu i ogranicza zużycie wody uzupełniającej.</p>
      <div class="consult-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/case-study/skraplacz-bac-kcaqua/">Case study: skraplacz BAC</a></div>
      <ul class="consult-hero__points" aria-label="Najważniejsze informacje"><li>Mniej wody uzupełniającej</li><li>Kontrola biofilmu i Legionelli</li><li>Stabilna wymiana ciepła</li></ul>
    </div>
    <div class="consult-hero__visual">
      <div class="consult-hero__frame">
        <img src="/assets/blog/blog-cooling-towers.png" alt="Wieże chłodnicze objęte programem KCAQUA 305" loading="eager">
      </div>
    </div>
  </div>
  <div class="consult-proof" aria-label="Najważniejsze informacje"><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v20M4 6l16 12M20 6 4 18"/><path d="M12 5 9.5 7M12 5l2.5 2M12 19l-2.5-2M12 19l2.5-2"/></svg></span><strong>Wieże i skraplacze</strong><span>BAC, EVAPCO i układy amoniakalne.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6M10 3v6l-5 8a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-8V3"/><path d="M7.5 14h9"/></svg></span><strong>3 w 1</strong><span>Biocyd, inhibitor i antyskalant w jednym programie.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><strong>Mniej wody</strong><span>Kontrola przewodności ogranicza odsalanie obiegu.</span></div></div>
</section>
<section class="consult-section consult-section--light">
  <div class="wrap">
    <div class="consult-section-head">
      <p class="consult-kicker">Co zagraża układowi chłodniczemu</p>
      <h2>Kamień i biofilm obniżają wydajność chłodzenia.</h2>
      <p>Każdy z tych problemów podnosi zużycie wody i energii, a w skrajnych przypadkach zatrzymuje produkcję.</p>
    </div>
    <div class="consult-fit-grid"><article class="fitcard"><span class="fitcard__no" aria-hidden="true">01</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><h3>Kamień w obiegu</h3><p>Osad na wymiennikach i wężownicach obniża wymianę ciepła.</p><span class="fitcard__tag">Antyskalant + odkamienianie</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">02</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-8 6-13 14-14 .5 8-4 14-12 14-1 0-2 0-2-3Z"/><path d="M9 15c2-2 4-3 7-4"/></svg></span><h3>Biofilm i mikroorganizmy</h3><p>Pogarszają chłodzenie, sprzyjają korozji i ryzyku Legionelli.</p><span class="fitcard__tag">Biocydy KCAQUA 305</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">03</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v5c0 4 3 7 7 8 4-1 7-4 7-8V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg></span><h3>Korozja</h3><p>Prowadzi do przecieków, awarii i skrócenia życia instalacji.</p><span class="fitcard__tag">Inhibitory korozji</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">04</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h16M7 20V10M12 20V5M17 20v-7"/></svg></span><h3>Nadmierne zużycie wody</h3><p>Zbyt częste odsalanie obiegu podnosi koszty wody i ścieków.</p><span class="fitcard__tag">Kontrola przewodności</span></article></div>
  </div>
</section>
<section class="consult-section kontakt-steps">
  <span class="consult-watermark" aria-hidden="true"></span>
  <div class="wrap">
    <div class="consult-section-head kontakt-steps__head">
      <p class="consult-kicker">Jak działamy</p>
      <h2>Program dobieramy do wody i obciążenia.</h2>
      <p>Wdrożenie prowadzimy w trakcie normalnej pracy układu chłodniczego.</p>
    </div>
    <ol class="kontakt-steps__list kontakt-steps__list--4"><li class="kontakt-step reveal"><span class="kontakt-step__no">1</span><h3>Diagnoza i analiza wody</h3><p>Ocena obiegu, jakości wody i dotychczasowego programu chemicznego.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">2</span><h3>Dobór programu KCAQUA 305</h3><p>Biocyd, inhibitor korozji i antyskalant w jednym preparacie.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">3</span><h3>Dozowanie i limity odsalania</h3><p>Ustawienie pomp dozujących oraz kontroli przewodności.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">4</span><h3>Monitoring efektów</h3><p>Bieżąca kontrola parametrów i raportowanie oszczędności.</p></li></ol>
  </div>
</section>
<section class="consult-section consult-section--value">
  <span class="consult-watermark consult-watermark--light" aria-hidden="true"></span>
  <div class="wrap consult-value">
    <div class="consult-value__intro">
      <p class="consult-kicker">Co zyskuje zakład</p>
      <h2>Stabilny chłód przy niższych kosztach wody i energii.</h2>
      <p class="consult-value__lead">Program KCAQUA 305 łączy ochronę urządzeń z policzalnym efektem operacyjnym.</p>
    </div>
    <div class="consult-value__list"><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></span><div><strong>Mniej wody uzupełniającej</strong><span>Wyższa dopuszczalna przewodność to rzadsze odsalanie obiegu.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v20M4 6l16 12M20 6 4 18"/><path d="M12 5 9.5 7M12 5l2.5 2M12 19l-2.5-2M12 19l2.5-2"/></svg></span><div><strong>Pełna wydajność chłodzenia</strong><span>Czyste powierzchnie wymiany ciepła pracują bez strat.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v5c0 4 3 7 7 8 4-1 7-4 7-8V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg></span><div><strong>Ochrona przed korozją</strong><span>Inhibitory chronią stal i ocynk, także przed białą rdzą.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-8 6-13 14-14 .5 8-4 14-12 14-1 0-2 0-2-3Z"/><path d="M9 15c2-2 4-3 7-4"/></svg></span><div><strong>Bezpieczeństwo biologiczne</strong><span>Kontrola biofilmu ogranicza ryzyko bakterii Legionella.</span></div></article></div>
  </div>
</section><section class="section reveal"><div class="wrap"><div class="section-head"><h2>Nasze rozwiązania dla chłodnictwa</h2></div><div class="card-grid"><a class="card" href="/uklady-chlodnicze/ochrona-wiez-chlodniczych/"><h3>Ochrona wież chłodniczych</h3><p>Biocydy i inhibitory, czyli kontrola biofilmu i korozji.</p><span class="card-link">Dowiedz się więcej →</span></a><a class="card" href="/uklady-chlodnicze/odkamienianie/"><h3>Odkamienianie układów</h3><p>Usuwanie kamienia z wież i skraplaczy w trakcie pracy.</p><span class="card-link">Dowiedz się więcej →</span></a><a class="card" href="/uklady-chlodnicze/skraplacze-amoniakalne/"><h3>Skraplacze amoniakalne</h3><p>Ochrona przed białą korozją i kamieniem.</p><span class="card-link">Dowiedz się więcej →</span></a></div></div></section><section class="section alt reveal"><div class="wrap narrow faq"><div class="section-head"><h2>Najczęstsze pytania</h2></div><details><summary>Jak często odkamieniać układ chłodniczy?</summary><div class="faq-a"><p>Przy prawidłowym kondycjonowaniu częstotliwość czyszczeń wyraźnie spada. Harmonogram ustalamy na podstawie jakości wody i obciążenia.</p></div></details><details><summary>Czy biocydy są bezpieczne dla środowiska?</summary><div class="faq-a"><p>Dobieramy preparaty i dawki zgodnie z wymaganiami i przepisami. Kontrolujemy stężenia w obiegu.</p></div></details><details><summary>Jak rozpoznać, że układ chłodniczy traci wydajność?</summary><div class="faq-a"><p>Sygnałem jest wzrost temperatury procesu, częstsze odsalanie, większe zużycie wody, osad na powierzchniach i niestabilne wskazania przewodności.</p></div></details><details><summary>Czy program KCAQUA działa w skraplaczach BAC i EVAPCO?</summary><div class="faq-a"><p>Tak. Dobieramy program do typu skraplacza, jakości wody i obciążenia cieplnego. Uwzględniamy ochronę przed kamieniem, biofilmem i korozją.</p></div></details><details><summary>Czy pomagacie ograniczyć zużycie wody w obiegu chłodniczym?</summary><div class="faq-a"><p>Tak. Analizujemy przewodność, cykle koncentracji i obecny sposób odsalania. Celem jest stabilna praca układu przy mniejszej ilości wody uzupełniającej i ścieków.</p></div></details></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/uklady-chlodnicze/skraplacze-amoniakalne/">Skraplacze amoniakalne</a></li><li><a href="/baza-wiedzy/wieze-chlodnicze/">Biofilm w układzie chłodniczym</a></li><li><a href="/uslugi/analiza-wody/">Analiza wody chłodniczej</a></li></ul></div></section>
<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Zacznij od diagnozy</p>
        <h2>Policz potencjał oszczędności układu chłodniczego.</h2>
        <p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>
        <a class="consult-final__tel" href="/case-study/skraplacz-bac-kcaqua/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>Zobacz case study skraplacza BAC</span></a>
      </div>
    </div>
  </div>
</section>""")],
}

PAGES["/uklady-chlodnicze/ochrona-wiez-chlodniczych/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/blog/blog-cooling-towers.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Rozwiązania · chłodnictwo</p><h1>Zwalczanie biofilmu i ochrona wież chłodniczych (Biocydy)</h1><p class="lead">Zabezpieczamy wieże chłodnicze przed biofilmem i korozją, sprawdzone biocydy i inhibitory KCAQUA dla ciągłości pracy układu.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/blog/blog-cooling-towers.png" alt="skraplacze, wieże chłodnicze i kontrola obiegu" loading="eager">
      <figcaption>skraplacze, wieże chłodnicze i kontrola obiegu</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap"><div class="section-head"><h2>Co kontrolujemy w wieży</h2></div><div class="feature-grid"><div class="feature"><div class="ficon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-8 6-13 14-14 .5 8-4 14-12 14-1 0-2 0-2-3Z"/><path d="M9 15c2-2 4-3 7-4"/></svg></div><h3>Biofilm i mikroorganizmy</h3><p>Ograniczamy rozwój bakterii i glonów w obiegu.</p></div><div class="feature"><div class="ficon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v5c0 4 3 7 7 8 4-1 7-4 7-8V6l-7-3Z"/><path d="m9 12 2 2 4-4"/></svg></div><h3>Korozja</h3><p>Chronimy metal inhibitorami korozji.</p></div><div class="feature"><div class="ficon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/></svg></div><h3>Kamień</h3><p>Antyskalant zapobiega wytrącaniu twardości.</p></div></div></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/uklady-chlodnicze/odkamienianie/">Odkamienianie układów chłodniczych</a></li><li><a href="/uklady-chlodnicze/skraplacze-amoniakalne/">Skraplacze amoniakalne</a></li><li><a href="/baza-wiedzy/wieze-chlodnicze/">Wieże chłodnicze, baza wiedzy</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/uklady-chlodnicze/odkamienianie/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/impact/impact-03-energy-reduction.jpeg')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Rozwiązania · chłodnictwo</p><h1>Odkamienianie układów chłodniczych i skraplaczy</h1><p class="lead">Bezpiecznie usuwamy kamień z wież i skraplaczy w trakcie eksploatacji, przywracamy pełną wydajność układu chłodniczego.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/impact/impact-03-energy-reduction.jpeg" alt="skraplacze, wieże chłodnicze i kontrola obiegu" loading="eager">
      <figcaption>skraplacze, wieże chłodnicze i kontrola obiegu</figcaption>
    </figure>
  </div>
</section><section class="section alt reveal"><div class="wrap"><div class="section-head"><h2>Jak odkamieniamy układ chłodniczy</h2></div><ol class="steps"><li><div class="step-num">1</div><div><h3>Diagnoza</h3><p>Oceniamy rodzaj i grubość osadu oraz jakość wody.</p></div></li><li><div class="step-num">2</div><div><h3>Czyszczenie chemiczne</h3><p>Rozpuszczamy kamień bez demontażu układu.</p></div></li><li><div class="step-num">3</div><div><h3>Kondycjonowanie</h3><p>Wdrażamy program, by osad nie narastał ponownie.</p></div></li></ol></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/uklady-chlodnicze/ochrona-wiez-chlodniczych/">Ochrona wież chłodniczych</a></li><li><a href="/case-study/skraplacz-evapco-przetworstwo-rybne/">Case study: skraplacz Evapco</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/uklady-chlodnicze/skraplacze-amoniakalne/"] = {
    "sections": [custom("""<section class="hero hero-basic" style="--page-art:url('/assets/case/case-skraplacz.png')">
  <div class="hero-basic__shade" aria-hidden="true"></div>
  <div class="wrap hero-basic__inner">
    <div class="hero-copy hero-basic__copy">
      <p class="eyebrow">Rozwiązania · chłodnictwo</p><h1>Serwis i kondycjonowanie skraplaczy amoniakalnych</h1><p class="lead">Kondycjonujemy wodę w skraplaczach natryskowo-wyparnych, chronimy wężownice przed białą korozją i kamieniem, utrzymując wydajność chłodzenia.</p>
      <div class="cta-row"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost" href="/case-study/warsztaty-amoniakalne-2024/">Warsztaty Amoniakalne 2024</a></div>
      
      <p class="hero-basic__geo">Obsługa zakładów przemysłowych w całej Polsce, z zespołem technicznym w Siedlcach i Toruniu.</p>
    </div>
    <figure class="hero-basic__art">
      <img src="/assets/case/case-skraplacz.png" alt="skraplacze, wieże chłodnicze i kontrola obiegu" loading="eager">
      <figcaption>skraplacze, wieże chłodnicze i kontrola obiegu</figcaption>
    </figure>
  </div>
</section><section class="section reveal"><div class="wrap narrow prose"><h2>Specyfika skraplaczy amoniakalnych</h2><p>Wężownice ocynkowane są narażone na tzw. białą rdzę i osady kamienia, które ograniczają wymianę ciepła. Program KCAQUA 305 chroni powierzchnie i stabilizuje pracę układu.</p></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/uklady-chlodnicze/ochrona-wiez-chlodniczych/">Ochrona wież chłodniczych</a></li><li><a href="/case-study/skraplacz-bac-kcaqua/">Case study: skraplacz BAC</a></li><li><a href="/baza-wiedzy/korozja/">Biała korozja, baza wiedzy</a></li></ul></div></section><section class="cta-band reveal"><div class="wrap cta-inner">
      <div><h2>Sprawdź, ile zaoszczędzi Twój zakład</h2><p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
      <div class="cta-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a></div>
    </div></section>""")],
}

PAGES["/uslugi/"] = {
    "body_class": "has-dark-hero firm-page solution-page services-page",
    "sections": [custom("""
<section class="solution-hero" style="--solution-image:url('/assets/visuals-v2/hero-service-v2.jpg'); --solution-position:center center" id="top">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner solution-hero__inner--editorial">
    <div class="solution-hero__copy reveal-left">
      <p class="firm-kicker">Usługi · diagnostyka i serwis</p>
      <h1>Usługi inżynieryjne: audyt, analiza wody i serwis</h1>
      <p>Trzy usługi inżynieryjne, które porządkują gospodarkę wodną zakładu: audyt techniczny, analiza wody i serwis urządzeń uzdatniania.</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>
        <a class="btn btn-ghost-light" href="/kontakt/">Kontakt</a>
      </div>
    </div>
    <aside class="solution-hero__panel knowledge-hero__panel reveal-right">
      <div><span>Audyt techniczny</span><strong>Wizyta inżyniera i ocena stanu instalacji.</strong></div>
      <div><span>Analiza wody</span><strong>Badanie parametrów wody kotłowej i chłodniczej.</strong></div>
      <div><span>Serwis urządzeń</span><strong>Stacje uzdatniania, pompy dozujące i sondy.</strong></div>
    </aside>
  </div>
</section>
<section class="knowledge-index">
  <div class="wrap">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Nasze usługi</p>
      <h2>Trzy usługi inżynieryjne dla Twojej instalacji.</h2>
    </div>
    <nav class="knowledge-index__rows" aria-label="Nasze usługi">
      <a class="reveal" href="/bezplatna-konsultacja/"><span>01</span><strong>Audyt techniczny</strong><em>Bezpłatna wizyta inżyniera i ocena stanu instalacji.</em></a>
      <a class="reveal" href="/uslugi/analiza-wody/"><span>02</span><strong>Analiza wody</strong><em>Badanie parametrów wody kotłowej i chłodniczej.</em></a>
      <a class="reveal" href="/uslugi/serwis-urzadzen/"><span>03</span><strong>Serwis urządzeń</strong><em>Serwis stacji uzdatniania, pomp dozujących i sond.</em></a>
    </nav>
  </div>
</section>
<section class="section alt reveal">
  <div class="wrap">
    <div class="firm-section-head reveal">
      <p class="firm-kicker">Proces współpracy</p>
      <h2>Od audytu do stałego serwisu.</h2>
    </div>
    <ol class="uslugi-process">
      <li class="reveal"><span class="uslugi-process__no">01</span><h3>Audyt techniczny</h3><p>Inżynier ocenia instalację i mierzy parametry.</p></li>
      <li class="reveal"><span class="uslugi-process__no">02</span><h3>Program chemiczny</h3><p>Dobieramy preparat KCAQUA do układu.</p></li>
      <li class="reveal"><span class="uslugi-process__no">03</span><h3>Monitoring i serwis</h3><p>Regularne wizyty i kontrola parametrów.</p></li>
    </ol>
  </div>
</section>
<nav class="solution-related" aria-label="Powiązane strony"><div class="wrap">
  <p>Powiązane strony</p>
  <div class="solution-related__links">
    <a href="/bezplatna-konsultacja/"><span>Kontakt</span><strong>Bezpłatna konsultacja</strong><i aria-hidden="true">↗</i></a>
    <a href="/branze/"><span>Branże</span><strong>Branże, które obsługujemy</strong><i aria-hidden="true">↗</i></a>
    <a href="/kalkulator-oszczednosci/"><span>Narzędzie</span><strong>Kalkulator oszczędności</strong><i aria-hidden="true">↗</i></a>
  </div>
</div></nav>
<section class="solution-cta"><span class="solution-cta__mark" aria-hidden="true"></span>
  <div class="wrap solution-cta__inner"><div>
    <p class="solution-kicker"><span></span>Następny krok</p>
    <h2>Sprawdź, ile zaoszczędzi Twój zakład.</h2>
    <p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>
    <div class="solution-cta__actions">
      <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>
      <a class="solution-phone-link" href="tel:+48662792875"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/></svg><span>Zadzwoń: +48 662 792 875</span></a>
    </div>
  </div>
</section>""")],
}

PAGES["/uslugi/serwis-urzadzen/"] = {
    "body_class": 'has-dark-hero',
    "jsonld": [{'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': 'Jak szybko reagujecie na awarię?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Awarie pilne staramy się obsłużyć priorytetowo. Serwis planowy realizujemy w uzgodnionym harmonogramie.'}}, {'@type': 'Question', 'name': 'Jakie marki urządzeń serwisujecie?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Obsługujemy popularne urządzenia stosowane w przemyśle. Zakres potwierdzamy po rozpoznaniu.'}}, {'@type': 'Question', 'name': 'Czy serwis obejmuje pompy dozujące chemię?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Sprawdzamy wydajność pomp, szczelność układu, stan przewodów, zawory i poprawność nastaw dozowania preparatów.'}}, {'@type': 'Question', 'name': 'Czy kalibrujecie sondy przewodności i pH?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Kalibracja sond jest częścią serwisu automatyki. Dzięki temu odsalanie, dozowanie i alarmy opierają się na wiarygodnych pomiarach.'}}, {'@type': 'Question', 'name': 'Czy po serwisie otrzymamy protokół?', 'acceptedAnswer': {'@type': 'Answer', 'text': 'Tak. Po wizycie przekazujemy zakres wykonanych prac, zalecenia, wykryte ryzyka i propozycję dalszych działań serwisowych.'}}]}],
    "sections": [custom("""
<section class="consult-hero" id="top">
  <div class="consult-hero__bg" aria-hidden="true"></div>
  <div class="wrap consult-hero__inner">
    <div class="consult-hero__copy">
      <p class="consult-kicker">Rozwiązania · Serwis i automatyka</p>
      <h1>Serwis przemysłowych stacji uzdatniania wody <em>i pomp</em></h1>
      <p class="consult-lead">Serwisujemy urządzenia uzdatniania wody: stacje zmiękczania i RO, pompy dozujące oraz sondy i sterowniki. Jeden partner od chemii, serwisu i automatyki.</p>
      <div class="consult-actions"><a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a><a class="btn btn-ghost-light" href="/bezplatna-konsultacja/">Audyt techniczny instalacji</a></div>
      <ul class="consult-hero__points" aria-label="Najważniejsze informacje"><li>Serwis planowy i awaryjny</li><li>Kalibracja sond i pomp</li><li>Protokół po każdej wizycie</li></ul>
    </div>
    <div class="consult-hero__visual">
      <div class="consult-hero__frame">
        <img src="/assets/impact/impact-04-installation-protection.png" alt="Serwisant przy pompie dozującej stacji uzdatniania wody" loading="eager">
      </div>
    </div>
  </div>
  <div class="consult-proof" aria-label="Najważniejsze informacje"><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M19 12a7 7 0 0 0-.1-1.3l2-1.5-2-3.4-2.3 1a7 7 0 0 0-2.3-1.3L13.8 1h-3.6l-.3 2.2a7 7 0 0 0-2.3 1.3l-2.3-1-2 3.4 2 1.5A7 7 0 0 0 5 12c0 .5 0 .9.1 1.3l-2 1.5 2 3.4 2.3-1a7 7 0 0 0 2.3 1.3l.3 2.2h3.6l.3-2.2a7 7 0 0 0 2.3-1.3l2.3 1 2-3.4-2-1.5c.1-.4.1-.8.1-1.3Z"/></svg></span><strong>Stacje SUW i RO</strong><span>Zmiękczanie i odwrócona osmoza pod opieką.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 4a5 5 0 0 1-6.5 6.5L6 19a2.1 2.1 0 0 1-3-3l8.5-8.5A5 5 0 0 1 18 3l-3 3 3 3 3-3Z"/></svg></span><strong>Pompy dozujące</strong><span>Kalibracja, naprawa i dobór układów dozowania.</span></div><div><span class="consult-proof__ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7Z"/></svg></span><strong>Automatyka</strong><span>Sondy przewodności i sterowniki odsalania.</span></div></div>
</section>
<section class="consult-section consult-section--light">
  <div class="wrap">
    <div class="consult-section-head">
      <p class="consult-kicker">Co serwisujemy</p>
      <h2>Serwis urządzeń odpowiedzialnych za wodę.</h2>
      <p>Prawidłowo skalibrowane urządzenia to warunek działania każdego programu chemicznego.</p>
    </div>
    <div class="consult-fit-grid"><article class="fitcard"><span class="fitcard__no" aria-hidden="true">01</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M19 12a7 7 0 0 0-.1-1.3l2-1.5-2-3.4-2.3 1a7 7 0 0 0-2.3-1.3L13.8 1h-3.6l-.3 2.2a7 7 0 0 0-2.3 1.3l-2.3-1-2 3.4 2 1.5A7 7 0 0 0 5 12c0 .5 0 .9.1 1.3l-2 1.5 2 3.4 2.3-1a7 7 0 0 0 2.3 1.3l.3 2.2h3.6l.3-2.2a7 7 0 0 0 2.3-1.3l2.3 1 2-3.4-2-1.5c.1-.4.1-.8.1-1.3Z"/></svg></span><h3>Stacje SUW i RO</h3><p>Przeglądy i naprawy stacji zmiękczania oraz odwróconej osmozy.</p><span class="fitcard__tag">Uzdatnianie</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">02</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 4a5 5 0 0 1-6.5 6.5L6 19a2.1 2.1 0 0 1-3-3l8.5-8.5A5 5 0 0 1 18 3l-3 3 3 3 3-3Z"/></svg></span><h3>Pompy dozujące</h3><p>Kalibracja i naprawa układów dozowania chemii.</p><span class="fitcard__tag">Dozowanie</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">03</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7Z"/></svg></span><h3>Sondy i sterowniki</h3><p>Sondy przewodności, sterowniki odsalania i pomiary online.</p><span class="fitcard__tag">Automatyka</span></article><article class="fitcard"><span class="fitcard__no" aria-hidden="true">04</span><span class="fitcard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg></span><h3>Dokumentacja</h3><p>Protokół, zalecenia i harmonogram kolejnych przeglądów.</p><span class="fitcard__tag">Po każdej wizycie</span></article></div>
  </div>
</section>
<section class="consult-section kontakt-steps">
  <span class="consult-watermark" aria-hidden="true"></span>
  <div class="wrap">
    <div class="consult-section-head kontakt-steps__head">
      <p class="consult-kicker">Jak przebiega serwis</p>
      <h2>Od zgłoszenia do protokołu z zaleceniami.</h2>
      <p>Awarie pilne obsługujemy priorytetowo, a serwis planowy realizujemy w uzgodnionym harmonogramie.</p>
    </div>
    <ol class="kontakt-steps__list kontakt-steps__list--4"><li class="kontakt-step reveal"><span class="kontakt-step__no">1</span><h3>Zgłoszenie i diagnoza</h3><p>Ustalamy objawy, typ urządzenia i pilność interwencji.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">2</span><h3>Naprawa lub kalibracja</h3><p>Przywracamy sprawność urządzenia i dokładność pomiarów.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">3</span><h3>Testy i uruchomienie</h3><p>Sprawdzamy pracę układu w rzeczywistych warunkach.</p></li><li class="kontakt-step reveal"><span class="kontakt-step__no">4</span><h3>Protokół i zalecenia</h3><p>Dokumentujemy zakres prac i wskazujemy kolejne kroki.</p></li></ol>
  </div>
</section>
<section class="consult-section consult-section--value">
  <span class="consult-watermark consult-watermark--light" aria-hidden="true"></span>
  <div class="wrap consult-value">
    <div class="consult-value__intro">
      <p class="consult-kicker">Dlaczego Kabi-Chemie</p>
      <h2>Jeden zespół od chemii i automatyki.</h2>
      <p class="consult-value__lead">Nie musisz koordynować trzech firm. Za program i urządzenia odpowiada jeden partner.</p>
    </div>
    <div class="consult-value__list"><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg></span><div><strong>Szybka reakcja</strong><span>Priorytet dla awarii, które zagrażają produkcji.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M19 12a7 7 0 0 0-.1-1.3l2-1.5-2-3.4-2.3 1a7 7 0 0 0-2.3-1.3L13.8 1h-3.6l-.3 2.2a7 7 0 0 0-2.3 1.3l-2.3-1-2 3.4 2 1.5A7 7 0 0 0 5 12c0 .5 0 .9.1 1.3l-2 1.5 2 3.4 2.3-1a7 7 0 0 0 2.3 1.3l.3 2.2h3.6l.3-2.2a7 7 0 0 0 2.3-1.3l2.3 1 2-3.4-2-1.5c.1-.4.1-.8.1-1.3Z"/></svg></span><div><strong>Serwis planowy</strong><span>Stały harmonogram przeglądów bez pilnowania terminów.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20h16M7 20V10M12 20V5M17 20v-7"/></svg></span><div><strong>Dokładne pomiary</strong><span>Skalibrowane sondy to wiarygodne dane i dozowanie.</span></div></article><article class="valuecard"><span class="valuecard__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg></span><div><strong>Pełna dokumentacja</strong><span>Protokoły i zalecenia po każdej wizycie serwisowej.</span></div></article></div>
  </div>
</section><section class="section alt reveal"><div class="wrap narrow faq"><div class="section-head"><h2>Najczęstsze pytania</h2></div><details><summary>Jak szybko reagujecie na awarię?</summary><div class="faq-a"><p>Awarie pilne staramy się obsłużyć priorytetowo. Serwis planowy realizujemy w uzgodnionym harmonogramie.</p></div></details><details><summary>Jakie marki urządzeń serwisujecie?</summary><div class="faq-a"><p>Obsługujemy popularne urządzenia stosowane w przemyśle. Zakres potwierdzamy po rozpoznaniu.</p></div></details><details><summary>Czy serwis obejmuje pompy dozujące chemię?</summary><div class="faq-a"><p>Tak. Sprawdzamy wydajność pomp, szczelność układu, stan przewodów, zawory i poprawność nastaw dozowania preparatów.</p></div></details><details><summary>Czy kalibrujecie sondy przewodności i pH?</summary><div class="faq-a"><p>Tak. Kalibracja sond jest częścią serwisu automatyki. Dzięki temu odsalanie, dozowanie i alarmy opierają się na wiarygodnych pomiarach.</p></div></details><details><summary>Czy po serwisie otrzymamy protokół?</summary><div class="faq-a"><p>Tak. Po wizycie przekazujemy zakres wykonanych prac, zalecenia, wykryte ryzyka i propozycję dalszych działań serwisowych.</p></div></details></div></section><section class="section related reveal"><div class="wrap"><h2>Powiązane strony</h2><ul class="related-list"><li><a href="/bezplatna-konsultacja/">Audyt techniczny</a></li><li><a href="/uslugi/analiza-wody/">Analiza wody</a></li></ul></div></section>
<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Potrzebujesz serwisu?</p>
        <h2>Zgłoś urządzenie i umów wizytę serwisową.</h2>
        <p>Opisz objawy w jednym zdaniu, a resztę ustalimy w rozmowie.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>
        <a class="consult-final__tel" href="/kontakt/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>Skontaktuj się z serwisem</span></a>
      </div>
    </div>
  </div>
</section>""")],
}

PAGES["/warunki-wspolpracy/"] = {
    "body_class": 'has-dark-hero firm-page firm-model-page',
    "sections": [custom("""
<section class="firm-hero firm-hero--model" style="--firm-bg:url('/assets/impact/impact-01-water-reduction.jpeg')" id="top">
  <div class="firm-hero__shade" aria-hidden="true"></div>
  <div class="wrap firm-hero__inner firm-hero__inner--wide">
    <div class="firm-hero__copy reveal-left">
      <p class="firm-kicker">Model współpracy</p>
      <h1>Najpierw diagnoza. Potem program chemiczny.</h1>
      <p>Współpraca z Kabi-Chemie jest poukładana tak, aby dział techniczny, produkcja i zarząd widzieli cel, zakres prac, odpowiedzialność oraz sposób mierzenia efektów.</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="/kontakt/">Porozmawiaj z inżynierem</a>
        <a class="btn btn-ghost-light" href="/kalkulator-oszczednosci/">Policz potencjał oszczędności</a>
      </div>
    </div>
    <ol class="firm-route reveal-right" aria-label="Skrócony model współpracy">
      <li><span>1</span><strong>Audyt</strong><em>instalacja, woda, koszty, ryzyka</em></li>
      <li><span>2</span><strong>Rekomendacja</strong><em>program KCAQUA i zakres wdrożenia</em></li>
      <li><span>3</span><strong>Wdrożenie</strong><em>chemia, dozowanie, parametry</em></li>
      <li><span>4</span><strong>Nadzór</strong><em>monitoring, raport, korekty</em></li>
    </ol>
  </div>
</section>

<section class="firm-process" data-scroll-fly>
  <div class="wrap">
    <div class="firm-section-head" data-fly="left">
      <p class="firm-kicker">Etapy współpracy</p>
      <h2>Każdy etap ma jasny cel i decyzję.</h2>
    </div>
    <div class="firm-process__timeline">
      <article data-fly="right"><span>01</span><h3>Rozmowa techniczna</h3><p>Ustalamy typ instalacji, objawy, koszty mediów i to, czy temat wymaga wizyty w zakładzie.</p></article>
      <article data-fly="right" data-fly-delay="0.04"><span>02</span><h3>Audyt i analiza wody</h3><p>Sprawdzamy parametry, sposób dozowania, punkty strat i warunki pracy kotła, skraplacza lub układu RO.</p></article>
      <article data-fly="right" data-fly-delay="0.08"><span>03</span><h3>Plan programu KCAQUA</h3><p>Dobieramy chemię, dawki, monitoring i sposób prowadzenia instalacji. Pokazujemy cel wdrożenia w liczbach.</p></article>
      <article data-fly="right" data-fly-delay="0.12"><span>04</span><h3>Start i stabilizacja</h3><p>Uruchamiamy program, obserwujemy reakcję układu, korygujemy parametry i zabezpieczamy instalację przed błędami eksploatacyjnymi.</p></article>
      <article data-fly="right" data-fly-delay="0.16"><span>05</span><h3>Raport efektów</h3><p>Porównujemy stan przed i po wdrożeniu. Raport może obejmować wodę, energię, ścieki, osady, korozję i przestoje.</p></article>
    </div>
  </div>
</section>

<section class="firm-commitments">
  <div class="wrap firm-commitments__grid">
    <div class="firm-commitments__intro reveal">
      <p class="firm-kicker">Zasady, które porządkują współpracę</p>
      <h2>Nie obiecujemy wyniku bez danych i nie komplikujemy decyzji zakupowej.</h2>
    </div>
    <dl class="firm-commitments__list">
      <div class="reveal"><dt>Zakres</dt><dd>Audyt, rekomendacja, dostawa chemii, dozowanie, monitoring i serwis ustalamy przed startem prac.</dd></div>
      <div class="reveal"><dt>Decyzja</dt><dd>Po rozpoznaniu otrzymujesz jasną informację, czy instalacja ma realny potencjał techniczny i kosztowy.</dd></div>
      <div class="reveal"><dt>Odpowiedzialność</dt><dd>Za program KCAQUA odpowiada zespół Kabi-Chemie, a nie przypadkowy zestaw produktów od kilku dostawców.</dd></div>
      <div class="reveal"><dt>Raportowanie</dt><dd>Efekty omawiamy w danych, które można pokazać utrzymaniu ruchu, produkcji i zarządowi.</dd></div>
    </dl>
  </div>
</section>

<section class="firm-river firm-river--dark" data-scroll-fly>
  <div class="wrap">
    <div class="firm-section-head" data-fly="left">
      <p class="firm-kicker">Co klient dostaje po audycie</p>
      <h2>Konkretny plan zamiast ogólnej prezentacji.</h2>
    </div>
    <ol class="firm-river__list firm-river__list--compact">
      <li data-fly="right"><span>01</span><strong>Ocena potencjału oszczędności</strong><p>Wstępny obraz strat wody, energii, ścieków i kosztów eksploatacyjnych.</p></li>
      <li data-fly="right" data-fly-delay="0.05"><span>02</span><strong>Mapa ryzyk technicznych</strong><p>Najważniejsze problemy: kamień, korozja, biofilm, przewodność, zrzuty i niestabilne dozowanie.</p></li>
      <li data-fly="right" data-fly-delay="0.1"><span>03</span><strong>Rekomendacja programu</strong><p>Proponowany preparat KCAQUA, sposób dozowania, kontrola parametrów i kolejność wdrożenia.</p></li>
      <li data-fly="right" data-fly-delay="0.15"><span>04</span><strong>Decyzja o dalszych krokach</strong><p>Wizyta, badanie wody, wdrożenie, serwis albo uczciwa informacja, że temat nie ma sensu biznesowego.</p></li>
    </ol>
  </div>
</section>

<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Zacznij od diagnozy</p>
        <h2>Wyślij temat instalacji i umów pierwszy kontakt techniczny.</h2>
        <p>Nie musisz mieć pełnej dokumentacji. Wystarczy typ instalacji, objawy i dane kontaktowe do osoby technicznej.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/kontakt/">Przejdź do kontaktu</a>
        <a class="consult-final__tel" href="/bezplatna-konsultacja/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>lub umów bezpłatny audyt</span></a>
      </div>
    </div>
  </div>
</section>
""")],
}

PAGES["/o-firmie/"] = {
    "body_class": 'has-dark-hero firm-page firm-about-page',
    "sections": [custom("""
<section class="firm-hero firm-hero--about" style="--firm-bg:url('/assets/industries/industry-heavy.jpg')" id="top">
  <div class="firm-hero__shade" aria-hidden="true"></div>
  <div class="wrap firm-hero__inner">
    <div class="firm-hero__copy reveal-left">
      <p class="firm-kicker">Misja firmy Kabi-Chemie</p>
      <h1>Producent chemii KCAQUA do kondycjonowania wody przemysłowej.</h1>
      <p>Kabi-Chemie pomaga zakładom przemysłowym ograniczać zużycie wody, energii i chemii przez lepsze prowadzenie kotłów parowych, układów chłodniczych, skraplaczy wyparnych i instalacji RO.</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatny audyt</a>
        <a class="btn btn-ghost-light" href="/warunki-wspolpracy/">Poznaj model współpracy</a>
      </div>
    </div>
    <div class="firm-hero__signals reveal-right" aria-label="Najważniejsze informacje o Kabi-Chemie">
      <div><strong>KCAQUA</strong><span>autorska technologia chemiczna, dozowanie i monitoring</span></div>
      <div><strong>Siedlce i Toruń</strong><span>zespół techniczny obsługujący zakłady w całej Polsce</span></div>
      <div><strong>Wynik w danych</strong><span>raportujemy parametry wody, energii, osadów i kosztów</span></div>
    </div>
  </div>
</section>

<section class="firm-manifest" data-scroll-fly>
  <span class="firm-watermark" aria-hidden="true">KCAQUA</span>
  <div class="wrap firm-manifest__grid">
    <div class="firm-manifest__lead" data-fly="left">
      <p class="firm-kicker">Dlaczego powstała marka</p>
      <h2>Przemysł potrzebuje kontroli nad wodą.</h2>
    </div>
    <div class="firm-manifest__text" data-fly="right">
      <p>Założyliśmy Kabi-Chemie, bo w wielu zakładach woda była traktowana jak koszt stały, a nie jak obszar realnej optymalizacji. W kotłowniach, skraplaczach i obiegach chłodniczych codziennie powstają straty, które da się policzyć i ograniczyć.</p>
      <p>Naszą odpowiedzią jest KCAQUA, czyli program chemiczny prowadzony razem z audytem, analizą parametrów, automatyką dozowania i raportowaniem efektów. Klient widzi nie tylko preparat, ale też powód jego zastosowania i wpływ na instalację.</p>
    </div>
  </div>
</section>

<section class="firm-river firm-river--light" data-scroll-fly>
  <div class="wrap">
    <div class="firm-section-head" data-fly="left">
      <p class="firm-kicker">Jak myślimy o technologii</p>
      <h2>Od diagnozy do wyniku bez zbędnych etapów.</h2>
      <p>Każdy projekt zaczynamy od instalacji klienta, a nie od gotowej listy produktów.</p>
    </div>
    <ol class="firm-river__list">
      <li data-fly="right"><span>01</span><strong>Rozumiemy instalację</strong><p>Sprawdzamy wodę, obciążenie układu, dotychczasową chemię i miejsca strat.</p></li>
      <li data-fly="right" data-fly-delay="0.05"><span>02</span><strong>Dobieramy program KCAQUA</strong><p>Łączymy skład preparatu, dozowanie i cel techniczny pod konkretny układ.</p></li>
      <li data-fly="right" data-fly-delay="0.1"><span>03</span><strong>Stabilizujemy parametry</strong><p>Kontrolujemy przewodność, twardość, pH, osady, korozję i pracę automatyki.</p></li>
      <li data-fly="right" data-fly-delay="0.15"><span>04</span><strong>Pokazujemy efekt</strong><p>Wynik opisujemy w danych zrozumiałych dla technika, produkcji i zarządu.</p></li>
    </ol>
  </div>
</section>

<section class="firm-media-split">
  <div class="firm-media-split__media" aria-hidden="true">
    <video autoplay muted loop playsinline preload="metadata">
      <source src="/assets/mission.mp4" type="video/mp4">
    </video>
  </div>
  <div class="firm-media-split__copy reveal">
    <p class="firm-kicker">Co jest dla nas ważne</p>
    <h2>Uczciwa diagnoza jest lepsza niż szybka sprzedaż.</h2>
    <p>Jeżeli instalacja nie ma realnego potencjału oszczędności, mówimy o tym wprost. Jeżeli problem wymaga dłuższego prowadzenia, pokazujemy, jak będziemy mierzyć postęp.</p>
    <ul class="firm-lines">
      <li><strong>Autorska chemia</strong><span>znamy skład, zastosowanie i granice technologii KCAQUA.</span></li>
      <li><strong>Kontakt z inżynierem</strong><span>rozmawiasz z osobą, która rozumie wodę, kotłownię i chłodnictwo.</span></li>
      <li><strong>Raport zamiast obietnicy</strong><span>opieramy rekomendację na parametrach, kosztach i ryzykach pracy instalacji.</span></li>
    </ul>
  </div>
</section>

<section class="firm-geo" data-scroll-fly>
  <div class="wrap firm-geo__grid">
    <div data-fly="left">
      <p class="firm-kicker">Zasięg i lokalizacja</p>
      <h2>Siedlce i Toruń obsługują zakłady w całej Polsce.</h2>
    </div>
    <div class="firm-geo__map" data-fly="right" aria-label="Lokalizacje Kabi-Chemie">
      <span style="--x:32%;--y:56%"><strong>Siedlce</strong><em>siedziba główna</em></span>
      <span style="--x:50%;--y:37%"><strong>Toruń</strong><em>oddział techniczny</em></span>
      <span style="--x:63%;--y:61%"><strong>Polska</strong><em>zakłady przemysłowe</em></span>
    </div>
  </div>
</section>

<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Następny krok</p>
        <h2>Sprawdź źródła strat w instalacji.</h2>
        <p>Wystarczy krótka rozmowa z inżynierem. Ustalimy typ instalacji i wskażemy najlepszy sposób diagnozy.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację</a>
        <a class="consult-final__tel" href="/referencje/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>Zobacz referencje i realizacje</span></a>
      </div>
    </div>
  </div>
</section>
""")],
}

PAGES["/referencje/"] = {
    "body_class": 'has-dark-hero firm-page firm-references-page',
    "sections": [custom("""
<section class="firm-hero firm-hero--refs" style="--firm-bg:url('/assets/case/case-evapco-fish-generated.png')" id="top">
  <div class="firm-hero__shade" aria-hidden="true"></div>
  <div class="wrap firm-hero__inner">
    <div class="firm-hero__copy reveal-left">
      <p class="firm-kicker">Referencje i realizacje</p>
      <h1>Zaufanie budujemy wynikami i nadzorem.</h1>
      <p>Pracujemy z zakładami, które potrzebują stabilnej wody technologicznej, niższych strat i mniejszego ryzyka awarii. Publicznie pokazujemy wybrane realizacje, a szczegółowe referencje omawiamy po uzyskaniu zgód klientów.</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="/case-study/">Zobacz case studies</a>
        <a class="btn btn-ghost-light" href="/kontakt/">Poproś o kontakt</a>
      </div>
    </div>
    <div class="firm-hero__signals firm-hero__signals--numbers reveal-right" aria-label="Skala doświadczenia">
      <div><strong>160+</strong><span>firm w bazie doświadczeń i rozmów technicznych</span></div>
      <div><strong>3 obszary</strong><span>kotły parowe, chłodnictwo przemysłowe i membrany RO</span></div>
      <div><strong>Polska</strong><span>wdrożenia, audyty i konsultacje dla zakładów w regionach przemysłowych</span></div>
    </div>
  </div>
</section>

<section class="firm-logo-stream" aria-label="Wybrane logotypy i branże">
  <div class="wrap firm-logo-stream__head">
    <p class="firm-kicker">Zaufali nam klienci z przemysłu</p>
    <h2>Logotypy pokazujemy tylko za zgodą klientów.</h2>
  </div>
  <div class="firm-logo-rail" aria-hidden="true">
    <div class="firm-logo-track">
      <img src="/assets/partners/partner-01-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-02-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-03-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-04-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-05-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-06-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-07-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-09-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-10-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-01-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-02-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-03-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-04-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-05-muted.png" alt="" loading="lazy">
      <img src="/assets/partners/partner-06-muted.png" alt="" loading="lazy">
    </div>
  </div>
</section>

<section class="firm-proof-list" data-scroll-fly>
  <div class="wrap">
    <div class="firm-section-head" data-fly="left">
      <p class="firm-kicker">Co potwierdzają wdrożenia</p>
      <h2>Jakość widać w pracy instalacji.</h2>
    </div>
    <div class="firm-proof-list__rows">
      <a href="/case-study/kociol-parowy-fako/" data-fly="right"><span>Kocioł parowy</span><strong>Odkamienianie, kondycjonowanie i mniejsze zużycie paliwa.</strong><em>Zobacz realizację</em></a>
      <a href="/case-study/skraplacz-bac-kcaqua/" data-fly="right" data-fly-delay="0.06"><span>Skraplacz BAC</span><strong>Program KCAQUA 305, stabilna wymiana ciepła i kontrola osadów.</strong><em>Zobacz realizację</em></a>
      <a href="/case-study/skraplacz-evapco-przetworstwo-rybne/" data-fly="right" data-fly-delay="0.12"><span>Przetwórstwo rybne</span><strong>Czyszczenie chemiczne i odzyskanie sprawności chłodzenia.</strong><em>Zobacz realizację</em></a>
    </div>
  </div>
</section>

<section class="firm-industries">
  <div class="wrap firm-industries__grid">
    <div class="firm-industries__copy reveal">
      <p class="firm-kicker">Branże, w których pracujemy</p>
      <h2>Znamy procesy wodne decydujące o kosztach.</h2>
    </div>
    <ul class="firm-industries__list">
      <li class="reveal"><strong>Zakłady mięsne</strong><span>para technologiczna, mycie, chłodzenie i higiena procesu.</span></li>
      <li class="reveal"><strong>Mleczarnie</strong><span>stabilne parametry wody, wymienniki, kotłownie i chłodzenie.</span></li>
      <li class="reveal"><strong>Chłodnie amoniakalne</strong><span>skraplacze wyparne, wieże chłodnicze, kamień i biofilm.</span></li>
      <li class="reveal"><strong>Przemysł ciężki</strong><span>duże obiegi, wysoka temperatura, korozja i koszt przestojów.</span></li>
    </ul>
  </div>
</section>

<section class="consult-final">
  <div class="wrap">
    <div class="consult-final__card">
      <span class="consult-final__mark" aria-hidden="true"></span>
      <div class="consult-final__copy">
        <p class="consult-kicker">Chcesz potwierdzić doświadczenie?</p>
        <h2>Opisz branżę. Dobierzemy podobną realizację.</h2>
        <p>Dobierzemy przykład do kotłowni, układu chłodniczego, skraplacza albo systemu RO.</p>
      </div>
      <div class="consult-final__actions">
        <a class="btn btn-primary" href="/kontakt/">Poproś o kontakt</a>
        <a class="consult-final__tel" href="/case-study/"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h13"/><path d="m13 6 6 6-6 6"/></svg><span>przejdź do case studies</span></a>
      </div>
    </div>
  </div>
</section>
""")],
}

# Najnowszy system sześciu głównych podstron rozwiązań zastępuje starsze definicje.
install_solution_pages(PAGES, custom)
install_company_case_pages(PAGES, custom, SITE)
install_knowledge_pages(PAGES, custom, SHORT)
