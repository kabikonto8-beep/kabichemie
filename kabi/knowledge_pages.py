# -*- coding: utf-8 -*-
"""Baza wiedzy KABI CHEMIE — jedno źródło prawdy, gotowe pod backend/CMS.

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

import content_source

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


def cat_path(cat):
    return f"{ROOT}{cat['slug']}/"


def articles_of(cat):
    """Artykuły przypisane do kategorii, w kolejności z bazy."""
    return [a for a in ARTICLES if a.get("category") == cat["slug"]]


def empty_category_redirects():
    """Kategorie bez artykułów → przekierowanie na hub.

    Pusta strona kategorii to cienka treść, której nie chcemy w indeksie.
    Reguła działa w obie strony automatycznie: gdy kategoria dostanie pierwszy
    artykuł, przekierowanie znika i powstaje pełna strona; gdy straci ostatni,
    wraca przekierowanie. Dzięki temu adres nigdy nie zwraca 404.
    """
    return {cat_path(c): ROOT for c in CATEGORIES if not articles_of(c)}


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


def _hub_hero(image, kicker, h1, lead, facts, primary, secondary):
    """Hero huba korzysta z tego samego układu co indeks case studies."""
    icons = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3C9 7.1 6.5 9.9 6.5 13.3a5.5 5.5 0 0 0 11 0C17.5 9.9 15 7.1 12 3Z"/><path d="M9.5 15.2c.8 1.2 2 1.8 3.4 1.5"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5-5l2.1 2.1-2.8 2.8-2.1-2.1a4 4 0 0 0 5 5l7.4 7.4a2.1 2.1 0 0 1-3 3l-7.4-7.4"/><path d="m5 19 3.5-3.5"/></svg>',
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19V5"/><path d="M4 19h16"/><path d="m7 15 4-4 3 3 5-6"/><path d="M16 8h3v3"/></svg>',
    )
    scope = _join(
        '<li><span class="case-index-hero__scope-icon" aria-hidden="true">'
        f'{icons[index]}</span><span>{value}</span></li>'
        for index, (_, value) in enumerate(facts)
    )
    return f"""
<section class="company-hero company-hero--knowledge case-index-hero knowledge-hero knowledge-hero--hub knowledge-index-hero" id="top" style="--company-image:url('{image}'); --company-position:center center">
  <div class="company-hero__media" aria-hidden="true"></div>
  <div class="company-hero__shade" aria-hidden="true"></div>
  <div class="wrap company-hero__inner">
    <div class="company-hero__copy">
      <p class="company-kicker"><span></span>{kicker}</p>
      <h1>{h1}</h1>
      <p class="company-hero__lead">{lead}</p>
      <div class="company-hero__actions">
        <a class="btn btn-primary" href="{primary[1]}">{primary[0]}</a>
        <a class="company-text-link" href="{secondary[1]}">{secondary[0]} <span aria-hidden="true">↗</span></a>
      </div>
      <ul class="case-index-hero__scope knowledge-index-hero__scope" aria-label="Zakres bazy wiedzy">{scope}</ul>
    </div>
  </div>
  <a class="company-hero__scroll" href="{primary[1]}"><span>{primary[0]}</span><i aria-hidden="true"></i></a>
</section>"""


def _hero(image, kicker, h1, lead, facts, primary, secondary, hub=False):
    """Pełnoekranowe, redakcyjne hero stron bazy wiedzy."""
    if hub:
        return _hub_hero(image, kicker, h1, lead, facts, primary, secondary)

    panel = _join(
        f"<div><span>{label}</span><strong>{value}</strong></div>"
        for label, value in facts
    )
    return f"""
