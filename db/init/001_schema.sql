-- =============================================================================
-- KABI CHEMIE — schemat treści (baza wiedzy + case studies)
--
-- Źródło prawdy dla sekcji /baza-wiedzy/ i /case-study/. Generator (build.py)
-- czyta stąd dane przez builder/export_content.py i składa statyczne www/.
--
-- Konwencja pól złożonych: JSONB jako tablica obiektów z NAZWANYMI kluczami
-- (nie krotki pozycyjne) — dzięki temu da się to sensownie edytować w pgAdmin.
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS kabi;
SET search_path TO kabi, public;


-- ----------------------------------------------------------------- pomocnicze
-- Polskie sortowanie (ą przed b, ł przed m…). Obraz alpine nie ma locale
-- systemowych, więc bierzemy kolację z ICU — działa niezależnie od systemu.
CREATE COLLATION IF NOT EXISTS kabi.pl (provider = icu, locale = 'pl-PL');

-- Slug: małe litery, cyfry i pojedyncze myślniki — 1:1 z adresami na stronie.
CREATE DOMAIN kabi.slug AS text
  CHECK (VALUE ~ '^[a-z0-9]+(-[a-z0-9]+)*$');

-- Tablica JSON (a nie obiekt/skalar) — wspólny warunek dla pól złożonych.
CREATE OR REPLACE FUNCTION kabi.is_json_array(value jsonb)
RETURNS boolean LANGUAGE sql IMMUTABLE AS $$
  SELECT value IS NULL OR jsonb_typeof(value) = 'array'
$$;

CREATE OR REPLACE FUNCTION kabi.touch_updated_at()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END;
$$;


