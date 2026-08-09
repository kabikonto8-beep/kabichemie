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
    { k: "topic", label: "Nadtemat", typ: "text", pomoc: "np. Kotły parowe" },
    { k: "lead", label: "Lead (idzie też w meta description)", typ: "textarea" },
    { k: "excerpt", label: "Zajawka na liście", typ: "text" },
    { k: "audience", label: "Dla kogo", typ: "text" },
    { k: "read_time", label: "Czas czytania", typ: "text", pomoc: "np. 6 min" },
    { k: "image", label: "Grafika", typ: "text", pomoc: "Pusto = grafika huba" },
    { k: "prose", label: "Treść artykułu (HTML)", typ: "kod" }
  ];

  // Pola listowe: kolumna → kolumny wiersza
  var LISTY = [
    { k: "faq", label: "FAQ", kolumny: [["q", "Pytanie"], ["a", "Odpowiedź"]] },
    { k: "related", label: "Powiązane odnośniki", kolumny: [["kicker", "Etykieta"], ["title", "Tytuł"], ["url", "Adres"]] },
    { k: "feature_stats", label: "Liczby w hero", kolumny: [["value", "Wartość"], ["label", "Opis"]] }
  ];

  var STYLE = "" +
    ":host{all:initial}" +
    "*{box-sizing:border-box;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif}" +
    ".tlo{position:fixed;inset:0;background:rgba(4,18,28,.62);backdrop-filter:blur(3px);z-index:2147483000;display:flex;align-items:stretch;justify-content:center;padding:24px}" +
    ".okno{background:#0e1c26;color:#e8f1f6;border:1px solid #1d3a4d;border-radius:14px;width:min(1180px,100%);display:grid;grid-template-columns:290px 1fr;overflow:hidden;box-shadow:0 24px 70px rgba(0,0,0,.5)}" +
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
    ".sekcja{border:1px solid rgba(255,255,255,.10);border-radius:10px;padding:12px}" +
    ".sekcja h3{margin:0 0 10px;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:#7fc4e8}" +
    ".komunikat{padding:8px 12px;border-radius:8px;font-size:12.5px;line-height:1.45}" +
    ".ok{background:rgba(46,125,80,.25);border:1px solid rgba(102,187,106,.5)}" +
    ".zly{background:rgba(140,40,30,.3);border:1px solid rgba(226,114,91,.55)}" +
    ".adres{font-family:ui-monospace,Consolas,monospace;font-size:12px;color:#9fe0b0}" +
    ".dwie{display:grid;grid-template-columns:1fr 1fr;gap:12px}" +
    "pre{white-space:pre-wrap;word-break:break-word;margin:0;font-size:11.5px;max-height:180px;overflow:auto}";

  var host, root, stan = { lista: [], kategorie: [], biezacy: null, zmiany: {} };

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
      '      <button class="zapisz glowny">Zapisz</button>' +
      '      <button class="publikuj">Zapisz i przebuduj</button>' +
      '      <button class="usun grozny">Usuń</button>' +
      '      <button class="zamknij">Zamknij</button>' +
      '    </div>' +
      '    <div class="form"></div>' +
      '  </div>' +
      '</div>';
    root.appendChild(tlo);

    tlo.addEventListener("mousedown", function (e) { if (e.target === tlo) zamknij(); });
    el(".zamknij").addEventListener("click", zamknij);
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

  function poleTekstowe(def, wartosc) {
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
    }

    function dodajWiersz(dane) {
      var w = document.createElement("div");
      w.className = "wiersz";
      w.style.gridTemplateColumns = def.kolumny.map(function () { return "1fr"; }).join(" ") + " auto";
      def.kolumny.forEach(function (kol) {
        var ta = document.createElement("textarea");
        ta.dataset.pole = kol[0];
        ta.placeholder = kol[1];
        ta.value = (dane && dane[kol[0]]) || "";
        ta.addEventListener("input", zbierz);
        w.appendChild(ta);
      });
      var kasuj = document.createElement("button");
      kasuj.textContent = "×";
      kasuj.title = "Usuń wiersz";
      kasuj.addEventListener("click", function () { w.remove(); zbierz(); });
      w.appendChild(kasuj);
      wiersze.appendChild(w);
    }

    (wartosc || []).forEach(dodajWiersz);
    sekcja.querySelector(".dodaj").addEventListener("click", function () { dodajWiersz(null); zbierz(); });
    return sekcja;
  }

  function odswiezAdres() {
    var slug = (stan.zmiany.slug != null ? stan.zmiany.slug : "").trim();
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
    form.appendChild(dodatki);

    el(".usun").style.display = artykul ? "" : "none";
    odswiezAdres();
  }

  // ------------------------------------------------------------- operacje
  function wczytaj(slug) {
    stan.zmiany = {};
    stan.biezacy = slug;
    if (!slug) {
      rysujFormularz(null);
      rysujListe();
      return;
    }
    api("articles/" + slug).then(function (a) {
      stan.zmiany = { category_id: a.category_id, published: a.published, sort_order: a.sort_order };
      rysujFormularz(a);
      rysujListe();
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
    return Promise.all([api("articles"), api("categories")]).then(function (wyniki) {
      stan.lista = wyniki[0];
      stan.kategorie = wyniki[1];
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
      zamknij();
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
