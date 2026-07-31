# -*- coding: utf-8 -*-
"""Baza wiedzy Kabi-Chemie — jedno źródło prawdy, gotowe pod backend/CMS.

Kategorie zlikwidowano: artykuły są na pierwszym planie, pod płaskimi adresami.
Cała sekcja `/baza-wiedzy/` generuje się z jednej listy danych:

    ARTICLES    — wpisy; każdy ma własny ``slug`` i ``image``

Adresy (płaskie, bez warstwy kategorii):

    /baza-wiedzy/                → hub (lista wszystkich artykułów)
    /baza-wiedzy/{wpis}/         → artykuł

Dodanie wpisu = dopisanie jednego słownika. Artykuły są też prezentowane na
stronie głównej (sekcja „Baza wiedzy", wzorem case studies). Stare adresy
kategorii i zagnieżdżonych wpisów przekierowuje 301 (REDIRECTS w build.py).
Wygląd jest wspólny ze stronami rozwiązań (komponenty solution-*).
"""

BODY_CLASS = "has-dark-hero firm-page solution-page knowledge-page"
ROOT = "/baza-wiedzy/"


def _join(items):
    return "".join(items)


def _faq_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


# ---------------------------------------------------------------- ścieżki (URL)
def art_path(art):
    return f"{ROOT}{art['slug']}/"


def art_image(a):
    """Grafika wpisu (własna, z fallbackiem na grafikę bazy wiedzy)."""
    return a.get("image") or HUB["image"]


# ---------------------------------------------------------------- komponenty
_PHONE_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 '
    '19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 '
    '1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 '
    '1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/></svg>'
)


def _hero(image, kicker, h1, lead, facts, primary, secondary, hub=False):
    """Pełnoekranowe, redakcyjne hero (jak na stronach rozwiązań)."""
    panel = _join(
        f"<div><span>{label}</span><strong>{value}</strong></div>"
        for label, value in facts
    )
    hero_class = " knowledge-hero--hub" if hub else ""
    facts_inline = ""
    side_panel = f'<aside class="solution-hero__panel knowledge-hero__panel reveal-right">{panel}</aside>'
    if hub:
        facts_inline = '<ul class="knowledge-hero__facts" aria-label="Zakres bazy wiedzy">' + _join(
            f'<li><img src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true"><strong>{value}</strong></li>'
            for _, value in facts
        ) + '</ul>'
        side_panel = ""
    return f"""
<section class="solution-hero knowledge-hero{hero_class}" style="--solution-image:url('{image}'); --solution-position:center center" id="top">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner solution-hero__inner--editorial">
    <div class="solution-hero__copy reveal-left">
      <p class="firm-kicker">{kicker}</p>
      <h1>{h1}</h1>
      <p>{lead}</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="{primary[1]}">{primary[0]}</a>
        <a class="{'knowledge-hero__link' if hub else 'btn btn-ghost-light'}" href="{secondary[1]}">{secondary[0]}{' <span aria-hidden="true">↗</span>' if hub else ''}</a>
      </div>
      {facts_inline}
    </div>
    {side_panel}
  </div>
</section>"""


def _related(items):
    links = _join(
        f'<a href="{href}"><span>{eyebrow}</span><strong>{title}</strong>'
        f'<i aria-hidden="true">↗</i></a>'
        for eyebrow, title, href in items
    )
    return (
        '<nav class="solution-related" aria-label="Powiązane strony"><div class="wrap">'
        '<p>Powiązane strony</p>'
        f'<div class="solution-related__links">{links}</div></div></nav>'
    )


def _faq(items,
         title="Najczęstsze pytania",
         intro="Krótkie odpowiedzi na pytania, które najczęściej pojawiają się przy tym temacie."):
    details = _join(
        f'<details{" open" if i == 0 else ""}><summary><span>{q}</span>'
        f'<i aria-hidden="true"></i></summary>'
        f'<div class="solution-faq__answer"><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(items)
    )
    return (
        '<section class="solution-faq" id="faq"><div class="wrap solution-faq__grid">'
        '<header class="solution-faq__intro reveal-left">'
        '<p class="solution-kicker"><span></span>FAQ</p>'
        f'<h2>{title}</h2><p>{intro}</p></header>'
        f'<div class="solution-faq__list">{details}</div></div></section>'
    )