<section class="solution-hero knowledge-hero" style="--solution-image:url('{image}'); --solution-position:center center" id="top">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner solution-hero__inner--editorial">
    <div class="solution-hero__copy reveal-left">
      <p class="firm-kicker">{kicker}</p>
      <h1>{h1}</h1>
      <p>{lead}</p>
      <div class="firm-actions">
        <a class="btn btn-primary" href="{primary[1]}">{primary[0]}</a>
        <a class="btn btn-ghost-light" href="{secondary[1]}">{secondary[0]}</a>
      </div>
    </div>
    <aside class="solution-hero__panel knowledge-hero__panel reveal-right">{panel}</aside>
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
        '<p>Bezpłatna konsultacja techniczna z inżynierem KABI CHEMIE, bez zobowiązań.</p></div>'
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


def render_category(cat):
    """Strona kategorii: hero z arkusza SEO + lista artykułów tej kategorii.

    Układ celowo powtarza hub — kategoria jest jego zawężeniem, nie osobnym
    gatunkiem strony. Artykuły linkują pod płaskie adresy ``/baza-wiedzy/{wpis}/``,
    więc włączenie kategorii nie zmienia adresów istniejących wpisów.
    """
    items = articles_of(cat)
    hero = _hero(
        cat["image"], cat["kicker"], cat["h1"], cat["lead"], cat["facts"],
        ("Czytaj artykuły", "#artykuly"), ("Zapytaj eksperta", "/kontakt/"),
    )
    stories = stories_section(
        items,
        [cat["stream_title"]],
        cat["lead"],
        section_id="artykuly",
        kicker=cat["title"],
    )
    return hero + stories + _related(cat["related"]) + _consult_final()


def render_article(a):
    # Artykuł może przynieść własny HTML całej treści — wtedy nie składamy
    # układu z pól, tylko wstawiamy go w całości. Nagłówek, stopka i sekcja
    # <head> nadal pochodzą z build.py, więc strona zostaje częścią serwisu.
    wlasny = (a.get("html") or "").strip()
    if wlasny:
        return wlasny

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


# ============================================= DANE: hub, kategorie, artykuly
# Zrodlem prawdy jest content/snapshot.json — generowany z Postgresa przez
# builder/export_snapshot.py. Wczesniej dane byly literalami w tym pliku
# (HUB, CATEGORIES, ARTICLES oraz generator artykulow testowych).
HUB = content_source.hub()
CATEGORIES = content_source.categories()
ARTICLES = content_source.articles()


def install_knowledge_pages(pages, custom, short):
    """Moduł jest właścicielem całej przestrzeni /baza-wiedzy/.

    Generujemy hub, strony kategorii ``/baza-wiedzy/{kategoria}/`` oraz płaskie
    wpisy ``/baza-wiedzy/{wpis}/``. Adresy artykułów pozostają płaskie — kategoria
    jest widokiem zbiorczym, nie warstwą w adresie. Usuwa wcześniejsze (statyczne)
    definicje z tej przestrzeni. `short` (C.SHORT) uzupełniamy o etykiety
    do breadcrumbów.
    """
    valid = ({ROOT}
             | {art_path(a) for a in ARTICLES}
             | {cat_path(c) for c in CATEGORIES})
    for p in [p for p in pages if p.startswith(ROOT) and p not in valid]:
        del pages[p]

    pages[ROOT] = {
        "body_class": BODY_CLASS,
        "sections": [custom(render_hub())],
    }

    puste = []
    for c in CATEGORIES:
        path = cat_path(c)
        if not articles_of(c):
            # Bez artykułów nie budujemy strony — build.py zrobi z tego
            # przekierowanie na hub (patrz empty_category_redirects()).
            puste.append(c["slug"])
            continue
        pages[path] = {
            "title": c["title"],
            "meta": c["lead"],
            "h1": c["h1"],
            "og_image": c["image"],
            "body_class": BODY_CLASS,
            "sections": [custom(render_category(c))],
        }
        short[path] = c["title"]
    if puste:
        print("Kategorie bez artykulow -> przekierowanie na hub: %s"
              % ", ".join(puste))
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
