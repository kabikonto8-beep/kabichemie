# -*- coding: utf-8 -*-
"""Spójny system podstron rozwiązań Kabi-Chemie."""


def _join(items):
    return "".join(items)


# width/height w markupie: ikona zostaje mała nawet zanim zadziała CSS.
_SVG = ('<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{}</svg>')

# Ikony sygnałów w hero. Ten sam rysunek co glify sekcyjne: 24x24, obrys 1.7.
HERO_ICONS = {
    # kotły parowe
    "feedwater": _SVG.format('<path d="M12 2.8S5.5 10.1 5.5 15a6.5 6.5 0 0 0 13 0C18.5 10.1 12 2.8 12 2.8Z"/>'
                             '<path d="M6 16.5c2 0 2-1.4 4-1.4s2 1.4 4 1.4 2-1.4 4-1.4"/>'),
    "steam": _SVG.format('<rect x="5" y="9" width="14" height="12" rx="3"/><circle cx="12" cy="14" r="2.4"/>'
                         '<path d="M8 18.5h8"/><path d="M9 6.5c0-1.6 1.6-1.6 1.6-3.2M14 6.5c0-1.6 1.6-1.6 1.6-3.2"/>'),
    "dosing": _SVG.format('<path d="M3 8h9"/><path d="m9 5 3 3-3 3"/>'
                          '<path d="M17 3s-4 4.8-4 8a4 4 0 0 0 8 0c0-3.2-4-8-4-8Z"/><path d="M8 17h12M8 21h8"/>'),
    # układy chłodnicze
    "condenser": _SVG.format('<rect x="3" y="5" width="18" height="14" rx="2"/>'
                             '<path d="M7 5v14M11 5v14M15 5v14"/><path d="M3 9.5h18M3 14.5h18"/>'),
    "ammonia": _SVG.format('<path d="M19 8a7.5 7.5 0 0 0-13-2L4 8"/><path d="M4 4v4h4"/>'
                           '<path d="M5 16a7.5 7.5 0 0 0 13 2l2-2"/><path d="M20 20v-4h-4"/>'
                           '<path d="M12 9.5v5M9.8 10.8l4.4 2.4M14.2 10.8l-4.4 2.4"/>'),
    "tower": _SVG.format('<path d="M6.5 3h11l-2.2 7.5c-.4 1.3-.4 2.7 0 4L17.5 21h-11l2.2-6.5c.4-1.3.4-2.7 0-4L6.5 3Z"/>'
                         '<path d="M8.6 10.5h6.8"/><path d="M4 21h16"/>'),
    # ochrona antykorozyjna
    "steel": _SVG.format('<path d="m12 3 9 4.5-9 4.5-9-4.5L12 3Z"/><path d="m3 12 9 4.5 9-4.5"/>'
                         '<path d="m3 16.5 9 4.5 9-4.5"/>'),
    "circuit": _SVG.format('<path d="M4 4v5a4 4 0 0 0 4 4h8a4 4 0 0 1 4 4v3"/><path d="M2 4h4M18 20h4"/>'
                           '<path d="M8 10v6M5 13h6"/>'),
    "passivation": _SVG.format('<path d="M12 3 4.5 6v5.2c0 4.6 2.9 8.1 7.5 9.8 4.6-1.7 7.5-5.2 7.5-9.8V6L12 3Z"/>'
                               '<path d="m8.3 12.2 2.3 2.3 5.2-5.2"/>'),
    # białe certyfikaty
    "qualify": _SVG.format('<path d="M8 4h8a2 2 0 0 1 2 2v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V6a2 2 0 0 1 2-2Z"/>'
                           '<path d="M9.5 2.8h5v3h-5z"/><path d="m9 13 1.8 1.8L15 10.6"/><path d="M9 17.5h6"/>'),
    "energy": _SVG.format('<path d="M4 4v16h16"/><path d="m7.5 15 3.5-4 2.5 2 5-6"/>'
                          '<path d="M15.5 7h3v3"/><path d="M12.6 3.2 10 7h3l-2.6 3.8"/>'),
    "utility_meter": _SVG.format('<rect x="3.5" y="5" width="17" height="14" rx="2.5"/>'
                                  '<path d="M7.5 14a4.8 4.8 0 0 1 9 0"/><path d="m12 14 3-3.4"/>'
                                  '<circle cx="12" cy="14" r="1" fill="currentColor" stroke="none"/>'
                                  '<path d="M7.5 18.8v2M16.5 18.8v2"/>'),
    "docs": _SVG.format('<path d="M8 3h6l4 4v12a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Z"/>'
                        '<path d="M14 3v4h4"/><path d="M10 12h6M10 15.5h6"/>'),
    # usługi: analiza wody i audyt
    "uptime": _SVG.format('<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/><path d="M12 7.5v5l3.5 2"/>'),
    "diagnose": _SVG.format('<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4A2 2 0 0 0 19 18l-5-9V3"/>'
                            '<path d="M7.5 16h9"/><path d="m9.4 12.8 1.6 1.2 2.2-2 2 1.3"/>'),
    "report": _SVG.format('<path d="M7 3h10v18H7z"/><path d="M9.5 7h5M9.5 11h5M9.5 15h2.5"/>'
                          '<path d="m13.6 16.1 1.2 1.2 2.3-2.5"/>'),
    "survey": _SVG.format('<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/>'
                          '<path d="M8 10.5h5M10.5 8v5"/>'),
    "scope": _SVG.format('<path d="M4 6h16M4 12h16M4 18h9"/><circle cx="8" cy="6" r="1.6"/>'
                         '<circle cx="15" cy="12" r="1.6"/><circle cx="6.5" cy="18" r="1.6"/>'),
    "priority": _SVG.format('<path d="M4 20V9M10 20V4M16 20v-7M22 20H2"/>'
                            '<path d="M4 9 10 4l6 9 6-6"/>'),
    # dodatkowe glify do sekcji parametrów (data)
    "bio": _SVG.format('<circle cx="12" cy="12" r="3.2"/><circle cx="5" cy="6" r="1.4"/>'
                       '<circle cx="19" cy="7" r="1.4"/><circle cx="18" cy="18" r="1.4"/><circle cx="5.5" cy="18" r="1.4"/>'
                       '<path d="m7 7 2.4 2.4M16.4 8.4 14.4 10M15 14.4l2 2.2M9.3 14.6 7 16.8"/>'),
    "crystal": _SVG.format('<path d="m12 3 5 3v6l-5 3-5-3V6l5-3Z"/><path d="M12 3v18M7 6l10 6M17 6 7 12"/>'),
    "salt": _SVG.format('<path d="M12 3v18"/><circle cx="5" cy="7" r="1.4"/><circle cx="7.5" cy="13" r="1.4"/>'
                        '<circle cx="4.5" cy="18" r="1.4"/><circle cx="18.5" cy="9" r="1.4"/>'
                        '<path d="M9.6 6.6h2.4M9.6 13h2.4M9.6 18h2.4"/>'),
    "gauge": _SVG.format('<path d="M4 18a8 8 0 1 1 16 0"/><path d="m12 14 4-4"/><path d="M7 20h10"/>'
                         '<path d="M5.5 14H7M17 14h1.5M12 8v1.5"/>'),
    "calendar": _SVG.format('<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M16 3v4M8 3v4M3.5 10h17"/>'
                            '<path d="M8 14h3M13.5 14h3M8 17.5h3"/>'),
}


def _hero_signal(item):
    """Sygnał hero: krotka (ikona, etykieta) rysuje glif, sam tekst zostaje przy kropce."""
    if isinstance(item, (tuple, list)):
        icon, label = item
        return (f'<li class="has-icon"><span class="solution-hero__signal-icon" aria-hidden="true">'
                f'{HERO_ICONS[icon]}</span><span>{label}</span></li>')
    return f"<li>{item}</li>"


def _faq_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in items
        ],
    }


def _render_kcaqua(config):
    principle_icons = {
        "sample": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M14.4 2v6.5L20 18a2 2 0 0 1-1.7 3H5.7A2 2 0 0 1 4 18l5.6-9.5V2"/><path d="M8.5 2h7"/><path d="M7 16h10"/></svg>',
        "settings": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 4h-7M10 4H3M21 12h-9M8 12H3M21 20h-5M12 20H3"/><circle cx="12" cy="4" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="14" cy="20" r="2"/></svg>',
        "load": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20.7 18a9 9 0 1 0-17.4 0"/><path d="M12 13l4-4"/><path d="M12 18v.01"/></svg>',
        "trend": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 3v17h17"/><path d="m7 15 4-4 3 3 6-7"/><path d="M16 7h4v4"/></svg>',
    }
    principles = [
        ("sample", "Rozpoznanie wody i instalacji", "Łączymy wyniki badań z obciążeniem kotła, udziałem kondensatu i sposobem uzdatniania."),
        ("settings", "Dobór funkcji programu", "Ustalamy ochronę przed osadem i korozją oraz wartości docelowe dla konkretnej kotłowni."),
        ("load", "Dozowanie zgodne z pracą", "Dawka może podążać za przepływem wody lub zmianą obciążenia, zamiast pozostawać stała."),
        ("trend", "Kontrola trendów i korekt", "Oceniamy kierunek zmian, zużycie mediów i efekt programu, a nie pojedynczy wynik bez kontekstu."),
    ]
    principle_rows = _join(
        f"""
        <article class="kcaqua-principle">
          <span class="kcaqua-glyph" aria-hidden="true">{principle_icons[icon]}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for icon, title, text in principles
    )

    program_steps = [
        ("Rozpoznajemy", "Charakterystyka wody", "Badamy wodę zasilającą, kotłową i kondensat oraz opisujemy zmienność pracy instalacji.", "Punkt odniesienia"),
        ("Projektujemy", "Matryca programu", "Dobieramy funkcje chemiczne, dawkę, wartości docelowe i sposób reakcji na odchylenia.", "Program i nastawy"),
        ("Uruchamiamy", "Układ dozowania", "Kalibrujemy pompy, sprawdzamy punkty wtrysku i łączymy dozowanie z właściwym sygnałem.", "Stabilna dawka"),
        ("Potwierdzamy", "Prowadzenie instalacji", "Porównujemy trendy parametrów, zużycie mediów i obserwacje eksploatacyjne.", "Raport i korekta"),
    ]
    program_rows = _join(
        f"""
        <li class="kcaqua-program__step">
          <span class="kcaqua-program__stage">{stage}</span>
          <div class="kcaqua-program__copy"><h3>{title}</h3><p>{text}</p></div>
          <strong class="kcaqua-program__result">{result}</strong>
        </li>"""
        for stage, title, text, result in program_steps
    )

    control_symbols = {
        "ph": "pH",
        "oxygen": "O₂",
        "water": """<svg viewBox="0 0 32 32" role="presentation">
          <path d="M16 2.5S6.5 12.8 6.5 19.5a9.5 9.5 0 0 0 19 0C25.5 12.8 16 2.5 16 2.5Z"/>
          <path d="M10 19.2c2 1.55 4 1.55 6 0s4-1.55 6 0"/>
          <path d="M11.2 23.5c1.6 1 3.2 1 4.8 0s3.2-1 4.8 0"/>
        </svg><small>Woda</small>""",
        "dose": """<svg viewBox="0 0 32 32" role="presentation">
          <path d="M2.5 12.5h13"/>
          <path d="m12 8.5 4 4-4 4"/>
          <path d="M23 4.5s-6.5 7.3-6.5 12.2a6.5 6.5 0 0 0 13 0C29.5 11.8 23 4.5 23 4.5Z"/>
          <path d="M20.1 18.8a3.2 3.2 0 0 0 2.9 1.7"/>
        </svg><small>Dawka</small>""",
    }
    controls = [
        ("ph", "Odczyn i ochrona metalu", "Pokazuje, czy warunki wspierają ochronę stali w kotle i obiegu kondensatu.", "ochrona powierzchni"),
        ("oxygen", "Tlen i kondensat", "Pomaga ocenić pracę odgazowania oraz ryzyko korozji w całym obiegu parowym.", "trwałość instalacji"),
        ("water", "Przewodność i odsalanie", "Pozwala utrzymać jakość wody kotłowej bez niepotrzebnej utraty gorącej wody.", "woda i energia"),
        ("dose", "Przepływ i dawka", "Łączy zużycie wody z rzeczywistą ilością preparatu podawaną do instalacji.", "stabilność programu"),
    ]
    control_rows = _join(
        f"""
        <article class="kcaqua-control__row">
          <span class="kcaqua-control__symbol{' kcaqua-control__symbol--icon' if symbol in ('water', 'dose') else ''}" aria-hidden="true">{control_symbols[symbol]}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
          <span class="kcaqua-control__effect">{effect}</span>
        </article>"""
        for symbol, title, text, effect in controls
    )

    outcomes = [
        ("Powtarzalne parametry", "Obsługa pracuje według jasnych wartości docelowych i reakcji na odchylenia."),
        ("Dawka adekwatna do pracy", "Dozowanie odpowiada aktualnemu przepływowi i obciążeniu instalacji."),
        ("Mniej działań interwencyjnych", "Zmiany są widoczne w trendach, zanim przerodzą się w kosztowny problem."),
        ("Czytelny raport", "Wyniki techniczne łączymy z wpływem programu na wodę, energię i eksploatację."),
    ]
    outcome_rows = _join(
        f"""
        <article class="kcaqua-proof__outcome">
          <img src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for title, text in outcomes
    )

    related = _join(
        f"""
        <a href="{href}">
          <span>{label}</span>
          <strong>{title}</strong>
          <i aria-hidden="true">↗</i>
        </a>"""
        for label, title, href in config["related"]
    )

    faqs = _join(
        f"""
        <details{' open' if index == 1 else ''}>
          <summary><span>{question}</span><i aria-hidden="true"></i></summary>
          <div class="solution-faq__answer"><p>{answer}</p></div>
        </details>"""
        for index, (question, answer) in enumerate(config["faq"])
    )

    signals = _join(
        f'<li><img src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true"><span>{signal}</span></li>'
        for signal in config["signals"]
    )

    return f"""
<section class="solution-hero kcaqua-hero" id="top" style="--solution-image:url('{config['image']}'); --solution-position:{config.get('image_position', 'center center')}">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner">
    <div class="solution-hero__copy">
      <p class="solution-kicker"><span></span>{config['kicker']}</p>
      <h1>{config['h1_html']}</h1>
      <p class="solution-hero__lead">{config['lead']}</p>
      <div class="solution-hero__actions">
        <a class="btn btn-primary" href="{config['primary_href']}">{config['primary_label']}</a>
        <a class="solution-text-link" href="{config['secondary_href']}">{config['secondary_label']} <span aria-hidden="true">↗</span></a>
      </div>
      <ul class="solution-hero__signals" aria-label="Najważniejsze elementy programu">{signals}</ul>
    </div>
  </div>
</section>

<section class="kcaqua-section kcaqua-intro" id="technologia">
  <img class="kcaqua-engraving kcaqua-engraving--light" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap kcaqua-intro__grid">
    <header class="kcaqua-section__intro reveal-left">
      <p class="solution-kicker solution-kicker--dark"><span></span>System KCAQUA</p>
      <h2>Preparat jest elementem.<br>Program tworzy wynik.</h2>
      <p>KCAQUA łączy analizę wody, funkcje chemiczne, automatykę dozowania i nadzór inżynierski. Każda warstwa programu odpowiada za inny fragment stabilnej pracy kotłowni.</p>
    </header>
    <div class="kcaqua-principles" data-reveal-loop>{principle_rows}</div>
  </div>
</section>

<section class="kcaqua-section kcaqua-program" id="program">
  <img class="kcaqua-engraving kcaqua-engraving--dark" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap kcaqua-program__grid">
    <header class="kcaqua-section__intro kcaqua-section__intro--dark reveal-left">
      <p class="solution-kicker"><span></span>Jak prowadzimy program</p>
      <h2>Od punktu wyjścia do stabilnej pracy.</h2>
      <p>Najpierw porządkujemy dane. Potem projektujemy program, uruchamiamy dozowanie i potwierdzamy efekt na podstawie trendów.</p>
    </header>
    <div class="kcaqua-program__flow reveal-right">
      <p class="kcaqua-program__edge"><span>Wejście</span><strong>Próbka wody i dane procesowe</strong></p>
      <ol class="kcaqua-program__steps" data-reveal-loop>{program_rows}</ol>
      <p class="kcaqua-program__edge kcaqua-program__edge--result"><span>Wynik</span><strong>Parametry, raport i plan dalszego prowadzenia</strong></p>
    </div>
  </div>
</section>

<section class="kcaqua-section kcaqua-control" id="pomiary">
  <div class="wrap">
    <header class="kcaqua-control__head reveal">
      <div>
        <p class="solution-kicker solution-kicker--dark"><span></span>Punkty kontrolne</p>
        <h2>Pomiary pokazują, kiedy skorygować program.</h2>
      </div>
      <p>Nie mnożymy parametrów bez potrzeby. Wybieramy te, które pomagają podejmować decyzje o dawce, odsalaniu i ochronie instalacji.</p>
    </header>
    <div class="kcaqua-control__rows" data-reveal-loop>{control_rows}</div>
  </div>
</section>

<section class="kcaqua-section kcaqua-proof" id="efekty">
  <div class="kcaqua-proof__media" aria-hidden="true"></div>
  <div class="kcaqua-proof__shade" aria-hidden="true"></div>
  <img class="kcaqua-engraving kcaqua-engraving--proof" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap kcaqua-proof__inner">
    <header class="kcaqua-proof__copy reveal-left">
      <p class="solution-kicker"><span></span>Efekt w instalacji</p>
      <h2>Program ma być widoczny w pracy kotłowni.</h2>
      <p>Skuteczność potwierdzamy wynikami wody, dozowaniem, zużyciem mediów oraz obserwacjami z eksploatacji. Dzięki temu wiadomo, co działa i kiedy potrzebna jest korekta.</p>
      <a class="solution-text-link" href="/case-study/kociol-parowy-fako/">Zobacz wdrożenie w kotłowni Fako <span aria-hidden="true">↗</span></a>
    </header>
    <div class="kcaqua-proof__outcomes" data-reveal-loop>{outcome_rows}</div>
  </div>
</section>

<nav class="solution-related kcaqua-related" aria-label="Powiązane rozwiązania">
  <div class="wrap">
    <p>Powiązane rozwiązania</p>
    <div class="solution-related__links">{related}</div>
  </div>
</nav>

<section class="solution-section solution-faq kcaqua-faq" id="faq">
  <div class="wrap solution-faq__grid">
    <header class="solution-faq__intro reveal-left">
      <p class="solution-kicker"><span></span>FAQ</p>
      <h2>{config['faq_title']}</h2>
      <p>{config['faq_intro']}</p>
    </header>
    <div class="solution-faq__list">{faqs}</div>
  </div>
</section>

<section class="solution-cta kcaqua-cta">
  <img class="kcaqua-engraving kcaqua-engraving--cta" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap solution-cta__inner">
    <div>
      <p class="solution-kicker"><span></span>{config['cta_kicker']}</p>
      <h2>{config['cta_title']}</h2>
      <p>{config['cta_text']}</p>
    </div>
    <div class="solution-cta__actions">
      <a class="btn btn-primary" href="{config['cta_primary_href']}">{config['cta_primary_label']}</a>
      <a class="solution-phone-link" href="tel:+48662792875" aria-label="Zadzwoń do Kabi-Chemie: +48 662 792 875">
        <span class="solution-phone-link__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/></svg>
        </span>
        <span>Zadzwoń: +48 662 792 875</span>
      </a>
    </div>
  </div>
</section>
"""


