# -*- coding: utf-8 -*-
"""Editorial system for KABI CHEMIE case studies and company pages."""

import content_source


def _join(items):
    return "".join(items)


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


def _case_icon(kind):
    """Small semantic icons used by the dedicated Fako case-study layout."""
    paths = {
        "water": '<path d="M12 2.7S5.6 9.5 5.6 14a6.4 6.4 0 0 0 12.8 0C18.4 9.5 12 2.7 12 2.7Z"/><path d="M8.9 14.7a3.4 3.4 0 0 0 3.1 2.2"/>',
        "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5-5l2.1 2.1-2.4 2.4-2.1-2.1a4 4 0 0 0 5 5l7.1 7.1a2.2 2.2 0 0 1-3.1 3.1l-7.1-7.1Z"/><circle cx="17.8" cy="17.8" r=".7"/>',
        "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="12" cy="12" r="1"/><path d="m15.1 8.9 5-5m-2.2 0h2.2v2.2"/>',
        "hardness": '<path d="M9 3h6m-5 0v5.2l-4.2 7.1A3.7 3.7 0 0 0 9 20.8h6a3.7 3.7 0 0 0 3.2-5.5L14 8.2V3"/><path d="M8.2 15h7.6"/><path d="m18.7 7 .5 1.2 1.3.5-1.3.5-.5 1.2-.5-1.2-1.3-.5 1.3-.5Z"/>',
        "conductivity": '<path d="M3 12h3l2-5 4 10 2.3-5H21"/><path d="M5 20h14"/><path d="M7 4h10"/>',
        "calendar": '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M7 2.5v4m10-4v4M3 9h18"/><circle cx="15.5" cy="15" r="2.7"/><path d="M15.5 13.6V15l1 .7"/>',
        "search": '<circle cx="10.8" cy="10.8" r="6.3"/><path d="m15.5 15.5 4.3 4.3"/><path d="m8.1 10.8 1.8 1.8 3.5-3.7"/>',
        "clean": '<path d="M4 16.5c3-1.1 5.8-1.1 8.4 0 2.5 1.1 5.1 1.1 7.6 0"/><path d="M4 20c3-1.1 5.8-1.1 8.4 0 2.5 1.1 5.1 1.1 7.6 0"/><path d="m13 3 .8 2.2L16 6l-2.2.8L13 9l-.8-2.2L10 6l2.2-.8Z"/><path d="m6.5 7 .5 1.4 1.5.6-1.5.6-.5 1.4L6 9.6 4.5 9 6 8.4Z"/>',
        "sliders": '<path d="M4 6h9m4 0h3M4 12h3m4 0h9M4 18h7m4 0h5"/><circle cx="15" cy="6" r="2"/><circle cx="9" cy="12" r="2"/><circle cx="13" cy="18" r="2"/>',
        "trend": '<path d="M4 19V5m0 14h16"/><path d="m7 15 4-4 3 2 5-6"/><path d="M16 7h3v3"/>',
        "gauge": '<path d="M4.2 17a8 8 0 1 1 15.6 0"/><path d="m12 13 4-4"/><circle cx="12" cy="13" r="1.5"/><path d="M6.5 17h11"/>',
        "report": '<path d="M6 2.8h8l4 4V21H6Z"/><path d="M14 2.8V7h4M9 12h6m-6 4h4"/><path d="m14.5 16.3 1 1 2-2.2"/>',
        "shield": '<path d="M12 2.5 19 5v5.7c0 4.5-2.7 8.2-7 10.8-4.3-2.6-7-6.3-7-10.8V5Z"/><path d="m8.5 12 2.2 2.2 4.8-5"/>',
        "thermometer": '<path d="M10 4a2 2 0 0 1 4 0v8.2a4.5 4.5 0 1 1-4 0Z"/><path d="M12 7v8"/><path d="M17 5h3m-3 4h2"/>',
        "valve": '<circle cx="12" cy="13" r="4"/><path d="M12 9V5m-4 0h8M4 13h4m8 0h4M8 3h8"/><path d="M12 17v4"/>',
        "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.5 2.6.6a2 2 0 0 1 2 2.3Z"/>',
    }
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true">{paths[kind]}</svg>'
    )


