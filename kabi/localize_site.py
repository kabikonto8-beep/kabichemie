# -*- coding: utf-8 -*-
"""Generate and verify complete EN, DE and AR mirrors of the Polish static site."""

from __future__ import annotations

import argparse
import copy
import difflib
import json
import os
import re
import shutil
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

from lxml import etree, html

from reviewed_translations import REVIEWED_TRANSLATIONS
from semantic_translations import AUTOKLAW_TRANSLATIONS


ROOT = Path(__file__).resolve().parent
WWW = ROOT / "www"
I18N = ROOT / "i18n"
DOMAIN = "https://kondycjonowanie-wody.pl"
LANGS = {
    "en": {"locale": "en_US", "name": "English", "dir": "ltr"},
    "de": {"locale": "de_DE", "name": "Deutsch", "dir": "ltr"},
    "ar": {"locale": "ar_SA", "name": "العربية", "dir": "rtl"},
}
LANG_CODES = ("pl", "en", "de", "ar")
SKIP_TAGS = {"script", "style", "svg", "path", "noscript", "template"}
META_KEYS = {
    "description", "og:title", "og:description", "og:image:alt",
    "twitter:title", "twitter:description", "twitter:image:alt",
}
JSON_SKIP_KEYS = {
    "@context", "@type", "@id", "url", "logo", "image", "telephone",
    "email", "taxID", "vatID", "dateModified", "postalCode", "addressCountry",
    "cssSelector",
}
PRESERVE_EXACT = {
    "KABI CHEMIE", "KABI", "CHEMIE", "KCAQUA", "RO", "NIP", "LinkedIn", "Facebook", "YouTube",
    "Łukasz Mielcarz", "Przemysław Jesiołkowski", "Łukasz Kumor",
    "Siedlce", "Toruń", "Evapco", "EVAPCO", "BAC", "Fako", "PL", "EN", "DE", "AR",
    "PLN", "pH", "CIP", "TDS", "COD", "B2B", "ISO", "Legionella",
    "kondycjonowanie-wody.pl", "Google Maps", "Microsoft Clarity",
}
POLISH_WORDS = re.compile(
    r"\b(?:aby|albo|analiza|audyt|baza|bezpłatn\w*|branż\w*|chemia|dane|dla|"
    r"działa\w*|energia|instalacj\w*|jest|koszt\w*|kocioł|kotł\w*|"
    r"można|najczęściej|ochrona|odkamienianie|oraz|osad\w*|parametr\w*|polski|"
    r"proces|przemysł\w*|rozwiązani\w*|serwis|sprawdź|strona|technologia|układ\w*|"
    r"umów|usług\w*|wartość|wiedza|woda|wody|wybierz|wynik\w*|zwiększ|zmniejsz)\b",
    re.IGNORECASE,
)
JS_STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
URL_OR_EMAIL_RE = re.compile(r"^(?:https?://|mailto:|tel:)|^[^\s@]+@[^\s@]+\.[^\s@]+$")
KEEP_RE = re.compile(r"https?://[^\s]+|[^\s@]+@[^\s@]+\.[^\s@]+|\+?\d[\d\s()-]{6,}")
MARKER_RE = re.compile(r"ZXKABISEG(\d{4})ZX")
BIDI_NUMBER_RE = re.compile(
    r"(?:\+?\d(?:[\d\s.,:/()\-]*\d)?|\d)"
    r"(?:\s*(?:%|٪|PLN|zł|°[CFn]?|µS|μS|m³|m²|m3|mm|cm|km|kW|MW|MWh|kWh|"
    r"t/h|mg/l|ppm|bar|min|h))?",
    re.IGNORECASE,
)


MANUAL = {
    "en": {
        "Strona główna": "Home", "Technologia KCAQUA": "KCAQUA Technology",
        "Rozwiązania": "Solutions", "Branże": "Industries", "Case studies": "Case Studies",
        "Kalkulator": "Calculator", "Baza wiedzy": "Knowledge Base", "Firma": "Company",
        "Kontakt": "Contact", "Umów darmowy audyt": "Book a free audit", "Oferta": "Solutions",
        "Usługi": "Services", "Misja firmy": "Company mission",
        "Model współpracy": "Collaboration model", "Referencje": "Client references",
        "Kotły parowe": "Steam boilers", "Skraplacze wyparne": "Evaporative condensers",
        "Autoklawy i pasteryzatory": "Autoclaves and pasteurizers",
        "Ochrona membran RO": "RO membrane protection", "Odkamienianie instalacji": "System descaling",
        "Ochrona antykorozyjna": "Corrosion protection", "Audyt techniczny": "Technical audit",
        "Analiza wody": "Water analysis", "Serwis i automatyka": "Service and automation",
        "Białe certyfikaty": "Energy efficiency certificates", "Wiedza": "Knowledge",
        "Polityka prywatności": "Privacy policy", "Oddział w Toruniu": "Toruń branch",
        "Siedziba główna": "Head office", "Przejdź do treści": "Skip to content",
        "Menu główne": "Main navigation", "Okruszki": "Breadcrumbs",
        "Wybierz język": "Choose language", "Dostępne języki": "Available languages",
        "Poprzednia strona": "Previous page", "Następna strona": "Next page", "zł": "PLN",
    },
    "de": {
        "Strona główna": "Startseite", "Technologia KCAQUA": "KCAQUA-Technologie",
        "Rozwiązania": "Lösungen", "Branże": "Branchen", "Case studies": "Fallstudien",
        "Kalkulator": "Rechner", "Baza wiedzy": "Wissen", "Firma": "Unternehmen",
        "Kontakt": "Kontakt", "Umów darmowy audyt": "Kostenloses Audit",
        "Oferta": "Lösungen", "Usługi": "Leistungen", "Misja firmy": "Unternehmensmission",
        "Model współpracy": "Zusammenarbeit", "Referencje": "Referenzen",
        "Kotły parowe": "Dampfkessel", "Skraplacze wyparne": "Verdunstungskondensatoren",
        "Autoklawy i pasteryzatory": "Autoklaven und Pasteurisierer",
        "Ochrona membran RO": "Schutz von RO-Membranen", "Odkamienianie instalacji": "Anlagenentkalkung",
        "Ochrona antykorozyjna": "Korrosionsschutz", "Audyt techniczny": "Technisches Audit",
        "Analiza wody": "Wasseranalyse", "Serwis i automatyka": "Service und Automatisierung",
        "Białe certyfikaty": "Energieeffizienzzertifikate", "Wiedza": "Wissen",
        "Polityka prywatności": "Datenschutzerklärung", "Oddział w Toruniu": "Niederlassung Toruń",
        "Siedziba główna": "Hauptsitz", "Przejdź do treści": "Zum Inhalt springen",
        "Menu główne": "Hauptnavigation", "Okruszki": "Brotkrümelnavigation",
        "Wybierz język": "Sprache wählen", "Dostępne języki": "Verfügbare Sprachen",
        "Poprzednia strona": "Vorherige Seite", "Następna strona": "Nächste Seite", "zł": "PLN",
    },
    "ar": {
        "Strona główna": "الرئيسية", "Technologia KCAQUA": "تقنية KCAQUA",
        "Rozwiązania": "الحلول", "Branże": "القطاعات", "Case studies": "دراسات الحالة",
        "Kalkulator": "الحاسبة", "Baza wiedzy": "مركز المعرفة", "Firma": "الشركة",
        "Kontakt": "اتصل بنا", "Umów darmowy audyt": "احجز تدقيقًا مجانيًا",
        "Oferta": "الحلول", "Usługi": "الخدمات", "Misja firmy": "رسالة الشركة",
        "Model współpracy": "نموذج التعاون", "Referencje": "المراجع والعملاء",
        "Kotły parowe": "الغلايات البخارية", "Skraplacze wyparne": "المكثفات التبخيرية",
        "Autoklawy i pasteryzatory": "الأوتوكلاف وأجهزة البسترة",
        "Ochrona membran RO": "حماية أغشية التناضح العكسي", "Odkamienianie instalacji": "إزالة التكلسات من الأنظمة",
        "Ochrona antykorozyjna": "الحماية من التآكل", "Audyt techniczny": "تدقيق فني",
        "Analiza wody": "تحليل المياه", "Serwis i automatyka": "الخدمة والأتمتة",
        "Białe certyfikaty": "شهادات كفاءة الطاقة", "Wiedza": "المعرفة",
        "Polityka prywatności": "سياسة الخصوصية", "Oddział w Toruniu": "فرع تورون",
        "Siedziba główna": "المقر الرئيسي", "Przejdź do treści": "الانتقال إلى المحتوى",
        "Menu główne": "التنقل الرئيسي", "Okruszki": "مسار التنقل",
        "Wybierz język": "اختر اللغة", "Dostępne języki": "اللغات المتاحة",
        "Poprzednia strona": "الصفحة السابقة", "Następna strona": "الصفحة التالية", "zł": "PLN",
    },
}