-- ================================================================== KATEGORIE
-- Odpowiednik knowledge_pages.CATEGORIES. Generuje /baza-wiedzy/{slug}/.
CREATE TABLE kabi.categories (
  id            integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  slug          kabi.slug NOT NULL UNIQUE,
  title         text    NOT NULL,
  h1            text    NOT NULL,
  kicker        text    NOT NULL,
  lead          text    NOT NULL,
  hub_blurb     text    NOT NULL,
  stream_title  text    NOT NULL,
  image         text    NOT NULL,

  -- [{"label": "Zakres", "value": "Kamień, kondensat…"}]
  facts         jsonb   NOT NULL DEFAULT '[]'::jsonb
                        CHECK (kabi.is_json_array(facts)),
  -- [{"kicker": "Rozwiązania", "title": "Kotły parowe", "url": "/kotly-parowe/"}]
  related       jsonb   NOT NULL DEFAULT '[]'::jsonb
                        CHECK (kabi.is_json_array(related)),

  published     boolean NOT NULL DEFAULT true,
  sort_order    integer NOT NULL DEFAULT 0,
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE  kabi.categories       IS 'Kategorie bazy wiedzy — generują /baza-wiedzy/{slug}/';
COMMENT ON COLUMN kabi.categories.image IS 'Ścieżka bezwzględna od roota www, np. /assets/blog/blog-kotly-parowe.jpg';
COMMENT ON COLUMN kabi.categories.facts IS 'Tablica {label, value} — kafelki faktów w hero kategorii';


-- =================================================================== ARTYKUŁY
-- Odpowiednik knowledge_pages.ARTICLES. Generuje /baza-wiedzy/{slug}/ (płasko).
CREATE TABLE kabi.articles (
  id            integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  slug          kabi.slug NOT NULL UNIQUE,
  category_id   integer REFERENCES kabi.categories(id) ON DELETE SET NULL,

  title         text    NOT NULL,   -- <title> i H1 artykułu
  list_title    text    NOT NULL,   -- nagłówek na liście/hubie
  short         text    NOT NULL,   -- krótka etykieta (breadcrumb, kafelki)
  topic         text    NOT NULL,   -- nadtemat, np. „Kotły parowe"
  excerpt       text,               -- zajawka na liście; brak → generator bierze `lead`
  lead          text    NOT NULL,   -- lead pod H1
  audience      text    NOT NULL,   -- „Dla kogo"
  read_time     text    NOT NULL,   -- np. „8 min"
  image         text,               -- NULL → grafika huba

  prose         text    NOT NULL,   -- treść artykułu jako HTML (h2/p/ul/…)

  -- [{"value": "+10%", "label": "więcej paliwa już przy 1 mm kamienia"}]
  -- NULL, a nie '[]' — rozróżnienie „pola nie ma" od „jest, ale puste"
  -- jest potrzebne, żeby eksport odtwarzał wejście bajt w bajt.
  feature_stats jsonb   CHECK (kabi.is_json_array(feature_stats)),
  -- [{"q": "Jak często odkamieniać kocioł?", "a": "Zależy od…"}]
  faq           jsonb   NOT NULL DEFAULT '[]'::jsonb
                        CHECK (kabi.is_json_array(faq)),
  -- [{"kicker": "Case study", "title": "Kocioł Fako", "url": "/case-study/…/"}]
  related       jsonb   NOT NULL DEFAULT '[]'::jsonb
                        CHECK (kabi.is_json_array(related)),

  published     boolean NOT NULL DEFAULT true,
  sort_order    integer NOT NULL DEFAULT 0,
  published_at  date    NOT NULL DEFAULT CURRENT_DATE,
  created_at    timestamptz NOT NULL DEFAULT now(),
  updated_at    timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX articles_category_idx ON kabi.articles (category_id);
CREATE INDEX articles_published_idx ON kabi.articles (published, sort_order);

COMMENT ON TABLE  kabi.articles      IS 'Artykuły bazy wiedzy — generują /baza-wiedzy/{slug}/';
COMMENT ON COLUMN kabi.articles.prose IS 'HTML treści (nie Markdown) — zachowuje klasy typu <p class="note">';
COMMENT ON COLUMN kabi.articles.faq  IS 'Tablica {q, a} — trafia też do JSON-LD FAQPage';


-- =============================================================== CASE STUDIES
-- Odpowiednik company_case_pages.CASE_STUDIES. Adres bierze się z `path`,
-- bo obecne URL-e nie są pochodną sluga (np. slug „fako" → /case-study/kociol-parowy-fako/).
CREATE TABLE kabi.case_studies (
  id              integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  slug            kabi.slug NOT NULL UNIQUE,
  path            text    NOT NULL UNIQUE
                          CHECK (path ~ '^/[a-z0-9/-]*/$'),

  kicker          text    NOT NULL,
  h1              text    NOT NULL,   -- może zawierać <span> do wyróżnienia
  lead            text    NOT NULL,
  image           text    NOT NULL,
  image_position  text    NOT NULL DEFAULT 'center center',

  -- ["Kocioł parowy Fako", "Odkamienianie chemiczne", …]
  signals         jsonb   NOT NULL DEFAULT '[]'::jsonb
                          CHECK (kabi.is_json_array(signals)),

  result_kicker   text,
  result_value    text,
  result_label    text,
  result_note     text,

  -- [{"label": "Diagnoza", "text": "Twarda woda, przewodność 4200 µS…"}]
  overview        jsonb   NOT NULL DEFAULT '[]'::jsonb
                          CHECK (kabi.is_json_array(overview)),

  challenge_title text,
  challenge_intro text,
  -- [{"title": "Twarda woda zasilająca", "text": "…", "tag": "Woda zasilająca"}]
  issues          jsonb   NOT NULL DEFAULT '[]'::jsonb
                          CHECK (kabi.is_json_array(issues)),

  process_title   text,
  process_intro   text,
  -- [{"title": "Analiza wody i oględziny", "text": "…"}]
  process         jsonb   NOT NULL DEFAULT '[]'::jsonb
                          CHECK (kabi.is_json_array(process)),

  results_title   text,
  results_intro   text,
  results_note    text,
  -- [{"count": 32, "prefix": "−", "suffix": "%", "label": "…", "before": "…", "after": "…"}]
  -- albo [{"value": "4200 → 2800 µS", "label": "…", "before": "…", "after": "…"}]
  metrics         jsonb   NOT NULL DEFAULT '[]'::jsonb
                          CHECK (kabi.is_json_array(metrics)),

  field_title     text,
  field_intro     text,
  -- [{"title": "…", "text": "…"}]
  field_notes     jsonb   NOT NULL DEFAULT '[]'::jsonb
                          CHECK (kabi.is_json_array(field_notes)),

  faq_title       text,
  faq_intro       text,
  faq             jsonb   NOT NULL DEFAULT '[]'::jsonb
                          CHECK (kabi.is_json_array(faq)),

  cta_title       text,
  cta_text        text,
  -- [{"classes": "btn btn-primary", "label": "Umów rozmowę", "url": "/kontakt/"}]
  -- Nieużywane przez obecne 3 case studies — stąd NULL zamiast '[]'.
  actions         jsonb   CHECK (kabi.is_json_array(actions)),
  related         jsonb   NOT NULL DEFAULT '[]'::jsonb
                          CHECK (kabi.is_json_array(related)),

  published       boolean NOT NULL DEFAULT true,
  sort_order      integer NOT NULL DEFAULT 0,
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE  kabi.case_studies      IS 'Case studies — generują stronę pod adresem z kolumny path';
COMMENT ON COLUMN kabi.case_studies.path IS 'Pełny adres ze slashem na końcu, np. /case-study/kociol-parowy-fako/';
COMMENT ON COLUMN kabi.case_studies.h1   IS 'Dopuszcza <span>…</span> do wyróżnienia fragmentu nagłówka';


-- ================================================================ HUB WIEDZY
-- Konfiguracja strony /baza-wiedzy/ (odpowiednik knowledge_pages.HUB).
-- Jeden wiersz, wymuszony warunkiem CHECK.
CREATE TABLE kabi.knowledge_hub (
  id       integer PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  kicker   text NOT NULL,
  h1       text NOT NULL,
  lead     text NOT NULL,
  image    text NOT NULL,
  facts    jsonb NOT NULL DEFAULT '[]'::jsonb
                 CHECK (kabi.is_json_array(facts)),
  updated_at timestamptz NOT NULL DEFAULT now()
);


-- ------------------------------------------------------------------ triggery
CREATE TRIGGER categories_touch    BEFORE UPDATE ON kabi.categories
  FOR EACH ROW EXECUTE FUNCTION kabi.touch_updated_at();
CREATE TRIGGER articles_touch      BEFORE UPDATE ON kabi.articles
  FOR EACH ROW EXECUTE FUNCTION kabi.touch_updated_at();
CREATE TRIGGER case_studies_touch  BEFORE UPDATE ON kabi.case_studies
  FOR EACH ROW EXECUTE FUNCTION kabi.touch_updated_at();
CREATE TRIGGER knowledge_hub_touch BEFORE UPDATE ON kabi.knowledge_hub
  FOR EACH ROW EXECUTE FUNCTION kabi.touch_updated_at();


-- -------------------------------------------------------- widoki dla pgAdmin
-- Wygodny przegląd artykułów z nazwą kategorii zamiast ID.
CREATE VIEW kabi.v_articles AS
SELECT a.id,
       a.slug,
       a.title,
       c.title            AS kategoria,
       a.read_time,
       a.published,
       a.sort_order,
       jsonb_array_length(a.faq)     AS pytan_faq,
       jsonb_array_length(a.related) AS powiazanych,
       length(a.prose)               AS dlugosc_html,
       a.updated_at
FROM kabi.articles a
LEFT JOIN kabi.categories c ON c.id = a.category_id
ORDER BY a.sort_order, a.slug;

COMMENT ON VIEW kabi.v_articles IS 'Przegląd artykułów do szybkiej kontroli w pgAdmin (tylko odczyt)';

CREATE VIEW kabi.v_case_studies AS
SELECT id, slug, path, h1, result_value, result_label, published, sort_order, updated_at
FROM kabi.case_studies
ORDER BY sort_order, slug;