def _cta():
    return (
        '<section class="solution-cta"><span class="solution-cta__mark" aria-hidden="true"></span>'
        '<div class="wrap solution-cta__inner"><div>'
        '<p class="solution-kicker"><span></span>Następny krok</p>'
        '<h2>Sprawdź, ile zaoszczędzi Twój zakład.</h2>'
        '<p>Bezpłatna konsultacja techniczna z inżynierem Kabi-Chemie, bez zobowiązań.</p></div>'
        '<div class="solution-cta__actions">'
        '<a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów bezpłatną konsultację</a>'
        f'<a class="solution-phone-link" href="tel:+48662792875">{_PHONE_SVG}'
        '<span>Zadzwoń: +48 662 792 875</span></a>'
        '</div></div></section>'
    )


def _stream_row(art, label):
    return (
        f'<a class="reveal" href="{art_path(art)}"><img src="{art_image(art)}" alt="" width="160" height="104" loading="lazy">'
        f'<span>{label}</span><strong>{art["excerpt"]}</strong></a>'
    )


def _consult_final():
    return (
        '<section class="solution-cta"><span class="solution-cta__mark" aria-hidden="true"></span>'
        '<div class="wrap solution-cta__inner"><div>'
        '<p class="solution-kicker"><span></span>Nie widzisz swojego problemu?</p>'
        '<h2>Opisz instalację. Podpowiemy pierwszy temat.</h2>'
        '<p>Możemy wskazać artykuł, zaproponować analizę wody albo umówić krótką rozmowę z inżynierem.</p></div>'
        '<div class="solution-cta__actions">'
        '<a class="btn btn-primary" href="/kontakt/">Zapytaj eksperta</a>'
        f'<a class="solution-phone-link" href="tel:+48662792875">{_PHONE_SVG}'
        '<span>Zadzwoń: +48 662 792 875</span></a>'
        '</div></div></section>'
    )


# ---------------------------------------------------------------- render stron
def stories_section(items, h2_spans, intro, section_id="artykuly",
                    kicker="Baza wiedzy", bg_word="WIEDZA"):
    """Redakcyjna lista artykułów (układ wspólny z indeksem case studies).

    Duży nagłówek po lewej + lista wierszy po prawej: etykieta, tytuł, strzałka.
    Znak wodny + sygnet spinają sekcję wizualnie z sekcjami strony głównej
    (Branże, Proces…). Wygląd: komponent ``.company-stories``.
    """
    rows = _join(
        f'<a class="reveal" href="{art_path(a)}">'
        f'<span>{a.get("topic", "Baza wiedzy")}</span>'
        f'<strong>{a.get("list_title", a["title"])}</strong>'
        f'<i aria-hidden="true">↗</i></a>'
        for a in items
    )
    heads = _join(f"<span>{s}</span>" for s in h2_spans)
    return f"""
<section class="company-stories" id="{section_id}">
  <span class="section-bg-word section-bg-word--dark" aria-hidden="true">{bg_word}</span>
  <img class="section-bg-logo section-bg-logo--dark" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap company-stories__grid">
    <header class="company-stories__intro reveal-left">
      <p class="company-kicker"><span></span>{kicker}</p>
      <h2>{heads}</h2>
      <p>{intro}</p>
      <div class="stories-search">
        <label class="stories-search__field">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
          <input type="search" class="stories-search__input" placeholder="Szukaj po tytule lub kategorii…" aria-label="Szukaj po tytule lub kategorii" data-stories-search>
        </label>
      </div>
    </header>
    <div class="company-stories__list">{rows}
      <p class="stories-search__empty" data-stories-empty hidden>Brak artykułów zawierających podaną frazę.</p>
      <nav class="stories-pager" data-stories-pager aria-label="Strony bazy wiedzy" hidden></nav>
    </div>
  </div>
</section>"""