MANUAL["en"].update({
    "Kondycjonowanie wody przemysłowej": "Industrial Water Conditioning",
    "kondycjonowanie wody przemysłowej": "industrial water conditioning",
    "FAQ KABI CHEMIE, pytania o kondycjonowanie wody przemysłowej":
        "KABI CHEMIE FAQ: industrial water conditioning questions",
    "Podajesz firmę, numer telefonu i temat rozmowy.":
        "Provide your company name, phone number and the subject of the call.",
    "Uruchamiamy program KCAQUA, ustawiamy dozowanie, punkty kontroli i sposób reagowania na odchylenia. Zespół zakładu wie, co obserwować.":
        "We launch the KCAQUA programme, configure dosing, monitoring points and the response to deviations. The plant team knows what to monitor.",
    "Czy KCAQUA może pracować z istniejącymi pompami dozującymi?":
        "Can KCAQUA work with existing dosing pumps?",
    "Administratorem danych osobowych jest KABI CHEMIE, Żabokliki-Kolonia, ul. Stocka 10, 08-110 Siedlce, NIP: 8212519774, dalej jako Administrator lub KABI CHEMIE.":
        "The controller of personal data is KABI CHEMIE, Żabokliki-Kolonia, ul. Stocka 10, 08-110 Siedlce, NIP: 8212519774, hereinafter referred to as the Controller or KABI CHEMIE.",
    "Analiza wody przemysłowej i kotłowej | kondycjonowanie-wody.pl": "Industrial and Boiler Water Analysis | kondycjonowanie-wody.pl",
    "Audyt i serwis instalacji uzdatniania - Umów wizytę | kondycjonowanie-wody.pl": "Water Treatment System Audit and Service - Book a Visit | kondycjonowanie-wody.pl",
    "Baza wiedzy o wodzie przemysłowej i KCAQUA | kondycjonowanie-wody.pl": "Industrial Water and KCAQUA Knowledge Base | kondycjonowanie-wody.pl",
    "Biocydy i ochrona wież chłodniczych - Sprawdź preparaty | kondycjonowanie-wody.pl": "Biocides and Cooling Tower Protection - Explore Solutions | kondycjonowanie-wody.pl",
    "Błąd 404: Nie znaleziono strony | kondycjonowanie-wody.pl": "Error 404: Page Not Found | kondycjonowanie-wody.pl",
    "Chemiczne czyszczenie instalacji - Zobacz technologię | kondycjonowanie-wody.pl": "Chemical System Cleaning - Explore the Technology | kondycjonowanie-wody.pl",
    "Czyszczenie skraplacza Evapco (Przetwórstwo) - Czytaj | kondycjonowanie-wody.pl": "Evapco Condenser Cleaning in Processing - Case Study | kondycjonowanie-wody.pl",
    "Inhibitory korozji do kotłów parowych - Sprawdź chemię | kondycjonowanie-wody.pl": "Steam Boiler Corrosion Inhibitors - Explore the Treatment | kondycjonowanie-wody.pl",
    "Kondycjonowanie wody przemysłowej - Sprawdź ofertę | kondycjonowanie-wody.pl": "Industrial Water Conditioning - Explore Our Solutions | kondycjonowanie-wody.pl",
    "Nasi eksperci od kondycjonowania wody - Poznaj zespół | kondycjonowanie-wody.pl": "Our Water Treatment Experts - Meet the Team | kondycjonowanie-wody.pl",
    "Ochrona antykorozyjna instalacji przemysłowych | kondycjonowanie-wody.pl": "Corrosion Protection for Industrial Systems | kondycjonowanie-wody.pl",
    "Odkamienianie instalacji przemysłowych, usuwanie kamienia | kondycjonowanie-wody.pl": "Industrial System Descaling and Scale Removal | kondycjonowanie-wody.pl",
    "Odkamienianie kotła Fako (Case Study) - Zobacz efekty | kondycjonowanie-wody.pl": "Fako Boiler Descaling - Case Study | kondycjonowanie-wody.pl",
    "Odkamienianie kotłów parowych - Zamów specjalistów | kondycjonowanie-wody.pl": "Steam Boiler Descaling - Book a Specialist | kondycjonowanie-wody.pl",
    "Odkamienianie skraplaczy i wież - Zamów czyszczenie | kondycjonowanie-wody.pl": "Condenser and Cooling Tower Descaling - Book Cleaning | kondycjonowanie-wody.pl",
    "Optymalizacja skraplacza BAC - Sprawdź wyniki | kondycjonowanie-wody.pl": "BAC Condenser Optimization - See the Results | kondycjonowanie-wody.pl",
    "Pasywacja stali nierdzewnej i węglowej - Zleć wycenę | kondycjonowanie-wody.pl": "Stainless and Carbon Steel Passivation - Request a Quote | kondycjonowanie-wody.pl",
    "Polityka Prywatności | kondycjonowanie-wody.pl": "Privacy Policy | kondycjonowanie-wody.pl",
    "Realizacje i oszczędności w przemyśle - Sprawdź | kondycjonowanie-wody.pl": "Industrial Projects and Savings - See the Results | kondycjonowanie-wody.pl",
    "Serwis skraplaczy amoniakalnych - Zobacz szczegóły | kondycjonowanie-wody.pl": "Ammonia Condenser Service - View Details | kondycjonowanie-wody.pl",
    "odkamienianie instalacji przemysłowych": "industrial system descaling",
    "Osad i częste czyszczenie ujawniły problem z jakością wody. Odkamieniliśmy kocioł, skorygowaliśmy parametry i uruchomiliśmy KCAQUA 303, aby utrzymać efekt w codziennej pracy.":
        "Deposits and frequent cleaning revealed a water quality problem. We descaled the boiler, adjusted the parameters and launched KCAQUA 303 to maintain the result during daily operation.",
    "Koszt odprowadzenia 1 m³ ścieków.": "Cost to discharge 1 m³ of wastewater.",
    "Koszt zakupu 1 m³ wody.": "Cost to purchase 1 m³ of water.",
    "O₂": "O₂",
    "zł/m³": "PLN/m³",
    "0 zł": "0 PLN",
    "Membrany RO": "RO Membranes",
    "Diagnozujemy instalację": "We diagnose the system",
    "Przebieg współpracy": "How we work",
    "Zapoznaj się z Polityką Prywatności KABI CHEMIE. Dowiedz się, jak bezpiecznie chronimy Twoje dane osobowe w serwisie kondycjonowanie-wody.pl. Przeczytaj.":
        "Read the KABI CHEMIE Privacy Policy and learn how we protect your personal data on kondycjonowanie-wody.pl.",
    "Technologia KCAQUA · chemia, automatyka i monitoring": "KCAQUA technology · treatment chemistry, automation and monitoring",
    "Co zyskuje Twój zakład": "What your plant gains",
    "Mniej wody i niższe koszty ścieków": "Lower water use and wastewater costs",
    "Niższe zużycie energii i paliwa": "Lower energy and fuel consumption",
    "Mniej osadów, korozji i awarii": "Fewer deposits, corrosion issues and failures",
    "Dłuższe cykle między czyszczeniami": "Longer intervals between cleanings",
    "Sprawdź potencjał oszczędności": "Check savings potential",
    "Skontaktuj się z inżynierem": "Contact an engineer",
    "Policz potencjał oszczędności": "Calculate savings potential",
    "wody i energii.": "for water and energy.",
    "Moc cieplna kotła": "Boiler thermal output",
    "Godziny pracy / rok": "Operating hours per year",
    "Cena gazu ziemnego": "Natural gas price",
    "Grubość kamienia": "Scale thickness",
    "Produkcja pary": "Steam production",
    "Moc chłodnicza układu": "System cooling capacity",
    "Cena energii elektr.": "Electricity price",
    "Średnica czystej wężownicy": "Clean coil diameter",
    "Średnica z osadem": "Coil diameter with deposits",
    "zł/MWh": "PLN/MWh",
    "Porozmawiajmy o": "Let's talk about",
    "Państwa instalacji.": "your system.",
})
MANUAL["de"].update({
    "Kondycjonowanie wody przemysłowej": "Industrielle Wasseraufbereitung",
    "kondycjonowanie wody przemysłowej": "industrielle Wasseraufbereitung",
    "FAQ KABI CHEMIE, pytania o kondycjonowanie wody przemysłowej":
        "FAQ von KABI CHEMIE zur industriellen Wasseraufbereitung",
    "Podajesz firmę, numer telefonu i temat rozmowy.":
        "Sie nennen uns Ihr Unternehmen, Ihre Telefonnummer und das Gesprächsthema.",
    "Uruchamiamy program KCAQUA, ustawiamy dozowanie, punkty kontroli i sposób reagowania na odchylenia. Zespół zakładu wie, co obserwować.":
        "Wir nehmen das KCAQUA-Programm in Betrieb, richten Dosierung, Kontrollpunkte und Reaktionen auf Abweichungen ein. Das Betriebsteam weiß, welche Parameter zu überwachen sind.",
    "Czy KCAQUA może pracować z istniejącymi pompami dozującymi?":
        "Kann KCAQUA mit vorhandenen Dosierpumpen betrieben werden?",
    "Administratorem danych osobowych jest KABI CHEMIE, Żabokliki-Kolonia, ul. Stocka 10, 08-110 Siedlce, NIP: 8212519774, dalej jako Administrator lub KABI CHEMIE.":
        "Verantwortlicher für die Verarbeitung personenbezogener Daten ist KABI CHEMIE, Żabokliki-Kolonia, ul. Stocka 10, 08-110 Siedlce, NIP: 8212519774, nachfolgend als Verantwortlicher oder KABI CHEMIE bezeichnet.",
    "Analiza wody przemysłowej i kotłowej | kondycjonowanie-wody.pl": "Analyse von Industrie- und Kesselwasser | kondycjonowanie-wody.pl",
    "Audyt i serwis instalacji uzdatniania - Umów wizytę | kondycjonowanie-wody.pl": "Audit und Service von Wasseraufbereitungsanlagen - Termin vereinbaren | kondycjonowanie-wody.pl",
    "Baza wiedzy o wodzie przemysłowej i KCAQUA | kondycjonowanie-wody.pl": "Wissensdatenbank für Industriewasser und KCAQUA | kondycjonowanie-wody.pl",
    "Biocydy i ochrona wież chłodniczych - Sprawdź preparaty | kondycjonowanie-wody.pl": "Biozide und Kühlturmschutz - Lösungen entdecken | kondycjonowanie-wody.pl",
    "Błąd 404: Nie znaleziono strony | kondycjonowanie-wody.pl": "Fehler 404: Seite nicht gefunden | kondycjonowanie-wody.pl",
    "Chemiczne czyszczenie instalacji - Zobacz technologię | kondycjonowanie-wody.pl": "Chemische Anlagenreinigung - Technologie kennenlernen | kondycjonowanie-wody.pl",
    "Czyszczenie skraplacza Evapco (Przetwórstwo) - Czytaj | kondycjonowanie-wody.pl": "Reinigung eines Evapco-Verflüssigers in der Verarbeitung - Fallstudie | kondycjonowanie-wody.pl",
    "Inhibitory korozji do kotłów parowych - Sprawdź chemię | kondycjonowanie-wody.pl": "Korrosionsinhibitoren für Dampfkessel - Wasserchemie entdecken | kondycjonowanie-wody.pl",
    "Kondycjonowanie wody przemysłowej - Sprawdź ofertę | kondycjonowanie-wody.pl": "Industrielle Wasseraufbereitung - Lösungen entdecken | kondycjonowanie-wody.pl",
    "Nasi eksperci od kondycjonowania wody - Poznaj zespół | kondycjonowanie-wody.pl": "Unsere Experten für Wasseraufbereitung - Team kennenlernen | kondycjonowanie-wody.pl",
    "Ochrona antykorozyjna instalacji przemysłowych | kondycjonowanie-wody.pl": "Korrosionsschutz für Industrieanlagen | kondycjonowanie-wody.pl",
    "Odkamienianie instalacji przemysłowych, usuwanie kamienia | kondycjonowanie-wody.pl": "Entkalkung von Industrieanlagen und Kesselsteinentfernung | kondycjonowanie-wody.pl",
    "Odkamienianie kotła Fako (Case Study) - Zobacz efekty | kondycjonowanie-wody.pl": "Entkalkung eines Fako-Kessels - Fallstudie | kondycjonowanie-wody.pl",
    "Odkamienianie kotłów parowych - Zamów specjalistów | kondycjonowanie-wody.pl": "Entkalkung von Dampfkesseln - Spezialisten beauftragen | kondycjonowanie-wody.pl",
    "Odkamienianie skraplaczy i wież - Zamów czyszczenie | kondycjonowanie-wody.pl": "Entkalkung von Verflüssigern und Kühltürmen - Reinigung beauftragen | kondycjonowanie-wody.pl",
    "Optymalizacja skraplacza BAC - Sprawdź wyniki | kondycjonowanie-wody.pl": "Optimierung eines BAC-Verflüssigers - Ergebnisse ansehen | kondycjonowanie-wody.pl",
    "Pasywacja stali nierdzewnej i węglowej - Zleć wycenę | kondycjonowanie-wody.pl": "Passivierung von Edelstahl und Kohlenstoffstahl - Angebot anfordern | kondycjonowanie-wody.pl",
    "Polityka Prywatności | kondycjonowanie-wody.pl": "Datenschutzerklärung | kondycjonowanie-wody.pl",
    "Realizacje i oszczędności w przemyśle - Sprawdź | kondycjonowanie-wody.pl": "Industrieprojekte und Einsparungen - Ergebnisse ansehen | kondycjonowanie-wody.pl",
    "Serwis skraplaczy amoniakalnych - Zobacz szczegóły | kondycjonowanie-wody.pl": "Service für Ammoniak-Verflüssiger - Details ansehen | kondycjonowanie-wody.pl",
    "odkamienianie instalacji przemysłowych": "Entkalkung von Industrieanlagen",
    "Osad i częste czyszczenie ujawniły problem z jakością wody. Odkamieniliśmy kocioł, skorygowaliśmy parametry i uruchomiliśmy KCAQUA 303, aby utrzymać efekt w codziennej pracy.":
        "Ablagerungen und häufige Reinigungen wiesen auf ein Problem mit der Wasserqualität hin. Wir entkalkten den Kessel, korrigierten die Parameter und nahmen KCAQUA 303 in Betrieb, um das Ergebnis im täglichen Betrieb zu sichern.",
    "418 tys. zł": "418 Tsd. PLN",
    "Koszt odprowadzenia 1 m³ ścieków.": "Kosten für die Ableitung von 1 m³ Abwasser.",
    "Koszt zakupu 1 m³ wody.": "Kosten für den Bezug von 1 m³ Wasser.",
    "O₂": "O₂",
    "zł/m³": "PLN/m³",
    "Ponad dwadzieścia sześć firm w bazie doświadczeń": "Mehr als sechsundzwanzig Unternehmen in unserer Projektdatenbank",
    "Żabokliki-Kolonia ul. Stocka 10": "Żabokliki-Kolonia, ul. Stocka 10",
    "0 zł": "0 PLN",
    "Business Development Manager": "Leiter Geschäftsentwicklung",
    "Diagnozujemy instalację": "Wir diagnostizieren die Anlage",
    "Przebieg współpracy": "Ablauf der Zusammenarbeit",
    "Zapoznaj się z Polityką Prywatności KABI CHEMIE. Dowiedz się, jak bezpiecznie chronimy Twoje dane osobowe w serwisie kondycjonowanie-wody.pl. Przeczytaj.":
        "Lesen Sie die Datenschutzerklärung von KABI CHEMIE und erfahren Sie, wie wir Ihre personenbezogenen Daten auf kondycjonowanie-wody.pl schützen.",
    "Technologia KCAQUA · chemia, automatyka i monitoring": "KCAQUA-Technologie · Wasserchemie, Automatisierung und Monitoring",
    "Co zyskuje Twój zakład": "Vorteile für Ihren Betrieb",
    "Mniej wody i niższe koszty ścieków": "Weniger Wasserverbrauch und Abwasserkosten",
    "Niższe zużycie energii i paliwa": "Geringerer Energie- und Brennstoffverbrauch",
    "Mniej osadów, korozji i awarii": "Weniger Ablagerungen, Korrosion und Ausfälle",
    "Dłuższe cykle między czyszczeniami": "Längere Intervalle zwischen den Reinigungen",
    "Sprawdź potencjał oszczędności": "Einsparpotenzial prüfen",
    "Skontaktuj się z inżynierem": "Ingenieur kontaktieren",
    "Policz potencjał oszczędności": "Einsparpotenzial berechnen",
    "wody i energii.": "bei Wasser und Energie.",
    "Moc cieplna kotła": "Thermische Kesselleistung",
    "Godziny pracy / rok": "Betriebsstunden pro Jahr",
    "Cena gazu ziemnego": "Erdgaspreis",
    "Grubość kamienia": "Kesselsteinschichtdicke",
    "Produkcja pary": "Dampfproduktion",
    "Moc chłodnicza układu": "Kälteleistung der Anlage",
    "Cena energii elektr.": "Strompreis",
    "Średnica czystej wężownicy": "Durchmesser der sauberen Rohrschlange",
    "Średnica z osadem": "Rohrschlangendurchmesser mit Ablagerungen",
    "zł/MWh": "PLN/MWh",
    "Porozmawiajmy o": "Sprechen wir über",
    "Państwa instalacji.": "Ihre Anlage.",
})
MANUAL["ar"].update({
    "Kondycjonowanie wody przemysłowej": "معالجة المياه الصناعية",
    "kondycjonowanie wody przemysłowej": "معالجة المياه الصناعية",
    "FAQ KABI CHEMIE, pytania o kondycjonowanie wody przemysłowej":
        "الأسئلة الشائعة حول معالجة المياه الصناعية من KABI CHEMIE",
    "Podajesz firmę, numer telefonu i temat rozmowy.":
        "تزوّدنا باسم الشركة ورقم الهاتف وموضوع المكالمة.",
    "Uruchamiamy program KCAQUA, ustawiamy dozowanie, punkty kontroli i sposób reagowania na odchylenia. Zespół zakładu wie, co obserwować.":
        "نُشغّل برنامج KCAQUA، ونضبط الجرعات ونقاط المراقبة وآلية الاستجابة للانحرافات. وبذلك يعرف فريق المنشأة ما يجب مراقبته.",
    "Analiza wody przemysłowej i kotłowej | kondycjonowanie-wody.pl":
        "تحليل المياه الصناعية ومياه الغلايات | kondycjonowanie-wody.pl",
    "Audyt i serwis instalacji uzdatniania - Umów wizytę | kondycjonowanie-wody.pl":
        "تدقيق وصيانة أنظمة معالجة المياه - احجز زيارة | kondycjonowanie-wody.pl",
    "Baza wiedzy o wodzie przemysłowej i KCAQUA | kondycjonowanie-wody.pl":
        "قاعدة المعرفة بالمياه الصناعية وتقنية KCAQUA | kondycjonowanie-wody.pl",
    "Biocydy i ochrona wież chłodniczych - Sprawdź preparaty | kondycjonowanie-wody.pl":
        "المبيدات الحيوية وحماية أبراج التبريد - تعرّف على الحلول | kondycjonowanie-wody.pl",
    "Błąd 404: Nie znaleziono strony | kondycjonowanie-wody.pl":
        "خطأ 404: الصفحة غير موجودة | kondycjonowanie-wody.pl",
    "Chemiczne czyszczenie instalacji - Zobacz technologię | kondycjonowanie-wody.pl":
        "التنظيف الكيميائي للأنظمة الصناعية - تعرّف على التقنية | kondycjonowanie-wody.pl",
    "Czyszczenie skraplacza Evapco (Przetwórstwo) - Czytaj | kondycjonowanie-wody.pl":
        "تنظيف مكثف Evapco في قطاع التصنيع - اقرأ دراسة الحالة | kondycjonowanie-wody.pl",
    "Inhibitory korozji do kotłów parowych - Sprawdź chemię | kondycjonowanie-wody.pl":
        "مثبطات التآكل للغلايات البخارية - تعرّف على المعالجة | kondycjonowanie-wody.pl",
    "Kondycjonowanie wody przemysłowej - Sprawdź ofertę | kondycjonowanie-wody.pl":
        "معالجة المياه الصناعية - تعرّف على حلولنا | kondycjonowanie-wody.pl",
    "Nasi eksperci od kondycjonowania wody - Poznaj zespół | kondycjonowanie-wody.pl":
        "خبراؤنا في معالجة المياه - تعرّف على الفريق | kondycjonowanie-wody.pl",
    "Ochrona antykorozyjna instalacji przemysłowych | kondycjonowanie-wody.pl":
        "حماية الأنظمة الصناعية من التآكل | kondycjonowanie-wody.pl",
    "Odkamienianie instalacji przemysłowych, usuwanie kamienia | kondycjonowanie-wody.pl":
        "إزالة الترسّبات الكلسية من الأنظمة الصناعية | kondycjonowanie-wody.pl",
    "Odkamienianie kotła Fako (Case Study) - Zobacz efekty | kondycjonowanie-wody.pl":
        "إزالة الترسّبات من غلاية Fako - دراسة حالة | kondycjonowanie-wody.pl",
    "Odkamienianie kotłów parowych - Zamów specjalistów | kondycjonowanie-wody.pl":
        "إزالة الترسّبات من الغلايات البخارية - اطلب خدمة متخصصة | kondycjonowanie-wody.pl",
    "Odkamienianie skraplaczy i wież - Zamów czyszczenie | kondycjonowanie-wody.pl":
        "إزالة الترسّبات من المكثفات وأبراج التبريد - اطلب التنظيف | kondycjonowanie-wody.pl",
    "Optymalizacja skraplacza BAC - Sprawdź wyniki | kondycjonowanie-wody.pl":
        "تحسين أداء مكثف BAC - اطّلع على النتائج | kondycjonowanie-wody.pl",
    "Pasywacja stali nierdzewnej i węglowej - Zleć wycenę | kondycjonowanie-wody.pl":
        "تخميل الفولاذ المقاوم للصدأ والفولاذ الكربوني - اطلب عرض سعر | kondycjonowanie-wody.pl",
    "Polityka Prywatności | kondycjonowanie-wody.pl":
        "سياسة الخصوصية | kondycjonowanie-wody.pl",
    "Realizacje i oszczędności w przemyśle - Sprawdź | kondycjonowanie-wody.pl":
        "مشروعات ناجحة ووفورات صناعية - اطّلع على النتائج | kondycjonowanie-wody.pl",
    "Serwis skraplaczy amoniakalnych - Zobacz szczegóły | kondycjonowanie-wody.pl":
        "صيانة مكثفات الأمونيا - اطّلع على التفاصيل | kondycjonowanie-wody.pl",
    "Artykuły o kamieniu, korozji, biofilmie, membranach RO i parametrach wody. Konkretne przyczyny, pomiary i działania dla zakładu przemysłowego.":
        "مقالات حول الترسّبات الكلسية والتآكل والغشاء الحيوي وأغشية التناضح العكسي RO ومعايير المياه. أسباب وقياسات وإجراءات محددة للمنشآت الصناعية.",
    "Czytaj o kamieniu, korozji, biofilmie, membranach RO i parametrach wody. Wiedza dla utrzymania ruchu, energetyki i zakładów produkcyjnych.":
        "اقرأ عن الترسّبات الكلسية والتآكل والغشاء الحيوي وأغشية التناضح العكسي RO ومعايير المياه. معلومات عملية للصيانة التشغيلية وقطاع الطاقة والمنشآت الإنتاجية.",
    "Warto sprawdzić zakamienienie i odsalanie, aby określić możliwość ograniczenia kosztów.":
        "يجدر فحص مستوى الترسّبات الكلسية ونظام التصريف لتحديد إمكانات خفض التكاليف.",
    "Czy można kondycjonować wodę bez wyłączania kotła?":
        "هل يمكن معالجة المياه من دون إيقاف الغلاية؟",
    "Kompleksowe kondycjonowanie skraplaczy amoniakalnych. Zapewniamy ochronę przed osadami, profesjonalny serwis i ciągłość produkcji. Sprawdź nasze usługi!":
        "معالجة متكاملة لمكثفات الأمونيا. نوفر الحماية من الرواسب والصيانة المتخصصة واستمرارية الإنتاج. تعرّف على خدماتنا.",
    "kondycjonowania": "معالجة المياه",
    "Kondycjonowanie": "معالجة المياه",
    "Kondycjonowanie układów chłodniczych": "معالجة المياه في دوائر التبريد",
    "Po czyszczeniu dobieramy program kondycjonowania i ustalamy zakres kontroli wody. Dzięki temu ograniczamy warunki, które sprzyjały tworzeniu osadu przed interwencją.":
        "بعد التنظيف، نختار برنامج معالجة المياه ونحدد نطاق مراقبة جودة المياه. وبذلك نحد من الظروف التي كانت تؤدي إلى تكوّن الرواسب قبل التدخل.",
    "Poznaj efekty dozowania KCAQUA 305 w skraplaczu BAC. Skuteczne kondycjonowanie, mniejsze zużycie wody i brak kamienia. Sprawdź szczegóły wdrożenia!":
        "تعرّف على نتائج جرعات KCAQUA 305 في مكثف BAC. معالجة فعالة للمياه، واستهلاك أقل للمياه، ومنع للترسّبات الكلسية. اطّلع على تفاصيل التنفيذ.",
    "Program został dopasowany do jakości wody, materiałów instalacji i zmiennego obciążenia chłodzenia.":
        "تمت مواءمة البرنامج مع جودة المياه ومواد النظام وتغيّر أحمال التبريد.",
    "Tak, samo kondycjonowanie prowadzimy w trakcie pracy. Odkamienianie planujemy zależnie od stanu układu.":
        "نعم، ننفذ معالجة المياه أثناء التشغيل. ونخطط لإزالة الترسّبات الكلسية وفقًا لحالة النظام.",
    "Wdrożenie kondycjonowania, by kamień nie wracał":
        "تطبيق برنامج معالجة المياه لمنع عودة الترسّبات الكلسية",
    "Neutralizujemy pozostałości, potwierdzamy parametry końcowe i przygotowujemy zalecenia po uruchomieniu.":
        "نعادل البقايا الكيميائية، ونتحقق من المعايير النهائية، ونعدّ توصيات ما بعد التشغيل.",
    "O demontażu, doborze chemii, kontroli prac, neutralizacji i ograniczeniu ponownego narastania osadu.":
        "حول التفكيك واختيار المواد الكيميائية ومراقبة الأعمال والمعادلة الكيميائية والحد من إعادة تكوّن الرواسب.",
    "Czy obsługujecie skraplacze amoniakalne BAC i EVAPCO?":
        "هل تقدمون خدمات لمكثفات الأمونيا BAC وEVAPCO؟",
    "Najważniejsze wnioski dla osób, które odpowiadają za skraplacze wyparne, zużycie wody i stabilną pracę instalacji amoniakalnej.":
        "أهم الاستنتاجات للمسؤولين عن المكثفات التبخيرية واستهلاك المياه واستقرار تشغيل نظام الأمونيا.",
    "Obiegi amoniakalne": "دوائر الأمونيا",
    "Serwis i kondycjonowanie skraplaczy amoniakalnych": "صيانة ومعالجة مياه مكثفات الأمونيا",
    "Skraplacze amoniakalne": "مكثفات الأمونيا",
    "O diagnozie, inhibitorach, pasywacji, pomiarach i ocenie skuteczności programu.":
        "حول التشخيص ومثبطات التآكل والتخميل والقياسات وتقييم فعالية البرنامج.",
    "Kotłownie parowe": "غرف الغلايات البخارية",
    "Wynik sumuje dwa składniki: koszt energii traconej przez kamień lub osad oraz potencjał wynikający z ograniczenia odsalania, czyli zużycia wody, ścieków, a w kotle także strat ciepła. Pokazuje wartość dla podanych godzin pracy i cen mediów, a nie gwarantowaną kwotę oszczędności.":
        "تجمع النتيجة عنصرين: تكلفة الطاقة المفقودة بسبب الترسّبات الكلسية أو الرواسب، والإمكانات الناتجة عن تقليل التصريف، أي استهلاك المياه ومياه الصرف، إضافة إلى فاقد الحرارة في الغلاية. وهي تعرض قيمة محسوبة وفق ساعات التشغيل وأسعار المرافق المدخلة، وليست مبلغًا مضمونًا للوفورات.",
    "To zależy od rodzaju instalacji, jakości wody i obecnie stosowanego programu chemicznego. W wybranych przypadkach oszczędności wody i energii sięgają nawet 70%.":
        "يعتمد ذلك على نوع النظام وجودة المياه وبرنامج المعالجة الكيميائية المستخدم حاليًا. في بعض الحالات، يمكن أن تصل وفورات المياه والطاقة إلى 70%.",
    "3 mies.": "3 أشهر",
    "7 min": "7 دقائق",
    "8 °n": "8 °n",
    "KABI CHEMIE Water Treatment": "KABI CHEMIE لمعالجة المياه",
    "KABI CHEMIE · water treatment": "KABI CHEMIE · معالجة المياه",
    "Art. 6 ust. 1 lit. f RODO.": "المادة 6، الفقرة 1، الحرف (f) من اللائحة العامة لحماية البيانات (GDPR).",
    "Ponad dwadzieścia sześć firm w bazie doświadczeń": "أكثر من ست وعشرين شركة في قاعدة خبراتنا",
    "Administratorem danych osobowych jest KABI CHEMIE, Żabokliki-Kolonia, ul. Stocka 10, 08-110 Siedlce, NIP: 8212519774, dalej jako Administrator lub KABI CHEMIE.":
        "المتحكم في البيانات الشخصية هو KABI CHEMIE، Żabokliki-Kolonia، ul. Stocka 10، 08-110 Siedlce، NIP: 8212519774، ويشار إليه فيما بعد باسم المتحكم أو KABI CHEMIE.",
    "© 2026 KABI CHEMIE. Wszelkie prawa zastrzeżone.": "© 2026 KABI CHEMIE. جميع الحقوق محفوظة.",
    "4200 µS": "4200 µS",
    "Zapoznaj się z Polityką Prywatności KABI CHEMIE. Dowiedz się, jak bezpiecznie chronimy Twoje dane osobowe w serwisie kondycjonowanie-wody.pl. Przeczytaj.":
        "اطّلع على سياسة الخصوصية لدى KABI CHEMIE وتعرّف على كيفية حماية بياناتك الشخصية على kondycjonowanie-wody.pl.",
    "Technologia KCAQUA · chemia, automatyka i monitoring": "تقنية KCAQUA · المعالجة الكيميائية والأتمتة والمراقبة",
    "Co zyskuje Twój zakład": "ما الذي تستفيده منشأتك",
    "Mniej wody i niższe koszty ścieków": "استهلاك أقل للمياه وتكاليف أقل لمياه الصرف",
    "Niższe zużycie energii i paliwa": "استهلاك أقل للطاقة والوقود",
    "Mniej osadów, korozji i awarii": "رواسب وتآكل وأعطال أقل",
    "Dłuższe cykle między czyszczeniami": "فترات أطول بين عمليات التنظيف",
    "Sprawdź potencjał oszczędności": "اكتشف إمكانات التوفير",
    "Skontaktuj się z inżynierem": "تواصل مع مهندس",
    "Policz potencjał oszczędności": "احسب إمكانات التوفير",
    "wody i energii.": "في المياه والطاقة.",
    "Moc cieplna kotła": "القدرة الحرارية للغلاية",
    "Godziny pracy / rok": "ساعات التشغيل سنويًا",
    "Cena gazu ziemnego": "سعر الغاز الطبيعي",
    "Grubość kamienia": "سماكة الترسّبات الكلسية",
    "Produkcja pary": "إنتاج البخار",
    "Moc chłodnicza układu": "قدرة التبريد للنظام",
    "Cena energii elektr.": "سعر الكهرباء",
    "Średnica czystej wężownicy": "قطر ملف التبادل الحراري النظيف",
    "Średnica z osadem": "قطر الملف مع الرواسب",
    "zł/MWh": "PLN/MWh",
    "Porozmawiajmy o": "لنتحدث عن",
    "Państwa instalacji.": "منشأتك.",
    "Firma / imię i nazwisko": "الشركة / الاسم الكامل",
    "Telefon": "رقم الهاتف",
    "Adres e-mail": "البريد الإلكتروني",
    "Wiadomość": "الرسالة",
    "Zgadzam się na kontakt w sprawie zapytania zgodnie z": "أوافق على أن يتم التواصل معي بشأن استفساري وفقًا لـ",
    "Wyślij wiadomość": "إرسال الرسالة",
})

