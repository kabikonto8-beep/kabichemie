# -*- coding: utf-8 -*-
"""Jednorazowy zrzut treści z modułów .py do content/snapshot.json.

To jest most między starym a nowym światem: czyta literały ARTICLES /
CATEGORIES / HUB / CASE_STUDIES z knowledge_pages.py i company_case_pages.py
i zapisuje je w formacie snapshotu. Po migracji źródłem prawdy jest Postgres,
a ten skrypt zostaje wyłącznie jako zapis pochodzenia danych.

Uruchomienie:
    docker compose run --rm --no-deps builder python /builder/seed_from_python.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/builder")
sys.path.insert(0, "/site")

from content_schema import to_snapshot  # noqa: E402

SNAPSHOT = Path("/site/content/snapshot.json")


def main():
    import knowledge_pages as K
    import company_case_pages as CC

    data = {
        "wersja": 1,
        "zrodlo": "seed_from_python.py — literały z knowledge_pages.py i company_case_pages.py",
        "hub": to_snapshot(K.HUB),
        "categories": [to_snapshot(r) for r in K.CATEGORIES],
        "articles": [to_snapshot(r) for r in K.ARTICLES],
        "case_studies": [to_snapshot(r) for r in CC.CASE_STUDIES],
    }

    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    with SNAPSHOT.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")

    print("zapisano %s" % SNAPSHOT)
    print("  kategorie:    %d" % len(data["categories"]))
    print("  artykuly:     %d" % len(data["articles"]))
    print("  case studies: %d" % len(data["case_studies"]))


if __name__ == "__main__":
    main()