def _render_ro(config):
    icons = {
        "water": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.8S5.5 10.1 5.5 15a6.5 6.5 0 0 0 13 0C18.5 10.1 12 2.8 12 2.8Z"/><path d="m9.2 15.2 1.8 1.8 4-4.2"/></svg>',
        "crystal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3 4.5 8.5 8 14h6l3.5-5.5L14 3H8Z"/><path d="m9 16-2 3 2 2h3l2-3-2-2H9Z"/><path d="m15.5 14.5 1.8 3 3.2-.2.8-2.3-2.2-2.3-3.6 1.8Z"/></svg>',
        "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5"/><path d="m3 16 9 5 9-5"/></svg>',
        "bio": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3.5"/><circle cx="5" cy="6" r="1.5"/><circle cx="19" cy="7" r="1.5"/><circle cx="18" cy="18" r="1.5"/><circle cx="5" cy="18" r="1.5"/><path d="m7 7.2 2.4 2.3M16.2 9.5l1.7-1.4M15 14.4l2 2M9.2 14.7l-2.8 2"/></svg>',
        "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4.5 6v5.2c0 4.6 2.9 8.1 7.5 9.8 4.6-1.7 7.5-5.2 7.5-9.8V6L12 3Z"/><path d="m8.5 15 7-7"/><path d="m8.5 9 6 6"/></svg>',
        "flow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h12"/><path d="m12 4 3 3-3 3"/><path d="M21 17H9"/><path d="m12 14-3 3 3 3"/><path d="M18 4v16"/></svg>',
        "salt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><circle cx="5" cy="7" r="1.4"/><circle cx="7" cy="13" r="1.4"/><circle cx="4" cy="18" r="1.4"/><circle cx="18" cy="10" r="1.4"/><path d="M9.5 6.5h2.5M9.5 13h2.5M9.5 18h2.5"/></svg>',
        "pressure": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 17a8 8 0 1 1 16 0"/><path d="m12 13 4-4"/><path d="M7 20h10"/><path d="M5.5 13H7M17 13h1.5M12 7v1.5"/></svg>',
        "recovery": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M19 8a7.5 7.5 0 0 0-13-2L4 8"/><path d="M4 4v4h4"/><path d="M5 16a7.5 7.5 0 0 0 13 2l2-2"/><path d="M20 20v-4h-4"/><path d="M12 7.5s-3 3.4-3 5.7a3 3 0 0 0 6 0c0-2.3-3-5.7-3-5.7Z"/></svg>',
        "flask": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4A2 2 0 0 0 19 18l-5-9V3"/><path d="M7.5 16h9"/></svg>',
        "projection": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4v16h16"/><path d="m6.5 14 4-3"/><path d="m10.5 11 8.5-3.5M10.5 11l8 3.2"/><path d="M14.5 8.9v-2h-2"/><circle cx="10.5" cy="11" r="1.1"/></svg>',
        "dose": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h9"/><path d="m9 5 3 3-3 3"/><path d="M17 3s-4 4.8-4 8a4 4 0 0 0 8 0c0-3.2-4-8-4-8Z"/><path d="M8 17h12M8 21h8"/></svg>',
        "trend": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 3v17h17"/><path d="m7 15 4-4 3 3 6-7"/><path d="M16 7h4v4"/></svg>',
        "clean": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3s-5 5.7-5 9.5a5 5 0 0 0 10 0C17 8.7 12 3 12 3Z"/><path d="M5 4v4M3 6h4M19 16v5M16.5 18.5h5"/></svg>',
    }

    hero_signals = [
        ("water", "Analiza wody i odzysku"),
        ("dose", "Dobór i kontrola dozowania"),
        ("trend", "Trendy wydajności membran"),
    ]
    hero_signal_rows = _join(
        f'<li><span class="ro-glyph" aria-hidden="true">{icons[icon]}</span><span>{label}</span></li>'
        for icon, label in hero_signals
    )

    diagnosis = [
        ("crystal", "Osad mineralny", "Sole wytrącające się w koncentracie ograniczają przepływ i zwiększają opór membran.", "Skład wody i odzysk"),
        ("layers", "Zanieczyszczenia organiczne i koloidalne", "Cząstki oraz związki organiczne odkładają się na powierzchni i skracają cykl między myciami.", "SDI i filtracja wstępna"),
        ("bio", "Biofilm", "Rozwój biologiczny podnosi różnicę ciśnień i powoduje coraz mniej stabilną pracę stacji.", "Mikrobiologia i postoje"),
        ("shield", "Utlenienie membrany", "Kontakt z chlorem lub innym utleniaczem może trwale obniżyć retencję soli.", "Chlor, ORP i retencja"),
    ]
    diagnosis_rows = _join(
        f"""
        <article class="ro-diagnosis__row">
          <span class="ro-glyph ro-glyph--large" aria-hidden="true">{icons[icon]}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
          <span class="ro-diagnosis__evidence">{evidence}</span>
        </article>"""
        for icon, title, text, evidence in diagnosis
    )

    signals = [
        ("flow", "Strumień permeatu", "Pokazuje, czy stacja utrzymuje ilość produkowanej wody po uwzględnieniu temperatury."),
        ("salt", "Retencja soli", "Pozwala ocenić jakość separacji i wychwycić pogorszenie pracy warstwy aktywnej."),
        ("pressure", "Różnica ciśnień", "Wzrost wskazuje, że kanały przepływowe stawiają coraz większy opór."),
        ("recovery", "Odzysk i zużycie", "Łączy bilans wody z dawką antyskalantu i rzeczywistym obciążeniem instalacji."),
    ]
    signal_rows = _join(
        f"""
        <article class="ro-signal">
          <span class="ro-glyph ro-glyph--signal" aria-hidden="true">{icons[icon]}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for icon, title, text in signals
    )

    program = [
        ("flask", "Analiza zasilania", "Badamy skład wody, temperaturę i ryzyko wytrącania przy planowanym odzysku.", "Punkt odniesienia"),
        ("projection", "Projekcja ryzyka", "Sprawdzamy, gdzie kończy się bezpieczny zakres pracy i czego wymaga uzdatnianie wstępne.", "Zakres pracy"),
        ("dose", "Stabilne dozowanie", "Dobieramy preparat, dawkę, punkt wtrysku oraz sterowanie zgodne z przepływem.", "Nastawy i zabezpieczenia"),
        ("trend", "Monitoring trendów", "Porównujemy znormalizowane wyniki i reagujemy, zanim odchylenie stanie się przestojem.", "Decyzja i korekta"),
    ]
    program_rows = _join(
        f"""
        <article class="ro-program__step">
          <span class="ro-glyph ro-glyph--program" aria-hidden="true">{icons[icon]}</span>
          <div class="ro-program__copy"><h3>{title}</h3><p>{text}</p></div>
          <strong>{result}</strong>
        </article>"""
        for icon, title, text, result in program
    )

    cip_rows = [
        ("trend", "Trend potwierdza zmianę", "Decyzję opieramy na znormalizowanym przepływie, retencji soli i różnicy ciśnień."),
        ("layers", "Rozpoznajemy rodzaj osadu", "Skład zanieczyszczeń decyduje o kolejności, chemii i parametrach mycia."),
        ("clean", "Chronimy membranę podczas CIP", "Kontrolujemy pH, temperaturę, przepływ i czas kontaktu zgodnie z materiałem membrany."),
    ]
    cip_items = _join(
        f"""
        <article class="ro-cip__item">
          <span class="ro-glyph" aria-hidden="true">{icons[icon]}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for icon, title, text in cip_rows
    )

    outcomes = [
        ("Stabilniejsza produkcja permeatu", "Parametry pracy są porównywalne w czasie, więc odchylenia widać wcześniej."),
        ("Dłuższe cykle między myciami", "Prawidłowa ochrona ogranicza osad i niepotrzebne przestoje serwisowe."),
        ("Mniejsze zużycie energii", "Czystsze kanały przepływowe nie wymagają niepotrzebnego podnoszenia ciśnienia."),
        ("Lepsza ochrona inwestycji", "Kontrola utleniaczy, dozowania i CIP wspiera dłuższą eksploatację membran."),
    ]
    outcome_rows = _join(
        f"""
        <article class="ro-outcome">
          <img src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for title, text in outcomes
    )

    related = _join(
        f"""
        <a href="{href}">
          <span>{label}</span>
          <strong>{title}</strong>
          <i aria-hidden="true">↗</i>
        </a>"""
        for label, title, href in config["related"]
    )
    faqs = _join(
        f"""
        <details{' open' if index == 0 else ''}>
          <summary><span>{question}</span><i aria-hidden="true"></i></summary>
          <div class="solution-faq__answer"><p>{answer}</p></div>
        </details>"""
        for index, (question, answer) in enumerate(config["faq"])
    )

    return f"""
<section class="solution-hero ro-hero" id="top" style="--solution-image:url('{config['image']}'); --solution-position:{config.get('image_position', 'center center')}">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <img class="ro-engraving ro-engraving--hero" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap solution-hero__inner">
    <div class="solution-hero__copy">
      <p class="solution-kicker"><span></span>Rozwiązania / Membrany RO</p>
      <h1>Ochrona membran RO.<br>Wydajność pod kontrolą.</h1>
      <p class="solution-hero__lead">Łączymy analizę wody, dobór antyskalantu, dozowanie i trendy pracy stacji. Dzięki temu wiadomo, co ogranicza przepływ, kiedy reagować i czy mycie CIP jest rzeczywiście potrzebne.</p>
      <div class="solution-hero__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Omów pracę stacji RO</a>
        <a class="solution-text-link" href="#diagnoza">Zobacz, jak chronimy membrany <span aria-hidden="true">↓</span></a>
      </div>
      <ul class="solution-hero__signals ro-hero__signals" aria-label="Zakres ochrony membran">{hero_signal_rows}</ul>
    </div>
  </div>
</section>

<section class="ro-section ro-diagnosis" id="diagnoza">
  <img class="ro-engraving ro-engraving--diagnosis" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap ro-diagnosis__layout">
    <header class="ro-section__intro reveal-left">
      <p class="solution-kicker solution-kicker--dark"><span></span>Diagnoza przed korektą</p>
      <h2>Najpierw diagnoza.</h2>
      <p>Nie każda zmiana oznacza kamień. Zestawiamy wodę, parametry pracy i historię stacji, aby oddzielić osad mineralny, zanieczyszczenia, biofilm oraz uszkodzenie membrany.</p>
    </header>
    <div class="ro-diagnosis__rows" data-reveal-loop>{diagnosis_rows}</div>
  </div>
</section>

<section class="ro-section ro-signals" id="monitoring">
  <img class="ro-engraving ro-engraving--signals" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap">
    <header class="ro-signals__head reveal">
      <div>
        <p class="solution-kicker"><span></span>Obraz pracy stacji</p>
        <h2>Cztery sygnały mówią więcej niż pojedynczy odczyt.</h2>
      </div>
      <p>Normalizujemy wyniki względem temperatury i warunków zasilania. Dopiero wtedy można rzetelnie porównać pracę stacji w czasie.</p>
    </header>
    <div class="ro-signals__matrix" data-reveal-loop>{signal_rows}</div>
  </div>
</section>

<section class="ro-section ro-program" id="program">
  <div class="wrap ro-program__layout">
    <header class="ro-section__intro ro-program__intro reveal-left">
      <p class="solution-kicker solution-kicker--dark"><span></span>Program ochrony RO</p>
      <h2>Od składu wody do stabilnej pracy membran.</h2>
      <p>Preparat jest jednym z elementów. Skuteczny program łączy projekcję ryzyka, uzdatnianie wstępne, dozowanie i bieżącą ocenę trendów.</p>
      <a class="solution-inline-link" href="/baza-wiedzy/membrany-ro/">Poznaj zasady ochrony RO <span aria-hidden="true">↗</span></a>
    </header>
    <div class="ro-program__steps" data-reveal-loop>{program_rows}</div>
  </div>
</section>

<section class="ro-section ro-cip" id="cip">
  <div class="ro-cip__media" aria-hidden="true"></div>
  <div class="ro-cip__shade" aria-hidden="true"></div>
  <img class="ro-engraving ro-engraving--cip" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap ro-cip__layout">
    <header class="ro-cip__intro reveal-left">
      <p class="solution-kicker"><span></span>Decyzja o myciu</p>
      <h2>CIP wykonujemy wtedy, gdy wskazują na to dane.</h2>
      <p>Zbyt późne mycie może utrwalić osad. Zbyt częste niepotrzebnie obciąża membrany i produkcję. Najpierw ustalamy przyczynę spadku parametrów.</p>
      <strong class="ro-cip__note">Właściwa diagnoza decyduje o chemii i przebiegu mycia.</strong>
    </header>
    <div class="ro-cip__items" data-reveal-loop>{cip_items}</div>
  </div>
</section>

<section class="ro-section ro-outcomes" id="efekty">
  <div class="wrap ro-outcomes__layout">
    <header class="ro-section__intro reveal-left">
      <p class="solution-kicker solution-kicker--dark"><span></span>Efekt dla zakładu</p>
      <h2>Stabilna stacja RO pracuje przewidywalnie.</h2>
      <p>Program ochrony ma utrzymać parametry procesu, ograniczać nieplanowane interwencje i dawać zespołowi technicznemu jasną podstawę do decyzji.</p>
    </header>
    <div class="ro-outcomes__list" data-reveal-loop>{outcome_rows}</div>
  </div>
</section>

<nav class="solution-related ro-related" aria-label="Powiązane rozwiązania">
  <div class="wrap">
    <p>Powiązane rozwiązania</p>
    <div class="solution-related__links">{related}</div>
  </div>
</nav>

<section class="solution-section solution-faq ro-faq" id="faq">
  <div class="wrap solution-faq__grid">
    <header class="solution-faq__intro reveal-left">
      <p class="solution-kicker"><span></span>FAQ</p>
      <h2>Pytania o wydajność i ochronę membran RO.</h2>
      <p>Konkretne odpowiedzi o diagnozie, antyskalancie, monitoringu oraz właściwym momencie mycia CIP.</p>
    </header>
    <div class="solution-faq__list">{faqs}</div>
  </div>
</section>

<section class="solution-cta ro-cta">
  <img class="ro-engraving ro-engraving--cta" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap solution-cta__inner">
    <div>
      <p class="solution-kicker solution-kicker--dark"><span></span>Rozmowa o stacji RO</p>
      <h2>Sprawdźmy, co ogranicza wydajność membran.</h2>
      <p>Wystarczą podstawowe parametry i krótki opis trendu. Wspólnie ustalimy, jakie dane warto uzupełnić i jaki kolejny krok będzie najrozsądniejszy.</p>
    </div>
    <div class="solution-cta__actions">
      <a class="btn btn-primary" href="/bezplatna-konsultacja/">Umów konsultację RO</a>
      <a class="solution-phone-link" href="tel:+48662792875" aria-label="Zadzwoń do Kabi-Chemie: +48 662 792 875">
        <span class="solution-phone-link__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/></svg>
        </span>
        <span>Zadzwoń: +48 662 792 875</span>
      </a>
    </div>
  </div>
</section>
"""


def _render_descaling(config):
    icons = {
        "exchanger": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4v16M19 4v16"/><path d="M5 7h5c2 0 2 3 4 3h5M5 14h5c2 0 2 3 4 3h5"/><path d="m8 4 2 3-2 3M16 14l-2 3 2 3"/></svg>',
        "pipes": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4v5a4 4 0 0 0 4 4h8a4 4 0 0 1 4 4v3"/><path d="M2 4h4M18 20h4"/><path d="M8 10v6M5 13h6"/></svg>',
        "boiler": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="16" rx="3"/><circle cx="12" cy="10" r="2.5"/><path d="M8 15h8M8 18h3M13 18h3M9 4V2M15 4V2"/></svg>',
        "heat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M10 14.8V5a2 2 0 1 1 4 0v9.8a4.5 4.5 0 1 1-4 0Z"/><path d="M12 8v8"/><path d="M4 7h3M4 12h3M4 17h3"/></svg>',
        "flow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h13"/><path d="m13 5 3 3-3 3"/><path d="M21 16H8"/><path d="m11 13-3 3 3 3"/><circle cx="19" cy="8" r="2"/><circle cx="5" cy="16" r="2"/></svg>',
        "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4.5 6v5.2c0 4.6 2.9 8.1 7.5 9.8 4.6-1.7 7.5-5.2 7.5-9.8V6L12 3Z"/><path d="m8.3 12.2 2.3 2.3 5.2-5.2"/></svg>',
        "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.5 2"/><path d="M7 2.8 4.2 5.6M17 2.8l2.8 2.8"/></svg>',
        "flask": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4A2 2 0 0 0 19 18l-5-9V3"/><path d="M7.5 16h9"/><path d="m9.2 13 1.6 1.2 2.2-2 2 1.3"/></svg>',
        "isolate": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M2 13h5.5M16.5 13h5.5"/><circle cx="12" cy="13" r="4"/><path d="M12 9V5.5M9.5 5.5h5"/></svg>',
        "circulate": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M19 8a7.5 7.5 0 0 0-13-2L4 8"/><path d="M4 4v4h4"/><path d="M5 16a7.5 7.5 0 0 0 13 2l2-2"/><path d="M20 20v-4h-4"/><path d="M12 8s-2.5 2.8-2.5 4.8a2.5 2.5 0 0 0 5 0C14.5 10.8 12 8 12 8Z"/></svg>',
        "flush": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3s-5 5.7-5 9.5a5 5 0 0 0 10 0C17 8.7 12 3 12 3Z"/><path d="m9.3 13 1.8 1.8 3.8-4"/><path d="M4 19h4M16 19h4"/></svg>',
        "gauge": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 17a8 8 0 1 1 16 0"/><path d="m12 13 4-4"/><path d="M7 20h10"/><path d="M5.5 13H7M17 13h1.5M12 7v1.5"/></svg>',
        "sample": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3h8M9 3v5l-3.5 9.5A2.6 2.6 0 0 0 8 21h8a2.6 2.6 0 0 0 2.5-3.5L15 8V3"/><path d="M7.2 15h9.6"/><circle cx="10" cy="18" r=".7"/><circle cx="14" cy="17" r=".7"/></svg>',
        "report": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3h10v18H7z"/><path d="M9.5 7h5M9.5 11h5M9.5 15h2.5"/><path d="m13.5 16 1.2 1.2 2.3-2.5"/></svg>',
    }

    hero_signals = [
        ("exchanger", "Wymienniki i wężownice", "wymiana ciepła"),
        ("pipes", "Rurociągi i obiegi", "przepływ medium"),
        ("boiler", "Kotły i skraplacze", "sprawność procesu"),
    ]
    hero_signal_rows = _join(
        f'<li><span class="descale-glyph descale-glyph--hero" aria-hidden="true">{icons[icon]}</span><span><strong>{title}</strong><small>{note}</small></span></li>'
        for icon, title, note in hero_signals
    )

    diagnosis = [
        ("heat", "Spadek wymiany ciepła", "Ta sama produkcja wymaga wyższej temperatury lub większej ilości energii.", "temperatura i energia"),
        ("flow", "Rosnące opory przepływu", "Zwężony przekrój obciąża pompy i ogranicza dostępną wydajność urządzenia.", "ciśnienie i przepływ"),
        ("shield", "Korozja ukryta pod osadem", "Złogi odcinają metal od programu ochronnego i sprzyjają lokalnym uszkodzeniom.", "materiał i próbka"),
        ("clock", "Coraz częstsze postoje", "Powtarzające się czyszczenia awaryjne wskazują, że przyczyna osadu nie została usunięta.", "historia pracy"),
    ]
    diagnosis_rows = _join(
        f"""
        <article class="descale-diagnosis__row">
          <span class="descale-glyph descale-glyph--large" aria-hidden="true">{icons[icon]}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
          <span class="descale-diagnosis__evidence">{evidence}</span>
        </article>"""
        for icon, title, text, evidence in diagnosis
    )

    process = [
        ("flask", "Próba i dobór technologii", "Sprawdzamy rodzaj osadu, reakcję próbki i zgodność chemii z metalem oraz uszczelnieniami.", "Chemia i czas kontaktu"),
        ("isolate", "Przygotowanie obiegu", "Wyznaczamy kierunek cyrkulacji, punkty podłączenia i sposób bezpiecznego odseparowania urządzenia.", "Zakres i zabezpieczenia"),
        ("circulate", "Czyszczenie pod kontrolą", "Prowadzimy obieg, obserwując temperaturę, odczyn, przepływ i rzeczywisty przebieg reakcji.", "Parametry procesu"),
        ("flush", "Płukanie i powrót do pracy", "Neutralizujemy pozostałości, potwierdzamy parametry końcowe i przygotowujemy zalecenia po uruchomieniu.", "Gotowość instalacji"),
    ]
    process_rows = _join(
        f"""
        <article class="descale-process__step">
          <span class="descale-glyph descale-glyph--process" aria-hidden="true">{icons[icon]}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
          <strong>{result}</strong>
        </article>"""
        for icon, title, text, result in process
    )

    controls = [
        ("gauge", "Cyrkulacja i temperatura", "Utrzymujemy warunki, które pozwalają skutecznie usuwać osad bez niepotrzebnego obciążania materiału."),
        ("sample", "Odczyn i przebieg reakcji", "Pomiary pokazują, czy proces nadal pracuje, czy wymaga korekty albo przejścia do płukania."),
        ("report", "Parametry końcowe", "Kończymy po spełnieniu ustalonych kryteriów i dokumentujemy warunki bezpiecznego uruchomienia."),
    ]
    control_rows = _join(
        f"""
        <article class="descale-control__item">
          <span class="descale-glyph" aria-hidden="true">{icons[icon]}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for icon, title, text in controls
    )

    outcomes = [
        ("Lepszy bilans temperatur", "Oczyszczona powierzchnia ponownie skutecznie przekazuje ciepło między mediami."),
        ("Stabilniejszy przepływ", "Usunięcie złogów przywraca dostępny przekrój i odciąża układ cyrkulacyjny."),
        ("Mniej interwencji awaryjnych", "Zaplanowany proces ogranicza potrzebę reagowania dopiero po alarmie lub postoju."),
        ("Plan ochrony przed nawrotem", "Raport łączy przyczynę osadu z zaleceniami dotyczącymi wody, filtracji i kontroli."),
    ]
    outcome_rows = _join(
        f"""
        <article class="descale-outcome">
          <img src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for title, text in outcomes
    )

    scope = [
        ("exchanger", "Wymienniki płytowe i rurowe", "Dobieramy kierunek przepływu i parametry procesu do geometrii kanałów oraz materiału płyt lub rur."),
        ("pipes", "Rurociągi i obiegi technologiczne", "Oceniamy pojemność, dostępne króćce, możliwość cyrkulacji i bezpieczny odbiór roztworu po pracy."),
        ("boiler", "Kotły, skraplacze i wężownice", "Łączymy odkamienianie z oceną jakości wody, aby ograniczyć ponowne narastanie osadu."),
    ]
    scope_rows = _join(
        f"""
        <article class="descale-scope__item">
          <span class="descale-glyph descale-glyph--large" aria-hidden="true">{icons[icon]}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for icon, title, text in scope
    )

    related = _join(
        f"""
        <a href="{href}">
          <span>{label}</span>
          <strong>{title}</strong>
          <i aria-hidden="true">↗</i>
        </a>"""
        for label, title, href in config["related"]
    )
    faqs = _join(
        f"""
        <details{' open' if index == 0 else ''}>
          <summary><span>{question}</span><i aria-hidden="true"></i></summary>
          <div class="solution-faq__answer"><p>{answer}</p></div>
        </details>"""
        for index, (question, answer) in enumerate(config["faq"])
    )

    return f"""
<section class="solution-hero descale-hero" id="top" style="--solution-image:url('{config['image']}'); --solution-position:{config.get('image_position', 'center center')}">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <img class="descale-engraving descale-engraving--hero" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap solution-hero__inner">
    <div class="solution-hero__copy">
      <p class="solution-kicker"><span></span>Rozwiązania / Odkamienianie instalacji</p>
      <h1>Odkamienianie instalacji.<br>Sprawność odzyskana pod kontrolą.</h1>
      <p class="solution-hero__lead">Najpierw ustalamy, co osiadło i z jakim materiałem pracujemy. Następnie prowadzimy czyszczenie w obiegu zamkniętym, kontrolując reakcję aż do bezpiecznego uruchomienia instalacji.</p>
      <div class="solution-hero__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/#consult-form">Omów odkamienianie instalacji</a>
        <a class="solution-text-link" href="#proces">Zobacz przebieg prac <span aria-hidden="true">↓</span></a>
      </div>
      <ul class="solution-hero__signals descale-hero__signals" aria-label="Zakres odkamieniania">{hero_signal_rows}</ul>
    </div>
  </div>
</section>

<section class="descale-section descale-diagnosis" id="diagnoza">
  <img class="descale-engraving descale-engraving--diagnosis" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap descale-diagnosis__layout">
    <header class="descale-section__intro reveal-left">
      <p class="solution-kicker solution-kicker--dark"><span></span>Diagnoza przed chemią</p>
      <h2>Najpierw ustalamy, co naprawdę ogranicza instalację.</h2>
      <p>Kamień mineralny, produkty korozji, osad procesowy i biofilm wymagają innego podejścia. Łączymy objawy z próbką oraz warunkami pracy, zanim zaproponujemy technologię.</p>
    </header>
    <div class="descale-diagnosis__rows" data-reveal-loop>{diagnosis_rows}</div>
  </div>
</section>

<section class="descale-section descale-process" id="proces">
  <img class="descale-engraving descale-engraving--process" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap descale-process__layout">
    <header class="descale-section__intro descale-process__intro reveal-left">
      <p class="solution-kicker"><span></span>Obieg zamknięty</p>
      <h2>Proces przygotowany pod urządzenie, materiał i postój.</h2>
      <p>Każdy etap ma własny cel i kryterium zakończenia. Zespół zakładu wie, co robimy, jakie parametry obserwujemy i kiedy instalacja może bezpiecznie wrócić do pracy.</p>
      <strong class="descale-process__note">Wejście: próbka osadu, dane urządzenia i warunki procesu.</strong>
    </header>
    <div class="descale-process__steps" data-reveal-loop>{process_rows}</div>
  </div>
</section>

<section class="descale-section descale-control" id="kontrola">
  <div class="descale-control__media" aria-hidden="true"></div>
  <div class="descale-control__shade" aria-hidden="true"></div>
  <img class="descale-engraving descale-engraving--control" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap descale-control__layout">
    <header class="descale-control__intro reveal-left">
      <p class="solution-kicker"><span></span>Kontrola podczas prac</p>
      <h2>Widzimy, kiedy reakcja się kończy.</h2>
      <p>Nie kończymy procesu tylko dlatego, że upłynął założony czas. Decyzję opieramy na przebiegu reakcji i parametrach właściwych dla wybranej technologii.</p>
      <strong>Pomiar prowadzi proces od pierwszego obiegu do ostatniego płukania.</strong>
    </header>
    <div class="descale-control__items" data-reveal-loop>{control_rows}</div>
  </div>
</section>

<section class="descale-section descale-outcomes" id="efekty">
  <div class="wrap descale-outcomes__layout">
    <header class="descale-section__intro reveal-left">
      <p class="solution-kicker solution-kicker--dark"><span></span>Efekt po uruchomieniu</p>
      <h2>Rezultat potwierdzamy w pracy instalacji.</h2>
      <p>Czysta powierzchnia jest początkiem. Po uruchomieniu liczą się temperatura, przepływ, stabilność procesu oraz plan ograniczający ponowne narastanie osadu.</p>
      <a class="solution-inline-link" href="/kalkulator-oszczednosci/">Sprawdź potencjał odzyskania kosztów <span aria-hidden="true">↗</span></a>
    </header>
    <div class="descale-outcomes__list" data-reveal-loop>{outcome_rows}</div>
  </div>
</section>

<section class="descale-section descale-scope" id="zakres">
  <img class="descale-engraving descale-engraving--scope" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap">
    <header class="descale-scope__head reveal">
      <div>
        <p class="solution-kicker"><span></span>Zakres zastosowań</p>
        <h2>Technologia zależy od miejsca i materiału.</h2>
      </div>
      <p>Jeżeli osad nie jest kamieniem, zmieniamy technologię zamiast zwiększać agresywność chemii. Bezpieczeństwo materiału jest równie ważne jak szybkość czyszczenia.</p>
    </header>
    <div class="descale-scope__items" data-reveal-loop>{scope_rows}</div>
  </div>
</section>

<nav class="solution-related descale-related" aria-label="Powiązane rozwiązania">
  <div class="wrap">
    <p>Powiązane rozwiązania</p>
    <div class="solution-related__links">{related}</div>
  </div>
</nav>

<section class="solution-section solution-faq descale-faq" id="faq">
  <div class="wrap solution-faq__grid">
    <header class="solution-faq__intro reveal-left">
      <p class="solution-kicker"><span></span>FAQ</p>
      <h2>Przed odkamienianiem warto ustalić kilka konkretów.</h2>
      <p>O demontażu, doborze chemii, kontroli prac, neutralizacji i ograniczeniu ponownego narastania osadu.</p>
    </header>
    <div class="solution-faq__list">{faqs}</div>
  </div>
</section>

<section class="solution-cta descale-cta">
  <img class="descale-engraving descale-engraving--cta" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap solution-cta__inner">
    <div>
      <p class="solution-kicker solution-kicker--dark"><span></span>Ocena instalacji</p>
      <h2>Omówmy objawy i bezpieczny zakres czyszczenia.</h2>
      <p>Wystarczą zdjęcia, krótki opis urządzenia i podstawowe parametry. Ustalimy, czy potrzebna jest próbka osadu, wizyta techniczna czy przygotowanie procesu.</p>
    </div>
    <div class="solution-cta__actions">
      <a class="btn btn-primary" href="/kontakt/#kontakt-form">Wyślij zapytanie techniczne</a>
      <a class="solution-phone-link" href="tel:+48662792875" aria-label="Zadzwoń do Kabi-Chemie: +48 662 792 875">
        <span class="solution-phone-link__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/></svg>
        </span>
        <span>Zadzwoń: +48 662 792 875</span>
      </a>
    </div>
  </div>
</section>
"""