# Semantic image and organization metadata added during the SEO/GEO audit.
MANUAL["en"].update({
    "Łukasz Mielcarz, prezes KABI CHEMIE": "Łukasz Mielcarz, President of KABI CHEMIE",
    "Przemysław Jesiołkowski, członek zarządu KABI CHEMIE": "Przemysław Jesiołkowski, Member of the Management Board of KABI CHEMIE",
    "Łukasz Kumor, Business Development Manager w KABI CHEMIE": "Łukasz Kumor, Business Development Manager at KABI CHEMIE",
    "Inżynier analizujący dane pracy przemysłowej instalacji wodnej": "Engineer analysing operating data from an industrial water system",
    "mazowieckie": "Masovian Voivodeship",
})
MANUAL["de"].update({
    "Łukasz Mielcarz, prezes KABI CHEMIE": "Łukasz Mielcarz, Geschäftsführer von KABI CHEMIE",
    "Przemysław Jesiołkowski, członek zarządu KABI CHEMIE": "Przemysław Jesiołkowski, Vorstandsmitglied von KABI CHEMIE",
    "Łukasz Kumor, Business Development Manager w KABI CHEMIE": "Łukasz Kumor, Business Development Manager bei KABI CHEMIE",
    "Inżynier analizujący dane pracy przemysłowej instalacji wodnej": "Ingenieur bei der Analyse von Betriebsdaten einer industriellen Wasseranlage",
    "mazowieckie": "Woiwodschaft Masowien",
})
MANUAL["ar"].update({
    "Łukasz Mielcarz, prezes KABI CHEMIE": "Łukasz Mielcarz، رئيس شركة KABI CHEMIE",
    "Przemysław Jesiołkowski, członek zarządu KABI CHEMIE": "Przemysław Jesiołkowski، عضو مجلس إدارة شركة KABI CHEMIE",
    "Łukasz Kumor, Business Development Manager w KABI CHEMIE": "Łukasz Kumor، مدير تطوير الأعمال في KABI CHEMIE",
    "Inżynier analizujący dane pracy przemysłowej instalacji wodnej": "مهندس يحلل بيانات تشغيل منظومة مياه صناعية",
    "mazowieckie": "محافظة مازوفيا",
})

