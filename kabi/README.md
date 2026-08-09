# KABI CHEMIE — strona internetowa (kondycjonowanie-wody.pl)

Statyczny serwis (czysty **HTML + CSS + odrobina JS**, bez zależności) zbudowany na
podstawie strategii SEO z pliku `Strategia SEO OCMD - kondycjonowanie-wody.pl.xlsx`.
Zawiera **42 podstrony** z dokładnie takimi adresami URL, tytułami, H1, meta opisami
i breadcrumbami, jak w arkuszu „Optymalizacja", oraz układami wg arkusza „Szkice widoków".

## 🚀 Jak uruchomić

Wszystko chodzi w Dockerze — **nie potrzebujesz Pythona na maszynie**.
Polecenia wykonuj w katalogu nadrzędnym (tam, gdzie leży `docker-compose.yml`):

```
docker compose up -d db pgadmin web
```

| Usługa | Adres | Do czego |
|---|---|---|
| `web` | http://localhost:8124 | podgląd wygenerowanej strony |
| `pgadmin` | http://localhost:5050 | edycja treści w bazie |
| `db` | localhost:5432 | PostgreSQL z treścią |

Hasła są w `.env` (plik lokalny, poza repozytorium — wzór w `.env.example`).

## ✏️ Jak dodać artykuł lub case study

Treść bazy wiedzy i case studies **nie jest już w kodzie** — mieszka w PostgreSQL:

| Tabela | Generuje |
|---|---|
| `kabi.articles` | `/baza-wiedzy/{slug}/` |
| `kabi.categories` | `/baza-wiedzy/{kategoria}/` |
| `kabi.case_studies` | adres z kolumny `path` |
| `kabi.knowledge_hub` | konfigurację `/baza-wiedzy/` |

1. Dodaj wiersz w pgAdmin (adres bierze się z kolumny `slug`).
2. Przebuduj stronę:
   ```
   docker compose run --rm builder
   ```
3. Odśwież http://localhost:8124

Kategoria bez ani jednego artykułu nie dostaje własnej strony — jej adres
przekierowuje na hub, żeby nie publikować cienkiej treści. Reguła działa
automatycznie w obie strony.

Pozostała treść (menu, stopka, strony rozwiązań) nadal siedzi w `content.py`,
a wygląd w `src/assets/style.css`. Po ich zmianie też uruchom build.

## 🌍 Wersje językowe

`build.py` **kasuje cały katalog `www/`** i odtwarza wyłącznie wersję polską.
Mirrory EN/DE/AR powstają osobnym krokiem:

```
docker compose run --rm builder python /builder/build_all.py --z-tlumaczeniami
```

Dopóki wszystkie teksty są w cache (`i18n/translations-*.json`), wystarcza lekki
obraz `builder`. **Nowa treść wymaga silnika tłumaczeń** z osobnego, ciężkiego obrazu:

```
docker compose run --rm translator python /builder/setup_translation.py
docker compose run --rm translator python localize_site.py generate
```

`setup_translation.py` dociąga pakiety argostranslate (pl→en, en→de) oraz model
NLLB dla arabskiego. Modele zostają w wolumenie `translator-models` i w `i18n/`
(poza repozytorium — setki MB).

## 📁 Struktura projektu

```
kabichemie/
├─ docker-compose.yml        ← db + pgadmin + web + builder + translator
├─ db/init/001_schema.sql    ← schemat treści (tabele kabi.*)
├─ builder/                  ← skrypty obiegu publikacji
│  ├─ import_snapshot.py     ← snapshot.json → Postgres
│  ├─ export_snapshot.py     ← Postgres → snapshot.json
│  ├─ build_all.py           ← eksport + build + (opcjonalnie) tłumaczenia
│  └─ setup_translation.py   ← jednorazowe pobranie silnika tłumaczeń
└─ kabi/
   ├─ www/                   ← GOTOWA STRONA (to hostujesz)
   ├─ content/snapshot.json  ← treść wyeksportowana z bazy, wersjonowana w gicie
   ├─ content_source.py      ← czyta snapshot dla generatora
   ├─ content_schema.py      ← przekład krotki ↔ nazwane klucze JSON
   ├─ build.py               ← generator stron
   ├─ content.py             ← treść pozostałych stron, menu, stopka
   ├─ knowledge_pages.py     ← render bazy wiedzy (dane z bazy)
   ├─ company_case_pages.py  ← render case studies (dane z bazy)
   ├─ localize_site.py       ← mirrory EN/DE/AR
   ├─ _seo.json              ← title/H1/meta/breadcrumbs z arkusza strategii
   └─ src/assets/            ← źródła stylów/JS/grafik
```

Obieg treści:

```
pgAdmin → Postgres → export_snapshot.py → content/snapshot.json → build.py → www/
```

`snapshot.json` jest commitowany, więc build nie potrzebuje dostępu do bazy —
działa tak samo lokalnie i w CI, a każda zmiana treści zostawia ślad w gicie.

## ✅ Co jest zaimplementowane pod SEO

- Unikalne `<title>` i `meta description` na każdej stronie (1:1 z arkusza)
- Jeden `<h1>` na stronę, nagłówki H2/H3, semantyczny HTML, `lang="pl"`
- `<link rel="canonical">`, Open Graph + Twitter Card, `theme-color`, favicon SVG
- Dane strukturalne JSON-LD: **Organization + WebSite** (strona główna),
  **BreadcrumbList** (każda podstrona), **FAQPage** (strony z sekcją FAQ)
- Widoczne breadcrumbsy, czyste adresy URL, `sitemap.xml`, `robots.txt`, strona `404`
- Responsywność (desktop / tablet / mobile), menu mobilne, formularz kontaktowy

## ⚠️ Do uzupełnienia przed publikacją (placeholdery)

- **Dane kontaktowe** — telefon, e-mail i adres (w `content.py` → `SITE`).
- **Logotypy i nazwy klientów** — obecnie neutralne placeholdery („Zakład mięsny" itp.).
  Prawdziwych marek użyj **wyłącznie za zgodą** klientów (uwaga z arkusza dot. referencji).
- **Dane liczbowe w case studies** — oznaczone jako „przykładowe"; potwierdź i autoryzuj.
- **Formularz kontaktowy** — wersja statyczna (demo). Podłącz do skrzynki e-mail lub usługi
  formularzy (np. Formspree / własny endpoint), żeby realnie wysyłał zgłoszenia.
- **Polityka prywatności / Warunki współpracy** — treść wzorcowa do uzupełnienia.
- **Zdjęcia** — w miejscach grafik są tła/placeholdery; podmień na realne zdjęcia instalacji.
- **Obrazek OG** — `assets/og-default.svg`; do social mediów warto wyeksportować wersję PNG 1200×630.

## 🌐 Wdrożenie

Folder `www/` to komplet plików statycznych — wrzuć go na dowolny hosting
(serwer WWW, Netlify, Cloudflare Pages, GitHub Pages, hosting współdzielony itp.).
Po wgraniu na docelową domenę adresy z arkusza zadziałają bez zmian.
