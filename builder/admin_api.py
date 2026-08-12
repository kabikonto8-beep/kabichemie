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
import shutil
import subprocess
import sys
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

PORT = int(os.environ.get("ADMIN_API_PORT", "8125"))
DATABASE_URL = os.environ["DATABASE_URL"]

# Python kładzie na sys.path katalog SKRYPTU (/builder), nie katalog roboczy.
# Bez tego podgląd nie zaimportuje knowledge_pages ani content_schema.
if "/site" not in sys.path:
    sys.path.insert(0, "/site")

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Kolumny, które panel może zapisywać. Reszta (id, znaczniki czasu) jest
# pilnowana przez bazę i celowo poza zasięgiem panelu.
EDITABLE = [
    "slug", "category_id", "title", "list_title", "short", "topic",
    "excerpt", "lead", "audience", "read_time", "image", "prose", "html",
    "feature_stats", "faq", "related", "published", "sort_order",
]
JSON_COLUMNS = {"feature_stats", "faq", "related"}
# Pola wymagane przy układzie składanym z pól. Artykuł z własnym HTML-em
# (kolumna `html`) potrzebuje tylko tego, czym żyje lista bazy wiedzy
# i adres strony — `prose` jest wtedy nieużywany.
REQUIRED = ["slug", "title", "list_title", "short", "topic",
            "lead", "audience", "read_time", "prose"]
REQUIRED_HTML = ["slug", "title", "list_title", "short", "topic",
                 "lead", "audience", "read_time"]

# --------------------------------------------------------- case studies
# Druga domena treści — działa DOKŁADNIE jak artykuły (te same pola, ten sam
# edytor prose + własny HTML), tyle że publikuje pod /case-study/{slug}/.
# Adres strony (kolumna `path`) wyliczamy ze sluga, nie każemy go wpisywać.
# Istniejące 3 wpisy (fako/bac/evapco) nie mają `prose`/`title` — renderują się
# dawnym, bogatym układem („niestandardowe"), patrz company_case_pages.
EDITABLE_CASE = [
    "slug", "path", "title", "list_title", "short", "topic",
    "excerpt", "lead", "audience", "read_time", "image", "prose", "html",
    "feature_stats", "faq", "related", "published", "sort_order",
]
JSON_COLUMNS_CASE = {"feature_stats", "faq", "related"}
REQUIRED_CASE = ["slug", "title", "list_title", "short", "topic",
                 "lead", "audience", "read_time", "prose"]
REQUIRED_CASE_HTML = ["slug", "title", "list_title", "short", "topic",
                      "lead", "audience", "read_time"]


def sciezka_case(slug):
    """Adres case study wyliczony ze sluga — jak /baza-wiedzy/ dla artykułów."""
    return "/case-study/%s/" % slug


import logowanie

CIASTECZKO = "kabi_panel"
# Endpointy dostępne bez zalogowania. Wszystko poza tą listą wymaga sesji.
BEZ_LOGOWANIA = {("POST", "/api/logowanie"), ("GET", "/api/sesja")}


def kto_zalogowany(naglowki):
    """Login z ważnej sesji albo None."""
    surowe = naglowki.get("Cookie") or ""
    token = None
    for kawalek in surowe.split(";"):
        nazwa, _, wartosc = kawalek.strip().partition("=")
        if nazwa == CIASTECZKO:
            token = wartosc
            break
    dane = logowanie.sesja(token)
    return dane["login"] if dane else None


def zaloguj(dane):
    dane = dane or {}
    login = str(dane.get("login") or "").strip()
    haslo = str(dane.get("haslo") or "")

    czekaj = logowanie.czy_zablokowany(login)
    if czekaj:
        raise Blad(429, "Za dużo nieudanych prób. Spróbuj za %d s." % czekaj)

    with polacz() as conn, conn.cursor() as cur:
        cur.execute("SELECT login, hash FROM kabi.panel_uzytkownicy WHERE login = %s",
                    (login,))
        konto = cur.fetchone()

    # Hasło sprawdzamy nawet dla nieistniejącego loginu — inaczej różnica
    # w czasie odpowiedzi zdradzałaby, które loginy istnieją.
    zapis = konto["hash"] if konto else logowanie.zahashuj("x" * 12)
    poprawne = logowanie.sprawdz_haslo(haslo, zapis) and konto is not None

    if not poprawne:
        logowanie.zapisz_nieudana(login)
        raise Blad(401, "Nieprawidłowy login lub hasło.")

    logowanie.wyczysc_nieudane(login)
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("UPDATE kabi.panel_uzytkownicy SET ostatnie_logowanie = now() "
                    "WHERE login = %s", (login,))
        conn.commit()

    return logowanie.zaloz_sesje(login), {"login": login, "komunikat": "Zalogowano."}