for source, (english, german, arabic) in AUTOKLAW_TRANSLATIONS.items():
    MANUAL["en"][source] = english
    MANUAL["de"][source] = german
    MANUAL["ar"][source] = arabic

for language, translations in REVIEWED_TRANSLATIONS.items():
    MANUAL[language].update(translations)

AR_GLOSSARY = [
    (r"\bodkamienianie\s+kotłów\s+parowych\b", "إزالة الترسّبات الكلسية من الغلايات البخارية"),
    (r"\bodkamienianie\s+instalacji\s+przemysłowych\b", "إزالة الترسّبات الكلسية من الأنظمة الصناعية"),
    (r"\bodkamienianie\s+skraplaczy\b", "إزالة الترسّبات الكلسية من المكثفات"),
    (r"\bchemiczne\s+czyszczenie\s+autoklawów\s+i\s+wózków\s+technologicznych\b", "التنظيف الكيميائي للأوتوكلافات والعربات الصناعية"),
    (r"\bpasywacja\s+stali\s+nierdzewnej\s+i\s+węglowej\b", "تخميل الفولاذ المقاوم للصدأ والفولاذ الكربوني"),
    (r"\bochron(?:a|y|ę|ie|ą)\s+przed\s+kamieniem\b", "الحماية من الترسّبات الكلسية"),
    (r"\bochron(?:a|y|ę|ie|ą)\s+przed\s+korozją\b", "الحماية من التآكل"),
    (r"\bryzyko\s+kamienia\b", "مخاطر الترسّبات الكلسية"),
    (r"\busuwamy\s+kamień\b", "نزيل الترسّبات الكلسية"),
    (r"\brozpuszczamy\s+kamień\b", "نذيب الترسّبات الكلسية"),
    (r"\bmniej\s+kamienia\b", "ترسّبات كلسية أقل"),
    (r"\bbez\s+kamienia\b", "من دون ترسّبات كلسية"),
    (r"\bpowierzchni(?:a|ę|y|ą)\s+wymiany\s+ciepła\b", "سطح انتقال الحرارة"),
    (r"\bczyszczeni(?:e|a|u|em)\s+chemiczn(?:e|ego|ym)\b", "التنظيف الكيميائي"),
    (r"\bproces(?:y|u|em|ie)?\s+chemiczn(?:y|e|ych|ego|ym)\b", "عملية المعالجة الكيميائية"),
    (r"\bbiał(?:a|ej|ą)\s+korozj(?:a|i|ę|ą)\b", "التآكل الأبيض"),
    (r"\bkamie(?:ń|nia|niem|niowi)\s+kotłow(?:y|ego|ym)\b", "الترسّبات الكلسية في الغلاية"),
    (r"\bodkamienian(?:ie|ia|iu|iem)\b", "إزالة الترسّبات الكلسية"),
    (r"\bodkamieni(?:amy|enie|enia|ać)\b", "إزالة الترسّبات الكلسية"),
    (r"\bkamie(?:ń|nia|niem|niowi)\b", "الترسّبات الكلسية"),
    (r"\bkondycjonowani(?:e|a|u|em)\s+wod(?:y|ę|zie)\b", "معالجة المياه"),
    (r"\bkondycjonujemy\s+wodę\b", "نعالج المياه"),
    (r"\buzdatniani(?:e|a|u|em)\s+wod(?:y|ę|zie)\b", "معالجة المياه"),
    (r"\bkotł(?:y|ów|om|ami)\s+parow(?:e|ych|ym|ymi)\b", "الغلايات البخارية"),
    (r"\bkotł(?:a|owi|em)\s+parow(?:ego|emu|ym)\b", "الغلاية البخارية"),
    (r"\bkocioł\s+parowy\b", "الغلاية البخارية"),
    (r"\bkotłowni(?:a|ę|ą|i)\b", "غرفة الغلايات"),
    (r"\bkotłow(?:y|a|e|ej|ego|ą|ym)\b", "خاص بالغلاية"),
    (r"\bkotł(?:y|ów|a|em|owi)\b", "الغلايات"),
    (r"\bskraplacz(?:e|y|a|ach|ami|om)\s+wyparn(?:e|ych|ym|ymi)\b", "المكثفات التبخيرية"),
    (r"\bskraplacz(?:a|owi|em)\b", "المكثف"),
    (r"\bskraplacz(?:e|y|ach|ami|om)\b", "المكثفات"),
    (r"\bskraplacz\b", "المكثف"),
    (r"\bchłodnictw(?:o|a|ie|em)\s+przemysłow(?:e|ego|ym)\b", "التبريد الصناعي"),
    (r"\bukład(?:y|ów|zie|ach|ami)?\s+chłodnicz(?:y|e|ych|ym|ymi)\b", "دائرة التبريد"),
    (r"\bobieg(?:i|ów|u|ach|ami)?\s+chłodnicz(?:y|e|ych|ym|ymi)\b", "دائرة التبريد"),
    (r"\bwież(?:a|e|y|ach|ami)\s+chłodnicz(?:a|e|ych|ymi)\b", "أبراج التبريد"),
    (r"\bchłodni(?:a|e|ach|ami)\b", "أبراج التبريد"),
    (r"\bchłodnictw(?:o|a|ie|em)\b", "التبريد"),
    (r"\bkorozj(?:a|i|ę|ą)\b", "التآكل"),
    (r"\bantykorozyjn(?:y|a|e|ej|ego|ą|ym|ych)\b", "المضاد للتآكل"),
    (r"\binhibitor(?:y|ów|a|ami|om)?\s+korozji\b", "مثبطات التآكل"),
    (r"\binhibitor(?:y|ów|a|ami|om)?\b", "المثبطات"),
    (r"\bpasywacj(?:a|i|ę|ą)\b", "التخميل"),
    (r"\bpasywujemy\b", "نُجري التخميل"),
    (r"\bautoklaw(?:y|ów|ach|ami|om|u)?\b", "الأوتوكلافات"),
    (r"\bwózk(?:i|ów|ach|ami|om)\s+technologiczn(?:e|ych|ym|ymi)\b", "العربات الصناعية"),
    (r"\bbiocyd(?:y|ów|ach|ami|om)?\b", "المبيدات الحيوية"),
    (r"\bbiofilm(?:u|em|owi)?\b", "الغشاء الحيوي"),
    (r"\bosad(?:y|ów|u|em|ach|ami|om)?\b", "الرواسب"),
    (r"\bzłog(?:i|ów|u|iem|ach|ami|om)?\b", "الرواسب"),
    (r"\binstalacj(?:a|e|i|ę|ą|ach|ami|om)\b", "النظام"),
    (r"\bzakład(?:y|ów|u|em|zie|ach|ami|om)?\b", "المنشأة الصناعية"),
    (r"\bwymiennik(?:i|ów|a|u|iem|ach|ami|om)?\b", "المبادلات الحرارية"),
    (r"\brurociąg(?:i|ów|u|iem|ach|ami|om)?\b", "الأنابيب"),
    (r"\bwężownic(?:a|e|y|ę|ą|ach|ami)\b", "ملفات التبادل الحراري"),
    (r"\bawari(?:a|e|i|ę|ą|ach|ami|om)\b", "الأعطال"),
    (r"\bprzepływ(?:y|ów|u|em|ie|ach|ami|om)?\b", "التدفق"),
    (r"\bdozowani(?:e|a|u|em)\b", "الجرعات"),
    (r"\bautomatyk(?:a|i|ę|ą)\b", "أنظمة التحكم الآلي"),
    (r"\bmonitoring(?:u|iem|owi)?\b", "المراقبة"),
    (r"\butrzymani(?:e|a|u|em)\s+ruchu\b", "الصيانة التشغيلية"),
    (r"\bprzypaleni(?:a|e|u|em)\b", "الرواسب المحترقة"),
    (r"\btłuszcz(?:e|ów|u|em|ach|ami|om)?\b", "الدهون"),
    (r"\bmikrobiologi(?:a|i|ę|ą)\b", "الأحياء الدقيقة"),
    (r"\bpar(?:a|y|ę|ze|ą)\b", "البخار"),
    (r"\bpaliw(?:o|a|em|ie)\b", "الوقود"),
    (r"\bodsalani(?:e|a|u|em)\b", "التصريف"),
    (r"\bwod(?:a|y|ę|zie|ą)\s+kotłow(?:a|ej|ą)\b", "مياه الغلاية"),
    (r"\bwod(?:a|y|ę|zie|ą)\s+zasilając(?:a|ej|ą)\b", "مياه التغذية"),
    (r"\bwod(?:a|y|ę|zie|ą)\s+uzupełniając(?:a|ej|ą)\b", "مياه التعويض"),
    (r"\bprzewodnoś(?:ć|ci|cią)\b", "الموصلية الكهربائية"),
    (r"\btwardoś(?:ć|ci|cią)\b", "عسر المياه"),
    (r"\bzasadowoś(?:ć|ci|cią)\b", "القلوية"),
    (r"\bchlork(?:i|ów|ami|om)\b", "الكلوريدات"),
    (r"\bwymian(?:a|y|ę|ie|ą)\s+ciepła\b", "انتقال الحرارة"),
    (r"\bmembran(?:a|y|ę|ie|ą|ach|ami)\s+RO\b", "أغشية التناضح العكسي RO"),
    (r"\bantyskalant(?:y|ów|u|em|ach|ami)?\b", "مانع الترسّب"),
    (r"\bprogram(?:y|ów|u|em|ie)?\s+chemiczn(?:y|e|ych|ego|ym|ymi)\b", "برنامج المعالجة الكيميائية"),
    (r"\bpreparat(?:y|ów|u|em|ach|ami)?\b", "مواد المعالجة الكيميائية"),
    (r"\bściek(?:i|ów|om|ami|ach)\b", "مياه الصرف"),
    (r"\baudyt(?:u|em|owi)?\s+techniczn(?:y|ego|ym)\b", "التدقيق الفني"),
    (r"\banaliz(?:a|y|ę|ie|ą)\s+wod(?:y|ę)\b", "تحليل المياه"),
    (r"\bRODO\b", "اللائحة العامة لحماية البيانات (GDPR)"),
]