def _render_service(config):
    icons = {
        "pump": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="13" r="5.5"/><path d="m9 13 3.4-3.4"/><path d="M9 7.5V4M14.5 13H18"/><path d="M18 9s-2 2.3-2 3.7a2 2 0 0 0 4 0C20 11.3 18 9 18 9Z"/></svg>',
        "probe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6v11.2a5 5 0 1 1-6 0V3Z"/><path d="M12 7v9M9 7h6M7 21h10"/></svg>',
        "controller": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 8h10M7 12h3M14 12h3M7 16h6"/><circle cx="17" cy="16" r="1"/></svg>',
        "station": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M5 6v12M19 6v12M3 18h18"/><rect x="7" y="9" width="4" height="6" rx="1"/><rect x="13" y="9" width="4" height="6" rx="1"/><path d="M11 12h2"/></svg>',
        "alarm": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9Z"/><path d="M10 21h4M12 3V1"/></svg>',
        "trend": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 3v17h17"/><path d="m7 15 4-4 3 3 6-7"/><path d="M16 7h4v4"/></svg>',
        "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5M8 10.5h5M10.5 8v5"/></svg>',
        "wrench": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M15 7.3a4 4 0 0 0-5.4 4.6l-6 6a1.7 1.7 0 0 0 2.4 2.4l6-6a4 4 0 0 0 4.6-5.4l-2.4 2.4-1.6-1.6 2.4-2.4Z"/></svg>',
        "test": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 18a8 8 0 0 1 16 0"/><path d="m12 15 4-5M7 18h10"/><path d="m9 21 2 2 4-4"/></svg>',
        "measure": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><path d="M12 4v3M12 17v3M4 12h3M17 12h3M12 12l4-3"/></svg>',
        "flow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h12M13 4l3 3-3 3M20 17H8M11 14l-3 3 3 3"/><circle cx="5" cy="17" r="2"/><circle cx="19" cy="7" r="2"/></svg>',
        "dose": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 5h7v7H5zM12 8h4v4h3M8.5 12v7"/><path d="M19 14.5s-2.5 2.7-2.5 4.3a2.5 2.5 0 0 0 5 0c0-1.6-2.5-4.3-2.5-4.3Z"/></svg>',
        "response": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l2-5 4 10 2-5h6"/><path d="M4 4v16h16"/></svg>',
        "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 11a8 8 0 1 1-4.7-7.3"/><path d="m8.5 11.5 2.4 2.4L20 5"/></svg>',
        "report": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h9l4 4v14H6z"/><path d="M15 3v5h4M9 12h6M9 16h6"/></svg>',
        "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18M8 14h3M13 14h3M8 18h3"/></svg>',
        "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13 13 20l-9-9V4h7z"/><circle cx="8.5" cy="8.5" r="1.5"/></svg>',
        "history": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5M12 7v5l3 2"/></svg>',
        "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/></svg>',
    }

    hero_signals = [
        ("pump", "Pompy dozujące", "wydajność i szczelność"),
        ("probe", "Sondy procesowe", "kalibracja i odniesienie"),
        ("controller", "Sterowanie", "sygnały, alarmy i logika"),
    ]
    symptoms = [
        ("pump", "Niestabilna dawka", "Pompa pracuje, ale rzeczywista ilość preparatu nie odpowiada nastawie lub przepływowi.", "dozowanie"),
        ("probe", "Wynik bez potwierdzenia", "Sonda pokazuje wartość, której nie potwierdza pomiar odniesienia ani zachowanie procesu.", "pomiar"),
        ("alarm", "Powracający alarm", "Kasowanie komunikatu nie usuwa przyczyny, jeżeli problem leży w zasilaniu, hydraulice lub logice sterowania.", "automatyka"),
        ("trend", "Proces wymaga ciągłych korekt", "Częste ręczne zmiany nastaw zwykle wskazują na brak stabilnego sygnału albo niewłaściwą reakcję układu.", "proces"),
    ]
    route = [
        ("search", "Rozpoznanie zgłoszenia", "Identyfikujemy urządzenie, objaw, alarmy i wpływ usterki na pracę zakładu."),
        ("measure", "Diagnostyka na obiekcie", "Sprawdzamy zasilanie, hydraulikę, pomiar, elementy wykonawcze oraz sygnały sterujące."),
        ("wrench", "Naprawa i kalibracja", "Usuwamy przyczynę, ustawiamy urządzenie i potwierdzamy wydajność lub dokładność pomiaru."),
        ("test", "Test w warunkach pracy", "Uruchamiamy układ z procesem, zapisujemy wynik i przekazujemy konkretne zalecenia."),
    ]
    control_loop = [
        ("measure", "Pomiar", "Wiarygodna wartość procesowa"),
        ("flow", "Sterowanie", "Właściwy sygnał i reakcja"),
        ("dose", "Dozowanie", "Dawka zgodna z obciążeniem"),
        ("response", "Proces", "Potwierdzony efekt w instalacji"),
    ]
    outcomes = [
        ("check", "Wiarygodne wskazania", "Sonda i pomiar odniesienia dają spójną podstawę do sterowania."),
        ("pump", "Potwierdzona wydajność", "Dawka jest sprawdzona przy rzeczywistej pracy urządzenia."),
        ("report", "Czytelny protokół", "Wyniki testu, wykonane prace i zalecenia pozostają po wizycie."),
        ("calendar", "Plan dalszej obsługi", "Wiadomo, które części i przeglądy warto zaplanować z wyprzedzeniem."),
    ]
    prepare = [
        ("tag", "Urządzenie", "Producent, model i zdjęcie tabliczki znamionowej."),
        ("alarm", "Objaw", "Komunikat alarmu i informacja, od kiedy występuje problem."),
        ("flow", "Warunki pracy", "Medium, przepływ, ciśnienie, używana chemia i obecne nastawy."),
        ("history", "Historia obsługi", "Ostatni przegląd, wymienione części i wcześniejsze usterki."),
    ]

    def icon(name):
        return icons[name]

    # Sygnały hero w tym samym stylu co pozostałe karty rozwiązań: glif w okrągłej obwódce, jeden wiersz.
    hero_signal_rows = _join(
        f'<li class="has-icon"><span class="solution-hero__signal-icon" aria-hidden="true">{icon(name)}</span><span>{title}</span></li>'
        for name, title, text in hero_signals
    )
    symptom_rows = _join(
        f'<article class="service-symptom"><span class="service-icon service-icon--line" aria-hidden="true">{icon(name)}</span><div><h3>{title}</h3><p>{text}</p></div><strong>{tag}</strong></article>'
        for name, title, text, tag in symptoms
    )
    route_rows = _join(
        f'<article class="service-route__step"><span class="service-icon service-icon--dark" aria-hidden="true">{icon(name)}</span><div><h3>{title}</h3><p>{text}</p></div></article>'
        for name, title, text in route
    )
    loop_rows = _join(
        f'<article class="service-loop__item"><span class="service-icon service-icon--loop" aria-hidden="true">{icon(name)}</span><div><h3>{title}</h3><p>{text}</p></div></article>'
        for name, title, text in control_loop
    )
    outcome_rows = _join(
        f'<article class="service-outcome"><span class="service-icon service-icon--outcome" aria-hidden="true">{icon(name)}</span><div><h3>{title}</h3><p>{text}</p></div></article>'
        for name, title, text in outcomes
    )
    prepare_rows = _join(
        f'<article class="service-prepare__item"><span class="service-icon service-icon--prepare" aria-hidden="true">{icon(name)}</span><div><h3>{title}</h3><p>{text}</p></div></article>'
        for name, title, text in prepare
    )
    related = _join(
        f'<a href="{href}"><span>{label}</span><strong>{title}</strong><i aria-hidden="true">↗</i></a>'
        for label, title, href in config["related"]
    )
    faqs = _join(
        f'<details{" open" if index == 0 else ""}><summary><span>{question}</span><i aria-hidden="true"></i></summary><div class="solution-faq__answer"><p>{answer}</p></div></details>'
        for index, (question, answer) in enumerate(config["faq"])
    )

    return f"""
<section class="solution-hero service-hero" id="top" style="--solution-image:url('{config['image']}'); --solution-position:{config.get('image_position', 'center center')}">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <img class="service-engraving service-engraving--hero" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap solution-hero__inner">
    <div class="solution-hero__copy">
      <p class="solution-kicker"><span></span>Serwis urządzeń i automatyki</p>
      <h1>Sprawne urządzenia.<br>Stabilny proces.</h1>
      <p class="solution-hero__lead">Diagnozujemy urządzenie w kontekście całej instalacji. Przywracamy wiarygodny pomiar, właściwe dozowanie i stabilne sterowanie, a po wizycie przekazujemy jasne zalecenia.</p>
      <div class="solution-hero__actions">
        <a class="btn btn-primary" href="/kontakt/#kontakt-form">Zgłoś urządzenie do serwisu</a>
        <a class="solution-text-link" href="#zakres">Sprawdź zakres serwisu <span aria-hidden="true">↓</span></a>
      </div>
      <ul class="solution-hero__signals" aria-label="Obsługiwane obszary">{hero_signal_rows}</ul>
    </div>
  </div>
</section>

<section class="service-section service-symptoms" id="zakres">
  <img class="service-engraving service-engraving--symptoms" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap service-symptoms__grid">
    <header class="service-section__intro reveal-left">
      <p class="solution-kicker solution-kicker--dark"><span></span>Rozpoznanie objawu</p>
      <h2>Urządzenie pokazuje objaw. Przyczyna często leży w całym torze.</h2>
      <p>Dlatego nie kończymy na skasowaniu alarmu. Sprawdzamy, czy pomiar, sterowanie i dozowanie działają razem w rzeczywistych warunkach pracy.</p>
    </header>
    <div class="service-symptoms__rows" data-reveal-loop>{symptom_rows}</div>
  </div>
</section>

<section class="service-section service-route" id="przebieg">
  <img class="service-engraving service-engraving--route" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap service-route__grid">
    <header class="service-section__intro service-section__intro--dark reveal-left">
      <p class="solution-kicker"><span></span>Przebieg serwisu</p>
      <h2>Od zgłoszenia do potwierdzenia pracy.</h2>
      <p>Każdy etap kończy się konkretną decyzją techniczną. Dzięki temu zakład wie, co zostało sprawdzone, co zmieniliśmy i jaki jest następny krok.</p>
    </header>
    <div class="service-route__steps" data-reveal-loop>{route_rows}</div>
  </div>
</section>

<section class="service-section service-loop" id="diagnostyka">
  <div class="wrap">
    <header class="service-loop__head reveal">
      <div>
        <p class="solution-kicker solution-kicker--dark"><span></span>Pełny tor działania</p>
        <h2>Sprawdzamy zależności, nie pojedynczy element.</h2>
      </div>
      <p>Sprawne urządzenie ma sens dopiero wtedy, gdy jego sygnał prowadzi do właściwej reakcji procesu. Testujemy więc cały obieg od pomiaru do efektu w instalacji.</p>
    </header>
    <div class="service-loop__track" data-reveal-loop>{loop_rows}</div>
  </div>
</section>

<section class="service-section service-results" id="efekt">
  <div class="service-results__media" aria-hidden="true"></div>
  <div class="service-results__shade" aria-hidden="true"></div>
  <img class="service-engraving service-engraving--results" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap service-results__grid">
    <header class="service-section__intro service-section__intro--dark reveal-left">
      <p class="solution-kicker"><span></span>Po zakończeniu prac</p>
      <h2>Wynik serwisu ma być czytelny także po wyjeździe technika.</h2>
      <p>Potwierdzamy działanie urządzenia w warunkach roboczych i porządkujemy informacje potrzebne do dalszej obsługi.</p>
    </header>
    <div class="service-results__list" data-reveal-loop>{outcome_rows}</div>
  </div>
</section>

<section class="service-section service-prepare" id="zgloszenie">
  <img class="service-engraving service-engraving--prepare" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap service-prepare__grid">
    <header class="service-section__intro reveal-left">
      <p class="solution-kicker solution-kicker--dark"><span></span>Przed zgłoszeniem</p>
      <h2>Kilka informacji pozwala szybciej przygotować serwis.</h2>
      <p>Nie trzeba mieć pełnej dokumentacji. Wystarczy to, co jest dostępne, a brakujące dane ustalimy telefonicznie lub na obiekcie.</p>
      <a class="service-inline-link" href="/kontakt/#kontakt-form">Przejdź do formularza <span aria-hidden="true">↗</span></a>
    </header>
    <div class="service-prepare__items" data-reveal-loop>{prepare_rows}</div>
  </div>
</section>

<nav class="solution-related service-related" aria-label="Powiązane rozwiązania">
  <div class="wrap">
    <p>Powiązane rozwiązania</p>
    <div class="solution-related__links">{related}</div>
  </div>
</nav>

<section class="solution-section solution-faq service-faq" id="faq">
  <div class="wrap solution-faq__grid">
    <header class="solution-faq__intro reveal-left">
      <p class="solution-kicker"><span></span>FAQ</p>
      <h2>{config['faq_title']}</h2>
      <p>Konkretnie o przygotowaniu wizyty, obsługiwanych urządzeniach, kalibracji oraz dokumentacji po zakończeniu prac.</p>
    </header>
    <div class="solution-faq__list">{faqs}</div>
  </div>
</section>

<section class="solution-cta service-cta">
  <img class="service-engraving service-engraving--cta" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap solution-cta__inner">
    <div>
      <p class="solution-kicker solution-kicker--dark"><span></span>Zgłoszenie serwisowe</p>
      <h2>Omówmy urządzenie i właściwy zakres serwisu.</h2>
      <p>Ocenimy pilność, wskażemy potrzebne informacje i ustalimy, czy kolejny krok to konsultacja zdalna, przygotowanie części czy wizyta technika.</p>
    </div>
    <div class="solution-cta__actions">
      <a class="btn btn-primary" href="/kontakt/#kontakt-form">Wyślij zgłoszenie serwisowe</a>
      <a class="solution-phone-link" href="tel:+48662792875" aria-label="Zadzwoń do Kabi-Chemie: +48 662 792 875">
        <span class="solution-phone-link__icon" aria-hidden="true">{icon('phone')}</span>
        <span>Zadzwoń: +48 662 792 875</span>
      </a>
    </div>
  </div>
</section>
"""


