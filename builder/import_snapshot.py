# -*- coding: utf-8 -*-
"""content/snapshot.json → PostgreSQL.

Ładuje treść do bazy, żeby dało się ją edytować w pgAdmin. Operacja jest
idempotentna: czyści tabele i wstawia zawartość snapshotu od nowa,
zachowując kolejność wpisów w kolumnie sort_order.

Uruchomienie:
    docker compose run --rm builder python /builder/import_snapshot.py
"""
import json
import os
import sys
from pathlib import Path

import psycopg
from psycopg.types.json import Jsonb

sys.path.insert(0, "/site")

SNAPSHOT = Path("/site/content/snapshot.json")

# Kolumny JSONB — wymagają owinięcia w Jsonb() przy zapisie.
JSON_COLUMNS = {
    "facts", "feature_stats", "faq", "related", "overview", "issues",
    "process", "field_notes", "actions", "signals", "metrics",
}

CATEGORY_COLUMNS = [
    "slug", "title", "h1", "kicker", "lead", "hub_blurb",
    "stream_title", "image", "facts", "related",
]
ARTICLE_COLUMNS = [
    "slug", "category_id", "title", "list_title", "short", "topic",
    "excerpt", "lead", "audience", "read_time", "image", "prose",
    "feature_stats", "faq", "related",
]
CASE_COLUMNS = [
    "slug", "path", "kicker", "h1", "lead", "image", "image_position",
    "signals", "result_kicker", "result_value", "result_label", "result_note",
    "overview", "challenge_title", "challenge_intro", "issues",
    "process_title", "process_intro", "process",
    "results_title", "results_intro", "results_note", "metrics",
    "field_title", "field_intro", "field_notes",
    "faq_title", "faq_intro", "faq",
    "cta_title", "cta_text", "actions", "related",
]


def wrap(column, value):
    if value is None:
        return None
    return Jsonb(value) if column in JSON_COLUMNS else value


def insert(cur, table, columns, row, sort_order):
    values = [wrap(c, row.get(c)) for c in columns] + [sort_order]
    placeholders = ", ".join(["%s"] * (len(columns) + 1))
    cur.execute(
        "INSERT INTO kabi.%s (%s, sort_order) VALUES (%s)"
        % (table, ", ".join(columns), placeholders),
        values,
    )


def main():
    with SNAPSHOT.open(encoding="utf-8") as fh:
        data = json.load(fh)

    url = os.environ["DATABASE_URL"]
    with psycopg.connect(url) as conn, conn.cursor() as cur:
        # Kolejność ma znaczenie — articles wskazuje na categories.
        cur.execute("TRUNCATE kabi.articles, kabi.case_studies, kabi.categories, "
                    "kabi.knowledge_hub RESTART IDENTITY CASCADE")

        hub = data["hub"]
        cur.execute(
            "INSERT INTO kabi.knowledge_hub (id, kicker, h1, lead, image, facts) "
            "VALUES (1, %s, %s, %s, %s, %s)",
            (hub["kicker"], hub["h1"], hub["lead"], hub["image"], Jsonb(hub["facts"])),
        )

        category_ids = {}
        for order, row in enumerate(data["categories"]):
            insert(cur, "categories", CATEGORY_COLUMNS, row, order)
            cur.execute("SELECT id FROM kabi.categories WHERE slug = %s", (row["slug"],))
            category_ids[row["slug"]] = cur.fetchone()[0]

        for order, row in enumerate(data["articles"]):
            prepared = dict(row)
            prepared["read_time"] = prepared.pop("read")
            slug = prepared.pop("category", None)
            if slug is not None and slug not in category_ids:
                raise ValueError(
                    "artykul %r wskazuje na nieistniejaca kategorie %r"
                    % (prepared["slug"], slug)
                )
            prepared["category_id"] = category_ids.get(slug)
            insert(cur, "articles", ARTICLE_COLUMNS, prepared, order)

        for order, row in enumerate(data["case_studies"]):
            insert(cur, "case_studies", CASE_COLUMNS, row, order)

        conn.commit()

        for table in ("categories", "articles", "case_studies"):
            cur.execute("SELECT count(*) FROM kabi.%s" % table)
            print("  %-13s %d" % (table + ":", cur.fetchone()[0]))

    print("zaladowano do bazy z %s" % SNAPSHOT)


if __name__ == "__main__":
    main()