HERO_LEAD = {
    "en": (
        "We design water treatment and conditioning programmes for steam boilers, "
        "evaporative condensers and industrial cooling circuits. KCAQUA technology "
        "combines treatment chemistry, dosing automation and monitoring to reduce water "
        "and energy consumption, corrosion, deposits and system failures."
    ),
    "de": (
        "Wir entwickeln Programme zur Wasseraufbereitung und Wasserkonditionierung für "
        "Dampfkessel, Verdunstungskondensatoren und industrielle Kühlkreisläufe. Die "
        "KCAQUA-Technologie verbindet Wasserchemie, Dosierautomatisierung und Monitoring, "
        "um den Wasser- und Energieverbrauch sowie Korrosion, Ablagerungen und "
        "Anlagenausfälle zu reduzieren."
    ),
    "ar": (
        "نصمم برامج لمعالجة المياه للغلايات البخارية والمكثفات التبخيرية ودوائر التبريد "
        "الصناعية. تجمع تقنية KCAQUA بين المعالجة الكيميائية وأتمتة الجرعات والمراقبة "
        "للحد من استهلاك المياه والطاقة والتآكل والرواسب وأعطال الأنظمة."
    ),
}


def source_pages() -> list[Path]:
    pages = []
    for path in sorted(WWW.rglob("*.html")):
        rel = path.relative_to(WWW)
        if rel.parts and rel.parts[0] in LANGS:
            continue
        pages.append(path)
    return pages


def route_for(path: Path) -> str:
    rel = path.relative_to(WWW).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-10]
    return "/" + rel


def localized_route(lang: str, route: str) -> str:
    return f"/{lang}{route}"


def is_inside_language_switch(element) -> bool:
    return bool(element.xpath("ancestor-or-self::*[contains(concat(' ', normalize-space(@class), ' '), ' language-switch ')]"))


def should_translate(value: str) -> bool:
    text = " ".join(value.split())
    if not text or text in PRESERVE_EXACT or text in {"Polski", "English", "Deutsch", "العربية"}:
        return False
    if URL_OR_EMAIL_RE.search(text):
        return False
    return any(char.isalpha() for char in text)


