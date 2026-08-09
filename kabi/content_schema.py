# -*- coding: utf-8 -*-
"""Wspólna specyfikacja kształtu treści — używana przez seed, import, eksport i generator.

Generator (knowledge_pages.py, company_case_pages.py) operuje na listach krotek,
np. ``faq = [("pytanie", "odpowiedź"), …]``. W bazie i w snapshocie trzymamy to
jako tablice obiektów z nazwanymi kluczami, bo krotki pozycyjne są nieczytelne
w pgAdmin. Ten moduł jest jedynym miejscem, które zna to przełożenie.
"""

# Pole → nazwy kluczy w kolejności pozycyjnej krotki.
TUPLE_KEYS = {
    "facts":         ("label", "value"),
    "feature_stats": ("value", "label"),
    "faq":           ("q", "a"),
    "related":       ("kicker", "title", "url"),
    "overview":      ("label", "text"),
    "issues":        ("title", "text", "tag"),
    "process":       ("title", "text"),
    "field_notes":   ("title", "text"),
    "actions":       ("classes", "label", "url"),
}

# Pola, które NIE są krotkami i przechodzą bez zmiany kształtu:
#   signals — lista zwykłych napisów
#   metrics — lista słowników o dwóch wariantach kluczy
PASSTHROUGH = ("signals", "metrics")

# Nazwa pola w generatorze → nazwa kolumny w bazie (gdy się różnią).
COLUMN_ALIASES = {
    "read": "read_time",
}
COLUMN_ALIASES_REVERSED = {v: k for k, v in COLUMN_ALIASES.items()}


def tuples_to_objects(field, value):
    """[("a", "b"), …] → [{"klucz1": "a", "klucz2": "b"}, …]"""
    if value is None:
        return None
    keys = TUPLE_KEYS[field]
    out = []
    for item in value:
        if len(item) != len(keys):
            raise ValueError(
                "pole %r: krotka ma %d elementów, oczekiwano %d (%s) — %r"
                % (field, len(item), len(keys), ", ".join(keys), item)
            )
        out.append(dict(zip(keys, item)))
    return out


def objects_to_tuples(field, value):
    """[{"klucz1": "a", "klucz2": "b"}, …] → [("a", "b"), …]"""
    if value is None:
        return None
    keys = TUPLE_KEYS[field]
    out = []
    for item in value:
        missing = [k for k in keys if k not in item]
        if missing:
            raise ValueError(
                "pole %r: w obiekcie brakuje kluczy %s — %r"
                % (field, ", ".join(missing), item)
            )
        out.append(tuple(item[k] for k in keys))
    return out


def to_snapshot(row):
    """Słownik generatora → postać zapisywana w snapshocie/bazie.

    Klucze nieobecne w wejściu pozostają nieobecne — to warunek tego,
    żeby round-trip odtwarzał oryginał, a nie jego „znormalizowaną" wersję.
    """
    out = {}
    for key, value in row.items():
        if key in TUPLE_KEYS:
            out[key] = tuples_to_objects(key, value)
        else:
            out[key] = value
    return out


def from_snapshot(row):
    """Postać ze snapshotu/bazy → słownik oczekiwany przez generator."""
    out = {}
    for key, value in row.items():
        if key in TUPLE_KEYS:
            out[key] = objects_to_tuples(key, value)
        else:
            out[key] = value
    return out
