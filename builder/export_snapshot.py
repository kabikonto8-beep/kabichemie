# -*- coding: utf-8 -*-
"""PostgreSQL → content/snapshot.json.

Baza jest źródłem prawdy do edycji, snapshot jest tym, co trafia do gita
i z czego buduje się strona. Ten skrypt zamyka obieg.

Zasady eksportu:
  * wpisy z published = false są pomijane — nie trafiają na stronę,
  * kolejność bierze się z sort_order,
  * kolumny o wartości NULL są POMIJANE, a nie zapisywane jako null —
    generator rozróżnia „pola nie ma" od „pole jest puste",
  * kolumny techniczne (id, sort_order, published, znaczniki czasu)
    nie trafiają do snapshotu — to stan bazy, nie treść.

Uruchomienie:
    docker compose run --rm builder python /builder/export_snapshot.py
"""
import json
import os
import sys
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

sys.path.insert(0, "/site")

SNAPSHOT = Path("/site/content/snapshot.json")

# Nigdy nie trafiają do snapshotu.
TECHNICAL = {"id", "category_id", "published", "sort_order",
             "created_at", "updated_at", "published_at"}


def clean(row, rename=None):
    """Usuwa kolumny techniczne i te o wartości NULL, stosuje zmiany nazw."""
    rename = rename or {}
    out = {}
    for key, value in row.items():
        if key in TECHNICAL or value is None:
            continue
        out[rename.get(key, key)] = value
    return out


def main():
    url = os.environ["DATABASE_URL"]
    with psycopg.connect(url) as conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT * FROM kabi.knowledge_hub WHERE id = 1")
        hub_row = cur.fetchone()
        if hub_row is None:
            raise RuntimeError("tabela kabi.knowledge_hub jest pusta — uruchom najpierw import")
        hub = clean(hub_row)

        cur.execute("""
            SELECT * FROM kabi.categories
            WHERE published
            ORDER BY sort_order, id
        """)
        categories = [clean(r) for r in cur.fetchall()]

        # category_id → slug kategorii, bo generator operuje na slugach
        cur.execute("""
            SELECT a.*, c.slug AS category
            FROM kabi.articles a
            LEFT JOIN kabi.categories c ON c.id = a.category_id
            WHERE a.published
            ORDER BY a.sort_order, a.id
        """)
        articles = [clean(r, rename={"read_time": "read"}) for r in cur.fetchall()]

        cur.execute("""
            SELECT * FROM kabi.case_studies
            WHERE published
            ORDER BY sort_order, id
        """)
        case_studies = [clean(r) for r in cur.fetchall()]

        cur.execute("""
            SELECT * FROM kabi.referencje
            WHERE published
            ORDER BY sort_order, id
        """)
        referencje = [clean(r) for r in cur.fetchall()]

    data = {
        "wersja": 1,
        "zrodlo": "export_snapshot.py — wygenerowane z bazy kabi",
        "hub": hub,
        "categories": categories,
        "articles": articles,
        "case_studies": case_studies,
        "referencje": referencje,
    }

    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    with SNAPSHOT.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")

    print("zapisano %s" % SNAPSHOT)
    print("  kategorie:    %d" % len(categories))
    print("  artykuly:     %d" % len(articles))
    print("  case studies: %d" % len(case_studies))


if __name__ == "__main__":
    main()
