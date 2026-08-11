/*
 * Panel redakcyjny bazy wiedzy — NARZĘDZIE LOKALNE.
 *
 * Skrót:  Ctrl + Alt + A   (Escape zamyka)
 *
 * Wstrzykiwany do stron TYLKO przy buildzie z KABI_ADMIN=1, więc w produkcyjnym
 * www/ tego pliku nie ma. Dodatkowo odmawia uruchomienia poza localhost — to
 * wygoda i zabezpieczenie przed pomyłką, nie mechanizm bezpieczeństwa.
 *
 * Formularz buduje się z /api/schema, czyli z information_schema.columns.
 * Dodanie kolumny w db/init/001_schema.sql pojawia się tu bez zmian w tym pliku.
 *
 * Cała warstwa wizualna siedzi w Shadow DOM, żeby style strony i panelu
 * nie mieszały się wzajemnie.
 */
(function () {
  "use strict";

  var LOKALNE = ["localhost", "127.0.0.1", "[::1]", "::1"];
  if (LOKALNE.indexOf(location.hostname) === -1) {
    console.warn("[panel] pominięty — działa wyłącznie na localhost");
    return;
  }

  // Skróty celowo są trzy, bo każdy ma inną wadę:
  //  * Ctrl+Shift+Y — podstawowy, wolny we wszystkich przeglądarkach
  //  * podwójny Shift — gdy skrót koliduje z czymś w systemie
  //  * #panel w adresie — gdy klawiatura zawodzi zupełnie
  // Porównujemy e.code, nie e.key: na polskim układzie AltGr to Ctrl+Alt,
  // więc Ctrl+Alt+A daje e.key === "ą" i porównanie do "a" nigdy nie trafia.
  var SKROT = "Ctrl + Shift + Y  (albo dwa razy Shift, albo #panel w adresie)";

  // Pola tekstowe: kolumna → etykieta i typ kontrolki
  var POLA = [
    { k: "slug", label: "Adres strony", typ: "text", pomoc: "Ta nazwa pojawi się w adresie strony. Same małe litery i myślniki." },
    { k: "title", label: "Tytuł artykułu", typ: "text" },
    { k: "list_title", label: "Tytuł na liście artykułów", typ: "text" },
    { k: "short", label: "Krótka nazwa", typ: "text" },
    { k: "lead", label: "Wstęp", typ: "textarea" },
    { k: "excerpt", label: "Zapowiedź na liście", typ: "text" },
    { k: "audience", label: "Dla kogo", typ: "text" },
    { k: "read_time", label: "Czas czytania", typ: "text", pomoc: "np. 6 min" },
    { k: "image", label: "Zdjęcie główne", typ: "text", pomoc: "Jeśli zostawisz puste, pojawi się zdjęcie z listy artykułów." },
    { k: "prose", label: "Treść artykułu", typ: "redaktor",
      pomoc: "Pisz jak w edytorze tekstu: Enter zaczyna akapit, Shift+Enter łamie " +
             "wiersz. Ukośnik „/” w pustym akapicie otwiera menu wstawiania " +
             "(nagłówki, listy, cytaty, tabele, zdjęcia). Działają skróty „## ”, " +
             "„- ”, „> ” oraz Ctrl+B/I, Ctrl+K (odnośnik), Ctrl+Z (cofnij), " +
             "Ctrl+S (zapis). Zdjęcia można przeciągać z dysku wprost na treść." },
    { k: "html", label: "Własny kod strony", typ: "kod",
      pomoc: "Dla zaawansowanych. Jeśli tu coś wpiszesz, zastąpi cały układ " +
             "artykułu. Menu i stopka strony zostają." }
  ];

  // Pola listowe: kolumna → kolumny wiersza
  var LISTY = [
    { k: "faq", label: "Pytania i odpowiedzi", kolumny: [["q", "Pytanie"], ["a", "Odpowiedź"]] },
    // Wszystkie trzy pola są listami — etykieta z już używanych, tytuł
    // i adres z istniejących stron serwisu, wzajemnie zsynchronizowane.
    { k: "related", label: "Polecane strony",
      kolumny: [["kicker", "Rodzaj", "etykiety"],
                ["title", "Tytuł", "tytuly-stron"],
                ["url", "Adres", "adresy"]] }
  ];

  var STYLE = "" +
    ":host{all:initial}" +
    "*{box-sizing:border-box;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}" +
    ".tlo{position:fixed;inset:0;background:rgba(4,18,28,.62);backdrop-filter:blur(3px);z-index:2147483000;display:flex;align-items:stretch;justify-content:center;padding:24px}" +
    ".okno{background:#0e1c26;color:#e8f1f6;border:1px solid #1d3a4d;border-radius:14px;width:min(1180px,100%);display:grid;grid-template-columns:290px 1fr;overflow:hidden;box-shadow:0 24px 70px rgba(0,0,0,.5)}" +
    ".okno.z-podgladem{width:min(1720px,100%);grid-template-columns:250px minmax(360px,1fr) minmax(420px,1.05fr)}" +
    ".podglad{display:none;flex-direction:column;min-height:0;border-left:1px solid rgba(255,255,255,.08);background:#060d13}" +
    ".okno.z-podgladem .podglad{display:flex}" +
    ".podglad__pasek{padding:9px 12px;border-bottom:1px solid rgba(255,255,255,.08);display:flex;align-items:center;gap:8px;font-size:12px;color:#9fc0d2}" +
    ".podglad__stan{margin-left:auto;font-size:11px;color:#7f95a3}" +
    ".podglad__stan.pracuje{color:#7fc4e8}" +
    ".podglad iframe{flex:1;width:100%;border:0;background:#0b1a24}" +
    ".szer{display:flex;gap:4px}" +
    ".szer button{padding:3px 8px;font-size:11px;font-weight:600}" +
    ".szer button.akt{background:#1c6fa0;border-color:#3f9dd0}" +
    // Maksymalizacja: chowamy listę i formularz, podgląd zajmuje całe okno,
    // a tło traci margines, żeby podgląd sięgał krawędzi ekranu.
    ".okno.podglad-max{width:100%;grid-template-columns:1fr;border-radius:0;border:0}" +
    ".okno.podglad-max .lewa,.okno.podglad-max .prawa{display:none}" +
    ".okno.podglad-max .podglad{display:flex;border-left:0}" +
    ".tlo.bez-marginesu{padding:0}" +
    ".podglad__max{padding:3px 9px;font-size:11px;font-weight:600}" +
    ".lewa{background:#0a151d;border-right:1px solid rgba(255,255,255,.08);display:flex;flex-direction:column;min-height:0}" +
    ".naglowek{padding:14px 16px;border-bottom:1px solid rgba(255,255,255,.08);display:flex;align-items:center;gap:8px}" +
    ".naglowek h2{margin:0;font-size:14px;letter-spacing:.04em;text-transform:uppercase;color:#7fc4e8;font-weight:700}" +
    ".szukaj{margin:10px;padding:8px 10px;background:#08121a;border:1px solid rgba(255,255,255,.12);border-radius:8px;color:#e8f1f6;font-size:13px}" +
    ".lista{overflow:auto;flex:1;padding:0 8px 8px}" +
    ".zakladka{flex:1;padding:7px 4px;font-size:12px;background:transparent;border-color:transparent;color:#8fa8b6}" +
    ".zakladka.akt{background:#12384f;border-color:rgba(127,196,232,.4);color:#e8f1f6}" +
    ".ref-form{display:grid;gap:12px;align-content:start}" +
    ".ref-plik{border:1px dashed rgba(127,196,232,.45);border-radius:10px;padding:12px;background:rgba(127,196,232,.05)}" +
    ".ref-plik__stan{font-size:12px;color:#9fc0d2;margin-top:6px}" +
    ".ref-plik input[type=file]{font-size:12px;color:#9fc0d2}" +
    ".poz{padding:8px 10px;border-radius:8px;cursor:pointer;font-size:13px;line-height:1.35;border:1px solid transparent}" +
    ".poz:hover{background:rgba(127,196,232,.10)}" +
    ".poz.akt{background:rgba(127,196,232,.16);border-color:rgba(127,196,232,.45)}" +
    ".poz small{display:block;color:#8fa8b6;font-size:11px;margin-top:2px}" +
    ".poz.ukryty{opacity:.45}" +
    ".prawa{display:flex;flex-direction:column;min-height:0}" +
    ".pasek{padding:12px 16px;border-bottom:1px solid rgba(255,255,255,.08);display:flex;gap:8px;align-items:center;flex-wrap:wrap}" +
    ".pasek .rosnie{flex:1}" +
    ".form{overflow:auto;padding:16px;display:grid;gap:14px;align-content:start}" +
    "label{display:block;font-size:12px;color:#9fc0d2;margin-bottom:5px;font-weight:600}" +
    "input[type=text],input[type=number],textarea,select{width:100%;background:#08121a;border:1px solid rgba(255,255,255,.14);border-radius:8px;color:#e8f1f6;padding:8px 10px;font-size:13px}" +
    "textarea{min-height:80px;resize:vertical;line-height:1.5}" +
    "textarea.kod{min-height:190px;font-family:ui-monospace,Consolas,monospace;font-size:12.5px}" +
    ".pomoc{font-size:11px;color:#7f95a3;margin-top:4px}" +
    ".zle input,.zle textarea{border-color:#e2725b}" +
    ".blad-pola{color:#ff9b86;font-size:11px;margin-top:4px}" +
    "button{background:#12384f;color:#e8f1f6;border:1px solid rgba(127,196,232,.4);border-radius:8px;padding:8px 14px;font-size:13px;cursor:pointer;font-weight:600}" +
    "button:hover{background:#17475f}" +
    "button.glowny{background:#1c6fa0;border-color:#3f9dd0}" +
    "button.grozny{background:#5c2320;border-color:#a3564d}" +
    "button:disabled{opacity:.5;cursor:not-allowed}" +
    ".red{border:1px solid rgba(255,255,255,.14);border-radius:8px}" +
    ".red__gora{position:sticky;top:0;z-index:6;background:#0a1620;border-bottom:1px solid rgba(255,255,255,.10);border-radius:8px 8px 0 0}" +
    ".red__pasek{display:flex;flex-wrap:wrap;gap:3px 0;padding:6px;align-items:center}" +
    ".red__pasek .grupa{display:flex;gap:2px;padding-right:7px;margin-right:7px;border-right:1px solid rgba(255,255,255,.12)}" +
    ".red__pasek .grupa:last-of-type{border-right:0;margin-right:0;padding-right:0}" +
    ".red__pasek button{padding:4px 8px;font-size:12px;font-weight:600;background:#12384f}" +
    ".red__pasek button.akt{background:#1c6fa0;border-color:#3f9dd0}" +
    ".red__pasek button:disabled{opacity:.4}" +
    ".red__pasek button.ikona{min-width:30px;text-align:center;padding:4px 6px}" +
    ".red__pasek button.b-b{font-weight:800}" +
    ".red__pasek button.b-i{font-style:italic}" +
    ".red__pasek button.b-s{text-decoration:line-through}" +
    ".red__pasek .rosnie{flex:1}" +
    ".red__kontekst{display:none;padding:5px 8px;border-top:1px dashed rgba(255,255,255,.14);gap:6px;align-items:center;font-size:11.5px;color:#9fc0d2;flex-wrap:wrap}" +
    ".red__kontekst.widoczny{display:flex}" +
    ".red__kontekst strong{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:#7fc4e8}" +
    ".red__kontekst select{width:auto;padding:3px 6px;font-size:11.5px}" +
    ".red__kontekst button{padding:3px 8px;font-size:11.5px}" +
    ".red__tresc{min-height:340px;padding:16px 18px;background:#08121a;font-size:14.5px;line-height:1.7;outline:none;position:relative}" +
    ".red__tresc:focus{background:#091620}" +
    ".red__tresc h2{font-size:19px;margin:1.4em 0 .5em;color:#cfe6f4;font-weight:700}" +
    ".red__tresc h2:first-child{margin-top:0}" +
    ".red__tresc h3{font-size:15.5px;margin:1.2em 0 .4em;color:#bcd9ea;font-weight:700}" +
    ".red__tresc p{margin:0 0 .9em}" +
    ".red__tresc ul,.red__tresc ol{margin:0 0 .9em;padding-left:1.4em}" +
    ".red__tresc li{margin:.3em 0}" +
    ".red__tresc a{color:#7fc4e8}" +
    ".red__tresc p.note{border-left:3px solid #7fc4e8;padding:.5em 0 .5em .9em;color:#a9c9da;background:rgba(127,196,232,.07)}" +
    ".red__tresc blockquote{border-left:3px solid #3f9dd0;margin:1em 0;padding:.4em 0 .4em 1em;color:#b7d3e2;font-style:italic;background:rgba(63,157,208,.06)}" +
    ".red__tresc hr{border:0;border-top:1px solid rgba(127,196,232,.4);margin:1.6em 0}" +
    ".red__tresc table{border-collapse:collapse;width:100%;margin:1.2em 0;font-size:13px}" +
    ".red__tresc th,.red__tresc td{border:1px solid rgba(255,255,255,.2);padding:.45em .6em;vertical-align:top;min-width:44px}" +
    ".red__tresc th{background:#10293a;font-weight:700;color:#cfe6f4}" +
    ".red__tresc figure.red-fig-akt{outline:2px solid #3f9dd0;outline-offset:2px}" +
    ".red__tresc.pusty::before{content:attr(data-placeholder);position:absolute;left:18px;top:16px;color:#5d7382;pointer-events:none}" +
    ".red__tresc.przeciaganie{outline:2px dashed #3f9dd0;outline-offset:-3px}" +
    ".red__tresc .tekst-srodek{text-align:center}" +
    ".red__tresc ul.tekst-srodek,.red__tresc ol.tekst-srodek," +
    ".red__tresc ul.tekst-prawo,.red__tresc ol.tekst-prawo{list-style-position:inside;padding-left:0}" +
    ".red__tresc .tekst-prawo{text-align:right}" +
    ".red__tresc figure.foto-mala{width:40%}" +
    ".red__tresc figure.foto-srednia{width:65%}" +
    ".red__tresc figure.tekst-srodek{margin-left:auto;margin-right:auto}" +
    ".red__tresc figure.foto-oblewa-lewo{float:left;margin:.35em 1.2rem .8rem 0}" +
    ".red__tresc figure.foto-oblewa-prawo{float:right;margin:.35em 0 .8rem 1.2rem}" +
    ".red__tresc h2,.red__tresc h3{clear:both}" +
    ".red__tresc::after{content:\'\';display:table;clear:both}" +
    ".red__tresc figure.tekst-prawo{margin-left:auto;margin-right:0}" +
    ".red__tresc figure{margin:1.2em 0}" +
    ".red__tresc img{display:block;width:100%;height:auto;border-radius:8px}" +
    ".red__tresc figcaption{margin-top:.4em;font-size:12px;color:#8fa8b6}" +
    ".red__stopka{display:flex;gap:10px;align-items:center;padding:5px 10px;border-top:1px solid rgba(255,255,255,.10);font-size:11.5px;color:#7f95a3;background:#0a1620;border-radius:0 0 8px 8px}" +
    ".red__stopka .rosnie{flex:1}" +
    ".red__stopka button{padding:2px 8px;font-size:11px;font-weight:600}" +
    ".red.maks{position:fixed;inset:0;z-index:60;display:flex;flex-direction:column;background:#0a151d;border:0;border-radius:0}" +
    ".red.maks .red__gora{border-radius:0}" +
    ".red.maks .red__pasek{justify-content:center}" +
    ".red.maks .red__tresc{flex:1;overflow:auto;width:100%;max-width:920px;margin:0 auto;font-size:16.5px;padding:32px 40px}" +
    ".red.maks .red__kod{flex:1;width:100%;max-width:1000px;margin:0 auto}" +
    ".red.maks .red__stopka{border-radius:0}" +
    ".red-nakladka{position:fixed;inset:0;z-index:2147483600;background:rgba(2,10,16,.6);display:flex;align-items:center;justify-content:center;padding:24px}" +
    ".red-dialog{background:#0e1c26;border:1px solid #1d3a4d;border-radius:12px;box-shadow:0 24px 70px rgba(0,0,0,.55);width:min(720px,100%);max-height:88vh;overflow:auto;padding:16px;display:grid;gap:10px}" +
    ".red-dialog h3{margin:0;font-size:12.5px;text-transform:uppercase;letter-spacing:.05em;color:#7fc4e8}" +
    ".red-dialog label{margin-bottom:0}" +
    ".red-dialog .w-linii{display:flex;align-items:center;gap:8px}" +
    ".red-dialog .w-linii input{width:auto}" +
    ".red-dialog .poglad{max-height:220px;width:auto;max-width:100%;border-radius:8px;justify-self:start}" +
    ".red-dialog .stopka-dialogu{display:flex;gap:8px;justify-content:flex-end;margin-top:4px}" +
    ".red-dialog .lista-stron{max-height:220px;overflow:auto;border:1px solid rgba(255,255,255,.12);border-radius:8px}" +
    ".red-dialog .lista-stron button{display:block;width:100%;text-align:left;background:transparent;border:0;border-bottom:1px solid rgba(255,255,255,.06);border-radius:0;padding:7px 10px;font-size:12.5px;font-weight:400}" +
    ".red-dialog .lista-stron button:hover{background:rgba(127,196,232,.12)}" +
    ".red-dialog .wgraj{border:1px dashed rgba(127,196,232,.45);border-radius:10px;padding:10px;display:flex;gap:10px;align-items:center;font-size:12px;color:#9fc0d2}" +
    ".red-dialog .siatka{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px}" +
    ".red-dialog .kafel{padding:0;overflow:hidden;background:#08121a;border:1px solid rgba(255,255,255,.14);border-radius:8px;cursor:pointer;text-align:left}" +
    ".red-dialog .kafel:hover{border-color:#3f9dd0}" +
    ".red-dialog .kafel img{display:block;width:100%;height:78px;object-fit:cover}" +
    ".red-dialog .kafel span{display:block;padding:5px 7px;font-size:10.5px;line-height:1.3;color:#9fc0d2;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}" +
    ".red-menu{position:fixed;z-index:2147483620;background:#0e1c26;border:1px solid #1d3a4d;border-radius:10px;box-shadow:0 16px 50px rgba(0,0,0,.55);min-width:270px;max-height:330px;overflow:auto;padding:4px}" +
    ".red-menu .naglowek-menu{padding:6px 10px;font-size:10.5px;color:#7f95a3;text-transform:uppercase;letter-spacing:.05em}" +
    ".red-menu button{display:block;width:100%;text-align:left;background:transparent;border:0;padding:6px 10px;border-radius:6px;font-weight:400;font-size:13px}" +
    ".red-menu button strong{display:block;font-size:12.5px;color:#e8f1f6}" +
    ".red-menu button small{color:#8fa8b6;font-size:11px}" +
    ".red-menu button.akt{background:#12384f}" +
    ".szkic-banner{display:flex;gap:10px;align-items:center;padding:9px 12px;border-radius:8px;font-size:12.5px;background:rgba(28,111,160,.22);border:1px solid rgba(63,157,208,.5)}" +
    ".szkic-banner span{flex:1}" +
    ".red__kod{width:100%;min-height:340px;border:0;border-radius:0;font-family:ui-monospace,Consolas,monospace;font-size:12.5px}" +
    ".wiersz{display:grid;gap:6px;margin-bottom:6px;align-items:start}" +
    ".wiersz textarea{min-height:52px}" +
    ".wiersz select{min-width:0}" +
    ".sekcja{border:1px solid rgba(255,255,255,.10);border-radius:10px;padding:12px}" +
    ".sekcja h3{margin:0 0 10px;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:#7fc4e8}" +
    ".komunikat{padding:8px 12px;border-radius:8px;font-size:12.5px;line-height:1.45}" +
    ".ok{background:rgba(46,125,80,.25);border:1px solid rgba(102,187,106,.5)}" +
    ".zly{background:rgba(140,40,30,.3);border:1px solid rgba(226,114,91,.55)}" +
    ".adres{font-family:ui-monospace,Consolas,monospace;font-size:12px;color:#9fe0b0}" +
    ".dwie{display:grid;grid-template-columns:1fr 1fr;gap:12px}" +
    "pre{white-space:pre-wrap;word-break:break-word;margin:0;font-size:11.5px;max-height:180px;overflow:auto}";

  var host, root, stan = { lista: [], kategorie: [], adresy: [], etykiety: [], grafiki: [],
                           biezacy: null, artykul: null, zmiany: {} };

  // ------------------------------------------------------------------ API
  function api(sciezka, opcje) {
    opcje = opcje || {};
    return fetch("/api/" + sciezka, {
      method: opcje.metoda || "GET",
      headers: opcje.dane ? { "Content-Type": "application/json" } : undefined,
      body: opcje.dane ? JSON.stringify(opcje.dane) : undefined
    }).then(function (r) {
      // Nie każda odpowiedź to JSON: nginx 413 (za duży plik) czy 502 wracają
      // HTML-em. Bez tej ochrony r.json() rzucało nieczytelny błąd parsera.
      return r.json().catch(function () {
        throw new Error(r.status === 413
          ? "Plik jest za duży dla serwera."
          : "HTTP " + r.status + " — serwer zwrócił nieoczekiwaną odpowiedź.");
      }).then(function (tresc) {
        if (!r.ok) throw new Error(tresc && tresc.blad ? tresc.blad : "HTTP " + r.status);
        return tresc;
      });
    });
  }

  function el(sel) { return root.querySelector(sel); }

  function komunikat(tekst, czyBlad) {
    var pole = el(".komunikat");
    pole.textContent = tekst;
    pole.className = "komunikat " + (czyBlad ? "zly" : "ok");
    pole.style.display = tekst ? "block" : "none";
  }

  // -------------------------------------------------------------- render
  function budujOkno() {
    host = document.createElement("div");
    host.id = "kabi-admin-host";
    document.body.appendChild(host);
    root = host.attachShadow({ mode: "open" });

    var style = document.createElement("style");
    style.textContent = STYLE;
    root.appendChild(style);

    var tlo = document.createElement("div");
    tlo.className = "tlo";
    tlo.innerHTML =
      '<div class="okno">' +
      '  <div class="lewa">' +
      '    <div class="naglowek">' +
      '      <button class="zakladka akt" data-widok="artykuly">Artykuły</button>' +
      '      <button class="zakladka" data-widok="referencje">Referencje</button>' +
      '    </div>' +
      '    <input class="szukaj" type="text" placeholder="Szukaj artykułu…">' +
      '    <div class="lista"></div>' +
      '    <div style="padding:10px;border-top:1px solid rgba(255,255,255,.08)">' +
      '      <button class="nowy" style="width:100%">+ Nowy wpis</button></div>' +
      '  </div>' +
      '  <div class="prawa">' +
      '    <div class="pasek">' +
      '      <span class="adres rosnie"></span>' +
      '      <button class="podglad-wl">Podgląd</button>' +
      '      <button class="zapisz glowny">Zapisz</button>' +
      '      <button class="usun grozny">Usuń</button>' +
      '      <button class="zamknij">Zamknij</button>' +
      '    </div>' +
      '    <div class="form"></div>' +
      '  </div>' +
      '  <div class="podglad">' +
      '    <div class="podglad__pasek">' +
      '      <span>Podgląd strony</span>' +
      '      <span class="szer">' +
      '        <button data-szer="100%" class="akt">desktop</button>' +
      '        <button data-szer="768px">tablet</button>' +
      '        <button data-szer="390px">telefon</button>' +
      '      </span>' +
      '      <button class="podglad__max" title="Pełny ekran (Escape wraca)">⤢ Pełny ekran</button>' +
      '      <span class="podglad__stan"></span>' +
      '    </div>' +
      '    <iframe title="Podgląd artykułu" sandbox="allow-same-origin"></iframe>' +
      '  </div>' +
      '</div>';
    root.appendChild(tlo);

    tlo.addEventListener("mousedown", function (e) { if (e.target === tlo) zamknij(); });
    el(".zamknij").addEventListener("click", zamknij);
    el(".podglad-wl").addEventListener("click", przelaczPodglad);
    el(".podglad__max").addEventListener("click", function () { przelaczMax(); });

    // Wyjście z trybu pełnoekranowego klawiszem przeglądarki musi cofnąć
    // także nasz układ — inaczej panel zostałby zmaksymalizowany w oknie.
    document.addEventListener("fullscreenchange", function () {
      if (!document.fullscreenElement && maksymalny()) przelaczMax(false);
    });
    root.querySelectorAll(".szer button").forEach(function (b) {
      b.addEventListener("click", function () {
        root.querySelectorAll(".szer button").forEach(function (x) { x.classList.remove("akt"); });
        b.classList.add("akt");
        var ramka = el(".podglad iframe");
        ramka.style.width = b.dataset.szer;
        ramka.style.margin = b.dataset.szer === "100%" ? "0" : "0 auto";
      });
    });
    el(".nowy").addEventListener("click", function () {
      if (widok === "referencje") { refBiezaca = null; rysujFormularzReferencji(null); rysujListeReferencji(); }
      else wczytaj(null);
    });
    el(".zapisz").addEventListener("click", function () {
      widok === "referencje" ? zapiszReferencje() : zapisz();
    });
    root.querySelectorAll(".zakladka").forEach(function (b) {
      b.addEventListener("click", function () { przelaczWidok(b.dataset.widok); });
    });
    el(".usun").addEventListener("click", function () {
      widok === "referencje" ? usunReferencje() : usun();
    });
    el(".szukaj").addEventListener("input", function () {
      widok === "referencje" ? rysujListeReferencji() : rysujListe();
    });
  }

  function rysujListe() {
    var fraza = (el(".szukaj").value || "").toLowerCase();
    var lista = el(".lista");
    lista.innerHTML = "";
    stan.lista
      .filter(function (a) {
        return !fraza || (a.title + " " + a.slug).toLowerCase().indexOf(fraza) !== -1;
      })
      .forEach(function (a) {
        var poz = document.createElement("div");
        poz.className = "poz" + (stan.biezacy === a.slug ? " akt" : "") + (a.published ? "" : " ukryty");
        poz.innerHTML = "<strong></strong><small></small>";
        poz.querySelector("strong").textContent = a.title;
        poz.querySelector("small").textContent =
          a.slug + (a.category ? " · " + a.category : "") + (a.published ? "" : " · ukryty");
        poz.addEventListener("click", function () { wczytaj(a.slug); });
        lista.appendChild(poz);
      });
  }

  /** Wartości, które już występują w bazie — lista do wyboru zamiast wpisywania. */
  function istniejaceWartosci(kolumna) {
    var zbior = {};
    stan.lista.forEach(function (a) {
      if (a[kolumna]) zbior[a[kolumna]] = true;
    });
    return Object.keys(zbior).sort(function (x, y) { return x.localeCompare(y, "pl"); });
  }

  function poleListy(def, wartosc) {
    // Wartownik bez znakow specjalnych — wczesniej byl tu bajt zerowy,
    // przez ktory select.value nigdy nie dopasowywal opcji.
    var NOWY = "__nowy__";
    var pole = document.createElement("div");
    pole.dataset.kolumna = def.k;
    pole.innerHTML = "<label></label><select></select>" +
      '<input type="text" style="display:none;margin-top:6px" placeholder="nazwa nowego działu">' +
      (def.pomoc ? '<div class="pomoc"></div>' : "");
    pole.querySelector("label").textContent = def.label;
    if (def.pomoc) pole.querySelector(".pomoc").textContent = def.pomoc;

    var select = pole.querySelector("select");
    var wpis = pole.querySelector("input");
    var wartosci = istniejaceWartosci(def.k);
    // Wartość edytowanego wpisu może nie występować nigdzie indziej —
    // bez tego wypadłaby z listy i zapis po cichu by ją zmienił.
    if (wartosc && wartosci.indexOf(wartosc) === -1) wartosci.unshift(wartosc);

    select.innerHTML = '<option value="">(wybierz z listy)</option>';
    wartosci.forEach(function (v) {
      var opt = document.createElement("option");
      opt.value = v;
      opt.textContent = v;
      if (v === wartosc) opt.selected = true;
      select.appendChild(opt);
    });
    var nowy = document.createElement("option");
    nowy.value = NOWY;
    nowy.textContent = "+ dodaj nowy dział…";
    select.appendChild(nowy);

    select.addEventListener("change", function () {
      if (select.value === NOWY) {
        wpis.style.display = "";
        wpis.value = "";
        wpis.focus();
        stan.zmiany[def.k] = "";
      } else {
        wpis.style.display = "none";
        stan.zmiany[def.k] = select.value;
      }
      zaplanujPodglad();
    });
    wpis.addEventListener("input", function () {
      stan.zmiany[def.k] = wpis.value;
      zaplanujPodglad();
    });
    return pole;
  }

  // ============================================== wizualny edytor treści
  // Redaktor nie powinien pisać znaczników. Pasek narzędzi produkuje pod
  // spodem dokładnie ten zestaw HTML-a, który dopuszcza i styluje serwis:
  // h2, h3, p, p.note, ul, ol, li, blockquote, hr, tabele, strong, em, s,
  // sub, sup, a, figure/img/figcaption.
  var DOZWOLONE = {
    H2: 1, H3: 1, P: 1, UL: 1, OL: 1, LI: 1, STRONG: 1, EM: 1, A: 1, BR: 1,
    FIGURE: 1, FIGCAPTION: 1, IMG: 1,
    BLOCKQUOTE: 1, HR: 1, S: 1, SUB: 1, SUP: 1,
    TABLE: 1, THEAD: 1, TBODY: 1, TR: 1, TH: 1, TD: 1
  };
  // Znaczniki równoważne mapujemy zamiast wyrzucać — wklejony tekst z Worda
  // albo innej strony zachowuje strukturę w granicach naszego słownika.
  var ZAMIENNIKI = { B: "STRONG", I: "EM", DIV: "P", H1: "H2", H4: "H3",
                     H5: "H3", H6: "H3", STRIKE: "S", DEL: "S", TFOOT: "TBODY" };

  // Wyrownanie i rozmiar zapisujemy KLASAMI, nie stylem inline: filtr i tak
  // wycina style, a zamkniety zestaw nazw gwarantuje, ze do tresci nie trafi
  // nic, czego CSS serwisu nie obsluguje.
  var KLASY_WYROWNANIA = ["tekst-srodek", "tekst-prawo"];
  var KLASY_ROZMIARU = ["foto-mala", "foto-srednia", "foto-pelna"];
  var KLASY_OBLEWANIA = ["foto-oblewa-lewo", "foto-oblewa-prawo"];

  function dozwolonaKlasa(nazwaZnacznika, wartosc) {
    var czesci = String(wartosc || "").split(/\s+/).filter(Boolean);
    if (!czesci.length) return false;
    return czesci.every(function (klasa) {
      if (klasa === "note") return nazwaZnacznika === "P";
      if (KLASY_WYROWNANIA.indexOf(klasa) !== -1) {
        // Na LI nie ma sensu — wyrownujemy cala liste.
        return nazwaZnacznika !== "LI";
      }
      if (KLASY_ROZMIARU.indexOf(klasa) !== -1) return nazwaZnacznika === "FIGURE";
      if (KLASY_OBLEWANIA.indexOf(klasa) !== -1) return nazwaZnacznika === "FIGURE";
      return false;
    });
  }

  function eskapujHtml(tekst) {
    return String(tekst == null ? "" : tekst)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  /** Rozpuszcza element, zachowując jego zawartość. */
  function rozpuscElement(wezel) {
    while (wezel.firstChild) wezel.parentNode.insertBefore(wezel.firstChild, wezel);
    wezel.parentNode.removeChild(wezel);
  }

  // Przegladarka potrafi zbudowac <p><ul>…</ul></p> albo <p><p>…</p></p>.
  // To niedozwolone zagniezdzenie: przy nastepnej edycji przegladarka je
  // rozrywa i lista przepada. Rozpuszczamy akapit, ktory zawiera blok.
  var BLOKI_W_AKAPICIE = { P: 1, UL: 1, OL: 1, H2: 1, H3: 1, FIGURE: 1,
                           BLOCKQUOTE: 1, TABLE: 1, HR: 1 };

  function rozbijAkapityZBlokami(korzen) {
    for (var runda = 0; runda < 5; runda++) {
      var winowajcy = [].slice.call(korzen.querySelectorAll("p")).filter(function (p) {
        return [].slice.call(p.children).some(function (dziecko) {
          return BLOKI_W_AKAPICIE[dziecko.tagName];
        });
      });
      if (!winowajcy.length) break;
      winowajcy.forEach(rozpuscElement);
    }
  }

  /** Sprowadza to, co wyprodukuje contenteditable, do dozwolonego HTML-a.
   *  UWAGA: mutuje przekazany wezel — wolaj na klonie albo kuble roboczym,
   *  nigdy na zywym DOM edytora (przestawianie wezlow gubi kursor). */
  function oczysc(korzen) {
    var dokument = korzen.ownerDocument;

    // Te znaczniki usuwamy RAZEM z zawartoscia. Rozpuszczenie ich zostawiloby
    // kod (albo kontrolki formularza) jako widoczny tekst artykulu.
    var DO_WYRZUCENIA = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, IFRAME: 1, OBJECT: 1,
                          EMBED: 1, FORM: 1, INPUT: 1, BUTTON: 1, SELECT: 1,
                          TEXTAREA: 1, VIDEO: 1, AUDIO: 1, CANVAS: 1, SVG: 1,
                          LINK: 1, META: 1, TITLE: 1, COLGROUP: 1, COL: 1 };

    (function przejdz(wezel) {
      var dzieci = [].slice.call(wezel.childNodes);
      dzieci.forEach(przejdz);

      if (wezel === korzen) return;
      // Komentarze (m.in. warunkowe Worda) nie mogą trafić do treści.
      if (wezel.nodeType === 8) {
        wezel.parentNode.removeChild(wezel);
        return;
      }
      if (wezel.nodeType !== 1) return;
      var nazwa = wezel.tagName;

      if (DO_WYRZUCENIA[nazwa]) {
        wezel.parentNode.removeChild(wezel);
        return;
      }

      if (ZAMIENNIKI[nazwa]) {
        var nowy = dokument.createElement(ZAMIENNIKI[nazwa]);
        while (wezel.firstChild) nowy.appendChild(wezel.firstChild);
        wezel.parentNode.replaceChild(nowy, wezel);
        wezel = nowy;
        nazwa = wezel.tagName;
      }

      if (!DOZWOLONE[nazwa]) {
        // Nieznany znacznik (span, font, style…) rozpuszczamy, zachowując treść.
        rozpuscElement(wezel);
        return;
      }

      [].slice.call(wezel.attributes).forEach(function (atr) {
        var zostaje =
          (nazwa === "A" && (atr.name === "href" || atr.name === "target" || atr.name === "rel")) ||
          (atr.name === "class" && dozwolonaKlasa(nazwa, atr.value)) ||
          (nazwa === "IMG" && (atr.name === "src" || atr.name === "alt" ||
                               atr.name === "loading" || atr.name === "width" ||
                               atr.name === "height"));
        // colspan/rowspan celowo NIE przechodzą: pasek tabeli zakłada równą
        // siatkę, a scalone komórki z wklejenia rozjechałyby dodawanie wierszy
        // i kolumn. Bez tych atrybutów komórka po prostu nie łączy się z sąsiadem.
        if (!zostaje) wezel.removeAttribute(atr.name);
      });
      // Adres z wklejonego kodu może przemycić niebezpieczny schemat. Przed
      // testem usuwamy białe znaki i znaki sterujące — przeglądarka i tak je
      // pomija przy rozwiązywaniu URL, więc „java&#9;script:" byłby aktywny.
      if (nazwa === "A") {
        var adres = (wezel.getAttribute("href") || "").replace(/[\x00-\x20]+/g, "");
        if (/^(javascript|data|vbscript):/i.test(adres)) wezel.removeAttribute("href");
      }
    })(korzen);

    rozbijAkapityZBlokami(korzen);

    // Tekst i elementy liniowe lezace bezposrednio w korzeniu opakowujemy
    // w akapit — inaczej trafilyby na strone poza jakimkolwiek blokiem.
    // Osierocone <li> (z wklejenia albo widoku kodu) zbieramy w <ul>, bo
    // <p><li> to niedozwolone zagniezdzenie, ktore przegladarka rozrywa.
    var BLOKOWE = { H2: 1, H3: 1, P: 1, UL: 1, OL: 1, FIGURE: 1,
                    BLOCKQUOTE: 1, TABLE: 1, HR: 1 };
    var biezacy = null, lista = null;
    [].slice.call(korzen.childNodes).forEach(function (wezel) {
      var pusty = wezel.nodeType === 3 && !wezel.nodeValue.trim();
      if (pusty) { biezacy = null; return; }
      if (wezel.nodeType === 1 && wezel.tagName === "LI") {
        biezacy = null;
        if (!lista) {
          lista = dokument.createElement("ul");
          korzen.insertBefore(lista, wezel);
        }
        lista.appendChild(wezel);
        return;
      }
      lista = null;
      if (wezel.nodeType === 1 && BLOKOWE[wezel.tagName]) { biezacy = null; return; }
      if (!biezacy) {
        biezacy = dokument.createElement("p");
        korzen.insertBefore(biezacy, wezel);
      }
      biezacy.appendChild(wezel);
    });

    return korzen.innerHTML
      .replace(/<p>(\s|&nbsp;|<br\s*\/?>)*<\/p>/gi, "")
      .trim();
  }

  /** Czyści HTML podany jako tekst (widok kodu, wklejanie). */
  function oczyscHtml(html) {
    var kubel = document.createElement("div");
    kubel.innerHTML = html || "";
    return oczysc(kubel);
  }

  /** Owija element w nowy znacznik i zwraca owijkę. */
  function owin(wezel, znacznik) {
    var nowy = wezel.ownerDocument.createElement(znacznik);
    wezel.parentNode.insertBefore(nowy, wezel);
    nowy.appendChild(wezel);
    return nowy;
  }

  /** Przygotowuje wklejony HTML: zanim filtr rozpuści <span>y z Worda
   *  i Dokumentów Google, odzyskujemy z ich stylów pogrubienie, kursywę,
   *  przekreślenie i indeksy. */
  function przygotujWklejone(kubel) {
    [].slice.call(kubel.querySelectorAll("span[style],font[style]")).forEach(function (el) {
      var styl = el.getAttribute("style") || "";
      var cel = el;
      if (/font-weight\s*:\s*(bold|bolder|[6-9]00)/i.test(styl)) cel = owin(cel, "strong");
      if (/font-style\s*:\s*(italic|oblique)/i.test(styl)) cel = owin(cel, "em");
      if (/text-decoration[^;]*line-through/i.test(styl)) cel = owin(cel, "s");
      if (/vertical-align\s*:\s*sub/i.test(styl)) cel = owin(cel, "sub");
      if (/vertical-align\s*:\s*super/i.test(styl)) cel = owin(cel, "sup");
    });
    // Dokumenty Google opakowują całość w <b style="font-weight:normal"> —
    // to kontener, nie pogrubienie. Rozpuszczamy, zanim filtr zrobi z niego
    // <strong> na całym tekście.
    [].slice.call(kubel.querySelectorAll("b")).forEach(function (b) {
      if (/font-weight\s*:\s*(normal|400)/i.test(b.getAttribute("style") || "")) {
        rozpuscElement(b);
      }
    });
  }

  function poleRedaktor(def, wartosc) {
    var pole = document.createElement("div");
    pole.dataset.kolumna = def.k;
    pole.innerHTML =
      "<label></label>" +
      '<div class="red">' +
      '  <div class="red__gora">' +
      '    <div class="red__pasek"></div>' +
      '    <div class="red__kontekst"></div>' +
      "  </div>" +
      '  <div class="red__tresc" contenteditable="true" data-placeholder="Zacznij pisać…  Ukośnik „/” otwiera menu wstawiania."></div>' +
      '  <textarea class="red__kod" style="display:none" spellcheck="false"></textarea>' +
      '  <div class="red__stopka"></div>' +
      "</div>" +
      (def.pomoc ? '<div class="pomoc"></div>' : "");
    pole.querySelector("label").textContent = def.label;
    if (def.pomoc) pole.querySelector(".pomoc").textContent = def.pomoc;

    var red = pole.querySelector(".red");
    var pasek = pole.querySelector(".red__pasek");
    var kontekst = pole.querySelector(".red__kontekst");
    var tresc = pole.querySelector(".red__tresc");
    var kod = pole.querySelector(".red__kod");
    var stopka = pole.querySelector(".red__stopka");
    tresc.innerHTML = wartosc || "";

    // Enter ma tworzyć <p>, nie <div>. Deklaracja działa na cały dokument
    // i jest idempotentna — wywołanie przy każdym edytorze nie szkodzi.
    try { document.execCommand("defaultParagraphSeparator", false, "p"); } catch (e) {}

    /** Zaznaczenie dokumentu (może być poza edytorem). */
    function wyborDokumentu() {
      var korzen = tresc.getRootNode();
      return (korzen && korzen.getSelection) ? korzen.getSelection()
                                             : tresc.ownerDocument.getSelection();
    }

    /** Zaznaczenie widoczne WEWNATRZ Shadow DOM.
     *  document.getSelection() zwraca tu zaznaczenie przekierowane na hosta,
     *  przez co anchorNode nigdy nie trafia w wezel edytora. */
    function zaznaczenie() {
      var sel = wyborDokumentu();
      return sel && sel.anchorNode && tresc.contains(sel.anchorNode) ? sel : null;
    }

    function blokKursora() {
      var sel = zaznaczenie();
      var wezel = sel && sel.anchorNode;
      while (wezel && wezel !== tresc) {
        if (wezel.nodeType === 1 && BLOKI_TRESCI[wezel.tagName]) return wezel;
        wezel = wezel.parentNode;
      }
      return null;
    }

    function przodek(znacznik) {
      var sel = zaznaczenie();
      var wezel = sel && sel.anchorNode;
      while (wezel && wezel !== tresc) {
        if (wezel.nodeType === 1 && wezel.tagName === znacznik) return wezel;
        wezel = wezel.parentNode;
      }
      return null;
    }

    /** Element najwyższego poziomu (dziecko korzenia), w którym stoi kursor. */
    function blokNajwyzszy() {
      var sel = zaznaczenie();
      var wezel = sel && sel.anchorNode;
      if (!wezel) return null;
      if (wezel === tresc) {
        return tresc.childNodes[Math.min(sel.anchorOffset, tresc.childNodes.length - 1)] || null;
      }
      while (wezel.parentNode && wezel.parentNode !== tresc) wezel = wezel.parentNode;
      return wezel.parentNode === tresc ? wezel : null;
    }

    function blokNadrzedny(wezel) {
      while (wezel && wezel.parentNode !== tresc) wezel = wezel.parentNode;
      return wezel;
    }

    /** Najbliższy blok treści (akapit, nagłówek, komórka, punkt listy…).
     *  Do odnośnika liczy się TEN blok, nie element najwyższego poziomu:
     *  dwa punkty tej samej listy mają wspólny blok najwyższy (UL), a mimo
     *  to odnośnik przez ich granicę rozrywałby strukturę. */
    function blokTekstu(wezel) {
      while (wezel && wezel !== tresc) {
        if (wezel.nodeType === 1 && BLOKI_TRESCI[wezel.tagName]) return wezel;
        wezel = wezel.parentNode;
      }
      return null;
    }

    function kursorNaPoczatek(wezel) {
      var sel = wyborDokumentu();
      if (!sel || !wezel) return;
      var zakres = tresc.ownerDocument.createRange();
      zakres.setStart(wezel, 0);
      zakres.collapse(true);
      sel.removeAllRanges();
      sel.addRange(zakres);
    }

    // ------------------------------------------------ kursor: zapis i odczyt
    function dlugoscWezla(w) {
      return w.nodeType === 3 ? w.nodeValue.length : w.childNodes.length;
    }

    function sciezkaWezla(wezel) {
      var sciezka = [];
      while (wezel && wezel !== tresc) {
        var rodzic = wezel.parentNode;
        if (!rodzic) return null;
        sciezka.unshift([].indexOf.call(rodzic.childNodes, wezel));
        wezel = rodzic;
      }
      return wezel === tresc ? sciezka : null;
    }

    function wezelZeSciezki(sciezka) {
      var wezel = tresc;
      for (var i = 0; i < sciezka.length; i++) {
        wezel = wezel.childNodes[sciezka[i]];
        if (!wezel) return null;
      }
      return wezel;
    }

    function zapamietajKursor() {
      var sel = zaznaczenie();
      if (!sel || !sel.rangeCount) return null;
      var zakres = sel.getRangeAt(0);
      var pocz = sciezkaWezla(zakres.startContainer);
      var kon = sciezkaWezla(zakres.endContainer);
      if (!pocz || !kon) return null;
      return { p: pocz, po: zakres.startOffset, k: kon, ko: zakres.endOffset };
    }

    function przywrocKursor(zapis) {
      if (!zapis) return;
      var pocz = wezelZeSciezki(zapis.p);
      var kon = wezelZeSciezki(zapis.k);
      if (!pocz || !kon) return;
      try {
        var zakres = tresc.ownerDocument.createRange();
        zakres.setStart(pocz, Math.min(zapis.po, dlugoscWezla(pocz)));
        zakres.setEnd(kon, Math.min(zapis.ko, dlugoscWezla(kon)));
        var sel = wyborDokumentu();
        sel.removeAllRanges();
        sel.addRange(zakres);
      } catch (e) { /* nieaktualna ścieżka nie może wywalić edytora */ }
    }

    /** Wykonuje operację przestawiającą węzły i zachowuje kursor.
     *  Trzymamy REFERENCJE węzłów granicznych, nie ścieżki: operacje typu
     *  akapit→nagłówek/lista przenoszą te same węzły tekstu (zachowują
     *  tożsamość), za to indeksy w drzewie się zmieniają, więc ścieżka by
     *  zawiodła. Bez tego kursor skakał na początek przerobionego bloku. */
    function zachowajKursor(operacja) {
      var sel = zaznaczenie();
      var z = sel && sel.rangeCount ? sel.getRangeAt(0) : null;
      var zapis = z ? { pn: z.startContainer, po: z.startOffset,
                        kn: z.endContainer, ko: z.endOffset } : null;
      operacja();
      if (!zapis || !tresc.contains(zapis.pn) || !tresc.contains(zapis.kn)) return;
      try {
        var zakres = tresc.ownerDocument.createRange();
        zakres.setStart(zapis.pn, Math.min(zapis.po, dlugoscWezla(zapis.pn)));
        zakres.setEnd(zapis.kn, Math.min(zapis.ko, dlugoscWezla(zapis.kn)));
        var s2 = wyborDokumentu();
        s2.removeAllRanges();
        s2.addRange(zakres);
      } catch (e) { /* przeniesiony węzeł mógł zniknąć — trudno */ }
    }

    // --------------------------------------------------- historia (cofanie)
    // Własny stos zamiast przeglądarkowego: operacje przestawiające DOM
    // (listy, tabele, wyrównanie) i tak wypadają z natywnego Ctrl+Z.
    var historia = [], histPozycja = -1, histTimer = null;

    function utrwalHistorie() {
      clearTimeout(histTimer);
      histTimer = null;
      // Migawka z oczyszczonego klonu — inaczej klasa „red-fig-akt" bieżącego
      // zaznaczenia zdjęcia trafiłaby do historii i po cofnięciu zostawałaby
      // widmowa ramka wokół obrazka, którego nikt nie zaznaczył.
      var klon = tresc.cloneNode(true);
      [].slice.call(klon.querySelectorAll(".red-fig-akt")).forEach(function (f) {
        f.classList.remove("red-fig-akt");
        if (!f.getAttribute("class")) f.removeAttribute("class");
      });
      var html = klon.innerHTML;
      if (histPozycja >= 0 && historia[histPozycja].html === html) return;
      historia.splice(histPozycja + 1);
      historia.push({ html: html, kursor: zapamietajKursor() });
      if (historia.length > 200) historia.shift();
      histPozycja = historia.length - 1;
      odswiezPasek();
    }

    function migawka(natychmiast) {
      clearTimeout(histTimer);
      if (natychmiast) utrwalHistorie();
      else histTimer = setTimeout(utrwalHistorie, 400);
    }

    function przejdzHistorie(krok) {
      if (kod.style.display !== "none") return;   // historia tylko w trybie wizualnym
      if (histTimer) utrwalHistorie();   // dopisz trwające pisanie przed skokiem
      var cel = histPozycja + krok;
      if (cel < 0 || cel >= historia.length) return;
      odznaczFigure();
      histPozycja = cel;
      tresc.innerHTML = historia[cel].html;
      przywrocKursor(historia[cel].kursor);
      zadbajOPustke();
      zapiszStan();
      odswiezPasek();
    }

    function cofnij() { przejdzHistorie(-1); }
    function ponow() { przejdzHistorie(1); }

    // ------------------------------------------------------------ zapis
    function zapiszStan() {
      if (kod.style.display !== "none") {
        stan.zmiany[def.k] = oczyscHtml(kod.value);
      } else {
        var klon = tresc.cloneNode(true);
        [].slice.call(klon.querySelectorAll(".red-fig-akt")).forEach(function (f) {
          f.classList.remove("red-fig-akt");
          if (!f.getAttribute("class")) f.removeAttribute("class");
        });
        stan.zmiany[def.k] = oczysc(klon);
      }
      odswiezStopke();
      zaplanujPodglad();
    }

    /** Wspólne zakończenie każdej operacji strukturalnej. */
    function utrwalZmiane() {
      zadbajOPustke();
      zapiszStan();
      migawka(true);
      odswiezPasek();
    }

    function polecenie(cmd) {
      tresc.focus();
      try { document.execCommand(cmd, false, null); } catch (e) {}
      utrwalZmiane();
    }

    // ------------------------------------------------------- pusty edytor
    function zadbajOPustke() {
      var pusto = !tresc.textContent.trim() && !tresc.querySelector("img,table,hr,li");
      if (pusto && !tresc.querySelector("p")) {
        tresc.innerHTML = "<p><br></p>";
        if (zaznaczenie() !== null) kursorNaPoczatek(tresc.querySelector("p"));
      }
      tresc.classList.toggle("pusty", pusto);
    }

    // ------------------------------------------------------- pasek narzędzi
    function przycisk(kontener, etykieta, tytul, dzialanie, klasa) {
      var b = document.createElement("button");
      b.type = "button";
      if (klasa) b.className = klasa;
      b.innerHTML = etykieta;   // etykiety to nasze stałe, nie dane użytkownika
      b.title = tytul;
      // mousedown zamiast click: klik najpierw zabrałby zaznaczenie tekstu,
      // a bez zaznaczenia polecenia formatujące nie mają na czym działać.
      b.addEventListener("mousedown", function (e) { e.preventDefault(); dzialanie(); });
      b.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); dzialanie(); }
      });
      kontener.appendChild(b);
      return b;
    }

    function grupa() {
      var g = document.createElement("span");
      g.className = "grupa";
      pasek.appendChild(g);
      return g;
    }

    /** Akapit ↔ nagłówek ↔ podtytuł; ponowne kliknięcie wraca do akapitu. */
    function ustawBlok(znacznik) {
      var bloki = blokiZaznaczenia().filter(function (b) {
        return b.tagName === "P" || b.tagName === "H2" || b.tagName === "H3";
      });
      if (!bloki.length) {
        komunikat("Ustaw kursor w akapicie albo nagłówku.", true);
        return;
      }
      var cel = znacznik;
      if (bloki.every(function (b) { return b.tagName === znacznik; })) cel = "P";
      zachowajKursor(function () {
        bloki.forEach(function (blok) {
          if (blok.tagName === cel) return;
          var nowy = tresc.ownerDocument.createElement(cel);
          // Wyrównanie zostaje, „note” nie ma sensu na nagłówku.
          var klasy = (blok.getAttribute("class") || "").split(/\s+/).filter(function (k) {
            return KLASY_WYROWNANIA.indexOf(k) !== -1 || (cel === "P" && k === "note");
          }).join(" ");
          if (klasy) nowy.setAttribute("class", klasy);
          while (blok.firstChild) nowy.appendChild(blok.firstChild);
          blok.parentNode.replaceChild(nowy, blok);
        });
      });
      utrwalZmiane();
    }
    /** Zamienia bloki objete zaznaczeniem w liste (albo liste z powrotem
     *  w akapity, albo liste jednego rodzaju w drugi). Robimy to sami, bo
     *  execCommand potrafi zbudowac <p><ul>…</ul></p>, co rozpada sie przy
     *  nastepnej edycji. */
    function przelaczListe(znacznik) {
      var bloki = blokiZaznaczenia();
      if (!bloki.length) {
        komunikat("Ustaw kursor w tekście, który ma być listą.", true);
        return;
      }

      var lista = bloki[0].closest && bloki[0].closest("ul,ol");
      if (lista && tresc.contains(lista)) {
        zachowajKursor(function () {
          if (lista.tagName === znacznik) {
            // Ta sama lista → rozbijamy na akapity.
            [].slice.call(lista.children).forEach(function (li) {
              var p = tresc.ownerDocument.createElement("p");
              while (li.firstChild) p.appendChild(li.firstChild);
              lista.parentNode.insertBefore(p, lista);
            });
            lista.parentNode.removeChild(lista);
          } else {
            // Inny rodzaj → podmieniamy znacznik listy.
            var inna = tresc.ownerDocument.createElement(znacznik);
            while (lista.firstChild) inna.appendChild(lista.firstChild);
            lista.parentNode.replaceChild(inna, lista);
          }
        });
        utrwalZmiane();
        return;
      }

      var doListy = bloki.filter(function (b) {
        return b.tagName === "P" || b.tagName === "H2" || b.tagName === "H3";
      });
      if (!doListy.length) {
        komunikat("Ustaw kursor w akapicie, który ma być listą.", true);
        return;
      }
      zachowajKursor(function () {
        var nowa = tresc.ownerDocument.createElement(znacznik);
        doListy[0].parentNode.insertBefore(nowa, doListy[0]);
        doListy.forEach(function (blok) {
          var li = tresc.ownerDocument.createElement("li");
          while (blok.firstChild) li.appendChild(blok.firstChild);
          nowa.appendChild(li);
          blok.parentNode.removeChild(blok);
        });
      });
      utrwalZmiane();
    }

    function przelaczCytat() {
      var cytat = przodek("BLOCKQUOTE");
      if (cytat) {
        zachowajKursor(function () { rozpuscElement(cytat); });
        utrwalZmiane();
        return;
      }
      var bloki = blokiZaznaczenia().filter(function (b) {
        return b.parentNode === tresc && b.tagName !== "FIGURE";
      });
      if (!bloki.length) {
        komunikat("Ustaw kursor w akapicie, który ma być cytatem.", true);
        return;
      }
      zachowajKursor(function () {
        var nowy = tresc.ownerDocument.createElement("blockquote");
        bloki[0].parentNode.insertBefore(nowy, bloki[0]);
        bloki.forEach(function (b) { nowy.appendChild(b); });
      });
      utrwalZmiane();
    }

    function przelaczNote() {
      var bloki = blokiZaznaczenia().filter(function (b) { return b.tagName === "P"; });
      if (!bloki.length) {
        komunikat("Wyróżnienie działa na zwykłym akapicie tekstu — ustaw w nim kursor.", true);
        return;
      }
      var wlaczyc = !bloki.every(function (b) { return b.classList.contains("note"); });
      bloki.forEach(function (b) {
        b.classList.toggle("note", wlaczyc);
        if (!b.getAttribute("class")) b.removeAttribute("class");
      });
      utrwalZmiane();
    }

    var BLOKI_TRESCI = { P: 1, H2: 1, H3: 1, LI: 1, FIGURE: 1, BLOCKQUOTE: 1,
                         TD: 1, TH: 1 };

    /** WSZYSTKIE bloki objete zaznaczeniem, nie tylko ten z kursorem —
     *  inaczej zaznaczenie trzech akapitow wyrownywaloby jeden. */
    function blokiZaznaczenia() {
      var sel = zaznaczenie();
      if (!sel || !sel.rangeCount) return [];
      var zakres = sel.getRangeAt(0);

      var wszystkie = [].slice.call(
        tresc.querySelectorAll("p,h2,h3,li,figure,blockquote,td,th"));
      var objete = wszystkie.filter(function (blok) {
        return zakres.intersectsNode ? zakres.intersectsNode(blok)
                                     : zakres.commonAncestorContainer.contains(blok);
      });
      // Zagniezdzone bloki (li wewnatrz zaznaczonego ul) liczymy raz.
      objete = objete.filter(function (blok) {
        return !objete.some(function (inny) { return inny !== blok && inny.contains(blok); });
      });
      if (objete.length) return objete;

      var wezel = sel.anchorNode;
      while (wezel && wezel !== tresc) {
        if (wezel.nodeType === 1 && BLOKI_TRESCI[wezel.tagName]) return [wezel];
        wezel = wezel.parentNode;
      }
      return [];
    }

    function wyrownaj(klasa) {
      var bloki = blokiZaznaczenia();
      if (!bloki.length) {
        komunikat("Ustaw kursor w akapicie, który chcesz wyrównać.", true);
        return;
      }
      var cele = [];
      bloki.forEach(function (blok) {
        // Pozycja listy: wyrownujemy CALA liste, nie pojedynczy punkt.
        // Inaczej punktor zostaje przy lewej krawedzi, a tekst ucieka
        // na prawo — dokladnie tak wyglada zepsuty sklad.
        var cel = blok.tagName === "LI" ? blok.parentNode : blok;
        if (cele.indexOf(cel) === -1) cele.push(cel);
        if (cel !== blok) {
          KLASY_WYROWNANIA.forEach(function (k) { blok.classList.remove(k); });
          if (!blok.getAttribute("class")) blok.removeAttribute("class");
        }
      });
      cele.forEach(function (cel) {
        KLASY_WYROWNANIA.forEach(function (k) { cel.classList.remove(k); });
        if (klasa) cel.classList.add(klasa);
        if (!cel.getAttribute("class")) cel.removeAttribute("class");
      });
      utrwalZmiane();
    }

    // ------------------------------------------------------ wstawianie bloków
    /** Wstawia element blokowy za bieżącym blokiem. Pusty akapit pod kursorem
     *  ląduje ZA wstawianym elementem, żeby dało się pisać dalej. */
    function wstawBlok(element) {
      var biezacy = blokNajwyzszy();
      if (biezacy && biezacy.nodeType === 1 && biezacy.tagName === "P" &&
          !biezacy.textContent.trim() && !biezacy.querySelector("img")) {
        tresc.insertBefore(element, biezacy);
        kursorNaPoczatek(biezacy);
      } else if (biezacy) {
        tresc.insertBefore(element, biezacy.nextSibling);
        var akapit = tresc.ownerDocument.createElement("p");
        akapit.innerHTML = "<br>";
        tresc.insertBefore(akapit, element.nextSibling);
        kursorNaPoczatek(akapit);
      } else {
        tresc.appendChild(element);
        var koncowy = tresc.ownerDocument.createElement("p");
        koncowy.innerHTML = "<br>";
        tresc.appendChild(koncowy);
        kursorNaPoczatek(koncowy);
      }
      utrwalZmiane();
      return element;
    }

    function wstawLinie() {
      wstawBlok(tresc.ownerDocument.createElement("hr"));
    }

    // ------------------------------------------------------------- tabele
    function komorkaKursora() { return przodek("TD") || przodek("TH"); }

    function zamienZnacznik(stary, nowyTag) {
      var nowy = stary.ownerDocument.createElement(nowyTag);
      while (stary.firstChild) nowy.appendChild(stary.firstChild);
      [].slice.call(stary.attributes).forEach(function (a) {
        nowy.setAttribute(a.name, a.value);
      });
      stary.parentNode.replaceChild(nowy, stary);
      return nowy;
    }

    function wstawTabele(wierszy, kolumn) {
      var dok = tresc.ownerDocument;
      var tabela = dok.createElement("table");
      var thead = dok.createElement("thead");
      var naglowek = dok.createElement("tr");
      for (var k = 0; k < kolumn; k++) {
        var th = dok.createElement("th");
        th.innerHTML = "<br>";
        naglowek.appendChild(th);
      }
      thead.appendChild(naglowek);
      tabela.appendChild(thead);
      var tbody = dok.createElement("tbody");
      for (var w = 0; w < wierszy; w++) {
        var wiersz = dok.createElement("tr");
        for (var k2 = 0; k2 < kolumn; k2++) {
          var td = dok.createElement("td");
          td.innerHTML = "<br>";
          wiersz.appendChild(td);
        }
        tbody.appendChild(wiersz);
      }
      tabela.appendChild(tbody);
      wstawBlok(tabela);
      kursorNaPoczatek(tabela.querySelector("th,td"));
      odswiezPasek();
    }

    function tabelaOp(op) {
      var komorka = komorkaKursora();
      if (!komorka) return;
      var tabela = komorka.closest("table");
      var wiersz = komorka.parentNode;
      var indeks = [].indexOf.call(wiersz.cells, komorka);
      var dok = tresc.ownerDocument;

      function nowaKomorka(znacznik) {
        var kom = dok.createElement(znacznik);
        kom.innerHTML = "<br>";
        return kom;
      }

      if (op === "wiersz+") {
        var nowy = dok.createElement("tr");
        for (var i = 0; i < wiersz.cells.length; i++) nowy.appendChild(nowaKomorka("td"));
        if (wiersz.parentNode.tagName === "THEAD") {
          var tbody = tabela.querySelector("tbody");
          if (!tbody) { tbody = dok.createElement("tbody"); tabela.appendChild(tbody); }
          tbody.insertBefore(nowy, tbody.firstChild);
        } else {
          wiersz.parentNode.insertBefore(nowy, wiersz.nextSibling);
        }
        kursorNaPoczatek(nowy.cells[Math.min(indeks, nowy.cells.length - 1)]);
      } else if (op === "wiersz-") {
        wiersz.parentNode.removeChild(wiersz);
        if (!tabela.querySelector("td,th")) tabela.parentNode.removeChild(tabela);
        else kursorNaPoczatek(tabela.querySelector("td,th"));
      } else if (op === "kolumna+") {
        [].slice.call(tabela.rows).forEach(function (w2) {
          var wzor = w2.cells[Math.min(indeks, w2.cells.length - 1)];
          var kom = nowaKomorka(wzor ? wzor.tagName : "TD");
          w2.insertBefore(kom, wzor ? wzor.nextSibling : null);
        });
        kursorNaPoczatek(wiersz.cells[indeks + 1]);
      } else if (op === "kolumna-") {
        if (wiersz.cells.length <= 1) {
          tabela.parentNode.removeChild(tabela);
        } else {
          [].slice.call(tabela.rows).forEach(function (w3) {
            if (w3.cells[indeks]) w3.removeChild(w3.cells[indeks]);
          });
          kursorNaPoczatek(wiersz.cells[Math.max(0, indeks - 1)]);
        }
      } else if (op === "naglowek") {
        var thead = tabela.querySelector("thead");
        if (thead) {
          var cialo = tabela.querySelector("tbody");
          if (!cialo) { cialo = dok.createElement("tbody"); tabela.appendChild(cialo); }
          [].slice.call(thead.rows).forEach(function (w4) {
            [].slice.call(w4.cells).forEach(function (kom) { zamienZnacznik(kom, "td"); });
            cialo.insertBefore(w4, cialo.firstChild);
          });
          thead.parentNode.removeChild(thead);
        } else {
          var pierwszy = tabela.rows[0];
          if (pierwszy) {
            [].slice.call(pierwszy.cells).forEach(function (kom) { zamienZnacznik(kom, "th"); });
            var nowyThead = dok.createElement("thead");
            nowyThead.appendChild(pierwszy);
            tabela.insertBefore(nowyThead, tabela.firstChild);
          }
        }
      } else if (op === "usun") {
        tabela.parentNode.removeChild(tabela);
      }
      utrwalZmiane();
    }

    function tabWTabeli(e) {
      var komorka = komorkaKursora();
      if (!komorka) return false;
      e.preventDefault();
      var tabela = komorka.closest("table");
      var komorki = [].slice.call(tabela.querySelectorAll("th,td"));
      var i = komorki.indexOf(komorka) + (e.shiftKey ? -1 : 1);
      if (i < 0) return true;
      if (i >= komorki.length) { tabelaOp("wiersz+"); return true; }
      var sel = wyborDokumentu();
      var zakres = tresc.ownerDocument.createRange();
      zakres.selectNodeContents(komorki[i]);
      sel.removeAllRanges();
      sel.addRange(zakres);
      odswiezPasek();
      return true;
    }

    // ------------------------------------------------------------- zdjęcia
    var wybranaFigura = null;

    function odznaczFigure() {
      if (!wybranaFigura) return;
      wybranaFigura.classList.remove("red-fig-akt");
      if (!wybranaFigura.getAttribute("class")) wybranaFigura.removeAttribute("class");
      wybranaFigura = null;
    }

    function zaznaczFigure(figura) {
      if (wybranaFigura === figura) return;
      odznaczFigure();
      wybranaFigura = figura;
      figura.classList.add("red-fig-akt");
      odswiezKontekst();
    }

    function usunFigure() {
      if (!wybranaFigura) return;
      var nastepny = wybranaFigura.nextElementSibling;
      wybranaFigura.parentNode.removeChild(wybranaFigura);
      wybranaFigura = null;
      if (nastepny) kursorNaPoczatek(nastepny);
      utrwalZmiane();
    }

    function wgrajGrafike(plik, gotowe) {
      if (!plik || (plik.type && plik.type.indexOf("image/") !== 0)) {
        komunikat("To nie wygląda na obraz — przyjmuję JPG, PNG, WEBP i GIF.", true);
        return;
      }
      // Limit sprawdzamy po stronie klienta (spójny z GRAFIKA_LIMIT_MB w API):
      // inaczej serwer odrzucał plik dopiero po przesłaniu ~4/3 jego rozmiaru,
      // a przy >48 MB nginx ucinał żądanie surowym błędem 413.
      if (plik.size > 20 * 1024 * 1024) {
        komunikat("Plik ma " + (plik.size / 1048576).toFixed(1) +
                  " MB — limit to 20 MB. Zmniejsz obraz i spróbuj ponownie.", true);
        return;
      }
      komunikat("Wgrywam " + plik.name + "…", false);
      var czytnik = new FileReader();
      czytnik.onload = function () {
        api("grafiki/wgraj", { metoda: "POST", dane: {
          nazwa: plik.name,
          dane: String(czytnik.result).split(",")[1]
        }}).then(function (w) {
          var nowa = { url: w.url, nazwa: w.nazwa, grupa: "wgrane",
                       rozmiar_kb: w.rozmiar_kb };
          stan.grafiki.unshift(nowa);
          komunikat(w.komunikat, false);
          gotowe(nowa);
        }).catch(function (e) {
          komunikat("Nie udało się wgrać: " + e.message, true);
        });
      };
      czytnik.readAsDataURL(plik);
    }

    // ------------------------------------------------------- okna dialogowe
    function otworzNakladke() {
      var nakladka = document.createElement("div");
      nakladka.className = "red-nakladka";
      var dialog = document.createElement("div");
      dialog.className = "red-dialog";
      nakladka.appendChild(dialog);
      function zamknijN() { nakladka.remove(); tresc.focus(); }
      nakladka._zamknij = zamknijN;
      nakladka.addEventListener("mousedown", function (e) {
        if (e.target === nakladka) zamknijN();
      });
      nakladka.addEventListener("keydown", function (e) {
        if (e.key === "Escape") { e.stopPropagation(); zamknijN(); }
      });
      root.appendChild(nakladka);
      return { nakladka: nakladka, dialog: dialog, zamknij: zamknijN };
    }

    function utworzLink(url, nowaKarta) {
      var sel = zaznaczenie();
      if (!sel || sel.isCollapsed) return;
      var zakres = sel.getRangeAt(0);
      // Odnośnik obejmuje tekst tylko w obrębie jednego bloku treści —
      // rozciągnięty przez granicę akapitu/punktu listy rozrywałby strukturę.
      if (blokTekstu(zakres.startContainer) !== blokTekstu(zakres.endContainer)) {
        komunikat("Odnośnik może objąć tekst w obrębie jednego akapitu.", true);
        return;
      }
      var wyjete = zakres.extractContents();
      // Odnośnik w odnośniku jest zabroniony.
      [].slice.call(wyjete.querySelectorAll("a")).forEach(rozpuscElement);
      var a = tresc.ownerDocument.createElement("a");
      a.setAttribute("href", url);
      if (nowaKarta) {
        a.setAttribute("target", "_blank");
        a.setAttribute("rel", "noopener");
      }
      a.appendChild(wyjete);
      zakres.insertNode(a);
      zakres.setStartAfter(a);
      zakres.collapse(true);
      sel.removeAllRanges();
      sel.addRange(zakres);
    }

    function otworzDialogLinku() {
      var istniejacy = przodek("A");
      var sel = zaznaczenie();
      if (!istniejacy && (!sel || sel.isCollapsed)) {
        komunikat("Zaznacz najpierw tekst, który ma być odnośnikiem.", true);
        return;
      }
      if (!istniejacy && sel) {
        var zakres = sel.getRangeAt(0);
        if (blokTekstu(zakres.startContainer) !== blokTekstu(zakres.endContainer)) {
          komunikat("Odnośnik może objąć tekst w obrębie jednego akapitu.", true);
          return;
        }
      }
      var zapamietane = zapamietajKursor();
      var n = otworzNakladke();
      n.dialog.innerHTML =
        "<h3>" + (istniejacy ? "Edytuj odnośnik" : "Wstaw odnośnik") + "</h3>" +
        "<label>Adres — wklej dowolny albo wybierz stronę serwisu poniżej</label>" +
        '<input type="text" class="url" placeholder="https://…  albo  /baza-wiedzy/…">' +
        '<label class="w-linii"><input type="checkbox" class="karta"> otwieraj w nowej karcie</label>' +
        '<input type="text" class="szukaj-strony" placeholder="Szukaj strony serwisu…">' +
        '<div class="lista-stron"></div>' +
        '<div class="stopka-dialogu">' +
        (istniejacy ? '<button class="zdejmij grozny">Usuń odnośnik</button>' : "") +
        '<button class="anuluj">Anuluj</button>' +
        '<button class="wstaw glowny">' + (istniejacy ? "Zapisz" : "Wstaw") + "</button>" +
        "</div>";

      var wpisUrl = n.dialog.querySelector(".url");
      var karta = n.dialog.querySelector(".karta");
      var szukajStrony = n.dialog.querySelector(".szukaj-strony");
      var listaStron = n.dialog.querySelector(".lista-stron");

      wpisUrl.value = istniejacy ? (istniejacy.getAttribute("href") || "") : "";
      karta.checked = istniejacy ? istniejacy.getAttribute("target") === "_blank" : false;

      wpisUrl.addEventListener("input", function () {
        karta.checked = /^(https?:)?\/\//i.test(wpisUrl.value.trim());
      });

      function rysujStrony() {
        var fraza = (szukajStrony.value || "").toLowerCase();
        listaStron.innerHTML = "";
        (stan.adresy || []).filter(function (a) {
          return !fraza || (a.etykieta + " " + a.url).toLowerCase().indexOf(fraza) !== -1;
        }).forEach(function (a) {
          var b = document.createElement("button");
          b.type = "button";
          b.textContent = a.etykieta + "  —  " + a.url;
          b.addEventListener("click", function () {
            wpisUrl.value = a.url;
            karta.checked = false;
          });
          listaStron.appendChild(b);
        });
      }
      szukajStrony.addEventListener("input", rysujStrony);
      rysujStrony();

      n.dialog.querySelector(".anuluj").addEventListener("click", n.zamknij);
      if (istniejacy) {
        n.dialog.querySelector(".zdejmij").addEventListener("click", function () {
          n.zamknij();
          przywrocKursor(zapamietane);
          if (tresc.contains(istniejacy)) rozpuscElement(istniejacy);
          utrwalZmiane();
        });
      }
      n.dialog.querySelector(".wstaw").addEventListener("click", function () {
        var url = wpisUrl.value.trim();
        if (!url) { wpisUrl.focus(); return; }
        n.zamknij();
        przywrocKursor(zapamietane);
        if (istniejacy && tresc.contains(istniejacy)) {
          istniejacy.setAttribute("href", url);
          if (karta.checked) {
            istniejacy.setAttribute("target", "_blank");
            istniejacy.setAttribute("rel", "noopener");
          } else {
            istniejacy.removeAttribute("target");
            istniejacy.removeAttribute("rel");
          }
        } else {
          utworzLink(url, karta.checked);
        }
        utrwalZmiane();
      });
      wpisUrl.focus();
    }

    /** Dialog zdjęcia: galeria + wgrywanie z dysku, potem opis i położenie. */
    function otworzDialogGrafiki(wstepna) {
      var zapamietane = zapamietajKursor();
      var n = otworzNakladke();
      var wybrana = wstepna || null;

      function krokSzczegoly() {
        n.dialog.innerHTML =
          "<h3>Zdjęcie w treści</h3>" +
          '<img class="poglad" alt="">' +
          "<label>Opis zdjęcia (wymagany) — napisz, co na nim widać</label>" +
          '<input type="text" class="opis">' +
          '<div class="blad-pola" style="display:none">Bez opisu zdjęcia nie zobaczą osoby niewidome ani Google.</div>' +
          "<label>Podpis pod zdjęciem (opcjonalny)</label>" +
          '<input type="text" class="podpis">' +
          '<div class="dwie">' +
          "<div><label>Wielkość</label><select class='rozmiar'>" +
          "<option value='foto-pelna'>pełna szerokość</option>" +
          "<option value='foto-srednia'>średnie (65%)</option>" +
          "<option value='foto-mala'>małe (40%)</option></select></div>" +
          "<div><label>Położenie</label><select class='polozenie'>" +
          "<option value='tekst-srodek' selected>osobno, wyśrodkowane</option>" +
          "<option value=''>osobno, do lewej</option>" +
          "<option value='tekst-prawo'>osobno, do prawej</option>" +
          "<option value='foto-oblewa-lewo'>obok tekstu, z lewej</option>" +
          "<option value='foto-oblewa-prawo'>obok tekstu, z prawej</option></select></div>" +
          "</div>" +
          '<div class="stopka-dialogu"><button class="wroc">&#8592; Galeria</button>' +
          '<button class="anuluj">Anuluj</button>' +
          '<button class="wstaw glowny">Wstaw zdjęcie</button></div>';

        n.dialog.querySelector(".poglad").src = wybrana.url;
        var opis = n.dialog.querySelector(".opis");
        var podpis = n.dialog.querySelector(".podpis");
        var rozmiar = n.dialog.querySelector(".rozmiar");
        var polozenie = n.dialog.querySelector(".polozenie");

        // Grafika na pelna szerokosc nie da sie oblac tekstem — przy wyborze
        // oblewania podnosimy rozmiar do sredniego.
        polozenie.addEventListener("change", function () {
          if (polozenie.value.indexOf("oblewa") !== -1 && rozmiar.value === "foto-pelna") {
            rozmiar.value = "foto-srednia";
          }
        });

        n.dialog.querySelector(".wroc").addEventListener("click", function () { krokGalerii(); });
        n.dialog.querySelector(".anuluj").addEventListener("click", n.zamknij);
        n.dialog.querySelector(".wstaw").addEventListener("click", function () {
          var alt = opis.value.trim();
          if (!alt) {
            n.dialog.querySelector(".blad-pola").style.display = "";
            opis.focus();
            return;
          }
          var dok = tresc.ownerDocument;
          var figura = dok.createElement("figure");
          var klasy = [rozmiar.value, polozenie.value].filter(Boolean).join(" ");
          if (klasy) figura.setAttribute("class", klasy);
          var obraz = dok.createElement("img");
          obraz.setAttribute("src", wybrana.url);
          obraz.setAttribute("alt", alt);
          obraz.setAttribute("loading", "lazy");
          figura.appendChild(obraz);
          var podpisTekst = podpis.value.trim();
          if (podpisTekst) {
            var figcaption = dok.createElement("figcaption");
            figcaption.textContent = podpisTekst;
            figura.appendChild(figcaption);
          }
          n.zamknij();
          przywrocKursor(zapamietane);
          wstawBlok(figura);
        });
        opis.focus();
      }

      function krokGalerii() {
        n.dialog.innerHTML =
          "<h3>Wybierz zdjęcie</h3>" +
          '<div class="wgraj"><button type="button" class="z-dysku">Wgraj z dysku…</button>' +
          "<span>JPG, PNG, WEBP albo GIF, do 20 MB. Plik możesz też przeciągnąć " +
          "wprost na treść artykułu.</span>" +
          '<input type="file" accept="image/*" style="display:none"></div>' +
          '<input type="text" class="szukaj-grafiki" placeholder="Szukaj po nazwie…">' +
          '<div class="siatka"></div>' +
          '<div class="stopka-dialogu"><button class="anuluj">Anuluj</button></div>';

        var siatka = n.dialog.querySelector(".siatka");
        var szukajGrafiki = n.dialog.querySelector(".szukaj-grafiki");
        var wyborPliku = n.dialog.querySelector("input[type=file]");

        function rysujKafle() {
          var fraza = (szukajGrafiki.value || "").toLowerCase();
          siatka.innerHTML = "";
          (stan.grafiki || []).filter(function (g) {
            return !fraza || (g.nazwa + " " + g.url).toLowerCase().indexOf(fraza) !== -1;
          }).forEach(function (g) {
            var kafel = document.createElement("button");
            kafel.type = "button";
            kafel.className = "kafel";
            kafel.title = g.url + "  (" + g.rozmiar_kb + " kB)";
            kafel.innerHTML = '<img alt="" loading="lazy"><span></span>';
            kafel.querySelector("img").src = g.url;
            kafel.querySelector("span").textContent = g.nazwa;
            kafel.addEventListener("click", function () {
              wybrana = g;
              krokSzczegoly();
            });
            siatka.appendChild(kafel);
          });
        }
        szukajGrafiki.addEventListener("input", rysujKafle);
        rysujKafle();

        n.dialog.querySelector(".z-dysku").addEventListener("click", function () {
          wyborPliku.click();
        });
        wyborPliku.addEventListener("change", function (e) {
          var plik = e.target.files && e.target.files[0];
          if (!plik) return;
          wgrajGrafike(plik, function (g) {
            wybrana = g;
            krokSzczegoly();
          });
        });
        n.dialog.querySelector(".anuluj").addEventListener("click", n.zamknij);
      }

      if (wybrana) krokSzczegoly();
      else krokGalerii();
    }

    function dialogOpisuFigury(figura) {
      var obraz = figura.querySelector("img");
      var podpisEl = figura.querySelector("figcaption");
      var n = otworzNakladke();
      n.dialog.innerHTML =
        "<h3>Opis i podpis zdjęcia</h3>" +
        "<label>Opis (dla osób niewidomych i Google)</label>" +
        '<input type="text" class="opis">' +
        "<label>Podpis pod zdjęciem</label>" +
        '<input type="text" class="podpis">' +
        '<div class="stopka-dialogu"><button class="anuluj">Anuluj</button>' +
        '<button class="wstaw glowny">Zapisz</button></div>';
      n.dialog.querySelector(".opis").value = (obraz && obraz.getAttribute("alt")) || "";
      n.dialog.querySelector(".podpis").value = podpisEl ? podpisEl.textContent : "";
      n.dialog.querySelector(".anuluj").addEventListener("click", n.zamknij);
      n.dialog.querySelector(".wstaw").addEventListener("click", function () {
        var opis = n.dialog.querySelector(".opis").value.trim();
        var podpis = n.dialog.querySelector(".podpis").value.trim();
        if (obraz) obraz.setAttribute("alt", opis);
        if (podpis) {
          if (!podpisEl) {
            podpisEl = figura.ownerDocument.createElement("figcaption");
            figura.appendChild(podpisEl);
          }
          podpisEl.textContent = podpis;
        } else if (podpisEl) {
          figura.removeChild(podpisEl);
          podpisEl = null;
        }
        n.zamknij();
        utrwalZmiane();
      });
      n.dialog.querySelector(".opis").focus();
    }

    // --------------------------------------------------------- menu „/”
    var menuEl = null, menuFiltr = "", menuIndeks = 0;

    var POZYCJE_MENU = [
      { tytul: "Nagłówek", opis: "Tytuł sekcji artykułu",
        akcja: function () { ustawBlok("H2"); } },
      { tytul: "Podtytuł", opis: "Mniejszy nagłówek wewnątrz sekcji",
        akcja: function () { ustawBlok("H3"); } },
      { tytul: "Lista punktowana", opis: "Wyliczenie od punktorów",
        akcja: function () { przelaczListe("UL"); } },
      { tytul: "Lista numerowana", opis: "Kroki po kolei: 1, 2, 3…",
        akcja: function () { przelaczListe("OL"); } },
      { tytul: "Cytat", opis: "Wypowiedź odsunięta od tekstu",
        akcja: function () { przelaczCytat(); } },
      { tytul: "Wyróżnienie", opis: "Akapit z kreską — ważna uwaga",
        akcja: function () { przelaczNote(); } },
      { tytul: "Tabela", opis: "3 × 3 z nagłówkiem; wiersze dodasz później",
        akcja: function () { wstawTabele(3, 3); } },
      { tytul: "Zdjęcie", opis: "Z galerii serwisu albo z dysku",
        akcja: function () { otworzDialogGrafiki(null); } },
      { tytul: "Pozioma linia", opis: "Oddziela części artykułu",
        akcja: function () { wstawLinie(); } }
    ];

    function pozycjeMenu() {
      var fraza = menuFiltr.toLowerCase();
      return POZYCJE_MENU.filter(function (p) {
        return !fraza || p.tytul.toLowerCase().indexOf(fraza) !== -1;
      });
    }

    function zamknijMenu() {
      if (menuEl) { menuEl.remove(); menuEl = null; }
    }

    function rysujMenu() {
      if (!menuEl) return;
      var pozycje = pozycjeMenu();
      if (menuIndeks >= pozycje.length) menuIndeks = 0;
      menuEl.innerHTML = "";
      var naglowek = document.createElement("div");
      naglowek.className = "naglowek-menu";
      naglowek.textContent = "Wstaw" + (menuFiltr ? ": " + menuFiltr : "");
      menuEl.appendChild(naglowek);
      pozycje.forEach(function (p, i) {
        var b = document.createElement("button");
        b.type = "button";
        if (i === menuIndeks) b.className = "akt";
        b.innerHTML = "<strong></strong><small></small>";
        b.querySelector("strong").textContent = p.tytul;
        b.querySelector("small").textContent = p.opis;
        b.addEventListener("mousedown", function (ev) {
          ev.preventDefault();
          zamknijMenu();
          p.akcja();
        });
        menuEl.appendChild(b);
      });
      if (!pozycje.length) {
        var pusta = document.createElement("div");
        pusta.className = "naglowek-menu";
        pusta.textContent = "brak pasujących pozycji";
        menuEl.appendChild(pusta);
      }
    }

    function otworzMenu() {
      zamknijMenu();
      menuFiltr = "";
      menuIndeks = 0;
      menuEl = document.createElement("div");
      menuEl.className = "red-menu";
      menuEl._zamknij = zamknijMenu;
      root.appendChild(menuEl);

      var prostokat = null;
      var sel = zaznaczenie();
      if (sel && sel.rangeCount) prostokat = sel.getRangeAt(0).getBoundingClientRect();
      if (!prostokat || (!prostokat.width && !prostokat.height && !prostokat.top)) {
        var blok = blokKursora();
        if (blok) prostokat = blok.getBoundingClientRect();
      }
      var lewa = prostokat ? prostokat.left : 200;
      var gora = prostokat ? prostokat.bottom + 6 : 200;
      menuEl.style.left = Math.max(12, Math.min(lewa, window.innerWidth - 300)) + "px";
      rysujMenu();
      var wysokosc = menuEl.offsetHeight;
      if (gora + wysokosc > window.innerHeight - 12) {
        gora = Math.max(12, (prostokat ? prostokat.top : gora) - wysokosc - 6);
      }
      menuEl.style.top = gora + "px";
    }

    function menuKlawisz(e) {
      if (!menuEl) return false;
      if (e.key === "Escape") {
        e.preventDefault();
        e.stopPropagation();
        zamknijMenu();
        return true;
      }
      if (e.key === "ArrowDown") { e.preventDefault(); menuIndeks++; rysujMenu(); return true; }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        menuIndeks = Math.max(0, menuIndeks - 1);
        rysujMenu();
        return true;
      }
      if (e.key === "Enter" || e.key === "Tab") {
        e.preventDefault();
        var pozycje = pozycjeMenu();
        var pozycja = pozycje[menuIndeks];
        zamknijMenu();
        if (pozycja) pozycja.akcja();
        return true;
      }
      if (e.key === "Backspace") {
        e.preventDefault();
        if (!menuFiltr) zamknijMenu();
        else { menuFiltr = menuFiltr.slice(0, -1); rysujMenu(); }
        return true;
      }
      if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        menuFiltr += e.key;
        menuIndeks = 0;
        rysujMenu();
        return true;
      }
      return false;
    }

    function sprobujMenu(e) {
      var blok = blokKursora();
      if (!blok || blok.tagName !== "P" || blok.textContent.trim()) return false;
      e.preventDefault();
      otworzMenu();
      return true;
    }

    // --------------------------------------------- skróty w stylu Markdowna
    function skrotMarkdown(e) {
      var blok = blokKursora();
      if (!blok || blok.tagName !== "P" || blok.parentNode !== tresc) return false;
      var sel = zaznaczenie();
      if (!sel || !sel.isCollapsed || !sel.rangeCount) return false;
      var zakres = sel.getRangeAt(0).cloneRange();
      zakres.setStart(blok, 0);
      var przed = zakres.toString();
      var znane = { "##": "h2", "###": "h3", "-": "ul", "*": "ul",
                    "1.": "ol", ">": "cytat" };
      var co = znane[przed];
      if (!co) return false;
      e.preventDefault();
      zakres.deleteContents();
      if (co === "h2") ustawBlok("H2");
      else if (co === "h3") ustawBlok("H3");
      else if (co === "ul") przelaczListe("UL");
      else if (co === "ol") przelaczListe("OL");
      else przelaczCytat();
      return true;
    }

    function enterSpecjalny(e) {
      var blok = blokKursora();
      if (!blok) return false;
      // „---” + Enter → pozioma linia.
      if (blok.tagName === "P" && blok.textContent.trim() === "---") {
        e.preventDefault();
        var hr = tresc.ownerDocument.createElement("hr");
        blok.parentNode.replaceChild(hr, blok);
        var akapit = tresc.ownerDocument.createElement("p");
        akapit.innerHTML = "<br>";
        hr.parentNode.insertBefore(akapit, hr.nextSibling);
        kursorNaPoczatek(akapit);
        utrwalZmiane();
        return true;
      }
      // Enter w pustym akapicie na końcu cytatu → wyjście z cytatu.
      var cytat = blok.parentNode && blok.parentNode.tagName === "BLOCKQUOTE"
                ? blok.parentNode : null;
      if (cytat && blok.tagName === "P" && !blok.textContent.trim() &&
          blok === cytat.lastElementChild) {
        e.preventDefault();
        cytat.parentNode.insertBefore(blok, cytat.nextSibling);
        if (!cytat.textContent.trim() && !cytat.children.length) {
          cytat.parentNode.removeChild(cytat);
        }
        kursorNaPoczatek(blok);
        utrwalZmiane();
        return true;
      }
      return false;
    }

    // ------------------------------------------------------------ wklejanie
    function tekstNaHtml(tekst) {
      var akapity = tekst.replace(/\r\n?/g, "\n").split(/\n{2,}/);
      return akapity.map(function (a) {
        return "<p>" + eskapujHtml(a).replace(/\n/g, "<br>") + "</p>";
      }).join("");
    }

    function wklejHtml(html) {
      tresc.focus();
      document.execCommand("insertHTML", false, html);
      rozbijAkapityZBlokami(tresc);
      utrwalZmiane();
    }

    // Wklejanie: obrazy idą na serwer, HTML z Worda/Dokumentów Google jest
    // czyszczony do naszego słownika z zachowaniem struktury, adres URL
    // na zaznaczeniu robi odnośnik, a czysty tekst dzieli się na akapity.
    tresc.addEventListener("paste", function (e) {
      e.preventDefault();
      var schowek = e.clipboardData || window.clipboardData;
      if (!schowek) return;

      var pliki = schowek.files;
      if (pliki && pliki.length && pliki[0].type.indexOf("image/") === 0) {
        wgrajGrafike(pliki[0], function (g) { otworzDialogGrafiki(g); });
        return;
      }

      var tekst = schowek.getData("text/plain") || "";
      var sel = zaznaczenie();
      if (sel && !sel.isCollapsed &&
          /^(https?:\/\/|mailto:|tel:|\/)\S+$/i.test(tekst.trim())) {
        utworzLink(tekst.trim(), /^https?:/i.test(tekst.trim()));
        utrwalZmiane();
        return;
      }

      var html = schowek.getData("text/html");
      var wstawka = "";
      if (html) {
        var kubel = document.createElement("div");
        kubel.innerHTML = html;
        przygotujWklejone(kubel);
        wstawka = oczysc(kubel);
        // Pojedynczy akapit wklejamy w miejscu kursora, bez nowego bloku.
        kubel.innerHTML = wstawka;
        var blok = blokKursora();
        if (kubel.children.length === 1 && kubel.children[0].tagName === "P" &&
            blok && blok.textContent.trim()) {
          wstawka = kubel.children[0].innerHTML;
        }
      } else if (tekst) {
        wstawka = tekstNaHtml(tekst);
      }
      if (wstawka) wklejHtml(wstawka);
    });

    // -------------------------------------------------- przeciąganie plików
    function przeciaganeSaPliki(e) {
      var dt = e.dataTransfer;
      return !!dt && [].slice.call(dt.types || []).indexOf("Files") !== -1;
    }

    tresc.addEventListener("dragover", function (e) {
      if (przeciaganeSaPliki(e)) {
        e.preventDefault();
        tresc.classList.add("przeciaganie");
      }
    });
    tresc.addEventListener("dragleave", function () {
      tresc.classList.remove("przeciaganie");
    });
    tresc.addEventListener("drop", function (e) {
      tresc.classList.remove("przeciaganie");
      if (!przeciaganeSaPliki(e)) return;
      e.preventDefault();
      var plik = e.dataTransfer.files[0];
      if (plik) wgrajGrafike(plik, function (g) { otworzDialogGrafiki(g); });
    });

    // -------------------------------------------------------- widok kodu
    function formatujHtml(html) {
      return html
        .replace(/<\/(p|h2|h3|ul|ol|li|blockquote|figure|table|thead|tbody|tr)>/g,
                 "</$1>\n")
        .replace(/<(ul|ol|blockquote|table|thead|tbody)>/g, "<$1>\n")
        .replace(/<hr>/g, "<hr>\n")
        .trim();
    }

    var przelacznikKod;

    function przelaczKod() {
      var doKodu = kod.style.display === "none";
      if (doKodu) {
        var klon = tresc.cloneNode(true);
        [].slice.call(klon.querySelectorAll(".red-fig-akt")).forEach(function (f) {
          f.classList.remove("red-fig-akt");
          if (!f.getAttribute("class")) f.removeAttribute("class");
        });
        kod.value = formatujHtml(oczysc(klon));
        kod.style.display = "";
        tresc.style.display = "none";
        przelacznikKod.classList.add("akt");
      } else {
        odznaczFigure();
        tresc.innerHTML = oczyscHtml(kod.value);
        kod.style.display = "none";
        tresc.style.display = "";
        przelacznikKod.classList.remove("akt");
        zadbajOPustke();
        migawka(true);
      }
      zapiszStan();
      odswiezPasek();
    }

    // ------------------------------------------------- pełny ekran edytora
    var przyciskMaks;

    function maksEdytora() { return red.classList.contains("maks"); }

    function przelaczMaksEdytora(wlacz) {
      var cel = wlacz === undefined ? !maksEdytora() : wlacz;
      red.classList.toggle("maks", cel);
      przyciskMaks.classList.toggle("akt", cel);
      tresc.focus();
    }
    red._zamknijMaks = function () {
      if (!maksEdytora()) return false;
      przelaczMaksEdytora(false);
      return true;
    };

    // ------------------------------------------------------------- stopka
    function odswiezStopke() {
      var tekst = tresc.textContent || "";
      var slowa = (tekst.match(/\S+/g) || []).length;
      var znaki = tekst.replace(/\s+/g, " ").trim().length;
      var minuty = Math.max(1, Math.round(slowa / 200));
      stopka.innerHTML = "";
      var info = document.createElement("span");
      info.textContent = slowa
        ? slowa + " słów · " + znaki + " znaków · czytanie ≈ " + minuty + " min"
        : "pusty artykuł";
      stopka.appendChild(info);
      var rosnie = document.createElement("span");
      rosnie.className = "rosnie";
      stopka.appendChild(rosnie);
      if (slowa && szkic().read_time !== minuty + " min") {
        var b = document.createElement("button");
        b.type = "button";
        b.textContent = "ustaw czas czytania: " + minuty + " min";
        b.title = "Wpisuje wyliczony czas w pole „Czas czytania”";
        b.addEventListener("click", function () {
          var wejscie = root.querySelector('[data-kolumna="read_time"] input');
          if (wejscie) wejscie.value = minuty + " min";
          stan.zmiany.read_time = minuty + " min";
          odswiezStopke();
          zaplanujPodglad();
        });
        stopka.appendChild(b);
      }
    }

    // ------------------------------------------------- pasek kontekstowy
    function odswiezKontekst() {
      kontekst.innerHTML = "";
      if (wybranaFigura && tresc.contains(wybranaFigura)) {
        rysujKontekstFigury();
        kontekst.classList.add("widoczny");
      } else if (komorkaKursora()) {
        rysujKontekstTabeli();
        kontekst.classList.add("widoczny");
      } else {
        kontekst.classList.remove("widoczny");
      }
    }

    function rysujKontekstFigury() {
      var figura = wybranaFigura;
      var opis = document.createElement("strong");
      opis.textContent = "Zdjęcie:";
      kontekst.appendChild(opis);

      var rozmiar = document.createElement("select");
      [["foto-pelna", "pełna szerokość"], ["foto-srednia", "średnie (65%)"],
       ["foto-mala", "małe (40%)"]].forEach(function (para) {
        var opt = document.createElement("option");
        opt.value = para[0];
        opt.textContent = para[1];
        if (figura.classList.contains(para[0])) opt.selected = true;
        rozmiar.appendChild(opt);
      });
      rozmiar.addEventListener("change", function () {
        KLASY_ROZMIARU.forEach(function (k) { figura.classList.remove(k); });
        figura.classList.add(rozmiar.value);
        utrwalZmiane();
      });
      kontekst.appendChild(rozmiar);

      var polozenie = document.createElement("select");
      [["tekst-srodek", "osobno, wyśrodkowane"], ["", "osobno, do lewej"],
       ["tekst-prawo", "osobno, do prawej"], ["foto-oblewa-lewo", "obok tekstu, z lewej"],
       ["foto-oblewa-prawo", "obok tekstu, z prawej"]].forEach(function (para) {
        var opt = document.createElement("option");
        opt.value = para[0];
        opt.textContent = para[1];
        if (para[0] && figura.classList.contains(para[0])) opt.selected = true;
        polozenie.appendChild(opt);
      });
      polozenie.addEventListener("change", function () {
        KLASY_WYROWNANIA.concat(KLASY_OBLEWANIA).forEach(function (k) {
          figura.classList.remove(k);
        });
        if (polozenie.value) figura.classList.add(polozenie.value);
        if (polozenie.value.indexOf("oblewa") !== -1 &&
            figura.classList.contains("foto-pelna")) {
          figura.classList.remove("foto-pelna");
          figura.classList.add("foto-srednia");
        }
        utrwalZmiane();
      });
      kontekst.appendChild(polozenie);

      przycisk(kontekst, "Opis i podpis…", "Zmień opis (alt) i podpis zdjęcia",
        function () { dialogOpisuFigury(figura); });
      przycisk(kontekst, "Usuń zdjęcie", "Usuń zdjęcie z treści",
        function () { usunFigure(); });
    }

    function rysujKontekstTabeli() {
      var opis = document.createElement("strong");
      opis.textContent = "Tabela:";
      kontekst.appendChild(opis);
      przycisk(kontekst, "+ wiersz", "Dodaj wiersz pod bieżącym",
        function () { tabelaOp("wiersz+"); });
      przycisk(kontekst, "− wiersz", "Usuń bieżący wiersz",
        function () { tabelaOp("wiersz-"); });
      przycisk(kontekst, "+ kolumna", "Dodaj kolumnę na prawo od bieżącej",
        function () { tabelaOp("kolumna+"); });
      przycisk(kontekst, "− kolumna", "Usuń bieżącą kolumnę",
        function () { tabelaOp("kolumna-"); });
      przycisk(kontekst, "nagłówek", "Włącz/wyłącz wiersz nagłówka",
        function () { tabelaOp("naglowek"); });
      przycisk(kontekst, "usuń tabelę", "Usuń całą tabelę",
        function () { tabelaOp("usun"); });
    }

    // ------------------------------------------------- stany przycisków
    var przyciskiStanu = {};

    function odswiezPasek() {
      function stanKomendy(cmd) {
        try { return document.queryCommandState(cmd); } catch (e) { return false; }
      }
      var blok = blokKursora();
      function wBloku(tag) {
        var w = blok;
        while (w && w !== tresc) {
          if (w.tagName === tag) return true;
          w = w.parentNode;
        }
        return false;
      }
      var ps = przyciskiStanu;
      if (ps.b) ps.b.classList.toggle("akt", stanKomendy("bold"));
      if (ps.i) ps.i.classList.toggle("akt", stanKomendy("italic"));
      if (ps.s) ps.s.classList.toggle("akt", stanKomendy("strikeThrough"));
      if (ps.sub) ps.sub.classList.toggle("akt", stanKomendy("subscript"));
      if (ps.sup) ps.sup.classList.toggle("akt", stanKomendy("superscript"));
      if (ps.p) ps.p.classList.toggle("akt",
        !!blok && blok.tagName === "P" && !blok.classList.contains("note"));
      if (ps.h2) ps.h2.classList.toggle("akt", wBloku("H2"));
      if (ps.h3) ps.h3.classList.toggle("akt", wBloku("H3"));
      if (ps.ul) ps.ul.classList.toggle("akt", !!przodek("UL"));
      if (ps.ol) ps.ol.classList.toggle("akt", !!przodek("OL"));
      if (ps.cytat) ps.cytat.classList.toggle("akt", !!przodek("BLOCKQUOTE"));
      if (ps.note) ps.note.classList.toggle("akt",
        !!blok && blok.tagName === "P" && blok.classList.contains("note"));
      if (ps.link) ps.link.classList.toggle("akt", !!przodek("A"));
      // W widoku kodu historia dotyczy trybu wizualnego — blokujemy strzałki,
      // żeby cofnięcie nie rozjechało się z ręcznie edytowanym HTML-em.
      var wKodzie = kod.style.display !== "none";
      if (ps.cofnij) ps.cofnij.disabled = wKodzie || histPozycja <= 0;
      if (ps.ponow) ps.ponow.disabled = wKodzie || histPozycja >= historia.length - 1;
      // Kursor uciekł poza zaznaczone zdjęcie → odznaczamy.
      if (wybranaFigura) {
        var sel = zaznaczenie();
        if (sel && sel.anchorNode && !wybranaFigura.contains(sel.anchorNode)) {
          odznaczFigure();
        }
      }
      odswiezKontekst();
    }

    // ------------------------------------------------------ budowa paska
    var gBlok = grupa();
    przyciskiStanu.p = przycisk(gBlok, "Akapit", "Zwykły akapit tekstu (Ctrl+Alt+0)",
      function () { ustawBlok("P"); });
    przyciskiStanu.h2 = przycisk(gBlok, "Nagłówek",
      "Nagłówek sekcji (Ctrl+Alt+2 albo „## ” na początku wiersza)",
      function () { ustawBlok("H2"); });
    przyciskiStanu.h3 = przycisk(gBlok, "Podtytuł",
      "Śródtytuł wewnątrz sekcji (Ctrl+Alt+3 albo „### ”)",
      function () { ustawBlok("H3"); });

    var gLinia = grupa();
    przyciskiStanu.b = przycisk(gLinia, "B", "Pogrubienie (Ctrl+B)",
      function () { polecenie("bold"); }, "ikona b-b");
    przyciskiStanu.i = przycisk(gLinia, "I", "Kursywa (Ctrl+I)",
      function () { polecenie("italic"); }, "ikona b-i");
    przyciskiStanu.s = przycisk(gLinia, "S", "Przekreślenie",
      function () { polecenie("strikeThrough"); }, "ikona b-s");
    przyciskiStanu.sub = przycisk(gLinia, "x<sub>2</sub>",
      "Indeks dolny — wzory chemiczne: H2O, CaCO3",
      function () { polecenie("subscript"); }, "ikona");
    przyciskiStanu.sup = przycisk(gLinia, "x<sup>2</sup>",
      "Indeks górny — jednostki: m3, potęgi",
      function () { polecenie("superscript"); }, "ikona");
    przyciskiStanu.link = przycisk(gLinia, "Link",
      "Odnośnik — dowolny adres albo strona serwisu (Ctrl+K)",
      function () { otworzDialogLinku(); });
    przycisk(gLinia, "Czyść", "Usuń formatowanie znaków z zaznaczenia",
      function () { polecenie("removeFormat"); });

    var gListy = grupa();
    przyciskiStanu.ul = przycisk(gListy, "• Lista", "Lista wypunktowana (albo „- ”)",
      function () { przelaczListe("UL"); });
    przyciskiStanu.ol = przycisk(gListy, "1. Lista", "Lista numerowana (albo „1. ”)",
      function () { przelaczListe("OL"); });
    przyciskiStanu.cytat = przycisk(gListy, "Cytat", "Cytat blokowy (albo „> ”)",
      function () { przelaczCytat(); });
    przyciskiStanu.note = przycisk(gListy, "Wyróżnienie",
      "Akapit odznaczony kreską przy krawędzi", function () { przelaczNote(); });

    var gWstaw = grupa();
    przycisk(gWstaw, "Zdjęcie",
      "Wstaw zdjęcie — z galerii albo z dysku; plik można też przeciągnąć na treść",
      function () { otworzDialogGrafiki(null); });
    przycisk(gWstaw, "Tabela", "Wstaw tabelę 3 × 3 (wiersze i kolumny zmienisz później)",
      function () { wstawTabele(3, 3); });
    przycisk(gWstaw, "Linia", "Pozioma linia oddzielająca (albo „---” i Enter)",
      function () { wstawLinie(); });

    var gWyrownanie = grupa();
    przycisk(gWyrownanie, "≡ Lewo", "Wyrównaj do lewej (domyślnie)",
      function () { wyrownaj(null); });
    przycisk(gWyrownanie, "≡ Środek", "Wyśrodkuj",
      function () { wyrownaj("tekst-srodek"); });
    przycisk(gWyrownanie, "≡ Prawo", "Wyrównaj do prawej",
      function () { wyrownaj("tekst-prawo"); });

    var rosniePasek = document.createElement("span");
    rosniePasek.className = "rosnie";
    pasek.appendChild(rosniePasek);

    var gKoniec = grupa();
    przyciskiStanu.cofnij = przycisk(gKoniec, "↶", "Cofnij (Ctrl+Z)",
      function () { cofnij(); }, "ikona");
    przyciskiStanu.ponow = przycisk(gKoniec, "↷", "Ponów (Ctrl+Y)",
      function () { ponow(); }, "ikona");
    przelacznikKod = przycisk(pasek, "Kod", "Podejrzyj i popraw kod HTML treści",
      function () { przelaczKod(); });
    przyciskMaks = przycisk(pasek, "⛶", "Pisanie na pełnym ekranie (Escape wraca)",
      function () { przelaczMaksEdytora(); }, "ikona");

    // ------------------------------------------------------------ zdarzenia
    tresc.addEventListener("input", function () {
      zadbajOPustke();
      zapiszStan();
      migawka();
    });
    kod.addEventListener("input", zapiszStan);

    tresc.addEventListener("click", function (e) {
      if (menuEl) zamknijMenu();
      var cel = e.target;
      var figura = cel && cel.closest ? cel.closest("figure") : null;
      if (figura && tresc.contains(figura)) {
        zaznaczFigure(figura);
      } else if (wybranaFigura) {
        odznaczFigure();
        odswiezKontekst();
      }
    });

    tresc.addEventListener("keydown", function (e) {
      if (menuEl && menuKlawisz(e)) return;
      var ctrl = e.ctrlKey || e.metaKey;

      // !e.altKey chroni polskie znaki: AltGr to Ctrl+Alt, więc „ż" (AltGr+Z)
      // ma e.ctrlKey i e.code==="KeyZ" — bez tej straży Ctrl+Z zjadałby literę
      // i cofał pisanie zamiast ją wstawić.
      if (ctrl && !e.altKey && !e.shiftKey && toKlawisz(e, "z")) { e.preventDefault(); cofnij(); return; }
      if (ctrl && !e.altKey && !e.shiftKey && toKlawisz(e, "y")) { e.preventDefault(); ponow(); return; }
      if (ctrl && !e.altKey && e.shiftKey && toKlawisz(e, "z")) { e.preventDefault(); ponow(); return; }
      if (ctrl && !e.altKey && toKlawisz(e, "k")) { e.preventDefault(); otworzDialogLinku(); return; }
      if (ctrl && e.altKey) {
        if (e.code === "Digit0") { e.preventDefault(); ustawBlok("P"); return; }
        if (e.code === "Digit2") { e.preventDefault(); ustawBlok("H2"); return; }
        if (e.code === "Digit3") { e.preventDefault(); ustawBlok("H3"); return; }
      }
      if ((e.key === "Backspace" || e.key === "Delete") && wybranaFigura) {
        e.preventDefault();
        usunFigure();
        return;
      }
      if (e.key === "Tab") { if (tabWTabeli(e)) return; }
      if (e.key === "/" && !ctrl && !e.altKey) { if (sprobujMenu(e)) return; }
      if (e.key === " ") { if (skrotMarkdown(e)) return; }
      if (e.key === "Enter" && !e.shiftKey) { if (enterSpecjalny(e)) return; }
      if (e.key === "Escape" && wybranaFigura) {
        e.stopPropagation();
        odznaczFigure();
        odswiezKontekst();
      }
    });

    // Podświetlenie paska podąża za kursorem. Nasłuch na dokumencie —
    // po przerysowaniu formularza stare edytory odfiltrowują się przez
    // isConnected i nie robią nic.
    var planPaska = null;
    document.addEventListener("selectionchange", function () {
      if (!tresc.isConnected || planPaska) return;
      planPaska = requestAnimationFrame(function () {
        planPaska = null;
        if (tresc.isConnected && zaznaczenie()) odswiezPasek();
      });
    });

    // ------------------------------------------------------------- start
    zadbajOPustke();
    odswiezStopke();
    migawka(true);   // stan wyjściowy historii — bez wpisu w stan.zmiany
    odswiezPasek();

    return pole;
  }

  /** Escape zamyka warstwy edytora od najwyższej: menu, dialog, pełny ekran.
   *  Zwraca true, gdy było co zamknąć — wtedy panel zostaje otwarty. */
  function zamknijWarstweRedaktora() {
    if (!root) return false;
    var menu = root.querySelector(".red-menu");
    if (menu) { if (menu._zamknij) menu._zamknij(); else menu.remove(); return true; }
    var nakladka = root.querySelector(".red-nakladka");
    if (nakladka) { if (nakladka._zamknij) nakladka._zamknij(); else nakladka.remove(); return true; }
    var maks = root.querySelector(".red.maks");
    if (maks && maks._zamknijMaks) return maks._zamknijMaks();
    return false;
  }

  function poleTekstowe(def, wartosc) {
    if (def.typ === "lista") return poleListy(def, wartosc);
    if (def.typ === "redaktor") return poleRedaktor(def, wartosc);

    var pole = document.createElement("div");
    pole.dataset.kolumna = def.k;
    var kontrolka = def.typ === "text"
      ? '<input type="text" value="">'
      : '<textarea class="' + (def.typ === "kod" ? "kod" : "") + '"></textarea>';
    pole.innerHTML = "<label></label>" + kontrolka +
      (def.pomoc ? '<div class="pomoc"></div>' : "");
    pole.querySelector("label").textContent = def.label;
    if (def.pomoc) pole.querySelector(".pomoc").textContent = def.pomoc;
    var wej = pole.querySelector("input,textarea");
    wej.value = wartosc == null ? "" : wartosc;
    wej.addEventListener("input", function () {
      stan.zmiany[def.k] = wej.value;
      if (def.k === "slug") odswiezAdres();
      zaplanujPodglad();
    });
    return pole;
  }

  function sekcjaListy(def, wartosc) {
    var sekcja = document.createElement("div");
    sekcja.className = "sekcja";
    sekcja.innerHTML = "<h3></h3><div class='wiersze'></div><button class='dodaj'>+ Dodaj wiersz</button>";
    sekcja.querySelector("h3").textContent = def.label;
    var wiersze = sekcja.querySelector(".wiersze");

    function zbierz() {
      var dane = [];
      wiersze.querySelectorAll(".wiersz").forEach(function (w) {
        var obiekt = {}, pusty = true;
        def.kolumny.forEach(function (kol) {
          var v = w.querySelector('[data-pole="' + kol[0] + '"]').value.trim();
          obiekt[kol[0]] = v;
          if (v) pusty = false;
        });
        if (!pusty) dane.push(obiekt);
      });
      stan.zmiany[def.k] = dane;
      zaplanujPodglad();
    }

    /** Lista rozwijana z opcjami; dopuszcza wartosc spoza listy. */
    function listaWyboru(nazwaPola, opcje, biezaca, pustyNapis) {
      var sel = document.createElement("select");
      sel.dataset.pole = nazwaPola;
      sel.innerHTML = '<option value="">' + pustyNapis + "</option>";

      var znane = opcje.some(function (o) { return o.wartosc === biezaca; });
      if (biezaca && !znane) {
        // Zapisana wartosc moze juz nie istniec w serwisie. Pokazujemy ja
        // oznaczona, zamiast po cichu wyczyscic powiazanie.
        var obca = document.createElement("option");
        obca.value = biezaca;
        obca.textContent = biezaca + "  \u2190 nie istnieje";
        obca.selected = true;
        sel.appendChild(obca);
      }
      opcje.forEach(function (o) {
        var opt = document.createElement("option");
        opt.value = o.wartosc;
        opt.textContent = o.etykieta;
        if (o.wartosc === biezaca) opt.selected = true;
        sel.appendChild(opt);
      });
      return sel;
    }

    function dodajWiersz(dane) {
      var w = document.createElement("div");
      w.className = "wiersz";
      w.style.gridTemplateColumns =
        def.kolumny.map(function () { return "1fr"; }).join(" ") + " auto";

      def.kolumny.forEach(function (kol) {
        var biezaca = (dane && dane[kol[0]]) || "";
        var rodzaj = kol[2];
        var kontrolka;

        if (rodzaj === "adresy") {
          kontrolka = listaWyboru(kol[0], stan.adresy.map(function (a) {
            return { wartosc: a.url, etykieta: a.etykieta + "  \u2014  " + a.url };
          }), biezaca, "(wybierz stron\u0119)");

        } else if (rodzaj === "tytuly-stron") {
          kontrolka = listaWyboru(kol[0], stan.adresy.map(function (a) {
            return { wartosc: a.etykieta, etykieta: a.etykieta };
          }), biezaca, "(wybierz tytu\u0142)");

        } else if (rodzaj === "etykiety") {
          kontrolka = listaWyboru(kol[0], stan.etykiety.map(function (e) {
            return { wartosc: e, etykieta: e };
          }), biezaca, "(wybierz etykiet\u0119)");

        } else {
          kontrolka = document.createElement("textarea");
          kontrolka.dataset.pole = kol[0];
          kontrolka.placeholder = kol[1];
          kontrolka.value = biezaca;
        }

        kontrolka.addEventListener(
          kontrolka.tagName === "SELECT" ? "change" : "input",
          function () {
            // Adres i tytul opisuja te sama strone, wiec trzymamy je zgodne:
            // wybor po jednej stronie ustawia druga.
            if (rodzaj === "adresy") {
              var pasujaca = stan.adresy.filter(function (a) {
                return a.url === kontrolka.value;
              })[0];
              var poleTytulu = w.querySelector('[data-pole="title"]');
              if (poleTytulu && pasujaca) poleTytulu.value = pasujaca.etykieta;
            } else if (rodzaj === "tytuly-stron") {
              var poUrl = stan.adresy.filter(function (a) {
                return a.etykieta === kontrolka.value;
              })[0];
              var poleUrl = w.querySelector('[data-pole="url"]');
              if (poleUrl && poUrl) poleUrl.value = poUrl.url;
            }
            zbierz();
          }
        );
        w.appendChild(kontrolka);
      });

      var kasuj = document.createElement("button");
      kasuj.textContent = "\u00d7";
      kasuj.title = "Usu\u0144 wiersz";
      kasuj.addEventListener("click", function () { w.remove(); zbierz(); });
      w.appendChild(kasuj);
      wiersze.appendChild(w);
    }

    (wartosc || []).forEach(function (d) { dodajWiersz(d); });
    sekcja.querySelector(".dodaj").addEventListener("click", function () {
      dodajWiersz(null);
      zbierz();
    });
    return sekcja;
  }

  // ------------------------------------------------- kopia robocza (autosave)
  // Panel zapisuje niezapisane zmiany do localStorage — awaria przeglądarki,
  // przypadkowe zamknięcie karty czy kliknięcie innego artykułu nie tracą
  // pracy redaktora.
  var szkicTimer = null;

  function brudny() { return Object.keys(stan.zmiany).length > 0; }

  function kluczSzkicu() { return "kabiPanelSzkic:" + (stan.biezacy || "(nowy)"); }

  function zapiszSzkicLokalnie() {
    try {
      // Czysty stan NIE kasuje kopii: klucz zależy od stan.biezacy, a ta
      // zmienia się podczas nawigacji — kasowanie tutaj wycięłoby dopiero co
      // zapisaną kopię pod innym slugiem. Kopię usuwają wyłącznie świadome
      // ścieżki (zapis, usunięcie, „Odrzuć").
      if (!brudny()) return;
      localStorage.setItem(kluczSzkicu(), JSON.stringify({
        czas: Date.now(), zmiany: stan.zmiany
      }));
    } catch (e) { /* pełny magazyn nie może blokować pisania */ }
  }

  function zaplanujSzkicLokalny() {
    clearTimeout(szkicTimer);
    szkicTimer = setTimeout(zapiszSzkicLokalnie, 1200);
  }

  function usunSzkicLokalny() {
    try { localStorage.removeItem(kluczSzkicu()); } catch (e) {}
  }

  function zaproponujSzkic() {
    var zapis = null;
    try { zapis = JSON.parse(localStorage.getItem(kluczSzkicu())); } catch (e) {}
    if (!zapis || !zapis.zmiany || !Object.keys(zapis.zmiany).length) return;
    var forma = el(".form");
    var pasek = document.createElement("div");
    pasek.className = "szkic-banner";
    pasek.innerHTML = "<span></span>" +
      '<button class="przywroc glowny">Przywróć</button>' +
      '<button class="odrzuc">Odrzuć</button>';
    pasek.querySelector("span").textContent =
      "Jest niezapisana kopia robocza z " +
      new Date(zapis.czas).toLocaleString("pl-PL") + ".";
    pasek.querySelector(".przywroc").addEventListener("click", function () {
      stan.zmiany = zapis.zmiany;
      rysujFormularz(szkic());
      odswiezAdres();
      zaplanujPodglad();
      komunikat("Przywrócono kopię roboczą. Zapisz, żeby ją utrwalić.", false);
    });
    pasek.querySelector(".odrzuc").addEventListener("click", function () {
      usunSzkicLokalny();
      pasek.remove();
    });
    forma.insertBefore(pasek, forma.firstChild);
  }

  // ------------------------------------------------------------- podgląd
  var podgladTimer = null, podgladOstatni = "", podgladNumer = 0;
  var wczytajNumer = 0;   // licznik wczytań artykułu — chroni przed wyścigiem

  function szkic() {
    // Formularz trzyma tylko ZMIANY, więc przy edycji istniejącego wpisu
    // trzeba je nałożyć na wczytany artykuł — inaczej podgląd gubiłby pola,
    // których użytkownik nie dotknął.
    var out = {};
    if (stan.artykul) {
      Object.keys(stan.artykul).forEach(function (k) { out[k] = stan.artykul[k]; });
    }
    Object.keys(stan.zmiany).forEach(function (k) { out[k] = stan.zmiany[k]; });
    return out;
  }

  function podgladWlaczony() {
    return el(".okno").classList.contains("z-podgladem");
  }

  function przelaczPodglad() {
    var okno = el(".okno");
    okno.classList.toggle("z-podgladem");
    el(".podglad-wl").classList.toggle("glowny", podgladWlaczony());
    if (podgladWlaczony()) odswiezPodglad();
  }

  function maksymalny() {
    return el(".okno").classList.contains("podglad-max");
  }

  function przelaczMax(wlacz) {
    var okno = el(".okno");
    var doWlaczenia = wlacz === undefined ? !maksymalny() : wlacz;

    okno.classList.toggle("podglad-max", doWlaczenia);
    el(".tlo").classList.toggle("bez-marginesu", doWlaczenia);
    el(".podglad__max").textContent = doWlaczenia ? "⤡ Zmniejsz" : "⤢ Pełny ekran";

    // Maksymalizacja bez włączonego podglądu nie miałaby czego pokazać.
    if (doWlaczenia && !podgladWlaczony()) przelaczPodglad();

    // Tryb pełnoekranowy przeglądarki bierzemy na documentElement, a nie na
    // hoście panelu — nakładka i tak jest position:fixed, więc pokryje ekran,
    // a nie musimy walczyć ze stylowaniem :host(:fullscreen).
    try {
      if (doWlaczenia && !document.fullscreenElement) {
        var p = document.documentElement.requestFullscreen();
        // Odmowa (brak gestu, polityka przeglądarki) nie jest błędem —
        // układ i tak jest już zmaksymalizowany w oknie.
        if (p && p.catch) p.catch(function () {});
      } else if (!doWlaczenia && document.fullscreenElement) {
        document.exitFullscreen();
      }
    } catch (e) { /* przeglądarka bez Fullscreen API */ }
  }

  function stanPodgladu(tekst, pracuje) {
    var pole = el(".podglad__stan");
    pole.textContent = tekst;
    pole.className = "podglad__stan" + (pracuje ? " pracuje" : "");
  }

  function zaplanujPodglad() {
    zaplanujSzkicLokalny();   // kopia robocza powstaje niezależnie od podglądu
    if (!podgladWlaczony()) return;
    clearTimeout(podgladTimer);
    stanPodgladu("składam…", true);
    podgladTimer = setTimeout(odswiezPodglad, 350);
  }

  function odswiezPodglad() {
    var dane = szkic();
    var odcisk = JSON.stringify(dane);
    if (odcisk === podgladOstatni) {
      // Stan już wyświetlony — unieważniamy ewentualny render w locie, żeby
      // jego spóźniona odpowiedź nie wróciła jako „starszy" widok.
      podgladNumer++;
      stanPodgladu("aktualny", false);
      return;
    }
    // Numer chroni przed wyścigiem: spóźniona odpowiedź starszego renderu
    // nie może nadpisać nowszego. Odcisk zapisujemy dopiero po sukcesie,
    // żeby po błędzie dało się ponowić identyczny render.
    var numer = ++podgladNumer;

    api("preview", { metoda: "POST", dane: dane }).then(function (w) {
      if (numer !== podgladNumer) return;
      podgladOstatni = odcisk;
      var ramka = el(".podglad iframe");
      // Zachowujemy pozycję przewijania — bez tego każde naciśnięcie klawisza
      // odrzucałoby podgląd na początek strony.
      var y = 0;
      try { y = ramka.contentWindow.scrollY || 0; } catch (e) { /* inny origin */ }
      ramka.onload = function () {
        try { ramka.contentWindow.scrollTo(0, y); } catch (e) { /* j.w. */ }
      };
      ramka.srcdoc = w.html;
      stanPodgladu("aktualny", false);
    }).catch(function (e) {
      if (numer === podgladNumer) stanPodgladu("błąd: " + e.message, false);
    });
  }

  function odswiezAdres() {
    // Czytamy ze szkicu, a nie z samych zmian — inaczej po wczytaniu
    // istniejącego artykułu pasek twierdziłby, że to nowy wpis, dopóki
    // użytkownik nie dotknie pola slug.
    var slug = (szkic().slug || "").trim();
    var poprawny = /^[a-z0-9]+(-[a-z0-9]+)*$/.test(slug);
    el(".adres").textContent = slug
      ? "/baza-wiedzy/" + slug + "/" + (poprawny ? "" : "  ← niepoprawny slug")
      : "(nowy artykuł — wpisz slug)";
    el(".adres").style.color = slug && !poprawny ? "#ff9b86" : "#9fe0b0";
  }

  function rysujFormularz(artykul) {
    var form = el(".form");
    form.innerHTML = '<div class="komunikat" style="display:none"></div>';

    var kategoria = document.createElement("div");
    kategoria.innerHTML = "<label>Kategoria</label><select></select>" +
      '<div class="pomoc">Ustala też napis nad tytułem artykułu. Kategoria bez artykułów przekierowuje na hub — pierwszy artykuł tworzy jej stronę.</div>';
    var select = kategoria.querySelector("select");
    select.innerHTML = '<option value="">(bez kategorii)</option>';
    stan.kategorie.forEach(function (k) {
      var opt = document.createElement("option");
      opt.value = k.id;
      opt.textContent = k.title + " (" + k.artykulow + ")";
      if (artykul && artykul.category_id === k.id) opt.selected = true;
      select.appendChild(opt);
    });
    select.addEventListener("change", function () {
      stan.zmiany.category_id = select.value ? parseInt(select.value, 10) : null;
      // „Dział" (napis nad tytułem) to ta sama informacja co kategoria.
      // Zamiast dwóch pól, które potrafią się rozjechać, bierzemy go
      // z wybranej kategorii.
      var wybrana = stan.kategorie.filter(function (k) {
        return k.id === stan.zmiany.category_id;
      })[0];
      if (wybrana && wybrana.dzial) stan.zmiany.topic = wybrana.dzial;
      zaplanujPodglad();
    });

    POLA.forEach(function (def) {
      form.appendChild(poleTekstowe(def, artykul ? artykul[def.k] : ""));
      if (def.k === "slug") form.appendChild(kategoria);
    });

    LISTY.forEach(function (def) {
      form.appendChild(sekcjaListy(def, artykul ? artykul[def.k] : []));
    });

    var dodatki = document.createElement("div");
    dodatki.className = "sekcja dwie";
    dodatki.innerHTML =
      "<div><label>Widoczny na stronie</label><select class='pub'>" +
      "<option value='true'>tak</option><option value='false'>nie — ukryty</option></select></div>" +
      "<div><label>Kolejność</label><input type='number' class='kol' value='0'></div>";
    // artykul bywa szkicem (kopia robocza), któremu brak published/sort_order —
    // wtedy wartości domyślne, a nie „undefined" w kontrolce.
    dodatki.querySelector(".pub").value =
      artykul && artykul.published !== undefined ? String(artykul.published) : "true";
    dodatki.querySelector(".kol").value =
      artykul && artykul.sort_order !== undefined ? artykul.sort_order : 0;
    dodatki.querySelector(".pub").addEventListener("change", function (e) {
      stan.zmiany.published = e.target.value === "true";
    });
    dodatki.querySelector(".kol").addEventListener("input", function (e) {
      stan.zmiany.sort_order = parseInt(e.target.value, 10) || 0;
    });
    // published i sort_order nie zmieniają wyglądu strony artykułu,
    // więc celowo nie odświeżają podglądu.
    form.appendChild(dodatki);

    // Usuń pokazujemy dla ZAPISANEGO wpisu (stan.biezacy), nie dla samego
    // faktu, że jest jakiś artykuł — przy przywróconej kopii nowego wpisu
    // artykul jest wypełniony, ale w bazie jeszcze nic nie ma.
    el(".usun").style.display = stan.biezacy ? "" : "none";
    odswiezAdres();
  }

  // ------------------------------------------------------------- operacje
  function wczytaj(slug) {
    // Kopia robocza i tak siedzi w localStorage, ale świadome porzucenie
    // zmian powinno być decyzją, nie przypadkiem.
    if (brudny() && slug !== stan.biezacy &&
        !confirm("Masz niezapisane zmiany w tym wpisie. Przejść dalej mimo to?\n" +
                 "(Kopia robocza zostanie zachowana i będzie można ją przywrócić.)")) {
      return;
    }
    clearTimeout(szkicTimer);
    zapiszSzkicLokalnie();   // utrwal kopię roboczą pod DOTYCHCZASOWYM slugiem
    stan.zmiany = {};
    stan.artykul = null;
    stan.biezacy = slug;
    podgladOstatni = "";
    // Numer chroni przed wyścigiem: szybkie przełączanie artykułów potrafi
    // sprawić, że spóźniona odpowiedź starszego GET-a nadpisze nowszy wpis.
    var numer = ++wczytajNumer;
    if (!slug) {
      rysujFormularz(null);
      rysujListe();
      zaproponujSzkic();
      zaplanujPodglad();
      return;
    }
    api("articles/" + slug).then(function (a) {
      if (numer !== wczytajNumer) return;   // wczytano już inny artykuł
      stan.artykul = a;
      stan.zmiany = {};
      rysujFormularz(a);
      rysujListe();
      zaproponujSzkic();
      odswiezPodglad();
    }).catch(function (e) {
      if (numer === wczytajNumer) komunikat(e.message, true);
    });
  }

  /** Przebudowa strony po każdej zmianie w bazie.
   *
   *  Build czyta z content/snapshot.json, a nie prosto z Postgresa. Bez tego
   *  kroku wpis siedzi w bazie, ale strony nie ma — i nie widać, że coś jest
   *  nie tak. Dlatego przebudowa nie jest osobnym przyciskiem do zapamiętania,
   *  tylko doklejonym końcem każdego zapisu i usunięcia.
   */
  function przebuduj(komunikatPoczatkowy) {
    komunikat(komunikatPoczatkowy, false);
    return api("publish", { metoda: "POST", dane: {} }).then(function (b) {
      komunikat(b.ok
        ? "Gotowe. Strona przebudowana — odśwież kartę, żeby zobaczyć zmiany."
        : "Zapisano w bazie, ale przebudowa się nie powiodła:\n" + b.wyjscie, !b.ok);
      return b.ok;
    });
  }

  function zapisz() {
    var dane = {};
    Object.keys(stan.zmiany).forEach(function (k) { dane[k] = stan.zmiany[k]; });
    if (!dane.slug && stan.biezacy) dane.slug = stan.biezacy;

    var zadanie = stan.biezacy
      ? api("articles/" + stan.biezacy, { metoda: "PUT", dane: dane })
      : api("articles", { metoda: "POST", dane: dane });

    el(".zapisz").disabled = el(".usun").disabled = true;
    komunikat("Zapisuję…", false);

    zadanie.then(function (wynik) {
      // Zapis w bazie się powiódł: kopia robocza przestaje być potrzebna
      // (pod starym i — po zmianie sluga — pod nowym kluczem), a zapisany
      // stan staje się punktem odniesienia dla kolejnych zmian.
      usunSzkicLokalny();
      stan.artykul = szkic();
      stan.biezacy = wynik.slug;
      stan.artykul.slug = wynik.slug;
      stan.zmiany = {};
      usunSzkicLokalny();
      return odswiezListe().then(function () {
        return przebuduj("Zapisano. Przebudowuję stronę…");
      });
    }).catch(function (e) {
      komunikat(e.message, true);
    }).then(function () {
      el(".zapisz").disabled = el(".usun").disabled = false;
    });
  }

  function usun() {
    if (!stan.biezacy) return;
    if (!confirm("Usunąć artykuł „" + stan.biezacy + "”? Tego nie da się cofnąć.")) return;
    api("articles/" + stan.biezacy, { metoda: "DELETE" }).then(function () {
      usunSzkicLokalny();   // musi być przed wyzerowaniem biezacy (klucz od niego zależy)
      stan.zmiany = {};
      stan.biezacy = null;
      // Bez tego szkic() dalej zwracałby usunięty artykuł, a pasek adresu
      // i podgląd trzymałyby jego treść.
      stan.artykul = null;
      podgladOstatni = "";
      return odswiezListe();
    }).then(function () {
      rysujFormularz(null);
      zaplanujPodglad();
      return przebuduj("Artykuł usunięty. Przebudowuję stronę…");
    }).catch(function (e) { komunikat(e.message, true); });
  }

  function odswiezListe() {
    return Promise.all([api("articles"), api("categories"),
                        api("adresy"), api("etykiety"), api("grafiki")])
      .then(function (wyniki) {
        stan.lista = wyniki[0];
        stan.kategorie = wyniki[1];
        stan.adresy = wyniki[2];
        stan.etykiety = wyniki[3];
        stan.grafiki = wyniki[4];
        rysujListe();
      });
  }

  // ============================================================ REFERENCJE
  // Druga zakladka panelu. Sekcja „Wybrane wdrozenia" na /referencje/ sklada
  // sie z kafli; wpis bez wgranego PDF-a zostaje kaflem „w trakcie tworzenia”.
  var widok = "artykuly";
  var refBiezaca = null;

  function przelaczWidok(nowy) {
    if (nowy === widok) return;   // klik w aktywną zakładkę nie resetuje formularza
    if (nowy === "referencje" && widok !== "referencje" && brudny() &&
        !confirm("Masz niezapisane zmiany w artykule. Przejść do referencji mimo to?\n" +
                 "(Kopia robocza zostanie zachowana.)")) {
      return;
    }
    if (nowy === "referencje") {
      clearTimeout(szkicTimer);
      zapiszSzkicLokalnie();
      stan.zmiany = {};
    }
    widok = nowy;
    root.querySelectorAll(".zakladka").forEach(function (b) {
      b.classList.toggle("akt", b.dataset.widok === nowy);
    });
    refBiezaca = null;
    if (nowy === "referencje") {
      el(".usun").style.display = "none";
      odswiezReferencje();
    } else {
      wczytaj(null);
    }
  }

  function odswiezReferencje() {
    return api("referencje").then(function (lista) {
      stan.referencje = lista;
      rysujListeReferencji();
      rysujFormularzReferencji(null);
    });
  }

  function rysujListeReferencji() {
    var fraza = (el(".szukaj").value || "").toLowerCase();
    var lista = el(".lista");
    lista.innerHTML = "";
    (stan.referencje || [])
      .filter(function (r) {
        return !fraza || (r.tytul + " " + (r.firma || "")).toLowerCase().indexOf(fraza) !== -1;
      })
      .forEach(function (r) {
        var poz = document.createElement("div");
        poz.className = "poz" + (refBiezaca === r.id ? " akt" : "") + (r.published ? "" : " ukryty");
        poz.innerHTML = "<strong></strong><small></small>";
        poz.querySelector("strong").textContent = r.tytul;
        poz.querySelector("small").textContent =
          (r.firma || "bez firmy") + (r.plik ? " · PDF" : " · brak pliku");
        poz.addEventListener("click", function () {
          refBiezaca = r.id;
          rysujFormularzReferencji(r);
          rysujListeReferencji();
        });
        lista.appendChild(poz);
      });
  }

  function poleRef(etykieta, klucz, wartosc, wielolinijkowe, pomoc) {
    var box = document.createElement("div");
    box.innerHTML = "<label></label>" +
      (wielolinijkowe ? "<textarea></textarea>" : '<input type="text">') +
      (pomoc ? '<div class="pomoc"></div>' : "");
    box.querySelector("label").textContent = etykieta;
    if (pomoc) box.querySelector(".pomoc").textContent = pomoc;
    var wej = box.querySelector("input,textarea");
    wej.dataset.klucz = klucz;
    wej.value = wartosc == null ? "" : wartosc;
    return box;
  }

  function rysujFormularzReferencji(r) {
    var form = el(".form");
    form.innerHTML = '<div class="komunikat" style="display:none"></div>';
    var box = document.createElement("div");
    box.className = "ref-form";

    box.appendChild(poleRef("Tytuł", "tytul", r && r.tytul, false,
      "Nagłówek kafla, np. „Kocioł parowy Fako”."));
    box.appendChild(poleRef("Firma lub zakład", "firma", r && r.firma, false,
      "Możesz zostawić puste, jeśli klient nie zgodził się na nazwę."));
    box.appendChild(poleRef("Opis", "opis", r && r.opis, true,
      "Dwa zdania o tym, czego dotyczy dokument."));

    var plik = document.createElement("div");
    plik.className = "ref-plik";
    plik.innerHTML =
      "<label>Dokument PDF</label>" +
      '<input type="file" accept="application/pdf,.pdf">' +
      '<div class="ref-plik__stan"></div>';
    var stanPliku = plik.querySelector(".ref-plik__stan");
    var sciezkaPliku = (r && r.plik) || "";

    function opiszPlik() {
      stanPliku.textContent = sciezkaPliku
        ? "Wgrany: " + sciezkaPliku
        : "Brak pliku — kafel pokaże napis „w trakcie tworzenia”.";
    }
    opiszPlik();

    plik.querySelector("input[type=file]").addEventListener("change", function (e) {
      var wybrany = e.target.files && e.target.files[0];
      if (!wybrany) return;
      stanPliku.textContent = "Wgrywam " + wybrany.name + "…";
      var czytnik = new FileReader();
      czytnik.onload = function () {
        api("referencje/wgraj", { metoda: "POST", dane: {
          nazwa: wybrany.name,
          dane: String(czytnik.result).split(",")[1]
        }}).then(function (w) {
          sciezkaPliku = w.plik;
          opiszPlik();
          komunikat(w.komunikat + " Kliknij Zapisz, żeby to utrwalić.", false);
        }).catch(function (err) {
          stanPliku.textContent = "Nie udało się wgrać: " + err.message;
          komunikat(err.message, true);
        });
      };
      czytnik.readAsDataURL(wybrany);
    });
    box.appendChild(plik);

    var dodatki = document.createElement("div");
    dodatki.className = "sekcja dwie";
    dodatki.innerHTML =
      "<div><label>Widoczna na stronie</label><select data-klucz='published'>" +
      "<option value='true'>tak</option><option value='false'>nie</option></select></div>" +
      "<div><label>Kolejność</label><input type='number' data-klucz='sort_order' value='0'></div>";
    dodatki.querySelector("[data-klucz=published]").value = r ? String(r.published) : "true";
    dodatki.querySelector("[data-klucz=sort_order]").value = r ? r.sort_order : 0;
    box.appendChild(dodatki);

    form.appendChild(box);

    el(".adres").textContent = r ? "/referencje/  ·  kafel „" + r.tytul + "”"
                                 : "/referencje/  ·  nowa referencja";
    el(".adres").style.color = "#9fe0b0";
    el(".usun").style.display = r ? "" : "none";

    form.dataset.plik = sciezkaPliku;
  }

  function zbierzReferencje() {
    var form = el(".form");
    var dane = { plik: form.dataset.plik || null };
    form.querySelectorAll("[data-klucz]").forEach(function (w) {
      var k = w.dataset.klucz;
      dane[k] = k === "published" ? w.value === "true"
              : k === "sort_order" ? (parseInt(w.value, 10) || 0)
              : w.value.trim() || null;
    });
    // Plik mogl zostac wgrany po narysowaniu formularza.
    var stanPliku = form.querySelector(".ref-plik__stan");
    if (stanPliku && stanPliku.textContent.indexOf("Wgrany: ") === 0) {
      dane.plik = stanPliku.textContent.replace("Wgrany: ", "").trim();
    }
    if (refBiezaca) dane.id = refBiezaca;
    return dane;
  }

  function zapiszReferencje() {
    el(".zapisz").disabled = el(".usun").disabled = true;
    komunikat("Zapisuję…", false);
    api("referencje", { metoda: "POST", dane: zbierzReferencje() })
      .then(function (w) {
        refBiezaca = w.id;
        return odswiezReferencje().then(function () {
          return przebuduj("Zapisano. Przebudowuję stronę…");
        });
      })
      .catch(function (e) { komunikat(e.message, true); })
      .then(function () { el(".zapisz").disabled = el(".usun").disabled = false; });
  }

  function usunReferencje() {
    if (!refBiezaca) return;
    if (!confirm("Usunąć tę referencję? Tego nie da się cofnąć.")) return;
    api("referencje/" + refBiezaca, { metoda: "DELETE" })
      .then(function () {
        refBiezaca = null;
        return odswiezReferencje();
      })
      .then(function () { return przebuduj("Referencja usunięta. Przebudowuję stronę…"); })
      .catch(function (e) { komunikat(e.message, true); });
  }

  // ---------------------------------------------------------------- skrót
  function otworz() {
    if (host) { host.style.display = ""; return; }
    budujOkno();
    odswiezListe().then(function () {
      rysujFormularz(null);
      // Oferujemy kopię roboczą „(nowy)" od razu po otwarciu — inaczej po awarii
      // przeglądarki niezapisany nowy wpis nie miałby jak wrócić.
      zaproponujSzkic();
    }).catch(function (e) {
      komunikat("Nie mogę połączyć się z API panelu (" + e.message + "). " +
                "Czy działa `docker compose up -d admin-api`?", true);
    });
  }

  function zamknij() { if (host) host.style.display = "none"; }

  function otwarty() { return !!host && host.style.display !== "none"; }
  function przelacz() { otwarty() ? zamknij() : otworz(); }

  var ostatniShift = 0;

  // Sprawdzamy OBA pola, bo każde zawodzi w innej sytuacji:
  //  * e.key  — na polskim układzie Ctrl+Alt to AltGr, więc np. Ctrl+Alt+A
  //             daje "ą" zamiast "a"
  //  * e.code — bywa puste przy zdarzeniach syntetycznych (automatyzacja,
  //             część rozszerzeń i narzędzi dostępności)
  function toKlawisz(e, litera) {
    return e.code === "Key" + litera.toUpperCase() ||
           (e.key && e.key.toLowerCase() === litera.toLowerCase());
  }

  document.addEventListener("keydown", function (e) {
    if (e.ctrlKey && e.shiftKey && toKlawisz(e, "y")) {
      e.preventDefault();
      przelacz();
      return;
    }

    // Ctrl+S zapisuje bieżący wpis zamiast otwierać zapis strony przeglądarki.
    if (e.ctrlKey && !e.shiftKey && !e.altKey && toKlawisz(e, "s") && otwarty()) {
      e.preventDefault();   // zawsze, żeby nie wyskoczył systemowy zapis strony
      // Przycisk Zapisz jest zablokowany na czas trwającego zapisu — to samo
      // źródło prawdy chroni przed podwójnym wysłaniem przez przytrzymany skrót.
      if (e.repeat || el(".zapisz").disabled) return;
      widok === "referencje" ? zapiszReferencje() : zapisz();
      return;
    }

    if (e.key === "Escape" && otwarty()) {
      // Escape schodzi o jeden poziom: najpierw warstwy edytora (menu,
      // dialog, pełny ekran pisania), potem wyjście z pełnego ekranu
      // podglądu, dopiero na końcu zamknięcie panelu. Inaczej jedno
      // naciśnięcie gubiłoby niezapisany formularz.
      if (zamknijWarstweRedaktora()) return;
      if (maksymalny()) przelaczMax(false);
      else zamknij();
      return;
    }

    // Podwójny Shift w ciągu 400 ms — awaryjnie, gdy skrót koliduje.
    // Ignorujemy, gdy kursor jest w polu tekstowym, żeby nie przeszkadzać w pisaniu.
    if (e.key === "Shift" && !e.ctrlKey && !e.altKey && !e.metaKey) {
      var cel = e.target;
      var wPolu = cel && (cel.tagName === "INPUT" || cel.tagName === "TEXTAREA" ||
                          cel.tagName === "SELECT" || cel.isContentEditable);
      var teraz = Date.now();
      if (!wPolu && teraz - ostatniShift < 400) {
        ostatniShift = 0;
        przelacz();
      } else {
        ostatniShift = teraz;
      }
    } else {
      ostatniShift = 0;
    }
  });

  // Ostatnia deska ratunku: dopisanie #panel do adresu.
  function sprawdzHash() {
    if (location.hash === "#panel" && !otwarty()) otworz();
  }
  window.addEventListener("hashchange", sprawdzHash);
  sprawdzHash();

  // Ułatwienie diagnostyki: wywołanie kabiPanel() w konsoli też otwiera panel.
  window.kabiPanel = przelacz;

  console.info("[panel] Panel redakcyjny gotowy. Otwórz: " + SKROT +
               ", albo wpisz kabiPanel() w konsoli.");
})();