class Blad(Exception):
    """Błąd z kodem HTTP — zwracany do panelu jako czytelny komunikat."""

    def __init__(self, kod, komunikat):
        super().__init__(komunikat)
        self.kod = kod
        self.komunikat = komunikat


def polacz():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def sprawdz(dane, nowy):
    wymagane = REQUIRED_HTML if str(dane.get("html") or "").strip() else REQUIRED
    braki = [k for k in wymagane if not str(dane.get(k) or "").strip()] if nowy else []
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


def sprawdz_case(dane, nowy):
    wymagane = REQUIRED_CASE_HTML if str(dane.get("html") or "").strip() \
        else REQUIRED_CASE
    braki = [k for k in wymagane if not str(dane.get(k) or "").strip()] \
        if nowy else []
    if braki:
        raise Blad(400, "Brakuje wymaganych pól: %s" % ", ".join(braki))

    slug = dane.get("slug")
    if slug is not None and not SLUG_RE.match(slug):
        raise Blad(400, "Slug %r jest niepoprawny — dozwolone są tylko małe "
                        "litery, cyfry i pojedyncze myślniki." % slug)

    for kolumna in JSON_COLUMNS_CASE:
        wartosc = dane.get(kolumna)
        if wartosc is not None and not isinstance(wartosc, list):
            raise Blad(400, "Pole %s musi być listą." % kolumna)


def wartosci_case(dane, kolumny):
    out = []
    for kolumna in kolumny:
        wartosc = dane.get(kolumna)
        if kolumna in JSON_COLUMNS_CASE and wartosc is not None:
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


WWW = "/site/www"
MIRRORY = ("en", "de", "ar")


def adresy():
    """Adresy stron serwisu — do wyboru w polu „powiązane odnośniki”.

    Czytamy z wygenerowanego www/, a nie z bazy, bo powiązania mogą wskazywać
    na dowolną stronę serwisu, nie tylko na artykuł. Pomijamy mirrory językowe
    (odnośnik ma prowadzić do wersji polskiej) oraz strony przekierowań,
    bo linkowanie do nich jest błędem.
    """
    wynik = []
    for katalog, _, pliki in os.walk(WWW):
        if "index.html" not in pliki:
            continue
        wzgledny = os.path.relpath(katalog, WWW).replace(os.sep, "/")
        if wzgledny == ".":
            adres = "/"
        else:
            if wzgledny.split("/")[0] in MIRRORY or wzgledny.split("/")[0] == "404":
                continue
            adres = "/" + wzgledny + "/"

        with open(os.path.join(katalog, "index.html"), encoding="utf-8") as fh:
            poczatek = fh.read(6000)
        if 'http-equiv="refresh"' in poczatek:
            continue

        dopasowanie = re.search(r"<title>(.*?)</title>", poczatek, re.S)
        etykieta = dopasowanie.group(1).strip() if dopasowanie else adres
        # Tytuły niosą ogon w stylu „ | kondycjonowanie-wody.pl” — do listy
        # rozwijanej liczy się sama nazwa strony.
        etykieta = re.split(r"\s+[|–-]\s+", etykieta)[0][:70]
        wynik.append({"url": adres, "etykieta": etykieta})
    return sorted(wynik, key=lambda p: p["url"])


GRAFIKI_ROZSZERZENIA = (".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif")
GRAFIKI_POMIJANE = ("favicon", "logo", "sygnet", "og-default")