def render_hub():
    hero = _hero(
        HUB["image"], HUB["kicker"], HUB["h1"], HUB["lead"], HUB["facts"],
        ("Czytaj artykuły", "#artykuly"), ("Zapytaj eksperta", "/kontakt/"), hub=True,
    )
    stories = stories_section(
        ARTICLES,
        ["Wiedza z prawdziwych", "instalacji."],
        "Każdy artykuł pokazuje konkretny problem instalacji, jego przyczyny "
        "i działania, które realnie obniżają koszty codziennej pracy.",
        section_id="artykuly", kicker="Artykuły",
    )
    return hero + stories + _consult_final()


def render_article(a):
    facts = [
        ("Czas czytania", a["read"]),
        ("Dla kogo", a.get("audience", "Utrzymanie ruchu i decyzje techniczne.")),
        ("Kolejny krok", "Umów konsultację techniczną."),
    ]
    hero = _hero(
        art_image(a), "Baza wiedzy", a["title"], a["lead"], facts,
        ("Umów konsultację", "/bezplatna-konsultacja/"),
        ("Wróć do bazy wiedzy", ROOT),
    )
    body = (
        '<section class="section knowledge-article reveal">'
        f'<div class="wrap narrow prose">{a["prose"]}</div></section>'
    )
    return hero + body + _related(a["related"]) + _faq(a["faq"]) + _cta()


# ================================================================== DANE: HUB
HUB = {
    "image": "/assets/blog/blog-baza-wiedzy.jpg",
    "kicker": "Baza wiedzy Kabi-Chemie",
    "h1": "Praktyczna wiedza o wodzie przemysłowej.",
    "lead": "Artykuły o kamieniu, korozji, biofilmie, membranach RO i parametrach wody. Konkretne przyczyny, pomiary i działania dla zakładu przemysłowego.",
    "facts": [
        ("Tematy", "Kotły, chłodnictwo, RO i korozja"),
        ("Dla kogo", "Technika i utrzymanie ruchu"),
        ("Cel", "Decyzje oparte na danych"),
    ],
}


