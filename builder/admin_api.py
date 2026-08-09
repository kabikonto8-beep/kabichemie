# -*- coding: utf-8 -*-
"""Lokalne API panelu redakcyjnego — most między przeglądarką a PostgreSQL.

Przeglądarka nie rozmawia z Postgresem bezpośrednio, więc panel wbudowany
w stronę potrzebuje pośrednika. To jest ten pośrednik: mały serwer HTTP
oparty wyłącznie o bibliotekę standardową + psycopg.

NARZĘDZIE WYŁĄCZNIE DEWELOPERSKIE. Nie ma uwierzytelniania — kto dosięgnie
portu, ten zapisuje do bazy. Ma stać za nginxem w sieci Dockera i nigdy
nie być wystawiony publicznie. Panel po stronie przeglądarki dodatkowo
odmawia działania poza localhost, ale to wygoda, nie zabezpieczenie.

Endpointy (wszystkie pod /api/, proxowane przez nginx z tego samego origin,
żeby nie łamać CSP `connect-src 'self'`):

    GET    /api/schema             — definicje pól z information_schema
    GET    /api/categories         — lista kategorii do wyboru
    GET    /api/articles           — lista artykułów (bez pola prose)
    GET    /api/articles/<slug>    — pełny artykuł
    POST   /api/articles           — nowy artykuł
    PUT    /api/articles/<slug>    — zapis zmian
    DELETE /api/articles/<slug>    — usunięcie
    POST   /api/publish            — eksport snapshotu + przebudowa www/
"""
import json
import os
import re
import subprocess
import sys
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

PORT = int(os.environ.get("ADMIN_API_PORT", "8125"))
DATABASE_URL = os.environ["DATABASE_URL"]

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Kolumny, które panel może zapisywać. Reszta (id, znaczniki czasu) jest
# pilnowana przez bazę i celowo poza zasięgiem panelu.
EDITABLE = [
    "slug", "category_id", "title", "list_title", "short", "topic",
    "excerpt", "lead", "audience", "read_time", "image", "prose",
    "feature_stats", "faq", "related", "published", "sort_order",
]
JSON_COLUMNS = {"feature_stats", "faq", "related"}
REQUIRED = ["slug", "title", "list_title", "short", "topic",
            "lead", "audience", "read_time", "prose"]


class Blad(Exception):
    """Błąd z kodem HTTP — zwracany do panelu jako czytelny komunikat."""

    def __init__(self, kod, komunikat):
        super().__init__(komunikat)
        self.kod = kod
        self.komunikat = komunikat


def polacz():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def sprawdz(dane, nowy):
    braki = [k for k in REQUIRED if not str(dane.get(k) or "").strip()] if nowy else []
    if braki:
        raise Blad(400, "Brakuje wymaganych pól: %s" % ", ".join(braki))

    slug = dane.get("slug")
    if slug is not None and not SLUG_RE.match(slug):
        raise Blad(400, "Slug %r jest niepoprawny — dozwolone są tylko małe "
                        "litery, cyfry i pojedyncze myślniki." % slug)

    for kolumna in JSON_COLUMNS:
        wartosc = dane.get(kolumna)
        if wartosc is not None and not isinstance(wartosc, list):
            raise Blad(400, "Pole %s musi być listą." % kolumna)


def wartosci(dane, kolumny):
    out = []
    for kolumna in kolumny:
        wartosc = dane.get(kolumna)
        if kolumna in JSON_COLUMNS and wartosc is not None:
            wartosc = Jsonb(wartosc)
        out.append(wartosc)
    return out


# --------------------------------------------------------------- operacje
def schema():
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'kabi' AND table_name = 'articles'
            ORDER BY ordinal_position
        """)
        kolumny = cur.fetchall()
    return {
        "kolumny": [k for k in kolumny if k["column_name"] in EDITABLE],
        "wymagane": REQUIRED,
        "json": sorted(JSON_COLUMNS),
        "slug_wzorzec": SLUG_RE.pattern,
    }


def categories():
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.slug, c.title,
                   (SELECT count(*) FROM kabi.articles a WHERE a.category_id = c.id) AS artykulow
            FROM kabi.categories c
            WHERE c.published
            ORDER BY c.sort_order, c.id
        """)
        return cur.fetchall()


