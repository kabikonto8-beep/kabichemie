# -*- coding: utf-8 -*-
"""Jednorazowe przygotowanie silnika tłumaczeń (uruchamiać w usłudze `translator`).

    docker compose run --rm translator python /builder/setup_translation.py

Pobiera to, czego localize_site.py oczekuje na dysku, a czego nie ma w repo:

  1. Pakiety językowe argostranslate: pl→en oraz en→de.
     Trafiają do wolumenu /models/argos (ARGOS_PACKAGES_DIR).

  2. Model NLLB-200-distilled-600M dla arabskiego, w dwóch postaciach:
       kabi/i18n/nllb-200-distilled-600M  — tokenizer + wagi z HuggingFace
       kabi/i18n/nllb-ct2-int8            — konwersja na ctranslate2 (int8)
     Oba katalogi są w .gitignore — to setki MB, trzymamy je poza repo.

Skrypt jest idempotentny: pomija kroki, których wynik już istnieje.
"""
import shutil
import subprocess
import sys
from pathlib import Path

I18N = Path("/site/i18n")
NLLB_DIR = I18N / "nllb-200-distilled-600M"
CT2_DIR = I18N / "nllb-ct2-int8"
HF_MODEL_ID = "facebook/nllb-200-distilled-600M"

# Pary, których używa localize_site.py: pl→en, potem en→de (przez angielski).
ARGOS_PAIRS = (("pl", "en"), ("en", "de"))


def krok(numer, opis):
    print("\n=== %s  %s ===" % (numer, opis), flush=True)


def setup_argos():
    krok("1/2", "pakiety językowe argostranslate")
    import argostranslate.package

    installed = {
        (p.from_code, p.to_code) for p in argostranslate.package.get_installed_packages()
    }
    brakujace = [para for para in ARGOS_PAIRS if para not in installed]
    if not brakujace:
        print("  wszystkie pary już zainstalowane: %s"
              % ", ".join("%s→%s" % p for p in ARGOS_PAIRS))
        return

    print("  aktualizuję indeks pakietów…", flush=True)
    argostranslate.package.update_package_index()
    dostepne = argostranslate.package.get_available_packages()

    for from_code, to_code in brakujace:
        match = next(
            (p for p in dostepne if p.from_code == from_code and p.to_code == to_code),
            None,
        )
        if match is None:
            sys.exit("BŁĄD: brak pakietu %s→%s w indeksie argostranslate"
                     % (from_code, to_code))
        print("  pobieram %s→%s…" % (from_code, to_code), flush=True)
        argostranslate.package.install_from_path(match.download())
        print("  zainstalowano %s→%s" % (from_code, to_code))


def setup_nllb():
    krok("2/2", "model NLLB dla arabskiego")

    if NLLB_DIR.exists() and any(NLLB_DIR.iterdir()):
        print("  %s już istnieje — pomijam pobieranie" % NLLB_DIR)
    else:
        print("  pobieram %s z HuggingFace (~2,5 GB)…" % HF_MODEL_ID, flush=True)
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        NLLB_DIR.mkdir(parents=True, exist_ok=True)
        # src_lang jak w localize_site.translate_catalog_nllb_ar
        tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_ID, src_lang="pol_Latn")
        tokenizer.save_pretrained(NLLB_DIR)
        model = AutoModelForSeq2SeqLM.from_pretrained(HF_MODEL_ID)
        model.save_pretrained(NLLB_DIR)
        print("  zapisano do %s" % NLLB_DIR)

    if CT2_DIR.exists() and any(CT2_DIR.iterdir()):
        print("  %s już istnieje — pomijam konwersję" % CT2_DIR)
        return

    converter = shutil.which("ct2-transformers-converter")
    if converter is None:
        sys.exit("BŁĄD: brak ct2-transformers-converter — czy to na pewno obraz `translator`?")

    print("  konwertuję na ctranslate2 (int8)…", flush=True)
    result = subprocess.run([
        converter,
        "--model", str(NLLB_DIR),
        "--output_dir", str(CT2_DIR),
        "--quantization", "int8",
    ])
    if result.returncode != 0:
        shutil.rmtree(CT2_DIR, ignore_errors=True)
        sys.exit("BŁĄD: konwersja ctranslate2 zakończyła się kodem %d" % result.returncode)
    print("  zapisano do %s" % CT2_DIR)


setup_argos()
setup_nllb()

print("\nSilnik gotowy. Teraz:")
print("  docker compose run --rm translator python localize_site.py generate")