def grafiki():
    """Grafiki, które redaktor może wstawić w treść artykułu.

    Czytamy z src/assets, a nie z www/assets — to jest źródło, które build
    kopiuje. Pomijamy logotypy i ikony interfejsu: w treści artykułu nie mają
    zastosowania, a zaśmiecałyby wybór.
    """
    korzen = "/site/src/assets"
    wynik = []
    for katalog, _, pliki in os.walk(korzen):
        for nazwa in pliki:
            if not nazwa.lower().endswith(GRAFIKI_ROZSZERZENIA):
                continue
            pelna = os.path.join(katalog, nazwa)
            wzgledna = os.path.relpath(pelna, korzen).replace(os.sep, "/")
            # Grafiki wgrane przez redaktora (uploads/) pokazujemy zawsze —
            # filtr nazw ukrywa tylko logotypy i ikony motywu, które i tak
            # mogą przypadkiem zawierać słowo „logo" w nazwie pliku.
            if not wzgledna.startswith("uploads/") \
                    and any(pomin in nazwa.lower() for pomin in GRAFIKI_POMIJANE):
                continue
            wynik.append({
                "url": "/assets/" + wzgledna,
                "nazwa": os.path.splitext(nazwa)[0].replace("-", " ").replace("_", " "),
                "grupa": wzgledna.split("/")[0] if "/" in wzgledna else "inne",
                "rozmiar_kb": round(os.path.getsize(pelna) / 1024),
            })
    return sorted(wynik, key=lambda g: (g["grupa"], g["url"]))


GRAFIKI_KATALOG = "/site/src/assets/uploads"
GRAFIKI_KATALOG_WWW = "/site/www/assets/uploads"
GRAFIKA_LIMIT_MB = 20
GRAFIKA_SYGNATURY = (
    (b"\xff\xd8\xff", ".jpg"),
    (b"\x89PNG\r\n\x1a\n", ".png"),
    (b"GIF87a", ".gif"),
    (b"GIF89a", ".gif"),
)


def grafiki_wgraj(dane):
    """Zapisuje grafikę wgraną z edytora treści do src/assets/uploads.

    Plik przychodzi jako base64 w JSON — jak referencje_wgraj, patrz tamtejsze
    uzasadnienie. Rodzaj pliku poznajemy po sygnaturze bajtów, nie po nazwie:
    nazwa przyjeżdża z przeglądarki i bywa dowolna. Kopiujemy grafikę także
    do www/assets/uploads, żeby podgląd i strona widziały ją od razu — build
    i tak odtworzy www/ z src/ przy najbliższej przebudowie.
    """
    import base64

    dane = dane or {}
    nazwa = str(dane.get("nazwa") or "").strip()
    zawartosc = dane.get("dane") or ""

    if "," in zawartosc and zawartosc.lstrip().startswith("data:"):
        zawartosc = zawartosc.split(",", 1)[1]
    try:
        bajty = base64.b64decode(zawartosc, validate=True)
    except Exception:
        raise Blad(400, "Nie potrafię odczytać przesłanego pliku.")

    rozszerzenie = None
    for sygnatura, roz in GRAFIKA_SYGNATURY:
        if bajty.startswith(sygnatura):
            rozszerzenie = roz
            break
    if rozszerzenie is None and len(bajty) > 12 \
            and bajty[:4] == b"RIFF" and bajty[8:12] == b"WEBP":
        rozszerzenie = ".webp"
    if rozszerzenie is None:
        raise Blad(400, "Przyjmuję tylko obrazy JPG, PNG, WEBP i GIF.")
    if len(bajty) > GRAFIKA_LIMIT_MB * 1024 * 1024:
        raise Blad(400, "Plik ma %.1f MB, limit to %d MB."
                        % (len(bajty) / 1048576, GRAFIKA_LIMIT_MB))

    baza = os.path.splitext(nazwa)[0] if nazwa else "grafika"
    bezpieczna = re.sub(r"[^a-z0-9]+", "-", baza.lower()).strip("-") or "grafika"
    os.makedirs(GRAFIKI_KATALOG, exist_ok=True)

    ostateczna, licznik = bezpieczna + rozszerzenie, 2
    while os.path.exists(os.path.join(GRAFIKI_KATALOG, ostateczna)):
        ostateczna = "%s-%d%s" % (bezpieczna, licznik, rozszerzenie)
        licznik += 1

    sciezka = os.path.join(GRAFIKI_KATALOG, ostateczna)
    with open(sciezka, "wb") as fh:
        fh.write(bajty)

    try:
        os.makedirs(GRAFIKI_KATALOG_WWW, exist_ok=True)
        shutil.copy2(sciezka, os.path.join(GRAFIKI_KATALOG_WWW, ostateczna))
    except OSError:
        pass  # brak www/ nie przerywa wgrywania — plik pojawi się po buildzie

    return {"url": "/assets/uploads/" + ostateczna,
            "nazwa": os.path.splitext(ostateczna)[0].replace("-", " "),
            "rozmiar_kb": round(len(bajty) / 1024),
            "komunikat": "Wgrano %s." % ostateczna}


