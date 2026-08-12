# -*- coding: utf-8 -*-
"""Pełny obieg publikacji: Postgres → snapshot → www/.

    docker compose run --rm builder                      # eksport + build PL
    docker compose run --rm builder python /builder/build_all.py --z-tlumaczeniami
    docker compose run --rm builder python /builder/build_all.py --bez-eksportu

Kroki:
  1. export_snapshot.py  — zrzuca treść z bazy do content/snapshot.json
  2. build.py            — składa statyczne www/ (tylko wersja polska)
  3. localize_site.py    — mirrory EN/DE/AR (opcjonalnie; korzysta z cache i18n/)

UWAGA: build.py kasuje cały katalog www/ i odtwarza wyłącznie wersję polską.
Mirrory językowe trzeba odtworzyć krokiem 3, inaczej znikną z dysku.
Dlatego domyślnie ostrzegamy, gdy mirrory istnieją, a build ma iść bez nich.

Krok 3 tłumaczy przez DeepL (HTTP) — działa w lekkim obrazie `builder`, bez
lokalnych modeli. Nowe ciągi wymagają klucza DEEPL_API_KEY w środowisku; gdy
wszystkie są już w cache (i18n/translations-*.json), krok 3 nie wysyła nic do
API i klucz nie jest potrzebny.
"""
import argparse
import subprocess
import sys
from pathlib import Path

SITE = Path("/site")
MIRRORS = ("en", "de", "ar")


def run(command, opis):
    print("\n=== %s ===" % opis, flush=True)
    result = subprocess.run(command, cwd=SITE)
    if result.returncode != 0:
        sys.exit("przerwano: %s zakonczylo sie kodem %d" % (opis, result.returncode))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bez-eksportu", action="store_true",
                        help="pomija krok 1 — buduje z istniejacego snapshot.json")
    parser.add_argument("--z-tlumaczeniami", action="store_true",
                        help="odtwarza mirrory EN/DE/AR po buildzie")
    args = parser.parse_args()

    mirrors_present = [d for d in MIRRORS if (SITE / "www" / d).is_dir()]
    if mirrors_present and not args.z_tlumaczeniami:
        print("UWAGA: build.py skasuje istniejace mirrory %s."
              % ", ".join(mirrors_present))
        print("       Odtworz je przez --z-tlumaczeniami albo osobno:")
        print("       docker compose run --rm builder python localize_site.py generate")

    if not args.bez_eksportu:
        run([sys.executable, "/builder/export_snapshot.py"], "1/3 eksport treści z bazy")

    run([sys.executable, "build.py"], "2/3 generowanie www/ (PL)")

    if args.z_tlumaczeniami:
        run([sys.executable, "localize_site.py", "generate"], "3/3 mirrory EN/DE/AR")

    print("\ngotowe.")


if __name__ == "__main__":
    main()