def _render_fako_case(config):
    # Ikony/wartości dobierane po pozycji wiersza. Modulo, bo panel redakcyjny
    # pozwala teraz dodać więcej wierszy niż pierwotne 3/4/3 — bez tego
    # dodatkowy wiersz wywalałby render (IndexError) i cały build.
    issue_icons = ("hardness", "conductivity", "calendar")
    issue_values = ("8 °n", "4200 µS", "3 mies.")
    issues = _join(
        f"""
        <article class="fako-diagnosis__row reveal">
          <span class="fako-icon fako-icon--large" aria-hidden="true">{_case_icon(issue_icons[index % len(issue_icons)])}</span>
          <strong class="fako-diagnosis__value">{issue_values[index % len(issue_values)]}</strong>
          <div><h3>{title}</h3><p>{text}</p></div>
          <em>{tag}</em>
        </article>"""
        for index, (title, text, tag) in enumerate(config["issues"])
    )

    process_icons = ("search", "clean", "sliders", "trend")
    process = _join(
        f"""
        <article class="fako-method__step reveal">
          <span class="fako-icon fako-icon--process" aria-hidden="true">{_case_icon(process_icons[index % len(process_icons)])}</span>
          <h3>{title}</h3>
          <p>{text}</p>
        </article>"""
        for index, (title, text) in enumerate(config["process"])
    )

    field_icons = ("gauge", "sliders", "report")
    field_notes = _join(
        f"""
        <article class="fako-control__item reveal">
          <span class="fako-icon" aria-hidden="true">{_case_icon(field_icons[index % len(field_icons)])}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for index, (title, text) in enumerate(config["field_notes"])
    )

    related = _join(
        f"""
        <a href="{href}">
          <span>{eyebrow}</span><strong>{title}</strong><i aria-hidden="true">↗</i>
        </a>"""
        for eyebrow, title, href in config["related"]
    )

    faq = _join(
        f"""
        <details{' open' if index == 0 else ''}>
          <summary><span>{question}</span><i aria-hidden="true"></i></summary>
          <div><p>{answer}</p></div>
        </details>"""
        for index, (question, answer) in enumerate(config["faq"])
    )

    signals = _join(f"<li>{signal}</li>" for signal in config["signals"])

    return f"""
<section class="fako-hero" id="top" style="--fako-image:url('{config['image']}'); --fako-position:{config.get('image_position', 'center center')}">
  <div class="fako-hero__media" aria-hidden="true"></div>
  <div class="fako-hero__shade" aria-hidden="true"></div>
  <div class="wrap fako-hero__inner">
    <div class="fako-hero__copy">
      <p class="fako-kicker"><span></span>{config['kicker']}</p>
      <h1><span>Fako: mniej paliwa.</span><span>Odzyskana wymiana ciepła.</span></h1>
      <p class="fako-hero__lead">{config['lead']}</p>
      <div class="fako-hero__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Omów podobną kotłownię</a>
        <a class="fako-text-link" href="/case-study/">Zobacz pozostałe realizacje <span aria-hidden="true">↗</span></a>
      </div>
      <ul class="fako-hero__signals" aria-label="Zakres realizacji">{signals}</ul>
    </div>
    <aside class="fako-hero__result" aria-label="Najważniejszy efekt realizacji">
      <span>{config['result_kicker']}</span>
      <strong>{config['result_value']}</strong>
      <em>{config['result_label']}</em>
      <p>{config['result_note']}</p>
    </aside>
  </div>
  <a class="fako-hero__scroll" href="#diagnoza"><span>Zobacz przebieg realizacji</span><i aria-hidden="true"></i></a>
</section>

<section class="fako-section fako-diagnosis" id="diagnoza">
  <span class="fako-brandmark fako-brandmark--diagnosis" aria-hidden="true"></span>
  <div class="wrap fako-diagnosis__grid">
    <header class="fako-section__intro reveal-left">
      <p class="fako-kicker fako-kicker--dark"><span></span>Diagnoza kotłowni</p>
      <h2><span>Osad był objawem.</span><span>Źródłem była woda.</span></h2>
      <p>Jednorazowe czyszczenie nie rozwiązywało przyczyny. Trzeba było równocześnie uporządkować jakość wody, odsalanie i sposób dozowania.</p>
    </header>
    <div class="fako-diagnosis__facts">{issues}</div>
  </div>
</section>

<section class="fako-section fako-method" id="przebieg">
  <div class="wrap">
    <header class="fako-method__head reveal">
      <div>
        <p class="fako-kicker"><span></span>Przebieg prac</p>
        <h2><span>Od usunięcia osadu</span><span>do stabilnej pracy.</span></h2>
      </div>
      <p>Najpierw odzyskaliśmy powierzchnię wymiany ciepła. Następnie ustawiliśmy program, który ogranicza warunki sprzyjające ponownemu odkładaniu kamienia.</p>
    </header>
    <div class="fako-method__grid">{process}</div>
  </div>
</section>

<section class="fako-section fako-results" id="efekty">
  <div class="wrap">
    <header class="fako-results__head reveal-left">
      <div>
        <p class="fako-kicker fako-kicker--dark"><span></span>Wynik w danych</p>
        <h2><span>Mniej paliwa.</span><span>Dłuższa praca kotła.</span></h2>
      </div>
      <p>Zmianę oceniliśmy nie po wyglądzie instalacji, lecz po parametrach, zużyciu paliwa i odstępach między kolejnymi czyszczeniami.</p>
    </header>
    <div class="fako-results__metrics">
      <article class="fako-result fako-result--primary reveal">
        <div class="fako-result__number"><b class="num-counter" data-count-to="32" data-prefix="−" data-suffix="%">0</b></div>
        <div class="fako-result__copy"><span>Paliwo</span><h3>Mniejsze zużycie po odzyskaniu wymiany ciepła</h3><p>Porównanie odniesiono do pracy kotła przed wdrożeniem.</p></div>
        <div class="fako-result__bars" aria-hidden="true"><span><i style="--bar:100%"></i><small>przed</small></span><span><i style="--bar:68%"></i><small>po</small></span></div>
      </article>
      <article class="fako-result reveal">
        <div class="fako-result__number"><b>4200</b><i aria-hidden="true">→</i><b>2800 <small>µS</small></b></div>
        <div class="fako-result__copy"><span>Przewodność</span><h3>Bezpieczniejszy zakres prowadzenia wody</h3><p>Parametr przestał utrudniać kontrolę odsalania.</p></div>
      </article>
      <article class="fako-result reveal">
        <div class="fako-result__number"><b>3</b><i aria-hidden="true">→</i><b>12 <small>mies.</small></b></div>
        <div class="fako-result__copy"><span>Utrzymanie ruchu</span><h3>Dłuższy cykl między czyszczeniami</h3><p>Mniej interwencji i łatwiejsze planowanie pracy kotłowni.</p></div>
      </article>
    </div>
    <p class="fako-results__note">{config['results_note']}</p>
  </div>
</section>

<section class="fako-section fako-control">
  <div class="wrap">
    <header class="fako-control__head reveal-left">
      <div>
        <p class="fako-kicker"><span></span>Utrzymanie efektu</p>
        <h2><span>Program utrzymuje efekt</span><span>po czyszczeniu.</span></h2>
      </div>
      <p>{config['field_intro']}</p>
    </header>
    <div class="fako-control__grid">{field_notes}</div>
  </div>
</section>

<nav class="fako-related" aria-label="Powiązane rozwiązania">
  <div class="wrap"><p>Przejdź dalej</p><div class="fako-related__links">{related}</div></div>
</nav>

<section class="fako-faq" id="faq">
  <div class="wrap fako-faq__grid">
    <header class="fako-faq__intro reveal-left">
      <p class="fako-kicker"><span></span>FAQ realizacji</p>
      <h2><span>Pytania przed</span><span>podobnym wdrożeniem.</span></h2>
      <p>{config['faq_intro']}</p>
    </header>
    <div class="fako-faq__list">{faq}</div>
  </div>
</section>

<section class="fako-cta">
  <span class="fako-brandmark fako-brandmark--cta" aria-hidden="true"></span>
  <div class="wrap fako-cta__inner">
    <div>
      <p class="fako-kicker fako-kicker--dark"><span></span>Podobny temat w zakładzie?</p>
      <h2>{config['cta_title']}</h2>
      <p>{config['cta_text']}</p>
    </div>
    <div class="fako-cta__actions">
      <a class="btn btn-primary" href="/kontakt/">Wyślij zapytanie techniczne</a>
      <a class="fako-phone" href="tel:+48662792875" aria-label="Zadzwoń do KABI CHEMIE: +48 662 792 875">{_case_icon('phone')}<span>+48 662 792 875</span></a>
    </div>
  </div>
</section>
"""


def _render_case(config):
    # Własny HTML całej treści — gdy wypełniony, pomijamy układ składany z pól
    # (także bespoke layout fako). Nagłówek strony, menu i stopka zostają,
    # bo pochodzą z build.py, nie stąd. Analogicznie do articles.html.
    wlasny = (config.get("html") or "").strip()
    if wlasny:
        return wlasny
    if config["slug"] == "fako":
        return _render_fako_case(config)

    issues = _join(
        f"""
        <article class="case-story-issue reveal">
          <span class="case-story-issue__mark" aria-hidden="true"></span>
          <div><h3>{title}</h3><p>{text}</p></div>
          <em>{tag}</em>
        </article>"""
        for title, text, tag in config["issues"]
    )

    process = _join(
        f"""
        <li class="reveal">
          <span class="case-story-process__mark" aria-hidden="true"></span>
          <div><h3>{title}</h3><p>{text}</p></div>
        </li>"""
        for title, text in config["process"]
    )

    def metric_value(metric):
        # Truthiness, nie samo istnienie klucza: panel zawsze emituje kolumnę
        # „count" (pustą, gdy redaktor jej nie wypełnił), więc puste count musi
        # spaść do wariantu tekstowego zamiast animować licznik od zera.
        if metric.get("count"):
            return (
                f'<b class="num-counter" data-count-to="{metric["count"]}" '
                f'data-prefix="{metric.get("prefix", "")}" '
                f'data-suffix="{metric.get("suffix", "")}">0</b>'
            )
        return f'<b>{metric.get("value", "")}</b>'

    metric_icon_sets = {
        "bac": ("water", "clean", "gauge"),
        "evapco": ("clean", "trend", "shield"),
    }
    metric_icons = metric_icon_sets.get(config["slug"], ("gauge", "trend", "shield"))
    metrics = _join(
        f"""
        <article class="case-story-metric reveal">
          <span class="case-story-metric__icon" aria-hidden="true">{_case_icon(metric_icons[index % len(metric_icons)])}</span>
          <div class="case-story-metric__outcome">
            <span class="case-story-metric__value">{metric_value(metric)}</span>
            <h3>{metric["label"]}</h3>
          </div>
          <div class="case-story-metric__change" aria-label="Zmiana: przed i po realizacji">
            <div class="case-story-metric__state case-story-metric__state--before">
              <span>Przed</span>
              <p>{metric["before"]}</p>
            </div>
            <span class="case-story-metric__flow" aria-hidden="true"></span>
            <div class="case-story-metric__state case-story-metric__state--after">
              <span>Po</span>
              <p>{metric["after"]}</p>
            </div>
          </div>
        </article>"""
        for index, metric in enumerate(config["metrics"])
    )

    field_notes = _join(
        f"""
        <li class="reveal">
          <span class="case-story-fieldnote__mark" aria-hidden="true"></span>
          <div><strong>{title}</strong><p>{text}</p></div>
        </li>"""
        for title, text in config["field_notes"]
    )

    related = _join(
        f"""
        <a href="{href}">
          <span>{eyebrow}</span>
          <strong>{title}</strong>
          <i aria-hidden="true">↗</i>
        </a>"""
        for eyebrow, title, href in config["related"]
    )

    faq = _join(
        f"""
        <details{' open' if index == 1 else ''}>
          <summary><span>{question}</span><i aria-hidden="true"></i></summary>
          <div><p>{answer}</p></div>
        </details>"""
        for index, (question, answer) in enumerate(config["faq"])
    )

    signals = _join(f"<li>{signal}</li>" for signal in config["signals"])

    return f"""
<section class="case-story-hero case-story-hero--{config['slug']}" id="top" style="--case-image:url('{config['image']}'); --case-position:{config.get('image_position', 'center center')}">
  <div class="case-story-hero__media" aria-hidden="true"></div>
  <div class="case-story-hero__shade" aria-hidden="true"></div>
  <div class="wrap case-story-hero__inner">
    <div class="case-story-hero__copy">
      <p class="case-story-kicker"><span></span>{config['kicker']}</p>
      <h1>{config['h1']}</h1>
      <p class="case-story-hero__lead">{config['lead']}</p>
      <div class="case-story-hero__actions">
        <a class="btn btn-primary" href="/bezplatna-konsultacja/">Omów podobną instalację</a>
        <a class="case-story-text-link" href="/case-study/">Wróć do realizacji <span aria-hidden="true">↗</span></a>
      </div>
      <ul class="case-story-hero__signals" aria-label="Zakres realizacji">{signals}</ul>
    </div>
    <aside class="case-story-hero__result" aria-label="Najważniejszy efekt realizacji">
      <span>{config['result_kicker']}</span>
      <strong>{config['result_value']}</strong>
      <em>{config['result_label']}</em>
      <p>{config['result_note']}</p>
    </aside>
  </div>
  <a class="case-story-hero__scroll" href="#wyzwanie"><span>Przejdź do przebiegu</span><i aria-hidden="true"></i></a>
</section>

<section class="case-story-section case-story-brief" id="wyzwanie">
  <span class="case-story-brandmark case-story-brandmark--brief" aria-hidden="true"></span>
  <div class="wrap case-story-brief__grid">
    <header class="case-story-section__intro reveal-left">
      <p class="case-story-kicker case-story-kicker--dark"><span></span>Co wymagało decyzji</p>
      <h2>{config['challenge_title']}</h2>
      <p>{config['challenge_intro']}</p>
    </header>
    <div class="case-story-issues">{issues}</div>
  </div>
</section>

<section class="case-story-section case-story-method" id="proces">
  <div class="wrap">
    <header class="case-story-method__head reveal">
      <div>
        <p class="case-story-kicker"><span></span>Przebieg prac</p>
        <h2>{config['process_title']}</h2>
      </div>
      <p>{config['process_intro']}</p>
    </header>
    <ol class="case-story-process">{process}</ol>
  </div>
</section>

<section class="case-story-section case-story-results" id="efekty">
  <div class="wrap">
    <header class="case-story-results__head reveal-left">
      <p class="case-story-kicker case-story-kicker--dark"><span></span>Co zmieniło się w instalacji</p>
      <h2>{config['results_title']}</h2>
      <p>{config['results_intro']}</p>
    </header>
    <div class="case-story-metrics">{metrics}</div>
    <p class="case-story-results__note">{config['results_note']}</p>
  </div>
</section>

<section class="case-story-fieldnote">
  <div class="wrap case-story-fieldnote__grid">
    <header class="case-story-fieldnote__intro reveal-left">
      <p class="case-story-kicker"><span></span>Co utrzymuje efekt</p>
      <h2>{config['field_title']}</h2>
      <p>{config['field_intro']}</p>
    </header>
    <ol class="case-story-fieldnote__list">{field_notes}</ol>
  </div>
</section>

<nav class="case-story-related" aria-label="Powiązane rozwiązania">
  <div class="wrap">
    <p>Przejdź dalej</p>
    <div class="case-story-related__links">{related}</div>
  </div>
</nav>

<section class="case-story-faq" id="faq">
  <div class="wrap case-story-faq__grid">
    <header class="case-story-faq__intro reveal-left">
      <p class="case-story-kicker"><span></span>FAQ realizacji</p>
      <h2>{config['faq_title']}</h2>
      <p>{config['faq_intro']}</p>
    </header>
    <div class="case-story-faq__list">{faq}</div>
  </div>
</section>

<section class="case-story-cta">
  <span class="case-story-brandmark case-story-brandmark--cta" aria-hidden="true"></span>
  <div class="wrap case-story-cta__inner">
    <div>
      <p class="case-story-kicker"><span></span>Podobny temat w zakładzie?</p>
      <h2>{config['cta_title']}</h2>
      <p>{config['cta_text']}</p>
    </div>
    <div class="case-story-cta__actions">
      <a class="btn btn-primary" href="/kontakt/">Napisz do inżyniera</a>
      <a class="case-story-phone" href="tel:+48662792875" aria-label="Zadzwoń do KABI CHEMIE: +48 662 792 875">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/></svg>
        <span>+48 662 792 875</span>
      </a>
    </div>
  </div>
</section>
"""


# Zrodlem prawdy jest content/snapshot.json — generowany z Postgresa przez
# builder/export_snapshot.py. Wczesniej dane byly literalem w tym pliku.
CASE_STUDIES = content_source.case_studies()
REFERENCJE = content_source.referencje()

# ------------------------------------------------------------------ REFERENCJE
# Siatka na /referencje/. Wpisy pochodza z tabeli kabi.referencje; wpis bez
# wgranego pliku zostaje kaflem „w trakcie tworzenia”, zeby uklad sekcji
# trzymal sie, zanim dokumenty beda gotowe.
MINIMUM_KAFLI = 6


def _kafel_referencji(r):
    """Kafel to sama miniaturka dokumentu — bez tytulu, firmy i opisu.

    Podpisy pod kaflem rozbijaly rowna siatke i powtarzaly informacje, ktora
    i tak jest widoczna na samym dokumencie. Caly kafel jest odnosnikiem;
    iframe ma wylaczone zdarzenia myszy, zeby klikniecie trafialo w link,
    a nie w przegladarke PDF.
    """
    tytul = r.get("tytul") or "Referencja"
    plik = (r.get("plik") or "").strip()

    if not plik:
        return ('<div class="company-reference-placeholder">'
                f'<span>{tytul}</span></div>')

    return (f'<a class="company-reference-card" href="{plik}" target="_blank" '
            f'rel="noopener" aria-label="{tytul} — otwórz dokument PDF">'
            f'<iframe src="{plik}#toolbar=0&navpanes=0&scrollbar=0&view=FitH" '
            f'title="{tytul}" tabindex="-1" aria-hidden="true" loading="lazy"></iframe>'
            "</a>")


def _siatka_referencji():
    wpisy = list(REFERENCJE)
    # Dopelniamy do pelnego wiersza, zeby siatka nie wygladala na urwana.
    puste = max(0, MINIMUM_KAFLI - len(wpisy))
    kafle = [_kafel_referencji(r) for r in wpisy]
    kafle += ['<div class="company-reference-placeholder">'
              '<span>w trakcie tworzenia</span></div>'] * puste
    return ('<div class="company-reference-placeholder-grid" '
            'aria-label="Referencje">' + "".join(kafle) + "</div>")



def _company_hero(config):
    actions = _join(
        f'<a class="{classes}" href="{href}">{label}</a>'
        for classes, label, href in config["actions"]
    )
    signals = _join(
        f"<li><span>{index:02d}</span><strong>{title}</strong><p>{text}</p></li>"
        for index, (title, text) in enumerate(config["signals"], 1)
    )
    return f"""
<section class="company-hero company-hero--{config['slug']}" id="top" style="--company-image:url('{config['image']}'); --company-position:{config.get('image_position', 'center center')}">
  <div class="company-hero__media" aria-hidden="true"></div>
  <div class="company-hero__shade" aria-hidden="true"></div>
  <div class="wrap company-hero__inner">
    <div class="company-hero__copy">
      <p class="company-kicker"><span></span>{config['kicker']}</p>
      <h1>{config['h1']}</h1>
      <p class="company-hero__lead">{config['lead']}</p>
      <div class="company-hero__actions">{actions}</div>
    </div>
    <ol class="company-hero__signals" aria-label="Najważniejsze informacje">{signals}</ol>
  </div>
  <a class="company-hero__scroll" href="{config['scroll_href']}"><span>{config['scroll_label']}</span><i aria-hidden="true"></i></a>
</section>
"""


def _company_editorial_hero(config):
    actions = _join(
        f'<a class="{classes}" href="{href}">{label}</a>'
        for classes, label, href in config["actions"]
    )
    return f"""
<section class="company-overview-hero company-overview-hero--{config['slug']}" id="top" style="--overview-image:url('{config['image']}'); --overview-position:{config.get('image_position', 'center center')}">
  <div class="company-overview-hero__media" aria-hidden="true"></div>
  <div class="company-overview-hero__shade" aria-hidden="true"></div>
  <img class="company-overview-hero__brandmark" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap company-overview-hero__inner">
    <div class="company-overview-hero__copy">
      <p class="company-kicker"><span></span>{config['kicker']}</p>
      <h1>{config['h1']}</h1>
      <p class="company-overview-hero__lead">{config['lead']}</p>
      <div class="company-overview-hero__actions">{actions}</div>
    </div>
  </div>
</section>
"""


def _case_index_hero():
    return """
<section class="company-hero company-hero--cases case-index-hero" id="top" style="--company-image:url('/assets/case/case-fako-boiler-generated.png'); --company-position:center center">
  <div class="company-hero__media" aria-hidden="true"></div>
  <div class="company-hero__shade" aria-hidden="true"></div>
  <div class="wrap company-hero__inner">
    <div class="company-hero__copy">
      <p class="company-kicker"><span></span>Case study · wyniki z instalacji</p>
      <h1>
        <span class="case-index-hero__title-line">Realizacje, które</span>
        <span class="case-index-hero__title-line">widać w liczbach.</span>
      </h1>
      <p class="company-hero__lead">Pokazujemy punkt wyjścia, zakres prac i efekt potwierdzony danymi z kotłowni parowych, układów chłodniczych oraz zakładów przetwórczych.</p>
      <div class="company-hero__actions">
        <a class="btn btn-primary" href="#realizacje">Zobacz realizacje</a>
        <a class="company-text-link" href="/kontakt/">Omów podobną instalację <span aria-hidden="true">↗</span></a>
      </div>
      <ul class="case-index-hero__scope" aria-label="Zakres realizacji">
        <li>
          <span class="case-index-hero__scope-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 19h12"/><path d="M8 19V9a4 4 0 0 1 8 0v10"/><path d="M9 5h6"/><path d="M10 13h4"/><path d="M12 13v3"/></svg>
          </span>
          <span>Kotłownie parowe</span>
        </li>
        <li>
          <span class="case-index-hero__scope-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="m4.93 6.93 14.14 14.14"/><path d="m19.07 6.93-14.14 14.14"/><path d="m9 4 3 3 3-3"/><path d="m9 20 3-3 3 3"/><path d="m4 9 3 3-3 3"/><path d="m20 9-3 3 3 3"/></svg>
          </span>
          <span>Chłodnictwo przemysłowe</span>
        </li>
        <li>
          <span class="case-index-hero__scope-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19V5"/><path d="M4 19h16"/><path d="m7 15 4-4 3 3 5-6"/><path d="M16 8h3v3"/></svg>
          </span>
          <span>Wyniki przed i po</span>
        </li>
      </ul>
    </div>
  </div>
  <a class="company-hero__scroll" href="#realizacje"><span>Przejdź do realizacji</span><i aria-hidden="true"></i></a>
</section>
"""


def _company_final(kicker, title, text, primary_label="Porozmawiaj z inżynierem", primary_href="/kontakt/", secondary_label="Zadzwoń: +48 662 792 875"):
    return f"""
<section class="company-final">
  <div class="wrap company-final__inner">
    <div>
      <p class="company-kicker"><span></span>{kicker}</p>
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
    <div class="company-final__actions">
      <a class="btn btn-primary" href="{primary_href}">{primary_label}</a>
      <a class="company-phone-link" href="tel:+48662792875">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/></svg>
        <span>{secondary_label}</span>
      </a>
    </div>
  </div>
</section>
"""


def _render_about():
    return """
<section class="company-hero company-hero--about" id="top" style="--company-image:url('/assets/visuals-v2/company-mission-v2.jpg'); --company-position:center center">
  <div class="company-hero__media" aria-hidden="true"></div>
  <div class="company-hero__shade" aria-hidden="true"></div>
  <img class="company-about-hero__brandmark" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap company-hero__inner company-about-hero__inner">
    <div class="company-hero__copy company-about-hero__copy">
      <p class="company-kicker"><span></span>KABI CHEMIE · technologia KCAQUA</p>
      <h1><span class="company-about-hero__title-line">Woda przemysłowa</span><span class="company-about-hero__title-line company-about-hero__title-line--accent">pod kontrolą.</span></h1>
      <p class="company-hero__lead">Łączymy analizę wody, chemię KCAQUA, dozowanie i stały nadzór. Pomagamy ograniczać zużycie wody i energii, chronić instalacje oraz szybciej reagować na odchylenia.</p>
      <div class="company-hero__actions">
        <a class="btn btn-primary" href="/warunki-wspolpracy/">Poznaj sposób współpracy</a>
        <a class="company-text-link" href="/kontakt/">Porozmawiaj z inżynierem <span aria-hidden="true">↗</span></a>
      </div>
      <ul class="company-about-hero__scope" aria-label="Zakres działania KABI CHEMIE">
        <li>
          <span class="company-about-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3C9 7.1 6.5 9.9 6.5 13.3a5.5 5.5 0 0 0 11 0C17.5 9.9 15 7.1 12 3Z"/><circle cx="17.5" cy="17.5" r="3"/><path d="m19.8 19.8 1.5 1.5"/></svg></span>
          <strong>Diagnoza</strong><em>Woda, obciążenie i miejsca strat.</em>
        </li>
        <li>
          <span class="company-about-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6"/><path d="M10 3v5l-4.7 8.2A3.2 3.2 0 0 0 8.1 21h7.8a3.2 3.2 0 0 0 2.8-4.8L14 8V3"/><path d="M7.6 14h8.8"/></svg></span>
          <strong>Program KCAQUA</strong><em>Chemia i dawki dobrane do instalacji.</em>
        </li>
        <li>
          <span class="company-about-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19V5"/><path d="M4 19h16"/><path d="m7 15 4-4 3 3 5-6"/><path d="M16 8h3v3"/></svg></span>
          <strong>Nadzór</strong><em>Pomiary, korekty i raport efektów.</em>
        </li>
      </ul>
    </div>
  </div>
  <a class="company-hero__scroll" href="#podejscie"><span>Zobacz, co kontrolujemy</span><i aria-hidden="true"></i></a>
</section>

<section class="company-manifest" id="podejscie">
  <div class="wrap company-manifest__grid">
    <header class="company-manifest__lead reveal-left">
      <p class="company-kicker company-kicker--dark"><span></span>Co porządkujemy</p>
      <h2>Mierzymy, zanim rekomendujemy.</h2>
    </header>
    <div class="company-manifest__copy reveal-right">
      <p>Koszt wody nie kończy się na jej poborze. O wyniku decydują również odsalanie, wymiany wody, zużycie energii, stan powierzchni wymiany ciepła i stabilność dozowania.</p>
      <dl class="company-manifest__scope">
        <div><dt>Bilans wody</dt><dd>Pobór, odsalanie, wymiany i ilość wody odprowadzanej z instalacji.</dd></div>
        <div><dt>Sprawność procesu</dt><dd>Temperatury, wymiana ciepła oraz zużycie pary, paliwa lub chłodu.</dd></div>
        <div><dt>Stan instalacji</dt><dd>Kamień, korozja, biofilm, dozowanie i działanie automatyki.</dd></div>
      </dl>
      <a class="company-inline-link" href="/kalkulator-oszczednosci/">Sprawdź potencjał oszczędności <span aria-hidden="true">↗</span></a>
    </div>
  </div>
</section>

<section class="company-principles">
  <div class="wrap company-principles__grid">
    <header class="company-principles__intro reveal-left">
      <p class="company-kicker"><span></span>Sposób pracy</p>
      <h2>Od diagnozy do wyniku.</h2>
      <p>Każdy etap odpowiada na konkretne pytanie techniczne i kończy się jasnym kolejnym krokiem.</p>
    </header>
    <ol class="company-principles__list">
      <li class="reveal"><span class="company-principles__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/><path d="M8.5 11h5M11 8.5v5"/></svg></span><div><h3>Diagnozujemy instalację</h3><p>Analizujemy wodę, obciążenie, historię pracy, odsalanie i sposób dozowania. Ustalamy, gdzie powstaje strata lub ryzyko.</p></div></li>
      <li class="reveal"><span class="company-principles__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v3"/><path d="M7.5 5.2 9 7.8"/><path d="m4.2 9 2.6 1.5"/><circle cx="12" cy="13" r="5"/><path d="M12 10v3l2 1"/><path d="M17.2 10.5 19.8 9"/></svg></span><div><h3>Dobieramy program KCAQUA</h3><p>Łączymy preparat, dawkę, automatykę i parametry docelowe w jeden program dopasowany do warunków pracy.</p></div></li>
      <li class="reveal"><span class="company-principles__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 20V10M12 20V4M19 20v-7"/><path d="M3 20h18"/></svg></span><div><h3>Nadzorujemy i raportujemy</h3><p>Śledzimy trendy, korygujemy ustawienia i pokazujemy wpływ programu na parametry instalacji oraz koszty jej pracy.</p></div></li>
    </ol>
  </div>
</section>

<section class="company-evidence">
  <div class="wrap company-evidence__grid">
    <div class="company-evidence__media" aria-hidden="true">
      <img src="/assets/visuals-v2/company-diagnostics-v3.webp" alt="Inżynier analizujący dane pracy przemysłowej instalacji wodnej" width="1680" height="945" loading="lazy" decoding="async">
    </div>
    <div class="company-evidence__copy reveal-right">
      <p class="company-kicker company-kicker--dark"><span></span>Decyzja oparta na danych</p>
      <h2>Uczciwa diagnoza. Jasna decyzja.</h2>
      <p>Po analizie wskazujemy, co warto poprawić, jakie działania mają uzasadnienie i po czym poznać ich efekt. Jeżeli instalacja nie ma realnego potencjału, mówimy o tym wprost.</p>
      <ul>
        <li><strong>Co mierzymy</strong><span>Parametry wody, pracę dozowania, odsalanie i punkty strat.</span></li>
        <li><strong>Co rekomendujemy</strong><span>Korektę nastaw, czyszczenie, audyt albo program KCAQUA.</span></li>
        <li><strong>Co raportujemy</strong><span>Zmianę parametrów, ryzyka techniczne i wpływ na koszty.</span></li>
      </ul>
    </div>
  </div>
</section>
""" + _company_final(
        "Pierwszy krok",
        "Sprawdźmy potencjał Twojej instalacji.",
        "Podaj typ instalacji, główny problem i dostępne dane. Inżynier wskaże, od czego warto zacząć.",
        "Umów bezpłatny audyt",
        "/bezplatna-konsultacja/",
    )


TRUSTED_PARTNERS = (
    (1, "Sokołów"),
    (2, "Farmio"),
    (3, "Silikaty Szlachta"),
    (4, "Bakalland"),
    (5, "Dolina Noteci"),
    (6, "Wipasz"),
    (7, "SEKO"),
    (8, "Łukowski"),
    (9, "Rauch"),
    (10, "OSM Garwolin"),
    (11, "Krynica Vitamin"),
    (12, "Komar Group"),
    (13, "Wierzejki"),
    (14, "OSM Kosów"),
    (15, "OSM Siedlce"),
    (16, "Wędzarnia Ostropol"),
    (17, "Podlaska Chata"),
    (18, "ZPC Bałtyk"),
)


def _company_trusted_strip():
    logos = _join(
        f'''<span class="company-trusted-logo" tabindex="0" aria-label="{name}">
          <img class="company-trusted-logo__muted" src="/assets/partners/partner-{index:02d}-muted.png" alt="{name}" loading="lazy">
          <img class="company-trusted-logo__color" src="/assets/partners/partner-{index:02d}-color.png" alt="" aria-hidden="true" loading="lazy">
        </span>'''
        for index, name in TRUSTED_PARTNERS
    )
    logos_duplicate = _join(
        f'''<span class="company-trusted-logo">
          <img class="company-trusted-logo__muted" src="/assets/partners/partner-{index:02d}-muted.png" alt="" aria-hidden="true" loading="lazy">
          <img class="company-trusted-logo__color" src="/assets/partners/partner-{index:02d}-color.png" alt="" aria-hidden="true" loading="lazy">
        </span>'''
        for index, _ in TRUSTED_PARTNERS
    )
    return f'''
<section class="company-trusted" aria-label="Firmy, które nam zaufały">
  <div class="company-trusted__viewport">
    <div class="company-trusted__track">
      <div class="company-trusted__group">{logos}</div>
      <div class="company-trusted__group" aria-hidden="true">{logos_duplicate}</div>
    </div>
  </div>
</section>
'''


def _render_model():
    hero = _company_editorial_hero({
        "slug": "model",
        "image": "/assets/visuals-v2/company-collaboration-v2.jpg",
        "image_position": "center center",
        "kicker": "Firma / Model współpracy",
        "h1": "Od diagnozy <span>do wyniku.</span>",
        "lead": "Każdy etap kończy się decyzją, zakresem odpowiedzialności i danymi potrzebnymi do oceny efektu.",
        "actions": [
            ("btn btn-primary", "Umów pierwszą rozmowę", "/kontakt/"),
            ("company-overview-link", "Poznaj cztery etapy", "#droga"),
        ],
    })
    return hero + _company_trusted_strip() + """
<section class="company-journey" id="droga">
  <div class="wrap">
    <header class="company-journey__head reveal-left">
      <p class="company-kicker company-kicker--dark"><span></span>Cztery czytelne etapy</p>
      <h2>Najpierw rozumiemy instalację. Dopiero potem proponujemy działanie.</h2>
      <p>Zakres dobieramy do rzeczywistego problemu. Każdy krok ma określony cel, rezultat i osobę odpowiedzialną.</p>
    </header>
    <ol class="company-journey__list">
      <li class="reveal"><span>01</span><div><h3>Rozpoznanie techniczne</h3><p>Ustalamy typ instalacji, objawy, historię problemu i dostępne dane. Jeżeli potrzebna jest wizyta lub próbki, określamy zakres przed przyjazdem.</p><small>Rezultat: lista danych i kolejny krok.</small></div></li>
      <li class="reveal"><span>02</span><div><h3>Diagnoza i plan działania</h3><p>Łączymy analizę wody, oględziny, pracę automatyki oraz koszty mediów. Oddzielamy przyczynę od skutków i ustalamy priorytety.</p><small>Rezultat: rekomendacja z zakresem i kryteriami oceny.</small></div></li>
      <li class="reveal"><span>03</span><div><h3>Bezpieczne wdrożenie</h3><p>Uruchamiamy program KCAQUA, ustawiamy dozowanie, punkty kontroli i sposób reagowania na odchylenia. Zespół zakładu wie, co obserwować.</p><small>Rezultat: działający program i jasne parametry docelowe.</small></div></li>
      <li class="reveal"><span>04</span><div><h3>Monitoring i ocena efektu</h3><p>Porównujemy dane, korygujemy ustawienia i raportujemy wpływ na wodę, energię, stan instalacji oraz ciągłość procesu.</p><small>Rezultat: decyzja oparta na porównywalnych danych.</small></div></li>
    </ol>
  </div>
</section>

<section class="company-responsibility">
  <div class="wrap company-responsibility__grid">
    <header class="company-responsibility__intro reveal-left">
      <p class="company-kicker"><span></span>Jedna odpowiedzialność</p>
      <h2>Każda strona wie, za co odpowiada.</h2>
      <p>To skraca wdrożenie, ogranicza błędy i pozwala oceniać efekt bez przerzucania odpowiedzialności między chemią, automatyką i obsługą.</p>
    </header>
    <div class="company-responsibility__columns reveal-right">
      <section>
        <span>Po stronie KABI CHEMIE</span>
        <ul><li>diagnoza i dobór programu,</li><li>parametry dozowania i kontroli,</li><li>interpretacja wyników i korekty,</li><li>czytelny raport z rekomendacją.</li></ul>
      </section>
      <section>
        <span>Po stronie zakładu</span>
        <ul><li>dostęp do instalacji i danych,</li><li>informacja o zmianach obciążenia,</li><li>realizacja uzgodnionych kontroli,</li><li>szybka reakcja na odchylenia.</li></ul>
      </section>
    </div>
  </div>
</section>

<section class="company-deliverables">
  <div class="wrap company-deliverables__grid">
    <header class="company-deliverables__intro reveal-left">
      <p class="company-kicker"><span></span>Konkretny rezultat</p>
      <h2>Po każdym etapie zostaje użyteczna decyzja.</h2>
      <p>Dokumentacja ma pomagać w pracy zakładu, a nie tylko zamykać spotkanie.</p>
    </header>
    <dl class="company-deliverables__list">
      <div class="reveal"><dt>Mapa ryzyka</dt><dd>Co wpływa na osady, korozję, zużycie mediów lub stabilność procesu i które obszary wymagają reakcji.</dd></div>
      <div class="reveal"><dt>Plan wdrożenia</dt><dd>Zakres programu, kolejność działań, wymagane przygotowanie instalacji oraz warunki bezpiecznego startu.</dd></div>
      <div class="reveal"><dt>Standard kontroli</dt><dd>Parametry, częstotliwość pomiarów, wartości docelowe i sposób postępowania przy odchyleniu.</dd></div>
      <div class="reveal"><dt>Ocena wyniku</dt><dd>Dane bazowe i bieżące zestawione tak, aby wynik był zrozumiały dla techniki, produkcji i zarządu.</dd></div>
    </dl>
  </div>
</section>

<section class="company-commitment">
  <div class="wrap company-commitment__inner">
    <div class="company-commitment__copy reveal-left">
      <p class="company-kicker"><span></span>Nasze zobowiązanie</p>
      <blockquote><span>Nie obiecujemy bez danych.</span><span>Efekt potwierdzamy w instalacji.</span></blockquote>
      <p>Od początku ustalamy, co mierzymy, kiedy oceniamy wynik i na jakiej podstawie podejmujemy kolejną decyzję.</p>
    </div>
  </div>
</section>
""" + _company_final(
        "Pierwszy krok",
        "Zacznijmy od krótkiego rozpoznania instalacji.",
        "Podaj typ układu i główny problem. Wskażemy dane potrzebne do pierwszej decyzji.",
        "Umów rozmowę techniczną",
        "/kontakt/",
    )


def _render_references():
    hero = _company_editorial_hero({
        "slug": "references",
        "image": "/assets/visuals-v2/company-references-v2.jpg",
        "image_position": "center center",
        "kicker": "Firma / Referencje",
        "h1": "Wyniki potwierdzone <span>danymi z instalacji.</span>",
        "lead": "Pokazujemy punkt wyjścia, zakres prac i efekt zmierzony bezpośrednio w instalacji.",
        "actions": [
            ("btn btn-primary", "Zobacz wybrane realizacje", "#realizacje"),
            ("company-overview-link", "Omów podobną instalację", "/kontakt/"),
        ],
    })
    return (hero + _company_trusted_strip() + """
<section class="company-reference-ledger" id="realizacje">
  <div class="wrap company-reference-ledger__grid">
    <header class="company-reference-ledger__intro reveal-left">
      <p class="company-kicker company-kicker--dark"><span></span>Wybrane wdrożenia</p>
      <h2>Punkt wyjścia, zakres prac i wynik.</h2>
      <p>Każdą realizację pokazujemy w tym samym układzie. Dzięki temu łatwo ocenić, czy odpowiada warunkom Państwa instalacji.</p>
      <a class="company-inline-link" href="/case-study/">Zobacz wszystkie case studies <span aria-hidden="true">↗</span></a>
    </header>
    <!--SIATKA-REFERENCJI-->
  </div>
</section>

<section class="company-reference-standard">
  <div class="wrap company-reference-standard__grid">
    <header class="reveal-left"><p class="company-kicker company-kicker--dark"><span></span>Jak czytać referencje</p><h2>Podobna branża. Inne warunki pracy.</h2></header>
    <ol class="reveal-right">
      <li><span>01</span><div><strong>Dobieramy przykład technicznie</strong><p>Porównujemy typ urządzenia, jakość wody, materiały i sposób obciążenia procesu.</p></div></li>
      <li><span>02</span><div><strong>Oddzielamy dane od deklaracji</strong><p>Wskazujemy, co zostało zmierzone, a co wymaga potwierdzenia w Państwa warunkach.</p></div></li>
      <li><span>03</span><div><strong>Zaczynamy od własnej bazy</strong><p>Punktem odniesienia są parametry Państwa instalacji przed i po wdrożeniu.</p></div></li>
    </ol>
  </div>
</section>
"""
            .replace("<!--SIATKA-REFERENCJI-->", _siatka_referencji())) + _company_final(
        "Państwa instalacja",
        "Dobierzmy właściwy punkt odniesienia.",
        "Podaj branżę, typ urządzenia i główny problem. Wskażemy realizację zbliżoną technicznie, nie tylko wizualnie.",
        "Omów podobne wdrożenie",
        "/kontakt/",
    )


COMPANY_FAQ = [
    (
        "Pierwsza rozmowa",
        [
            ("Czy pierwsza konsultacja jest bezpłatna?", "Tak. Pierwsza rozmowa techniczna służy rozpoznaniu instalacji i problemu. Nie zobowiązuje do zakupu chemii ani usługi."),
            ("Co warto przygotować przed kontaktem?", "Wystarczy typ instalacji, krótki opis objawów i kontakt do osoby, która zna jej codzienną pracę. Jeśli masz wyniki wody lub dane o zużyciu mediów, warto je zachować do rozmowy."),
            ("Kiedy najlepiej zadzwonić zamiast pisać?", "Przy ryzyku postoju, nagłym pogorszeniu chłodzenia, przecieku lub problemie wymagającym szybkiej oceny technicznej najlepiej zadzwonić bezpośrednio."),
        ],
    ),
    (
        "Audyt i program",
        [
            ("Jak wygląda audyt techniczny?", "Zakres ustalamy do instalacji. Może obejmować analizę wody, oględziny urządzeń, ocenę dozowania, danych z automatyki i kosztów mediów. Wynik przekładamy na konkretne działania."),
            ("Czy KCAQUA zastępuje dotychczasową chemię?", "W wielu instalacjach tak, ale nie podejmujemy tej decyzji bez analizy warunków pracy. Program dobieramy do jakości wody, materiałów, obciążenia i celu technicznego."),
            ("Kiedy można ocenić efekt wdrożenia?", "Parametry wody zmieniają się natychmiast, a oszczędności wody można zauważyć już w ciągu 24 godzin od rozpoczęcia dozowania. Odkamienianie jest procesem rozłożonym w czasie i może trwać nawet kilka miesięcy, w zależności od stanu instalacji."),
        ],
    ),
    (
        "Instalacje przemysłowe",
        [
            ("Jakie instalacje obsługuje KABI CHEMIE?", "Pracujemy przy kotłach parowych, skraplaczach wyparnych, wieżach chłodniczych, obiegach technologicznych, wymiennikach i instalacjach odwróconej osmozy."),
            ("Czy cienka warstwa kamienia ma znaczenie?", "Tak. Nawet cienki osad ogranicza wymianę ciepła, może podnosić zużycie energii i przyspieszać ryzyko przegrzań lub problemów serwisowych. Skala efektu zależy od konkretnej instalacji."),
            ("Czy program chemiczny może ograniczyć zużycie wody?", "Może, jeżeli instalacja pozwala bezpiecznie utrzymać korzystniejsze parametry pracy. Najpierw sprawdzamy jakość wody i limity urządzenia, a dopiero później optymalizujemy odsalanie lub zrzuty."),
        ],
    ),
    (
        "Zakres i decyzja",
        [
            ("Czy obsługujecie zakłady w całej Polsce?", "Tak. KABI CHEMIE realizuje audyty, wdrożenia i opiekę techniczną w zakładach przemysłowych w całej Polsce. Zakres oraz termin wizyty ustalamy po wstępnym rozpoznaniu instalacji."),
            ("Czy współpraca musi zaczynać się od pełnego audytu?", "Nie. Pierwszym krokiem może być krótka rozmowa, ocena dostępnych danych albo analiza wody. Pełny audyt proponujemy wtedy, gdy jest potrzebny do bezpiecznej decyzji."),
            ("Co otrzymujemy po rozpoznaniu instalacji?", "Wskazujemy źródła ryzyka, rekomendowany zakres działań, potrzebne pomiary i sposób oceny efektu. Jeżeli nie widzimy uzasadnienia dla wdrożenia, mówimy o tym wprost."),
        ],
    ),
]


def _render_faq():
    groups = _join(
        f"""
        <section class="company-faq-group" id="faq-{index}">
          <p>{title}</p>
          {_join(
              f'''
              <details name="company-faq"{' open' if index == 1 and question_index == 0 else ''}>
                <summary><span class="company-faq-editorial__question"><span class="company-faq-editorial__mark" aria-hidden="true"></span><span>{question}</span></span><i aria-hidden="true"></i></summary>
                <div><p>{answer}</p></div>
              </details>'''
              for question_index, (question, answer) in enumerate(items)
          )}
        </section>"""
        for index, (title, items) in enumerate(COMPANY_FAQ, 1)
    )
    all_questions = [item for _, items in COMPANY_FAQ for item in items]
    hero = _company_editorial_hero({
        "slug": "faq",
        "image": "/assets/visuals-v2/company-faq-v2.jpg",
        "image_position": "center center",
        "kicker": "Firma / FAQ",
        "h1": "Odpowiedzi przed <span>pierwszą rozmową.</span>",
        "lead": "Konkretnie o instalacjach, audycie, programie KCAQUA, wdrożeniu i odpowiedzialności za wynik.",
        "actions": [
            ("btn btn-primary", "Zadaj pytanie techniczne", "/kontakt/"),
            ("company-overview-link", "Przejdź do odpowiedzi", "#pytania"),
        ],
    })
    return hero + f"""
<section class="company-faq-editorial" id="pytania">
  <div class="wrap company-faq-editorial__grid">
    <header class="company-faq-editorial__intro reveal-left">
      <p class="company-kicker"><span></span>Najczęstsze pytania</p>
      <h2><span>Krótko i rzeczowo.</span><span>Bez pustych obietnic.</span></h2>
      <p>Odpowiedzi wyjaśniają sposób pracy. Ostateczne parametry programu zawsze ustalamy dla konkretnej instalacji.</p>
      <a class="company-inline-link" href="/baza-wiedzy/">Przejdź do bazy wiedzy <span aria-hidden="true">↗</span></a>
    </header>
    <div class="company-faq-editorial__content">{groups}</div>
  </div>
</section>
""" + _company_final(
        "Nie znalazłeś odpowiedzi?",
        "Nie ma tu Państwa pytania? Porozmawiajmy o konkretnej instalacji.",
        "Wystarczy typ urządzenia i krótki opis problemu. Inżynier dopyta o dane potrzebne do pierwszej oceny.",
        "Zadaj pytanie inżynierowi",
        "/kontakt/",
    ), _faq_schema(all_questions)


def _icon(kind):
    paths = {
        "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.64a2 2 0 0 1-.45 2.11L8 9.75a16 16 0 0 0 6 6l1.28-1.28a2 2 0 0 1 2.11-.45c.86.29 1.74.5 2.64.62A2 2 0 0 1 22 16.92Z"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        "pin": '<path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[kind]}</svg>'


def _render_contact(site):
    return f"""
<section class="contact-editorial-hero" id="top">
  <video class="contact-editorial-hero__media" autoplay muted loop playsinline preload="auto" poster="/assets/visuals-v2/contact-v2.jpg" aria-hidden="true" tabindex="-1">
    <source src="/assets/contact-hero-v2.mp4" type="video/mp4">
  </video>
  <div class="contact-editorial-hero__shade" aria-hidden="true"></div>
  <div class="wrap contact-editorial-hero__inner">
    <div class="contact-editorial-hero__copy">
      <p class="company-kicker"><span></span>Kontakt z KABI CHEMIE</p>
      <h1>Porozmawiajmy o <span>Państwa instalacji.</span></h1>
      <p>Proszę krótko opisać instalację. Nasz inżynier uporządkuje temat i wskaże rozsądny kolejny krok.</p>
      <div class="contact-editorial-hero__actions">
        <a class="btn btn-primary" href="#kontakt-form">Napisz do nas</a>
        <a class="contact-editorial-hero__call" href="tel:{site['phone_raw']}" aria-label="Zadzwoń do biura KABI CHEMIE pod numer {site['phone']}">{_icon("phone")}<span>Zadzwoń do biura</span></a>
      </div>
    </div>
    <aside class="contact-editorial-directory" aria-label="Dane kontaktowe KABI CHEMIE">
      <p class="contact-editorial-directory__label">Dane kontaktowe</p>
      <address class="contact-editorial-office">
        <div class="contact-editorial-office__heading">
          <span class="contact-editorial-office__icon">{_icon("pin")}</span>
          <strong>KABI CHEMIE</strong>
        </div>
        <p>{site['postal_code']} {site['city']}<br>{site['street']}<br><span>NIP: {site['nip']}</span></p>
        <div class="contact-editorial-office__links">
          <a href="tel:{site['phone_raw']}">{_icon("phone")}<span>{site['phone']}</span></a>
          <a href="mailto:{site['email']}">{_icon("mail")}<span>{site['email']}</span></a>
        </div>
      </address>
    </aside>
  </div>
</section>

<section class="contact-editorial-main" id="kontakt-form">
  <div class="wrap contact-editorial-main__grid">
    <aside class="contact-editorial-details reveal-left">
      <p class="company-kicker company-kicker--dark"><span></span>Formularz kontaktowy</p>
      <h2><span>Napisz, czego</span><span>dotyczy instalacja.</span></h2>
      <p>Nie trzeba przygotowywać pełnej dokumentacji. Nazwa firmy, numer telefonu i kilka słów o sprawie wystarczą, aby skierować wiadomość do właściwej osoby.</p>
      <p class="contact-editorial-details__note">W pilnej sprawie prosimy o bezpośredni telefon do biura.</p>
    </aside>
    <div class="contact-editorial-form-stage reveal-right">
      <span class="contact-editorial-form-sigil" aria-hidden="true"></span>
      <form class="contact-form contact-form--smart contact-editorial-form" data-email="{site['email']}" novalidate>
      <div class="contact-editorial-form__head">
        <strong>Napisz do nas</strong>
      </div>
      <div class="field field--identity">
        <label for="editorial-contact-identity">Firma / imię i nazwisko <span class="field-meta">wymagane</span></label>
        <input id="editorial-contact-identity" name="identity" autocomplete="name organization" required placeholder="np. ABC Sp. z o.o., Jan Kowalski">
        <p class="field-hint">Podaj nazwę firmy i osobę, do której możemy oddzwonić.</p>
      </div>
      <div class="contact-form__row">
        <div class="field field--phone">
          <label for="editorial-contact-phone">Telefon <span class="field-meta">wymagane</span></label>
          <input id="editorial-contact-phone" name="phone" type="tel" autocomplete="tel" required placeholder="np. 600 000 000">
        </div>
        <div class="field field--email">
          <label for="editorial-contact-email">Adres e-mail <span class="field-meta">opcjonalne</span></label>
          <input id="editorial-contact-email" name="email" type="email" autocomplete="email" placeholder="np. biuro@firma.pl">
        </div>
      </div>
      <div class="field field--message">
        <label for="editorial-contact-message">Wiadomość <span class="field-meta">opcjonalne</span></label>
        <textarea id="editorial-contact-message" name="message" rows="5" placeholder="Napisz krótko, czego dotyczy sprawa lub jaki typ instalacji mamy omówić."></textarea>
      </div>
      <div class="form-consents" aria-label="Zgody i informacje prawne">
        <label class="form-consent form-consent--required" for="editorial-contact-privacy-consent">
          <input id="editorial-contact-privacy-consent" name="privacyConsent" type="checkbox" required>
          <span>Zgadzam się na kontakt w sprawie zapytania zgodnie z <a href="/polityka-prywatnosci/">polityką prywatności</a>. <span class="form-consent__tag">wymagane</span></span>
        </label>
      </div>
      <button type="submit" class="btn btn-primary">Wyślij wiadomość <span aria-hidden="true">→</span></button>
      <p class="form-note" role="status" aria-live="polite" hidden></p>
      </form>
    </div>
  </div>
</section>
"""


def _render_case_index():
    hero = _case_index_hero()
    return hero + """
<section class="company-stories" id="realizacje">
  <span class="section-bg-word section-bg-word--dark" aria-hidden="true">REALIZACJE</span>
  <img class="section-bg-logo section-bg-logo--dark" src="/assets/kabi-sygnet.svg" alt="" aria-hidden="true">
  <div class="wrap company-stories__grid">
    <header class="company-stories__intro reveal-left">
      <p class="company-kicker"><span></span>Wybrane realizacje</p>
      <h2><span>Wdrożenia KCAQUA</span><span>w przemyśle.</span></h2>
      <p>Każdy materiał pokazuje konkretny punkt wyjścia, zakres działań i efekt ważny dla codziennej pracy instalacji.</p>
      <div class="stories-search">
        <label class="stories-search__field">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
          <input type="search" class="stories-search__input" placeholder="Szukaj po tytule lub kategorii…" aria-label="Szukaj po tytule lub kategorii" data-stories-search>
        </label>
      </div>
    </header>
    <div class="company-stories__list">
      <a class="reveal" href="/case-study/kociol-parowy-fako/"><span>Kotłownia parowa</span><strong>Fako: odzysk wymiany ciepła i niższe zużycie paliwa.</strong><i aria-hidden="true">↗</i></a>
      <a class="reveal" href="/case-study/skraplacz-bac-kcaqua/"><span>Chłodnictwo przemysłowe</span><strong>BAC: stabilniejsza praca skraplacza z programem KCAQUA 305.</strong><i aria-hidden="true">↗</i></a>
      <a class="reveal" href="/case-study/skraplacz-evapco-przetworstwo-rybne/"><span>Przetwórstwo rybne</span><strong>Evapco: odzysk wydajności chłodzenia bez wymiany urządzenia.</strong><i aria-hidden="true">↗</i></a>
      <a class="reveal" href="/case-study/warsztaty-amoniakalne-2024/"><span>Wiedza techniczna</span><strong>Warsztaty Amoniakalne 2024: praktyka prowadzenia wody w chłodnictwie.</strong><i aria-hidden="true">↗</i></a>
      """ + _index_rows_standard() + """
      <p class="stories-search__empty" data-stories-empty hidden>Brak realizacji zawierających podaną frazę.</p>
    </div>
  </div>
</section>
""" + _company_final(
        "Podobna instalacja",
        "Sprawdź, ile zaoszczędzi Twój zakład.",
        "Bezpłatna konsultacja techniczna z inżynierem KABI CHEMIE, bez zobowiązań. Opisz instalację, a wskażemy właściwy punkt odniesienia.",
        "Umów bezpłatną konsultację",
        "/bezplatna-konsultacja/",
    )


WARSZTATY_FAQ = [
    (
        "Dlaczego jakość wody wpływa na wydajność skraplacza wyparnego?",
        "Osad, biofilm i niewłaściwe zasolenie ograniczają kontakt wody z powierzchnią wymiany ciepła. Układ może wtedy zużywać więcej wody i energii, a parametry chłodzenia stają się mniej przewidywalne.",
    ),
    (
        "Które parametry warto obserwować podczas normalnej pracy?",
        "Zakres zależy od instalacji, ale zwykle obejmuje przewodność, pH, twardość wody uzupełniającej, zasadowość oraz wskaźniki mikrobiologiczne. Równie ważne są odsalanie, zużycie wody i warunki obciążenia układu.",
    ),
    (
        "Czy zwiększenie odsalania zawsze poprawia bezpieczeństwo instalacji?",
        "Nie. Nadmierne odsalanie zwiększa zużycie wody i ilość ścieków, a nadal nie rozwiązuje problemów z dozowaniem, dystrybucją wody lub biofilmem. Nastawy powinny wynikać z pomiarów i bilansu całego układu.",
    ),
    (
        "Kiedy sama korekta programu chemicznego nie wystarczy?",
        "Gdy problem wynika z niedrożnych dysz, nierównomiernego zraszania, uszkodzeń powierzchni, niewłaściwej filtracji albo braku kontroli nad punktem dozowania. Wtedy potrzebna jest również korekta techniczna lub serwisowa.",
    ),
    (
        "Od czego rozpocząć ocenę własnego układu chłodniczego?",
        "Od krótkiego bilansu: jakości wody uzupełniającej, aktualnych nastaw, zużycia wody, częstotliwości czyszczenia i obserwowanych objawów. Na tej podstawie można wskazać pomiary, które rzeczywiście pomogą podjąć decyzję.",
    ),
]


def _render_warsztaty():
    focus = [
        ("thermometer", "Wymiana ciepła", "Czysta i równomiernie zwilżana powierzchnia pozwala utrzymać sprawność bez kompensowania strat pracą wentylatorów i pomp."),
        ("water", "Woda i odsalanie", "Przewodność oraz bilans wody pokazują, czy instalacja pracuje w bezpiecznym zakresie bez niepotrzebnego zrzutu."),
        ("shield", "Ochrona instalacji", "Program powinien jednocześnie ograniczać osad, korozję i ryzyko mikrobiologiczne, a jego skuteczność musi być możliwa do sprawdzenia."),
    ]
    focus_html = _join(
        f"""
        <article class="ammonia-focus__row reveal">
          <span class="ammonia-icon" aria-hidden="true">{_case_icon(icon)}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for icon, title, text in focus
    )

    inspection = [
        ("search", "Oględziny powierzchni", "Sprawdzamy rozkład osadu, drożność i miejsca, w których woda nie pracuje równomiernie."),
        ("clean", "Ocena charakteru osadu", "Wygląd powierzchni zestawiamy z wynikami wody i historią eksploatacji, zamiast opierać decyzję na jednym parametrze."),
        ("wrench", "Decyzja techniczna", "Dopiero wtedy określamy, czy potrzebna jest korekta nastaw, czyszczenie, serwis albo zmiana programu ochrony."),
    ]
    inspection_html = _join(
        f"""
        <article class="ammonia-inspection__step reveal">
          <span class="ammonia-icon" aria-hidden="true">{_case_icon(icon)}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for icon, title, text in inspection
    )

    takeaways = [
        ("valve", "Prowadź układ według obciążenia", "Stała nastawa nie odpowiada na zmianę temperatury, jakości wody ani intensywności pracy instalacji."),
        ("sliders", "Łącz pomiar z nastawą", "Wynik ma prowadzić do konkretnej decyzji o odsalaniu, dawce, filtracji lub przeglądzie urządzenia."),
        ("report", "Zostaw czytelny punkt odniesienia", "Trend parametrów, zużycia wody i obserwacji serwisowych pozwala ocenić, czy program naprawdę działa."),
    ]
    takeaways_html = _join(
        f"""
        <article class="ammonia-takeaways__item reveal">
          <span class="ammonia-icon ammonia-icon--dark" aria-hidden="true">{_case_icon(icon)}</span>
          <div><h3>{title}</h3><p>{text}</p></div>
        </article>"""
        for icon, title, text in takeaways
    )

    faq_html = _join(
        f"""
        <details{' open' if index == 0 else ''}>
          <summary><span>{question}</span><i aria-hidden="true"></i></summary>
          <div><p>{answer}</p></div>
        </details>"""
        for index, (question, answer) in enumerate(WARSZTATY_FAQ)
    )

    return f"""
<section class="ammonia-hero" id="top">
  <div class="ammonia-hero__media" aria-hidden="true"></div>
  <div class="ammonia-hero__shade" aria-hidden="true"></div>
  <span class="ammonia-sigil ammonia-sigil--hero" aria-hidden="true"></span>
  <div class="wrap ammonia-hero__inner">
    <div class="ammonia-hero__copy">
      <p class="ammonia-kicker"><span></span>Warsztaty Amoniakalne 2024</p>
      <h1><span>Woda pod kontrolą.</span><span>Chłodzenie <em>bez niespodzianek.</em></span></h1>
      <p class="ammonia-hero__lead">Najważniejsze wnioski dla osób, które odpowiadają za skraplacze wyparne, zużycie wody i stabilną pracę instalacji amoniakalnej.</p>
      <div class="ammonia-hero__actions">
        <a class="btn btn-primary" href="#wnioski">Zobacz najważniejsze wnioski</a>
        <a class="ammonia-text-link" href="/uklady-chlodnicze/">Poznaj rozwiązania dla chłodnictwa <span aria-hidden="true">↗</span></a>
      </div>
      <ul class="ammonia-hero__signals" aria-label="Zakres materiału">
        <li>{_case_icon('thermometer')}<span>Wymiana ciepła</span></li>
        <li>{_case_icon('water')}<span>Woda i odsalanie</span></li>
        <li>{_case_icon('shield')}<span>Korozja i mikrobiologia</span></li>
      </ul>
    </div>
  </div>
  <a class="ammonia-hero__scroll" href="#wnioski"><span>Przejdź do wniosków</span><i aria-hidden="true"></i></a>
</section>

<section class="ammonia-focus" id="wnioski">
  <div class="wrap ammonia-focus__grid">
    <header class="ammonia-section-intro reveal-left">
      <p class="ammonia-kicker ammonia-kicker--dark"><span></span>Co decyduje o wyniku</p>
      <h2><span>Jedna instalacja.</span><span>Trzy powiązane obszary.</span></h2>
      <p>Skraplacz nie pracuje w oderwaniu od jakości wody. Efekt techniczny powstaje na styku wymiany ciepła, gospodarki wodnej i ochrony materiałów.</p>
    </header>
    <div class="ammonia-focus__list">{focus_html}</div>
  </div>
</section>

<section class="ammonia-field" aria-label="Pomiar w instalacji">
  <div class="ammonia-field__media" aria-hidden="true"></div>
  <div class="ammonia-field__shade" aria-hidden="true"></div>
  <div class="wrap ammonia-field__inner">
    <div class="ammonia-field__copy reveal-left">
      <p class="ammonia-kicker"><span></span>Pomiar w kontekście</p>
      <h2><span>Próbka mówi więcej,</span><span>gdy znamy warunki pracy.</span></h2>
      <p>Wynik laboratoryjny zestawiamy z punktem poboru, temperaturą, odsalaniem, obciążeniem i zużyciem wody. Dopiero takie połączenie prowadzi do wiarygodnej korekty programu.</p>
      <ul>
        <li>{_case_icon('search')}<span>Właściwy punkt poboru</span></li>
        <li>{_case_icon('gauge')}<span>Rzeczywiste obciążenie układu</span></li>
        <li>{_case_icon('sliders')}<span>Aktualne nastawy i dozowanie</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="ammonia-inspection">
  <div class="wrap ammonia-inspection__grid">
    <figure class="ammonia-inspection__media reveal-left">
      <img src="/assets/case/case-ammonia-workshop-inspection.png" alt="Inspekcja powierzchni wymiany ciepła w instalacji przemysłowej" loading="lazy" decoding="async">
      <figcaption>Inspekcja powierzchni pozwala połączyć wyniki wody z rzeczywistym stanem urządzenia.</figcaption>
    </figure>
    <div class="ammonia-inspection__content reveal-right">
      <p class="ammonia-kicker ammonia-kicker--dark"><span></span>Od pomiaru do decyzji</p>
      <h2><span>Wyniki wskazują kierunek.</span><span>Inspekcja potwierdza stan.</span></h2>
      <div class="ammonia-inspection__steps">{inspection_html}</div>
    </div>
  </div>
</section>

<section class="ammonia-takeaways">
  <div class="wrap ammonia-takeaways__grid">
    <header class="ammonia-section-intro ammonia-section-intro--dark reveal-left">
      <p class="ammonia-kicker"><span></span>Wnioski do zastosowania</p>
      <h2><span>Trzy decyzje, które</span><span>porządkują pracę układu.</span></h2>
      <p>Warsztaty były punktem wymiany doświadczeń. W praktyce najważniejsze jest przełożenie wiedzy na prosty rytm kontroli i działania.</p>
    </header>
    <div class="ammonia-takeaways__list">{takeaways_html}</div>
  </div>
</section>

<nav class="ammonia-related" aria-label="Powiązane rozwiązania i realizacje">
  <div class="wrap ammonia-related__inner">
    <p>Przejdź dalej</p>
    <a href="/uklady-chlodnicze/"><span>Rozwiązanie</span><strong>Skraplacze wyparne</strong><i aria-hidden="true">↗</i></a>
    <a href="/case-study/skraplacz-bac-kcaqua/"><span>Realizacja</span><strong>BAC: program KCAQUA 305</strong><i aria-hidden="true">↗</i></a>
    <a href="/case-study/skraplacz-evapco-przetworstwo-rybne/"><span>Realizacja</span><strong>Evapco: odzyskana wymiana ciepła</strong><i aria-hidden="true">↗</i></a>
  </div>
</nav>

<section class="ammonia-faq" id="faq">
  <div class="wrap ammonia-faq__grid">
    <header class="ammonia-section-intro ammonia-section-intro--dark reveal-left">
      <p class="ammonia-kicker"><span></span>FAQ techniczne</p>
      <h2><span>Pytania o pracę</span><span>układu chłodniczego.</span></h2>
      <p>Konkretne odpowiedzi pomagają przygotować dane i szybciej przejść od objawu do właściwej decyzji technicznej.</p>
    </header>
    <div class="ammonia-faq__list">{faq_html}</div>
  </div>
</section>

<section class="ammonia-cta">
  <span class="ammonia-sigil ammonia-sigil--cta" aria-hidden="true"></span>
  <div class="wrap ammonia-cta__inner">
    <div>
      <p class="ammonia-kicker ammonia-kicker--dark"><span></span>Państwa instalacja</p>
      <h2><span>Sprawdźmy Państwa układ</span><span>w rzeczywistych warunkach.</span></h2>
      <p>Krótki opis instalacji i obserwowanych objawów wystarczy, aby wskazać dane potrzebne do pierwszej oceny.</p>
    </div>
    <div class="ammonia-cta__actions">
      <a class="btn btn-primary" href="/kontakt/">Wyślij zapytanie techniczne</a>
      <a class="ammonia-phone" href="tel:+48662792875" aria-label="Zadzwoń do KABI CHEMIE: +48 662 792 875">{_case_icon('phone')}<span>+48 662 792 875</span></a>
    </div>
  </div>
</section>
"""


# Nowe case studies używają silnika bazy wiedzy (te same pola: title, lead,
# prose, html, faq, related). Wygląd = strony rozwiązań/bazy wiedzy.
CASE_BODY_CLASS = "has-dark-hero firm-page solution-page knowledge-page"


def _case_standardowe(case):
    """Wpis „artykułowy" (nowy) rozpoznajemy po treści prose albo własnym HTML.
    Stare 3 wpisy nie mają żadnego z nich — idą dawnym, bogatym rendererem."""
    return bool((case.get("prose") or "").strip() or (case.get("html") or "").strip())


def render_case_standard(a):
    """Case study renderowane DOKŁADNIE jak artykuł bazy wiedzy: własny HTML
    całości albo hero + prose + powiązane + FAQ + CTA. Różni się od artykułu
    tylko etykietami (kicker „Case study", powrót na /case-study/)."""
    import knowledge_pages as kp

    wlasny = (a.get("html") or "").strip()
    if wlasny:
        return wlasny

    facts = [
        ("Czas czytania", a.get("read") or a.get("read_time") or "— min"),
        ("Dla kogo", a.get("audience") or "Utrzymanie ruchu i decyzje techniczne."),
        ("Kolejny krok", "Umów konsultację techniczną."),
    ]
    hero = kp._hero(
        a.get("image") or "/assets/case/case-fako-boiler-generated.png",
        "Case study", a["title"], a["lead"], facts,
        ("Umów konsultację", "/bezplatna-konsultacja/"),
        ("Wróć do case studies", "/case-study/"),
    )
    body = ('<section class="section knowledge-article reveal">'
            f'<div class="wrap narrow prose">{a["prose"]}</div></section>')
    return (hero + body + kp._related(a.get("related", []))
            + kp._faq(a.get("faq", [])) + kp._cta())


def _index_rows_standard():
    """Wiersze indeksu /case-study/ dla nowych, artykułowych wpisów."""
    return _join(
        f'<a class="reveal" href="{c["path"]}">'
        f'<span>{c.get("topic") or "Realizacja"}</span>'
        f'<strong>{c.get("list_title") or c.get("title") or c["slug"]}</strong>'
        f'<i aria-hidden="true">↗</i></a>'
        for c in CASE_STUDIES if _case_standardowe(c)
    )


def install_company_case_pages(pages, custom, site):
    for case in CASE_STUDIES:
        if _case_standardowe(case):
            # Nowy wpis „artykułowy" — silnik jak baza wiedzy.
            tytul = (case.get("title") or "").strip() or case["slug"]
            pages[case["path"]] = {
                "title": tytul,
                "meta": case.get("lead", ""),
                "h1": tytul,
                "og_type": "article",
                "og_image": case.get("image") or "/assets/case/case-fako-boiler-generated.png",
                "body_class": CASE_BODY_CLASS,
                "jsonld": [_faq_schema(case.get("faq", []))],
                "sections": [custom(render_case_standard(case))],
            }
            continue
        # Istniejący, „niestandardowy" wpis — dawny, bogaty układ sekcyjny.
        pages[case["path"]] = {
            "title": case["h1"].replace("<span>", "").replace("</span>", ""),
            "meta": case["lead"],
            "h1": case["h1"].replace("<span>", "").replace("</span>", ""),
            "og_image": case["image"],
            "og_type": "article",
            "body_class": f"has-dark-hero case-story-page case-story-page--{case['slug']}",
            "jsonld": [_faq_schema(case["faq"])],
            "sections": [custom(_render_case(case))],
        }

    faq_html, faq_schema = _render_faq()

    pages["/case-study/"] = {
        "h1": "Case Studies: Realizacje z zakresu uzdatniania wody",
        "og_image": "/assets/case/case-fako-boiler-generated.png",
        "body_class": "has-dark-hero company-editorial-page company-references-editorial-page case-index-editorial-page",
        "sections": [custom(_render_case_index())],
    }
    pages["/case-study/warsztaty-amoniakalne-2024/"] = {
        "title": "Warsztaty Amoniakalne 2024 | Wnioski dla chłodnictwa",
        "meta": "Praktyczne wnioski z Warsztatów Amoniakalnych 2024: wymiana ciepła, jakość wody, odsalanie i ochrona skraplaczy wyparnych.",
        "h1": "Woda pod kontrolą. Chłodzenie bez niespodzianek.",
        "og_type": "article",
        "og_image": "/assets/case/case-ammonia-workshop-hero.png",
        "body_class": "has-dark-hero case-warsztaty-editorial-page",
        "jsonld": [_faq_schema(WARSZTATY_FAQ)],
        "sections": [custom(_render_warsztaty())],
    }

    pages["/o-firmie/"] = {
        "title": "KABI CHEMIE - kontrola wody przemysłowej z KCAQUA",
        "meta": "KABI CHEMIE łączy analizę wody, chemię KCAQUA, dozowanie i nadzór, aby ograniczać zużycie mediów i chronić instalacje przemysłowe.",
        "h1": "Woda przemysłowa pod kontrolą.",
        "og_image": "/assets/visuals-v2/company-mission-v2.jpg",
        "body_class": "has-dark-hero company-editorial-page company-about-editorial-page",
        "no_breadcrumbs": True,
        "sections": [custom(_render_about())],
    }
    pages["/warunki-wspolpracy/"] = {
        "title": "Model współpracy KABI CHEMIE | Od diagnozy do wyniku",
        "meta": "Poznaj model współpracy KABI CHEMIE: od rozmowy technicznej i diagnozy, przez program KCAQUA, po monitoring danych z instalacji.",
        "h1": "Od diagnozy do wyniku.",
        "og_image": "/assets/visuals-v2/company-collaboration-v2.jpg",
        "body_class": "has-dark-hero company-editorial-page company-model-editorial-page",
        "sections": [custom(_render_model())],
    }
    pages["/referencje/"] = {
        "title": "Referencje KABI CHEMIE | Wyniki z instalacji przemysłowych",
        "meta": "Wybrane realizacje KABI CHEMIE dla kotłów parowych, skraplaczy wyparnych i instalacji RO. Poznaj zakres prac i wyniki potwierdzone danymi.",
        "h1": "Wdrożenia potwierdzone danymi z instalacji.",
        "og_image": "/assets/visuals-v2/company-references-v2.jpg",
        "body_class": "has-dark-hero company-editorial-page company-references-editorial-page",
        "sections": [custom(_render_references())],
    }
    pages["/faq/"] = {
        "title": "FAQ KABI CHEMIE | Audyt, KCAQUA i współpraca",
        "meta": "Konkretne odpowiedzi o audycie technicznym, programie KCAQUA, instalacjach przemysłowych, wdrożeniu i opiece KABI CHEMIE.",
        "h1": "Odpowiedzi przed pierwszą rozmową.",
        "og_image": "/assets/visuals-v2/company-faq-v2.jpg",
        "body_class": "has-dark-hero company-editorial-page company-faq-editorial-page",
        "jsonld": [faq_schema],
        "sections": [custom(faq_html)],
    }
    pages["/kontakt/"] = {
        "title": "Kontakt z KABI CHEMIE | Rozmowa z inżynierem",
        "meta": "Skontaktuj się z inżynierem KABI CHEMIE. Opisz instalację, problem z wodą lub zadzwoń, aby ustalić kolejny krok.",
        "h1": "Porozmawiajmy o Twojej instalacji.",
        "og_image": "/assets/visuals-v2/contact-v2.jpg",
        "body_class": "has-dark-hero contact-editorial-page",
        "sections": [custom(_render_contact(site))],
    }