REFERENCJE_KOLUMNY = ["tytul", "firma", "opis", "plik", "miniatura",
                      "published", "sort_order"]
REFERENCJE_KATALOG = "/site/src/assets/referencje"
PDF_LIMIT_MB = 15


def referencje_lista():
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, tytul, firma, opis, plik, published, sort_order, updated_at
            FROM kabi.referencje
            ORDER BY sort_order, id
        """)
        return cur.fetchall()


def referencje_zapisz(dane):
    dane = dane or {}
    if not str(dane.get("tytul") or "").strip():
        raise Blad(400, "Podaj tytuł referencji.")

    kolumny = [k for k in REFERENCJE_KOLUMNY if k in dane]
    with polacz() as conn, conn.cursor() as cur:
        if dane.get("id"):
            cur.execute(
                "UPDATE kabi.referencje SET %s WHERE id = %%s RETURNING id"
                % ", ".join("%s = %%s" % k for k in kolumny),
                [dane[k] for k in kolumny] + [dane["id"]],
            )
            if cur.fetchone() is None:
                raise Blad(404, "Nie ma referencji o tym numerze.")
            komunikat = "Zapisano."
        else:
            cur.execute(
                "INSERT INTO kabi.referencje (%s) VALUES (%s) RETURNING id"
                % (", ".join(kolumny), ", ".join(["%s"] * len(kolumny))),
                [dane[k] for k in kolumny],
            )
            dane["id"] = cur.fetchone()["id"]
            komunikat = "Referencja dodana."
        conn.commit()
    return {"id": dane["id"], "komunikat": komunikat}


def referencje_usun(numer):
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM kabi.referencje WHERE id = %s RETURNING id", (numer,))
        if cur.fetchone() is None:
            raise Blad(404, "Nie ma referencji o tym numerze.")
        conn.commit()
    return {"komunikat": "Referencja usunięta."}


def referencje_wgraj(dane):
    """Zapisuje wgrany PDF do src/assets/referencje i zwraca jego adres.

    Plik przychodzi jako base64 w JSON, a nie jako multipart. Serwer stoi
    na bibliotece standardowej, a parsowanie multiparta bez zewnętrznych
    bibliotek to więcej kodu i więcej miejsc na błąd niż zysku.
    """
    import base64
    import re as _re

    dane = dane or {}
    nazwa = str(dane.get("nazwa") or "").strip()
    zawartosc = dane.get("dane") or ""
    if not nazwa.lower().endswith(".pdf"):
        raise Blad(400, "Przyjmuję wyłącznie pliki PDF.")

    if "," in zawartosc and zawartosc.lstrip().startswith("data:"):
        zawartosc = zawartosc.split(",", 1)[1]
    try:
        bajty = base64.b64decode(zawartosc, validate=True)
    except Exception:
        raise Blad(400, "Nie potrafię odczytać przesłanego pliku.")

    if not bajty.startswith(b"%PDF"):
        raise Blad(400, "To nie jest plik PDF — brakuje nagłówka dokumentu.")
    if len(bajty) > PDF_LIMIT_MB * 1024 * 1024:
        raise Blad(400, "Plik ma %.1f MB, limit to %d MB."
                        % (len(bajty) / 1048576, PDF_LIMIT_MB))

    bezpieczna = _re.sub(r"[^a-z0-9]+", "-", nazwa[:-4].lower()).strip("-") or "referencja"
    os.makedirs(REFERENCJE_KATALOG, exist_ok=True)

    ostateczna, licznik = bezpieczna + ".pdf", 2
    while os.path.exists(os.path.join(REFERENCJE_KATALOG, ostateczna)):
        ostateczna = "%s-%d.pdf" % (bezpieczna, licznik)
        licznik += 1

    sciezka = os.path.join(REFERENCJE_KATALOG, ostateczna)
    with open(sciezka, "wb") as fh:
        fh.write(bajty)

    miniatura, uwaga = zrob_miniature(sciezka)
    return {"plik": "/assets/referencje/" + ostateczna,
            "miniatura": miniatura,
            "rozmiar_kb": round(len(bajty) / 1024),
            "komunikat": "Wgrano %s.%s" % (ostateczna, (" " + uwaga) if uwaga else "")}


MINIATURA_SZEROKOSC = 720


def zrob_miniature(sciezka_pdf):
    """Renderuje pierwszą stronę PDF-a do PNG obok dokumentu.

    Osadzanie PDF-a w <iframe> oddawało wygląd wtyczce przeglądarki: własne
    paski przewijania i banner „Ten plik ma ograniczone uprawnienia” przy
    dokumentach z ustawionymi restrykcjami. Obrazek daje pełną kontrolę
    nad kadrem i wygląda tak samo wszędzie.

    Zwraca (adres_miniatury, uwaga). Niepowodzenie nie przerywa wgrywania —
    kafel pokaże wtedy sam dokument bez podglądu.
    """
    try:
        import pypdfium2
    except ImportError:
        return None, "Podgląd pominięty: brak biblioteki pypdfium2 w obrazie."

    docelowy = os.path.splitext(sciezka_pdf)[0] + ".png"
    try:
        dokument = pypdfium2.PdfDocument(sciezka_pdf)
        if len(dokument) == 0:
            return None, "Dokument nie ma ani jednej strony."
        strona = dokument[0]
        skala = MINIATURA_SZEROKOSC / strona.get_width()
        strona.render(scale=skala).to_pil().save(docelowy, optimize=True)
        dokument.close()
    except Exception as exc:
        traceback.print_exc()
        return None, "Nie udało się wygenerować podglądu (%s)." % type(exc).__name__

    return "/assets/referencje/" + os.path.basename(docelowy), None


def etykiety():
    """Etykiety (kickery) już używane w powiązanych odnośnikach."""
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT r->>'kicker' AS etykieta, count(*) AS ile
            FROM kabi.articles, jsonb_array_elements(related) r
            WHERE published AND r->>'kicker' <> ''
            GROUP BY 1
            ORDER BY 2 DESC, 1
        """)
        return [w["etykieta"] for w in cur.fetchall()]


