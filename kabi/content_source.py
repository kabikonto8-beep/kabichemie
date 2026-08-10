# -*- coding: utf-8 -*-
"""Źródło treści dla generatora: content/snapshot.json.

Snapshot jest plikiem wersjonowanym w gicie i wygenerowanym z Postgresa
(builder/export_snapshot.py). Dzięki temu `build.py` nie potrzebuje dostępu
do bazy — buduje się tak samo lokalnie, jak i w CI.

Obieg treści:
    pgAdmin → Postgres → export_snapshot.py → content/snapshot.json → build.py → www/
"""
import json
from pathlib import Path

from content_schema import from_snapshot

ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT / "content" / "snapshot.json"

_cache = None


def _load():
    global _cache
    if _cache is None:
        if not SNAPSHOT.exists():
            raise FileNotFoundError(
                "Brak %s — wygeneruj go z bazy:\n"
                "    docker compose run --rm builder python /builder/export_snapshot.py"
                % SNAPSHOT
            )
        with SNAPSHOT.open(encoding="utf-8") as fh:
            _cache = json.load(fh)
    return _cache


def hub():
    return from_snapshot(_load()["hub"])


def categories():
    return [from_snapshot(r) for r in _load()["categories"]]


def articles():
    return [from_snapshot(r) for r in _load()["articles"]]


def case_studies():
    return [from_snapshot(r) for r in _load()["case_studies"]]


def referencje():
    """Referencje na /referencje/. Brak klucza = starszy snapshot, sprzed
    wprowadzenia tej sekcji — traktujemy jak pustą listę."""
    return [from_snapshot(r) for r in _load().get("referencje", [])]