def should_translate_js(value: str) -> bool:
    return should_translate(value) and (bool(POLISH_WORDS.search(value)) or bool(re.search(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", value)))


def parse_page(path: Path):
    parser = html.HTMLParser(encoding="utf-8", remove_comments=False)
    return html.document_fromstring(path.read_bytes(), parser=parser)


def collect_json_strings(value, key: str | None, out: set[str]) -> None:
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            collect_json_strings(child_value, child_key, out)
    elif isinstance(value, list):
        for child in value:
            collect_json_strings(child, key, out)
    elif isinstance(value, str) and key not in JSON_SKIP_KEYS and key not in {"inLanguage", "availableLanguage"}:
        if should_translate(value):
            out.add(" ".join(value.split()))


def collect_page_strings(doc) -> set[str]:
    strings: set[str] = set()
    for node in doc.xpath("//text()[normalize-space()]"):
        parent = node.getparent()
        if parent is None or parent.tag in SKIP_TAGS or is_inside_language_switch(parent):
            continue
        value = " ".join(str(node).split())
        if should_translate(value):
            strings.add(value)
    for element in doc.iter():
        if not isinstance(element.tag, str) or is_inside_language_switch(element):
            continue
        for attr in ("alt", "title", "aria-label", "placeholder"):
            value = element.get(attr)
            if value and should_translate(value):
                strings.add(" ".join(value.split()))
        if element.tag == "input" and element.get("type") in {"submit", "button"}:
            value = element.get("value")
            if value and should_translate(value):
                strings.add(" ".join(value.split()))
        if element.tag == "meta" and element.get("content"):
            key = element.get("name") or element.get("property") or ""
            if key in META_KEYS and should_translate(element.get("content")):
                strings.add(" ".join(element.get("content").split()))
    for script in doc.xpath('//script[@type="application/ld+json"]'):
        try:
            collect_json_strings(json.loads(script.text or ""), None, strings)
        except json.JSONDecodeError:
            pass
    return strings


def js_literal_value(token: str) -> str:
    body = token[1:-1]
    body = body.replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t")
    body = body.replace("\\\"", "\"").replace("\\'", "'").replace("\\\\", "\\")
    return body


def collect_js_strings() -> set[str]:
    source = (WWW / "assets" / "main.js").read_text(encoding="utf-8")
    strings = set()
    for token in JS_STRING_RE.findall(source):
        value = js_literal_value(token)
        if should_translate_js(value):
            strings.add(value)
    return strings


def protect_value(
    value: str,
    glossary: list[tuple[str, str]] | None = None,
) -> tuple[str, dict[str, str]]:
    keep: dict[str, str] = {}
    protected = value
    for expression, translation in glossary or []:
        pattern = re.compile(expression, re.IGNORECASE)
        if not pattern.search(protected):
            continue
        marker = f"https://keep.invalid/K{len(keep):03d}"
        protected = pattern.sub(marker, protected)
        keep[marker] = translation
    fixed = sorted(PRESERVE_EXACT, key=len, reverse=True)
    for item in fixed:
        pattern = re.compile(rf"(?<!\w){re.escape(item)}(?!\w)")
        if not pattern.search(protected):
            continue
        marker = f"https://keep.invalid/K{len(keep):03d}"
        protected = pattern.sub(marker, protected)
        keep[marker] = item
    for match in list(KEEP_RE.finditer(protected)):
        item = match.group(0)
        if item in keep.values() or item.startswith("https://keep.invalid/"):
            continue
        marker = f"https://keep.invalid/K{len(keep):03d}"
        protected = protected.replace(item, marker, 1)
        keep[marker] = item
    return protected, keep


def restore_value(value: str, keep: dict[str, str]) -> str:
    restored = value
    for marker, original in keep.items():
        restored = restored.replace(marker, original)
    return " ".join(restored.split())


# ---------------------------------------------------------------- silnik: DeepL
# Zamiast lokalnych modeli (argostranslate + NLLB, setki MB) tłumaczymy przez
# DeepL API: jeden endpoint HTTP + klucz w zmiennej DEEPL_API_KEY. Klucze Free
# kończą się na ":fx" i muszą trafiać na host api-free. `tag_handling=html`
# chroni znaczniki i encje. Cache (i18n/*.json) zostaje — do API idą TYLKO nowe
# stringi, więc build bez zmian treści nie wysyła ani jednego znaku.
DEEPL_SOURCE = {"pl": "PL", "en": "EN", "de": "DE", "ar": "AR"}
DEEPL_TARGET = {"pl": "PL", "en": "EN-US", "de": "DE", "ar": "AR"}
DEEPL_BATCH = 40   # limit DeepL: 50 tekstów / 128 KiB na żądanie — 40 z zapasem


def deepl_translate(texts: list[str], source: str, target: str) -> list[str]:
    """Tłumaczy partię stringów source->target jednym żądaniem DeepL,
    zachowując kolejność wejścia i chroniąc HTML (tag_handling=html)."""
    if not texts:
        return []
    key = os.environ.get("DEEPL_API_KEY")
    if not key:
        raise RuntimeError(
            "DEEPL_API_KEY nie jest ustawiony, a są nowe stringi do przetłumaczenia. "
            "Ustaw klucz DeepL (Free kończy się na ':fx') w środowisku builda."
        )
    host = "https://api-free.deepl.com" if key.endswith(":fx") else "https://api.deepl.com"
    fields = [("text", t) for t in texts] + [
        ("source_lang", DEEPL_SOURCE.get(source, source.upper())),
        ("target_lang", DEEPL_TARGET.get(target, target.upper())),
        ("tag_handling", "html"),
        ("split_sentences", "nonewlines"),
    ]
    body = urllib.parse.urlencode(fields).encode("utf-8")
    request = urllib.request.Request(
        host + "/v2/translate", data=body,
        headers={"Authorization": "DeepL-Auth-Key " + key,
                 "Content-Type": "application/x-www-form-urlencoded"},
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return [item["text"] for item in payload["translations"]]
        except urllib.error.HTTPError as exc:
            # 429/529 = za dużo żądań; 456 = wyczerpany limit znaków.
            if exc.code in (429, 529) and attempt < 3:
                time.sleep(2 * (attempt + 1))
                continue
            raise
    raise RuntimeError("DeepL: przekroczono liczbę prób.")


def request_translation(text: str, source: str, target: str, retries: int = 4) -> str:
    """Pojedynczy string przez DeepL (używane m.in. przez backcheck)."""
    return deepl_translate([text], source, target)[0]


def cache_path(target: str, prefix: str = "translations") -> Path:
    return I18N / f"{prefix}-{target}.json"


def load_cache(target: str, prefix: str = "translations") -> dict[str, str]:
    path = cache_path(target, prefix)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_cache(target: str, cache: dict[str, str], prefix: str = "translations") -> None:
    I18N.mkdir(exist_ok=True)
    ordered = dict(sorted(cache.items(), key=lambda item: item[0].casefold()))
    cache_path(target, prefix).write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def translate_catalog(
    strings: set[str], source: str, target: str,
    prefix: str = "translations",
    glossary: list[tuple[str, str]] | None = None,
) -> dict[str, str]:
    cache = load_cache(target, prefix)
    if source == "pl" and target in MANUAL:
        cache.update(MANUAL[target])
    pending = [value for value in sorted(strings, key=lambda item: (len(item), item.casefold()))
               if value not in cache]
    if not pending:
        return cache
    # Chronimy marki/liczby/glosariusz markerami-URL, tłumaczymy resztę partiami
    # DeepL (zwraca wyniki w kolejności wejścia), potem przywracamy markery.
    protected = [protect_value(value, glossary) for value in pending]
    total = (len(pending) + DEEPL_BATCH - 1) // DEEPL_BATCH
    for batch_index, start in enumerate(range(0, len(pending), DEEPL_BATCH), start=1):
        rows = protected[start:start + DEEPL_BATCH]
        originals = pending[start:start + DEEPL_BATCH]
        outputs = deepl_translate([row[0] for row in rows], source, target)
        for original, (_, keep), output in zip(originals, rows, outputs):
            cache[original] = restore_value(output, keep)
        save_cache(target, cache, prefix)
        print(f"[{source}->{target}] batch {batch_index}/{total}; cached={len(cache)}", flush=True)
    return cache




def translated(value: str, mapping: dict[str, str]) -> str:
    compact = " ".join(value.split())
    return mapping.get(compact, compact)


def replace_node_text(node, mapping: dict[str, str]) -> None:
    parent = node.getparent()
    raw = str(node)
    compact = " ".join(raw.split())
    if compact not in mapping:
        return
    leading = raw[:len(raw) - len(raw.lstrip())]
    trailing = raw[len(raw.rstrip()):]
    value = leading + mapping[compact] + trailing
    if node.is_text:
        parent.text = value
    else:
        parent.tail = value


def rewrite_internal_url(value: str, lang: str) -> str:
    if not value or value.startswith(("#", "mailto:", "tel:", "javascript:")):
        return value
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme or parsed.netloc:
        if parsed.netloc != urllib.parse.urlsplit(DOMAIN).netloc:
            return value
        path = parsed.path
        if path.startswith(("/assets/", "/en/", "/de/", "/ar/")):
            return value
        new_path = localized_route(lang, path or "/")
        return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, new_path, parsed.query, parsed.fragment))
    if not parsed.path.startswith("/"):
        return value
    if parsed.path.startswith(("/assets/", "/en/", "/de/", "/ar/")) or parsed.path in {"/favicon.ico", "/robots.txt", "/sitemap.xml", "/llms.txt"}:
        return value
    return urllib.parse.urlunsplit(("", "", localized_route(lang, parsed.path), parsed.query, parsed.fragment))


def translate_json_value(value, key: str | None, mapping: dict[str, str], lang: str):
    if isinstance(value, dict):
        entity_type = value.get("@type")
        entity_types = set(entity_type if isinstance(entity_type, list) else [entity_type])
        stable_entity = bool(entity_types & {"Organization", "LocalBusiness", "ProfessionalService", "WebSite"})
        translated_object = {}
        for child_key, child_value in value.items():
            if stable_entity and child_key in {"@id", "url"}:
                translated_object[child_key] = child_value
            elif "WebSite" in entity_types and child_key == "inLanguage":
                translated_object[child_key] = child_value
            else:
                translated_object[child_key] = translate_json_value(child_value, child_key, mapping, lang)
        return translated_object
    if isinstance(value, list):
        if key == "availableLanguage":
            return list(LANG_CODES)
        return [translate_json_value(child, key, mapping, lang) for child in value]
    if not isinstance(value, str):
        return value
    if key == "inLanguage":
        return lang
    if key == "@id" and value.endswith(("/#organization", "/#website")):
        return value
    if key in {"@id", "url"}:
        return rewrite_internal_url(value, lang)
    if key in JSON_SKIP_KEYS:
        return value
    return translated(value, mapping) if should_translate(value) else value


def configure_language_switch(doc, route: str, lang: str) -> None:
    details = doc.xpath("//*[contains(concat(' ', normalize-space(@class), ' '), ' language-switch ')]")
    if not details:
        return
    details = details[0]
    summary = details.xpath(".//summary")[0]
    summary.set("aria-label", MANUAL[lang]["Wybierz język"])
    code = details.xpath(".//*[contains(concat(' ', normalize-space(@class), ' '), ' language-switch__code ')]")[0]
    code.text = lang.upper()
    menu = details.xpath(".//ul")[0]
    menu.set("aria-label", MANUAL[lang]["Dostępne języki"])
    labels = {"pl": "Polski", "en": "English", "de": "Deutsch", "ar": "العربية"}
    for anchor in menu.xpath(".//a[@hreflang]"):
        option = anchor.get("hreflang")
        anchor.set("href", route if option == "pl" else localized_route(option, route))
        if option == lang:
            anchor.set("aria-current", "page")
        else:
            anchor.attrib.pop("aria-current", None)
        strong = anchor.find("strong")
        if strong is not None:
            strong.text = labels[option]


def ensure_hreflangs(doc, route: str, current_lang: str) -> None:
    head = doc.find("head")
    for node in head.xpath('./link[@rel="alternate"][@hreflang]'):
        head.remove(node)
    links = [
        ("pl-PL", DOMAIN + route),
        ("en", DOMAIN + localized_route("en", route)),
        ("de", DOMAIN + localized_route("de", route)),
        ("ar", DOMAIN + localized_route("ar", route)),
        ("x-default", DOMAIN + route),
    ]
    canonical = head.xpath('./link[@rel="canonical"]')
    insert_at = head.index(canonical[0]) + 1 if canonical else len(head)
    for offset, (hreflang, href) in enumerate(links):
        node = etree.Element("link", rel="alternate", hreflang=hreflang, href=href)
        head.insert(insert_at + offset, node)
    current = DOMAIN + (route if current_lang == "pl" else localized_route(current_lang, route))
    if canonical:
        canonical[0].set("href", current)
    for node in head.xpath('./meta[@property="og:url"]'):
        node.set("content", current)


def rebuild_hero_lead(doc, lang: str) -> None:
    brands = doc.xpath(
        "//*[contains(concat(' ', normalize-space(@class), ' '), ' hero-editorial__brand ')]"
    )
    if brands:
        brand = brands[0]
        brand.set("aria-label", "KABI CHEMIE")
        strong = brand.find("strong")
        span = brand.find("span")
        if strong is not None:
            strong.text = "KABI"
        if span is not None:
            span.text = "CHEMIE"
    nodes = doc.xpath(
        "//*[contains(concat(' ', normalize-space(@class), ' '), ' hero-lead-reveal ')]"
    )
    if not nodes:
        return
    node = nodes[0]
    for child in list(node):
        node.remove(child)
    node.text = None
    for index, word in enumerate(HERO_LEAD[lang].split()):
        if index:
            node[-1].tail = " "
        span = etree.Element("span", {"class": "hero-word", "style": f"--wd:{index}"})
        span.text = word
        node.append(span)


def _isolate_numeric_text(node) -> None:
    raw = str(node)
    matches = list(BIDI_NUMBER_RE.finditer(raw))
    if not matches:
        return
    owner = node.getparent()
    if owner is None:
        return
    if node.is_text:
        owner.text = raw[:matches[0].start()]
        container = owner
        insert_at = 0
    else:
        container = owner.getparent()
        if container is None:
            return
        owner.tail = raw[:matches[0].start()]
        insert_at = container.index(owner) + 1
    for index, match in enumerate(matches):
        isolated = etree.Element("bdi", {"dir": "ltr", "class": "bidi-number"})
        isolated.text = match.group(0)
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(raw)
        isolated.tail = raw[match.end():next_start]
        container.insert(insert_at, isolated)
        insert_at += 1


def stabilize_arabic_bidi(doc) -> None:
    ltr_elements = doc.xpath(
        '//a[starts-with(@href,"tel:") or starts-with(@href,"mailto:")]'
        ' | //input[@type="number" or @type="tel" or @type="email"'
        ' or @inputmode="decimal" or @inputmode="numeric"]'
        ' | //output | //*[@data-count-to]'
    )
    for element in ltr_elements:
        element.set("dir", "ltr")
    numeric_nodes = list(doc.xpath("//body//text()[contains(., '0') or contains(., '1') or "
                                   "contains(., '2') or contains(., '3') or contains(., '4') or "
                                   "contains(., '5') or contains(., '6') or contains(., '7') or "
                                   "contains(., '8') or contains(., '9')]"))
    for node in numeric_nodes:
        parent = node.getparent()
        if parent is None or parent.tag in SKIP_TAGS or parent.tag in {"bdi", "option"}:
            continue
        current = parent
        already_ltr = False
        while current is not None:
            if current.get("dir") == "ltr" or current.tag == "bdi":
                already_ltr = True
                break
            current = current.getparent()
        if not already_ltr:
            _isolate_numeric_text(node)


def translate_document(source_path: Path, mapping: dict[str, str], lang: str):
    doc = parse_page(source_path)
    route = route_for(source_path)
    root = doc.getroottree().getroot()
    root.set("lang", lang)
    if LANGS[lang]["dir"] == "rtl":
        root.set("dir", "rtl")
    else:
        root.attrib.pop("dir", None)
    body = doc.find("body")
    if body is not None:
        classes = [item for item in (body.get("class") or "").split() if not item.startswith("lang-")]
        classes.append(f"lang-{lang}")
        body.set("class", " ".join(classes))
    text_nodes = list(doc.xpath("//text()[normalize-space()]"))
    for node in text_nodes:
        parent = node.getparent()
        if parent is None or parent.tag in SKIP_TAGS or is_inside_language_switch(parent):
            continue
        replace_node_text(node, mapping)
    for element in doc.iter():
        if not isinstance(element.tag, str) or is_inside_language_switch(element):
            continue
        for attr in ("alt", "title", "aria-label", "placeholder"):
            value = element.get(attr)
            if value and should_translate(value):
                element.set(attr, translated(value, mapping))
        if element.tag == "input" and element.get("type") in {"submit", "button"}:
            value = element.get("value")
            if value and should_translate(value):
                element.set("value", translated(value, mapping))
        if element.tag == "meta" and element.get("content"):
            key = element.get("name") or element.get("property") or ""
            if key in META_KEYS and should_translate(element.get("content")):
                element.set("content", translated(element.get("content"), mapping))
    for script in doc.xpath('//script[@type="application/ld+json"]'):
        try:
            payload = json.loads(script.text or "")
            script.text = json.dumps(translate_json_value(payload, None, mapping, lang), ensure_ascii=False)
        except json.JSONDecodeError:
            pass
    for element in doc.xpath("//*[@href or @action]"):
        if is_inside_language_switch(element):
            continue
        for attr in ("href", "action"):
            if element.get(attr):
                element.set(attr, rewrite_internal_url(element.get(attr), lang))
    for meta in doc.xpath('//meta[translate(@http-equiv,"REFSH","refsh")="refresh"][@content]'):
        content = meta.get("content")
        meta.set("content", re.sub(r"(?i)(url\s*=\s*)(/[^\s]+)", lambda match: match.group(1) + rewrite_internal_url(match.group(2), lang), content))
    for meta in doc.xpath('//meta[@property="og:locale"]'):
        meta.set("content", LANGS[lang]["locale"])
    for script in doc.xpath('//script[contains(@src,"/assets/main.js")]'):
        script.set("src", script.get("src").replace("/assets/main.js", f"/assets/main.{lang}.js"))
    configure_language_switch(doc, route, lang)
    ensure_hreflangs(doc, route, lang)
    rebuild_hero_lead(doc, lang)
    if lang == "ar":
        stabilize_arabic_bidi(doc)
    return doc


def serialize_document(doc) -> bytes:
    return html.tostring(doc, encoding="utf-8", method="html", doctype="<!doctype html>", pretty_print=False)


def encode_js_string(value: str, quote: str) -> str:
    body = value.replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    body = body.replace(quote, "\\" + quote)
    return quote + body + quote


def generate_localized_js(lang: str, mapping: dict[str, str]) -> None:
    source = (WWW / "assets" / "main.js").read_text(encoding="utf-8")
    def replace(match: re.Match) -> str:
        token = match.group(0)
        value = js_literal_value(token)
        if value not in mapping:
            return token
        return encode_js_string(mapping[value], token[0])
    localized = JS_STRING_RE.sub(replace, source)
    (WWW / "assets" / f"main.{lang}.js").write_text(localized, encoding="utf-8")


def update_polish_hreflangs() -> None:
    for path in source_pages():
        text = path.read_text(encoding="utf-8")
        route = route_for(path)
        text = re.sub(r'\n?<link rel="alternate" hreflang="(?:en|de|ar)"[^>]*>', "", text)
        additions = (
            f'\n<link rel="alternate" hreflang="en" href="{DOMAIN}/en{route}">'
            f'\n<link rel="alternate" hreflang="de" href="{DOMAIN}/de{route}">'
            f'\n<link rel="alternate" hreflang="ar" href="{DOMAIN}/ar{route}">'
        )
        marker = re.search(r'<link rel="alternate" hreflang="pl-PL"[^>]*>', text)
        if marker:
            text = text[:marker.end()] + additions + text[marker.end():]
        else:
            canonical = re.search(r'<link rel="canonical"[^>]*>', text)
            if canonical:
                pl = f'\n<link rel="alternate" hreflang="pl-PL" href="{DOMAIN}{route}">'
                default = f'\n<link rel="alternate" hreflang="x-default" href="{DOMAIN}{route}">'
                text = text[:canonical.end()] + pl + additions + default + text[canonical.end():]
        path.write_text(text, encoding="utf-8")


def generate_sitemap(mappings: dict[str, dict[str, str]]) -> None:
    sitemap_path = WWW / "sitemap.xml"
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    image_ns = "http://www.google.com/schemas/sitemap-image/1.1"
    xhtml_ns = "http://www.w3.org/1999/xhtml"
    tree = etree.parse(str(sitemap_path))
    originals = []
    for node in tree.getroot().findall(f"{{{ns}}}url"):
        loc = node.find(f"{{{ns}}}loc")
        if loc is None or not loc.text:
            continue
        path = urllib.parse.urlsplit(loc.text).path
        if not path.startswith(("/en/", "/de/", "/ar/")):
            originals.append(node)
    root = etree.Element(f"{{{ns}}}urlset", nsmap={None: ns, "image": image_ns, "xhtml": xhtml_ns})
    for original in originals:
        original_loc = original.find(f"{{{ns}}}loc").text
        route = urllib.parse.urlsplit(original_loc).path
        alternates = {
            "pl-PL": DOMAIN + route,
            "en": DOMAIN + localized_route("en", route),
            "de": DOMAIN + localized_route("de", route),
            "ar": DOMAIN + localized_route("ar", route),
            "x-default": DOMAIN + route,
        }
        for lang in ("pl", "en", "de", "ar"):
            clone = copy.deepcopy(original)
            for existing_link in clone.findall(f"{{{xhtml_ns}}}link"):
                clone.remove(existing_link)
            loc = clone.find(f"{{{ns}}}loc")
            loc.text = DOMAIN + (route if lang == "pl" else localized_route(lang, route))
            if lang != "pl":
                for caption in clone.findall(f".//{{{image_ns}}}caption"):
                    caption.text = translated(caption.text or "", mappings[lang])
            for hreflang, href in alternates.items():
                etree.SubElement(clone, f"{{{xhtml_ns}}}link", rel="alternate", hreflang=hreflang, href=href)
            root.append(clone)
    sitemap_path.write_bytes(etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True))


def postedit_western_mapping(lang: str, mapping: dict[str, str]) -> dict[str, str]:
    edited: dict[str, str] = {}
    for source, target in mapping.items():
        value = re.sub(
            r"(?i)(?:conditioning|konditionierung)-water\.pl",
            "kondycjonowanie-wody.pl",
            target,
        )
        if lang == "en":
            value = value.replace("Nope.", "No.")
            value = value.replace("Yeah.", "Yes.")
            if re.search(r"kamie(?:ń|nia|niem)|zakamien", source, re.IGNORECASE):
                value = re.sub(r"\b(?:stones?|rock)\b", "scale", value, flags=re.IGNORECASE)
                value = re.sub(r"rescheduling of scale", "scale redeposition", value, flags=re.IGNORECASE)
                value = re.sub(r"regrowth of scale", "scale buildup", value, flags=re.IGNORECASE)
            if re.search(r"odkamien", source, re.IGNORECASE):
                value = re.sub(r"\b(?:de[- ]?scaling|descalation|destone(?:ing)?)\b", "descaling", value, flags=re.IGNORECASE)
                value = re.sub(r"\bdestoned\b", "descaled", value, flags=re.IGNORECASE)
                value = re.sub(r"\bdegradation\b", "descaling", value, flags=re.IGNORECASE)
            if re.search(r"układ\w*\s+chłodnicz", source, re.IGNORECASE):
                value = re.sub(r"\brefrigerat(?:ion|ing) systems?\b", lambda m: "cooling systems" if m.group(0).lower().endswith("systems") else "cooling system", value, flags=re.IGNORECASE)
            if re.search(r"wież\w*\s+chłodnicz", source, re.IGNORECASE):
                value = re.sub(r"\brefrigerat(?:ion|ing) towers?\b", lambda m: "cooling towers" if m.group(0).lower().endswith("towers") else "cooling tower", value, flags=re.IGNORECASE)
            if re.search(r"odsal", source, re.IGNORECASE):
                value = re.sub(r"\bdesalination\b", "blowdown", value, flags=re.IGNORECASE)
            if re.search(r"preparat", source, re.IGNORECASE):
                value = re.sub(r"\bpreparations\b", "treatment products", value, flags=re.IGNORECASE)
                value = re.sub(r"\bpreparation\b", "treatment product", value, flags=re.IGNORECASE)
            if re.search(r"dozow|dozuj|dawkow", source, re.IGNORECASE):
                value = re.sub(r"\bdispensing\b", "dosing", value, flags=re.IGNORECASE)
            if re.search(r"utrzymani\w* ruchu|obieg", source, re.IGNORECASE):
                value = re.sub(r"maintenance of traffic", "industrial maintenance", value, flags=re.IGNORECASE)
                value = re.sub(r"\btraffic\b", "operation", value, flags=re.IGNORECASE)
            if re.search(r"osad|złog", source, re.IGNORECASE):
                value = re.sub(r"\bsettlements\b", "deposits", value, flags=re.IGNORECASE)
                value = re.sub(r"\bsettlement\b", "deposit", value, flags=re.IGNORECASE)
            if re.search(r"wod\w* uzupełniając", source, re.IGNORECASE):
                value = re.sub(r"supplementary water", "make-up water", value, flags=re.IGNORECASE)
            if re.search(r"wod\w* zasilając", source, re.IGNORECASE):
                value = re.sub(r"water supply", "feedwater", value, flags=re.IGNORECASE)
            value = value.replace("Set up a cleaning service!", "Book a cleaning service!")
            value = value.replace("long stop", "extended shutdown")
        elif lang == "de":
            value = value.replace("Nope.", "Nein.")
            value = value.replace("Stromdosierung", "aktuelle Dosierung")
            value = value.replace("Fahrereinstellungen", "Reglereinstellungen")
            value = value.replace("Wette", "Anlage")
            if re.search(r"kamie(?:ń|nia|niem)|zakamien", source, re.IGNORECASE):
                value = re.sub(r"\bSteindicke\b", "Kesselsteinschichtdicke", value, flags=re.IGNORECASE)
                value = re.sub(r"\bSteingeschichte\b", "Kesselsteinbildung", value, flags=re.IGNORECASE)
                value = re.sub(r"\bSteine?n?\b", "Kesselstein", value, flags=re.IGNORECASE)
                value = value.replace("Steinrisiko", "Kesselsteinrisiko")
                value = re.sub(r"Umplanung von Kesselstein", "erneute Kesselsteinbildung", value, flags=re.IGNORECASE)
            if re.search(r"odkamien", source, re.IGNORECASE):
                value = re.sub(r"\b(?:Destone|Deskalierung)\b", "Entkalkung", value, flags=re.IGNORECASE)
                value = re.sub(r"\bentsteinen\b", "entkalken", value, flags=re.IGNORECASE)
            if re.search(r"odsal", source, re.IGNORECASE):
                value = value.replace("Entsalzung", "Abschlämmung").replace("entsalzung", "abschlämmung")
            if re.search(r"preparat", source, re.IGNORECASE):
                value = re.sub(r"\bZubereitungen\b", "Behandlungsprodukte", value, flags=re.IGNORECASE)
                value = re.sub(r"\bZubereitung\b", "Behandlungsprodukt", value, flags=re.IGNORECASE)
            if re.search(r"dozow|dozuj|dawkow", source, re.IGNORECASE):
                value = re.sub(r"\bAbgabe\b", "Dosierung", value, flags=re.IGNORECASE)
                value = value.replace("Abgabepumpen", "Dosierpumpen")
            if re.search(r"utrzymani\w* ruchu|obieg", source, re.IGNORECASE):
                value = re.sub(r"\bVerkehrs\b", "Betriebs", value, flags=re.IGNORECASE)
                value = re.sub(r"\bVerkehr\b", "Betrieb", value, flags=re.IGNORECASE)
            if re.search(r"osad|złog", source, re.IGNORECASE):
                value = re.sub(r"\bSiedlungen\b", "Ablagerungen", value, flags=re.IGNORECASE)
                value = re.sub(r"\bSiedlung\b", "Ablagerung", value, flags=re.IGNORECASE)
            if re.search(r"wod\w* uzupełniając", source, re.IGNORECASE):
                value = re.sub(r"zusätzliche\w* Wasser", "Nachspeisewasser", value, flags=re.IGNORECASE)
                value = value.replace("Zusatzwasser", "Nachspeisewasser")
            value = value.replace(" - Read |", " - Lesen |")
        edited[source] = value
    edited.update(MANUAL[lang])
    return edited


def postedit_arabic_mapping(mapping: dict[str, str]) -> dict[str, str]:
    replacements = (
        ("المنشأة الصناعية الصناعية", "المنشآت الصناعية"),
        ("التهزيم العكسي", "التناضح العكسي"),
        ("المكثف بخارجي", "المكثف التبخيري"),
        ("المكثف بخارية", "المكثف التبخيري"),
        ("المكثف بخار", "المكثف التبخيري"),
        ("المكثفات بخار", "المكثفات التبخيرية"),
        ("المياه خاص بالغلاية", "مياه الغلايات"),
        ("الماء خاص بالغلاية", "مياه الغلاية"),
        ("و خاص بالغلاية", " ومياه الغلاية"),
        ("حماية المضاد للتآكل", "الحماية من التآكل"),
        ("الحماية المضاد للتآكل", "الحماية من التآكل"),
        ("النظافة الكيميائية", "التنظيف الكيميائي"),
        ("دراسة قضائية", "دراسة حالة"),
        ("المثبطات التآكل", "مثبطات التآكل"),
        ("النظام المياه", "منظومة المياه"),
        ("النظام الغلاية", "منظومة الغلاية"),
        ("الترسّبات الكلسية الغلايات", "الترسّبات الكلسية من الغلايات"),
        ("التصفية الأولية", "الترشيح الأولي"),
        ("المبيدات الحيوية وحده", "المبيدات الحيوية وحدها"),
        ("كم عدد المرات التي", "كم مرة"),
        ("مواد المعالجة الكيميائية العالمي", "مادة معالجة كيميائية عامة"),
    )
    edited = {}
    for source, target in mapping.items():
        value = target
        for old, new in replacements:
            value = value.replace(old, new)
        edited[source] = value
    edited.update(MANUAL["ar"])
    return edited


def generate() -> None:
    I18N.mkdir(exist_ok=True)
    pages = source_pages()
    documents = [(path, parse_page(path)) for path in pages]
    strings = collect_js_strings()
    for _, doc in documents:
        strings.update(collect_page_strings(doc))
    print(f"Catalog: {len(strings)} unique translatable strings across {len(pages)} HTML files", flush=True)
    mappings: dict[str, dict[str, str]] = {}
    # DeepL tłumaczy bezpośrednio PL->EN, PL->DE i PL->AR — bez pivota przez
    # angielski (mniej błędów) i bez lokalnych modeli NLLB.
    raw_english = translate_catalog(strings, "pl", "en")
    raw_german = translate_catalog(strings, "pl", "de")
    raw_arabic = translate_catalog(strings, "pl", "ar", glossary=AR_GLOSSARY)
    mappings["en"] = postedit_western_mapping("en", raw_english)
    mappings["de"] = postedit_western_mapping("de", raw_german)
    save_cache("en", mappings["en"])
    save_cache("de", mappings["de"])
    mappings["ar"] = postedit_arabic_mapping(raw_arabic)
    save_cache("ar", mappings["ar"])
    update_polish_hreflangs()
    for lang, mapping in mappings.items():
        target_root = (WWW / lang).resolve()
        if target_root.parent != WWW.resolve():
            raise RuntimeError(f"Unsafe language output path: {target_root}")
        if target_root.exists():
            shutil.rmtree(target_root)
        for source_path in pages:
            rel = source_path.relative_to(WWW)
            output_path = target_root / rel
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(serialize_document(translate_document(source_path, mapping, lang)))
        generate_localized_js(lang, mapping)
        print(f"Generated {lang}: {len(pages)} HTML files", flush=True)
    generate_sitemap(mappings)


def normalized_for_compare(value: str) -> str:
    value = value.casefold()
    value = re.sub(r"[^\w%]+", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def backcheck() -> None:
    report = {}
    for lang in LANGS:
        forward = load_cache(lang)
        translated_values = {value for value in forward.values() if should_translate(value)}
        back = translate_catalog(translated_values, lang, "pl", prefix=f"back-{lang}")
        flagged = []
        for source, target in forward.items():
            returned = back.get(target, "")
            if not returned:
                flagged.append({"source": source, "translation": target, "back": "", "score": 0})
                continue
            score = difflib.SequenceMatcher(None, normalized_for_compare(source), normalized_for_compare(returned)).ratio()
            source_numbers = re.findall(r"\d+(?:[.,]\d+)?", source)
            target_numbers = re.findall(r"\d+(?:[.,]\d+)?", target)
            number_mismatch = source_numbers != target_numbers
            length_ratio = len(target.split()) / max(1, len(source.split()))
            if (len(source.split()) >= 5 and score < .34) or number_mismatch or not (.35 <= length_ratio <= 2.8):
                flagged.append({
                    "source": source, "translation": target, "back": returned,
                    "score": round(score, 3), "number_mismatch": number_mismatch,
                    "length_ratio": round(length_ratio, 3),
                })
        flagged.sort(key=lambda item: (item.get("number_mismatch", False) is False, item["score"]))
        report[lang] = {"checked": len(forward), "flagged": len(flagged), "items": flagged}
        print(f"Backcheck {lang}: checked={len(forward)} flagged={len(flagged)}", flush=True)
    (I18N / "backtranslation-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def localized_file_for_route(lang: str, route: str) -> Path:
    clean = urllib.parse.urlsplit(route).path
    if clean.endswith("/"):
        return WWW / clean.lstrip("/") / "index.html"
    return WWW / clean.lstrip("/")


def qa() -> None:
    pages = source_pages()
    expected = {path.relative_to(WWW).as_posix() for path in pages}
    errors = []
    stats = {}
    for lang, config in LANGS.items():
        target_root = WWW / lang
        actual = {path.relative_to(target_root).as_posix() for path in target_root.rglob("*.html")} if target_root.exists() else set()
        if actual != expected:
            errors.append(f"{lang}: page set mismatch missing={sorted(expected-actual)} extra={sorted(actual-expected)}")
        untranslated = []
        broken = []
        json_errors = []
        selector_pages = 0
        for rel in sorted(actual):
            path = target_root / rel
            doc = parse_page(path)
            root = doc.getroottree().getroot()
            if root.get("lang") != lang:
                errors.append(f"{lang}/{rel}: invalid html lang")
            if config["dir"] == "rtl" and root.get("dir") != "rtl":
                errors.append(f"{lang}/{rel}: missing RTL direction")
            if config["dir"] != "rtl" and root.get("dir"):
                errors.append(f"{lang}/{rel}: unexpected direction")
            route = route_for(WWW / rel)
            if doc.xpath("//*[contains(concat(' ', normalize-space(@class), ' '), ' language-switch ')]"):
                selector_pages += 1
            hreflangs = doc.xpath('./head/link[@rel="alternate"][@hreflang]/@hreflang')
            if set(hreflangs) != {"pl-PL", "en", "de", "ar", "x-default"}:
                errors.append(f"{lang}/{rel}: incomplete hreflang set")
            for node in doc.xpath("//text()[normalize-space()]"):
                parent = node.getparent()
                if parent is None or parent.tag in SKIP_TAGS or is_inside_language_switch(parent):
                    continue
                value = " ".join(str(node).split())
                probe = value
                for preserved in PRESERVE_EXACT:
                    probe = probe.replace(preserved, "")
                if len(value.split()) >= 3 and POLISH_WORDS.search(probe):
                    untranslated.append(value)
            for script in doc.xpath('//script[@type="application/ld+json"]'):
                try:
                    json.loads(script.text or "")
                except json.JSONDecodeError as exc:
                    json_errors.append(f"{rel}: {exc}")
            for anchor in doc.xpath('//a[@href]'):
                href = anchor.get("href")
                if not href or not href.startswith(f"/{lang}/"):
                    continue
                target = localized_file_for_route(lang, href)
                if not target.exists():
                    broken.append(f"{rel} -> {href}")
        untranslated = sorted(set(untranslated))
        broken = sorted(set(broken))
        if untranslated:
            errors.append(f"{lang}: untranslated Polish fragments={len(untranslated)}")
        if broken:
            errors.append(f"{lang}: broken localized links={len(broken)}")
        if json_errors:
            errors.append(f"{lang}: JSON-LD errors={len(json_errors)}")
        stats[lang] = {
            "pages": len(actual), "selector_pages": selector_pages,
            "untranslated": untranslated, "broken_links": broken, "json_errors": json_errors,
        }
        print(f"QA {lang}: pages={len(actual)} untranslated={len(untranslated)} broken={len(broken)} json={len(json_errors)}", flush=True)
    report = {"ok": not errors, "errors": errors, "stats": stats}
    I18N.mkdir(exist_ok=True)
    (I18N / "qa-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit("Localization QA failed: " + " | ".join(errors))
    print("Localization QA: OK", flush=True)


def quality() -> None:
    pages = source_pages()
    strings = collect_js_strings()
    for path in pages:
        strings.update(collect_page_strings(parse_page(path)))

    report = {}
    all_errors = []
    protected_terms = (
        "KABI CHEMIE", "KCAQUA", "Łukasz Mielcarz",
        "Przemysław Jesiołkowski", "Łukasz Kumor",
    )
    forbidden_arabic = (
        "فساد", "حجارة", "طائرات", "دبابات", "تحطيم", "الأمونيكال",
        "الثلاجة الصناعية", "المنشط", "المزق", "الاطارات", "القوارض",
    )
    allowed_latin_ar = {
        "08-110 Siedlce", "4200 µS", "8 °n", "KCAQUA 305",
        "NIP: 8212519774", "OSM Siedlce", "Żabokliki-Kolonia ul. Stocka 10",
    }

    for lang in LANGS:
        mapping = load_cache(lang)
        missing = sorted(value for value in strings if value not in mapping)
        empty = sorted(source for source, target in mapping.items() if not target.strip())
        markers = sorted(
            source for source, target in mapping.items()
            if "ZXKABI" in target or "keep.invalid" in target
        )
        number_mismatches = []
        protected_missing = []
        mutated_domains = []
        suspicious_arabic = []
        latin_only_arabic = []
        for source, target in mapping.items():
            source_numbers = re.findall(r"\d+(?:[.,]\d+)?", source)
            target_numbers = re.findall(r"\d+(?:[.,]\d+)?", target)
            if source_numbers != target_numbers:
                number_mismatches.append({"source": source, "translation": target})
            for term in protected_terms:
                if term in source and term not in target:
                    protected_missing.append({"term": term, "source": source, "translation": target})
            if "kondycjonowanie-wody.pl" in source and "kondycjonowanie-wody.pl" not in target:
                mutated_domains.append({"source": source, "translation": target})
            if lang == "ar":
                found = [term for term in forbidden_arabic if term in target]
                if found:
                    suspicious_arabic.append({"terms": found, "source": source, "translation": target})
                has_arabic = bool(re.search(r"[\u0600-\u06ff]", target))
                if (
                    len(target.split()) >= 2 and not has_arabic
                    and target not in allowed_latin_ar
                    and source not in PRESERVE_EXACT
                ):
                    latin_only_arabic.append({"source": source, "translation": target})

        errors = {
            "missing": missing,
            "empty": empty,
            "markers": markers,
            "number_mismatches": number_mismatches,
            "protected_missing": protected_missing,
            "mutated_domains": mutated_domains,
            "suspicious_arabic": suspicious_arabic,
            "latin_only_arabic": latin_only_arabic,
        }
        error_count = sum(len(items) for items in errors.values())
        if error_count:
            all_errors.append(f"{lang}: {error_count} editorial QA errors")
        report[lang] = {
            "catalog_strings": len(strings),
            "mapping_entries": len(mapping),
            "error_count": error_count,
            **errors,
        }
        print(f"Quality {lang}: strings={len(strings)} errors={error_count}", flush=True)

    payload = {"ok": not all_errors, "errors": all_errors, "languages": report}
    (I18N / "editorial-qa-report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if all_errors:
        raise SystemExit("Editorial QA failed: " + " | ".join(all_errors))
    print("Editorial QA: OK", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("generate", "qa", "quality", "backcheck"))
    args = parser.parse_args()
    if args.action == "generate":
        generate()
    elif args.action == "qa":
        qa()
    elif args.action == "quality":
        quality()
    else:
        backcheck()


if __name__ == "__main__":
    main()
