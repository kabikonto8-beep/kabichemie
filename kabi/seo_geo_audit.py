# -*- coding: utf-8 -*-
"""Deep technical audit for SEO, GEO, images, structured data and crawler files."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

from lxml import etree, html


ROOT = Path(__file__).resolve().parent
WWW = ROOT / "www"
DOMAIN = "https://kondycjonowanie-wody.pl"
LANGS = {"pl": "pl-PL", "en": "en", "de": "de", "ar": "ar"}
NOINDEX_BASE_ROUTES = {
    "/404/",
    "/autor/",
    *(f"/baza-wiedzy/artykul-testowy-{index:02d}/" for index in range(1, 21)),
}
SECURITY_HEADERS = {
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "Strict-Transport-Security",
    "Content-Security-Policy",
}


def route_for(path: Path) -> str:
    relative = path.relative_to(WWW).as_posix()
    return "/" if relative == "index.html" else "/" + relative.removesuffix("index.html")


def base_route(route: str) -> str:
    match = re.match(r"^/(en|de|ar)(/.*)$", route)
    return match.group(2) if match else route


def expected_language(route: str) -> str:
    match = re.match(r"^/(en|de|ar)(?:/|$)", route)
    return match.group(1) if match else "pl"


def is_redirect(document, source: str) -> bool:
    return bool(document.xpath('//meta[translate(@http-equiv,"REFSH","refsh")="refresh"]')) and "noindex" in source


def has_hidden_ancestor(node) -> bool:
    current = node
    while current is not None:
        if current.get("aria-hidden") == "true":
            return True
        current = current.getparent()
    return False


def walk_json(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json(child)


def add_error(errors: list[str], route: str, message: str) -> None:
    errors.append(f"{route}: {message}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    indexable_urls: set[str] = set()
    page_count = redirect_count = image_count = json_count = 0

    for path in sorted(WWW.rglob("index.html")):
        route = route_for(path)
        source = path.read_text(encoding="utf-8")
        document = html.fromstring(source)
        if is_redirect(document, source):
            redirect_count += 1
            continue

        page_count += 1
        language = expected_language(route)
        canonical_url = DOMAIN + route
        noindex_expected = base_route(route) in NOINDEX_BASE_ROUTES

        root = document.getroottree().getroot()
        if root.get("lang") != language:
            add_error(errors, route, f"html lang={root.get('lang')!r}, oczekiwano {language!r}")
        if language == "ar" and root.get("dir") != "rtl":
            add_error(errors, route, "wersja arabska bez dir=rtl")

        exact_one = {
            "title": document.xpath("/html/head/title[normalize-space()]"),
            "meta description": document.xpath('/html/head/meta[@name="description"][@content]'),
            "canonical": document.xpath('/html/head/link[@rel="canonical"][@href]'),
            "meta robots": document.xpath('/html/head/meta[@name="robots"][@content]'),
            "main": document.xpath("//main"),
            "h1": document.xpath("//main//h1"),
        }
        for label, nodes in exact_one.items():
            if len(nodes) != 1:
                add_error(errors, route, f"{label}: znaleziono {len(nodes)}, oczekiwano 1")

        canonical = document.xpath('string(/html/head/link[@rel="canonical"]/@href)')
        if canonical != canonical_url:
            add_error(errors, route, f"canonical {canonical!r} nie odpowiada URL")

        robots = document.xpath('string(/html/head/meta[@name="robots"]/@content)').lower()
        if noindex_expected:
            if "noindex" not in robots:
                add_error(errors, route, "strona techniczna/testowa bez noindex")
        else:
            if "index" not in robots or "noindex" in robots:
                add_error(errors, route, "gotowa strona nie jest indeksowalna")
            indexable_urls.add(canonical_url)

        hreflangs = document.xpath('/html/head/link[@rel="alternate"][@hreflang]/@hreflang')
        if Counter(hreflangs) != Counter({"pl-PL": 1, "en": 1, "de": 1, "ar": 1, "x-default": 1}):
            add_error(errors, route, f"niepoprawny zestaw hreflang: {hreflangs}")

        for selector, label in (
            ('/html/head/meta[@property="og:image"][@content]', "og:image"),
            ('/html/head/meta[@property="og:image:alt"][@content]', "og:image:alt"),
            ('/html/head/meta[@property="og:image:width"][@content]', "og:image:width"),
            ('/html/head/meta[@property="og:image:height"][@content]', "og:image:height"),
            ('/html/head/meta[@property="og:image:type"][@content]', "og:image:type"),
            ('/html/head/meta[@name="twitter:image"][@content]', "twitter:image"),
            ('/html/head/meta[@name="twitter:image:alt"][@content]', "twitter:image:alt"),
        ):
            if len(document.xpath(selector)) != 1:
                add_error(errors, route, f"brak lub duplikat {label}")

        ids = document.xpath('//@id')
        duplicates = [value for value, count in Counter(ids).items() if count > 1]
        if duplicates:
            add_error(errors, route, f"zduplikowane id HTML: {duplicates[:5]}")

        heading_levels = [int(node.tag[1]) for node in document.xpath('//main//*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6]')]
        if any(current > previous + 1 for previous, current in zip(heading_levels, heading_levels[1:])):
            add_error(errors, route, "przeskok poziomu nagłówków")

        main_text = " ".join(document.xpath('string(//main)').split())
        if not noindex_expected and len(main_text) < 500:
            warnings.append(f"{route}: mało tekstu dostępnego bez JavaScript ({len(main_text)} znaków)")

        for image in document.xpath("//img"):
            image_count += 1
            src = image.get("src", "")
            if image.get("alt") is None:
                add_error(errors, route, f"obraz bez alt: {src}")
            if src.startswith("/assets/"):
                asset = WWW / src.lstrip("/")
                if not asset.exists():
                    add_error(errors, route, f"brak pliku obrazu: {src}")
                for attribute in ("width", "height", "decoding"):
                    if image.get(attribute) is None:
                        add_error(errors, route, f"obraz {src} bez {attribute}")
            if image.get("alt") == "" and not has_hidden_ancestor(image):
                classes = image.get("class", "")
                if not any(token in classes for token in ("logo", "engraving", "mark", "sigil")):
                    add_error(errors, route, f"pusty alt przy obrazie niedekoracyjnym: {src}")

        json_objects = []
        for script in document.xpath('//script[@type="application/ld+json"]'):
            json_count += 1
            try:
                json_objects.append(json.loads(script.text or ""))
            except json.JSONDecodeError as exc:
                add_error(errors, route, f"niepoprawny JSON-LD: {exc}")

        graph = [node for payload in json_objects for node in walk_json(payload)]
        top_types = {item for payload in json_objects for item in ([payload.get("@type")] if not isinstance(payload.get("@type"), list) else payload.get("@type")) if item}
        if "Organization" not in top_types or "WebSite" not in top_types:
            add_error(errors, route, "brak encji Organization lub WebSite")
        if not top_types.intersection({"WebPage", "AboutPage", "ContactPage", "CollectionPage", "Article", "BlogPosting"}):
            add_error(errors, route, "brak encji opisującej stronę")

        for node in graph:
            node_id = node.get("@id")
            if isinstance(node_id, str) and node_id.endswith(("/#organization", "/#website")):
                expected = DOMAIN + ("/#organization" if node_id.endswith("/#organization") else "/#website")
                if node_id != expected:
                    add_error(errors, route, f"rozszczepiona encja globalna: {node_id}")
        page_nodes = [node for node in graph if node.get("@id") == canonical_url + "#webpage"]
        if len(page_nodes) != 1:
            add_error(errors, route, f"oczekiwano jednej encji WebPage dla canonical, znaleziono {len(page_nodes)}")
        elif page_nodes[0].get("url") != canonical_url:
            add_error(errors, route, "URL encji strony nie zgadza się z canonical")

    sitemap = etree.parse(str(WWW / "sitemap.xml"))
    namespaces = {
        "s": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "x": "http://www.w3.org/1999/xhtml",
        "i": "http://www.google.com/schemas/sitemap-image/1.1",
    }
    sitemap_urls = sitemap.xpath("//s:url", namespaces=namespaces)
    locations = [node.xpath("string(./s:loc)", namespaces=namespaces) for node in sitemap_urls]
    if len(locations) != len(set(locations)):
        errors.append("sitemap.xml: zduplikowane adresy loc")
    for node, location in zip(sitemap_urls, locations):
        alternates = node.xpath("./x:link/@hreflang", namespaces=namespaces)
        if Counter(alternates) != Counter({"pl-PL": 1, "en": 1, "de": 1, "ar": 1, "x-default": 1}):
            errors.append(f"sitemap.xml: {location} ma niepoprawne hreflang {alternates}")
        if len(node.xpath("./i:image/i:loc", namespaces=namespaces)) != 1:
            errors.append(f"sitemap.xml: {location} bez dokładnie jednego image:loc")
    if set(locations) != indexable_urls:
        missing = sorted(indexable_urls - set(locations))
        extra = sorted(set(locations) - indexable_urls)
        errors.append(f"sitemap.xml: różnica z indeksem, brak={missing[:5]}, nadmiar={extra[:5]}")

    robots = (WWW / "robots.txt").read_text(encoding="utf-8")
    for token in ("User-agent: *", "User-agent: Googlebot", "User-agent: OAI-SearchBot", "Sitemap: " + DOMAIN + "/sitemap.xml"):
        if token not in robots:
            errors.append(f"robots.txt: brak {token}")
    for filename in ("llms.txt", "llms-full.txt"):
        text = (WWW / filename).read_text(encoding="utf-8")
        if "KABI CHEMIE" not in text or DOMAIN not in text:
            errors.append(f"{filename}: brak opisu firmy lub linków kanonicznych")

    for filename in ("_headers", ".htaccess"):
        text = (WWW / filename).read_text(encoding="utf-8")
        for header in SECURITY_HEADERS:
            if header not in text:
                errors.append(f"{filename}: brak nagłówka {header}")

    print(f"Strony gotowe do indeksacji: {len(indexable_urls)}")
    print(f"Strony noindex: {page_count - len(indexable_urls)}")
    print(f"Przekierowania: {redirect_count}")
    print(f"Obrazy sprawdzone: {image_count}")
    print(f"Bloki JSON-LD sprawdzone: {json_count}")
    print(f"Adresy w sitemapie: {len(locations)}")
    print(f"Ostrzeżenia: {len(warnings)}")
    for warning in warnings[:20]:
        print("  !", warning)
    print(f"Błędy: {len(errors)}")
    for error in errors[:80]:
        print("  X", error)
    print("WYNIK:", "OK" if not errors else "WYMAGA POPRAWEK")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
