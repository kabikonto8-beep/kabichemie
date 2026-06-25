# -*- coding: utf-8 -*-
"""
Treść i konfiguracja serwisu Kabi-Chemie.
Dane SEO (title/meta/h1/breadcrumbs) pochodzą z _seo.json (arkusz „Optymalizacja”).
Tu definiujemy: SITE, NAV, FOOTER, SHORT (etykiety okruszków) oraz PAGES (sekcje).
"""

# ------------------------------------------------------------------ globalne
SITE = {
    "name": "Kabi-Chemie",
    "legal": "Kabi-Chemie",
    "company": "WELDCUT",
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
        {"label": "Audyt techniczny", "href": "/uslugi/audyt-techniczny/"},
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
        {"label": "Układy chłodnicze", "href": "/uklady-chlodnicze/"},
        {"label": "Membrany RO", "href": "/membrany-ro/"},
        {"label": "Odkamienianie instalacji", "href": "/odkamienianie-instalacji/"},
        {"label": "Ochrona antykorozyjna", "href": "/ochrona-antykorozyjna/"},
    ]},
    {"title": "Usługi", "links": [
        {"label": "Audyt techniczny", "href": "/uslugi/audyt-techniczny/"},
        {"label": "Analiza wody", "href": "/uslugi/analiza-wody/"},
        {"label": "Serwis urządzeń", "href": "/uslugi/serwis-urzadzen/"},
        {"label": "Bezpłatna konsultacja", "href": "/bezplatna-konsultacja/"},
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
    {"label": "Rozwiązania", "href": "/uslugi/", "promo": ("Dobierzemy program chemiczny pod Twoją instalację.", "Umów bezpłatny audyt", "/bezplatna-konsultacja/"), "children": [
        {"label": "Kotły parowe", "href": "/kotly-parowe/"},
        {"label": "Skraplacze wyparne", "href": "/uklady-chlodnicze/"},
        {"label": "Technologia KCAQUA", "href": "/kotly-parowe/kondycjonowanie-wody-kotlowej/"},
        {"label": "Białe certyfikaty", "href": "/bezplatna-konsultacja/"},
        {"label": "Ochrona membran RO", "href": "/membrany-ro/"},
        {"label": "Serwis i automatyka", "href": "/uslugi/serwis-urzadzen/"},
    ]},
    {"label": "Case studies", "href": "/case-study/", "promo": ("Realne wdrożenia z liczbami gotowymi dla zarządu.", "Zobacz wszystkie realizacje", "/case-study/"), "children": [
        {"label": "Fako: −32% paliwa", "href": "/case-study/kociol-parowy-fako/"},
        {"label": "BAC: KCAQUA 305", "href": "/case-study/skraplacz-bac-kcaqua/"},
        {"label": "Evapco — przetwórstwo rybne", "href": "/case-study/skraplacz-evapco-przetworstwo-rybne/"},
    ]},
    {"label": "Branże", "href": "/branze/"},
    {"label": "Baza wiedzy", "href": "/baza-wiedzy/", "promo": ("Praktyczna wiedza o kondycjonowaniu wody w przemyśle.", "Przejdź do bazy wiedzy", "/baza-wiedzy/"), "children": [
        {"label": "Centrum Wiedzy", "href": "/baza-wiedzy/"},
        {"label": "Kotły parowe", "href": "/baza-wiedzy/kotly-parowe/"},
        {"label": "Skraplacze i chłodnictwo", "href": "/baza-wiedzy/wieze-chlodnicze/"},
        {"label": "Oszczędność wody i parametry", "href": "/baza-wiedzy/parametry-wody/"},
        {"label": "Membrany RO", "href": "/baza-wiedzy/membrany-ro/"},
        {"label": "Korozja i chemia", "href": "/baza-wiedzy/korozja/"},
    ]},
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
    "/referencje/": "Referencje",
    "/case-study/": "Case studies",
    "/case-study/kociol-parowy-fako/": "Kocioł parowy Fako",
    "/case-study/skraplacz-bac-kcaqua/": "Skraplacz BAC",
    "/case-study/skraplacz-evapco-przetworstwo-rybne/": "Skraplacz Evapco",
    "/case-study/warsztaty-amoniakalne-2024/": "Warsztaty Amoniakalne 2024",
    "/faq/": "FAQ",
    "/kotly-parowe/": "Kotły parowe",
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
        video="/assets/kabi-hero-latest.mp4",
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
            ("Skontaktuj się z inżynierem", "/kontakt/"),
        ],
        scroll_cue="Zobacz więcej",
        scroll_href="#nasze-branze",
    ),
    custom("""
<section class="section branze-svc section-brand-panel" id="nasze-branze" aria-labelledby="branze-svc-title" data-branze-svc>
  <div class="branze-svc__bg" aria-hidden="true"></div>
  <span class="branze-watermark section-bg-word" aria-hidden="true">KABI CHEMIE</span>
  <img class="branze-logo-bg section-bg-logo" src="/assets/logo-mark.png" alt="" aria-hidden="true">
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
        <a class="branze-pane__cta" href="/branze/#zaklady-miesne/">Zobacz branżę <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></a>
      </div>
      <div class="branze-pane" data-branze-pane="1" style="--pane-img:url('/assets/industries/industry-dairy.jpg')">
        <div class="branze-card"><span class="branze-card__num">01</span><h3>Wymienniki i pasteryzacja</h3><p>Ochrona powierzchni wymiany ciepła przed kamieniem i osadami.</p></div>
        <div class="branze-card"><span class="branze-card__num">02</span><h3>Stacje CIP</h3><p>Stabilna woda technologiczna do mycia — powtarzalna higiena procesu.</p></div>
        <div class="branze-card"><span class="branze-card__num">03</span><h3>Kotły parowe</h3><p>Niższe zużycie paliwa i pary dzięki czystym instalacjom.</p></div>
        <a class="branze-pane__cta" href="/branze/#mleczarnie/">Zobacz branżę <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></a>
      </div>
      <div class="branze-pane" data-branze-pane="2" style="--pane-img:url('/assets/industries/industry-cold-storage.jpg')">
        <div class="branze-card"><span class="branze-card__num">01</span><h3>Skraplacze wyparne</h3><p>Kontrola osadów i biofilmu w układach BAC i EVAPCO (program KCAQUA 305).</p></div>
        <div class="branze-card"><span class="branze-card__num">02</span><h3>Wieże chłodnicze</h3><p>Inhibitory korozji i antyskalanty — stabilna wymiana ciepła.</p></div>
        <div class="branze-card"><span class="branze-card__num">03</span><h3>Obiegi amoniakalne</h3><p>Mniej korozji i osadów w wymagających instalacjach chłodniczych.</p></div>
        <a class="branze-pane__cta" href="/branze/#chlodnie/">Zobacz branżę <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></a>
      </div>
      <div class="branze-pane" data-branze-pane="3" style="--pane-img:url('/assets/industries/industry-heavy.jpg')">
        <div class="branze-card"><span class="branze-card__num">01</span><h3>Wysokie obciążenia cieplne</h3><p>Programy dla instalacji pracujących w trudnych, ekstremalnych warunkach.</p></div>
        <div class="branze-card"><span class="branze-card__num">02</span><h3>Korozja i kamień</h3><p>Ograniczenie ubytków, osadów i kosztownych awarii.</p></div>
        <div class="branze-card"><span class="branze-card__num">03</span><h3>Redukcja przestojów</h3><p>Dłuższe cykle między czyszczeniami i większa dyspozycyjność.</p></div>
        <a class="branze-pane__cta" href="/branze/#przemysl-ciezki/">Zobacz branżę <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></a>
      </div>
      <div class="branze-pane" data-branze-pane="4" style="--pane-img:url('/assets/industries/industry-food-producers.jpg')">
        <div class="branze-card"><span class="branze-card__num">01</span><h3>Para i chłód</h3><p>Niezawodne media procesowe przy stabilnych parametrach pracy.</p></div>
        <div class="branze-card"><span class="branze-card__num">02</span><h3>Woda technologiczna</h3><p>Powtarzalna jakość wody i higiena całego procesu produkcji.</p></div>
        <div class="branze-card"><span class="branze-card__num">03</span><h3>Oszczędności</h3><p>Mniej wody, energii i ścieków — niższe koszty operacyjne.</p></div>
        <a class="branze-pane__cta" href="/branze/#producenci-zywnosci/">Zobacz branżę <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></a>
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
  <div class="partner-scale-group" data-partner-scale aria-label="Ponad sto sześćdziesiąt cztery firmy w bazie doświadczeń">
    <div class="partner-scale-copy">
      <span>Dołącz do firm, które oszczędzają pieniądze</span>
      <svg class="partner-growth-arrow" viewBox="0 0 520 84" aria-hidden="true" focusable="false">
        <path class="partner-growth-line" d="M14 30 C150 82 340 80 478 33" />
        <path class="partner-growth-head" d="M498 26 L476 44 L472 22 Z" />
      </svg>
    </div>
    <div class="partner-scale-badge">
    <strong class="partner-scale-number" data-count-to="164" data-suffix="+">0+</strong>
    <span>firm w bazie doświadczeń</span>
    <em>pokazujemy tylko część z nich</em>
    </div>
  </div>
  <div class="partner-rails">
    <div class="partner-rail" data-logo-rail data-direction="-1" data-repeats="3">
      <div class="partner-track">
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-01-muted.png" alt="Sokołów"><img class="logo-color" src="/assets/partners/partner-01-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-02-muted.png" alt="Nestlé"><img class="logo-color" src="/assets/partners/partner-02-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-03-muted.png" alt="Tarczyński"><img class="logo-color" src="/assets/partners/partner-03-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-04-muted.png" alt="Bakalland"><img class="logo-color" src="/assets/partners/partner-04-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-05-muted.png" alt="Dolina Noteci"><img class="logo-color" src="/assets/partners/partner-05-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-06-muted.png" alt="Wipasz"><img class="logo-color" src="/assets/partners/partner-06-color.png" alt="" aria-hidden="true"></span>
      </div>
    </div>
    <div class="partner-rail" data-logo-rail data-direction="1" data-repeats="3">
      <div class="partner-track">
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-07-muted.png" alt="Seko"><img class="logo-color" src="/assets/partners/partner-07-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-08-muted.png" alt="Głuchowski"><img class="logo-color" src="/assets/partners/partner-08-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-09-muted.png" alt="Rauch"><img class="logo-color" src="/assets/partners/partner-09-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-10-muted.png" alt="OSM Garwolin"><img class="logo-color" src="/assets/partners/partner-10-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-11-muted.png" alt="Krynicavitamin"><img class="logo-color" src="/assets/partners/partner-11-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-12-muted.png" alt="Komar Group"><img class="logo-color" src="/assets/partners/partner-12-color.png" alt="" aria-hidden="true"></span>
      </div>
    </div>
    <div class="partner-rail" data-logo-rail data-direction="-1" data-repeats="3">
      <div class="partner-track partner-track-compact">
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-13-muted.png" alt="Wierzejki"><img class="logo-color" src="/assets/partners/partner-13-color.png" alt="" aria-hidden="true"></span>
        <span class="partner-logo"><img class="logo-muted" src="/assets/partners/partner-14-muted.png" alt="OSM Kosów"><img class="logo-color" src="/assets/partners/partner-14-color.png" alt="" aria-hidden="true"></span>
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
      <p class="scrub-l">Porządkujemy gospodarkę wodną tam, gdzie codziennie uciekają pieniądze: w poborze świeżej wody, zrzutach ścieków, energii i awaryjności instalacji.</p>
      <a class="btn btn-primary btn-arrow impact-copy__cta scrub-l" href="/bezplatna-konsultacja/">Umów darmowy audyt</a>
    </div>
    <div class="impact-grid impact-accordion scrub-r" data-impact-accordion aria-label="Animowane obszary wpływu Kabi-Chemie">
      <article class="impact-card impact-card--active" role="button" tabindex="0" aria-expanded="true" data-impact-item style="--card-img:url('/assets/impact/impact-01-water-reduction.jpeg');--card-pos:center center;--card-a:#062030;--card-b:#0f6f93;--card-accent:#7fd4ef">
        <span class="impact-card__number">01</span>
        <div class="impact-card__visual" aria-hidden="true"></div>
        <div class="impact-card__content">
          <p class="impact-card__kicker">Woda procesowa</p>
          <h3>Ograniczamy pobór wody</h3>
          <p>Wyższa stabilność parametrów pozwala zmniejszyć ilość świeżej wody potrzebnej do pracy instalacji.</p>
        </div>
      </article>
      <article class="impact-card" role="button" tabindex="0" aria-expanded="false" data-impact-item style="--card-img:url('/assets/impact/impact-02-effluent-control.jpeg');--card-pos:center center;--card-a:#061d1a;--card-b:#1f9d57;--card-accent:#8ce8bd">
        <span class="impact-card__number">02</span>
        <div class="impact-card__visual" aria-hidden="true"></div>
        <div class="impact-card__content">
          <p class="impact-card__kicker">Zrzuty i opłaty</p>
          <h3>Ograniczamy zrzuty ścieków</h3>
          <p>Mniej odsalania i wymian wody to mniej ścieków technologicznych oraz niższe opłaty operacyjne.</p>
        </div>
      </article>
      <article class="impact-card" role="button" tabindex="0" aria-expanded="false" data-impact-item style="--card-img:url('/assets/impact/impact-03-energy-reduction.jpeg');--card-pos:center center;--card-a:#061a2a;--card-b:#1789b6;--card-accent:#8ee3ff">
        <span class="impact-card__number">03</span>
        <div class="impact-card__visual" aria-hidden="true"></div>
        <div class="impact-card__content">
          <p class="impact-card__kicker">Energia i wymiana ciepła</p>
          <h3>Zmniejszamy zużycie energii</h3>
          <p>Czystsze powierzchnie wymiany ciepła zmniejszają straty paliwa, pary i chłodu.</p>
        </div>
      </article>
      <article class="impact-card" role="button" tabindex="0" aria-expanded="false" data-impact-item style="--card-img:url('/assets/impact/impact-04-installation-protection.png');--card-pos:center center;--card-a:#061421;--card-b:#0b3d5c;--card-accent:#b8eaff">
        <span class="impact-card__number">04</span>
        <div class="impact-card__visual" aria-hidden="true"></div>
        <div class="impact-card__content">
          <p class="impact-card__kicker">Ochrona instalacji</p>
          <h3>Chronimy instalacje</h3>
          <p>Kontrolujemy kamień, korozję, biofilm i osady, które skracają żywotność urządzeń.</p>
        </div>
      </article>
      <article class="impact-card" role="button" tabindex="0" aria-expanded="false" data-impact-item style="--card-img:url('/assets/impact/impact-05-operational-costs.png');--card-pos:center center;--card-a:#071824;--card-b:#0a789b;--card-accent:#7fd4ef">
        <span class="impact-card__number">05</span>
        <div class="impact-card__visual" aria-hidden="true"></div>
        <div class="impact-card__content">
          <p class="impact-card__kicker">Koszty operacyjne</p>
          <h3>Obniżamy koszty operacyjne</h3>
          <p>Łączymy chemię, audyt i monitoring, żeby oszczędność była policzalna dla zarządu i utrzymania ruchu.</p>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section process-loss-section section-brand-panel" id="proces-kcaqua" data-scroll-fly>
  <div class="process-loss-bg" aria-hidden="true"></div>
  <span class="section-bg-word" aria-hidden="true">PROCES</span>
  <img class="section-bg-logo" src="/assets/logo-mark.png" alt="" aria-hidden="true">
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
          <img src="/assets/logo-mark.png" alt="Kabi-Chemie" width="86" height="84" loading="lazy">
          <strong>Kabi-Chemie</strong>
          <small>Proces od audytu do oszczędności</small>
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
  <img class="section-bg-logo section-bg-logo--dark" src="/assets/logo-mark.png" alt="" aria-hidden="true">
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
  <img class="section-bg-logo section-bg-logo--dark" src="/assets/logo-mark.png" alt="" aria-hidden="true">
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

    <a class="impact-curve__cta" href="/bezplatna-konsultacja/" aria-label="Zacznij oszczędzać — umów bezpłatny audyt">
      <span>Zacznij<br>oszczędzać</span>
    </a>

    <div class="impact-stat" style="left:19.2%;top:64%">
      <span class="impact-stat__num"><b class="num-counter" data-count-to="6000000">0</b></span>
      <span class="impact-stat__label">litrów wody zaoszczędzonych u jednego klienta w 6 miesięcy</span>
    </div>
    <div class="impact-stat" style="left:43.3%;top:49%">
      <span class="impact-stat__num"><b class="num-counter" data-count-to="50">0</b><i class="impact-stat__unit">%</i></span>
      <span class="impact-stat__label">mniej zużycia energii w wybranych instalacjach</span>
    </div>
    <div class="impact-stat" style="left:68.3%;top:31%">
      <span class="impact-stat__num"><b>dziesiątki</b></span>
      <span class="impact-stat__label">zakładów objętych programami Kabi-Chemie</span>
    </div>
    <div class="impact-stat" style="left:90%;top:20%">
      <span class="impact-stat__num"><b>milionowe</b></span>
      <span class="impact-stat__label">oszczędności kosztów operacyjnych</span>
    </div>

    <span class="impact-node" style="left:19.17%;top:73.08%"></span>
    <span class="impact-node" style="left:43.33%;top:57.69%"></span>
    <span class="impact-node" style="left:68.33%;top:40.38%"></span>
    <span class="impact-node" style="left:90%;top:28.85%"></span>
    <span class="impact-curve__spark" aria-hidden="true"></span>
  </div>

  <div class="wrap">
    <ul class="impact-stack" aria-hidden="false">
      <li><span class="impact-stat__num"><b>6 000 000</b></span><span class="impact-stat__label">litrów wody zaoszczędzonych u jednego klienta w 6 miesięcy</span></li>
      <li><span class="impact-stat__num"><b>50</b><i class="impact-stat__unit">%</i></span><span class="impact-stat__label">mniej zużycia energii w wybranych instalacjach</span></li>
      <li><span class="impact-stat__num"><b>dziesiątki</b></span><span class="impact-stat__label">zakładów objętych programami Kabi-Chemie</span></li>
      <li><span class="impact-stat__num"><b>milionowe</b></span><span class="impact-stat__label">oszczędności kosztów operacyjnych</span></li>
    </ul>
  </div>
</section>

<section class="section alt cert-section" data-scrub>
  <div class="wrap certificate-grid">
    <div class="scrub-l">
      <p class="eyebrow">Dodatkowe źródło oszczędności</p>
      <h2>Oszczędzasz energię. Możesz otrzymać dodatkowe środki.</h2>
      <p>Białe certyfikaty to forma wsparcia dla przedsiębiorstw wdrażających rozwiązania ograniczające zużycie energii. W niektórych przypadkach ich wartość może pokryć znaczną część kosztów programu chemicznego.</p>
      <p class="note">W jednym z projektów wartość uzyskanych białych certyfikatów odpowiadała około półrocznemu kosztowi programu chemicznego.</p>
      <a class="btn btn-primary btn-arrow" href="/bezplatna-konsultacja/">Sprawdź kwalifikację instalacji</a>
    </div>
    <div class="cert-card scrub-r">
      <span>Program obejmuje</span>
      <ul class="check-list">
        <li>Darmowy audyt techniczny</li>
        <li>Wdrożenie technologii</li>
        <li>Monitoring efektów</li>
        <li>Oszczędność wody i energii</li>
        <li>Wsparcie w zakresie białych certyfikatów</li>
      </ul>
    </div>
  </div>
</section>

<section class="section gallery-section" data-scroll-fly>
  <span class="section-bg-word section-bg-word--dark" aria-hidden="true">REALIZACJE</span>
  <img class="section-bg-logo section-bg-logo--dark" src="/assets/logo-mark.png" alt="" aria-hidden="true">
  <div class="wrap">
    <div class="gallery-head">
      <div class="gallery-head__copy" data-fly="left">
        <p class="eyebrow">Realizacje</p>
        <h2>Mierzalne oszczędności, nie obietnice</h2>
        <p>Wybrane wdrożenia w zakładach przemysłowych: realny problem, zastosowany program KCAQUA i efekt w kosztach pary, wody oraz energii — gotowy do przedstawienia zarządowi.</p>
      </div>
      <div class="gallery-nav" data-fly="right" data-fly-delay="0.06" data-fly-sync=".gallery-track" data-fly-distance="0.32">
        <button type="button" class="gallery-arrow" data-gallery-prev aria-label="Poprzedni">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5"/><path d="m12 19-7-7 7-7"/></svg>
        </button>
        <button type="button" class="gallery-arrow" data-gallery-next aria-label="Następny">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
        </button>
      </div>
    </div>
  </div>

  <div class="gallery-viewport" data-gallery>
    <div class="gallery-track" data-gallery-track>
      <a class="gallery-card" data-fly="right" data-fly-delay="0.06" href="/case-study/kociol-parowy-fako/" style="--img:url('/assets/case/case-fako-boiler-generated.png')">
        <span class="gallery-card__media" aria-hidden="true"></span>
        <span class="gallery-card__shade" aria-hidden="true"></span>
        <span class="gallery-card__body">
          <span class="gallery-card__kicker">Kocioł parowy 8 t/h</span>
          <span class="gallery-card__title">Fako: −32% paliwa</span>
          <span class="gallery-card__desc">Częste odsalanie, straty energii i wdrożenie programu KCAQUA 303.</span>
          <span class="gallery-card__more">Zobacz case study <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg></span>
        </span>
      </a>
      <a class="gallery-card" data-fly="right" data-fly-delay="0.12" href="/case-study/skraplacz-bac-kcaqua/" style="--img:url('/assets/case/case-bac-kcaqua-generated.png')">
        <span class="gallery-card__media" aria-hidden="true"></span>
        <span class="gallery-card__shade" aria-hidden="true"></span>
        <span class="gallery-card__body">
          <span class="gallery-card__kicker">Skraplacz wyparny</span>
          <span class="gallery-card__title">BAC: KCAQUA 305</span>
          <span class="gallery-card__desc">Optymalizacja pracy skraplacza i stabilna kontrola osadów.</span>
          <span class="gallery-card__more">Zobacz case study <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg></span>
        </span>
      </a>
      <a class="gallery-card" data-fly="right" data-fly-delay="0.18" href="/case-study/skraplacz-evapco-przetworstwo-rybne/" style="--img:url('/assets/case/case-evapco-fish-generated.png')">
        <span class="gallery-card__media" aria-hidden="true"></span>
        <span class="gallery-card__shade" aria-hidden="true"></span>
        <span class="gallery-card__body">
          <span class="gallery-card__kicker">Przetwórstwo rybne</span>
          <span class="gallery-card__title">Evapco: odzysk wydajności</span>
          <span class="gallery-card__desc">Czyszczenie chemiczne i poprawa wydajności chłodzenia.</span>
          <span class="gallery-card__more">Zobacz case study <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg></span>
        </span>
      </a>
    </div>
  </div>

  <div class="wrap">
    <div class="gallery-dots" data-gallery-dots data-fly="right" data-fly-delay="0.06" data-fly-sync=".gallery-track" data-fly-distance="0.32" aria-label="Nawigacja case studies"></div>
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

<section class="section knowledge-section" data-scroll-fly>
  <span class="section-bg-word section-bg-word--dark" aria-hidden="true">WIEDZA</span>
  <img class="section-bg-logo section-bg-logo--dark" src="/assets/logo-mark.png" alt="" aria-hidden="true">
  <div class="wrap">
    <div class="section-head" data-fly="left">
      <p class="eyebrow">Centrum Wiedzy</p>
      <h2>Baza wiedzy: ekspercki blog o kondycjonowaniu wody</h2>
      <p>Praktyczna wiedza dla osób odpowiedzialnych za kotłownie parowe, instalacje chłodnicze i gospodarkę wodną w zakładach przemysłowych.</p>
    </div>
    <div class="knowledge-layout">
      <a class="featured-post" data-fly="left" href="/baza-wiedzy/pojedynczy-wpis-blogowy-1/" style="--post-img:url('/assets/blog/blog-water-reduction.png')">
        <span class="post-cat">Wyróżniony wpis</span>
        <h3>Jak ograniczyć zużycie wody w kotłowni bez kosztownej modernizacji?</h3>
        <p>Wyjaśniamy, skąd biorą się straty wody, dlaczego odsalanie zwiększa koszty energii i jak technologia KCAQUA pomaga odzyskać kontrolę nad parametrami instalacji.</p>
        <span class="post-meta">Kategoria: Kotły parowe · Autor: Kabi-Chemie · 2026</span>
      </a>
      <div class="knowledge-cats">
        <a class="knowledge-cat" data-fly="right" data-fly-delay="0.05" href="/baza-wiedzy/kotly-parowe/" style="--cat-img:url('/assets/blog/blog-boiler-scale.png')"><strong>Kotły parowe</strong><span>Odsalanie, przewodność, kamień kotłowy i straty energii.</span></a>
        <a class="knowledge-cat" data-fly="right" data-fly-delay="0.11" href="/baza-wiedzy/wieze-chlodnicze/" style="--cat-img:url('/assets/blog/blog-cooling-towers.png')"><strong>Skraplacze wyparne</strong><span>BAC, EVAPCO, koncentracja obiegów, osady i biofilm.</span></a>
        <a class="knowledge-cat" data-fly="right" data-fly-delay="0.05" href="/baza-wiedzy/parametry-wody/" style="--cat-img:url('/assets/blog/blog-water-reduction.png')"><strong>Oszczędność wody</strong><span>Koszt m3 wody, ścieki, odzysk i gospodarka wodna zakładu.</span></a>
        <a class="knowledge-cat" data-fly="right" data-fly-delay="0.11" href="/baza-wiedzy/korozja/" style="--cat-img:url('/assets/blog/blog-corrosion-pipes.png')"><strong>Chemia i korozja</strong><span>Polimery, inhibitory, antyskalanty i błędy w programach chemicznych.</span></a>
      </div>
    </div>
    <div class="blog-strip">
      <a data-fly="left" data-fly-delay="0.04" href="/baza-wiedzy/pojedynczy-wpis-blogowy-2/" style="--post-img:url('/assets/blog/blog-biofilm-cleaning.png')">Biofilm w układzie chłodniczym — jak go kontrolować?</a>
      <a data-fly="right" data-fly-delay="0.08" href="/baza-wiedzy/pojedynczy-wpis-blogowy-3/" style="--post-img:url('/assets/blog/blog-ro-antiscalant.png')">Antyskalant do membran RO — kiedy naprawdę działa?</a>
      <a data-fly="right" data-fly-delay="0.14" href="/baza-wiedzy/korozja/" style="--post-img:url('/assets/blog/blog-cooling-towers.png')">Białe certyfikaty i oszczędność energii — od czego zacząć?</a>
    </div>
    <div class="knowledge-cta">
      <p data-fly="left">Masz pytanie techniczne? Zgłoś się po bezpłatną konsultację inżyniera.</p>
      <a class="btn btn-primary btn-arrow" data-fly="left" data-fly-delay="0.06" href="/bezplatna-konsultacja/">Umów konsultację</a>
      <a class="btn btn-ghost btn-arrow" data-fly="right" data-fly-delay="0.1" href="/baza-wiedzy/">Przejdź do bazy wiedzy</a>
    </div>
  </div>
</section>

<section class="section home-faq-section section-brand-panel" id="faq" data-faq-scroll>
  <span class="section-bg-word" aria-hidden="true">PYTANIA</span>
  <img class="section-bg-logo" src="/assets/logo-mark.png" alt="" aria-hidden="true">
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
  <img class="section-bg-logo" src="/assets/logo-mark.png" alt="" aria-hidden="true">
  <div class="wrap audit-form-grid">
    <div class="audit-benefits">
      <h2>Jesteśmy po to, aby Ci pomóc.</h2>
      <p>Każda instalacja ma swoją specyfikę. Opowiedz nam krótko, z czym się mierzysz, a nasz inżynier pomoże znaleźć właściwe rozwiązanie.</p>
      <div class="audit-flow" aria-label="Jak możemy Ci pomóc">
        <div><span>01</span><strong>Opowiedz nam o sytuacji</strong><p>Napisz tyle, ile wiesz. Nie musisz znać technicznych szczegółów.</p></div>
        <div><span>02</span><strong>Porozmawiaj z inżynierem</strong><p>Skontaktujemy się w ciągu 24 godzin, odpowiemy na pytania i wspólnie ustalimy kolejny krok.</p></div>
        <div class="audit-flow__phone"><span aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.5 15.5 0 0 0 6.6 6.6l2.2-2.2a1.5 1.5 0 0 1 1.6-.34c1.05.35 2.18.54 3.35.54A1.65 1.65 0 0 1 22 17.05v3.3A1.65 1.65 0 0 1 20.35 22C10.22 22 2 13.78 2 3.65A1.65 1.65 0 0 1 3.65 2h3.3A1.65 1.65 0 0 1 8.6 3.65c0 1.18.19 2.3.54 3.36a1.5 1.5 0 0 1-.34 1.59Z"/></svg></span><strong>Wolisz porozmawiać?</strong><p><a href="tel:+48662792875">+48 662 792 875</a></p></div>
      </div>
    </div>
    <form class="contact-form audit-form-card" data-email="info@kondycjonowanie-wody.pl" novalidate>
      <div class="audit-form-card__head">
        <strong>Powiedz nam, jak możemy pomóc</strong>
      </div>
      <div class="row2">
        <div class="field"><label for="audit-name">Imię i nazwisko</label><input id="audit-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="audit-phone">Telefon</label><input id="audit-phone" name="phone" type="tel" autocomplete="tel" placeholder="np. 600 000 000" required></div>
      </div>
      <div class="row2">
        <div class="field"><label for="audit-company">Firma / zakład <span>(opcjonalnie)</span></label><input id="audit-company" name="company" autocomplete="organization"></div>
        <div class="field"><label for="audit-email">E-mail <span>(opcjonalnie)</span></label><input id="audit-email" name="email" type="email" autocomplete="email"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="audit-installation">Typ instalacji</label>
          <select id="audit-installation" name="installation">
            <option>Kocioł parowy</option>
            <option>Skraplacz wyparny / układ chłodniczy</option>
            <option>Wieża chłodnicza</option>
            <option>Membrany RO</option>
            <option>Stacja uzdatniania / serwis</option>
            <option>Nie wiem — potrzebuję diagnozy</option>
          </select></div>
        <div class="field"><label for="audit-goal">Najważniejszy cel</label>
          <select id="audit-goal" name="goal">
            <option>Ograniczenie zużycia wody</option>
            <option>Oszczędność energii</option>
            <option>Kamień, osady lub korozja</option>
            <option>Białe certyfikaty</option>
            <option>Awaria / niestabilne parametry</option>
          </select></div>
      </div>
      <div class="field"><label for="audit-message">Jak możemy Ci pomóc? <span>(opcjonalnie)</span></label><textarea id="audit-message" name="message" rows="3" placeholder="Opisz krótko sytuację lub pytanie, z którym się do nas zwracasz"></textarea></div>
      <label class="form-consent"><input type="checkbox" required> Zgadzam się na kontakt w sprawie mojego zapytania.</label>
      <button type="submit" class="btn btn-primary">Poproś o kontakt <span aria-hidden="true">→</span></button>
      <p class="form-note" hidden></p>
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
PAGES["/bezplatna-konsultacja/"] = {"sections": [
    hero(lead="<strong>Inżynier oddzwoni w 24 h i ustali termin wizyty w Twoim zakładzie.</strong> Konsultacja jest bezpłatna i bez zobowiązań — chcemy najpierw zrozumieć Twoją instalację.",
         ctas=[("Wypełnij formularz", "#main"), ("Zadzwoń teraz", "/kontakt/")]),
    steps("Jak wygląda konsultacja", [
        ("Kontakt", "Wypełniasz formularz lub dzwonisz. Oddzwaniamy w 24 h."),
        ("Wizyta inżyniera", "Przyjeżdżamy do zakładu, oglądamy instalację i pobieramy próbki wody."),
        ("Sprawozdanie i rekomendacja", "Otrzymujesz raport z parametrami, rekomendacją programu i szacunkiem oszczędności."),
    ]),
    features("Co zyskujesz", [
        (ICON["doc"], "Konkretny raport", "Pomiar parametrów wody i ocena stanu instalacji — na piśmie."),
        (ICON["chart"], "Szacunek oszczędności", "Pokazujemy potencjał redukcji kosztów wody i energii."),
        (ICON["check"], "Zero zobowiązań", "Decyzję o współpracy podejmujesz po zapoznaniu się z danymi."),
    ]),
    contact(title="Umów bezpłatną konsultację", text="Zostaw kontakt i krótko opisz instalację — odezwiemy się w 24 h."),
    faq([
        ("Czy konsultacja jest naprawdę bezpłatna?", "Tak. Pierwsza wizyta, oględziny i wstępne rozpoznanie są bezpłatne i nie zobowiązują do współpracy."),
        ("Jak długo czekam na wizytę inżyniera?", "Zwykle oddzwaniamy w ciągu 24 h i ustalamy termin dopasowany do Twojego harmonogramu."),
        ("Co jeśli nie mogę teraz zmienić dostawcy chemii?", "Nie ma problemu — możemy zacząć od audytu i analizy wody, a zmianę zaplanować na później."),
    ]),
]}

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
    "title": "Kalkulator oszczędności wody dla przemysłu | Kabi-Chemie",
    "meta": "Policz orientacyjny potencjał oszczędności wody, ścieków i energii w zakładzie przemysłowym. Prosty kalkulator Kabi-Chemie dla instalacji wodnych.",
    "sections": [
    hero(
        h1="Kalkulator oszczędności wody dla zakładów przemysłowych",
        lead="Wpisz podstawowe dane instalacji i sprawdź orientacyjny potencjał oszczędności wody, ścieków oraz energii. Wynik jest szacunkiem do rozmowy z inżynierem, nie ofertą handlową.",
        ctas=[("Policz oszczędności", "#kalkulator"), ("Umów audyt techniczny", "/bezplatna-konsultacja/")],
    ),
    custom("""
<section class="section calc2-section" id="kalkulator">
  <div class="wrap">
    <div class="section-head calc2-head">
      <p class="eyebrow">Kalkulator potencjału</p>
      <h2>Policz roczny potencjał oszczędności</h2>
      <p>Wybierz typ instalacji i podaj parametry pracy. Model liczy dwa źródła strat - <strong>zakamienienie</strong> (gorsza wymiana ciepła = więcej energii / paliwa) oraz <strong>zasolenie</strong> (nadmierne odsalanie = strata wody i ciepła). Wynik to szacunek inżynierski do rozmowy, nie oferta handlowa.</p>
    </div>

    <form class="calc2" data-savings-calculator novalidate>
      <div class="calc2-grid">
        <div class="calc2-panel">
          <div class="calc2-typebar" role="tablist" aria-label="Typ instalacji">
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
              <legend><span class="calc2-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" aria-hidden="true"><path d="M12 3c.4 5.2 3.8 8.6 9 9-5.2.4-8.6 3.8-9 9-.4-5.2-3.8-8.6-9-9 5.2-.4 8.6-3.8 9-9Z"/></svg></span> Zakamienienie powierzchni grzewczych</legend>
              <div class="calc2-rows">
                <label class="calc2-field"><span class="calc2-field__label">Moc cieplna kotła <i class="calc2-info" tabindex="0" aria-label="Maksymalna moc cieplna kotła parowego określona przez producenta." data-tip="Maksymalna moc cieplna kotła parowego określona przez producenta.">i</i></span><span class="calc2-input"><input type="number" name="kb_power" value="2500" min="0" step="50" inputmode="decimal"><em>kW</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Godziny pracy / rok <i class="calc2-info" tabindex="0" aria-label="Łączna liczba godzin pracy kotła w ciągu roku (365 dni × 24 h)." data-tip="Łączna liczba godzin pracy kotła w ciągu roku (365 dni × 24 h).">i</i></span><span class="calc2-input"><input type="number" name="kb_hours" value="8760" min="0" max="8760" step="10" inputmode="decimal"><em>h</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Cena gazu ziemnego <i class="calc2-info" tabindex="0" aria-label="Aktualny koszt zakupu gazu wykorzystywanego do produkcji pary." data-tip="Aktualny koszt zakupu gazu wykorzystywanego do produkcji pary.">i</i></span><span class="calc2-input"><input type="number" name="kb_gas" value="425" min="0" step="5" inputmode="decimal"><em>zł/MWh</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Grubość kamienia <i class="calc2-info" tabindex="0" aria-label="Szacowana lub zmierzona grubość osadów na powierzchniach grzewczych kotła." data-tip="Szacowana lub zmierzona grubość osadów na powierzchniach grzewczych kotła.">i</i></span><span class="calc2-input"><input type="number" name="kb_scale" value="0.2" min="0" max="2" step="0.1" inputmode="decimal"><em>mm</em></span></label>
              </div>
            </fieldset>
            <fieldset class="calc2-group">
              <legend><span class="calc2-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.3 6 10.5a6 6 0 0 1-12 0C6 9.3 12 3 12 3Z"/></svg></span> Zasolenie wody kotłowej</legend>
              <div class="calc2-rows">
                <label class="calc2-field"><span class="calc2-field__label">Produkcja pary <i class="calc2-info" tabindex="0" aria-label="Ilość pary produkowanej przez kocioł w ciągu godziny." data-tip="Ilość pary produkowanej przez kocioł w ciągu godziny.">i</i></span><span class="calc2-input"><input type="number" name="kb_steam" value="20" min="0" step="1" inputmode="decimal"><em>t/h</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Powrót kondensatu <i class="calc2-info" tabindex="0" aria-label="Procent kondensatu zawracanego do kotła po wykorzystaniu pary." data-tip="Procent kondensatu zawracanego do kotła po wykorzystaniu pary.">i</i></span><span class="calc2-input"><input type="number" name="kb_cret" value="70" min="0" max="100" step="1" inputmode="decimal"><em>%</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Aktualne zasolenie <i class="calc2-info" tabindex="0" aria-label="Aktualna przewodność wody kotłowej utrzymywana podczas eksploatacji kotła." data-tip="Aktualna przewodność wody kotłowej utrzymywana podczas eksploatacji kotła.">i</i></span><span class="calc2-input"><input type="number" name="kb_cond" value="1500" min="0" step="50" inputmode="decimal"><em>µS/cm</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Docelowe zasolenie <i class="calc2-info" tabindex="0" aria-label="Poziom przewodności możliwy do utrzymania po wdrożeniu technologii." data-tip="Poziom przewodności możliwy do utrzymania po wdrożeniu technologii.">i</i></span><span class="calc2-input"><input type="number" name="kb_condT" value="3500" min="0" step="50" inputmode="decimal"><em>µS/cm</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Woda uzup. - odwrócona osmoza (RO) <i class="calc2-info" tabindex="0" aria-label="Przewodność świeżej wody uzupełniającej po odwróconej osmozie. Wpisz 0, jeśli zakład nie ma RO. Mocno wpływa na wynik (uwaga z arkusza)." data-tip="Przewodność świeżej wody uzupełniającej po odwróconej osmozie. Wpisz 0, jeśli zakład nie ma RO. Mocno wpływa na wynik (uwaga z arkusza).">i</i></span><span class="calc2-input"><input type="number" name="kb_make_ro" value="30" min="0" step="5" inputmode="decimal"><em>µS/cm</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Woda uzup. - stacja zmiękczania <i class="calc2-info" tabindex="0" aria-label="Przewodność świeżej wody uzupełniającej po stacji zmiękczania. Wpisz 0, jeśli zakład jej nie ma." data-tip="Przewodność świeżej wody uzupełniającej po stacji zmiękczania. Wpisz 0, jeśli zakład jej nie ma.">i</i></span><span class="calc2-input"><input type="number" name="kb_make_soft" value="0" min="0" step="5" inputmode="decimal"><em>µS/cm</em></span></label>
              </div>
            </fieldset>
          </div>

          <div class="calc2-fields" data-calc-fields="skraplacze" hidden>
            <fieldset class="calc2-group">
              <legend><span class="calc2-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" aria-hidden="true"><path d="M12 3c.4 5.2 3.8 8.6 9 9-5.2.4-8.6 3.8-9 9-.4-5.2-3.8-8.6-9-9 5.2-.4 8.6-3.8 9-9Z"/></svg></span> Zakamienienie wężownic / wymiany ciepła</legend>
              <div class="calc2-rows">
                <label class="calc2-field"><span class="calc2-field__label">Moc chłodnicza układu <i class="calc2-info" tabindex="0" aria-label="Moc układu chłodniczego opisana w karcie produktu." data-tip="Moc układu chłodniczego opisana w karcie produktu.">i</i></span><span class="calc2-input"><input type="number" name="sk_power" value="1400" min="0" step="50" inputmode="decimal"><em>kW</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">COP układu <i class="calc2-info" tabindex="0" aria-label="Współczynnik efektywności energetycznej (moc chłodnicza / pobór elektryczny). Skraplacze wyparne BAC zwykle systemowo 3–5; wartość z karty produktu." data-tip="Współczynnik efektywności energetycznej (moc chłodnicza / pobór elektryczny). Skraplacze wyparne BAC zwykle systemowo 3–5; wartość z karty produktu.">i</i></span><span class="calc2-input"><input type="number" name="sk_cop" value="4" min="1" step="0.1" inputmode="decimal"><em>–</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Godziny pracy / rok <i class="calc2-info" tabindex="0" aria-label="Dla instalacji pracujących całorocznie w trybie ciągłym przyjmuje się 8760 h/rok (365 dni × 24 h)." data-tip="Dla instalacji pracujących całorocznie w trybie ciągłym przyjmuje się 8760 h/rok (365 dni × 24 h).">i</i></span><span class="calc2-input"><input type="number" name="sk_hours" value="8760" min="0" max="8760" step="10" inputmode="decimal"><em>h</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Cena energii elektr. <i class="calc2-info" tabindex="0" aria-label="Cena energii elektrycznej netto." data-tip="Cena energii elektrycznej netto.">i</i></span><span class="calc2-input"><input type="number" name="sk_energy" value="425" min="0" step="5" inputmode="decimal"><em>zł/MWh</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Średnica czystej wężownicy <i class="calc2-info" tabindex="0" aria-label="Średnica zewnętrzna czystej wężownicy, zmierzona suwmiarką." data-tip="Średnica zewnętrzna czystej wężownicy, zmierzona suwmiarką.">i</i></span><span class="calc2-input"><input type="number" name="sk_d_clean" value="20" min="0" step="0.5" inputmode="decimal"><em>mm</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Średnica z osadem <i class="calc2-info" tabindex="0" aria-label="Średnica wężownicy z osadem. Osad liczony po obu stronach, dlatego grubość = (z osadem − czysta) / 2." data-tip="Średnica wężownicy z osadem. Osad liczony po obu stronach, dlatego grubość = (z osadem − czysta) / 2.">i</i></span><span class="calc2-input"><input type="number" name="sk_d_scaled" value="22" min="0" step="0.5" inputmode="decimal"><em>mm</em></span></label>
              </div>
            </fieldset>
            <fieldset class="calc2-group">
              <legend><span class="calc2-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.3 6 10.5a6 6 0 0 1-12 0C6 9.3 12 3 12 3Z"/></svg></span> Zasolenie wody obiegowej</legend>
              <div class="calc2-rows">
                <label class="calc2-field"><span class="calc2-field__label">Sumaryczna moc skraplania <i class="calc2-info" tabindex="0" aria-label="Łączna moc wszystkich skraplaczy wyparnych pracujących w zakładzie." data-tip="Łączna moc wszystkich skraplaczy wyparnych pracujących w zakładzie.">i</i></span><span class="calc2-input"><input type="number" name="sk_statpower" value="15000" min="0" step="100" inputmode="decimal"><em>kW</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Współczynnik spustu <i class="calc2-info" tabindex="0" aria-label="Założony poziom zatrzymania substancji mineralnych w obiegu wodnym." data-tip="Założony poziom zatrzymania substancji mineralnych w obiegu wodnym.">i</i></span><span class="calc2-input"><input type="number" name="sk_blow" value="95" min="0" max="100" step="1" inputmode="decimal"><em>%</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Aktualne zasolenie <i class="calc2-info" tabindex="0" aria-label="Aktualna przewodność wody obiegowej utrzymywana przez sterownik układu." data-tip="Aktualna przewodność wody obiegowej utrzymywana przez sterownik układu.">i</i></span><span class="calc2-input"><input type="number" name="sk_cond" value="1800" min="0" step="50" inputmode="decimal"><em>µS/cm</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Docelowe zasolenie <i class="calc2-info" tabindex="0" aria-label="Przewodność możliwa do utrzymania po wdrożeniu technologii." data-tip="Przewodność możliwa do utrzymania po wdrożeniu technologii.">i</i></span><span class="calc2-input"><input type="number" name="sk_condT" value="4000" min="0" step="50" inputmode="decimal"><em>µS/cm</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Przewodność wody uzup. <i class="calc2-info" tabindex="0" aria-label="Przewodność świeżej wody doprowadzanej do układu." data-tip="Przewodność świeżej wody doprowadzanej do układu.">i</i></span><span class="calc2-input"><input type="number" name="sk_make" value="500" min="0" step="10" inputmode="decimal"><em>µS/cm</em></span></label>
              </div>
            </fieldset>
          </div>

          <details class="calc2-adv">
            <summary>Założenia i ceny mediów</summary>
            <div class="calc2-fields" data-calc-fields="kotly">
              <div class="calc2-rows">
                <label class="calc2-field"><span class="calc2-field__label">Entalpia odsolin <i class="calc2-info" tabindex="0" aria-label="Ilość energii cieplnej zawartej w jednej tonie odsolin." data-tip="Ilość energii cieplnej zawartej w jednej tonie odsolin.">i</i></span><span class="calc2-input"><input type="number" name="kb_enth" value="721" min="0" step="1" inputmode="decimal"><em>kJ/kg</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Sprawność kotła <i class="calc2-info" tabindex="0" aria-label="Sprawność przetwarzania energii paliwa na energię zawartą w parze." data-tip="Sprawność przetwarzania energii paliwa na energię zawartą w parze.">i</i></span><span class="calc2-input"><input type="number" name="kb_eff" value="94" min="1" max="100" step="1" inputmode="decimal"><em>%</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Cena gazu - odzysk ciepła <i class="calc2-info" tabindex="0" aria-label="Cena paliwa użyta do wyceny odzysku ciepła z ograniczenia odsalania (B30 w arkuszu)." data-tip="Cena paliwa użyta do wyceny odzysku ciepła z ograniczenia odsalania (B30 w arkuszu).">i</i></span><span class="calc2-input"><input type="number" name="kb_gas2" value="425.4" min="0" step="0.1" inputmode="decimal"><em>zł/MWh</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Gęstość wody <i class="calc2-info" tabindex="0" aria-label="Parametr używany do przeliczeń masy i objętości." data-tip="Parametr używany do przeliczeń masy i objętości.">i</i></span><span class="calc2-input"><input type="number" name="kb_dens" value="997" min="0" step="1" inputmode="decimal"><em>kg/m³</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Koszt wody <i class="calc2-info" tabindex="0" aria-label="Koszt zakupu 1 m³ wody." data-tip="Koszt zakupu 1 m³ wody.">i</i></span><span class="calc2-input"><input type="number" name="kb_water" value="6" min="0" step="0.5" inputmode="decimal"><em>zł/m³</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Koszt ścieków <i class="calc2-info" tabindex="0" aria-label="Koszt odprowadzenia 1 m³ ścieków." data-tip="Koszt odprowadzenia 1 m³ ścieków.">i</i></span><span class="calc2-input"><input type="number" name="kb_sewage" value="6" min="0" step="0.5" inputmode="decimal"><em>zł/m³</em></span></label>
              </div>
            </div>
            <div class="calc2-fields" data-calc-fields="skraplacze" hidden>
              <div class="calc2-rows">
                <label class="calc2-field"><span class="calc2-field__label">Entalpia parowania <i class="calc2-info" tabindex="0" aria-label="Ilość energii potrzebna do odparowania 1 kg wody (przy ok. 33°C)." data-tip="Ilość energii potrzebna do odparowania 1 kg wody (przy ok. 33°C).">i</i></span><span class="calc2-input"><input type="number" name="sk_enth" value="2426" min="0" step="1" inputmode="decimal"><em>kJ/kg</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Gęstość wody <i class="calc2-info" tabindex="0" aria-label="Parametr wykorzystywany do przeliczeń masy i objętości." data-tip="Parametr wykorzystywany do przeliczeń masy i objętości.">i</i></span><span class="calc2-input"><input type="number" name="sk_dens" value="997" min="0" step="1" inputmode="decimal"><em>kg/m³</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Koszt wody <i class="calc2-info" tabindex="0" aria-label="Koszt zakupu 1 m³ wody." data-tip="Koszt zakupu 1 m³ wody.">i</i></span><span class="calc2-input"><input type="number" name="sk_water" value="6" min="0" step="0.5" inputmode="decimal"><em>zł/m³</em></span></label>
                <label class="calc2-field"><span class="calc2-field__label">Koszt ścieków <i class="calc2-info" tabindex="0" aria-label="Koszt odprowadzenia 1 m³ ścieków." data-tip="Koszt odprowadzenia 1 m³ ścieków.">i</i></span><span class="calc2-input"><input type="number" name="sk_sewage" value="6" min="0" step="0.5" inputmode="decimal"><em>zł/m³</em></span></label>
              </div>
            </div>
          </details>
        </div>

        <aside class="calc2-result" aria-live="polite">
          <span class="panel-kicker">Suma oszczędności / rok</span>
          <strong data-calc-total>0 zł</strong>
          <span class="calc2-accent" aria-hidden="true"></span>
          <p class="calc2-result-sub" data-calc-message>Uzupełnij dane, aby zobaczyć potencjał oszczędności.</p>
          <div class="calc2-split">
            <div><span class="calc2-split__val" data-calc-scale>0 zł</span><span class="calc2-split__lbl">odkamienienie (energia)</span></div>
            <div><span class="calc2-split__val calc2-split__val--alt" data-calc-salt>0 zł</span><span class="calc2-split__lbl">zatężenie (woda + ścieki)</span></div>
          </div>
          <div class="calc2-bar" role="img" aria-label="Udział oszczędności: odkamienienie i zatężenie">
            <span class="calc2-bar__seg calc2-bar__seg--scale" data-calc-bar-scale style="width:50%"></span>
            <span class="calc2-bar__seg calc2-bar__seg--salt" data-calc-bar-salt style="width:50%"></span>
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
          <p class="calc2-disclaimer">Wynik orientacyjny - konserwatywny model oparty o praktykę eksploatacyjną oraz zależności HVAC/ASHRAE. Dokładne wartości potwierdzamy audytem technicznym.</p>
        </aside>
      </div>

      <details class="calc2-steps">
        <summary>Szczegóły obliczeń - krok po kroku (jak w arkuszu)</summary>
        <div class="calc2-steps-inner" data-calc-fields="kotly">
          <div class="calc2-steptab">
            <h4>Zakamienienie</h4>
            <dl class="calc2-steplist">
              <div><dt>Szacowany wzrost zużycia gazu</dt><dd data-step="kb_loss">—</dd></div>
              <div><dt>Roczne zużycie energii</dt><dd data-step="kb_annualE">—</dd></div>
              <div><dt>Roczna strata energii</dt><dd data-step="kb_lossE">—</dd></div>
              <div><dt>Oszczędność po odkamienieniu</dt><dd data-step="kb_scaleSav">—</dd></div>
            </dl>
          </div>
          <div class="calc2-steptab">
            <h4>Zasolenie</h4>
            <dl class="calc2-steplist">
              <div><dt>Współczynnik odsalania</dt><dd data-step="kb_coefNow">—</dd></div>
              <div><dt>Ilość odsolin (bieżąca)</dt><dd data-step="kb_bdNow">—</dd></div>
              <div><dt>Współczynnik odsalania po zmianach</dt><dd data-step="kb_coefAfter">—</dd></div>
              <div><dt>Ilość odsolin po zmianach</dt><dd data-step="kb_bdAfter">—</dd></div>
              <div><dt>Odsoliny w ciągu roku</dt><dd data-step="kb_yrNow">—</dd></div>
              <div><dt>Odsoliny rocznie po zmianach</dt><dd data-step="kb_yrAfter">—</dd></div>
              <div><dt>Różnica w ilości odsolin</dt><dd data-step="kb_diff">—</dd></div>
              <div><dt>Zysk energetyczny</dt><dd data-step="kb_energyGain">—</dd></div>
              <div><dt>Zysk finansowy (odzysk ciepła)</dt><dd data-step="kb_finGain">—</dd></div>
              <div><dt>Oszczędność na wodzie i ściekach</dt><dd data-step="kb_waterSav">—</dd></div>
              <div><dt>Oszczędność mediów (zasolenie)</dt><dd data-step="kb_saltSav">—</dd></div>
            </dl>
          </div>
        </div>
        <div class="calc2-steps-inner" data-calc-fields="skraplacze" hidden>
          <div class="calc2-steptab">
            <h4>Zakamienienie</h4>
            <dl class="calc2-steplist">
              <div><dt>Wyliczona grubość osadu</dt><dd data-step="sk_thick">—</dd></div>
              <div><dt>Szacowany wzrost zużycia energii</dt><dd data-step="sk_loss">—</dd></div>
              <div><dt>Moc elektryczna układu</dt><dd data-step="sk_elec">—</dd></div>
              <div><dt>Dodatkowa moc elektryczna</dt><dd data-step="sk_addElec">—</dd></div>
              <div><dt>Roczna strata energii</dt><dd data-step="sk_lossE">—</dd></div>
              <div><dt>Roczny koszt strat (oszczędność)</dt><dd data-step="sk_scaleSav">—</dd></div>
            </dl>
          </div>
          <div class="calc2-steptab">
            <h4>Zasolenie</h4>
            <dl class="calc2-steplist">
              <div><dt>Współczynnik odsalania</dt><dd data-step="sk_coefNow">—</dd></div>
              <div><dt>Ilość odparowywanej wody</dt><dd data-step="sk_evap">—</dd></div>
              <div><dt>Ilość odsolin (bieżąca)</dt><dd data-step="sk_bdNow">—</dd></div>
              <div><dt>Współczynnik odsalania po zmianach</dt><dd data-step="sk_coefAfter">—</dd></div>
              <div><dt>Ilość odsolin po zmianach</dt><dd data-step="sk_bdAfter">—</dd></div>
              <div><dt>Odsoliny w ciągu roku</dt><dd data-step="sk_yrNow">—</dd></div>
              <div><dt>Odsoliny rocznie po zmianach</dt><dd data-step="sk_yrAfter">—</dd></div>
              <div><dt>Różnica w ilości odsolin</dt><dd data-step="sk_diff">—</dd></div>
              <div><dt>Oszczędność mediów (zasolenie)</dt><dd data-step="sk_saltSav">—</dd></div>
            </dl>
          </div>
        </div>
      </details>
    </form>
  </div>
</section>
"""),
    std_cta("Chcesz sprawdzić wynik na realnych danych?",
            "Podczas audytu policzymy potencjał na podstawie parametrów Twojej instalacji, kosztów mediów i obecnego programu chemicznego."),
]}

# ---------- CASE STUDIES (zbiorcza) --------------------------------------
PAGES["/case-study/"] = {"sections": [
    hero(lead="Realne dane przed i po wdrożeniu programu KCAQUA — z kotłowni parowych, chłodni amoniakalnych i zakładów przetwórczych.",
         ctas=[CONSULT]),
    cards("Realizacje", [
        {"h": "Kocioł parowy Fako", "desc": "Chemiczne odkamienianie i kondycjonowanie wody kotłowej.", "href": "/case-study/kociol-parowy-fako/", "cta": "Zobacz efekty"},
        {"h": "Skraplacz BAC — KCAQUA 305", "desc": "Optymalizacja pracy skraplacza wyparnego.", "href": "/case-study/skraplacz-bac-kcaqua/", "cta": "Zobacz efekty"},
        {"h": "Skraplacz Evapco — przetwórstwo rybne", "desc": "Czyszczenie chemiczne i odzysk wydajności chłodzenia.", "href": "/case-study/skraplacz-evapco-przetworstwo-rybne/", "cta": "Zobacz efekty"},
        {"h": "Warsztaty Amoniakalne 2024", "desc": "Nasza relacja i prelekcje o kondycjonowaniu wody.", "href": "/case-study/warsztaty-amoniakalne-2024/", "cta": "Przeczytaj"},
    ]),
    bluf("Dane liczbowe w poszczególnych realizacjach są przykładowe — do potwierdzenia i autoryzacji przez klientów przed publikacją."),
    std_cta(),
]}

# ---------- CASE STUDY: FAKO ---------------------------------------------
PAGES["/case-study/kociol-parowy-fako/"] = {"og_type": "article", "sections": [
    hero(lead="Zakład z kotłem parowym Fako zmagał się z kamieniem, stratami energii i częstymi czyszczeniami. Po wdrożeniu programu KCAQUA poprawiliśmy parametry pracy i obniżyliśmy zużycie paliwa.",
         ctas=[CONSULT]),
    richtext(title="Z czym zgłosił się zakład?", blocks=[
        ("p", "Kocioł pracował na wodzie o wysokiej twardości i przewodności. Narastający kamień izolował powierzchnie grzewcze, co zwiększało zużycie paliwa i wymuszało częste przestoje na czyszczenie."),
    ]),
    richtext(title="Jak rozwiązaliśmy problem?", blocks=[
        ("ul", ["Analiza wody i oględziny instalacji",
                "Chemiczne odkamienianie układu preparatem KCAQUA",
                "Wdrożenie programu kondycjonowania wody kotłowej (KCAQUA 303)",
                "Monitoring przewodności, twardości i pH oraz korekta dozowania"]),
    ]),
    compare("Parametry przed i po (dane przykładowe)", ["Wskaźnik", "Przed", "Po 6 tygodniach"], [
        ["Przewodność", "4200 µS", "2800 µS"],
        ["Twardość", "8°n", "0,02°n"],
        ["Zużycie paliwa", "100%", "−32%"],
        ["Cykl czyszczenia", "co 3 mies.", "co 12 mies."],
    ]),
    related([
        ("Kondycjonowanie wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
        ("Odkamienianie kotłów parowych", "/kotly-parowe/odkamienianie/"),
        ("Audyt techniczny instalacji", "/uslugi/audyt-techniczny/"),
    ]),
    std_cta("Chcesz wiedzieć, czy Twój kocioł jest właściwie kondycjonowany?"),
]}

# ---------- CASE STUDY: BAC ----------------------------------------------
PAGES["/case-study/skraplacz-bac-kcaqua/"] = {"og_type": "article", "sections": [
    hero(lead="Skraplacz wyparny BAC tracił wydajność przez osady i kamień. Dozowanie KCAQUA 305 ustabilizowało pracę układu i ograniczyło zużycie wody.",
         ctas=[CONSULT]),
    richtext(title="Sytuacja wyjściowa", blocks=[
        ("p", "Osady na powierzchniach wymiany ciepła pogarszały skuteczność chłodzenia i zwiększały zużycie wody uzupełniającej."),
    ]),
    richtext(title="Nasze działanie", blocks=[
        ("ul", ["Dobór preparatu KCAQUA 305 (biocyd + inhibitor + antyskalant)",
                "Ustawienie programu dozowania i kontroli przewodności",
                "Monitoring i korekta w pierwszych tygodniach pracy"]),
    ]),
    compare("Efekty wdrożenia (dane przykładowe)", ["Wskaźnik", "Przed", "Po"], [
        ["Zużycie wody", "100%", "−40%"],
        ["Osady na wymienniku", "narastające", "pod kontrolą"],
        ["Stabilność pracy", "spadki wydajności", "stabilna"],
    ]),
    related([
        ("Skraplacze amoniakalne", "/uklady-chlodnicze/skraplacze-amoniakalne/"),
        ("Ochrona wież chłodniczych", "/uklady-chlodnicze/ochrona-wiez-chlodniczych/"),
    ]),
    std_cta(),
]}

# ---------- CASE STUDY: EVAPCO -------------------------------------------
PAGES["/case-study/skraplacz-evapco-przetworstwo-rybne/"] = {"og_type": "article", "sections": [
    hero(lead="W zakładzie przetwórstwa rybnego skraplacz Evapco pokrył się kamieniem, tracąc wydajność chłodzenia. Przeprowadziliśmy chemiczne czyszczenie i wdrożyliśmy program kondycjonowania.",
         ctas=[CONSULT]),
    richtext(title="Problem", blocks=[
        ("p", "Twardy kamień na wężownicy ograniczał wymianę ciepła, co przekładało się na wyższe koszty i ryzyko przestojów w produkcji."),
    ]),
    richtext(title="Jak działaliśmy", blocks=[
        ("ul", ["Oględziny i analiza wody chłodzącej",
                "Chemiczne czyszczenie skraplacza",
                "Wdrożenie programu kondycjonowania i monitoring parametrów"]),
    ]),
    related([
        ("Odkamienianie układów chłodniczych", "/uklady-chlodnicze/odkamienianie/"),
        ("Skraplacze amoniakalne", "/uklady-chlodnicze/skraplacze-amoniakalne/"),
        ("Woda w przemyśle spożywczym", "/branze/"),
    ]),
    std_cta(),
]}

# ---------- CASE STUDY: WARSZTATY ----------------------------------------
PAGES["/case-study/warsztaty-amoniakalne-2024/"] = {"og_type": "article", "sections": [
    hero(lead="Uczestniczyliśmy w Warsztatach Amoniakalnych — jednym z najważniejszych wydarzeń branży chłodnictwa amoniakalnego w Polsce. Dzielimy się relacją i wnioskami z prelekcji.",
         ctas=[("Zobacz układy chłodnicze", "/uklady-chlodnicze/"), CONSULT]),
    richtext(title="Dlaczego tam jesteśmy", blocks=[
        ("p", "Warsztaty Amoniakalne to miejsce wymiany wiedzy między inżynierami i służbami utrzymania ruchu. Prezentujemy tam praktyczne podejście do kondycjonowania wody w skraplaczach natryskowo-wyparnych."),
        ("note", "Element budujący E-E-A-T: potwierdza nasze doświadczenie i obecność w środowisku branżowym."),
    ]),
    related([
        ("Skraplacze amoniakalne", "/uklady-chlodnicze/skraplacze-amoniakalne/"),
        ("Biała korozja na ocynku — baza wiedzy", "/baza-wiedzy/korozja/"),
    ]),
    std_cta(),
]}

# ---------- FAQ -----------------------------------------------------------
PAGES["/faq/"] = {"sections": [
    hero(lead="Jak dbać o kocioł parowy? Dlaczego twarda woda szkodzi? Zebraliśmy odpowiedzi na pytania, które najczęściej zadają kierownicy techniczni.",
         ctas=[CONSULT]),
    faq(title="Kotły parowe", items=[
        ("Co to jest kamień kotłowy i czemu niszczy kocioł?", "Kamień to osad z soli twardości wytrącających się na gorących powierzchniach. Izoluje je termicznie — już 1 mm kamienia może podnieść zużycie paliwa o ok. 10% i prowadzić do przegrzań."),
        ("Jak często należy kondycjonować wodę kotłową?", "Kondycjonowanie to proces ciągły — dozujemy chemię i monitorujemy parametry na bieżąco, a nie jednorazowo."),
        ("Czy kondycjonowanie zmniejsza zużycie paliwa?", "Tak. Czyste powierzchnie grzewcze lepiej przewodzą ciepło, więc kocioł zużywa mniej paliwa do wytworzenia tej samej ilości pary."),
    ]),
    faq(title="Chłodnice i wieże", items=[
        ("Czym jest biofilm w wieży chłodniczej?", "To warstwa mikroorganizmów na powierzchniach układu. Pogarsza wymianę ciepła, sprzyja korozji i może być siedliskiem bakterii (np. Legionella)."),
        ("Jak często odkamieniać układ chłodniczy?", "Zależnie od jakości wody i obciążenia — przy prawidłowym kondycjonowaniu częstotliwość czyszczeń znacząco spada."),
    ]),
    faq(title="Współpraca", items=[
        ("Jak wygląda pierwsza wizyta?", "Inżynier ogląda instalację, pobiera próbki wody i wykonuje pomiary. Na tej podstawie powstaje raport i rekomendacja."),
        ("Czy chemia jest bezpieczna dla zakładu spożywczego?", "Dobieramy preparaty i programy zgodnie z wymaganiami danego zakładu — bezpieczeństwo procesu jest priorytetem."),
        ("Co jeśli efekty są widoczne dopiero po kilku tygodniach?", "Mówimy o tym wprost. Część efektów (np. usuwanie kamienia) jest stopniowa — pokazujemy postęp na danych."),
    ]),
    std_cta(),
]}

# ================================================================== KOTŁY PAROWE
PAGES["/kotly-parowe/"] = {"sections": [
    hero(lead="<strong>Kondycjonujemy wodę w kotłach parowych</strong> — usuwamy kamień, chronimy przed korozją i obniżamy zużycie energii. Autorska chemia KCAQUA 303 dopasowana do Twojej kotłowni.",
         ctas=[CONSULT, ("Zobacz case study Fako", "/case-study/kociol-parowy-fako/")]),
    richtext(title="Dlaczego woda kotłowa wymaga kondycjonowania?", blocks=[
        ("ul", ["<strong>1 mm kamienia</strong> to nawet +10% zużycia paliwa i ryzyko przegrzania rur.",
                "Zła przewodność wymusza częstsze odsalanie — to marnowana woda i energia.",
                "Korozja tlenowa prowadzi do wżerów, nieszczelności i kosztownych awarii."]),
    ]),
    cards("Nasze rozwiązania dla kotłowni", [
        {"h": "Kondycjonowanie wody kotłowej", "desc": "Program dozowania KCAQUA 303 — ochrona i oszczędność.", "href": "/kotly-parowe/kondycjonowanie-wody-kotlowej/"},
        {"h": "Odkamienianie kotłów", "desc": "Chemiczne usuwanie kamienia w trakcie eksploatacji.", "href": "/kotly-parowe/odkamienianie/"},
        {"h": "Ochrona antykorozyjna", "desc": "Inhibitory korozji i wiązanie tlenu w układzie parowym.", "href": "/kotly-parowe/ochrona-antykorozyjna/"},
    ]),
    steps("Jak kondycjonujemy wodę kotłową", [
        ("Analiza wody i instalacji", "Pomiar twardości, pH, przewodności i żelaza."),
        ("Dobór preparatu KCAQUA 303", "Inhibitor korozji + odtlenianie + korekta pH."),
        ("Wdrożenie dozowania", "Ustawienie programu i pomp dozujących."),
        ("Monitoring i korekta", "Bieżąca kontrola parametrów i raportowanie."),
    ]),
    table("Co niszczy kocioł parowy", ["Problem", "Skutek", "Nasze rozwiązanie"], [
        ["Kamień", "−10% efektywności na 1 mm", "KCAQUA 303 + odkamienianie"],
        ["Korozja tlenowa", "Wżery i nieszczelności rur", "Inhibitory + wiązanie tlenu"],
        ["Złe pH", "Przyspieszona korozja", "Korekta chemiczna"],
    ]),
    faq([
        ("Jak kondycjonowanie wody zmniejsza rachunki za paliwo?", "Usuwając warstwę kamienia, która izoluje powierzchnie grzewcze. Czysty kocioł oddaje ciepło wodzie znacznie efektywniej."),
        ("Czy program wymaga wyłączenia kotła?", "Kondycjonowanie prowadzimy w trakcie normalnej eksploatacji. Odkamienianie chemiczne planujemy zależnie od stanu układu."),
        ("Co się stanie, jeśli nie będę kondycjonować wody?", "Narasta kamień i korozja — rosną koszty paliwa, częstotliwość czyszczeń i ryzyko awarii."),
    ]),
    related([
        ("Kondycjonowanie wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
        ("Odkamienianie kotłów parowych", "/kotly-parowe/odkamienianie/"),
        ("Audyt techniczny instalacji", "/uslugi/audyt-techniczny/"),
    ]),
    std_cta("Sprawdź, czy Twój kocioł jest właściwie kondycjonowany"),
]}

PAGES["/kotly-parowe/kondycjonowanie-wody-kotlowej/"] = {"sections": [
    hero(lead="Prowadzimy kondycjonowanie wody kotłowej w oparciu o pomiar i program dozowania KCAQUA 303 — z realnym efektem energetycznym.",
         ctas=[CONSULT]),
    table("Parametry wody kotłowej", ["Parametr", "Norma", "Znaczenie"], [
        ["pH", "9,0–11,0", "ochrona przed korozją"],
        ["Twardość", "< 0,02°n", "zapobiega kamieniowi"],
        ["Przewodność", "< 3000 µS", "kontrola odsalania"],
        ["Żelazo", "< 0,1 mg/l", "wskaźnik korozji"],
    ], note="Wartości orientacyjne — docelowe normy dobieramy do konkretnego kotła i wymagań procesu."),
    steps("Jak działamy", [
        ("Analiza wody", "Pomiar parametrów i ocena instalacji."),
        ("Dobór preparatu", "KCAQUA 303 do Twojego układu."),
        ("Wdrożenie i monitoring", "Dozowanie, kontrola przewodności i pH, korekta."),
    ]),
    related([
        ("Odkamienianie kotłów", "/kotly-parowe/odkamienianie/"),
        ("Ochrona antykorozyjna układów parowych", "/kotly-parowe/ochrona-antykorozyjna/"),
        ("Parametry wody — baza wiedzy", "/baza-wiedzy/parametry-wody/"),
    ]),
    std_cta(),
]}

PAGES["/kotly-parowe/odkamienianie/"] = {"sections": [
    hero(lead="Chemicznie rozpuszczamy kamień w kotłach parowych — przywracamy wymianę ciepła i chronimy instalację przed awariami, bez kosztownego demontażu.",
         ctas=[CONSULT]),
    richtext(title="Po co odkamieniać kocioł?", blocks=[
        ("p", "Kamień działa jak izolator. Im grubsza warstwa, tym więcej paliwa potrzeba do wytworzenia pary i tym większe ryzyko przegrzań i pęknięć."),
    ]),
    steps("Przebieg odkamieniania", [
        ("Ocena stanu i wody", "Określamy rodzaj i grubość osadu."),
        ("Czyszczenie chemiczne", "Dobrany preparat rozpuszcza kamień."),
        ("Płukanie i pasywacja", "Zabezpieczamy oczyszczone powierzchnie."),
        ("Kondycjonowanie", "Wdrażamy program, by kamień nie wracał."),
    ]),
    related([
        ("Kondycjonowanie wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
        ("Case study: kocioł parowy Fako", "/case-study/kociol-parowy-fako/"),
        ("Chemiczne czyszczenie instalacji", "/ochrona-antykorozyjna/chemiczne-czyszczenie/"),
    ]),
    std_cta(),
]}

PAGES["/kotly-parowe/ochrona-antykorozyjna/"] = {"sections": [
    hero(lead="Chronimy układy parowe przed korozją — inhibitory korozji, chemiczne wiązanie tlenu i korekta pH w jednym programie.",
         ctas=[CONSULT]),
    features("Jak chronimy układ parowy", [
        (ICON["shield"], "Inhibitory korozji", "Tworzą warstwę ochronną na powierzchniach metalu."),
        (ICON["drop"], "Wiązanie tlenu", "Usuwamy tlen rozpuszczony — główny sprawca korozji tlenowej."),
        (ICON["flask"], "Korekta pH", "Utrzymujemy pH w zakresie bezpiecznym dla stali."),
    ]),
    richtext(title="Warstwa magnetytowa — naturalna ochrona", blocks=[
        ("p", "Prawidłowo prowadzony układ buduje na stali ochronną warstwę magnetytu. Naszym zadaniem jest ją utrzymać, a nie zniszczyć agresywną chemią."),
    ]),
    related([
        ("Kondycjonowanie wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
        ("Korozja tlenowa — baza wiedzy", "/baza-wiedzy/korozja/"),
        ("Pasywacja stali", "/ochrona-antykorozyjna/pasywacja-stali/"),
    ]),
    std_cta(),
]}

# ================================================================== UKŁADY CHŁODNICZE
PAGES["/uklady-chlodnicze/"] = {"sections": [
    hero(lead="<strong>Kondycjonujemy wodę w układach chłodniczych</strong> — chronimy wieże i skraplacze przed kamieniem, korozją i biofilmem, ograniczając zużycie wody.",
         ctas=[CONSULT, ("Case study: skraplacz BAC", "/case-study/skraplacz-bac-kcaqua/")]),
    cards("Nasze rozwiązania dla chłodnictwa", [
        {"h": "Ochrona wież chłodniczych", "desc": "Biocydy i inhibitory — kontrola biofilmu i korozji.", "href": "/uklady-chlodnicze/ochrona-wiez-chlodniczych/"},
        {"h": "Odkamienianie układów", "desc": "Usuwanie kamienia z wież i skraplaczy w trakcie pracy.", "href": "/uklady-chlodnicze/odkamienianie/"},
        {"h": "Skraplacze amoniakalne", "desc": "Ochrona przed białą korozją i kamieniem.", "href": "/uklady-chlodnicze/skraplacze-amoniakalne/"},
    ]),
    table("Co zagraża układowi chłodniczemu", ["Problem", "Skutek", "Rozwiązanie"], [
        ["Kamień", "Spadek wymiany ciepła", "Antyskalant + odkamienianie"],
        ["Biofilm", "Korozja, ryzyko Legionelli", "Biocydy KCAQUA 305"],
        ["Korozja", "Awarie i przecieki", "Inhibitory korozji"],
    ]),
    faq([
        ("Jak często odkamieniać układ chłodniczy?", "Przy prawidłowym kondycjonowaniu częstotliwość czyszczeń wyraźnie spada. Harmonogram ustalamy na podstawie jakości wody i obciążenia."),
        ("Czy biocydy są bezpieczne dla środowiska?", "Dobieramy preparaty i dawki zgodnie z wymaganiami i przepisami. Kontrolujemy stężenia w obiegu."),
    ]),
    related([
        ("Skraplacze amoniakalne", "/uklady-chlodnicze/skraplacze-amoniakalne/"),
        ("Biofilm w układzie chłodniczym — baza wiedzy", "/baza-wiedzy/wieze-chlodnicze/"),
        ("Analiza wody chłodniczej", "/uslugi/analiza-wody/"),
    ]),
    std_cta(),
]}

PAGES["/uklady-chlodnicze/ochrona-wiez-chlodniczych/"] = {"sections": [
    hero(lead="Zabezpieczamy wieże chłodnicze przed biofilmem i korozją — sprawdzone biocydy i inhibitory KCAQUA dla ciągłości pracy układu.",
         ctas=[CONSULT]),
    features("Co kontrolujemy w wieży", [
        (ICON["leaf"], "Biofilm i mikroorganizmy", "Ograniczamy rozwój bakterii i glonów w obiegu."),
        (ICON["shield"], "Korozja", "Chronimy metal inhibitorami korozji."),
        (ICON["drop"], "Kamień", "Antyskalant zapobiega wytrącaniu twardości."),
    ]),
    related([
        ("Odkamienianie układów chłodniczych", "/uklady-chlodnicze/odkamienianie/"),
        ("Skraplacze amoniakalne", "/uklady-chlodnicze/skraplacze-amoniakalne/"),
        ("Wieże chłodnicze — baza wiedzy", "/baza-wiedzy/wieze-chlodnicze/"),
    ]),
    std_cta(),
]}

PAGES["/uklady-chlodnicze/odkamienianie/"] = {"sections": [
    hero(lead="Bezpiecznie usuwamy kamień z wież i skraplaczy w trakcie eksploatacji — przywracamy pełną wydajność układu chłodniczego.",
         ctas=[CONSULT]),
    steps("Jak odkamieniamy układ chłodniczy", [
        ("Diagnoza", "Oceniamy rodzaj i grubość osadu oraz jakość wody."),
        ("Czyszczenie chemiczne", "Rozpuszczamy kamień bez demontażu układu."),
        ("Kondycjonowanie", "Wdrażamy program, by osad nie narastał ponownie."),
    ]),
    related([
        ("Ochrona wież chłodniczych", "/uklady-chlodnicze/ochrona-wiez-chlodniczych/"),
        ("Case study: skraplacz Evapco", "/case-study/skraplacz-evapco-przetworstwo-rybne/"),
    ]),
    std_cta(),
]}

PAGES["/uklady-chlodnicze/skraplacze-amoniakalne/"] = {"sections": [
    hero(lead="Kondycjonujemy wodę w skraplaczach natryskowo-wyparnych — chronimy wężownice przed białą korozją i kamieniem, utrzymując wydajność chłodzenia.",
         ctas=[CONSULT, ("Warsztaty Amoniakalne 2024", "/case-study/warsztaty-amoniakalne-2024/")]),
    richtext(title="Specyfika skraplaczy amoniakalnych", blocks=[
        ("p", "Wężownice ocynkowane są narażone na tzw. białą rdzę i osady kamienia, które ograniczają wymianę ciepła. Program KCAQUA 305 chroni powierzchnie i stabilizuje pracę układu."),
    ]),
    related([
        ("Ochrona wież chłodniczych", "/uklady-chlodnicze/ochrona-wiez-chlodniczych/"),
        ("Case study: skraplacz BAC", "/case-study/skraplacz-bac-kcaqua/"),
        ("Biała korozja — baza wiedzy", "/baza-wiedzy/korozja/"),
    ]),
    std_cta(),
]}

# ================================================================== MEMBRANY RO
PAGES["/membrany-ro/"] = {"sections": [
    hero(lead="<strong>Chronimy membrany odwróconej osmozy przed foulingiem i kamieniem.</strong> Nasz antyskalant wydłuża żywotność membran i utrzymuje wydajność stacji RO.",
         ctas=[CONSULT]),
    features("Jak chronimy membrany RO", [
        (ICON["membrane"], "Antyskalant", "Zapobiega wytrącaniu soli na powierzchni membran."),
        (ICON["leaf"], "Kontrola foulingu", "Ograniczamy osady organiczne i biologiczne."),
        (ICON["bolt"], "Wiązanie gazów", "Nasz preparat wiąże chlor i chlorki degradujące membrany."),
    ], intro="Chlor i chlorki są groźne dla membran RO — dlatego ich kontrola jest kluczowa."),
    richtext(title="Dlaczego to ważne", blocks=[
        ("p", "Fouling i kamień na membranach obniżają strumień permeatu i podnoszą ciśnienie pracy. Dobrze dobrany antyskalant to dłuższa żywotność membran i niższe koszty eksploatacji."),
    ]),
    related([
        ("Antyskalant do membran RO — baza wiedzy", "/baza-wiedzy/membrany-ro/"),
        ("Analiza wody", "/uslugi/analiza-wody/"),
        ("Odkamienianie instalacji", "/odkamienianie-instalacji/"),
    ]),
    std_cta(),
]}

# ================================================================== ODKAMIENIANIE INSTALACJI
PAGES["/odkamienianie-instalacji/"] = {"sections": [
    hero(lead="Profesjonalnie odkamieniamy instalacje przemysłowe — bezpiecznie usuwamy twardy kamień i osady z rurociągów oraz wymienników ciepła.",
         ctas=[CONSULT]),
    features("Co odkamieniamy", [
        (ICON["flame"], "Wymienniki ciepła", "Przywracamy sprawność wymiany cieplnej."),
        (ICON["wrench"], "Rurociągi", "Udrażniamy przepływy ograniczone osadem."),
        (ICON["snow"], "Układy chłodnicze", "Usuwamy kamień z wież i skraplaczy."),
    ]),
    steps("Jak przebiega odkamienianie", [
        ("Audyt układu", "Oceniamy rodzaj osadu i materiał instalacji."),
        ("Dobór chemii", "Bezpieczny dla materiału preparat czyszczący."),
        ("Czyszczenie i płukanie", "Rozpuszczamy osad i neutralizujemy."),
        ("Zabezpieczenie", "Pasywacja i program zapobiegający nawrotom."),
    ]),
    related([
        ("Chemiczne czyszczenie instalacji", "/ochrona-antykorozyjna/chemiczne-czyszczenie/"),
        ("Odkamienianie kotłów parowych", "/kotly-parowe/odkamienianie/"),
        ("Odkamienianie układów chłodniczych", "/uklady-chlodnicze/odkamienianie/"),
    ]),
    std_cta(),
]}

# ================================================================== OCHRONA ANTYKOROZYJNA
PAGES["/ochrona-antykorozyjna/"] = {"sections": [
    hero(lead="<strong>Wdrażamy programy antykorozyjne dla przemysłu.</strong> Chronimy instalacje wodne przed rdzą i degradacją — od pasywacji po chemiczne czyszczenie.",
         ctas=[CONSULT]),
    cards("Zakres ochrony antykorozyjnej", [
        {"h": "Pasywacja stali", "desc": "Zabezpieczenie nowych instalacji przed montażem i po montażu.", "href": "/ochrona-antykorozyjna/pasywacja-stali/"},
        {"h": "Chemiczne czyszczenie", "desc": "Usuwanie osadów i produktów korozji z instalacji.", "href": "/ochrona-antykorozyjna/chemiczne-czyszczenie/"},
    ]),
    features("Jak chronimy instalacje", [
        (ICON["shield"], "Inhibitory korozji", "Warstwa ochronna na powierzchniach metalu."),
        (ICON["drop"], "Kontrola tlenu i pH", "Eliminujemy główne przyczyny korozji."),
        (ICON["doc"], "Monitoring", "Pomiar korozyjności i raportowanie trendów."),
    ]),
    related([
        ("Ochrona antykorozyjna układów parowych", "/kotly-parowe/ochrona-antykorozyjna/"),
        ("Korozja w instalacjach — baza wiedzy", "/baza-wiedzy/korozja/"),
    ]),
    std_cta(),
]}

PAGES["/ochrona-antykorozyjna/pasywacja-stali/"] = {"sections": [
    hero(lead="Pasywujemy stal nierdzewną i węglową — zabezpieczamy nowe instalacje przemysłowe przed korozją, zanim zacznie się problem.",
         ctas=[CONSULT]),
    richtext(title="Czym jest pasywacja", blocks=[
        ("p", "Pasywacja to chemiczne wytworzenie lub odtworzenie warstwy ochronnej na powierzchni stali. Dla instalacji po montażu lub spawaniu to kluczowy krok wydłużający żywotność."),
    ]),
    related([
        ("Chemiczne czyszczenie instalacji", "/ochrona-antykorozyjna/chemiczne-czyszczenie/"),
        ("Pasywacja stali — baza wiedzy", "/baza-wiedzy/korozja/"),
    ]),
    std_cta(),
]}

PAGES["/ochrona-antykorozyjna/chemiczne-czyszczenie/"] = {"sections": [
    hero(lead="Specjalistyczne chemiczne czyszczenie instalacji przemysłowych — usuwamy uporczywe osady i przywracamy przepływy oraz wydajność układu.",
         ctas=[CONSULT]),
    steps("Przebieg czyszczenia chemicznego", [
        ("Diagnoza", "Identyfikujemy osad i dobieramy bezpieczny preparat."),
        ("Czyszczenie", "Rozpuszczamy osady w obiegu zamkniętym."),
        ("Neutralizacja i pasywacja", "Zabezpieczamy oczyszczone powierzchnie."),
    ]),
    related([
        ("Odkamienianie instalacji", "/odkamienianie-instalacji/"),
        ("Pasywacja stali", "/ochrona-antykorozyjna/pasywacja-stali/"),
    ]),
    std_cta(),
]}

# ================================================================== USŁUGI
PAGES["/uslugi/"] = {"sections": [
    hero(lead="<strong>Trzy usługi inżynieryjne, które porządkują gospodarkę wodną zakładu:</strong> audyt techniczny, analiza wody i serwis urządzeń uzdatniania.",
         ctas=[CONSULT]),
    cards("Nasze usługi", [
        {"h": "Audyt techniczny", "desc": "Bezpłatna wizyta inżyniera i ocena stanu instalacji.", "href": "/uslugi/audyt-techniczny/"},
        {"h": "Analiza wody", "desc": "Badanie parametrów wody kotłowej i chłodniczej.", "href": "/uslugi/analiza-wody/"},
        {"h": "Serwis urządzeń", "desc": "Serwis stacji uzdatniania, pomp i sond.", "href": "/uslugi/serwis-urzadzen/"},
    ]),
    steps("Proces współpracy", [
        ("Audyt techniczny", "Inżynier ocenia instalację i mierzy parametry."),
        ("Program chemiczny", "Dobieramy preparat KCAQUA do układu."),
        ("Monitoring i serwis", "Regularne wizyty i kontrola parametrów."),
    ]),
    related([
        ("Bezpłatna konsultacja", "/bezplatna-konsultacja/"),
        ("Branże, które obsługujemy", "/branze/"),
    ]),
    std_cta(),
]}

PAGES["/uslugi/audyt-techniczny/"] = {"sections": [
    hero(lead="Zamów bezpłatny audyt techniczny instalacji uzdatniania wody. Inżynier oceni stan urządzeń i zaproponuje optymalizację kosztów chemii.",
         ctas=[CONSULT]),
    features("Co sprawdzamy podczas audytu", [
        (ICON["drop"], "Parametry wody", "Twardość, pH, przewodność, TDS, żelazo."),
        (ICON["flame"], "Stan instalacji", "Kotły, wieże, wymienniki i membrany."),
        (ICON["chart"], "Potencjał oszczędności", "Zużycie wody i energii vs możliwa redukcja."),
    ]),
    richtext(title="Co zawiera sprawozdanie", blocks=[
        ("ul", ["Wyniki pomiarów parametrów wody",
                "Ocena stanu instalacji i zidentyfikowane ryzyka",
                "Rekomendowany program chemiczny",
                "Szacunkowe oszczędności"]),
    ]),
    faq([
        ("Ile trwa audyt techniczny?", "Sama wizyta to zwykle kilka godzin. Sprawozdanie z rekomendacjami dostarczamy w ustalonym terminie po analizie."),
        ("Czy audyt jest płatny?", "Podstawowy audyt i oględziny są bezpłatne i bez zobowiązań."),
    ]),
    related([
        ("Analiza wody", "/uslugi/analiza-wody/"),
        ("Bezpłatna konsultacja", "/bezplatna-konsultacja/"),
    ]),
    std_cta(),
]}

PAGES["/uslugi/analiza-wody/"] = {"sections": [
    hero(lead="Badamy parametry wody przemysłowej — kotłowej i chłodniczej — by zapobiegać kamieniowi i korozji, zanim wywołają awarię.",
         ctas=[CONSULT]),
    table("Co badamy", ["Parametr", "Po co", "Ryzyko przy odchyleniu"], [
        ["pH", "kontrola korozyjności", "korozja zasadowa/kwasowa"],
        ["Twardość", "ryzyko kamienia", "narastanie osadu"],
        ["Przewodność", "sterowanie odsalaniem", "marnowanie wody"],
        ["Żelazo", "wskaźnik korozji", "wżery i osady"],
    ]),
    steps("Jak wygląda badanie", [
        ("Pobór próbki", "Pomiar własnym sprzętem w zakładzie."),
        ("Analiza", "Porównanie z normami i wymaganiami procesu."),
        ("Raport", "Rekomendacje i program korygujący."),
    ]),
    related([
        ("Audyt techniczny", "/uslugi/audyt-techniczny/"),
        ("Parametry wody — baza wiedzy", "/baza-wiedzy/parametry-wody/"),
    ]),
    std_cta(),
]}

PAGES["/uslugi/serwis-urzadzen/"] = {"sections": [
    hero(lead="Serwisujemy urządzenia uzdatniania wody — stacje zmiękczania i RO, pompy dozujące oraz sondy i sterowniki.",
         ctas=[CONSULT]),
    features("Co serwisujemy", [
        (ICON["gear"], "Stacje SUW i RO", "Stacje zmiękczania i odwróconej osmozy."),
        (ICON["wrench"], "Pompy dozujące", "Kalibracja i naprawa układów dozowania."),
        (ICON["bolt"], "Sondy i sterowniki", "Sondy przewodności i sterowniki odsalania."),
    ]),
    faq([
        ("Jak szybko reagujecie na awarię?", "Awarie pilne staramy się obsłużyć priorytetowo. Serwis planowy realizujemy w uzgodnionym harmonogramie."),
        ("Jakie marki urządzeń serwisujecie?", "Obsługujemy popularne urządzenia stosowane w przemyśle. Zakres potwierdzamy po rozpoznaniu."),
    ]),
    related([
        ("Audyt techniczny", "/uslugi/audyt-techniczny/"),
        ("Analiza wody", "/uslugi/analiza-wody/"),
    ]),
    std_cta(),
]}

# ================================================================== BRANŻE
PAGES["/branze/"] = {"sections": [
    hero(lead="<strong>Dobieramy kondycjonowanie wody do specyfiki Twojej branży.</strong> Obsługujemy zakłady spożywcze, chłodnie i przemysł ciężki.",
         ctas=[CONSULT]),
    features("Branże, które obsługujemy", [
        (ICON["factory"], "Zakłady mięsne i drób", "Para do produkcji — kamień to straty ciepła. Program KCAQUA 303."),
        (ICON["flask"], "Mleczarnie i browary", "Pasteryzacja i procesy cieplne — kamień w wymiennikach."),
        (ICON["snow"], "Chłodnie i skraplacze", "Skraplacze natryskowo-wyparne — ochrona przed kamieniem i białą korozją."),
        (ICON["bolt"], "Przemysł ciężki", "Huty i kopalnie — systemy chłodzenia w trudnych warunkach."),
    ]),
    related([
        ("Kotły parowe", "/kotly-parowe/"),
        ("Układy chłodnicze", "/uklady-chlodnicze/"),
        ("Case studies", "/case-study/"),
    ]),
    std_cta(),
]}

# ================================================================== BAZA WIEDZY (BLOG)
PAGES["/baza-wiedzy/"] = {"sections": [
    hero(lead="Ekspercki blog o kondycjonowaniu wody w przemyśle — kamień, korozja, parametry wody i membrany RO. Wiedza dla inżynierów i kierowników utrzymania ruchu.",
         ctas=[("Umów konsultację", "/bezplatna-konsultacja/")]),
    cards("Kategorie", [
        {"h": "Kotły parowe i para", "desc": "Kamień, korozja, oszczędność paliwa.", "href": "/baza-wiedzy/kotly-parowe/"},
        {"h": "Wieże chłodnicze", "desc": "Biofilm, biocydy, odkamienianie skraplaczy.", "href": "/baza-wiedzy/wieze-chlodnicze/"},
        {"h": "Korozja i ochrona", "desc": "Inhibitory, pasywacja, rodzaje korozji.", "href": "/baza-wiedzy/korozja/"},
        {"h": "Parametry wody", "desc": "pH, twardość, przewodność, TDS.", "href": "/baza-wiedzy/parametry-wody/"},
        {"h": "Membrany RO", "desc": "Antyskalant, fouling, demineralizacja.", "href": "/baza-wiedzy/membrany-ro/"},
    ]),
    bloglist("Najnowsze artykuły", [
        {"h": "Co to jest kamień kotłowy i dlaczego niszczy kotły parowe?", "desc": "Jak powstaje kamień, jak wpływa na zużycie paliwa i jak go usunąć.", "href": "/baza-wiedzy/pojedynczy-wpis-blogowy-1/", "cat": "Kotły parowe", "meta": "8 min czytania"},
        {"h": "Biofilm w układzie chłodniczym — jak usunąć osady biologiczne?", "desc": "Dlaczego biofilm jest groźny i jak go kontrolować biocydami.", "href": "/baza-wiedzy/pojedynczy-wpis-blogowy-2/", "cat": "Wieże chłodnicze", "meta": "7 min czytania"},
        {"h": "Antyskalant i jego rola w ochronie membran RO", "desc": "Jak antyskalant chroni membrany odwróconej osmozy przed foulingiem.", "href": "/baza-wiedzy/pojedynczy-wpis-blogowy-3/", "cat": "Membrany RO", "meta": "6 min czytania"},
    ]),
    std_cta(),
]}

PAGES["/autor/"] = {"sections": [
    hero(lead="Za treściami w bazie wiedzy stoją inżynierowie i technolodzy z praktycznym doświadczeniem w kondycjonowaniu wody przemysłowej.",
         ctas=[("Baza wiedzy", "/baza-wiedzy/"), CONSULT]),
    author("Zespół ekspertów Kabi-Chemie", "Inżynierowie i technolodzy kondycjonowania wody",
           "Tworzymy specjalistyczne treści o uzdatnianiu i kondycjonowaniu wody dla przemysłu. Nasze doświadczenie potwierdza m.in. udział w Warsztatach Amoniakalnych. <em>(Biogram do uzupełnienia o realne dane i zdjęcia autorów.)</em>"),
    bloglist("Artykuły zespołu", [
        {"h": "Co to jest kamień kotłowy?", "desc": "", "href": "/baza-wiedzy/pojedynczy-wpis-blogowy-1/", "cat": "Kotły parowe"},
        {"h": "Biofilm w układzie chłodniczym", "desc": "", "href": "/baza-wiedzy/pojedynczy-wpis-blogowy-2/", "cat": "Wieże chłodnicze"},
        {"h": "Antyskalant do membran RO", "desc": "", "href": "/baza-wiedzy/pojedynczy-wpis-blogowy-3/", "cat": "Membrany RO"},
    ]),
    std_cta(),
]}

def _blog_cat(lead, posts, related_links):
    return {"sections": [
        hero(lead=lead, ctas=[("Umów konsultację", "/bezplatna-konsultacja/")]),
        bloglist("Artykuły w tej kategorii", posts),
        related(related_links),
        std_cta(),
    ]}

PAGES["/baza-wiedzy/kotly-parowe/"] = _blog_cat(
    "Wszystko o kondycjonowaniu wody w kotłach parowych — jak zapobiegać awariom, usuwać kamień i oszczędzać paliwo.",
    [{"h": "Co to jest kamień kotłowy i dlaczego niszczy kotły parowe?", "desc": "Mechanizm powstawania kamienia i jego wpływ na koszty.", "href": "/baza-wiedzy/pojedynczy-wpis-blogowy-1/", "cat": "Kotły parowe", "meta": "8 min"}],
    [("Kotły parowe — oferta", "/kotly-parowe/"), ("Parametry wody", "/baza-wiedzy/parametry-wody/")])

PAGES["/baza-wiedzy/wieze-chlodnicze/"] = _blog_cat(
    "Optymalizacja pracy wież chłodniczych i obiegów — biofilm, biocydy i usuwanie kamienia ze skraplaczy.",
    [{"h": "Biofilm w układzie chłodniczym — jak usunąć osady biologiczne?", "desc": "Kontrola mikroorganizmów w obiegu chłodzącym.", "href": "/baza-wiedzy/pojedynczy-wpis-blogowy-2/", "cat": "Wieże chłodnicze", "meta": "7 min"}],
    [("Układy chłodnicze — oferta", "/uklady-chlodnicze/"), ("Skraplacze amoniakalne", "/uklady-chlodnicze/skraplacze-amoniakalne/")])

PAGES["/baza-wiedzy/korozja/"] = _blog_cat(
    "Jak chronić instalacje przemysłowe przed korozją — inhibitory, pasywacja stali i rodzaje korozji.",
    [{"h": "Korozja w instalacjach przemysłowych — rodzaje i zapobieganie", "desc": "Korozja tlenowa, wżerowa i biała — jak im przeciwdziałać.", "href": "/baza-wiedzy/pojedynczy-wpis-blogowy-1/", "cat": "Korozja", "meta": "9 min"}],
    [("Ochrona antykorozyjna — oferta", "/ochrona-antykorozyjna/"), ("Pasywacja stali", "/ochrona-antykorozyjna/pasywacja-stali/")])

PAGES["/baza-wiedzy/parametry-wody/"] = _blog_cat(
    "Zrozum parametry wody w przemyśle — wpływ pH, twardości i przewodności na pracę kotłów i układów chłodniczych.",
    [{"h": "Twardość wody — dlaczego niszczy kotły i instalacje?", "desc": "Stopnie twardości i ich znaczenie dla przemysłu.", "href": "/baza-wiedzy/pojedynczy-wpis-blogowy-1/", "cat": "Parametry wody", "meta": "6 min"}],
    [("Analiza wody", "/uslugi/analiza-wody/"), ("Kondycjonowanie wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/")])

PAGES["/baza-wiedzy/membrany-ro/"] = _blog_cat(
    "Ochrona membran odwróconej osmozy (RO) przed foulingiem — dobór antyskalantu i dbałość o demineralizację.",
    [{"h": "Antyskalant i jego rola w ochronie membran RO", "desc": "Jak antyskalant przedłuża żywotność membran.", "href": "/baza-wiedzy/pojedynczy-wpis-blogowy-3/", "cat": "Membrany RO", "meta": "6 min"}],
    [("Membrany RO — oferta", "/membrany-ro/"), ("Analiza wody", "/uslugi/analiza-wody/")])

# ---------- WPISY BLOGOWE -------------------------------------------------
def _post(lead, blocks, faqs, rel, image=None, image_alt="", image_caption=""):
    secs = [
        hero(lead=lead, ctas=[("Umów konsultację", "/bezplatna-konsultacja/")]),
    ]
    if image:
        caption = f'<figcaption>{image_caption}</figcaption>' if image_caption else ''
        secs.append(custom(f'''<section class="section post-cover-section">
  <div class="wrap">
    <figure class="post-cover reveal">
      <img src="{image}" alt="{image_alt}" loading="eager">
      {caption}
    </figure>
  </div>
</section>'''))
    secs.append(richtext(blocks=blocks))
    if faqs:
        secs.append(faq(faqs))
    secs.append(related(rel))
    secs.append(std_cta())
    page = {"og_type": "article", "sections": secs}
    if image:
        page["og_image"] = image
    return page

PAGES["/baza-wiedzy/pojedynczy-wpis-blogowy-1/"] = _post(
    "Kamień kotłowy to osad soli twardości na gorących powierzchniach kotła. Działa jak izolator — podnosi zużycie paliwa i grozi przegrzaniem rur.",
    [("h2", "Jak powstaje kamień kotłowy?"),
     ("p", "Podgrzewana woda traci zdolność utrzymania rozpuszczonych soli wapnia i magnezu. Wytrącają się one na najgorętszych powierzchniach, tworząc twardą skorupę."),
     ("h2", "Jak kamień wpływa na rachunki za paliwo?"),
     ("p", "Już <strong>1 mm kamienia</strong> może zwiększyć zużycie paliwa o około 10%, bo ciepło trudniej przenika do wody."),
     ("h2", "Jak usunąć kamień kotłowy?"),
     ("ul", ["Chemiczne odkamienianie dobranym preparatem",
             "Płukanie i pasywacja powierzchni",
             "Wdrożenie kondycjonowania, by kamień nie wracał"]),
     ("note", "Information gain: w realizacji Fako po wdrożeniu programu KCAQUA cykl czyszczenia wydłużył się z 3 do 12 miesięcy (dane przykładowe).")],
    [("Jak często należy odkamieniać kocioł?", "Zależy od jakości wody i obciążenia. Przy prawidłowym kondycjonowaniu potrzeba czyszczeń wyraźnie maleje."),
     ("Czy można kondycjonować wodę bez wyłączania kotła?", "Tak, samo kondycjonowanie prowadzimy w trakcie pracy. Odkamienianie planujemy zależnie od stanu układu.")],
    [("Odkamienianie kotłów parowych", "/kotly-parowe/odkamienianie/"),
     ("Kondycjonowanie wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
     ("Case study: kocioł Fako", "/case-study/kociol-parowy-fako/")],
    image="/assets/blog/blog-boiler-scale.png",
    image_alt="Kotłownia przemysłowa z rurociągami i instalacją parową",
    image_caption="Kamień kotłowy ogranicza wymianę ciepła i podnosi koszt pracy kotła.")

PAGES["/baza-wiedzy/pojedynczy-wpis-blogowy-2/"] = _post(
    "Biofilm to warstwa mikroorganizmów na powierzchniach układu chłodniczego. Pogarsza wymianę ciepła, sprzyja korozji i bywa siedliskiem bakterii.",
    [("h2", "Dlaczego biofilm jest groźny?"),
     ("p", "Biofilm izoluje powierzchnie wymiany ciepła i chroni mikroorganizmy przed działaniem chemii. Może też sprzyjać rozwojowi bakterii Legionella."),
     ("h2", "Jak usunąć i kontrolować biofilm?"),
     ("ul", ["Dozowanie biocydów (np. w ramach programu KCAQUA 305)",
             "Kontrola parametrów obiegu i przewodności",
             "Okresowe czyszczenie układu"])],
    [("Jak chronić wieżę przed Legionellą?", "Przez konsekwentną kontrolę biofilmu, biocydy i monitoring parametrów wody w obiegu.")],
    [("Ochrona wież chłodniczych", "/uklady-chlodnicze/ochrona-wiez-chlodniczych/"),
     ("Odkamienianie układów chłodniczych", "/uklady-chlodnicze/odkamienianie/")],
    image="/assets/blog/blog-biofilm-cleaning.png",
    image_alt="Technik czyszczący wymiennik w przemysłowym układzie chłodniczym",
    image_caption="Biofilm obniża sprawność wymiany ciepła i wymaga regularnej kontroli programu chemicznego.")

PAGES["/baza-wiedzy/pojedynczy-wpis-blogowy-3/"] = _post(
    "Antyskalant to preparat zapobiegający wytrącaniu soli na membranach odwróconej osmozy. Chroni membrany przed kamieniem i wydłuża ich żywotność.",
    [("h2", "Jak działa antyskalant?"),
     ("p", "Antyskalant utrzymuje sole twardości w roztworze, zapobiegając ich krystalizacji na powierzchni membrany i spadkowi wydajności stacji RO."),
     ("h2", "Dlaczego chlor i chlorki są groźne dla membran?"),
     ("p", "Degradują strukturę membrany. Dlatego ważna jest ich kontrola — nasz preparat potrafi wiązać te gazy.")],
    [("Jak dobrać antyskalant do mojej wody?", "Na podstawie analizy wody surowej i parametrów pracy stacji RO. Najlepiej zacząć od badania wody.")],
    [("Membrany RO — oferta", "/membrany-ro/"),
     ("Analiza wody", "/uslugi/analiza-wody/")],
    image="/assets/blog/blog-ro-antiscalant.png",
    image_alt="Przemysłowa stacja odwróconej osmozy z membranami i armaturą",
    image_caption="Antyskalant chroni membrany RO przed krystalizacją soli i spadkiem wydajności.")

# ================================================================== KONTAKT
PAGES["/kontakt/"] = {"sections": [
    hero(lead="Masz problem z twardą wodą lub kamieniem w instalacji? Skontaktuj się z inżynierami Kabi-Chemie — znajdziemy oszczędności dla Twojego zakładu.",
         ctas=[("Zadzwoń", "tel:" + SITE["phone_raw"]), ("Bezpłatna konsultacja", "/bezplatna-konsultacja/")]),
    contact(),
    std_cta(),
]}

# ================================================================== STRONY INFORMACYJNE
PAGES["/polityka-prywatnosci/"] = {"sections": [
    hero(h1="Polityka prywatności", lead="Zasady przetwarzania danych osobowych w serwisie kondycjonowanie-wody.pl."),
    richtext(blocks=[
        ("note", "To wzorcowa treść do uzupełnienia przez firmę / dział prawny o realne dane administratora, podstawy prawne i okresy przechowywania."),
        ("h2", "Administrator danych"),
        ("p", "Administratorem danych jest WELDCUT, Żabokliki-Kolonia ul. Stocka 10, 08-110 Siedlce, NIP: 8212519774. Kontakt: info@kondycjonowanie-wody.pl, +48 662 792 875."),
        ("h2", "Zakres i cel przetwarzania"),
        ("p", "Dane podane w formularzu kontaktowym przetwarzamy wyłącznie w celu obsługi zapytania i kontaktu zwrotnego."),
        ("h2", "Pliki cookies"),
        ("p", "Serwis może używać plików cookies w celach technicznych i statystycznych."),
        ("h2", "Twoje prawa"),
        ("p", "Masz prawo dostępu do danych, ich sprostowania, usunięcia oraz ograniczenia przetwarzania."),
    ]),
]}

PAGES["/warunki-wspolpracy/"] = {"sections": [
    hero(h1="Warunki współpracy", lead="Ogólne zasady współpracy i realizacji usług Kabi-Chemie."),
    richtext(blocks=[
        ("note", "Treść wzorcowa do uzupełnienia o realny regulamin / warunki handlowe."),
        ("h2", "Zakres usług"),
        ("p", "Świadczymy usługi kondycjonowania wody, odkamieniania, ochrony antykorozyjnej oraz serwisu urządzeń uzdatniania."),
        ("h2", "Konsultacja i audyt"),
        ("p", "Wstępna konsultacja i podstawowy audyt są bezpłatne i nie zobowiązują do dalszej współpracy."),
        ("h2", "Realizacja i rozliczenia"),
        ("p", "Szczegóły zakresu, harmonogramu i wynagrodzenia ustalamy indywidualnie w ofercie."),
    ]),
]}

PAGES["/warunki-wspolpracy/"] = {"sections": [
    hero(h1="Model współpracy z Kabi-Chemie",
         lead="Pracujemy etapowo: najpierw diagnozujemy instalację, potem określamy potencjał oszczędności, wdrażamy technologię KCAQUA i raportujemy realne efekty.",
         ctas=[("Umów badanie wody", "/kontakt/"), ("Bezpłatna konsultacja", "/bezplatna-konsultacja/")]),
    steps("Jak pracujemy", [
        ("Bezpłatny audyt techniczny", "Analizujemy parametry instalacji, zużycie wody, energii oraz aktualnie stosowany program chemiczny."),
        ("Ocena potencjału oszczędności", "Określamy, czy technologia KCAQUA może przynieść wymierne korzyści dla zakładu."),
        ("Wdrożenie technologii KCAQUA", "Uruchamiamy program chemiczny i konfigurujemy parametry prowadzenia instalacji."),
        ("Monitoring i nadzór", "Regularnie kontrolujemy parametry pracy instalacji i stabilność efektów."),
        ("Raportowanie efektów", "Pokazujemy rzeczywiste oszczędności wody, energii i kosztów."),
        ("Długoterminowa współpraca", "Dbamy o utrzymanie osiągniętych rezultatów i dalszą optymalizację."),
    ], intro="Model jest zaprojektowany tak, aby kierownik techniczny i zarząd widzieli nie tylko działania, ale też wynik biznesowy."),
    richtext(title="Co dostajesz po audycie", blocks=[
        ("ul", [
            "wstępną ocenę potencjału oszczędności",
            "informację, czy instalacja kwalifikuje się do wdrożenia technologii KCAQUA",
            "wskazanie najważniejszych obszarów strat wody i energii",
            "rekomendacje dalszych działań",
            "odpowiedzi na pytania techniczne dotyczące eksploatacji instalacji",
        ]),
        ("note", "Jeżeli uznamy, że nie jesteśmy w stanie osiągnąć wymiernych korzyści dla Twojej instalacji, powiemy o tym wprost."),
    ]),
    std_cta("Umów badanie wody w Twoim zakładzie",
            "Rozmowa z inżynierem pozwoli szybko ocenić, czy w instalacji istnieje realny potencjał oszczędności."),
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
