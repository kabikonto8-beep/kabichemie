# -*- coding: utf-8 -*-
"""Zakłada konto do panelu albo zmienia hasło istniejącemu.

    docker compose run --rm builder python /builder/ustaw_haslo.py

Hasło wpisujesz sam, przy wyłączonym echu — nie pojawia się na ekranie,
w historii poleceń ani w logach. Do bazy trafia wyłącznie wynik funkcji
scrypt razem z solą; samego hasła nie da się z niego odtworzyć.

Jeśli zapomnisz hasła, nie ma go jak odzyskać — uruchom skrypt ponownie
i ustaw nowe.
"""
import getpass
import os
import sys

sys.path.insert(0, "/builder")

import psycopg  # noqa: E402
from psycopg.rows import dict_row  # noqa: E402

import logowanie  # noqa: E402


def main():
    print("Konto do panelu redakcyjnego KABI CHEMIE")
    print("-" * 45)

    login = input("Login: ").strip()
    if not login:
        sys.exit("Login nie może być pusty.")

    haslo = getpass.getpass("Hasło (min. %d znaków, nie będzie widoczne): "
                            % logowanie.MIN_DLUGOSC_HASLA)
    powtorz = getpass.getpass("Powtórz hasło: ")

    if haslo != powtorz:
        sys.exit("Hasła się różnią — nic nie zmieniono.")
    try:
        zapis = logowanie.zahashuj(haslo)
    except ValueError as exc:
        sys.exit(str(exc))

    with psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO kabi.panel_uzytkownicy (login, hash)
                VALUES (%s, %s)
                ON CONFLICT (login) DO UPDATE SET hash = EXCLUDED.hash
                RETURNING login, (xmax = 0) AS nowe
            """, (login, zapis))
            wynik = cur.fetchone()
            conn.commit()

    print()
    print("Konto %r %s." % (wynik["login"],
                            "utworzone" if wynik["nowe"] else "zaktualizowane"))
    print("Zaloguj się w panelu skrótem Ctrl + Shift + Y.")


if __name__ == "__main__":
    main()