def articles():
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT a.id, a.slug, a.title, a.topic, a.read_time, a.published,
                   a.sort_order, a.updated_at, c.slug AS category
            FROM kabi.articles a
            LEFT JOIN kabi.categories c ON c.id = a.category_id
            ORDER BY a.sort_order, a.id
        """)
        return cur.fetchall()


def article(slug):
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM kabi.articles WHERE slug = %s", (slug,))
        wiersz = cur.fetchone()
    if wiersz is None:
        raise Blad(404, "Nie ma artykułu o slugu %r." % slug)
    return wiersz


def create(dane):
    sprawdz(dane, nowy=True)
    kolumny = [k for k in EDITABLE if k in dane]
    with polacz() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO kabi.articles (%s) VALUES (%s) RETURNING slug"
            % (", ".join(kolumny), ", ".join(["%s"] * len(kolumny))),
            wartosci(dane, kolumny),
        )
        wynik = cur.fetchone()
        conn.commit()
    return {"slug": wynik["slug"], "komunikat": "Artykuł dodany."}


def update(slug, dane):
    sprawdz(dane, nowy=False)
    kolumny = [k for k in EDITABLE if k in dane]
    if not kolumny:
        raise Blad(400, "Nie przesłano żadnego pola do zapisania.")
    with polacz() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE kabi.articles SET %s WHERE slug = %%s RETURNING slug"
            % ", ".join("%s = %%s" % k for k in kolumny),
            wartosci(dane, kolumny) + [slug],
        )
        wynik = cur.fetchone()
        if wynik is None:
            raise Blad(404, "Nie ma artykułu o slugu %r." % slug)
        conn.commit()
    return {"slug": wynik["slug"], "komunikat": "Zapisano."}


def delete(slug):
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM kabi.articles WHERE slug = %s RETURNING slug", (slug,))
        if cur.fetchone() is None:
            raise Blad(404, "Nie ma artykułu o slugu %r." % slug)
        conn.commit()
    return {"komunikat": "Artykuł usunięty."}


def publish():
    """Eksport treści z bazy + przebudowa www/ (bez mirrorów językowych)."""
    wynik = subprocess.run(
        [sys.executable, "/builder/build_all.py"],
        cwd="/site", capture_output=True, text=True,
    )
    return {
        "ok": wynik.returncode == 0,
        "kod": wynik.returncode,
        "wyjscie": (wynik.stdout or "") + (wynik.stderr or ""),
    }


# ------------------------------------------------------------------ HTTP
class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format, *args):
        sys.stderr.write("[admin-api] %s\n" % (format % args))

    def _odpowiedz(self, kod, dane):
        tresc = json.dumps(dane, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(kod)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(tresc)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(tresc)

    def _cialo(self):
        dlugosc = int(self.headers.get("Content-Length") or 0)
        if not dlugosc:
            return {}
        try:
            return json.loads(self.rfile.read(dlugosc).decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise Blad(400, "Nieczytelny JSON w żądaniu: %s" % exc)

    def _sciezka(self):
        return self.path.split("?")[0].rstrip("/") or "/"

    def _obsluz(self, metoda):
        sciezka = self._sciezka()
        try:
            if sciezka == "/api/schema" and metoda == "GET":
                return self._odpowiedz(200, schema())
            if sciezka == "/api/categories" and metoda == "GET":
                return self._odpowiedz(200, categories())
            if sciezka == "/api/articles" and metoda == "GET":
                return self._odpowiedz(200, articles())
            if sciezka == "/api/articles" and metoda == "POST":
                return self._odpowiedz(201, create(self._cialo()))
            if sciezka == "/api/publish" and metoda == "POST":
                return self._odpowiedz(200, publish())

            if sciezka.startswith("/api/articles/"):
                slug = sciezka[len("/api/articles/"):]
                if metoda == "GET":
                    return self._odpowiedz(200, article(slug))
                if metoda == "PUT":
                    return self._odpowiedz(200, update(slug, self._cialo()))
                if metoda == "DELETE":
                    return self._odpowiedz(200, delete(slug))

            raise Blad(404, "Nieznany endpoint: %s %s" % (metoda, sciezka))
        except Blad as exc:
            self._odpowiedz(exc.kod, {"blad": exc.komunikat})
        except psycopg.errors.UniqueViolation:
            self._odpowiedz(409, {"blad": "Artykuł o takim slugu już istnieje."})
        except psycopg.errors.CheckViolation as exc:
            self._odpowiedz(400, {"blad": "Baza odrzuciła dane: %s" % exc})
        except Exception:
            traceback.print_exc()
            self._odpowiedz(500, {"blad": "Błąd serwera — szczegóły w logach kontenera."})

    def do_GET(self):
        self._obsluz("GET")

    def do_POST(self):
        self._obsluz("POST")

    def do_PUT(self):
        self._obsluz("PUT")

    def do_DELETE(self):
        self._obsluz("DELETE")


if __name__ == "__main__":
    print("[admin-api] nasłuch na porcie %d" % PORT, flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
