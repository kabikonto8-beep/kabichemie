# -*- coding: utf-8 -*-
"""Logowanie do panelu: haszowanie haseł i sesje.

HASŁA
Nie przechowujemy haseł, tylko wynik funkcji scrypt — algorytmu celowo
kosztownego pamięciowo, więc odpornego na łamanie na kartach graficznych.
Każde hasło ma własną losową sól, żeby dwa identyczne hasła dawały różne
wyniki i żeby nie dało się użyć gotowych tablic.

Zapis w bazie ma postać samoopisującą:
    scrypt$n=16384,r=8,p=1$<sól base64>$<hasz base64>
Parametry są w rekordzie, więc podniesienie kosztu w przyszłości nie unieważni
istniejących haseł — stare zweryfikują się swoimi parametrami.

SESJE
Token to 32 losowe bajty z generatora kryptograficznego. Trzymamy je w pamięci
procesu, nie w bazie: restart API wylogowuje wszystkich, co dla narzędzia
lokalnego jest zaletą, a nie wadą — nie ma czego wykraść z dysku.
"""
import base64
import hashlib
import hmac
import os
import secrets
import time

# Parametry scrypt. n=16384 to około 16 MB pamięci na jedno sprawdzenie —
# dla logowania niezauważalne, dla łamania hasła bardzo kosztowne.
SCRYPT_N = 16384
SCRYPT_R = 8
SCRYPT_P = 1
DLUGOSC_SOLI = 16
DLUGOSC_HASZA = 32

WAZNOSC_SESJI = 12 * 3600          # 12 godzin
MIN_DLUGOSC_HASLA = 10


def zahashuj(haslo):
    """Hasło → samoopisujący się zapis do zapisania w bazie."""
    if len(haslo) < MIN_DLUGOSC_HASLA:
        raise ValueError("Hasło musi mieć co najmniej %d znaków." % MIN_DLUGOSC_HASLA)

    sol = os.urandom(DLUGOSC_SOLI)
    hasz = hashlib.scrypt(haslo.encode("utf-8"), salt=sol,
                          n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P, dklen=DLUGOSC_HASZA)
    return "scrypt$n=%d,r=%d,p=%d$%s$%s" % (
        SCRYPT_N, SCRYPT_R, SCRYPT_P,
        base64.b64encode(sol).decode("ascii"),
        base64.b64encode(hasz).decode("ascii"),
    )


def sprawdz_haslo(haslo, zapis):
    """Czy hasło pasuje do zapisu z bazy. Porównanie odporne na pomiar czasu."""
    try:
        algorytm, parametry, sol_b64, hasz_b64 = zapis.split("$")
        if algorytm != "scrypt":
            return False
        wartosci = dict(kv.split("=") for kv in parametry.split(","))
        sol = base64.b64decode(sol_b64)
        oczekiwany = base64.b64decode(hasz_b64)
        policzony = hashlib.scrypt(
            haslo.encode("utf-8"), salt=sol,
            n=int(wartosci["n"]), r=int(wartosci["r"]), p=int(wartosci["p"]),
            dklen=len(oczekiwany),
        )
    except Exception:
        return False
    # compare_digest zamiast ==: czas porównania nie zdradza, ile znaków się zgadza.
    return hmac.compare_digest(policzony, oczekiwany)


# --------------------------------------------------------------- sesje
_sesje = {}          # token -> {"login": str, "wygasa": float}


def zaloz_sesje(login):
    token = secrets.token_urlsafe(32)
    _sesje[token] = {"login": login, "wygasa": time.time() + WAZNOSC_SESJI}
    _posprzataj()
    return token


def sesja(token):
    """Zwraca dane sesji albo None. Sam token nie wystarczy po wygaśnięciu."""
    dane = _sesje.get(token or "")
    if not dane:
        return None
    if dane["wygasa"] < time.time():
        _sesje.pop(token, None)
        return None
    return dane


def zamknij_sesje(token):
    _sesje.pop(token or "", None)


def _posprzataj():
    teraz = time.time()
    for token in [t for t, d in _sesje.items() if d["wygasa"] < teraz]:
        _sesje.pop(token, None)


# ------------------------------------------- ochrona przed zgadywaniem
# Każda nieudana próba wydłuża oczekiwanie dla danego loginu. Bez tego
# hasło można by zgadywać w nieskończoność z pełną prędkością.
_nieudane = {}       # login -> {"ile": int, "do_kiedy": float}
LIMIT_PROB = 5
BLOKADA_SEKUND = 30


def czy_zablokowany(login):
    wpis = _nieudane.get(login)
    if not wpis:
        return 0
    pozostalo = wpis["do_kiedy"] - time.time()
    return int(pozostalo) if pozostalo > 0 else 0


def zapisz_nieudana(login):
    wpis = _nieudane.setdefault(login, {"ile": 0, "do_kiedy": 0})
    wpis["ile"] += 1
    if wpis["ile"] >= LIMIT_PROB:
        # Blokada rośnie z każdą kolejną serią: 30 s, 60 s, 120 s…
        mnoznik = 2 ** (wpis["ile"] - LIMIT_PROB)
        wpis["do_kiedy"] = time.time() + BLOKADA_SEKUND * mnoznik


def wyczysc_nieudane(login):
    _nieudane.pop(login, None)
