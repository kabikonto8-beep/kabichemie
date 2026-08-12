# Hostowany panel redakcyjny — runbook wdrożeniowy

Publiczną stronę hostuje **Vercel** (serwuje `kabi/www/` z gałęzi repo). Ten
katalog stawia **hostowany panel** do zdalnej edycji treści. Panel edytuje bazę,
a „Publikuj" robi eksport → czysty build → `git push`; Vercel sam deployuje.

```
   Vercel (publiczna strona)  ◀── git push ──  Host panelu               Neon
      kabi/www/ z repo                          admin-api + nginx +       (Postgres)
                                                Caddy HTTPS, KABI_ADMIN ── treść + konta
```

## Co gdzie mieszka

| Element | Gdzie |
|---|---|
| Publiczna strona (statyczny `www/`) | Vercel (bez zmian) |
| Panel + admin-api + nginx + Caddy | Host panelu (Docker) — ten katalog |
| Postgres (treść + konta) | Neon / Supabase (zewnętrzna) |
| Tłumaczenia EN/DE/AR | DeepL (HTTP, klucz w env) |

## Wymagania wstępne
- Host z Dockerem (Railway/Render/Fly.io/VPS) i publicznym IP + portami 80/443.
- Domena panelu wskazująca na host, np. `panel.kondycjonowanie-wody.pl` (rekord A/AAAA).
- Konto Neon (darmowe), klucz DeepL (Free), dostęp do repo na GitHubie.

---

## Krok 1 — Baza Neon
1. Załóż projekt na neon.tech, weź connection string (z `?sslmode=require`).
2. Zastosuj schemat i wgraj treść (lokalnie, wskazując na Neon):
   ```bash
   export DATABASE_URL='postgresql://…@…/kabi?sslmode=require'
   psql "$DATABASE_URL" -f db/init/001_schema.sql
   docker compose run --rm -e DATABASE_URL="$DATABASE_URL" builder python /builder/import_snapshot.py
   ```
3. Załóż konto do panelu (hasło ustawiasz Ty):
   ```bash
   docker compose run --rm -e DATABASE_URL="$DATABASE_URL" builder python /builder/ustaw_haslo.py
   ```

## Krok 2 — Klucz deploy do repo (żeby „Publikuj" mógł pushować)
Na hoście panelu:
```bash
cd deploy
ssh-keygen -t ed25519 -N "" -f ./deploy_key            # tworzy deploy_key + deploy_key.pub
ssh-keyscan github.com > ./known_hosts                 # host key GitHuba
```
Wgraj `deploy_key.pub` do repo na GitHubie jako **Deploy key z prawem zapisu**
(Settings → Deploy keys → Add, zaznacz „Allow write access").
Ustaw remote repo na SSH: `git remote set-url origin git@github.com:reginx032-prog/kabi-nowe.git`.
> `deploy_key` NIE trafia do repo (jest w `.gitignore`).

## Krok 3 — Konfiguracja i start
```bash
cd deploy
cp .env.example .env      # i uzupełnij wartości
docker compose -f docker-compose.panel.yml up -d --build
```
`.env` (patrz `.env.example`): `DATABASE_URL`, `DEEPL_API_KEY`, `PANEL_DOMAIN`,
`PANEL_HOSTS` (= domena panelu), `PANEL_GIT_BRANCH`.

Caddy sam pobierze certyfikat Let's Encrypt dla `PANEL_DOMAIN` (port 80/443 muszą być otwarte).

## Krok 4 — Weryfikacja
- `https://panel.…/` — otwiera stronę; skrót/`#panel` pokazuje ekran logowania.
- Zaloguj się kontem z Kroku 1. Panel działa (blokada localhost przepuszcza `PANEL_HOSTS`).
- Edytuj coś → „Publikuj". W logach `admin-api` zobaczysz export → build → push.
- Vercel po pushu zdeployuje nową wersję publicznej strony.

---

## Jak działa publikacja (tryb `PANEL_DEPLOY=git`)
`admin_api._publish_git()`:
1. `export_snapshot.py` — baza → `kabi/content/snapshot.json`.
2. `build.py` **bez** `KABI_ADMIN` — czyste `www/` (bez panelu) + mirrory DeepL.
3. `git add` (www, snapshot, i18n, uploads, referencje) → `commit` → `push`.
4. Odbudowa wersji **z** panelem, żeby host dalej serwował edytor.

Host panelu jest **jedynym** miejscem, które pushuje wygenerowane `www/` na gałąź
Vercela — nie edytuj tej gałęzi z dwóch stron równolegle (konflikt na plikach
generowanych). Zmiany w kodzie rób na osobnej gałęzi / przez PR.

## Bezpieczeństwo (już zapewnione / do pilnowania)
- HTTPS (Caddy) + ciasteczko `Secure` (`PANEL_SECURE_COOKIE=1`) + `HttpOnly; SameSite=Strict`.
- Logowanie scrypt + blokada zgadywania hasła (5 prób → narastające opóźnienie).
- admin-api nieopublikowany — ruch tylko przez Caddy→nginx z tego samego origin.
- Sesje trzymane w RAM → jedna instancja admin-api, restart wylogowuje (OK dla małego zespołu).
- Redaktor przez pole „Własny kod strony" (`html`) może wstawić `<script>` na publiczną
  stronę (CSP dopuszcza inline) — świadoma decyzja, ufaj tylko zaufanym kontom.
- Opcjonalnie: limit żądań na `/api/logowanie` na poziomie hosta/WAF.