def categories():
    with polacz() as conn, conn.cursor() as cur:
        # `dzial` to krótka nazwa pokazywana nad tytułem artykułu. Siedzi
        # w kickerze kategorii („Baza wiedzy · Kotły parowe"), więc bierzemy
        # ją stamtąd zamiast kazać redaktorowi wpisywać drugi raz to samo.
        cur.execute("""
            SELECT c.id, c.slug, c.title,
                   trim(split_part(c.kicker, '·', 2)) AS dzial,
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


# ------------------------------------------------------- CRUD case studies
def case_studies():
    """Lista do lewego panelu. Nazwę bierzemy z title (nowe), a dla starych
    wpisów z h1 — dzięki temu i nowe, i „niestandardowe" mają czym się pokazać."""
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, slug, path,
                   COALESCE(NULLIF(title, ''), h1) AS title,
                   topic, (prose IS NOT NULL OR html IS NOT NULL) AS standardowe,
                   published, sort_order, updated_at
            FROM kabi.case_studies
            ORDER BY sort_order, id
        """)
        return cur.fetchall()


def case_study(slug):
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM kabi.case_studies WHERE slug = %s", (slug,))
        wiersz = cur.fetchone()
    if wiersz is None:
        raise Blad(404, "Nie ma case study o slugu %r." % slug)
    return wiersz


def create_case(dane):
    sprawdz_case(dane, nowy=True)
    if dane.get("slug"):
        dane["path"] = sciezka_case(dane["slug"])   # adres ze sluga, jak w artykułach
    kolumny = [k for k in EDITABLE_CASE if k in dane]
    with polacz() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO kabi.case_studies (%s) VALUES (%s) RETURNING slug"
            % (", ".join(kolumny), ", ".join(["%s"] * len(kolumny))),
            wartosci_case(dane, kolumny),
        )
        wynik = cur.fetchone()
        conn.commit()
    return {"slug": wynik["slug"], "komunikat": "Case study dodane."}


def update_case(slug, dane):
    sprawdz_case(dane, nowy=False)
    if dane.get("slug"):
        dane["path"] = sciezka_case(dane["slug"])   # zmiana sluga = nowy adres
    kolumny = [k for k in EDITABLE_CASE if k in dane]
    if not kolumny:
        raise Blad(400, "Nie przesłano żadnego pola do zapisania.")
    with polacz() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE kabi.case_studies SET %s WHERE slug = %%s RETURNING slug"
            % ", ".join("%s = %%s" % k for k in kolumny),
            wartosci_case(dane, kolumny) + [slug],
        )
        wynik = cur.fetchone()
        if wynik is None:
            raise Blad(404, "Nie ma case study o slugu %r." % slug)
        conn.commit()
    return {"slug": wynik["slug"], "komunikat": "Zapisano."}


def delete_case(slug):
    with polacz() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM kabi.case_studies WHERE slug = %s RETURNING slug",
                    (slug,))
        if cur.fetchone() is None:
            raise Blad(404, "Nie ma case study o slugu %r." % slug)
        conn.commit()
    return {"komunikat": "Case study usunięte."}


# Podglądowi nie wolno animować wejścia: bez main.js elementy .reveal zostają
# z opacity:0 i strona wygląda na pustą. Wyłączamy też przewijanie kotwic.
PODGLAD_STYL = """
  .reveal, .reveal-left, .reveal-right { opacity: 1 !important; transform: none !important; }
  html { scroll-behavior: auto; }
  body { margin: 0; }
"""

PODGLAD_SZKIELET = """<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<base href="/">
<link rel="stylesheet" href="/assets/style.css?v=%(wersja)s">
<link rel="stylesheet" href="/assets/solution-pages.css?v=%(wersja)s">
<link rel="stylesheet" href="/assets/company-case-pages.css?v=%(wersja)s">
<style>%(styl)s</style>
</head>
<body class="%(klasy)s">
%(tresc)s
</body>
</html>"""


def wersja_stylow():
    """Znacznik zmiany arkuszy — inaczej podgląd pokazuje CSS z cache'u.

    nginx trzyma /assets/ przez godzinę, więc bez tego poprawka w style.css
    nie jest widoczna w podglądzie do czasu twardego odświeżenia.
    """
    najnowszy = 0
    for nazwa in ("style.css", "solution-pages.css", "company-case-pages.css"):
        sciezka = os.path.join("/site/www/assets", nazwa)
        if os.path.exists(sciezka):
            najnowszy = max(najnowszy, os.path.getmtime(sciezka))
    return int(najnowszy)

# Wartości zastępcze, żeby podgląd działał już przy w połowie wypełnionym
# formularzu — renderer sięga po te klucze bezwarunkowo.
PODGLAD_DOMYSLNE = {
    "title": "(tytuł artykułu)",
    "lead": "(lead — pierwszy akapit pod nagłówkiem)",
    "prose": "<p>(treść artykułu)</p>",
    "read": "— min",
    "audience": "(dla kogo)",
    "faq": [],
    "related": [],
}


def preview(dane):
    """Renderuje szkic tym samym kodem, którym buduje się stronę.

    Świadomie NIE odtwarzamy wyglądu w JavaScripcie — podgląd ma pokazywać
    to, co naprawdę wyjdzie z build.py, razem z produkcyjnym CSS-em.
    """
    import knowledge_pages
    from content_schema import from_snapshot

    szkic = dict(PODGLAD_DOMYSLNE)
    for klucz, wartosc in (dane or {}).items():
        if wartosc not in (None, ""):
            szkic[klucz] = wartosc
    # kolumna w bazie nazywa się read_time, renderer oczekuje "read"
    if "read_time" in szkic:
        szkic["read"] = szkic.pop("read_time") or PODGLAD_DOMYSLNE["read"]

    # Puste wiersze list z panelu odrzucamy, żeby konwersja nie wywaliła się
    # na brakujących kluczach.
    for pole, klucze in (("faq", ("q", "a")), ("related", ("kicker", "title", "url")),
                         ("feature_stats", ("value", "label"))):
        if isinstance(szkic.get(pole), list):
            szkic[pole] = [w for w in szkic[pole]
                           if isinstance(w, dict) and all(k in w for k in klucze)]

    try:
        artykul = from_snapshot(szkic)
        tresc = knowledge_pages.render_article(artykul)
    except Exception as exc:
        tresc = ('<div style="padding:40px;font:14px system-ui;color:#b00">'
                 '<strong>Nie mogę wyrenderować podglądu.</strong><br>%s</div>'
                 % html_escape(str(exc)))

    return {"html": PODGLAD_SZKIELET % {
        "wersja": wersja_stylow(),
        "styl": PODGLAD_STYL,
        "klasy": knowledge_pages.BODY_CLASS,
        "tresc": tresc,
    }}


# Case study renderuje się silnikiem artykułów — te same klucze co przy
# podglądzie artykułu (renderer sięga po nie bezwarunkowo).
PODGLAD_DOMYSLNE_CASE = {
    "title": "(tytuł case study)",
    "lead": "(lead — pierwszy akapit pod nagłówkiem)",
    "prose": "<p>(treść case study)</p>",
    "read": "— min",
    "audience": "(dla kogo)",
    "image": "/assets/case/case-fako-boiler-generated.png",
    "faq": [],
    "related": [],
}


def preview_case(dane):
    """Podgląd case study — tym samym silnikiem, co artykuły (render_case_standard)."""
    import company_case_pages
    from content_schema import from_snapshot

    szkic = dict(PODGLAD_DOMYSLNE_CASE)
    for klucz, wartosc in (dane or {}).items():
        if wartosc not in (None, ""):
            szkic[klucz] = wartosc
    if "read_time" in szkic:
        szkic["read"] = szkic.pop("read_time") or PODGLAD_DOMYSLNE_CASE["read"]

    # Puste wiersze list odrzucamy, żeby konwersja nie wywaliła się na brakach.
    for pole, klucze in (("faq", ("q", "a")),
                         ("related", ("kicker", "title", "url")),
                         ("feature_stats", ("value", "label"))):
        if isinstance(szkic.get(pole), list):
            szkic[pole] = [w for w in szkic[pole]
                           if isinstance(w, dict) and all(k in w for k in klucze)]

    try:
        rekord = from_snapshot(szkic)
        tresc = company_case_pages.render_case_standard(rekord)
    except Exception as exc:
        tresc = ('<div style="padding:40px;font:14px system-ui;color:#b00">'
                 '<strong>Nie mogę wyrenderować podglądu.</strong><br>%s</div>'
                 % html_escape(str(exc)))

    return {"html": PODGLAD_SZKIELET % {
        "wersja": wersja_stylow(),
        "styl": PODGLAD_STYL,
        "klasy": company_case_pages.CASE_BODY_CLASS,
        "tresc": tresc,
    }}


def html_escape(tekst):
    return (tekst.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


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

    def _odpowiedz(self, kod, dane, ciasteczko=None):
        tresc = json.dumps(dane, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(kod)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(tresc)))
        self.send_header("Cache-Control", "no-store")
        if ciasteczko is not None:
            # HttpOnly — token jest niedostępny dla JavaScriptu, więc nie da się
            # go wykraść skryptem wstrzykniętym w stronę.
            # SameSite=Strict — przeglądarka nie dołączy go do żądań z obcych
            # witryn, co odcina ataki typu CSRF.
            # Secure — TYLKO na hostowanym panelu za HTTPS (PANEL_SECURE_COOKIE=1).
            # Lokalnie po http://localhost przeglądarka odrzuciłaby ciasteczko
            # z flagą Secure i logowanie by nie działało, więc domyślnie wyłączone.
            secure = "; Secure" if os.environ.get("PANEL_SECURE_COOKIE") == "1" else ""
            if ciasteczko:
                self.send_header("Set-Cookie",
                                 "%s=%s; HttpOnly; SameSite=Strict%s; Path=/; Max-Age=%d"
                                 % (CIASTECZKO, ciasteczko, secure, logowanie.WAZNOSC_SESJI))
            else:
                self.send_header("Set-Cookie",
                                 "%s=; HttpOnly; SameSite=Strict%s; Path=/; Max-Age=0"
                                 % (CIASTECZKO, secure))
        self.end_headers()
        self.wfile.write(tresc)

    def _token(self):
        for kawalek in (self.headers.get("Cookie") or "").split(";"):
            nazwa, _, wartosc = kawalek.strip().partition("=")
            if nazwa == CIASTECZKO:
                return wartosc
        return None

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
            # ---- brama uwierzytelniania ----
            # Stoi PRZED wszystkimi endpointami, więc dodanie nowego nie wymaga
            # pamiętania o zabezpieczeniu go — domyślnie jest chroniony.
            if (metoda, sciezka) not in BEZ_LOGOWANIA:
                if not kto_zalogowany(self.headers):
                    raise Blad(401, "Wymagane zalogowanie.")

            if sciezka == "/api/logowanie" and metoda == "POST":
                token, wynik = zaloguj(self._cialo())
                return self._odpowiedz(200, wynik, ciasteczko=token)
            if sciezka == "/api/wylogowanie" and metoda == "POST":
                logowanie.zamknij_sesje(self._token())
                return self._odpowiedz(200, {"komunikat": "Wylogowano."},
                                       ciasteczko="")
            if sciezka == "/api/sesja" and metoda == "GET":
                login = kto_zalogowany(self.headers)
                return self._odpowiedz(200, {"zalogowany": bool(login), "login": login})

            if sciezka == "/api/schema" and metoda == "GET":
                return self._odpowiedz(200, schema())
            if sciezka == "/api/categories" and metoda == "GET":
                return self._odpowiedz(200, categories())
            if sciezka == "/api/adresy" and metoda == "GET":
                return self._odpowiedz(200, adresy())
            if sciezka == "/api/etykiety" and metoda == "GET":
                return self._odpowiedz(200, etykiety())
            if sciezka == "/api/grafiki" and metoda == "GET":
                return self._odpowiedz(200, grafiki())
            if sciezka == "/api/grafiki/wgraj" and metoda == "POST":
                return self._odpowiedz(200, grafiki_wgraj(self._cialo()))

            if sciezka == "/api/referencje" and metoda == "GET":
                return self._odpowiedz(200, referencje_lista())
            if sciezka == "/api/referencje" and metoda == "POST":
                return self._odpowiedz(200, referencje_zapisz(self._cialo()))
            if sciezka == "/api/referencje/wgraj" and metoda == "POST":
                return self._odpowiedz(200, referencje_wgraj(self._cialo()))
            if sciezka.startswith("/api/referencje/") and metoda == "DELETE":
                return self._odpowiedz(200, referencje_usun(
                    sciezka[len("/api/referencje/"):]))
            if sciezka == "/api/articles" and metoda == "GET":
                return self._odpowiedz(200, articles())
            if sciezka == "/api/articles" and metoda == "POST":
                return self._odpowiedz(201, create(self._cialo()))
            if sciezka == "/api/publish" and metoda == "POST":
                return self._odpowiedz(200, publish())
            if sciezka == "/api/preview" and metoda == "POST":
                return self._odpowiedz(200, preview(self._cialo()))
            if sciezka == "/api/case-preview" and metoda == "POST":
                return self._odpowiedz(200, preview_case(self._cialo()))

            if sciezka == "/api/case-studies" and metoda == "GET":
                return self._odpowiedz(200, case_studies())
            if sciezka == "/api/case-studies" and metoda == "POST":
                return self._odpowiedz(201, create_case(self._cialo()))
            if sciezka.startswith("/api/case-studies/"):
                slug = sciezka[len("/api/case-studies/"):]
                if metoda == "GET":
                    return self._odpowiedz(200, case_study(slug))
                if metoda == "PUT":
                    return self._odpowiedz(200, update_case(slug, self._cialo()))
                if metoda == "DELETE":
                    return self._odpowiedz(200, delete_case(slug))

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
            self._odpowiedz(409, {"blad": "Wpis o takim slugu lub adresie już istnieje."})
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
