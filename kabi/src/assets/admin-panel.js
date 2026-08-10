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
    { k: "slug", label: "Adres (slug)", typ: "text", pomoc: "Zostanie adresem: /baza-wiedzy/<slug>/" },
    { k: "title", label: "Tytuł (H1 i <title>)", typ: "text" },
    { k: "list_title", label: "Tytuł na liście", typ: "text" },
    { k: "short", label: "Etykieta w breadcrumbach", typ: "text" },
    { k: "topic", label: "Nadtemat", typ: "lista",
      pomoc: "Widoczny nad tytułem i na liście artykułów." },
    { k: "lead", label: "Lead (idzie też w meta description)", typ: "textarea" },
    { k: "excerpt", label: "Zajawka na liście", typ: "text" },
    { k: "audience", label: "Dla kogo", typ: "text" },
    { k: "read_time", label: "Czas czytania", typ: "text", pomoc: "np. 6 min" },
    { k: "image", label: "Grafika", typ: "text", pomoc: "Pusto = grafika huba" },
    { k: "prose", label: "Treść artykułu", typ: "redaktor",
      pomoc: "Enter zaczyna nowy akapit (z odstępem). Shift+Enter łamie wiersz " +
             "wewnątrz akapitu, bez odstępu." },
    { k: "html", label: "Własny HTML całej strony", typ: "kod",
      pomoc: "Wypełnione = zastępuje cały układ powyżej. Pozwala wyjść poza schemat. " +
             "Nagłówek i stopka serwisu zostają." }
  ];

  // Pola listowe: kolumna → kolumny wiersza
  var LISTY = [
    { k: "faq", label: "FAQ", kolumny: [["q", "Pytanie"], ["a", "Odpowiedź"]] },
    // Wszystkie trzy pola są listami — etykieta z już używanych, tytuł
    // i adres z istniejących stron serwisu, wzajemnie zsynchronizowane.
    { k: "related", label: "Powiązane odnośniki",
      kolumny: [["kicker", "Etykieta", "etykiety"],
                ["title", "Tytuł", "tytuly-stron"],
                ["url", "Adres", "adresy"]] },
    { k: "feature_stats", label: "Liczby w hero", kolumny: [["value", "Wartość"], ["label", "Opis"]] }
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
    ".red{border:1px solid rgba(255,255,255,.14);border-radius:8px;overflow:hidden}" +
    ".red__pasek{display:flex;flex-wrap:wrap;gap:3px;padding:6px;background:#0a1620;border-bottom:1px solid rgba(255,255,255,.10)}" +
    ".red__pasek button{padding:4px 9px;font-size:12px;font-weight:600;background:#12384f}" +
    ".red__pasek button.akt{background:#1c6fa0;border-color:#3f9dd0}" +
    ".red__pasek .sep{width:1px;background:rgba(255,255,255,.14);margin:2px 4px}" +
    ".red__pasek .rosnie{flex:1}" +
    ".red__tresc{min-height:220px;max-height:460px;overflow:auto;padding:14px 16px;background:#08121a;font-size:14px;line-height:1.65;outline:none}" +
    ".red__tresc:focus{background:#091620}" +
    ".red__tresc h2{font-size:19px;margin:1.4em 0 .5em;color:#cfe6f4;font-weight:700}" +
    ".red__tresc h2:first-child{margin-top:0}" +
    ".red__tresc h3{font-size:15.5px;margin:1.2em 0 .4em;color:#bcd9ea;font-weight:700}" +
    ".red__tresc p{margin:0 0 .9em}" +
    ".red__tresc ul,.red__tresc ol{margin:0 0 .9em;padding-left:1.4em}" +
    ".red__tresc li{margin:.3em 0}" +
    ".red__tresc a{color:#7fc4e8}" +
    ".red__tresc p.note{border-left:3px solid #7fc4e8;padding:.5em 0 .5em .9em;color:#a9c9da;background:rgba(127,196,232,.07)}" +
    ".red__tresc:empty::before{content:attr(data-placeholder);color:#5d7382}" +
    ".wybor-grafiki{position:absolute;z-index:6;left:16px;right:16px;background:#0e1c26;box-shadow:0 12px 40px rgba(0,0,0,.55);max-height:70vh;overflow:auto}" +
    ".wybor-grafiki .opcje-foto{display:flex;gap:12px;margin-top:8px}" +
    ".wybor-grafiki .opcje-foto label{flex:1;font-size:11px}" +
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
    ".wybor-grafiki .siatka{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;margin-top:10px}" +
    ".wybor-grafiki .kafel{padding:0;overflow:hidden;background:#08121a;border:1px solid rgba(255,255,255,.14);border-radius:8px;cursor:pointer;text-align:left}" +
    ".wybor-grafiki .kafel:hover{border-color:#3f9dd0}" +
    ".wybor-grafiki .kafel img{display:block;width:100%;height:78px;object-fit:cover}" +
    ".wybor-grafiki .kafel span{display:block;padding:5px 7px;font-size:10.5px;line-height:1.3;color:#9fc0d2;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}" +
    ".red__tresc figure{margin:1.2em 0}" +
    ".red__tresc img{display:block;width:100%;height:auto;border-radius:8px}" +
    ".red__tresc figcaption{margin-top:.4em;font-size:12px;color:#8fa8b6}" +
    ".red__kod{width:100%;min-height:220px;border:0;border-radius:0;font-family:ui-monospace,Consolas,monospace;font-size:12.5px}" +
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
      return r.json().then(function (tresc) {
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
      '    <div class="naglowek"><h2>Baza wiedzy</h2></div>' +
      '    <input class="szukaj" type="text" placeholder="Szukaj artykułu…">' +
      '    <div class="lista"></div>' +
      '    <div style="padding:10px;border-top:1px solid rgba(255,255,255,.08)">' +
      '      <button class="nowy" style="width:100%">+ Nowy artykuł</button></div>' +
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
    el(".nowy").addEventListener("click", function () { wczytaj(null); });
    el(".zapisz").addEventListener("click", zapisz);
    el(".usun").addEventListener("click", usun);
    el(".szukaj").addEventListener("input", rysujListe);
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
      '<input type="text" style="display:none;margin-top:6px" placeholder="nazwa nowego nadtematu">' +
      (def.pomoc ? '<div class="pomoc"></div>' : "");
    pole.querySelector("label").textContent = def.label;
    if (def.pomoc) pole.querySelector(".pomoc").textContent = def.pomoc;

    var select = pole.querySelector("select");
    var wpis = pole.querySelector("input");
    var wartosci = istniejaceWartosci(def.k);
    // Wartość edytowanego wpisu może nie występować nigdzie indziej —
    // bez tego wypadłaby z listy i zapis po cichu by ją zmienił.
    if (wartosc && wartosci.indexOf(wartosc) === -1) wartosci.unshift(wartosc);

    select.innerHTML = '<option value="">(wybierz)</option>';
    wartosci.forEach(function (v) {
      var opt = document.createElement("option");
      opt.value = v;
      opt.textContent = v;
      if (v === wartosc) opt.selected = true;
      select.appendChild(opt);
    });
    var nowy = document.createElement("option");
    nowy.value = NOWY;
    nowy.textContent = "+ nowy nadtemat…";
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
  // spodem dokładnie ten zestaw HTML-a, który dopuszcza serwis:
  // h2, h3, p, p.note, ul, ol, li, strong, em, a.
  var DOZWOLONE = {
    H2: 1, H3: 1, P: 1, UL: 1, OL: 1, LI: 1, STRONG: 1, EM: 1, A: 1, BR: 1,
    FIGURE: 1, FIGCAPTION: 1, IMG: 1
  };
  var ZAMIENNIKI = { B: "STRONG", I: "EM", DIV: "P" };

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

  /** Sprowadza to, co wyprodukuje contenteditable, do dozwolonego HTML-a. */
  function oczysc(korzen) {
    var dokument = korzen.ownerDocument;

    // Te znaczniki usuwamy RAZEM z zawartoscia. Rozpuszczenie ich zostawiloby
    // kod jako widoczny tekst artykulu.
    var DO_WYRZUCENIA = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, IFRAME: 1, OBJECT: 1, EMBED: 1 };

    (function przejdz(wezel) {
      var dzieci = [].slice.call(wezel.childNodes);
      dzieci.forEach(przejdz);

      if (wezel.nodeType !== 1 || wezel === korzen) return;
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
        while (wezel.firstChild) wezel.parentNode.insertBefore(wezel.firstChild, wezel);
        wezel.parentNode.removeChild(wezel);
        return;
      }

      [].slice.call(wezel.attributes).forEach(function (atr) {
        var zostaje =
          (nazwa === "A" && (atr.name === "href" || atr.name === "target" || atr.name === "rel")) ||
          (atr.name === "class" && dozwolonaKlasa(nazwa, atr.value)) ||
          (nazwa === "IMG" && (atr.name === "src" || atr.name === "alt" ||
                               atr.name === "loading" || atr.name === "width" ||
                               atr.name === "height"));
        if (!zostaje) wezel.removeAttribute(atr.name);
      });
    })(korzen);

    // Przegladarka potrafi zbudowac <p><ul>…</ul></p> albo <p><p>…</p></p>.
    // To niedozwolone zagniezdzenie: przy nastepnej edycji przegladarka je
    // rozrywa i lista przepada. Rozpuszczamy akapit, ktory zawiera blok.
    var BLOKI_W_AKAPICIE = { P: 1, UL: 1, OL: 1, H2: 1, H3: 1, FIGURE: 1 };
    for (var runda = 0; runda < 5; runda++) {
      var winowajcy = [].slice.call(korzen.querySelectorAll("p")).filter(function (p) {
        return [].slice.call(p.children).some(function (dziecko) {
          return BLOKI_W_AKAPICIE[dziecko.tagName];
        });
      });
      if (!winowajcy.length) break;
      winowajcy.forEach(function (p) {
        while (p.firstChild) p.parentNode.insertBefore(p.firstChild, p);
        p.parentNode.removeChild(p);
      });
    }

    // Tekst i elementy liniowe lezace bezposrednio w korzeniu opakowujemy
    // w akapit — inaczej trafilyby na strone poza jakimkolwiek blokiem.
    var BLOKOWE = { H2: 1, H3: 1, P: 1, UL: 1, OL: 1, FIGURE: 1 };
    var biezacy = null;
    [].slice.call(korzen.childNodes).forEach(function (wezel) {
      var blok = wezel.nodeType === 1 && BLOKOWE[wezel.tagName];
      var pusty = wezel.nodeType === 3 && !wezel.nodeValue.trim();
      if (blok || pusty) { biezacy = null; return; }
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

  function poleRedaktor(def, wartosc) {
    var pole = document.createElement("div");
    pole.dataset.kolumna = def.k;
    pole.innerHTML =
      "<label></label>" +
      '<div class="red">' +
      '  <div class="red__pasek"></div>' +
      '  <div class="red__tresc" contenteditable="true" data-placeholder="Zacznij pisać…  (Enter = nowy akapit, Shift+Enter = złamanie wiersza)"></div>' +
      '  <textarea class="red__kod" style="display:none"></textarea>' +
      "</div>" +
      (def.pomoc ? '<div class="pomoc"></div>' : "");
    pole.querySelector("label").textContent = def.label;
    if (def.pomoc) pole.querySelector(".pomoc").textContent = def.pomoc;

    var pasek = pole.querySelector(".red__pasek");
    var tresc = pole.querySelector(".red__tresc");
    var kod = pole.querySelector(".red__kod");
    tresc.innerHTML = wartosc || "";

    /** Zaznaczenie widoczne WEWNATRZ Shadow DOM.
     *  document.getSelection() zwraca tu zaznaczenie przekierowane na hosta,
     *  przez co anchorNode nigdy nie trafia w wezel edytora. */
    function zaznaczenie() {
      var korzen = tresc.getRootNode();
      var sel = (korzen && korzen.getSelection) ? korzen.getSelection()
                                                : tresc.ownerDocument.getSelection();
      return sel && tresc.contains(sel.anchorNode) ? sel : null;
    }

    function zapiszStan() {
      stan.zmiany[def.k] = kod.style.display === "none" ? oczysc(tresc) : kod.value;
      zaplanujPodglad();
    }

    function polecenie(cmd, arg) {
      tresc.focus();
      document.execCommand(cmd, false, arg);
      zapiszStan();
    }

    function przycisk(etykieta, tytul, dzialanie) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = etykieta;
      b.title = tytul;
      // mousedown zamiast click: klik najpierw zabrałby zaznaczenie tekstu,
      // a bez zaznaczenia polecenia formatujące nie mają na czym działać.
      b.addEventListener("mousedown", function (e) { e.preventDefault(); dzialanie(); });
      pasek.appendChild(b);
      return b;
    }

    function separator() {
      var s = document.createElement("span");
      s.className = "sep";
      pasek.appendChild(s);
    }

    // Zestaw i nazewnictwo pod redaktora, nie pod programiste: zamiast
    // "H2"/"H3" jest "Naglowek", zamiast wpisywania adresu — wybor strony,
    // zamiast znacznika <img> — wybor grafiki z podgladem.
    przycisk("Nagłówek", "Nagłówek sekcji artykułu", function () {
      polecenie("formatBlock", "<h2>");
    });
    przycisk("Paragraf", "Zwykły akapit tekstu", function () {
      polecenie("formatBlock", "<p>");
    });
    /** Zamienia bloki objete zaznaczeniem w liste (albo liste z powrotem
     *  w akapity). Robimy to sami, bo execCommand potrafi zbudowac
     *  <p><ul>…</ul></p>, co rozpada sie przy nastepnej edycji. */
    function przelaczListe(znacznik) {
      var bloki = blokiZaznaczenia();
      if (!bloki.length) {
        komunikat("Ustaw kursor w tekście, który ma być listą.", true);
        return;
      }

      // Kursor w istniejacej liscie tego samego rodzaju → rozbijamy na akapity.
      var lista = bloki[0].closest && bloki[0].closest(znacznik.toLowerCase());
      if (lista && tresc.contains(lista)) {
        [].slice.call(lista.children).forEach(function (li) {
          var p = tresc.ownerDocument.createElement("p");
          while (li.firstChild) p.appendChild(li.firstChild);
          lista.parentNode.insertBefore(p, lista);
        });
        lista.parentNode.removeChild(lista);
        zapiszStan();
        return;
      }

      var nowa = tresc.ownerDocument.createElement(znacznik);
      bloki[0].parentNode.insertBefore(nowa, bloki[0]);
      bloki.forEach(function (blok) {
        var li = tresc.ownerDocument.createElement("li");
        while (blok.firstChild) li.appendChild(blok.firstChild);
        nowa.appendChild(li);
        blok.parentNode.removeChild(blok);
      });
      zapiszStan();
    }

    przycisk("Lista punktowana", "Lista wypunktowana", function () {
      przelaczListe("UL");
    });
    przycisk("Lista numerowana", "Lista numerowana", function () {
      przelaczListe("OL");
    });
    przycisk("Zdjęcie", "Wstaw grafikę z zasobów serwisu", function () {
      pokazWyborGrafiki(function (kodHtml) {
        tresc.focus();
        document.execCommand("insertHTML", false, kodHtml);
        zapiszStan();
      });
    });
    przycisk("Link", "Wstaw odnośnik do strony serwisu", function () {
      var sel = zaznaczenie();
      if (!sel || !String(sel)) {
        komunikat("Zaznacz najpierw tekst, który ma być odnośnikiem.", true);
        return;
      }
      pokazWyborStrony(function (url) { polecenie("createLink", url); });
    });

    separator();

    var BLOKI_TRESCI = { P: 1, H2: 1, H3: 1, LI: 1, FIGURE: 1 };

    /** WSZYSTKIE bloki objete zaznaczeniem, nie tylko ten z kursorem —
     *  inaczej zaznaczenie trzech akapitow wyrownywaloby jeden. */
    function blokiZaznaczenia() {
      var sel = zaznaczenie();
      if (!sel || !sel.rangeCount) return [];
      var zakres = sel.getRangeAt(0);

      var wszystkie = [].slice.call(tresc.querySelectorAll("p,h2,h3,li,figure"));
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
      zapiszStan();
    }

    przycisk("\u2261 Lewo", "Wyrównaj do lewej (domyślnie)", function () { wyrownaj(null); });
    przycisk("\u2261 Środek", "Wyśrodkuj", function () { wyrownaj("tekst-srodek"); });
    przycisk("\u2261 Prawo", "Wyrównaj do prawej", function () { wyrownaj("tekst-prawo"); });

    separator();
    przycisk("B", "Pogrubienie", function () { polecenie("bold"); });
    przycisk("I", "Kursywa", function () { polecenie("italic"); });
    przycisk("Uwaga", "Wyróżniony akapit na marginesie", function () {
      tresc.focus();
      document.execCommand("formatBlock", false, "<p>");
      var sel = zaznaczenie();
      var wezel = sel && sel.anchorNode;
      while (wezel && wezel !== tresc && wezel.tagName !== "P") wezel = wezel.parentNode;
      if (wezel && wezel.tagName === "P") wezel.classList.toggle("note");
      else komunikat("Ustaw kursor w akapicie, który ma być uwagą.", true);
      zapiszStan();
    });

    separator();
    var rosnie = document.createElement("span");
    rosnie.className = "rosnie";
    pasek.appendChild(rosnie);

    var przelacznik = przycisk("HTML", "Podejrzyj i popraw kod źródłowy", function () {
      var doKodu = kod.style.display === "none";
      if (doKodu) {
        kod.value = oczysc(tresc);
        kod.style.display = "";
        tresc.style.display = "none";
        przelacznik.classList.add("akt");
      } else {
        tresc.innerHTML = kod.value;
        kod.style.display = "none";
        tresc.style.display = "";
        przelacznik.classList.remove("akt");
      }
      zapiszStan();
    });

    tresc.addEventListener("input", zapiszStan);
    kod.addEventListener("input", zapiszStan);

    // Wklejanie zawsze jako czysty tekst — inaczej z Worda albo strony WWW
    // wjeżdżają style, tabele i znaczniki, których serwis nie obsługuje.
    tresc.addEventListener("paste", function (e) {
      e.preventDefault();
      var tekst = (e.clipboardData || window.clipboardData).getData("text/plain");
      document.execCommand("insertText", false, tekst);
    });

    return pole;
  }

  /** Wybór grafiki z podglądem. Redaktor nie wpisuje ścieżki ani znacznika. */
  function pokazWyborGrafiki(gotowe) {
    var okno = document.createElement("div");
    okno.className = "sekcja wybor-grafiki";
    okno.innerHTML =
      "<h3>Wstaw zdjęcie</h3>" +
      '<input type="text" class="opis" placeholder="Opis zdjęcia (alt) — ważny dla wyszukiwarki i czytników ekranu">' +
      '<input type="text" class="podpis" placeholder="Podpis pod zdjęciem (opcjonalny)" style="margin-top:6px">' +
      '<div class="opcje-foto">' +
      '  <label>Rozmiar<select class="rozmiar">' +
      '    <option value="foto-pelna">pełna szerokość</option>' +
      '    <option value="foto-srednia">średnie (65%)</option>' +
      '    <option value="foto-mala">małe (40%)</option>' +
      '  </select></label>' +
      '  <label>Położenie<select class="polozenie">' +
      '    <option value="tekst-srodek" selected>osobno, wyśrodkowane</option>' +
      '    <option value="">osobno, do lewej</option>' +
      '    <option value="tekst-prawo">osobno, do prawej</option>' +
      '    <option value="foto-oblewa-lewo">obok tekstu, z lewej</option>' +
      '    <option value="foto-oblewa-prawo">obok tekstu, z prawej</option>' +
      '  </select></label>' +
      '</div>' +
      '<div class="siatka"></div>' +
      '<button class="anuluj" style="margin-top:10px">Anuluj</button>';

    var siatka = okno.querySelector(".siatka");
    var opis = okno.querySelector(".opis");
    var podpis = okno.querySelector(".podpis");

    (stan.grafiki || []).forEach(function (g) {
      var kafel = document.createElement("button");
      kafel.className = "kafel";
      kafel.title = g.url + "  (" + g.rozmiar_kb + " kB)";
      kafel.innerHTML = '<img src="' + g.url + '" alt="" loading="lazy"><span></span>';
      kafel.querySelector("span").textContent = g.nazwa;
      kafel.addEventListener("click", function () {
        var alt = opis.value.trim();
        if (!alt) {
          komunikat("Wpisz opis zdjęcia — bez niego grafika jest niewidoczna " +
                    "dla wyszukiwarki i czytników ekranu.", true);
          opis.focus();
          return;
        }
        var podpisTekst = podpis.value.trim();
        var klasy = [okno.querySelector(".rozmiar").value,
                     okno.querySelector(".polozenie").value].filter(Boolean).join(" ");
        var kod = '<figure class="' + klasy + '"><img src="' + g.url +
                  '" alt="' + alt.replace(/"/g, "&quot;") + '" loading="lazy">' +
                  (podpisTekst ? "<figcaption>" + podpisTekst + "</figcaption>" : "") +
                  "</figure><p><br></p>";
        okno.remove();
        gotowe(kod);
      });
      siatka.appendChild(kafel);
    });

    // Grafika na pelna szerokosc nie da sie oblac tekstem — przy wyborze
    // oblewania podnosimy rozmiar do sredniego, zamiast dawac ustawienie,
    // ktore nic nie zmienia.
    var polePolozenia = okno.querySelector(".polozenie");
    var poleRozmiaru = okno.querySelector(".rozmiar");
    polePolozenia.addEventListener("change", function () {
      var oblewa = polePolozenia.value.indexOf("oblewa") !== -1;
      if (oblewa && poleRozmiaru.value === "foto-pelna") {
        poleRozmiaru.value = "foto-srednia";
        komunikat("Grafika oblewana tekstem nie może zajmować pełnej " +
                  "szerokości — ustawiłem rozmiar średni.", false);
      }
    });

    okno.querySelector(".anuluj").addEventListener("click", function () { okno.remove(); });
    el(".form").appendChild(okno);
    okno.scrollIntoView({ block: "nearest" });
    opis.focus();
  }

  /** Małe okienko wyboru strony — używane przy wstawianiu odnośnika. */
  function pokazWyborStrony(gotowe) {
    var wybor = document.createElement("select");
    wybor.innerHTML = '<option value="">(wybierz stronę)</option>';
    stan.adresy.forEach(function (a) {
      var opt = document.createElement("option");
      opt.value = a.url;
      opt.textContent = a.etykieta + "  —  " + a.url;
      wybor.appendChild(opt);
    });

    var okno = document.createElement("div");
    okno.className = "sekcja";
    okno.style.cssText = "position:absolute;z-index:5;left:16px;right:16px;background:#0e1c26;box-shadow:0 12px 40px rgba(0,0,0,.5)";
    okno.innerHTML = "<h3>Odnośnik do strony</h3>";
    okno.appendChild(wybor);
    var anuluj = document.createElement("button");
    anuluj.textContent = "Anuluj";
    anuluj.style.marginTop = "10px";
    anuluj.addEventListener("click", function () { okno.remove(); });
    okno.appendChild(anuluj);

    wybor.addEventListener("change", function () {
      if (wybor.value) gotowe(wybor.value);
      okno.remove();
    });

    el(".form").appendChild(okno);
    wybor.focus();
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

  // ------------------------------------------------------------- podgląd
  var podgladTimer = null, podgladOstatni = "";

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
    if (!podgladWlaczony()) return;
    clearTimeout(podgladTimer);
    stanPodgladu("składam…", true);
    podgladTimer = setTimeout(odswiezPodglad, 350);
  }

  function odswiezPodglad() {
    var dane = szkic();
    var odcisk = JSON.stringify(dane);
    if (odcisk === podgladOstatni) { stanPodgladu("aktualny", false); return; }
    podgladOstatni = odcisk;

    api("preview", { metoda: "POST", dane: dane }).then(function (w) {
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
      stanPodgladu("błąd: " + e.message, false);
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
      '<div class="pomoc">Kategoria bez artykułów przekierowuje na hub — pierwszy artykuł tworzy jej stronę.</div>';
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
    dodatki.querySelector(".pub").value = artykul ? String(artykul.published) : "true";
    dodatki.querySelector(".kol").value = artykul ? artykul.sort_order : 0;
    dodatki.querySelector(".pub").addEventListener("change", function (e) {
      stan.zmiany.published = e.target.value === "true";
    });
    dodatki.querySelector(".kol").addEventListener("input", function (e) {
      stan.zmiany.sort_order = parseInt(e.target.value, 10) || 0;
    });
    // published i sort_order nie zmieniają wyglądu strony artykułu,
    // więc celowo nie odświeżają podglądu.
    form.appendChild(dodatki);

    el(".usun").style.display = artykul ? "" : "none";
    odswiezAdres();
  }

  // ------------------------------------------------------------- operacje
  function wczytaj(slug) {
    stan.zmiany = {};
    stan.artykul = null;
    stan.biezacy = slug;
    podgladOstatni = "";
    if (!slug) {
      rysujFormularz(null);
      rysujListe();
      zaplanujPodglad();
      return;
    }
    api("articles/" + slug).then(function (a) {
      stan.artykul = a;
      stan.zmiany = {};
      rysujFormularz(a);
      rysujListe();
      odswiezPodglad();
    }).catch(function (e) { komunikat(e.message, true); });
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
      stan.biezacy = wynik.slug;
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
      stan.biezacy = null;
      return odswiezListe();
    }).then(function () {
      rysujFormularz(null);
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

  // ---------------------------------------------------------------- skrót
  function otworz() {
    if (host) { host.style.display = ""; return; }
    budujOkno();
    odswiezListe().then(function () {
      rysujFormularz(null);
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

    if (e.key === "Escape" && otwarty()) {
      // Escape schodzi o jeden poziom: najpierw wyjście z pełnego ekranu,
      // dopiero potem zamknięcie panelu. Inaczej jedno naciśnięcie gubiłoby
      // niezapisany formularz.
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