def _render_solution(config):
    if config.get("slug") == "kcaqua":
        return _render_kcaqua(config)
    if config.get("slug") == "ro":
        return _render_ro(config)
    if config.get("slug") == "descaling":
        return _render_descaling(config)
    if config.get("slug") == "service":
        return _render_service(config)

    issues = _join(
        f"""
        <article class="solution-issue">
          <span class="solution-issue__mark" aria-hidden="true"></span>
          <div class="solution-issue__copy"><h3>{title}</h3><p>{text}</p></div>
          <span class="solution-issue__tag">{tag}</span>
        </article>"""
        for title, text, tag in config["issues"]
    )

    process_stages = config.get("process_stages", [])
    process_results = config.get("process_results", [])
    process = _join(
        f"""
        <li>
          <span class="solution-process__mark" aria-hidden="true"></span>
          {f'<span class="solution-process__stage">{process_stages[index]}</span>' if index < len(process_stages) else ''}
          <div><h3>{title}</h3><p>{text}</p></div>
          {f'<span class="solution-process__result">{process_results[index]} <i aria-hidden="true">→</i></span>' if index < len(process_results) else ''}
        </li>"""
        for index, (title, text) in enumerate(config["process"])
    )

    outcomes = _join(
        f"""
        <article class="solution-outcome">
          <span class="solution-outcome__mark" aria-hidden="true"></span>
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for title, text in config["outcomes"]
    )

    data_icons = config.get("data_icons", [])

    def render_data_row(index, title, text):
        icon_name = data_icons[index] if index < len(data_icons) else None
        marker = (
            f'<span class="solution-data__icon" aria-hidden="true">{HERO_ICONS[icon_name]}</span>'
            if icon_name in HERO_ICONS
            else '<span class="solution-data__mark" aria-hidden="true"></span>'
        )
        return f"""
        <li>
          {marker}
          <div><strong>{title}</strong><p>{text}</p></div>
        </li>"""

    data_rows = _join(
        render_data_row(index, title, text)
        for index, (title, text) in enumerate(config["data_rows"])
    )

    related = _join(
        f"""
        <a href="{href}">
          <span>{label}</span>
          <strong>{title}</strong>
          <i aria-hidden="true">↗</i>
        </a>"""
        for label, title, href in config["related"]
    )

    faqs = _join(
        f"""
        <details{' open' if index == 1 else ''}>
          <summary><span>{question}</span><i aria-hidden="true"></i></summary>
          <div class="solution-faq__answer"><p>{answer}</p></div>
        </details>"""
        for index, (question, answer) in enumerate(config["faq"])
    )

    signals = _join(_hero_signal(signal) for signal in config["signals"])
    signals_markup = (
        f'<ul class="solution-hero__signals" aria-label="Najważniejsze obszary">{signals}</ul>'
        if signals else ""
    )

    diagnosis_section = f"""
<section class="solution-section solution-diagnosis" id="diagnoza">
  <div class="wrap solution-diagnosis__grid">
    <header class="solution-section__intro reveal-left">
      <p class="solution-kicker solution-kicker--dark"><span></span>{config['issues_kicker']}</p>
      <h2>{config['issues_title']}</h2>
      <p>{config['issues_intro']}</p>
    </header>
    <div class="solution-issues" data-reveal-loop>{issues}</div>
  </div>
</section>
"""

    process_flow = (
        f"""
    <div class="solution-process-flow reveal">
      <p class="solution-process-flow__edge solution-process-flow__edge--entry"><span>Wejście</span><strong>{config['process_entry']}</strong></p>
      <ol class="solution-process-list" data-reveal-loop>{process}</ol>
      <p class="solution-process-flow__edge solution-process-flow__edge--exit"><span>Wynik</span><strong>{config['process_exit']}</strong></p>
    </div>"""
        if config.get("process_entry") and config.get("process_exit")
        else f'<ol class="solution-process-list" data-reveal-loop>{process}</ol>'
    )

    # Zdjęcie w tle sekcji procesu, w rytmie stron RO i odkamieniania.
    method_photo = config.get("method_image")
    method_attrs = (
        f' style="--method-image:url(\'{method_photo}\'); '
        f'--method-position:{config.get("method_position", "center center")}"'
        if method_photo else ""
    )
    method_media = (
        '<div class="solution-method__media" aria-hidden="true"></div>'
        '<div class="solution-method__shade" aria-hidden="true"></div>'
        if method_photo else '<span class="solution-method__mark" aria-hidden="true"></span>'
    )

    method_section = f"""
<section class="solution-section solution-method{' solution-method--photo' if method_photo else ''}" id="proces"{method_attrs}>
  {method_media}
  <div class="wrap">
    <header class="solution-method__head reveal">
      <div>
        <p class="solution-kicker"><span></span>{config['process_kicker']}</p>
        <h2>{config['process_title']}</h2>
      </div>
      <p>{config['process_intro']}</p>
    </header>
    {process_flow}
  </div>
</section>
"""

    results_section = f"""
<section class="solution-section solution-results" id="efekty">
  <div class="wrap solution-results__grid">
    <header class="solution-results__intro reveal-left">
      <p class="solution-kicker solution-kicker--dark"><span></span>{config['outcomes_kicker']}</p>
      <h2>{config['outcomes_title']}</h2>
      <p>{config['outcomes_intro']}</p>
      <a class="solution-inline-link" href="{config['outcomes_href']}">{config['outcomes_link']} <span aria-hidden="true">↗</span></a>
    </header>
    <div class="solution-outcomes" data-reveal-loop>{outcomes}</div>
  </div>
</section>
"""

    data_section = f"""
<section class="solution-section solution-data" id="dane">
  <div class="wrap solution-data__grid">
    <header class="solution-data__intro reveal-left">
      <p class="solution-kicker"><span></span>{config['data_kicker']}</p>
      <h2>{config['data_title']}</h2>
      <p>{config['data_intro']}</p>
    </header>
    <ol class="solution-data__list" data-reveal-loop>{data_rows}</ol>
  </div>
</section>
"""

    section_map = {
        "diagnosis": diagnosis_section,
        "method": method_section,
        "results": results_section,
        "data": data_section,
    }
    story = _join(
        section_map[name]
        for name in config.get("sequence", ("diagnosis", "method", "results", "data"))
    )

    return f"""
<section class="solution-hero solution-hero--{config['slug']}" id="top" style="--solution-image:url('{config['image']}'); --solution-position:{config.get('image_position', 'center center')}">
  <div class="solution-hero__media" aria-hidden="true"></div>
  <div class="solution-hero__shade" aria-hidden="true"></div>
  <div class="wrap solution-hero__inner">
    <div class="solution-hero__copy">
      <p class="solution-kicker"><span></span>{config['kicker']}</p>
      <h1>{config['h1_html']}</h1>
      <p class="solution-hero__lead">{config['lead']}</p>
      <div class="solution-hero__actions">
        <a class="btn btn-primary" href="{config['primary_href']}">{config['primary_label']}</a>
        <a class="solution-text-link" href="{config['secondary_href']}">{config['secondary_label']} <span aria-hidden="true">↗</span></a>
      </div>
      {signals_markup}
    </div>
  </div>
</section>

{story}

<nav class="solution-related" aria-label="Powiązane rozwiązania">
  <div class="wrap">
    <p>Powiązane rozwiązania</p>
    <div class="solution-related__links">{related}</div>
  </div>
</nav>

<section class="solution-section solution-faq" id="faq">
  <div class="wrap solution-faq__grid">
    <header class="solution-faq__intro reveal-left">
      <p class="solution-kicker"><span></span>FAQ</p>
      <h2>{config['faq_title']}</h2>
      <p>{config['faq_intro']}</p>
    </header>
    <div class="solution-faq__list">{faqs}</div>
  </div>
</section>

<section class="solution-cta">
  <span class="solution-cta__mark" aria-hidden="true"></span>
  <div class="wrap solution-cta__inner">
    <div>
      <p class="solution-kicker"><span></span>{config['cta_kicker']}</p>
      <h2>{config['cta_title']}</h2>
      <p>{config['cta_text']}</p>
    </div>
    <div class="solution-cta__actions">
      <a class="btn btn-primary" href="{config['cta_primary_href']}">{config['cta_primary_label']}</a>
      <a class="solution-phone-link" href="tel:+48662792875" aria-label="Zadzwoń do Kabi-Chemie: +48 662 792 875">
        <span class="solution-phone-link__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/></svg>
        </span>
        <span>Zadzwoń: +48 662 792 875</span>
      </a>
    </div>
  </div>
</section>
"""


SOLUTIONS = [
    {
        "path": "/kotly-parowe/",
        "slug": "boilers",
        "layout": "editorial",
        "sequence": ("diagnosis", "results", "method", "data"),
        "title": "Kondycjonowanie wody w kotłach parowych | Kabi-Chemie",
        "meta": "Programy kondycjonowania wody dla kotłów parowych. Kontrola kamienia, korozji i odsalania, dobór chemii KCAQUA, automatyka oraz monitoring efektów.",
        "image": "/assets/visuals-v2/hero-boilers-v2.jpg",
        "image_position": "62% center",
        "kicker": "Rozwiązania / Kotły parowe",
        "h1_html": "Kondycjonowanie wody <span>w kotłach parowych.</span>",
        "lead": "Łączymy chemię, automatykę dozowania i stałą kontrolę parametrów, aby ograniczać kamień, korozję oraz koszt wytwarzania pary. Program dobieramy do warunków pracy konkretnej kotłowni.",
        "primary_label": "Porozmawiaj o kotłowni",
        "primary_href": "/bezplatna-konsultacja/",
        "secondary_label": "Zobacz wdrożenie Fako",
        "secondary_href": "/case-study/kociol-parowy-fako/",
        "signals": [("feedwater", "Woda zasilająca i kotłowa"), ("steam", "Para i kondensat"),
                    ("dosing", "Dozowanie i odsalanie")],
        "chapter": "01",
        "chapter_label": "Kotły parowe",
        "proof": [
            ("Wymiana ciepła", "Kontrolujemy osad na powierzchniach grzewczych."),
            ("Odsalanie", "Ustalamy przewodność odpowiednią dla kotła i wody."),
            ("Ochrona metalu", "Prowadzimy pH, tlen i kondensat pod kontrolą."),
        ],
        "issues_kicker": "Diagnoza kotłowni",
        "issues_title": "Koszt pary zależy od kontroli parametrów.",
        "issues_intro": "Nie zaczynamy od sprzedaży preparatu. Najpierw sprawdzamy wodę, sposób prowadzenia kotła i miejsca, w których instalacja traci energię, wodę lub trwałość.",
        "issues": [
            ("Kamień na powierzchniach grzewczych", "Warstwa osadu działa jak izolacja. Kocioł potrzebuje więcej paliwa, aby przekazać tę samą ilość ciepła do wody.", "Sprawność cieplna"),
            ("Korozja w układzie pary i kondensatu", "Tlen, niewłaściwe pH i zanieczyszczenia powodują wżery, nieszczelności oraz szybsze zużycie instalacji.", "Bezpieczeństwo"),
            ("Nadmierne odsalanie i odmulanie", "Zbyt ostrożne nastawy usuwają z kotła gorącą wodę, chemię i energię, które można utrzymać w procesie.", "Woda i energia"),
            ("Niestabilne dozowanie", "Pompa bez kalibracji lub dawka niedopasowana do obciążenia nie zapewniają przewidywalnej ochrony kotła.", "Automatyka"),
        ],
        "method_image": "/assets/visuals-v2/case-fako-v2.jpg",
        "method_position": "62% center",
        "process_kicker": "Sposób działania",
        "process_title": '<span class="solution-title-line">Od danych z instalacji</span><span class="solution-title-line">do mierzalnego efektu.</span>',
        "process_intro": "Najpierw ustalamy punkt wyjścia. Następnie dobieramy, uruchamiamy i prowadzimy program na podstawie wyników.",
        "process_entry": "Próbka wody i dane procesowe",
        "process_exit": "Raport i plan dalszego prowadzenia",
        "process_stages": ["Rozpoznajemy", "Projektujemy", "Uruchamiamy", "Potwierdzamy"],
        "process_results": ["Punkt odniesienia", "Program i nastawy", "Stabilna praca", "Raport i korekta"],
        "process": [
            ("Bilans instalacji", "Analizujemy wodę zasilającą, kotłową i kondensat, obciążenie kotła, odsalanie oraz obecne dozowanie."),
            ("Program chemiczny", "Dobieramy funkcje preparatu, dawkę, wartości docelowe oraz reakcje na odchylenia."),
            ("Uruchomienie", "Kalibrujemy dozowanie, wyznaczamy punkty pomiarowe i porządkujemy procedury obsługi."),
            ("Nadzór efektów", "Śledzimy parametry i zużycie mediów, a program korygujemy wraz ze zmianą pracy kotłowni."),
        ],
        "outcomes_kicker": "Efekt dla zakładu",
        "outcomes_title": "Mniej strat, więcej przewidywalności.",
        "outcomes_intro": "Dobrze prowadzona woda kotłowa wspiera jednocześnie produkcję, utrzymanie ruchu i kontrolę kosztów.",
        "outcomes_href": "/kalkulator-oszczednosci/",
        "outcomes_link": "Sprawdź potencjał odzyskania kosztów",
        "outcomes": [
            ("Niższe zapotrzebowanie na paliwo", "Czyste powierzchnie grzewcze skuteczniej przekazują energię do wody."),
            ("Mniej wody i ścieków", "Stabilna przewodność pozwala ograniczyć niepotrzebne odsalanie."),
            ("Dłuższa praca bez awarii", "Kontrola korozji i osadu zmniejsza ryzyko uszkodzeń oraz nieplanowanych postojów."),
            ("Dane gotowe do decyzji", "Raport łączy parametry techniczne z wpływem na koszty eksploatacji."),
        ],
        "data_kicker": "Zakres audytu",
        "data_title": "Parametry, które opisują pracę kotła.",
        "data_intro": "Nie potrzebujesz kompletnej dokumentacji na pierwszą rozmowę. Brakujące pomiary porządkujemy wspólnie podczas audytu.",
        "data_rows": [
            ("Woda i kondensat", "Twardość, pH, przewodność, zasadowość, żelazo oraz udział powrotu kondensatu."),
            ("Praca kotła", "Ciśnienie, produkcja pary, godziny pracy, zmienność obciążenia i temperatura spalin."),
            ("Zużycie mediów", "Paliwo, woda uzupełniająca, odsalanie, ścieki i obecne zużycie preparatów."),
            ("Dozowanie i pomiar", "Pompy, sondy, punkty poboru prób, alarmy oraz sposób dokumentowania wyników."),
        ],
        "data_icons": ["feedwater", "steam", "utility_meter", "dosing"],
        "related": [
            ("Technologia", "KCAQUA do wody kotłowej", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
            ("Realizacja", "Kocioł parowy Fako", "/case-study/kociol-parowy-fako/"),
            ("Narzędzie", "Kalkulator oszczędności", "/kalkulator-oszczednosci/"),
        ],
        "faq_title": "Pytania o program dla kotłowni parowej.",
        "faq_intro": "Konkretnie o pomiarach, postoju, odsalaniu i zakresie odpowiedzialności.",
        "faq": [
            ("Od czego zaczyna się dobór programu dla kotła parowego?", "Od analizy wody zasilającej, kotłowej i kondensatu oraz od poznania ciśnienia, produkcji pary, odsalania i obecnego dozowania. Dopiero ten obraz pozwala ustalić preparat, dawkę i wartości docelowe."),
            ("Czy wdrożenie wymaga postoju kotłowni?", "Analizę, uruchomienie dozowania i monitoring zwykle prowadzimy podczas normalnej pracy. Jeżeli potrzebne jest czyszczenie chemiczne albo zmiana elementów instalacji, termin i zakres postoju ustalamy oddzielnie."),
            ("Jak rozpoznać, że kamień podnosi już koszt pary?", "Sygnałem może być rosnące zużycie paliwa na jednostkę pary, wyższa temperatura spalin, pogorszenie wymiany ciepła lub osad widoczny podczas rewizji. Pojedynczy objaw nie wystarcza, dlatego porównujemy trendy i wyniki badań."),
            ("Jak ograniczyć odsalanie bez pogorszenia bezpieczeństwa?", "Najpierw stabilizujemy jakość wody zasilającej i dozowanie, następnie wyznaczamy bezpieczny zakres przewodności zgodny z warunkami pracy i wymaganiami producenta kotła. Zmiany wprowadzamy stopniowo, pod kontrolą pomiarów."),
            ("Co zakład otrzymuje po audycie?", "Otrzymuje uporządkowaną diagnozę, listę ryzyk, docelowe parametry, rekomendowany sposób dozowania i monitoringu oraz plan weryfikacji efektów technicznych i kosztowych."),
        ],
        "cta_kicker": "Pierwszy krok",
        "cta_title": "Porozmawiajmy o pracy Twojej kotłowni.",
        "cta_text": "Wystarczą podstawowe parametry i opis problemu. Inżynier pomoże uporządkować dane oraz wskazać rozsądny kolejny krok.",
        "cta_primary_label": "Wyślij zapytanie techniczne",
        "cta_primary_href": "/bezplatna-konsultacja/#consult-form",
    },
    {
        "path": "/uklady-chlodnicze/",
        "slug": "cooling",
        "style": "boilers",
        "layout": "editorial",
        "sequence": ("diagnosis", "results", "method", "data"),
        "title": "Skraplacze wyparne i kondycjonowanie wody | Kabi-Chemie",
        "meta": "Kondycjonowanie wody w skraplaczach wyparnych i obiegach chłodniczych. Ochrona przed kamieniem, korozją i biofilmem, kontrola odsalania oraz monitoring.",
        "image": "/assets/visuals-v2/hero-cooling-v2.jpg",
        "image_position": "64% center",
        "kicker": "Rozwiązania / Skraplacze wyparne",
        "h1_html": "Skraplacze wyparne <span>bez kamienia i biofilmu.</span>",
        "lead": "Prowadzimy wodę w skraplaczach i wieżach chłodniczych tak, aby utrzymać wymianę ciepła, ograniczyć zużycie wody i chronić instalację przed korozją oraz rozwojem mikrobiologicznym.",
        "primary_label": "Sprawdź układ chłodniczy",
        "primary_href": "/bezplatna-konsultacja/",
        "secondary_label": "Zobacz wdrożenie BAC",
        "secondary_href": "/case-study/skraplacz-bac-kcaqua/",
        "signals": [("condenser", "Skraplacze BAC i EVAPCO"), ("ammonia", "Obiegi amoniakalne"),
                    ("tower", "Wieże chłodnicze")],
        "chapter": "02",
        "chapter_label": "Chłodnictwo",
        "proof": [
            ("Kamień", "Chronimy wężownice i powierzchnie wymiany ciepła."),
            ("Mikrobiologia", "Program biocydowy prowadzimy na podstawie kontroli."),
            ("Odsalanie", "Cykle koncentracji dopasowujemy do jakości wody."),
        ],
        "issues_kicker": "Diagnoza obiegu",
        "issues_title": "Stabilne chłodzenie zaczyna się w obiegu.",
        "issues_intro": "W układzie otwartym parametry zmieniają się razem z pogodą, obciążeniem i wodą uzupełniającą. Dlatego program musi reagować na rzeczywiste warunki, a nie działać według stałej dawki przez cały rok.",
        "issues": [
            ("Osad na wężownicach", "Wytrącające się sole ograniczają wymianę ciepła i mogą podnosić temperaturę skraplania oraz zużycie energii.", "Wydajność"),
            ("Biofilm i mikroorganizmy", "Warstwa biologiczna pogarsza chłodzenie, wspiera korozję podosadową i utrudnia utrzymanie higieny obiegu.", "Higiena obiegu"),
            ("Korozja stali i ocynku", "Nieprawidłowe pH, zasolenie lub program chemiczny skracają trwałość wymienników, wanien i rurociągów.", "Ochrona materiałów"),
            ("Zbyt częste odsalanie", "Niewłaściwe nastawy przewodności zwiększają pobór wody uzupełniającej i ilość ścieków bez poprawy chłodzenia.", "Koszt wody"),
        ],
        "method_image": "/assets/visuals-v2/case-bac-v2.jpg",
        "method_position": "58% center",
        "process_kicker": "Program obiegowy",
        "process_title": "Program dopasowany do sezonu i obciążenia.",
        "process_intro": "Łączymy analizę wody, program KCAQUA, automatykę odsalania i nadzór mikrobiologiczny w jeden proces eksploatacyjny.",
        "process_entry": "Dane obiegu i wody uzupełniającej",
        "process_exit": "Raport i nastawy na kolejny sezon",
        "process_stages": ["Rozpoznajemy", "Projektujemy", "Uruchamiamy", "Prowadzimy"],
        "process_results": ["Punkt odniesienia", "Program i nastawy", "Stabilna praca", "Kontrola sezonu"],
        "process": [
            ("Rozpoznanie układu", "Sprawdzamy materiały, pojemność obiegu, temperatury, wodę uzupełniającą, sposób odsalania i historię osadów."),
            ("Dobór programu", "Ustalamy ochronę przed kamieniem i korozją oraz strategię biocydową odpowiednią dla pracy zakładu."),
            ("Automatyka i dozowanie", "Kalibrujemy pompy, sondę przewodności, progi odsalania i harmonogram dawkowania."),
            ("Kontrola sezonowa", "Oceniamy wyniki chemiczne, mikrobiologiczne i eksploatacyjne, a parametry korygujemy wraz z obciążeniem."),
        ],
        "outcomes_kicker": "Efekt operacyjny",
        "outcomes_title": "Stabilne chłodzenie wspiera plan produkcji.",
        "outcomes_intro": "Celem nie jest samo spełnienie tabeli parametrów, lecz stabilny proces przy rozsądnym zużyciu mediów.",
        "outcomes_href": "/case-study/skraplacz-bac-kcaqua/",
        "outcomes_link": "Zobacz wyniki wdrożenia",
        "outcomes": [
            ("Stabilna wymiana ciepła", "Czyste wężownice pomagają utrzymać temperaturę procesu przy zmiennym obciążeniu."),
            ("Mniejszy pobór wody", "Dobrze ustawione cykle koncentracji ograniczają wodę uzupełniającą i ścieki."),
            ("Kontrola ryzyka biologicznego", "Program biocydowy, monitoring i higiena ograniczają warunki sprzyjające rozwojowi mikroorganizmów."),
            ("Dłuższa trwałość urządzeń", "Ochrona materiałów zmniejsza ryzyko przecieków, białej korozji i kosztownych napraw."),
        ],
        "data_kicker": "Dane z instalacji",
        "data_title": "Dane, które opisują pracę układu.",
        "data_intro": "Pełny obraz powstaje z parametrów chemicznych, trendów automatyki i obserwacji eksploatacyjnych.",
        "data_rows": [
            ("Woda uzupełniająca i obiegowa", "Twardość, alkaliczność, chlorki, przewodność, pH oraz czynniki wpływające na ryzyko osadu."),
            ("Parametry chłodzenia", "Temperatury, obciążenie, podejście temperaturowe, ciśnienie skraplania i sezonowość pracy."),
            ("Mikrobiologia", "Wyniki kontroli, historia biofilmu, sposób dawkowania biocydów oraz działania higieniczne."),
            ("Odsalanie i dozowanie", "Nastawy sterownika, praca sond, wydajność pomp i zużycie wody oraz preparatów."),
        ],
        "data_icons": ["feedwater", "condenser", "bio", "dosing"],
        "related": [
            ("Realizacja", "Skraplacz BAC i KCAQUA", "/case-study/skraplacz-bac-kcaqua/"),
            ("Realizacja", "Skraplacz EVAPCO", "/case-study/skraplacz-evapco-przetworstwo-rybne/"),
            ("Usługa", "Analiza wody obiegowej", "/uslugi/analiza-wody/"),
        ],
        "faq_title": "Pytania o skraplacz i obieg chłodniczy.",
        "faq_intro": "O wodzie, mikrobiologii, odsalaniu i wdrożeniu bez zbędnych skrótów.",
        "faq": [
            ("Czy jeden program może kontrolować kamień, korozję i biofilm?", "Te trzy obszary trzeba prowadzić wspólnie, ale nie oznacza to jednej uniwersalnej dawki. Skład programu, częstotliwość biocydu i zakres przewodności dobieramy do wody, materiałów oraz obciążenia układu."),
            ("Jak ograniczyć zużycie wody w skraplaczu wyparnym?", "Analizujemy cykle koncentracji, jakość wody uzupełniającej i obecne progi odsalania. Następnie stabilizujemy chemię i stopniowo ustawiamy przewodność tak, aby ograniczyć zrzut bez zwiększenia ryzyka kamienia lub korozji."),
            ("Czy obsługujecie skraplacze amoniakalne BAC i EVAPCO?", "Tak. Program dobieramy do konkretnego urządzenia, materiałów i warunków pracy, ze szczególnym uwzględnieniem wężownic, powierzchni ocynkowanych, jakości wody i wymagań producenta."),
            ("Jak kontrolujecie ryzyko mikrobiologiczne?", "Łączymy właściwy program biocydowy z regularną kontrolą, higieną urządzenia i dokumentowaniem wyników. Zakres ustalamy z uwzględnieniem obowiązków właściciela instalacji i oceny ryzyka dla zakładu."),
            ("Czy wdrożenie wymaga zatrzymania chłodzenia?", "Analizę, korektę dozowania i większość prac automatyki można przeprowadzić podczas pracy. Czyszczenie, naprawy lub działania wymagające dostępu do wnętrza urządzenia planujemy w uzgodnionym oknie serwisowym."),
        ],
        "cta_kicker": "Stabilny sezon",
        "cta_title": "Sprawdźmy, gdzie układ traci wodę i wydajność.",
        "cta_text": "Krótka rozmowa i podstawowe dane wystarczą, aby ocenić, czy potrzebna jest korekta programu, automatyki czy pełny audyt obiegu.",
        "cta_primary_label": "Umów rozmowę o chłodzeniu",
        "cta_primary_href": "/bezplatna-konsultacja/",
    },
    {
        "path": "/kotly-parowe/kondycjonowanie-wody-kotlowej/",
        "slug": "kcaqua",
        "layout": "kcaqua",
        "sequence": ("diagnosis", "method", "data", "results"),
        "title": "Technologia KCAQUA do wody kotłowej | Kabi-Chemie",
        "meta": "Technologia KCAQUA łączy dobór chemii, automatykę dozowania, kontrolę parametrów i monitoring wody kotłowej. Program dopasowany do konkretnej instalacji.",
        "image": "/assets/visuals-v2/hero-kcaqua-v2.jpg",
        "image_position": "66% center",
        "kicker": "Technologia KCAQUA",
        "h1_html": "KCAQUA.<br>Chemia prowadzona na danych.",
        "lead": "Dobieramy chemię, dozowanie i zakres kontroli do rzeczywistej pracy instalacji. Program reaguje na zmiany jakości wody, obciążenia kotła i udziału kondensatu.",
        "primary_label": "Porozmawiaj o programie KCAQUA",
        "primary_href": "/bezplatna-konsultacja/",
        "secondary_label": "Zobacz wdrożenie Fako",
        "secondary_href": "/case-study/kociol-parowy-fako/",
        "signals": ["Dobór do instalacji", "Automatyczne dozowanie", "Raportowanie efektów"],
        "chapter": "03",
        "chapter_label": "KCAQUA",
        "proof": [
            ("Chemia", "Funkcje programu dobieramy do wody i instalacji."),
            ("Automatyka", "Dawka podąża za przepływem i obciążeniem układu."),
            ("Monitoring", "Parametry i efekty oceniamy w stałym rytmie."),
        ],
        "issues_kicker": "Logika technologii",
        "issues_title": "Program KCAQUA zaczyna się od danych.",
        "issues_intro": "Ta sama instalacja może wymagać innej dawki rano, przy szczycie produkcji i po zmianie jakości wody. Dlatego KCAQUA opisujemy jako sposób prowadzenia procesu, a nie pojedynczy kanister.",
        "issues": [
            ("Jakość wody zasilającej", "Twardość, alkaliczność i zanieczyszczenia określają ryzyko osadu oraz zapotrzebowanie na chemię.", "Punkt wejścia"),
            ("pH i ochrona metalu", "Zakres pH musi wspierać warstwę ochronną stali i jednocześnie odpowiadać warunkom pracy kotła.", "Korozja"),
            ("Tlen i kondensat", "Ochrona nie kończy się w walczaku. Obejmuje także wodę zasilającą, linię pary oraz powrót kondensatu.", "Cały obieg"),
            ("Przewodność i odsalanie", "Stabilne zasolenie pozwala utrzymać jakość pary bez niepotrzebnej utraty gorącej wody.", "Efektywność"),
        ],
        "process_kicker": "Od receptury do nadzoru",
        "process_title": "Jedna technologia, pełna kontrola programu.",
        "process_intro": "Program pozostaje czytelny dla obsługi i mierzalny dla osób odpowiedzialnych za koszty oraz niezawodność.",
        "process": [
            ("Charakterystyka wody", "Badamy źródło, uzdatnianie, wodę kotłową i kondensat oraz rozpoznajemy zmienność parametrów."),
            ("Matryca programu", "Dobieramy funkcje chemiczne, dawkę bazową, korekty i wartości graniczne dla pomiarów."),
            ("Układ dozowania", "Weryfikujemy pompy, zbiorniki, punkty wtrysku, sygnały przepływu i możliwość automatycznej regulacji."),
            ("Prowadzenie instalacji", "Ustalamy harmonogram badań, reakcje na odchylenia i sposób raportowania efektów."),
        ],
        "outcomes_kicker": "Przewaga programu",
        "outcomes_title": "Chemia prowadzona jak element procesu.",
        "outcomes_intro": "Dzięki połączeniu dozowania i danych program może nadążać za instalacją zamiast działać obok niej.",
        "outcomes_href": "/case-study/kociol-parowy-fako/",
        "outcomes_link": "Zobacz KCAQUA w praktyce",
        "outcomes": [
            ("Powtarzalne parametry", "Obsługa pracuje według jasno ustalonych wartości i reakcji na odchylenia."),
            ("Dawka adekwatna do pracy", "Dozowanie można powiązać z przepływem wody lub obciążeniem, zamiast utrzymywać stałą wartość."),
            ("Mniej działań interwencyjnych", "Stabilny program ogranicza sytuacje, w których problem jest zauważany dopiero podczas awarii lub rewizji."),
            ("Czytelna odpowiedzialność", "Jeden zespół łączy analizę, chemię, automatykę i interpretację wyników."),
        ],
        "data_kicker": "Punkty kontrolne",
        "data_title": "Parametry, które dają kontrolę nad programem.",
        "data_intro": "Zakres pomiarów dobieramy do instalacji. Poniższe obszary tworzą podstawę większości programów kotłowych.",
        "data_rows": [
            ("Parametry chemiczne", "pH, przewodność, twardość, zasadowość, siarczyny lub inny wskaźnik działania programu oraz żelazo."),
            ("Warunki procesowe", "Ciśnienie, temperatura, produkcja pary, przepływ wody i udział kondensatu."),
            ("Praca automatyki", "Wydajność pomp, sygnały sterujące, stan sond, alarmy i rzeczywisty czas dozowania."),
            ("Efekt eksploatacyjny", "Zużycie paliwa, wody, ścieków, chemii oraz obserwacje z rewizji i czyszczeń."),
        ],
        "related": [
            ("Zastosowanie", "Kotły parowe", "/kotly-parowe/"),
            ("Realizacja", "Kocioł parowy Fako", "/case-study/kociol-parowy-fako/"),
            ("Serwis", "Dozowanie i sondy", "/uslugi/serwis-urzadzen/"),
        ],
        "faq_title": "Najczęstsze pytania przed wdrożeniem KCAQUA.",
        "faq_intro": "Konkretnie o doborze, dozowaniu, pomiarach i potwierdzaniu efektów programu.",
        "faq": [
            ("Czym KCAQUA różni się od uniwersalnego preparatu z katalogu?", "KCAQUA traktujemy jako program. Obejmuje rozpoznanie wody i instalacji, dobór funkcji chemicznych, ustalenie dawki, uruchomienie dozowania oraz kontrolę wyników. Preparat jest ważnym elementem, ale nie zastępuje całego procesu."),
            ("Jak dobierana jest dawka preparatu?", "Uwzględniamy przepływ wody uzupełniającej, jakość uzdatniania, alkaliczność, twardość, warunki kotła, udział kondensatu i oczekiwany efekt programu. Dawkę potwierdzamy pomiarem i korygujemy po uruchomieniu."),
            ("Jak często trzeba kontrolować parametry?", "Na początku programu pomiary wykonuje się częściej, aby ustabilizować instalację. Późniejszy rytm zależy od ryzyka, zmienności obciążenia, automatyki i powtarzalności wyników."),
            ("Czy KCAQUA może pracować z istniejącymi pompami dozującymi?", "Najczęściej tak, o ile pompy mają odpowiednią wydajność, zakres regulacji i kompatybilne materiały. Przed wdrożeniem sprawdzamy ich stan, punkt wtrysku i sposób sterowania."),
            ("Jak potwierdzacie efekt programu?", "Porównujemy trendy parametrów wody, dozowania, odsalania i zużycia mediów, a także obserwacje z rewizji instalacji. Wnioski zapisujemy w raporcie wraz z rekomendacjami kolejnych korekt."),
        ],
        "cta_kicker": "Program dla kotłowni",
        "cta_title": "Dobierzmy KCAQUA do warunków Państwa instalacji.",
        "cta_text": "Na pierwszą rozmowę wystarczą podstawowe parametry i opis obecnego sposobu prowadzenia wody. Wskażemy, które dane warto uzupełnić przed doborem programu.",
        "cta_primary_label": "Umów rozmowę techniczną",
        "cta_primary_href": "/bezplatna-konsultacja/",
    },
    {
        "path": "/biale-certyfikaty/",
        "slug": "certificates",
        "style": "boilers",
        "layout": "editorial",
        "sequence": ("diagnosis", "results", "method", "data"),
        "title": "Białe certyfikaty dla przemysłu | Kabi-Chemie",
        "meta": "Wstępna kwalifikacja inwestycji, audyt efektywności energetycznej i wsparcie procesu uzyskania białych certyfikatów dla modernizacji przemysłowych.",
        "image": "/assets/visuals-v2/hero-white-certificates-v2.jpg",
        "image_position": "67% center",
        "kicker": "Efektywność energetyczna / Białe certyfikaty",
        "h1_html": "Białe certyfikaty <span>dla modernizacji przemysłu.</span>",
        "lead": "Pomagamy ocenić, czy planowana modernizacja ograniczająca zużycie energii może wejść do systemu świadectw efektywności energetycznej. Porządkujemy dane, audyt i dokumentację przed rozpoczęciem inwestycji.",
        "primary_label": "Sprawdź kwalifikację inwestycji",
        "primary_href": "/bezplatna-konsultacja/",
        "secondary_label": "Policz potencjał oszczędności",
        "secondary_href": "/kalkulator-oszczednosci/",
        "signals": [("qualify", "Wstępna kwalifikacja"), ("energy", "Audyt efektywności"),
                    ("docs", "Wsparcie dokumentacji")],
        "chapter": "04",
        "chapter_label": "Efektywność",
        "proof": [
            ("Przed inwestycją", "Harmonogram procedury ustalamy przed rozpoczęciem prac."),
            ("Audyt energetyczny", "Oszczędność opisujemy metodą możliwą do zweryfikowania."),
            ("Decyzja URE", "O wydaniu świadectwa ostatecznie decyduje Prezes URE."),
        ],
        "issues_kicker": "Wstępna kwalifikacja",
        "issues_title": "Najpierw sprawdzamy podstawy projektu.",
        "issues_intro": "Biały certyfikat nie jest automatyczną dotacją do każdej modernizacji. Potrzebne są mierzalne oszczędności energii, właściwy moment złożenia wniosku i dokumentacja zgodna z wymaganiami systemu.",
        "issues": [
            ("Projekt jest dopiero planowany", "Co do zasady procedurę trzeba rozpocząć przed zawarciem zobowiązań i rozpoczęciem przedsięwzięcia. Termin sprawdzamy na samym początku.", "Moment zgłoszenia"),
            ("Oszczędność można policzyć", "Punkt odniesienia, sposób obliczeń i założenia muszą pokazywać oszczędność energii finalnej w sposób możliwy do oceny.", "Metodyka"),
            ("Zakres mieści się w systemie", "Weryfikujemy rodzaj modernizacji, warunki kwalifikacji i dostępność danych potrzebnych do audytu.", "Kwalifikowalność"),
            ("Dokumentacja jest kompletna", "Spójność audytu, projektu i wniosku ogranicza ryzyko pytań, korekt oraz opóźnień w postępowaniu.", "Formalności"),
        ],
        "method_image": "/assets/industries/industry-heavy.jpg",
        "method_position": "56% center",
        "process_kicker": "Przebieg współpracy",
        "process_title": "Od oceny projektu do poprawnego wniosku.",
        "process_intro": "Każdy etap ma punkt kontrolny. Jeżeli projekt nie spełnia podstawowych warunków, klient dowiaduje się o tym przed kosztowną pracą dokumentacyjną.",
        "process_entry": "Opis modernizacji i dane o energii",
        "process_exit": "Kompletny wniosek i plan potwierdzenia efektu",
        "process_stages": ["Sprawdzamy", "Liczymy", "Dokumentujemy", "Wspieramy"],
        "process_results": ["Decyzja o kwalifikacji", "Model oszczędności", "Audyt i wniosek", "Wsparcie postępowania"],
        "process": [
            ("Prekwalifikacja", "Poznajemy zakres inwestycji, przewidywany harmonogram, zużycie energii i dostępne dane techniczne."),
            ("Model oszczędności", "Ustalamy stan odniesienia, wariant po modernizacji i sposób obliczenia energii finalnej."),
            ("Audyt i dokumentacja", "Przygotowujemy lub porządkujemy audyt efektywności energetycznej oraz materiały potrzebne do wniosku."),
            ("Wsparcie postępowania", "Pomagamy w wyjaśnieniach i uzupełnieniach, a po realizacji porządkujemy dane potrzebne do potwierdzenia efektu."),
        ],
        "outcomes_kicker": "Wartość dla inwestora",
        "outcomes_title": "Decyzja oparta na danych i realnym efekcie.",
        "outcomes_intro": "Klient otrzymuje rzetelną ocenę projektu i dokumentację, która łączy technikę, energię oraz wymogi procedury.",
        "outcomes_href": "/bezplatna-konsultacja/",
        "outcomes_link": "Zobacz zakres audytu technicznego",
        "outcomes": [
            ("Wcześniejsza ocena szans", "Projekt można uporządkować lub zatrzymać, zanim powstaną niepotrzebne koszty dokumentacji."),
            ("Czytelny bilans energii", "Założenia, dane wejściowe i wynik są zrozumiałe dla inwestora oraz osób oceniających projekt."),
            ("Spójna dokumentacja", "Audyt, opis techniczny i harmonogram przedsięwzięcia mówią o tym samym zakresie."),
            ("Wsparcie w komunikacji", "Pomagamy odpowiadać na pytania techniczne i porządkować wymagane uzupełnienia."),
        ],
        "data_kicker": "Dane do oceny",
        "data_title": "Dane potrzebne do kwalifikacji projektu.",
        "data_intro": "Na pierwszym etapie nie potrzebujemy gotowego audytu. Wystarczy opis planowanej zmiany i dane pozwalające oszacować skalę oszczędności.",
        "data_rows": [
            ("Zakres modernizacji", "Co ma zostać wymienione, zmienione lub zoptymalizowane oraz jaki problem techniczny rozwiązuje projekt."),
            ("Stan przed inwestycją", "Zużycie energii, godziny pracy, obciążenie, parametry urządzeń i dostępne dane historyczne."),
            ("Wariant po modernizacji", "Oferta, projekt, karty urządzeń, zakładane parametry i planowany termin realizacji."),
            ("Harmonogram decyzji", "Planowane zamówienia, umowy i rozpoczęcie prac, które mogą mieć znaczenie dla prawidłowej kolejności procedury."),
        ],
        "data_icons": ["scope", "survey", "energy", "calendar"],
        "related": [
            ("Narzędzie", "Kalkulator oszczędności", "/kalkulator-oszczednosci/"),
            ("Usługa", "Audyt techniczny instalacji", "/bezplatna-konsultacja/"),
            ("Kontakt", "Rozmowa z inżynierem", "/bezplatna-konsultacja/"),
        ],
        "faq_title": "Pytania o białe certyfikaty.",
        "faq_intro": "Najważniejsze kwestie, które warto wyjaśnić przed podpisaniem umów i rozpoczęciem modernizacji.",
        "faq": [
            ("Czym jest biały certyfikat?", "Biały certyfikat to świadectwo efektywności energetycznej wydawane przez Prezesa URE. Potwierdza oszczędność energii finalnej wynikającą z przedsięwzięcia, a związane z nim prawa majątkowe mogą mieć wartość ekonomiczną."),
            ("Kiedy należy rozpocząć procedurę?", "Co do zasady przed rozpoczęciem przedsięwzięcia. Moment zawarcia umowy, złożenia zamówienia lub rozpoczęcia prac może mieć znaczenie, dlatego harmonogram trzeba zweryfikować przed podjęciem zobowiązań."),
            ("Czy każda modernizacja ograniczająca energię kwalifikuje się do systemu?", "Nie. Projekt musi spełniać warunki wynikające z przepisów i aktualnych zasad systemu, a oszczędność powinna być potwierdzona audytem. Wstępna kwalifikacja pozwala ocenić to przed przygotowaniem pełnej dokumentacji."),
            ("Czy program chemiczny lub modernizacja instalacji wodnej może być podstawą wniosku?", "Może, jeżeli planowane działanie prowadzi do mierzalnej oszczędności energii finalnej i spełnia warunki systemu. Każdy przypadek wymaga osobnej oceny zakresu, punktu odniesienia i sposobu potwierdzenia efektu."),
            ("Czy Kabi-Chemie gwarantuje wydanie świadectwa?", "Nie. O wydaniu świadectwa decyduje Prezes URE. Naszą rolą jest rzetelna kwalifikacja techniczna, przygotowanie obliczeń i dokumentacji oraz wsparcie klienta w przebiegu postępowania."),
        ],
        "cta_kicker": "Zanim rozpoczną się prace",
        "cta_title": "Oceńmy potencjał projektu przed decyzją o inwestycji.",
        "cta_text": "Krótka prekwalifikacja pozwoli ocenić zakres, dane i właściwą kolejność dalszych działań.",
        "cta_primary_label": "Umów wstępną kwalifikację",
        "cta_primary_href": "/bezplatna-konsultacja/",
    },
    {
        "path": "/membrany-ro/",
        "slug": "ro",
        "layout": "ro",
        "sequence": ("diagnosis", "data", "method", "results"),
        "title": "Ochrona membran RO i dobór antyskalantu | Kabi-Chemie",
        "meta": "Ochrona przemysłowych membran RO przed skalowaniem, foulingiem i utlenianiem. Analiza wody, dobór antyskalantu, dozowanie, monitoring i wsparcie CIP.",
        "image": "/assets/visuals-v2/hero-ro-v2.jpg",
        "image_position": "65% center",
        "kicker": "Rozwiązania / Membrany RO",
        "h1_html": "Ochrona membran RO.<br><span>Stabilna wydajność stacji.</span>",
        "lead": "Dobieramy ochronę membran do składu wody, odzysku i warunków pracy. Łączymy antyskalant, kontrolę dozowania i analizę trendów, aby ograniczyć spadki wydajności oraz niepotrzebne mycia CIP.",
        "primary_label": "Sprawdź ochronę membran",
        "primary_href": "/bezplatna-konsultacja/",
        "secondary_label": "Przejdź do bazy wiedzy RO",
        "secondary_href": "/baza-wiedzy/membrany-ro/",
        "signals": ["Skalowanie", "Fouling i biofouling", "Utlenianie membran"],
        "chapter": "05",
        "chapter_label": "Membrany RO",
        "proof": [
            ("Analiza wody", "Ryzyko oceniamy dla rzeczywistego składu zasilania."),
            ("Dobór dawki", "Antyskalant łączymy z odzyskiem i warunkami pracy."),
            ("Trendy RO", "Wynik oceniamy na danych znormalizowanych, nie na wrażeniu."),
        ],
        "issues_kicker": "Diagnoza stacji RO",
        "issues_title": "Spadek wydajności ma konkretną przyczynę.",
        "issues_intro": "Rosnące ciśnienie lub mniejszy strumień permeatu nie zawsze oznaczają ten sam problem. Analiza trendów i wody pozwala oddzielić skalowanie od foulingu, biofoulingu oraz uszkodzenia warstwy aktywnej.",
        "issues": [
            ("Skalowanie solami", "Przekroczenie rozpuszczalności soli w koncentracie tworzy osad, który ogranicza przepływ i zwiększa opory membran.", "Antyskalant"),
            ("Fouling koloidalny i organiczny", "Cząstki oraz związki organiczne odkładają się na powierzchni i mogą skracać cykl między myciami.", "Wstępne uzdatnianie"),
            ("Biofouling", "Rozwój biologiczny tworzy trudną do usunięcia warstwę, powoduje wzrost różnicy ciśnień i niestabilną pracę.", "Kontrola biologiczna"),
            ("Utlenianie membrany", "Wolny chlor i inne utleniacze mogą trwale uszkodzić typowe membrany poliamidowe oraz obniżyć retencję soli.", "Ochrona materiału"),
        ],
        "process_kicker": "Program ochrony RO",
        "process_title": "Najpierw projekcja, potem dawka i kontrola.",
        "process_intro": "Nie korygujemy instalacji wyłącznie na podstawie bieżącej przewodności permeatu. Oceniamy cały układ i jego zachowanie w czasie.",
        "process": [
            ("Analiza zasilania", "Badamy skład jonowy, pH, temperaturę, przewodność, potencjał foulingu i obecność utleniaczy."),
            ("Projekcja i dobór", "Oceniamy ryzyko wytrącania przy planowanym odzysku oraz dobieramy preparat i dawkę."),
            ("Uruchomienie dozowania", "Sprawdzamy pompę, punkt wtrysku, mieszanie, zabezpieczenia i zgodność nastaw z przepływem."),
            ("Normalizacja wyników", "Śledzimy przepływ, retencję soli i ciśnienia po korekcie temperatury oraz warunków zasilania."),
        ],
        "outcomes_kicker": "Efekt dla stacji",
        "outcomes_title": "Trendy wspierają stabilną pracę membran.",
        "outcomes_intro": "Ochrona RO ma utrzymać parametry procesu, a nie tylko przesunąć termin kolejnego mycia.",
        "outcomes_href": "/baza-wiedzy/membrany-ro/",
        "outcomes_link": "Poznaj zasady ochrony RO",
        "outcomes": [
            ("Dłuższe cykle między CIP", "Ograniczenie osadu i foulingu może zmniejszyć częstotliwość myć oraz przestojów."),
            ("Stabilny strumień permeatu", "Prawidłowo prowadzona stacja utrzymuje wydajność w przewidywalnym zakresie."),
            ("Niższe opory hydrauliczne", "Czystsze kanały przepływowe ograniczają niepotrzebny wzrost ciśnienia i energii."),
            ("Lepsza ochrona inwestycji", "Kontrola utleniaczy, osadów i mycia wspiera dłuższą eksploatację elementów membranowych."),
        ],
        "data_kicker": "Monitoring RO",
        "data_title": "Trendy, które pokazują stan membran.",
        "data_intro": "Dane procesowe zestawiamy z wynikami wody zasilającej i historią zmian w instalacji.",
        "data_rows": [
            ("Woda zasilająca", "Pełny skład jonowy, pH, temperatura, przewodność, krzemionka, żelazo, SDI i wolny chlor, zależnie od układu."),
            ("Warunki pracy", "Przepływy zasilania, permeatu i koncentratu, odzysk, ciśnienia na stopniach oraz temperatura."),
            ("Wydajność membran", "Znormalizowany przepływ permeatu, retencja soli, różnica ciśnień i przewodność na stopniach."),
            ("Historia eksploatacji", "Mycia CIP, wymiany wkładów, zmiany źródła wody, alarmy, dawki chemii i wcześniejsze uszkodzenia."),
        ],
        "related": [
            ("Wiedza", "Antyskalanty i membrany RO", "/baza-wiedzy/membrany-ro/"),
            ("Usługa", "Analiza wody", "/uslugi/analiza-wody/"),
            ("Serwis", "Automatyka i dozowanie", "/uslugi/serwis-urzadzen/"),
        ],
        "faq_title": "Pytania o wydajność i ochronę RO.",
        "faq_intro": "O diagnozie, antyskalancie, monitoringu i właściwym momencie mycia CIP.",
        "faq": [
            ("Jak odróżnić skalowanie od biofoulingu?", "Porównujemy przebieg różnicy ciśnień, znormalizowanego przepływu i retencji soli z analizą wody, historią pracy oraz osadem z filtrów lub CIP. Sama przewodność permeatu nie pozwala wiarygodnie wskazać przyczyny."),
            ("Czy antyskalant rozwiąże każdy problem ze spadkiem wydajności?", "Nie. Antyskalant ogranicza ryzyko wytrącania określonych soli. Nie zastąpi właściwej filtracji wstępnej, kontroli biologicznej, ochrony przed utleniaczami ani prawidłowego mycia membran."),
            ("Jak dobierana jest dawka antyskalantu?", "Na podstawie składu jonowego wody, pH, temperatury, zakładanego odzysku i warunków koncentratu. Dobór powinien uwzględniać także ograniczenia producenta membran i rzeczywistą stabilność dozowania."),
            ("Które parametry warto śledzić codziennie?", "Przepływy, ciśnienia, różnicę ciśnień, przewodność permeatu i koncentratu, odzysk oraz temperaturę. Do oceny kondycji membran wartości należy normalizować i analizować jako trend."),
            ("Kiedy wykonać mycie CIP?", "Decyzję opieramy na zmianie znormalizowanego przepływu, retencji soli i różnicy ciśnień oraz na zaleceniach producenta membran. Zbyt późne mycie może utrwalić osad, a zbyt częste niepotrzebnie obciąża membrany i produkcję."),
        ],
        "cta_kicker": "Diagnoza przed korektą",
        "cta_title": "Sprawdźmy, co ogranicza wydajność stacji RO.",
        "cta_text": "Prześlij podstawowe parametry i opis trendu. Pomożemy ustalić, czy kolejny krok to korekta antyskalantu, uzdatniania wstępnego, automatyki czy procedury CIP.",
        "cta_primary_label": "Umów konsultację RO",
        "cta_primary_href": "/bezplatna-konsultacja/",
    },
    {
        "path": "/uslugi/serwis-urzadzen/",
        "slug": "service",
        "layout": "field",
        "sequence": ("diagnosis", "results", "method", "data"),
        "title": "Serwis i automatyka uzdatniania wody | Kabi-Chemie",
        "meta": "Serwis stacji uzdatniania wody, pomp dozujących, sond i sterowników. Diagnostyka, kalibracja, naprawa, uruchomienie oraz protokół z zaleceniami.",
        "image": "/assets/visuals-v2/hero-service-v2.jpg",
        "image_position": "68% center",
        "kicker": "Usługi / Serwis i automatyka",
        "h1_html": "Serwis i automatyka<br><span>uzdatniania wody.</span>",
        "lead": "Diagnozujemy, kalibrujemy i uruchamiamy urządzenia, które odpowiadają za jakość wody oraz dozowanie chemii. Jeden zespół łączy mechanikę, pomiar, sterowanie i proces technologiczny.",
        "primary_label": "Zgłoś urządzenie do serwisu",
        "primary_href": "/kontakt/",
        "secondary_label": "Umów audyt techniczny",
        "secondary_href": "/bezplatna-konsultacja/",
        "signals": ["Stacje SUW i RO", "Pompy dozujące", "Sondy i sterowniki"],
        "chapter": "06",
        "chapter_label": "Serwis",
        "proof": [
            ("Diagnoza", "Ustalamy przyczynę, nie tylko kasujemy objaw."),
            ("Kalibracja", "Pomiar i dawkę potwierdzamy w rzeczywistych warunkach."),
            ("Protokół", "Po wizycie zostaje zakres prac i lista zaleceń."),
        ],
        "issues_kicker": "Zakres serwisu",
        "issues_title": "Sprawne urządzenie musi działać w całym procesie.",
        "issues_intro": "Pompa może pracować, a mimo to podawać niewłaściwą dawkę. Sonda może wyświetlać wynik, ale sterować odsalaniem na błędnej podstawie. Dlatego testujemy cały tor od pomiaru do reakcji instalacji.",
        "issues": [
            ("Pompy i układy dozowania", "Sprawdzamy wydajność, szczelność, zawory, przewody, punkt wtrysku i reakcję na sygnał sterujący.", "Chemia"),
            ("Sondy i analizatory", "Czyścimy, kalibrujemy i weryfikujemy wskazania przewodności, pH oraz innych pomiarów procesowych.", "Pomiar"),
            ("Sterowniki i automatyka", "Kontrolujemy progi, alarmy, wyjścia, harmonogramy oraz logikę odsalania i dozowania.", "Sterowanie"),
            ("Stacje uzdatniania", "Diagnozujemy zmiękczacze, filtrację, RO i urządzenia pomocnicze w kontekście wymagań całej instalacji.", "Uzdatnianie"),
        ],
        "process_kicker": "Przebieg wizyty",
        "process_title": "Od diagnozy do uruchomienia.",
        "process_intro": "Przed przyjazdem zbieramy podstawowe informacje, aby technik miał właściwe narzędzia i możliwie szybko przeszedł do diagnozy.",
        "process": [
            ("Rozpoznanie zgłoszenia", "Ustalamy urządzenie, objawy, alarmy, wpływ na produkcję oraz dostępne zdjęcia i dokumentację."),
            ("Diagnostyka na obiekcie", "Sprawdzamy zasilanie, hydraulikę, elementy wykonawcze, czujniki i logikę sterowania."),
            ("Naprawa i kalibracja", "Usuwamy usterkę, ustawiamy urządzenie i potwierdzamy rzeczywistą wydajność lub dokładność pomiaru."),
            ("Test i protokół", "Uruchamiamy układ w warunkach roboczych, zapisujemy wyniki oraz wskazujemy działania zapobiegawcze."),
        ],
        "outcomes_kicker": "Efekt serwisu",
        "outcomes_title": "Mniej interwencji, większa kontrola procesu.",
        "outcomes_intro": "Dobrze utrzymana automatyka pozwala programowi chemicznemu działać stabilnie i przewidywalnie.",
        "outcomes_href": "/kontakt/",
        "outcomes_link": "Skontaktuj się z serwisem",
        "outcomes": [
            ("Wiarygodne pomiary", "Skalibrowane sondy dają podstawę do prawidłowych decyzji i alarmów."),
            ("Powtarzalne dozowanie", "Sprawna pompa podaje dawkę adekwatną do nastawy i rzeczywistego przepływu."),
            ("Krótsza diagnoza awarii", "Uporządkowana dokumentacja i historia serwisu ułatwiają kolejne interwencje."),
            ("Plan zamiast niespodzianki", "Zalecenia po wizycie pomagają zaplanować części, przeglądy i modernizacje."),
        ],
        "data_kicker": "Przed zgłoszeniem",
        "data_title": "Informacje, które usprawniają serwis.",
        "data_intro": "Jeżeli nie masz wszystkich danych, wyślij to, co jest dostępne. Resztę ustalimy telefonicznie lub na obiekcie.",
        "data_rows": [
            ("Identyfikacja urządzenia", "Producent, model, zdjęcie tabliczki znamionowej i krótki opis funkcji w instalacji."),
            ("Objawy i alarmy", "Co się zmieniło, od kiedy występuje problem i czy urządzenie zatrzymuje lub ogranicza proces."),
            ("Warunki pracy", "Medium, ciśnienie, przepływ, używana chemia, ostatnie nastawy i warunki otoczenia."),
            ("Historia obsługi", "Ostatni przegląd, wymieniane części, wcześniejsze awarie i dostępne protokoły."),
        ],
        "related": [
            ("Usługa", "Audyt techniczny", "/bezplatna-konsultacja/"),
            ("Usługa", "Analiza wody", "/uslugi/analiza-wody/"),
            ("Technologia", "Program KCAQUA", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
        ],
        "faq_title": "Pytania przed zgłoszeniem serwisu.",
        "faq_intro": "O przygotowaniu wizyty, zakresie urządzeń, kalibracji i dokumentacji po pracach.",
        "faq": [
            ("Jakie informacje warto podać przy zgłoszeniu awarii?", "Najbardziej pomagają zdjęcie tabliczki znamionowej, krótki opis objawu, komunikat alarmu, informacja o wpływie na produkcję i termin ostatniego serwisu. Na tej podstawie ustalamy priorytet oraz przygotowanie technika."),
            ("Czy serwisujecie urządzenia różnych producentów?", "Obsługujemy wiele urządzeń stosowanych w przemysłowym uzdatnianiu i dozowaniu. Możliwość naprawy oraz dostępność części potwierdzamy po identyfikacji modelu i zakresu usterki."),
            ("Czy serwis obejmuje pompy dozujące i sondy?", "Tak. Sprawdzamy wydajność pomp, szczelność, zawory i sterowanie, a sondy czyścimy, kalibrujemy oraz porównujemy z pomiarem odniesienia."),
            ("Czy po wizycie otrzymamy protokół?", "Tak. Protokół opisuje wykonane czynności, wyniki testów, wykryte ryzyka, zastosowane części i zalecenia dotyczące dalszej eksploatacji."),
            ("Czy można ustalić stały harmonogram przeglądów?", "Tak. Częstotliwość dobieramy do znaczenia urządzenia dla procesu, warunków pracy, zaleceń producenta i historii usterek. Harmonogram może obejmować również kalibrację pomiarów i kontrolę dozowania."),
        ],
        "cta_kicker": "Zgłoszenie serwisowe",
        "cta_title": "Omówmy urządzenie i właściwy zakres serwisu.",
        "cta_text": "Ocenimy pilność, poprosimy o potrzebne dane i ustalimy, czy problem wymaga wizyty, części czy konsultacji zdalnej.",
        "cta_primary_label": "Przejdź do kontaktu",
        "cta_primary_href": "/kontakt/",
    },
    {
        "path": "/odkamienianie-instalacji/",
        "slug": "descaling",
        "layout": "evidence",
        "sequence": ("method", "diagnosis", "results", "data"),
        "title": "Odkamienianie instalacji przemysłowych | Kabi-Chemie",
        "meta": "Kontrolowane odkamienianie wymienników, rurociągów i obiegów przemysłowych. Rozpoznanie osadu, dobór procesu, płukanie, neutralizacja i zalecenia eksploatacyjne.",
        "image": "/assets/visuals-v2/hero-descaling-v2.jpg",
        "image_position": "center center",
        "kicker": "Rozwiązania / Odkamienianie instalacji",
        "h1_html": "Odkamienianie instalacji.<br><span>Kontrolowany powrót sprawności.</span>",
        "lead": "Rozpoznajemy rodzaj osadu, materiał instalacji i warunki procesu, a następnie projektujemy bezpieczne czyszczenie w obiegu zamkniętym. Każdy etap prowadzimy na pomiarach, od pierwszej próbki po płukanie i zalecenia po uruchomieniu.",
        "primary_label": "Omów czyszczenie instalacji",
        "primary_href": "/kontakt/",
        "secondary_label": "Zobacz odkamienianie kotłów",
        "secondary_href": "/kotly-parowe/odkamienianie/",
        "signals": ["Wymienniki ciepła", "Rurociągi i obiegi", "Skraplacze i kotły"],
        "chapter": "07",
        "chapter_label": "Odkamienianie",
        "proof": [
            ("Dobór do osadu", "Proces ustalamy po rozpoznaniu składu i grubości złogów."),
            ("Ochrona materiału", "Uwzględniamy stal, miedź, aluminium, uszczelnienia i powłoki."),
            ("Kontrola procesu", "Monitorujemy obieg, temperaturę, odczyn i zakończenie reakcji."),
        ],
        "issues_kicker": "Kiedy instalacja traci wydajność",
        "issues_title": "Osad zmienia warunki pracy instalacji.",
        "issues_intro": "Spadek wymiany ciepła, rosnące opory przepływu i niestabilne temperatury często mają wspólne źródło. Przed czyszczeniem oddzielamy kamień mineralny od produktów korozji, zanieczyszczeń procesowych i biofilmu.",
        "issues": [
            ("Gorsza wymiana ciepła", "Warstwa osadu ogranicza kontakt medium z powierzchnią i zwiększa energię potrzebną do osiągnięcia zadanych parametrów.", "Energia"),
            ("Rosnące opory przepływu", "Zwężenie przekroju utrudnia cyrkulację, obciąża pompy i może ograniczać wydajność całego procesu.", "Hydraulika"),
            ("Korozja pod osadem", "Złogi tworzą lokalne warunki sprzyjające wżerom i utrudniają skuteczne działanie programu ochronnego.", "Trwałość"),
            ("Nieplanowane postoje", "Czyszczenie wykonywane dopiero po alarmie wymaga szybkich decyzji i ogranicza możliwość spokojnego przygotowania procesu.", "Dostępność"),
        ],
        "process_kicker": "Przebieg prac",
        "process_title": "Czyszczenie dopasowane do konkretnej instalacji.",
        "process_intro": "Zakres ustalamy po analizie osadu i warunków ruchowych. Dzięki temu zespół klienta zna kolejność prac, kryteria zakończenia oraz warunki bezpiecznego powrotu do produkcji.",
        "process": [
            ("Rozpoznanie instalacji", "Zbieramy historię pracy, parametry, materiały, objawy i informacje o wcześniejszych czyszczeniach."),
            ("Próba i dobór procesu", "Oceniamy reakcję osadu, kompatybilność materiałową, stężenie, temperaturę i potrzebny czas kontaktu."),
            ("Kontrolowany obieg", "Prowadzimy cyrkulację środka czyszczącego, obserwujemy parametry i dokumentujemy przebieg reakcji."),
            ("Płukanie i zabezpieczenie", "Neutralizujemy pozostałości, potwierdzamy warunki końcowe i określamy sposób ochrony powierzchni po czyszczeniu."),
        ],
        "outcomes_kicker": "Efekt techniczny",
        "outcomes_title": "Czysta powierzchnia przywraca wymianę ciepła.",
        "outcomes_intro": "Po zakończeniu prac oceniamy rezultat w parametrach istotnych dla danego urządzenia, a nie wyłącznie na podstawie wyglądu wypłukanego osadu.",
        "outcomes_href": "/kalkulator-oszczednosci/",
        "outcomes_link": "Sprawdź potencjał odzyskania kosztów",
        "outcomes": [
            ("Sprawniejsza wymiana ciepła", "Odsłonięta powierzchnia może skuteczniej przekazywać energię pomiędzy mediami."),
            ("Niższe opory przepływu", "Usunięcie złogów przywraca dostępny przekrój i ułatwia stabilną cyrkulację."),
            ("Lepsze warunki ochrony", "Program antykorozyjny i kondycjonowanie działają na oczyszczonej, dostępnej powierzchni."),
            ("Plan dalszej eksploatacji", "Raport wskazuje przyczynę osadu, wykonane prace i działania ograniczające jego powrót."),
        ],
        "data_kicker": "Przed przygotowaniem oferty",
        "data_title": "Bezpieczne czyszczenie zaczyna się od diagnozy.",
        "data_intro": "Na pierwszą rozmowę wystarczy opis instalacji i objawów. Brakujące dane techniczne oraz potrzebne próby ustalamy wspólnie.",
        "data_rows": [
            ("Urządzenie i materiały", "Typ wymiennika lub obiegu, pojemność, schemat, materiały konstrukcyjne, uszczelnienia i dostępne króćce."),
            ("Objawy eksploatacyjne", "Zmiany temperatury, przepływu, ciśnienia, zużycia energii, alarmów i częstotliwości postojów."),
            ("Charakter osadu", "Zdjęcia, próbka, dostępne analizy, twardość wody, żelazo i informacje o zanieczyszczeniach procesowych."),
            ("Warunki organizacyjne", "Dostępny czas postoju, miejsce ustawienia układu czyszczącego, odbiór popłuczyn i wymagania BHP zakładu."),
        ],
        "related": [
            ("Usługa", "Chemiczne czyszczenie instalacji", "/ochrona-antykorozyjna/chemiczne-czyszczenie/"),
            ("Rozwiązanie", "Ochrona antykorozyjna", "/ochrona-antykorozyjna/"),
            ("Analiza", "Badanie wody przemysłowej", "/uslugi/analiza-wody/"),
        ],
        "faq_title": "Pytania przed odkamienianiem instalacji.",
        "faq_intro": "O bezpieczeństwie materiałów, przygotowaniu postoju, kontroli procesu i działaniach po czyszczeniu.",
        "faq": [
            ("Czy instalację trzeba demontować?", "W wielu przypadkach czyszczenie prowadzimy w obiegu zamkniętym przez dostępne króćce, bez demontażu urządzenia. Ostateczny sposób zależy od geometrii, przepływu, rodzaju osadu i możliwości bezpiecznego odseparowania instalacji."),
            ("Skąd wiadomo, jaki preparat zastosować?", "Dobór opieramy na próbce osadu, materiałach konstrukcyjnych i warunkach pracy. Sprawdzamy skuteczność reakcji oraz kompatybilność z metalami, uszczelnieniami i elementami pomocniczymi."),
            ("Jak kontrolowany jest proces czyszczenia?", "Monitorujemy parametry odpowiednie dla zastosowanej technologii, między innymi temperaturę, odczyn, czas, cyrkulację i przebieg reakcji. Kryteria zakończenia ustalamy przed rozpoczęciem prac."),
            ("Co dzieje się z roztworem po czyszczeniu?", "Sposób neutralizacji i zagospodarowania ustalamy zgodnie ze składem kąpieli, warunkami zakładu oraz obowiązującymi wymaganiami. Nie zakładamy automatycznie, że popłuczyny mogą trafić do instalacji ściekowej."),
            ("Jak ograniczyć ponowne narastanie kamienia?", "Po czyszczeniu analizujemy przyczynę osadu. Dalsze działania mogą obejmować korektę jakości wody, dozowania, odsalania, filtracji, parametrów procesu lub częstotliwości kontroli."),
        ],
        "cta_kicker": "Instalacja wymaga oceny?",
        "cta_title": "Omówmy objawy i bezpieczny zakres czyszczenia.",
        "cta_text": "Zdjęcia, schemat i podstawowe parametry pomogą ocenić, czy potrzebna jest próbka osadu, wizyta techniczna czy od razu plan czyszczenia.",
        "cta_primary_label": "Skonsultuj odkamienianie",
        "cta_primary_href": "/kontakt/",
    },
    {
        "path": "/ochrona-antykorozyjna/",
        "slug": "corrosion",
        "style": "boilers",
        "layout": "editorial",
        "sequence": ("diagnosis", "results", "method", "data"),
        "title": "Ochrona antykorozyjna instalacji przemysłowych | Kabi-Chemie",
        "meta": "Programy ochrony antykorozyjnej dla instalacji przemysłowych. Diagnoza mechanizmu korozji, inhibitory, pasywacja, kontrola wody i monitoring efektów.",
        "image": "/assets/visuals-v2/hero-corrosion-v2.jpg",
        "image_position": "center center",
        "kicker": "Rozwiązania / Ochrona antykorozyjna",
        "h1_html": "Ochrona antykorozyjna. <span>Program oparty na przyczynie.</span>",
        "lead": "Łączymy ocenę wody, materiałów i warunków pracy z właściwym programem chemicznym, pasywacją oraz monitoringiem. Celem jest stabilna ochrona instalacji, którą można potwierdzać pomiarami i obserwacją trendów.",
        "primary_label": "Omów ochronę instalacji",
        "primary_href": "/kontakt/",
        "secondary_label": "Poznaj pasywację stali",
        "secondary_href": "/ochrona-antykorozyjna/pasywacja-stali/",
        "signals": [("steel", "Stal węglowa i nierdzewna"), ("circuit", "Obiegi wodne i kondensat"),
                    ("passivation", "Pasywacja i monitoring")],
        "chapter": "08",
        "chapter_label": "Antykorozja",
        "proof": [
            ("Mechanizm korozji", "Najpierw ustalamy, co rzeczywiście niszczy powierzchnię."),
            ("Program do instalacji", "Chemię i parametry dobieramy do materiału oraz procesu."),
            ("Ocena w czasie", "Ochronę potwierdzamy trendami wody, żelaza i stanu urządzeń."),
        ],
        "issues_kicker": "Diagnoza ryzyka",
        "issues_title": "Objaw korozji wymaga rozpoznania mechanizmu.",
        "issues_intro": "Wżery, rdza, osad i rosnące stężenie żelaza mogą wynikać z różnych warunków. Oceniamy tlen, pH, przewodność, temperaturę, prędkość przepływu, materiały i historię pracy, zanim dobierzemy ochronę.",
        "issues": [
            ("Tlen i niewłaściwe pH", "Rozpuszczony tlen oraz odczyn poza właściwym zakresem przyspieszają korozję stali i powstawanie lokalnych uszkodzeń.", "Chemia wody"),
            ("Korozja pod osadem", "Złogi ograniczają kontakt inhibitora z metalem i tworzą obszary o innych warunkach elektrochemicznych.", "Powierzchnia"),
            ("Materiały połączone w jednym układzie", "Różne metale, niewłaściwe warunki po montażu i prądy błądzące mogą zmieniać lokalne ryzyko korozji.", "Konstrukcja"),
            ("Brak stałej kontroli", "Jednorazowa korekta nie wystarcza, gdy zmieniają się uzupełnienia wody, obciążenie, temperatura lub dozowanie.", "Monitoring"),
        ],
        "method_image": "/assets/blog/blog-corrosion-pipes.png",
        "method_position": "60% center",
        "process_kicker": "Program ochronny",
        "process_title": "Od mapy ryzyka do codziennej kontroli.",
        "process_intro": "Ochrona ma działać w rzeczywistych warunkach zakładu. Ustalamy nie tylko preparat, lecz także sposób przygotowania powierzchni, dozowania, pomiarów i reakcji na odchylenia.",
        "process_entry": "Opis instalacji, materiały i wyniki wody",
        "process_exit": "Program ochrony i plan kontroli",
        "process_stages": ["Rozpoznajemy", "Przygotowujemy", "Dobieramy", "Nadzorujemy"],
        "process_results": ["Mechanizm korozji", "Powierzchnia gotowa", "Program i nastawy", "Trwała ochrona"],
        "process": [
            ("Ocena instalacji", "Rozpoznajemy materiały, miejsca awarii, jakość wody, temperaturę, przepływ i dotychczasowe działania ochronne."),
            ("Przygotowanie powierzchni", "Gdy jest to potrzebne, planujemy usunięcie produktów korozji, czyszczenie i warunki prawidłowej pasywacji."),
            ("Dobór programu", "Ustalamy funkcje inhibitora, dawkę, parametry docelowe, punkt podawania i wymagania wobec automatyki."),
            ("Nadzór i korekty", "Kontrolujemy wodę, żelazo, dozowanie, wygląd powierzchni i dane eksploatacyjne, a program aktualizujemy wraz ze zmianą procesu."),
        ],
        "outcomes_kicker": "Efekt dla utrzymania ruchu",
        "outcomes_title": "Ochrona ogranicza ryzyko i porządkuje serwis.",
        "outcomes_intro": "Skuteczność programu oceniamy w czasie, zestawiając parametry wody ze stanem instalacji i historią interwencji.",
        "outcomes_href": "/baza-wiedzy/korozja/",
        "outcomes_link": "Poznaj mechanizmy korozji",
        "outcomes": [
            ("Mniejsze ryzyko nieszczelności", "Stabilne warunki chemiczne ograniczają tempo degradacji i rozwój lokalnych ognisk korozji."),
            ("Lepsza ochrona po czyszczeniu", "Prawidłowe przygotowanie i pasywacja pomagają zabezpieczyć odsłoniętą powierzchnię metalu."),
            ("Szybsza reakcja na odchylenia", "Ustalone parametry i częstotliwość kontroli pozwalają wcześniej zauważyć zmianę warunków."),
            ("Czytelna historia instalacji", "Raporty łączą pomiary wody, dozowanie, przeglądy i zdarzenia istotne dla trwałości urządzeń."),
        ],
        "data_kicker": "Punkty kontroli",
        "data_title": "Mierzalne parametry skutecznej ochrony.",
        "data_intro": "Zakres pomiarów zależy od instalacji. Wybieramy parametry, które pomagają ocenić mechanizm korozji i potwierdzić działanie ochrony.",
        "data_rows": [
            ("Parametry chemiczne", "pH, przewodność, twardość, zasadowość, chlorki, siarczany, tlen rozpuszczony oraz żelazo, zależnie od układu."),
            ("Warunki procesowe", "Temperatura, ciśnienie, przepływ, postoje, zmienność obciążenia i udział świeżej wody w obiegu."),
            ("Dozowanie i automatyka", "Wydajność pomp, sygnały sterujące, punkt wtrysku, alarmy, zapas preparatu i rzeczywiste zużycie."),
            ("Stan powierzchni", "Oględziny, kupony lub sondy korozyjne, pomiary grubości, produkty korozji i historia nieszczelności."),
        ],
        "data_icons": ["diagnose", "gauge", "dosing", "steel"],
        "related": [
            ("Usługa", "Pasywacja stali", "/ochrona-antykorozyjna/pasywacja-stali/"),
            ("Usługa", "Chemiczne czyszczenie", "/ochrona-antykorozyjna/chemiczne-czyszczenie/"),
            ("Wiedza", "Korozja w instalacjach", "/baza-wiedzy/korozja/"),
        ],
        "faq_title": "Pytania o ochronę antykorozyjną.",
        "faq_intro": "O diagnozie, inhibitorach, pasywacji, pomiarach i ocenie skuteczności programu.",
        "faq": [
            ("Czy inhibitor korozji wystarczy bez wcześniejszego czyszczenia?", "Nie zawsze. Jeżeli powierzchnię pokrywa kamień, produkt korozji lub osad procesowy, preparat może nie docierać równomiernie do metalu. Najpierw oceniamy stan powierzchni i potrzebę przygotowania instalacji."),
            ("Jak ustalacie przyczynę korozji?", "Łączymy analizę wody, materiały, temperaturę, przepływ, miejsca uszkodzeń i historię pracy. W zależności od układu wykorzystujemy także oględziny, pomiar grubości, żelazo w wodzie, kupony lub sondy korozyjne."),
            ("Kiedy potrzebna jest pasywacja?", "Najczęściej po montażu, spawaniu, remoncie lub chemicznym czyszczeniu, gdy powierzchnia wymaga wytworzenia albo odtworzenia stabilnej warstwy ochronnej. Technologię dobieramy do materiału i przeznaczenia instalacji."),
            ("Jak często należy kontrolować program ochronny?", "Częstotliwość zależy od znaczenia instalacji, zmienności obciążenia, jakości uzupełnień i stabilności automatyki. Na początku wdrożenia pomiary zwykle wykonuje się częściej, a po stabilizacji ustala rytm eksploatacyjny."),
            ("Po czym poznać, że program działa?", "Oceniamy trend parametrów wody, stężenie żelaza, zużycie preparatu, wyniki pomiarów powierzchni i historię awarii. Pojedyncza próbka nie wystarcza do rzetelnego potwierdzenia ochrony."),
        ],
        "cta_kicker": "Widzisz rdzę, wżery lub rosnące żelazo?",
        "cta_title": "Ustalmy przyczynę korozji i właściwy sposób ochrony.",
        "cta_text": "Krótki opis instalacji, zdjęcia i ostatnie wyniki wody pozwolą wskazać potrzebne pomiary oraz właściwy kolejny krok.",
        "cta_primary_label": "Skonsultuj ochronę instalacji",
        "cta_primary_href": "/kontakt/",
    },
    {
        "path": "/uslugi/analiza-wody/",
        "slug": "analysis",
        "style": "boilers",
        "layout": "editorial",
        "sequence": ("diagnosis", "results", "method", "data"),
        "title": "Analiza wody przemysłowej | Kabi-Chemie",
        "meta": "Analiza wody kotłowej, chłodniczej i technologicznej. Pomiar parametrów, interpretacja wyników oraz raport z rekomendacją dalszych działań.",
        "image": "/assets/impact/impact-02-effluent-control.jpeg",
        "image_position": "center center",
        "kicker": "Usługi / Analiza wody",
        "h1_html": "Badamy wodę <span>przed awarią instalacji.</span>",
        "lead": "Analiza wody przemysłowej pomaga szybko zobaczyć, czy instalacja pracuje stabilnie. Wynik przekładamy na konkretne decyzje dla kotłowni, chłodnictwa i RO.",
        "primary_label": "Zleć analizę wody",
        "primary_href": "/kontakt/",
        "secondary_label": "Poznaj parametry wody",
        "secondary_href": "/baza-wiedzy/parametry-wody/",
        "signals": [("uptime", "Utrzymanie ruchu i produkcja"), ("diagnose", "Diagnoza kamienia i korozji"),
                    ("report", "Raport z rekomendacją")],
        "chapter": "09",
        "chapter_label": "Analiza wody",
        "proof": [
            ("Pobór próbki", "Miejsce poboru dobieramy do typu instalacji."),
            ("Interpretacja", "Liczby zestawiamy z objawami i pracą urządzeń."),
            ("Rekomendacja", "Wskazujemy jeden konkretny kolejny krok."),
        ],
        "issues_kicker": "Kiedy warto zbadać wodę",
        "issues_title": "Objaw w instalacji widać najpierw w wodzie.",
        "issues_intro": "Analiza ma sens wtedy, gdy odpowiada na pytanie techniczne. Dlatego zawsze zaczynamy od objawu i warunków pracy, a dopiero potem dobieramy zakres pomiarów.",
        "issues": [
            ("Spada wymiana ciepła", "Rosnące zużycie energii i wyższa temperatura procesu zwykle zaczynają się od twardości i narastania osadu.", "Kamień"),
            ("Rdza, wżery i brudny kondensat", "Żelazo w wodzie oraz odczyn poza zakresem wskazują na korozję, zanim pojawi się nieszczelność.", "Korozja"),
            ("Niestabilna praca obiegu", "Zmienna przewodność i zasolenie utrudniają utrzymanie powtarzalnych parametrów procesu.", "Zasolenie"),
            ("Rosnące zużycie wody i ścieków", "Zbyt ostrożne odsalanie podnosi koszty mediów, choć nie poprawia bezpieczeństwa instalacji.", "Koszt mediów"),
        ],
        "outcomes_kicker": "Co otrzymujesz",
        "outcomes_title": "Raport czytelny dla technika i zarządu.",
        "outcomes_intro": "Wynik ma prowadzić do decyzji, a nie kończyć się tabelą liczb. Dlatego każdy parametr opisujemy w kontekście pracy instalacji i kosztów.",
        "outcomes_href": "/baza-wiedzy/parametry-wody/",
        "outcomes_link": "Poznaj znaczenie parametrów wody",
        "outcomes": [
            ("Stan wody na dziś", "Wyniki pomiarów z krótkim komentarzem technicznym, bez laboratoryjnego żargonu."),
            ("Nazwane ryzyko", "Kamień, korozja, biofilm, zasolenie i strata energii opisane dla Twojej instalacji."),
            ("Konkretny kolejny krok", "Korekta dozowania, czyszczenie, pasywacja, audyt albo regularny monitoring."),
            ("Argument dla zarządu", "Raport łączy parametry techniczne z wpływem na koszty eksploatacji."),
        ],
        "method_image": "/assets/blog/blog-parametry-wody.jpg",
        "method_position": "58% center",
        "process_kicker": "Od próbki do decyzji",
        "process_title": "Wynik badania prowadzi do działania.",
        "process_intro": "Każdy etap ma jasny cel. Dzięki temu wiadomo, skąd pochodzi próbka, co mierzymy i dlaczego rekomendujemy dany krok.",
        "process_entry": "Próbka wody i opis instalacji",
        "process_exit": "Raport z rekomendacją",
        "process_stages": ["Pobieramy", "Mierzymy", "Interpretujemy", "Rekomendujemy"],
        "process_results": ["Reprezentatywna próbka", "Zestaw wyników", "Diagnoza", "Plan działania"],
        "process": [
            ("Pobór próbki", "Ustalamy miejsce poboru i typ instalacji, aby wynik miał sens techniczny."),
            ("Pomiar parametrów", "Sprawdzamy wskaźniki właściwe dla wody kotłowej, chłodniczej lub technologicznej."),
            ("Interpretacja", "Łączymy liczby z objawami, pracą instalacji i kosztami eksploatacji."),
            ("Rekomendacja", "Przekazujemy jasny kolejny krok, bez nadmiaru laboratoryjnego żargonu."),
        ],
        "data_kicker": "Zakres badania",
        "data_title": "Parametry dobieramy do instalacji.",
        "data_intro": "Inaczej czytamy wodę kotłową, inaczej wodę w skraplaczu, a jeszcze inaczej układ RO. Zakres ustalamy po rozmowie o instalacji i objawach.",
        "data_rows": [
            ("Odczyn i zasadowość", "pH oraz zasadowość opisują kierunek korozji i stabilność programu chemicznego."),
            ("Twardość i skłonność do osadu", "Ocena ryzyka narastania kamienia na powierzchniach wymiany ciepła."),
            ("Przewodność, TDS i chlorki", "Zasolenie, agresywność wody oraz podstawa do ustawienia odsalania i zrzutów."),
            ("Żelazo i produkty korozji", "Sygnał transportu osadów, korozji instalacji oraz zabrudzenia kondensatu."),
        ],
        "data_icons": ["diagnose", "crystal", "salt", "passivation"],
        "related": [
            ("Wiedza", "Parametry wody przemysłowej", "/baza-wiedzy/parametry-wody/"),
            ("Usługa", "Serwis i automatyka", "/uslugi/serwis-urzadzen/"),
            ("Kontakt", "Rozmowa z inżynierem", "/bezplatna-konsultacja/"),
        ],
        "faq_title": "Pytania o analizę wody.",
        "faq_intro": "O próbce, zakresie badania, interpretacji wyników i tym, co dzieje się po raporcie.",
        "faq": [
            ("Jak pobrać próbkę, aby wynik był wiarygodny?", "Próbkę pobiera się z ustalonego, reprezentatywnego punktu, do czystego naczynia i najlepiej podczas normalnej pracy instalacji. Ważne jest opisanie miejsca poboru, daty i warunków pracy, bo bez tego kontekstu liczby trudno rzetelnie ocenić."),
            ("Jakie parametry są badane?", "Zakres zależy od instalacji. Najczęściej sprawdzamy odczyn, zasadowość, twardość, przewodność, chlorki, TDS oraz żelazo. Dla układów chłodniczych i RO dobieramy dodatkowe wskaźniki związane z ryzykiem osadu, korozji i mikrobiologii."),
            ("Czy jedna analiza wystarczy?", "Pojedynczy wynik pokazuje stan w danym momencie i zwykle wystarcza do wstępnej diagnozy. Ocena skuteczności programu chemicznego wymaga jednak serii pomiarów, ponieważ liczy się trend, a nie pojedynczy odczyt."),
            ("Co dzieje się po otrzymaniu wyników?", "Wyniki omawiamy w kontekście pracy instalacji i wskazujemy kolejny krok: korektę dozowania, czyszczenie, pasywację, audyt techniczny albo regularny monitoring. Nie zostawiamy klienta z samą tabelą liczb."),
            ("Czy trzeba mieć własne laboratorium lub wcześniejsze wyniki?", "Nie. Jeżeli nie masz aktualnych pomiarów, wykonujemy analizę od podstaw. Jeżeli masz wyniki z innego źródła, możemy je odczytać i wskazać, czego brakuje do pełnego obrazu."),
        ],
        "cta_kicker": "Masz aktualne wyniki wody?",
        "cta_title": "Wyślij parametry. Pomożemy je odczytać.",
        "cta_text": "Możesz też zamówić analizę, jeśli nie masz pewnych danych z ostatnich pomiarów. Wystarczy krótki opis instalacji i objawu.",
        "cta_primary_label": "Wyślij zapytanie",
        "cta_primary_href": "/kontakt/",
    },
    {
        "path": "/autoklawy-i-pasteryzatory/",
        "slug": "autoclaves",
        "style": "boilers",
        "layout": "editorial",
        "sequence": ("diagnosis", "method", "results", "data"),
        "title": "Kondycjonowanie wody w autoklawach i pasteryzatorach | Kabi-Chemie",
        "meta": "Ochrona obiegów wodnych autoklawów i pasteryzatorów przed kamieniem i korozją. Analiza wody, dozowanie, monitoring oraz serwis Kabi-Chemie.",
        "image": "/assets/visuals-v2/hero-autoclaves-pasteurizers-v1.webp",
        "image_position": "center center",
        "kicker": "Rozwiązania / Autoklawy i pasteryzatory",
        "h1_html": "Autoklawy i pasteryzatory.",
        "lead": "Stabilizujemy wymianę ciepła, chroniąc obiegi wodne przed kamieniem, korozją i niekontrolowanym zużyciem preparatu.",
        "primary_label": "Sprawdź obieg wodny",
        "primary_href": "/bezplatna-konsultacja/",
        "secondary_label": "Zleć analizę wody",
        "secondary_href": "/uslugi/analiza-wody/",
        "signals": [],
        "issues_kicker": "Diagnoza instalacji",
        "issues_title": "Osad i korozja zmieniają czas cyklu.",
        "issues_intro": "Sprawdzamy obieg w płaszczu urządzenia, instalację zasilającą i chłodzącą oraz sposób dozowania. Dzięki temu oddzielamy problem wody od problemu samego procesu technologicznego.",
        "issues": [
            ("Kamień na powierzchniach wymiany ciepła", "Osad ogranicza przekazywanie energii. Grzanie lub chłodzenie może trwać dłużej, mimo że urządzenie pracuje z tymi samymi nastawami.", "Powtarzalność"),
            ("Zmienna jakość wody uzupełniającej", "Twardość, zasolenie i pH zmieniają ryzyko wytrącania osadu oraz wpływają na stabilność programu chemicznego.", "Parametry wody"),
            ("Korozja płaszcza i rurociągów", "Tlen, chlorki i niewłaściwy odczyn przyspieszają zużycie elementów obiegu oraz zwiększają ryzyko nieszczelności.", "Trwałość"),
            ("Dozowanie bez kontroli obciążenia", "Stała dawka nie zawsze odpowiada liczbie cykli, uzupełnieniom i zrzutom wody. To utrudnia kontrolę zużycia preparatu.", "Koszt mediów"),
        ],
        "process_kicker": "Program dla obiegu wodnego",
        "process_title": '<span class="solution-title-line">Od danych urządzenia</span><span class="solution-title-line">do stabilnych parametrów.</span>',
        "process_intro": "Zakres dobieramy do konstrukcji urządzenia i sposobu pracy zakładu. Każdy etap kończy się konkretną decyzją techniczną.",
        "process_entry": "Schemat obiegu, próbka wody i dane cyklu",
        "process_exit": "Nastawy, monitoring i plan kontroli",
        "process_stages": ["Rozpoznajemy", "Mierzymy", "Dobieramy", "Prowadzimy"],
        "process_results": ["Zakres instalacji", "Punkt odniesienia", "Program i nastawy", "Raport i korekta"],
        "process": [
            ("Bilans obiegu", "Ustalamy źródło wody, materiały, objętość, temperatury, liczbę cykli, uzupełnienia oraz miejsca zrzutu."),
            ("Analiza wody i osadu", "Badamy parametry związane z kamieniem i korozją, a wyniki porównujemy ze stanem powierzchni oraz historią pracy."),
            ("Program chemiczny i dozowanie", "Dobieramy funkcje preparatu KCAQUA, dawkę, punkt podania i sposób sterowania odpowiedni dla obciążenia urządzenia."),
            ("Monitoring efektu", "Śledzimy parametry, zużycie mediów i obserwacje eksploatacyjne. Nastawy korygujemy na podstawie trendu, nie pojedynczego wyniku."),
        ],
        "outcomes_kicker": "Efekt dla produkcji",
        "outcomes_title": "Stabilniejszy proces, mniej interwencji.",
        "outcomes_intro": "Prawidłowo prowadzony obieg wodny wspiera powtarzalność cykli i ogranicza obciążenie utrzymania ruchu.",
        "outcomes_href": "/bezplatna-konsultacja/",
        "outcomes_link": "Sprawdź potencjał swojej instalacji",
        "outcomes": [
            ("Powtarzalne grzanie i chłodzenie", "Czyste powierzchnie wymiany ciepła pomagają utrzymać przewidywalny przebieg kolejnych cykli."),
            ("Mniejsze zużycie energii", "Ograniczenie warstwy osadu poprawia warunki przekazywania ciepła między obiegiem a urządzeniem."),
            ("Lepsza ochrona instalacji", "Kontrola pH, zasolenia i korozji wspiera trwałość płaszcza, wymienników oraz rurociągów."),
            ("Czytelne zasady obsługi", "Ustalone punkty pomiarowe, wartości docelowe i reakcje na odchylenia porządkują codzienną kontrolę."),
        ],
        "data_kicker": "Zakres audytu",
        "data_title": "Dane, które opisują rzeczywistą pracę obiegu.",
        "data_intro": "Na pierwszą rozmowę wystarczy podstawowy opis urządzenia. Brakujące pomiary i dokumentację porządkujemy wspólnie.",
        "data_rows": [
            ("Woda i materiały", "Źródło wody, twardość, pH, przewodność, chlorki oraz materiały płaszcza, wymiennika i rurociągów."),
            ("Temperatura i czas", "Temperatury grzania i chłodzenia, czas cyklu, liczba cykli oraz zmienność obciążenia w ciągu doby."),
            ("Przepływ i uzupełnienia", "Objętość obiegu, ilość wody uzupełniającej, zrzuty, przepływy i sposób odbioru ciepła."),
            ("Dozowanie i kontrola", "Pompy, punkty podania, stężenie preparatu, miejsca poboru prób oraz obecny rytm pomiarów."),
        ],
        "data_icons": ["circuit", "calendar", "gauge", "dosing"],
        "related": [
            ("Usługa", "Analiza wody przemysłowej", "/uslugi/analiza-wody/"),
            ("Technologia", "Program KCAQUA", "/kotly-parowe/kondycjonowanie-wody-kotlowej/"),
            ("Wsparcie", "Serwis i automatyka", "/uslugi/serwis-urzadzen/"),
        ],
        "faq_title": "Pytania o wodę w autoklawach i pasteryzatorach.",
        "faq_intro": "Konkretnie o zakresie programu, pomiarach, postoju i odpowiedzialności za proces.",
        "faq": [
            ("Jaki obszar instalacji obejmuje program Kabi-Chemie?", "Zajmujemy się obiegiem wodnym współpracującym z autoklawem lub pasteryzatorem: wodą uzupełniającą, płaszczem, wymiennikiem, rurociągami, dozowaniem i kontrolą parametrów. Zakres potwierdzamy po poznaniu schematu urządzenia."),
            ("Czy program wygląda tak samo dla autoklawu i pasteryzatora?", "Nie. Dobór zależy od materiałów, temperatur, sposobu grzania i chłodzenia, pojemności obiegu, liczby cykli oraz jakości wody. Dlatego zaczynamy od danych urządzenia i analizy próbki."),
            ("Czy Kabi-Chemie odpowiada za walidację procesu termicznego?", "Nie. Odpowiadamy za kondycjonowanie i kontrolę obiegu wodnego. Parametry technologiczne produktu, walidacja procesu i wymagania jakościowe pozostają po stronie producenta urządzenia oraz zakładu."),
            ("Czy wdrożenie wymaga zatrzymania produkcji?", "Audyt, pobór próbek i uruchomienie dozowania zwykle można zaplanować bez długiego postoju. Jeżeli potrzebne jest czyszczenie chemiczne, zakres i termin ustalamy osobno z utrzymaniem ruchu."),
            ("Jakie dane przygotować przed pierwszą rozmową?", "Wystarczy typ i model urządzenia, schemat obiegu, źródło wody, temperatury, liczba cykli oraz opis objawu. Jeżeli masz wyniki badań, zdjęcia osadu lub dane o dozowaniu, przyspieszą wstępną ocenę."),
        ],
        "cta_kicker": "Pierwszy krok",
        "cta_title": "Sprawdźmy obieg wodny Twojego urządzenia.",
        "cta_text": "Prześlij model urządzenia, podstawowe parametry i opis problemu. Inżynier wskaże potrzebne pomiary oraz rozsądny kolejny krok.",
        "cta_primary_label": "Umów konsultację techniczną",
        "cta_primary_href": "/bezplatna-konsultacja/",
    },
]


def install_solution_pages(pages, custom):
    for config in SOLUTIONS:
        pages[config["path"]] = {
            "body_class": (
                f"has-dark-hero solution-page solution-page--{config.get('style', config['slug'])} "
                f"solution-layout--{config.get('layout', 'editorial')}"
            ),
            "title": config["title"],
            "meta": config["meta"],
            "og_image": config["image"],
            "preload_image": config["image"],
            "jsonld": [_faq_schema(config["faq"])],
            "sections": [custom(_render_solution(config))],
        }
