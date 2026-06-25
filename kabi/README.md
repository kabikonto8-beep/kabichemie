# Kabi-Chemie — strona internetowa (kondycjonowanie-wody.pl)

Statyczny serwis (czysty **HTML + CSS + odrobina JS**, bez zależności) zbudowany na
podstawie strategii SEO z pliku `Strategia SEO OCMD - kondycjonowanie-wody.pl.xlsx`.
Zawiera **42 podstrony** z dokładnie takimi adresami URL, tytułami, H1, meta opisami
i breadcrumbami, jak w arkuszu „Optymalizacja", oraz układami wg arkusza „Szkice widoków".

## 🚀 Jak obejrzeć stronę

**Najprościej:** kliknij dwukrotnie **`start-podglad.bat`** — otworzy się przeglądarka
pod adresem `http://localhost:8124/`. Okno terminala zostaw otwarte (zamknięcie = stop serwera).

Alternatywnie z terminala (w tym folderze):

```
py -m http.server 8124 --directory www
```

> Strona używa „czystych" adresów (np. `/kotly-parowe/odkamienianie/`), dlatego najlepiej
> oglądać ją przez lokalny serwer (jak wyżej), a nie przez dwukrotne kliknięcie `www/index.html`
> (przy otwarciu z dysku `file://` nie działają adresy katalogowe i wspólny CSS).

## 📁 Struktura projektu

```
kabi/
├─ www/                      ← GOTOWA STRONA (to hostujesz / oddajesz)
│  ├─ index.html             ← strona główna
│  ├─ kotly-parowe/…         ← 42 podstrony w strukturze katalogów = czyste URL-e
│  ├─ assets/                ← style.css, main.js, logo, favicon, obrazek OG
│  ├─ sitemap.xml, robots.txt, 404.html
│
├─ build.py                  ← generator (składa strony z danych + treści)
├─ content.py                ← TREŚĆ i konfiguracja (menu, stopka, sekcje stron)
├─ _seo.json                 ← title/H1/meta/breadcrumbs wyciągnięte z arkusza
├─ _extract_seo.py           ← skrypt, który tworzy _seo.json z pliku .xlsx
├─ _validate.py              ← kontrola: linki wewnętrzne + kompletność SEO
└─ src/assets/               ← źródła stylów/JS/grafik (kopiowane do www/assets)
```

## ✏️ Jak edytować i przegenerować

1. Treść stron i menu zmieniasz w **`content.py`**, wygląd w **`src/assets/style.css`**.
2. Przegeneruj stronę:
   ```
   py -X utf8 build.py
   ```
3. (Opcjonalnie) sprawdź spójność:
   ```
   py -X utf8 _validate.py
   ```
   Ostatni raport: **42 strony, 2366 linków wewnętrznych, 0 błędnych, 0 braków SEO.**

Jeśli zaktualizujesz arkusz strategii, odśwież dane SEO: `py -X utf8 _extract_seo.py`, potem `build.py`.

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
