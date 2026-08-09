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
    { k: "prose", label: "Treść artykułu (HTML)", typ: "kod",
      pomoc: "Wstawiana w standardowy układ: hero, treść, FAQ, powiązania." },
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

  var host, root, stan = { lista: [], kategorie: [], adresy: [], etykiety: [],
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
      '      <button class="publikuj">Zapisz i przebuduj</button>' +
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
    el(".zapisz").addEventListener("click", function () { zapisz(false); });
    el(".publikuj").addEventListener("click", function () { zapisz(true); });
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

  function poleTekstowe(def, wartosc) {
    if (def.typ === "lista") return poleListy(def, wartosc);

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

  function zapisz(przebuduj) {
    var dane = {};
    Object.keys(stan.zmiany).forEach(function (k) { dane[k] = stan.zmiany[k]; });
    if (!dane.slug && stan.biezacy) dane.slug = stan.biezacy;

    var zadanie = stan.biezacy
      ? api("articles/" + stan.biezacy, { metoda: "PUT", dane: dane })
      : api("articles", { metoda: "POST", dane: dane });

    el(".zapisz").disabled = el(".publikuj").disabled = true;
    komunikat("Zapisuję…", false);

    zadanie.then(function (wynik) {
      stan.biezacy = wynik.slug;
      return odswiezListe().then(function () {
        if (!przebuduj) { komunikat(wynik.komunikat, false); return; }
        komunikat("Zapisano. Przebudowuję stronę…", false);
        return api("publish", { metoda: "POST", dane: {} }).then(function (b) {
          komunikat(b.ok
            ? "Gotowe. Strona przebudowana — odśwież, żeby zobaczyć zmiany."
            : "Zapisano, ale build się nie powiódł:\n" + b.wyjscie, !b.ok);
        });
      });
    }).catch(function (e) {
      komunikat(e.message, true);
    }).then(function () {
      el(".zapisz").disabled = el(".publikuj").disabled = false;
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
      komunikat("Artykuł usunięty. Przebuduj stronę, żeby zniknął z www/.", false);
    }).catch(function (e) { komunikat(e.message, true); });
  }

  function odswiezListe() {
    return Promise.all([api("articles"), api("categories"),
                        api("adresy"), api("etykiety")])
      .then(function (wyniki) {
        stan.lista = wyniki[0];
        stan.kategorie = wyniki[1];
        stan.adresy = wyniki[2];
        stan.etykiety = wyniki[3];
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
