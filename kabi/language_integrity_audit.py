# -*- coding: utf-8 -*-
"""Deep language, bidirectional text and compact-UI audit for localized pages."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

from lxml import html

import localize_site as L


ROOT = Path(__file__).resolve().parent
WWW = ROOT / "www"
I18N = ROOT / "i18n"

MOJIBAKE = re.compile(r"�|Ã.|Â(?!°|µ)|Å[\x80-\xbf]|Ř.|Ů.")
POLISH_LETTERS = re.compile(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]")
POLISH_TERMS = re.compile(
    r"\b(?:strona|główna|rozwiązania|branże|firma|kontakt|woda|wody|"
    r"instalacja|instalacji|sprawdź|umów|zobacz|czytaj|więcej|mniej|"
    r"kamień|korozja|osad|kocioł|kotły|skraplacz|ochrona|analiza)\b",
    re.IGNORECASE,
)
SUSPICIOUS_EN = re.compile(
    r"\b(?:stones?|traffic|settlements?|dispensing|desalination|"
    r"destone(?:d|ing)?|descalation|betting|refrigerator|aircraft|tanks?)\b",
    re.IGNORECASE,
)
SUSPICIOUS_DE = re.compile(
    r"\b(?:Steine?|Verkehr|Siedlungen?|Zubereitungen?|Abgabe|Entsalzung|Wette|"
    r"Kühlschrank|Flugzeug|Panzer)\b",
    re.IGNORECASE,
)
SUSPICIOUS_AR = re.compile(
    r"(?:فساد|حجارة|طائرات|دبابات|تحطيم|الأمونيكال|الثلاجة الصناعية|"
    r"المنشط|المزق|الاطارات|القوارض)"
)
ARABIC = re.compile(r"[\u0600-\u06ff]")
DIGIT = re.compile(r"\d")
COMPACT_XPATH = (
    '//a[contains(concat(" ", normalize-space(@class), " "), " btn ")]'
    ' | //button | //summary'
    ' | //ul[contains(concat(" ", normalize-space(@class), " "), " menu ")]/li/a'
)

ALLOWED_POLISH = {
    "Łukasz Mielcarz", "Przemysław Jesiołkowski", "Łukasz Kumor",
    "Żabokliki-Kolonia", "Toruń", "Siedlce", "KABI CHEMIE", "KCAQUA",
}
AR_LATIN_ALLOWED = {
    "08-110 Siedlce", "4200 µS", "8 °n", "KCAQUA 305",
    "NIP: 8212519774", "OSM Siedlce", "Żabokliki-Kolonia ul. Stocka 10",
}


def strip_allowed(value: str) -> str:
    value = re.sub(r"https?://\S+|\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", "", value)
    value = value.replace("kondycjonowanie-wody.pl", "")
    for term in ALLOWED_POLISH:
        value = value.replace(term, "")
    return value


def catalog() -> set[str]:
    strings = L.collect_js_strings()
    for page in L.source_pages():
        strings.update(L.collect_page_strings(L.parse_page(page)))
    return strings


def mapping_issues(lang: str, strings: set[str]) -> list[dict[str, str]]:
    mapping = L.load_cache(lang)
    issues: list[dict[str, str]] = []
    for source in sorted(strings, key=str.casefold):
        target = mapping.get(source, "")
        if not target:
            issues.append({"kind": "missing", "source": source, "target": target})
            continue
        if MOJIBAKE.search(target):
            issues.append({"kind": "mojibake", "source": source, "target": target})
        source_numbers = re.findall(r"\d+(?:[.,]\d+)?", source)
        target_numbers = re.findall(r"\d+(?:[.,]\d+)?", target)
        if source_numbers != target_numbers:
            issues.append({"kind": "numbers", "source": source, "target": target})
        probe = strip_allowed(target)
        polish_match = POLISH_TERMS.search(probe) if lang in {"en", "de"} else None
        if polish_match and not (lang == "de" and polish_match.group(0).casefold() == "kontakt"):
            issues.append({"kind": "polish-term", "source": source, "target": target})
        elif lang in {"en", "de"} and POLISH_LETTERS.search(probe):
            issues.append({"kind": "polish-letter", "source": source, "target": target})
        if lang == "en" and SUSPICIOUS_EN.search(target):
            issues.append({"kind": "technical-calque", "source": source, "target": target})
        if lang == "de" and SUSPICIOUS_DE.search(target):
            issues.append({"kind": "technical-calque", "source": source, "target": target})
        if lang == "ar":
            if SUSPICIOUS_AR.search(target):
                issues.append({"kind": "technical-calque", "source": source, "target": target})
            if (len(target.split()) >= 2 and not ARABIC.search(target)
                    and source not in L.PRESERVE_EXACT and target not in AR_LATIN_ALLOWED):
                issues.append({"kind": "latin-only", "source": source, "target": target})
    return issues


def has_ltr_context(element) -> bool:
    current = element
    while current is not None:
        if current.get("dir") == "ltr" or current.tag == "bdi":
            return True
        current = current.getparent()
    return False


def arabic_dom_issues() -> tuple[list[dict[str, str]], Counter]:
    issues: list[dict[str, str]] = []
    longest: Counter = Counter()
    for path in sorted((WWW / "ar").rglob("*.html")):
        doc = html.document_fromstring(path.read_bytes(), parser=html.HTMLParser(encoding="utf-8"))
        rel = path.relative_to(WWW).as_posix()
        for node in doc.xpath("//body//text()[normalize-space()]"):
            parent = node.getparent()
            if parent is None or parent.tag in L.SKIP_TAGS or parent.tag in {"bdi", "option"}:
                continue
            value = " ".join(str(node).split())
            if DIGIT.search(value) and not has_ltr_context(parent):
                issues.append({"kind": "unisolated-number", "page": rel, "text": value[:220]})
        for anchor in doc.xpath('//a[starts-with(@href,"tel:")]'):
            if anchor.get("dir") != "ltr":
                issues.append({"kind": "phone-direction", "page": rel, "text": " ".join(anchor.text_content().split())})
        for control in doc.xpath('//input[@type="number" or @type="tel" or @inputmode="decimal" or @inputmode="numeric"]'):
            if control.get("dir") != "ltr":
                issues.append({"kind": "control-direction", "page": rel, "text": control.get("name") or control.get("id") or control.tag})
        for element in doc.xpath(COMPACT_XPATH):
            text = " ".join(element.text_content().split())
            if text:
                longest[(rel, element.tag, text)] = len(text)
    return issues, longest


def compact_text_report(lang: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted((WWW / lang).rglob("*.html")):
        doc = html.document_fromstring(path.read_bytes(), parser=html.HTMLParser(encoding="utf-8"))
        rel = path.relative_to(WWW).as_posix()
        source_rel = path.relative_to(WWW / lang)
        source_path = WWW / source_rel
        source_elements = []
        if source_path.exists():
            source_doc = html.document_fromstring(
                source_path.read_bytes(), parser=html.HTMLParser(encoding="utf-8")
            )
            source_elements = source_doc.xpath(COMPACT_XPATH)
        for index, element in enumerate(doc.xpath(COMPACT_XPATH)):
            text = " ".join(element.text_content().split())
            if len(text) >= 44:
                source = ""
                if index < len(source_elements):
                    source = " ".join(source_elements[index].text_content().split())
                rows.append({
                    "page": rel,
                    "tag": element.tag,
                    "length": len(text),
                    "source": source,
                    "text": text,
                })
    return sorted(rows, key=lambda row: int(row["length"]), reverse=True)


def main() -> int:
    strings = catalog()
    report: dict[str, object] = {"catalog_strings": len(strings), "languages": {}}
    total_errors = 0
    for lang in L.LANGS:
        issues = mapping_issues(lang, strings)
        compact = compact_text_report(lang)
        report["languages"][lang] = {
            "mapping_issues": issues,
            "compact_text_review": compact,
        }
        total_errors += len(issues)
        print(f"{lang.upper()}: katalog={len(strings)}, problemy językowe={len(issues)}, długie kontrolki={len(compact)}")
    bidi, _ = arabic_dom_issues()
    report["arabic_bidi_issues"] = bidi
    total_errors += len(bidi)
    print(f"AR RTL: nieizolowane liczby i kontrolki={len(bidi)}")
    by_kind = Counter(item["kind"] for lang in L.LANGS for item in report["languages"][lang]["mapping_issues"])
    by_kind.update(item["kind"] for item in bidi)
    print("Kategorie:", dict(by_kind))
    (I18N / "language-integrity-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("WYNIK:", "OK" if total_errors == 0 else f"WYMAGA POPRAWEK ({total_errors})")
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