# ================================================================== KATEGORIE
CATEGORIES = [
    {
        "slug": "kotly-parowe",
        "title": "Kotły parowe i para",
        "kicker": "Baza wiedzy · Kotły parowe",
        "h1": "Kotły parowe i para wodna - Artykuły eksperckie",
        "lead": "Wszystko o kondycjonowaniu wody w kotłach parowych, jak zapobiegać awariom, usuwać kamień i oszczędzać paliwo.",
        "hub_blurb": "kamień, kondensat, odsalanie i ochrona przed korozją.",
        "stream_title": "Kamień, para i stabilna praca kotłowni.",
        "image": "/assets/blog/blog-kotly-parowe.jpg",
        "facts": [
            ("Zakres", "Kamień, kondensat, odsalanie i ochrona kotła."),
            ("Dla kogo", "Kotłownie, utrzymanie ruchu i energetyka zakładowa."),
            ("Następny krok", "Umów konsultację techniczną."),
        ],
        "related": [
            ("Rozwiązania", "Kotły parowe", "/kotly-parowe/"),
            ("Baza wiedzy", "Parametry wody", "/baza-wiedzy/parametry-wody/"),
            ("Case study", "Kocioł parowy Fako", "/case-study/kociol-parowy-fako/"),
        ],
    },
    {
        "slug": "wieze-chlodnicze",
        "title": "Wieże chłodnicze i skraplacze",
        "kicker": "Baza wiedzy · Wieże chłodnicze",
        "h1": "Wieże chłodnicze i obiegi chłodzące - Baza wiedzy",
        "lead": "Optymalizacja pracy wież chłodniczych i obiegów, biofilm, biocydy i usuwanie kamienia ze skraplaczy.",
        "hub_blurb": "biofilm, biocydy, odkamienianie i zużycie wody.",
        "stream_title": "Czysty obieg i stabilne chłodzenie.",
        "image": "/assets/blog/blog-wieze-chlodnicze.jpg",
        "facts": [
            ("Zakres", "Biofilm, biocydy, odkamienianie i zużycie wody."),
            ("Dla kogo", "Chłodnictwo przemysłowe i utrzymanie ruchu."),
            ("Następny krok", "Umów konsultację techniczną."),
        ],
        "related": [
            ("Rozwiązania", "Układy chłodnicze", "/uklady-chlodnicze/"),
            ("Rozwiązania", "Skraplacze amoniakalne", "/uklady-chlodnicze/skraplacze-amoniakalne/"),
            ("Baza wiedzy", "Korozja i ochrona", "/baza-wiedzy/korozja/"),
        ],
    },
    {
        "slug": "korozja",
        "title": "Korozja i ochrona metalu",
        "kicker": "Baza wiedzy · Korozja i ochrona",
        "h1": "Korozja w instalacjach przemysłowych - Zapobieganie",
        "lead": "Jak chronić instalacje przemysłowe przed korozją, inhibitory, pasywacja stali i rodzaje korozji.",
        "hub_blurb": "inhibitory, pasywacja, rodzaje korozji i objawy w instalacji.",
        "stream_title": "Objawy, przyczyny i ochrona metalu.",
        "image": "/assets/blog/blog-korozja.jpg",
        "facts": [
            ("Zakres", "Inhibitory, pasywacja i rodzaje korozji."),
            ("Dla kogo", "Utrzymanie ruchu i służby techniczne."),
            ("Następny krok", "Umów konsultację techniczną."),
        ],
        "related": [
            ("Rozwiązania", "Ochrona antykorozyjna", "/ochrona-antykorozyjna/"),
            ("Rozwiązania", "Pasywacja stali", "/ochrona-antykorozyjna/pasywacja-stali/"),
            ("Baza wiedzy", "Kotły parowe", "/baza-wiedzy/kotly-parowe/"),
        ],
    },
    {
        "slug": "parametry-wody",
        "title": "Parametry wody i oszczędności",
        "kicker": "Baza wiedzy · Parametry wody",
        "h1": "Przewodność i pH wody przemysłowej - Poradniki",
        "lead": "Zrozum parametry wody w przemyśle, wpływ pH, twardości i przewodności na pracę kotłów i układów chłodniczych.",
        "hub_blurb": "pH, przewodność, twardość, TDS, ścieki i energia.",
        "stream_title": "Parametry, które decydują o kosztach.",
        "image": "/assets/blog/blog-parametry-wody.jpg",
        "facts": [
            ("Zakres", "pH, przewodność, twardość, TDS i odsalanie."),
            ("Dla kogo", "Technolodzy i utrzymanie ruchu."),
            ("Następny krok", "Umów analizę wody."),
        ],
        "related": [
            ("Usługi", "Analiza wody", "/uslugi/analiza-wody/"),
            ("Rozwiązania", "Kondycjonowanie wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
            ("Baza wiedzy", "Kotły parowe", "/baza-wiedzy/kotly-parowe/"),
        ],
    },
    {
        "slug": "membrany-ro",
        "title": "Membrany RO",
        "kicker": "Baza wiedzy · Membrany RO",
        "h1": "Membrany RO pod kontrolą.",
        "lead": "Jak chronić membrany przed osadem i foulingiem, utrzymać stabilny odzysk oraz planować CIP na podstawie danych z instalacji.",
        "hub_blurb": "antyskalanty, fouling, płukanie i ochrona wydajności.",
        "stream_title": "Ochrona membran i stabilny odzysk.",
        "image": "/assets/blog/blog-membrany-ro-v2.webp",
        "facts": [
            ("Zakres", "Antyskalanty, fouling, płukanie i wydajność."),
            ("Dla kogo", "Operatorzy stacji RO i utrzymanie ruchu."),
            ("Następny krok", "Umów konsultację techniczną."),
        ],
        "related": [
            ("Rozwiązania", "Membrany RO", "/membrany-ro/"),
            ("Usługi", "Analiza wody", "/uslugi/analiza-wody/"),
            ("Baza wiedzy", "Parametry wody", "/baza-wiedzy/parametry-wody/"),
        ],
    },
]


# ================================================================== WPISY
ARTICLES = [
    {
        "slug": "kamien-kotlowy",
        "category": "kotly-parowe",
        "image": "/assets/blog/blog-boiler-scale.png",
        "short": "Kamień kotłowy",
        "topic": "Kotły parowe",
        "list_title": "Kamień kotłowy: jak cienki osad podnosi koszty pracy kotła.",
        "title": "Co to jest kamień kotłowy i dlaczego niszczy kotły parowe?",
        "excerpt": "mechanizm powstawania kamienia i jego wpływ na koszty pracy kotła.",
        "lead": "Kamień kotłowy to osad soli twardości na gorących powierzchniach kotła. Działa jak izolator, podnosi zużycie paliwa i grozi przegrzaniem rur.",
        "read": "8 min",
        "audience": "Utrzymanie ruchu i decyzje techniczne.",
        "feature_stats": [
            ("+10%", "więcej paliwa już przy 1 mm kamienia"),
            ("3 → 12 mies.", "dłuższy cykl między czyszczeniami (Fako)"),
        ],
        "prose": (
            "<h2>Jak powstaje kamień kotłowy?</h2>"
            "<p>Podgrzewana woda traci zdolność utrzymania rozpuszczonych soli wapnia i magnezu. "
            "Wytrącają się one na najgorętszych powierzchniach, tworząc twardą skorupę.</p>"
            "<h2>Jak kamień wpływa na rachunki za paliwo?</h2>"
            "<p>Już <strong>1 mm kamienia</strong> może zwiększyć zużycie paliwa o około 10%, "
            "bo ciepło trudniej przenika do wody.</p>"
            "<h2>Jak usunąć kamień kotłowy?</h2>"
            "<ul><li>Chemiczne odkamienianie dobranym preparatem</li>"
            "<li>Płukanie i pasywacja powierzchni</li>"
            "<li>Wdrożenie kondycjonowania, by kamień nie wracał</li></ul>"
            "<p class=\"note\">Information gain: w realizacji Fako po wdrożeniu programu KCAQUA "
            "cykl czyszczenia wydłużył się z 3 do 12 miesięcy (dane przykładowe).</p>"
        ),
        "faq": [
            ("Jak często należy odkamieniać kocioł?",
             "Zależy od jakości wody, obciążenia i historii osadów. Przy prawidłowym kondycjonowaniu potrzeba czyszczeń wyraźnie maleje."),
            ("Czy można kondycjonować wodę bez wyłączania kotła?",
             "Tak, samo kondycjonowanie prowadzimy w trakcie pracy. Odkamienianie planujemy zależnie od stanu układu."),
            ("Po czym poznać, że w kotle narasta kamień?",
             "Typowe objawy to rosnące zużycie paliwa, gorsza wymiana ciepła, częstsze alarmy, osady w wodzie i problemy z utrzymaniem stabilnych parametrów."),
            ("Czy 1 mm kamienia naprawdę ma znaczenie?",
             "Tak. Nawet cienka warstwa osadu działa jak izolacja cieplna. Kocioł musi zużyć więcej paliwa, aby przekazać tę samą ilość energii do wody."),
            ("Jak zapobiec powrotowi kamienia po czyszczeniu?",
             "Po odkamienianiu warto wdrożyć stałą kontrolę twardości, przewodności i pH oraz dobrać program KCAQUA do pracy konkretnej kotłowni."),
        ],
        "related": [
            ("Rozwiązania", "Odkamienianie kotłów parowych", "/kotly-parowe/odkamienianie/"),
            ("Rozwiązania", "Kondycjonowanie wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
            ("Case study", "Kocioł parowy Fako", "/case-study/kociol-parowy-fako/"),
        ],
    },
    {
        "slug": "biofilm-w-ukladzie-chlodniczym",
        "category": "wieze-chlodnicze",
        "image": "/assets/blog/blog-biofilm-cleaning.png",
        "short": "Biofilm w układzie chłodniczym",
        "topic": "Chłodnictwo przemysłowe",
        "list_title": "Biofilm w układzie chłodniczym: jak rozpoznać i usunąć osady.",
        "title": "Biofilm w układzie chłodniczym: jak rozpoznać i usunąć osady?",
        "excerpt": "jak rozpoznać problem, zanim spadnie sprawność skraplacza.",
        "lead": "Biofilm to warstwa mikroorganizmów na powierzchniach układu chłodniczego. Pogarsza wymianę ciepła, sprzyja korozji i bywa siedliskiem bakterii.",
        "read": "7 min",
        "audience": "Utrzymanie ruchu i chłodnictwo przemysłowe.",
        "prose": (
            "<h2>Dlaczego biofilm jest groźny?</h2>"
            "<p>Biofilm izoluje powierzchnie wymiany ciepła i chroni mikroorganizmy przed działaniem chemii. "
            "Może też sprzyjać rozwojowi bakterii Legionella.</p>"
            "<h2>Jak usunąć i kontrolować biofilm?</h2>"
            "<ul><li>Dozowanie biocydów (np. w ramach programu KCAQUA 305)</li>"
            "<li>Kontrola parametrów obiegu i przewodności</li>"
            "<li>Okresowe czyszczenie układu</li></ul>"
        ),
        "faq": [
            ("Jak chronić wieżę przed Legionellą?",
             "Podstawą jest kontrola biofilmu, właściwy biocyd, regularny monitoring wody i utrzymanie czystości powierzchni kontaktu z wodą."),
            ("Czy sam biocyd wystarczy do usunięcia biofilmu?",
             "Nie zawsze. Biofilm może chronić mikroorganizmy przed chemią, dlatego często potrzebna jest korekta programu, czyszczenie i kontrola parametrów obiegu."),
            ("Jakie objawy wskazują na biofilm w układzie chłodniczym?",
             "Najczęściej widać spadek wydajności chłodzenia, śliski osad, wzrost zużycia wody, nieprzyjemny zapach i większą podatność instalacji na korozję."),
            ("Czy biofilm wpływa na koszty energii?",
             "Tak. Warstwa biologiczna pogarsza wymianę ciepła, więc układ musi pracować ciężej, aby utrzymać wymaganą temperaturę procesu."),
            ("Jak często trzeba kontrolować wodę w wieży chłodniczej?",
             "Częstotliwość zależy od obciążenia i jakości wody. W praktyce warto kontrolować przewodność, pH, biologię i skuteczność programu chemicznego w stałym harmonogramie."),
        ],
        "related": [
            ("Rozwiązania", "Ochrona wież chłodniczych", "/uklady-chlodnicze/ochrona-wiez-chlodniczych/"),
            ("Rozwiązania", "Odkamienianie układów chłodniczych", "/uklady-chlodnicze/odkamienianie/"),
            ("Case study", "Skraplacz BAC + KCAQUA 305", "/case-study/skraplacz-bac-kcaqua/"),
        ],
    },
    {
        "slug": "antyskalant-ro",
        "category": "membrany-ro",
        "image": "/assets/blog/blog-ro-antiscalant.png",
        "short": "Antyskalant do membran RO",
        "topic": "Membrany RO",
        "list_title": "Antyskalant RO: kiedy naprawdę chroni membranę.",
        "title": "Antyskalant do membran RO: kiedy naprawdę chroni membranę?",
        "excerpt": "kiedy realnie chroni membranę, a kiedy maskuje problem z jakością wody.",
        "lead": "Antyskalant to preparat zapobiegający wytrącaniu soli na membranach odwróconej osmozy. Chroni membrany przed kamieniem i wydłuża ich żywotność.",
        "read": "6 min",
        "audience": "Operatorzy stacji RO i utrzymanie ruchu.",
        "prose": (
            "<h2>Jak działa antyskalant?</h2>"
            "<p>Antyskalant utrzymuje sole twardości w roztworze, zapobiegając ich krystalizacji "
            "na powierzchni membrany i spadkowi wydajności stacji RO.</p>"
            "<h2>Dlaczego chlor i chlorki są groźne dla membran?</h2>"
            "<p>Degradują strukturę membrany. Dlatego ważna jest ich kontrola, "
            "nasz preparat potrafi wiązać te gazy.</p>"
        ),
        "faq": [
            ("Jak dobrać antyskalant do mojej wody?",
             "Na podstawie analizy wody surowej, odzysku instalacji RO i parametrów pracy membran. Najlepiej zacząć od badania wody."),
            ("Po czym poznać, że membrany RO są zagrożone osadem?",
             "Sygnałem jest spadek wydajności, wzrost różnicy ciśnień, pogorszenie jakości permeatu i częstsza potrzeba płukania chemicznego."),
            ("Czy antyskalant zastępuje prawidłową filtrację wstępną?",
             "Nie. Antyskalant chroni przed wytrącaniem soli, ale filtracja, kontrola żelaza, chloru i zawiesiny nadal są kluczowe dla żywotności membran."),
            ("Jak często trzeba kontrolować dawkę antyskalantu?",
             "Dawkę warto weryfikować przy zmianie jakości wody, odzysku, przepływu lub ciśnienia. Stała kontrola ogranicza ryzyko przewymiarowania i niedozowania."),
            ("Czy pomagacie dobrać chemię do istniejącej stacji RO?",
             "Tak. Analizujemy wodę, parametry pracy i historię awarii. Na tej podstawie dobieramy antyskalant oraz zalecenia dla obsługi stacji."),
        ],
        "related": [
            ("Rozwiązania", "Membrany RO", "/membrany-ro/"),
            ("Usługi", "Analiza wody", "/uslugi/analiza-wody/"),
            ("Baza wiedzy", "Więcej artykułów", "/baza-wiedzy/"),
        ],
    },
]


# ================================================================== ARTYKUŁY TESTOWE
# Placeholder do testów listy i wyszukiwarki. Aby je usunąć: skasuj ten blok
# (ARTICLES wróci do realnych wpisów).
_TEST_IMAGES = {
    "Kotły parowe": "/assets/blog/blog-kotly-parowe.jpg",
    "Chłodnictwo przemysłowe": "/assets/blog/blog-wieze-chlodnicze.jpg",
    "Membrany RO": "/assets/blog/blog-membrany-ro-v2.webp",
    "Korozja i ochrona": "/assets/blog/blog-korozja.jpg",
    "Parametry wody": "/assets/blog/blog-parametry-wody.jpg",
}

_TEST_SEED = [
    ("Kotły parowe", "Odsalanie kotła: jak ustawić cykle koncentracji."),
    ("Kotły parowe", "Odmulanie i odszlamianie: praktyczny harmonogram."),
    ("Kotły parowe", "Korozja kondensatu i aminy neutralizujące."),
    ("Kotły parowe", "Tlen w wodzie zasilającej i odgazowanie termiczne."),
    ("Chłodnictwo przemysłowe", "Cykle zagęszczania w wieży chłodniczej."),
    ("Chłodnictwo przemysłowe", "Legionella w obiegu: kontrola i dezynfekcja."),
    ("Chłodnictwo przemysłowe", "Biocydy utleniające i nieutleniające."),
    ("Chłodnictwo przemysłowe", "Biała rdza na ocynku skraplacza wyparnego."),
    ("Membrany RO", "Fouling organiczny membran i płukanie CIP."),
    ("Membrany RO", "Indeks SDI a praca stacji RO."),
    ("Membrany RO", "Krzemionka na membranach i granice odzysku."),
    ("Membrany RO", "Dobór antyskalantu do wody twardej."),
    ("Korozja i ochrona", "Korozja wżerowa stali w instalacjach."),
    ("Korozja i ochrona", "Pasywacja stali po montażu i spawaniu."),
    ("Korozja i ochrona", "Warstwa magnetytu jako ochrona kotła."),
    ("Korozja i ochrona", "Inhibitory filmujące a anodowe."),
    ("Parametry wody", "Twardość ogólna, węglanowa i niewęglanowa."),
    ("Parametry wody", "Przewodność jako wskaźnik zasolenia wody."),
    ("Parametry wody", "pH i zasadowość w wodzie technologicznej."),
    ("Parametry wody", "TDS a koszty ścieków i odsalania."),
]


def _make_test_article(i, topic, title):
    return {
        "slug": f"artykul-testowy-{i:02d}",
        "image": _TEST_IMAGES.get(topic, HUB["image"]),
        "short": f"Test {i:02d}",
        "topic": topic,
        "list_title": title,
        "title": title,
        "lead": (f"Artykuł testowy {i:02d} ({topic}). Treść przykładowa (placeholder) do "
                 "testów listy i wyszukiwarki w bazie wiedzy — do zastąpienia realnym materiałem."),
        "read": "5 min",
        "audience": "Materiał testowy (placeholder).",
        "prose": (
            "<h2>Wprowadzenie</h2>"
            f"<p>To jest artykuł testowy z obszaru „{topic}”. Treść ma charakter przykładowy "
            "i służy do sprawdzenia układu listy, stron artykułów oraz wyszukiwarki w bazie wiedzy.</p>"
            "<h2>Zakres</h2>"
            f"<p><strong>{title}</strong> Poniższy tekst jest wypełnieniem (placeholder) "
            "i należy go zastąpić realną treścią przed publikacją.</p>"
            "<ul><li>Punkt testowy 1</li><li>Punkt testowy 2</li><li>Punkt testowy 3</li></ul>"
        ),
        "faq": [
            ("Czego dotyczy ten artykuł?",
             f"To materiał testowy dotyczący tematu: {title} Treść jest przykładowa i służy do testów bazy wiedzy."),
            ("Czy mogę uzyskać konsultację techniczną?",
             "Tak. Umów bezpłatną konsultację z inżynierem Kabi-Chemie, aby omówić swoją instalację."),
        ],
        "related": [
            ("Baza wiedzy", "Więcej artykułów", ROOT),
            ("Usługi", "Analiza wody", "/uslugi/analiza-wody/"),
            ("Konsultacja", "Umów bezpłatną konsultację", "/bezplatna-konsultacja/"),
        ],
    }


ARTICLES = ARTICLES + [_make_test_article(i, t, ti) for i, (t, ti) in enumerate(_TEST_SEED, 1)]


def install_knowledge_pages(pages, custom, short):
    """Moduł jest właścicielem całej przestrzeni /baza-wiedzy/.

    Kategorie nie istnieją: generujemy hub oraz płaskie wpisy
    ``/baza-wiedzy/{wpis}/``. Usuwa wcześniejsze (statyczne) definicje z tej
    przestrzeni. `short` (C.SHORT) uzupełniamy o etykiety do breadcrumbów.
    """
    valid = {ROOT} | {art_path(a) for a in ARTICLES}
    for p in [p for p in pages if p.startswith(ROOT) and p not in valid]:
        del pages[p]

    pages[ROOT] = {
        "body_class": BODY_CLASS,
        "sections": [custom(render_hub())],
    }
    for a in ARTICLES:
        path = art_path(a)
        pages[path] = {
            "title": a["title"],
            "meta": a["lead"],
            "h1": a["title"],
            "og_type": "article",
            "og_image": art_image(a),
            "body_class": BODY_CLASS,
            "jsonld": [_faq_schema(a["faq"])],
            "sections": [custom(render_article(a))],
        }
        short[path] = a["short"]
