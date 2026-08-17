/* KABI CHEMIE — drobna interaktywność (bez zależności) */
(function () {
  "use strict";

  // --- menu mobilne ---
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  var mobileNavMq = window.matchMedia("(max-width: 1160px)");
  var setMobileNavOpen = function (open) {
    if (!toggle || !nav) return;
    nav.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.documentElement.classList.toggle("nav-open", open && mobileNavMq.matches);
  };
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setMobileNavOpen(!nav.classList.contains("open"));
    });
    nav.addEventListener("click", function (event) {
      var link = event.target.closest("a");
      if (!link || !mobileNavMq.matches) return;
      var topLevelSubmenu = link.parentElement && link.parentElement.classList.contains("has-sub");
      if (topLevelSubmenu && !link.parentElement.classList.contains("open")) return;
      if (!topLevelSubmenu || link.closest(".nav-panel")) setMobileNavOpen(false);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key !== "Escape" || !nav.classList.contains("open")) return;
      setMobileNavOpen(false);
      toggle.focus();
    });
    window.addEventListener("resize", function () {
      if (!mobileNavMq.matches && nav.classList.contains("open")) setMobileNavOpen(false);
    });
    window.addEventListener("pageshow", function () {
      if (!nav.classList.contains("open")) document.documentElement.classList.remove("nav-open");
    });
  }

  // --- FAQ firmowe: tylko jedna odpowiedź aktywna w całym zestawie ---
  var companyFaqItems = Array.prototype.slice.call(document.querySelectorAll(".company-faq-editorial details"));
  companyFaqItems.forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (!item.open) return;
      companyFaqItems.forEach(function (other) {
        if (other !== item && other.open) other.open = false;
      });
    });
  });

  // --- mega-menu: hover/focus na desktopie, pierwszy tap na mobile ---
  var mq = window.matchMedia("(max-width: 1160px)");
  var submenuItems = Array.prototype.slice.call(document.querySelectorAll(".has-sub"));
  var clearSubmenuTimer = function (item) {
    if (!item._submenuCloseTimer) return;
    window.clearTimeout(item._submenuCloseTimer);
    item._submenuCloseTimer = null;
  };
  var closeSubmenu = function (item) {
    clearSubmenuTimer(item);
    item.classList.remove("is-open");
    item.removeAttribute("data-click-open");
    var trigger = item.querySelector(":scope > a");
    if (trigger) trigger.setAttribute("aria-expanded", "false");
  };
  var scheduleSubmenuClose = function (item) {
    clearSubmenuTimer(item);
    item._submenuCloseTimer = window.setTimeout(function () {
      item._submenuCloseTimer = null;
      closeSubmenu(item);
    }, 260);
  };
  var openSubmenu = function (item) {
    clearSubmenuTimer(item);
    submenuItems.forEach(function (other) { if (other !== item) closeSubmenu(other); });
    item.classList.add("is-open");
    var trigger = item.querySelector(":scope > a");
    if (trigger) trigger.setAttribute("aria-expanded", "true");
  };

  submenuItems.forEach(function (item) {
    var link = item.querySelector(":scope > a");
    var panel = item.querySelector(":scope > .nav-panel");
    if (!link) return;
    // Desktop: panel otwiera się tylko po kliknięciu (nie na hover). Klik przełącza otwarcie.
    item.addEventListener("focusout", function () {
      if (mq.matches) return;
      window.setTimeout(function () {
        if (!item.contains(document.activeElement)) closeSubmenu(item);
      }, 0);
    });
    link.addEventListener("click", function (e) {
      var li = link.parentElement;
      if (!mq.matches) {
        e.preventDefault();
        if (li.classList.contains("is-open")) {
          closeSubmenu(li);
        } else {
          openSubmenu(li);
        }
        return;
      }
      if (!li.classList.contains("open")) {
        e.preventDefault();              // pierwszy tap: rozwiń
        document.querySelectorAll(".has-sub.open").forEach(function (o) {
          if (o !== li) {
            o.classList.remove("open");
            var oldTrigger = o.querySelector(":scope > a");
            if (oldTrigger) oldTrigger.setAttribute("aria-expanded", "false");
          }
        });
        li.classList.add("open");
        link.setAttribute("aria-expanded", "true");
      }
    });
    item.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      item.classList.remove("open");
      closeSubmenu(item);
      link.focus();
    });
  });

  document.addEventListener("click", function (e) {
    if (mq.matches || e.target.closest(".has-sub")) return;
    submenuItems.forEach(closeSubmenu);
  });

  // --- autostart wideo w hero (niezawodny fallback dla mobile/iOS) ---
  var heroVid = document.querySelector(".hero-bg");
  if (heroVid) {
    var tryPlay = function () { var p = heroVid.play(); if (p && p.catch) p.catch(function () {}); };
    // pętla ponawiająca: próbuj co 250 ms, aż film ruszy (max ~6 s)
    var attempts = 0;
    var pump = setInterval(function () {
      if (!heroVid.paused || ++attempts > 24) { clearInterval(pump); return; }
      tryPlay();
    }, 250);
    heroVid.addEventListener("loadeddata", tryPlay);
    heroVid.addEventListener("canplay", tryPlay);
    window.addEventListener("load", tryPlay);
    // pierwsza interakcja użytkownika jako ostateczny fallback
    ["touchstart", "click", "scroll"].forEach(function (ev) {
      window.addEventListener(ev, function once() {
        tryPlay();
        window.removeEventListener(ev, once);
      }, { passive: true });
    });
    tryPlay();
  }

  // --- cień nagłówka przy scrollu ---
  var header = document.querySelector(".site-header");
  if (header) {
    var lastY = window.scrollY || window.pageYOffset || 0;
    var onScroll = function () {
      var currentY = window.scrollY || window.pageYOffset || 0;
      var delta = currentY - lastY;
      var menuOpen = nav && (nav.classList.contains("open") || nav.querySelector(".has-sub.is-open"));
      header.classList.toggle("solid", currentY > 72);
      if (currentY < 90 || menuOpen) {
        header.classList.remove("nav-hidden");
      } else if (delta > 6 && currentY > 180) {
        header.classList.add("nav-hidden");
      } else if (delta < -6) {
        header.classList.remove("nav-hidden");
      }
      lastY = Math.max(0, currentY);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // --- animacje sekcji, liczników i wykresów ---
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // --- rotator zdań w hero ---
  document.querySelectorAll("[data-hero-rotator]").forEach(function (rotator) {
    var sentences = Array.prototype.slice.call(rotator.querySelectorAll(".hero-sentence"));
    if (sentences.length < 2) return;
    var active = Math.max(0, sentences.findIndex(function (sentence) {
      return sentence.classList.contains("is-active");
    }));
    sentences.forEach(function (sentence, index) {
      sentence.classList.toggle("is-active", index === active);
      sentence.classList.remove("is-exiting");
    });
    if (reduceMotion) return;

    var rotate = function () {
      var current = sentences[active];
      var nextIndex = (active + 1) % sentences.length;
      var next = sentences[nextIndex];
      current.classList.remove("is-active");
      current.classList.add("is-exiting");
      next.classList.add("is-active");
      window.setTimeout(function () {
        current.classList.remove("is-exiting");
      }, 680);
      active = nextIndex;
    };
    window.setTimeout(function () {
      rotate();
      window.setInterval(rotate, 3600);
    }, 3000);
  });

  // --- HERO V2: subtelny parallax kursora i separacja planów przy scrollu ---
  var heroV2 = document.querySelector("[data-hero-v2]");
  if (heroV2) {
    var heroStageV2 = heroV2.querySelector("[data-hero-stage]");
    var heroCommandV2 = heroV2.querySelector("[data-hero-command]");
    var heroPointerTicking = false;
    var heroPointerX = 0;
    var heroPointerY = 0;

    var applyHeroPointer = function () {
      heroPointerTicking = false;
      if (!heroStageV2 || !heroCommandV2 || reduceMotion) return;
      heroV2.style.setProperty("--hero-shift-x", (heroPointerX * 14).toFixed(1) + "px");
      heroV2.style.setProperty("--hero-shift-y", (heroPointerY * 10).toFixed(1) + "px");
      heroCommandV2.style.setProperty("--hero-rotate-x", (heroPointerY * -2.4).toFixed(2) + "deg");
      heroCommandV2.style.setProperty("--hero-rotate-y", (heroPointerX * 3.2).toFixed(2) + "deg");
    };
    var requestHeroPointer = function () {
      if (heroPointerTicking) return;
      heroPointerTicking = true;
      requestAnimationFrame(applyHeroPointer);
    };
    heroV2.addEventListener("pointermove", function (event) {
      if (window.innerWidth < 960 || reduceMotion) return;
      var rect = heroV2.getBoundingClientRect();
      heroPointerX = ((event.clientX - rect.left) / Math.max(1, rect.width) - .5) * 2;
      heroPointerY = ((event.clientY - rect.top) / Math.max(1, rect.height) - .5) * 2;
      requestHeroPointer();
    }, { passive: true });
    heroV2.addEventListener("pointerleave", function () {
      heroPointerX = 0;
      heroPointerY = 0;
      requestHeroPointer();
    });

    var heroScrollTicking = false;
    var applyHeroScroll = function () {
      heroScrollTicking = false;
      if (!heroStageV2) return;
      var progress = reduceMotion ? 0 : Math.max(0, Math.min(1, (window.scrollY || window.pageYOffset || 0) / Math.max(1, heroV2.offsetHeight * .72)));
      heroStageV2.style.translate = "0 " + (-progress * 34).toFixed(1) + "px";
      heroStageV2.style.opacity = (1 - progress * .42).toFixed(3);
    };
    var requestHeroScroll = function () {
      if (heroScrollTicking) return;
      heroScrollTicking = true;
      requestAnimationFrame(applyHeroScroll);
    };
    window.addEventListener("scroll", requestHeroScroll, { passive: true });
    window.addEventListener("resize", requestHeroScroll);
    applyHeroScroll();
  }

  var logoRails = document.querySelectorAll("[data-logo-rail]");
  var trustLabel = document.querySelector("[data-trust-label]");
  var partnerScale = document.querySelector("[data-partner-scale]");
  var updatePartnerScaleCount = function (progress) {
    if (!partnerScale) return;
    var number = partnerScale.querySelector(".partner-scale-number");
    if (!number) return;
    var target = Number(number.getAttribute("data-count-to") || "164");
    var suffix = number.getAttribute("data-suffix") || "+";
    var visibleProgress = reduceMotion ? 1 : Math.max(0, Math.min(1, progress));
    number.textContent = Math.round(target * visibleProgress) + suffix;
  };
  if (logoRails.length) {
    logoRails.forEach(function (rail) {
      var track = rail.querySelector(".partner-track");
      if (!track || track.dataset.cloned === "1") return;
      var originals = Array.prototype.slice.call(track.children);
      for (var i = 1; i < Number(rail.getAttribute("data-repeats") || "3"); i += 1) {
        originals.forEach(function (node) {
          var clone = node.cloneNode(true);
          clone.setAttribute("aria-hidden", "true");
          clone.querySelectorAll("img").forEach(function (img) {
            img.setAttribute("alt", "");
          });
          track.appendChild(clone);
        });
      }
      track.dataset.cloned = "1";
    });
    var logoTicking = false;
    var updateLogoRails = function () {
      logoTicking = false;
      if (trustLabel) {
        var trustSection = trustLabel.closest(".partner-marquee");
        var rect = trustSection ? trustSection.getBoundingClientRect() : { top: 0 };
        var tvh = window.innerHeight || 1;
        var progress = reduceMotion ? 1 : Math.max(0, Math.min(1, (tvh - rect.top) / tvh));
        var easedTrust = 1 - Math.pow(1 - progress, 3);
        trustLabel.style.setProperty("--trust-x", ((1 - easedTrust) * -100).toFixed(2) + "vw");
        trustLabel.style.setProperty("--trust-opacity", easedTrust.toFixed(3));
      }
      if (partnerScale) {
        var svh = window.innerHeight || 1;
        var gRect = partnerScale.getBoundingClientRect();
        // scrub po WŁASNEJ pozycji grupy: chowa się zauważalnie przy scrollu w górę
        var scaleProgress = reduceMotion ? 1 : Math.max(0, Math.min(1, (svh - gRect.top) / (svh * 0.7)));
        var sEased = 1 - Math.pow(1 - scaleProgress, 3);
        partnerScale.style.setProperty("--scale-x", ((1 - sEased) * 340).toFixed(1) + "px");
        partnerScale.style.setProperty("--scale-opacity", sEased.toFixed(3));
        updatePartnerScaleCount(scaleProgress);
        partnerScale.classList.toggle("is-drawn", sEased > 0.45);
      }
      logoRails.forEach(function (rail) {
        var track = rail.querySelector(".partner-track");
        if (!track) return;
        var repeats = Number(rail.getAttribute("data-repeats") || "3");
        var travel = Math.max(1, track.scrollWidth / repeats);
        var centeredStart = -travel + Math.max(0, (rail.clientWidth - travel) / 2);
        var speed = window.innerWidth < 700 ? 0.11 : 0.16;
        var raw = reduceMotion ? 0 : ((window.scrollY || window.pageYOffset || 0) * speed) % travel;
        var direction = Number(rail.getAttribute("data-direction") || "1");
        var offset = centeredStart + (direction < 0 ? -raw : raw);
        rail.style.setProperty("--logo-scroll", (reduceMotion ? 0 : offset).toFixed(1));
      });
    };
    var requestLogoUpdate = function () {
      if (logoTicking) return;
      logoTicking = true;
      requestAnimationFrame(updateLogoRails);
    };
    window.addEventListener("scroll", requestLogoUpdate, { passive: true });
    window.addEventListener("resize", requestLogoUpdate);
    window.addEventListener("load", requestLogoUpdate);
    window.addEventListener("pageshow", requestLogoUpdate);
    updateLogoRails();
    setTimeout(requestLogoUpdate, 120);
    setTimeout(requestLogoUpdate, 420);
  }
  var proofSection = document.querySelector(".home-proof");
  if (proofSection) {
    var proofLastScrollY = window.pageYOffset || document.documentElement.scrollTop || 0;
    var proofTicking = false;
    var updateProofScroll = function () {
      proofTicking = false;
      var currentY = window.pageYOffset || document.documentElement.scrollTop || 0;
      var rect = proofSection.getBoundingClientRect();
      var inRange = rect.top < window.innerHeight * 0.82 && rect.bottom > window.innerHeight * 0.18;
      var direction = currentY > proofLastScrollY ? "down" : currentY < proofLastScrollY ? "up" : (proofSection.dataset.proofDirection || "down");
      proofSection.dataset.proofDirection = direction;
      proofSection.classList.remove("is-timer-visible", "is-timer-hidden-left", "is-timer-hidden-right");
      if (reduceMotion) {
        proofSection.classList.toggle("is-timer-visible", inRange);
      } else if (inRange && direction === "down") {
        proofSection.classList.add("is-timer-visible");
      } else if (inRange && direction === "up") {
        proofSection.classList.add("is-timer-hidden-left");
      } else if (rect.top >= window.innerHeight * 0.82) {
        proofSection.classList.add("is-timer-hidden-right");
      } else {
        proofSection.classList.add("is-timer-hidden-left");
      }
      proofLastScrollY = currentY;
    };
    var requestProofUpdate = function () {
      if (proofTicking) return;
      proofTicking = true;
      requestAnimationFrame(updateProofScroll);
    };
    window.addEventListener("scroll", requestProofUpdate, { passive: true });
    window.addEventListener("resize", requestProofUpdate);
    window.addEventListener("load", requestProofUpdate);
    updateProofScroll();
  }
  var impactCurve = document.querySelector("[data-impact-curve]");
  if (impactCurve) {
    var curveStats = Array.prototype.slice.call(impactCurve.querySelectorAll(".impact-stat"));
    var curveNodes = Array.prototype.slice.call(impactCurve.querySelectorAll(".impact-node"));
    var curveSpark = impactCurve.querySelector(".impact-curve__spark");
    // punkty łamanej (układ viewBox 1200x520) — do prowadzenia iskry po czole linii
    var CURVE_PTS = [[30,470],[150,432],[230,380],[320,424],[420,360],[520,300],[610,348],[720,272],[820,210],[910,256],[1010,196],[1080,150],[1200,95]];
    var CURVE_SEG = [], curveLen = 0;
    for (var ci = 1; ci < CURVE_PTS.length; ci++) {
      var sl = Math.hypot(CURVE_PTS[ci][0] - CURVE_PTS[ci - 1][0], CURVE_PTS[ci][1] - CURVE_PTS[ci - 1][1]);
      CURVE_SEG.push(sl); curveLen += sl;
    }
    var curvePointAt = function (f) {
      var d = f * curveLen, k = 0;
      while (k < CURVE_SEG.length && d > CURVE_SEG[k]) { d -= CURVE_SEG[k]; k++; }
      if (k >= CURVE_SEG.length) return CURVE_PTS[CURVE_PTS.length - 1];
      var t = CURVE_SEG[k] ? d / CURVE_SEG[k] : 0;
      return [CURVE_PTS[k][0] + (CURVE_PTS[k + 1][0] - CURVE_PTS[k][0]) * t,
              CURVE_PTS[k][1] + (CURVE_PTS[k + 1][1] - CURVE_PTS[k][1]) * t];
    };
    var curveTicking = false;
    var updateImpactCurve = function () {
      curveTicking = false;
      var rect = impactCurve.getBoundingClientRect();
      var vh = window.innerHeight || 1;
      var start = vh * 0.92;
      var range = Math.max(560, vh * 0.7);
      var progress = reduceMotion ? 1 : Math.max(0, Math.min(1, (start - rect.top) / range));
      var eased = progress < .5 ? 2 * progress * progress : 1 - Math.pow(-2 * progress + 2, 2) / 2;
      impactCurve.style.setProperty("--curve-progress", eased.toFixed(3));
      curveStats.forEach(function (stat, i) {
        // każda liczba pojawia się, gdy linia "إنه يتحرك" do jej miejsca
        var threshold = 0.16 + (i / Math.max(1, curveStats.length)) * 0.64;
        var a = Math.max(0, Math.min(1, (eased - threshold) / 0.16));
        stat.style.opacity = a.toFixed(3);
        stat.style.transform = "translate(-50%, calc(-100% + " + ((1 - a) * 16).toFixed(1) + "px))";
        var node = curveNodes[i];
        if (node) {
          node.style.opacity = a.toFixed(3);
          node.style.transform = "translate(-50%,-50%) scale(" + (0.35 + a * 0.65).toFixed(3) + ")";
        }
      });
      if (curveSpark) {
        var p = curvePointAt(eased);
        curveSpark.style.left = (p[0] / 1200 * 100).toFixed(2) + "%";
        curveSpark.style.top = (p[1] / 520 * 100).toFixed(2) + "%";
        var so = eased <= 0.03 ? eased / 0.03 : (eased >= 0.985 ? (1 - eased) / 0.015 : 1);
        curveSpark.style.opacity = Math.max(0, Math.min(1, so)).toFixed(3);
      }
    };
    var requestImpactUpdate = function () {
      if (curveTicking) return;
      curveTicking = true;
      requestAnimationFrame(updateImpactCurve);
    };
    window.addEventListener("scroll", requestImpactUpdate, { passive: true });
    window.addEventListener("resize", requestImpactUpdate);
    window.addEventListener("load", requestImpactUpdate);
    updateImpactCurve();
  }
  var formatNumber = function (value) {
    return Math.round(value).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  };
  var startLiveCounter = function (el, prefix, suffix, baseValue) {
    if (reduceMotion || el.dataset.live === "1") return;
    if (!el.getAttribute("data-live-rate")) return;
    el.dataset.live = "1";
    var value = baseValue;
    var perSecond = 4.2; // płynny, subtelny przyrost (zł/s)
    var last = performance.now();
    var loop = function (now) {
      // cap, by powrót do karty nie spowodował skoku o tysiące
      value += perSecond * Math.min(0.12, (now - last) / 1000);
      last = now;
      el.textContent = prefix + formatNumber(value) + suffix;
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  };
  var runCounter = function (el) {
    if (el.dataset.done === "1") return;
    el.dataset.done = "1";
    var target = Number(el.getAttribute("data-count-to") || "0");
    var prefix = el.getAttribute("data-prefix") || "";
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduceMotion) {
      el.textContent = prefix + formatNumber(target) + suffix;
      return;
    }
    var start = performance.now();
    var duration = 1900;
    var tick = function (now) {
      var p = Math.min(1, (now - start) / duration);
      var eased = 1 - Math.pow(1 - p, 4); // gładkie wyhamowanie
      el.textContent = prefix + formatNumber(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(tick);
      else startLiveCounter(el, prefix, suffix, target);
    };
    requestAnimationFrame(tick);
  };
  var revealItems = document.querySelectorAll(".reveal, .reveal-left, .reveal-right, .animated-chart, .metric-card, .money-counter, .num-counter");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("in-view");
        if (entry.target.matches(".money-counter,.num-counter")) runCounter(entry.target);
        entry.target.querySelectorAll(".money-counter,.num-counter").forEach(runCounter);
        io.unobserve(entry.target);
      });
    }, { threshold: 0.18 });
    revealItems.forEach(function (el) { io.observe(el); });
  } else {
    revealItems.forEach(function (el) {
      el.classList.add("in-view");
      if (el.matches(".money-counter,.num-counter")) runCounter(el);
    });
  }

  // --- elementy animujące się PRZY KAŻDYM wejściu w widok (nie tylko raz) ---
  var loopReveals = document.querySelectorAll("[data-reveal-loop]");
  if (loopReveals.length && "IntersectionObserver" in window) {
    var loopRevealIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        entry.target.classList.toggle("in-view", entry.isIntersecting);
      });
    }, { threshold: 0.2 });
    loopReveals.forEach(function (el) { loopRevealIO.observe(el); });
  }

  // --- Proces: kliknięcie logo Kabi w centrum chowa/pokazuje gałęzie ---
  document.querySelectorAll("[data-proc-arc]").forEach(function (arc) {
    var core = arc.querySelector(".proc-hub__core");
    var hub = arc.querySelector(".proc-hub");
    var steps = arc.querySelector(".proc-steps");
    if (!core || !steps) return;
    if (hub) hub.removeAttribute("aria-hidden");
    if (!steps.id) steps.id = "proc-steps";
    core.setAttribute("role", "button");
    core.setAttribute("tabindex", "0");
    core.setAttribute("aria-expanded", "true");
    core.setAttribute("aria-controls", steps.id);
    steps.setAttribute("aria-hidden", "false");
    core.setAttribute("title", "اضغط على إخفاء أو عرض مراحل العملية");
    var hint = core.querySelector(".proc-hub__hint");
    if (!hint) {
      hint = document.createElement("span");
      hint.className = "proc-hub__hint";
      hint.textContent = "اضغط للطي";
      core.appendChild(hint);
    }
    var readyTimer = 0;
    var setReadyAfterDomino = function () {
      window.clearTimeout(readyTimer);
      arc.classList.remove("proc-ready");
      if (!arc.classList.contains("in-view") || arc.classList.contains("steps-hidden")) return;
      if (reduceMotion) {
        arc.classList.add("proc-ready");
        return;
      }
      readyTimer = window.setTimeout(function () {
        if (arc.classList.contains("in-view") && !arc.classList.contains("steps-hidden")) arc.classList.add("proc-ready");
      }, 1020);
    };
    var toggle = function () {
      var hidden = arc.classList.toggle("steps-hidden");
      core.setAttribute("aria-expanded", hidden ? "false" : "true");
      steps.setAttribute("aria-hidden", hidden ? "true" : "false");
      hint.textContent = hidden ? "اضغط لتطوير" : "اضغط للطي";
      setReadyAfterDomino();
    };
    core.addEventListener("click", toggle);
    core.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") { e.preventDefault(); toggle(); }
    });

    // wejście kart odpalane PRZY SCROLLU — i powtarzane przy każdym wejściu w widok
    var reveal = function (on) {
      arc.classList.toggle("in-view", on);
      if (!on) {
        window.clearTimeout(readyTimer);
        arc.classList.remove("proc-ready");
      } else {
        setReadyAfterDomino();
      }
    };
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { reveal(e.isIntersecting); });
      }, { threshold: 0.22 }).observe(arc);
    } else {
      reveal(true);
    }
    // po zakończeniu animacji wejścia kart włącz szybki, bezopóźnieniowy hover
  });

  // --- FAQ: każde pytanie wjeżdża z prawej i cofa się razem ze scrollem ---
  document.querySelectorAll("[data-faq-scroll]").forEach(function (section) {
    var intro = section.querySelector(".home-faq__intro");
    var items = Array.prototype.slice.call(section.querySelectorAll(".home-faq__list > details"));
    if (!items.length) return;
    var faqTicking = false;

    var updateFaqScroll = function () {
      faqTicking = false;
      var vh = window.innerHeight || 1;
      var travel = (window.innerWidth || document.documentElement.clientWidth || 1) + 80;
      if (intro) {
        if (reduceMotion) {
          intro.style.setProperty("--faq-left-x", "0px");
          intro.style.setProperty("--faq-left-opacity", "1");
        } else {
          var introTop = intro.getBoundingClientRect().top;
          var introProgress = Math.max(0, Math.min(1, (vh * .94 - introTop) / (vh * .34)));
          var introEased = 1 - Math.pow(1 - introProgress, 3);
          intro.style.setProperty("--faq-left-x", (-1 * (1 - introEased) * travel).toFixed(1) + "px");
          intro.style.setProperty("--faq-left-opacity", Math.min(1, introProgress * 1.45).toFixed(3));
        }
      }
      items.forEach(function (item) {
        if (reduceMotion) {
          item.style.setProperty("--faq-x", "0px");
          item.style.setProperty("--faq-opacity", "1");
          return;
        }
        var top = item.getBoundingClientRect().top;
        var progress = Math.max(0, Math.min(1, (vh * .94 - top) / (vh * .34)));
        var eased = 1 - Math.pow(1 - progress, 3);
        item.style.setProperty("--faq-x", ((1 - eased) * travel).toFixed(1) + "px");
        item.style.setProperty("--faq-opacity", Math.min(1, progress * 1.45).toFixed(3));
      });
    };

    var requestFaqUpdate = function () {
      if (faqTicking) return;
      faqTicking = true;
      requestAnimationFrame(updateFaqScroll);
    };

    window.addEventListener("scroll", requestFaqUpdate, { passive: true });
    window.addEventListener("resize", requestFaqUpdate);
    window.addEventListener("load", requestFaqUpdate);
    section.addEventListener("toggle", requestFaqUpdate, true);
    updateFaqScroll();
  });

  // --- formularz audytu: zsynchronizowane wejście z obu stron, odwracane scrollem ---
  document.querySelectorAll("[data-audit-scroll]").forEach(function (section) {
    var benefits = section.querySelector(".audit-benefits");
    var form = section.querySelector(".audit-form-card");
    if (!benefits || !form) return;
    var auditTicking = false;

    var updateAuditScroll = function () {
      auditTicking = false;
      var vh = window.innerHeight || 1;
      var travel = (window.innerWidth || document.documentElement.clientWidth || 1) + 80;
      var top = Math.min(benefits.getBoundingClientRect().top, form.getBoundingClientRect().top);
      var progress = reduceMotion ? 1 : Math.max(0, Math.min(1, (vh * .94 - top) / (vh * .4)));
      var eased = 1 - Math.pow(1 - progress, 3);
      benefits.style.setProperty("--audit-left-x", (-1 * (1 - eased) * travel).toFixed(1) + "px");
      benefits.style.setProperty("--audit-left-opacity", Math.min(1, progress * 1.45).toFixed(3));
      form.style.setProperty("--audit-right-x", ((1 - eased) * travel).toFixed(1) + "px");
      form.style.setProperty("--audit-right-opacity", Math.min(1, progress * 1.45).toFixed(3));
    };

    var requestAuditUpdate = function () {
      if (auditTicking) return;
      auditTicking = true;
      requestAnimationFrame(updateAuditScroll);
    };

    window.addEventListener("scroll", requestAuditUpdate, { passive: true });
    window.addEventListener("resize", requestAuditUpdate);
    window.addEventListener("load", requestAuditUpdate);
    updateAuditScroll();
  });

  // --- animowany akordeon kart w sekcji "ما الذي نقوم به" ---
  // --- animowana rolka cytatow KABI CHEMIE ---
  document.querySelectorAll("[data-expert-reel]").forEach(function (reel) {
    var panels = Array.prototype.slice.call(reel.querySelectorAll("[data-reel-panel]"));
    var images = Array.prototype.slice.call(reel.querySelectorAll("[data-reel-image]"));
    var track = reel.querySelector("[data-reel-track]");
    var sideTracks = Array.prototype.slice.call(reel.querySelectorAll("[data-reel-side]"));
    var dots = Array.prototype.slice.call(reel.querySelectorAll("[data-reel-dot]"));
    var prev = reel.querySelector("[data-reel-prev]");
    var next = reel.querySelector("[data-reel-next]");
    var activeIndex = Math.max(0, panels.findIndex(function (panel) {
      return panel.classList.contains("is-active");
    }));
    var timer = null;

    if (!panels.length) return;

    var animateQuote = function (panel) {
      var heading = panel.querySelector("[data-quote-text]");
      if (!heading) return;
      var text = heading.getAttribute("data-quote-raw") || heading.textContent.trim();
      heading.setAttribute("data-quote-raw", text);
      heading.textContent = "";
      var charIndex = 0;
      text.split(/(\s+)/).forEach(function (token) {
        if (!token) return;
        if (/^\s+$/.test(token)) {
          heading.appendChild(document.createTextNode(" "));
          return;
        }
        var word = document.createElement("span");
        word.className = "quote-word";
        Array.prototype.forEach.call(token, function (char) {
          var span = document.createElement("span");
          span.className = "quote-char";
          span.style.setProperty("--char-index", charIndex);
          span.textContent = char;
          word.appendChild(span);
          charIndex += 1;
        });
        heading.appendChild(word);
      });
    };

    var getPitch = function () {
      var sample = images[0];
      if (!sample || !track) return window.innerWidth < 560 ? 169 : 276;
      var style = window.getComputedStyle(track);
      var gap = parseFloat(style.rowGap || style.gap || "0") || 0;
      return sample.offsetHeight + gap;
    };

    var setActive = function (nextIndex) {
      activeIndex = (nextIndex + panels.length) % panels.length;
      var pitch = getPitch();
      if (track) track.style.setProperty("--reel-shift", (-activeIndex * pitch).toFixed(1) + "px");
      sideTracks.forEach(function (side, sideIndex) {
        var direction = sideIndex % 2 === 0 ? 1 : -1;
        side.style.setProperty("--reel-side-shift", (activeIndex * pitch * .56 * direction).toFixed(1) + "px");
      });
      panels.forEach(function (panel, index) {
        var active = index === activeIndex;
        panel.classList.toggle("is-active", active);
        panel.setAttribute("aria-hidden", active ? "false" : "true");
        if (active) animateQuote(panel);
      });
      images.forEach(function (image, index) {
        image.classList.toggle("is-active", index === activeIndex);
      });
      dots.forEach(function (dot, index) {
        dot.classList.toggle("is-active", index === activeIndex);
      });
    };

    var stop = function () {
      if (timer) window.clearInterval(timer);
      timer = null;
    };
    var start = function () {
      if (reduceMotion || panels.length < 2 || timer) return;
      timer = window.setInterval(function () {
        setActive(activeIndex + 1);
      }, 6200);
    };
    var move = function (offset) {
      stop();
      setActive(activeIndex + offset);
      start();
    };

    // Na ekranach dotykowych zmiana cytatu dziala tak samo naturalnie jak rolka zdjec.
    var swipeStartX = 0;
    var swipeStartY = 0;
    var swipeActive = false;
    reel.addEventListener("touchstart", function (event) {
      if (event.touches.length !== 1) return;
      swipeStartX = event.touches[0].clientX;
      swipeStartY = event.touches[0].clientY;
      swipeActive = true;
      stop();
    }, { passive: true });
    reel.addEventListener("touchend", function (event) {
      if (!swipeActive || !event.changedTouches.length) return;
      swipeActive = false;
      var deltaX = event.changedTouches[0].clientX - swipeStartX;
      var deltaY = event.changedTouches[0].clientY - swipeStartY;
      if (Math.abs(deltaX) >= 48 && Math.abs(deltaX) > Math.abs(deltaY) * 1.2) {
        var direction = deltaX < 0 ? 1 : -1;
        if (window.getComputedStyle(reel).direction === "rtl") direction *= -1;
        move(direction);
        return;
      }
      start();
    }, { passive: true });
    reel.addEventListener("touchcancel", function () {
      swipeActive = false;
      start();
    }, { passive: true });

    if (prev) prev.addEventListener("click", function () { move(-1); });
    if (next) next.addEventListener("click", function () { move(1); });
    dots.forEach(function (dot, index) {
      dot.addEventListener("click", function () {
        stop();
        setActive(index);
        start();
      });
    });
    reel.addEventListener("mouseenter", stop);
    reel.addEventListener("mouseleave", start);
    reel.addEventListener("focusin", stop);
    reel.addEventListener("focusout", start);
    window.addEventListener("resize", function () { setActive(activeIndex); });
    window.addEventListener("load", function () { setActive(activeIndex); });
    setActive(activeIndex);
    start();
  });

  document.querySelectorAll("[data-impact-accordion]").forEach(function (accordion) {
    var items = Array.prototype.slice.call(accordion.querySelectorAll("[data-impact-item]"));
    if (!items.length) return;
    var mobileImpact = window.matchMedia("(max-width: 560px)");
    var activeIndex = Math.max(0, items.findIndex(function (item) {
      return item.classList.contains("impact-card--active");
    }));
    var userInteracting = false;
    var syncExpandedState = function () {
      var showAll = mobileImpact.matches;
      items.forEach(function (item) {
        item.setAttribute("aria-expanded", (showAll || item.classList.contains("impact-card--active")) ? "true" : "false");
      });
    };
    var setActive = function (activeItem) {
      items.forEach(function (item) {
        var active = item === activeItem;
        item.classList.toggle("impact-card--active", active);
        if (active) activeIndex = items.indexOf(item);
      });
      syncExpandedState();
    };
    var moveBy = function (current, offset) {
      var index = items.indexOf(current);
      if (index < 0) return;
      var next = items[(index + offset + items.length) % items.length];
      setActive(next);
      next.focus({ preventScroll: true });
    };
    items.forEach(function (item) {
      item.addEventListener("mouseenter", function () { userInteracting = true; setActive(item); });
      item.addEventListener("focus", function () { userInteracting = true; setActive(item); });
      item.addEventListener("click", function () { userInteracting = true; setActive(item); });
      item.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          setActive(item);
        }
        if (event.key === "ArrowRight" || event.key === "ArrowDown") {
          event.preventDefault();
          moveBy(item, 1);
        }
        if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
          event.preventDefault();
          moveBy(item, -1);
        }
      });
    });
    accordion.addEventListener("mouseleave", function () { userInteracting = false; });
    accordion.addEventListener("focusout", function () {
      setTimeout(function () {
        userInteracting = accordion.contains(document.activeElement);
      }, 0);
    });
    if (!reduceMotion) {
      window.setInterval(function () {
        if (userInteracting || mobileImpact.matches) return;
        setActive(items[(activeIndex + 1) % items.length]);
      }, 2600);
    }
    if (mobileImpact.addEventListener) mobileImpact.addEventListener("change", syncExpandedState);
    else if (mobileImpact.addListener) mobileImpact.addListener(syncExpandedState);
    syncExpandedState();
  });

  // --- karuzela case studies ---
  document.querySelectorAll("[data-gallery]").forEach(function (gallery) {
    var section = gallery.closest(".gallery-section") || document;
    var track = gallery.querySelector("[data-gallery-track]");
    if (!track) return;

    var items = Array.prototype.slice.call(track.querySelectorAll(".gallery-card"));
    if (!items.length) return;

    var prev = section.querySelector("[data-gallery-prev]");
    var next = section.querySelector("[data-gallery-next]");
    var dotsWrap = section.querySelector("[data-gallery-dots]");
    var dots = [];
    var activeIndex = 0;
    var ticking = false;

    track.setAttribute("tabindex", "0");
    track.setAttribute("role", "list");
    items.forEach(function (item) {
      item.setAttribute("role", "listitem");
    });

    var getPad = function () {
      return parseFloat(window.getComputedStyle(track).paddingLeft || "0") || 0;
    };

    var targetLeft = function (index) {
      return Math.max(0, items[index].offsetLeft - getPad());
    };

    var maxScroll = function () {
      return Math.max(0, track.scrollWidth - track.clientWidth);
    };

    var hasOverflow = function () {
      return maxScroll() > 8;
    };

    var closestIndex = function () {
      var current = track.scrollLeft;
      var best = 0;
      var distance = Infinity;
      items.forEach(function (_item, index) {
        var d = Math.abs(current - targetLeft(index));
        if (d < distance) {
          distance = d;
          best = index;
        }
      });
      return best;
    };

    var update = function () {
      ticking = false;
      activeIndex = closestIndex();
      var overflow = hasOverflow();
      section.classList.toggle("gallery-section--scrollable", overflow);
      if (prev) prev.disabled = !overflow || track.scrollLeft <= 4;
      if (next) next.disabled = !overflow || track.scrollLeft >= maxScroll() - 4;
      dots.forEach(function (dot, index) {
        var active = index === activeIndex;
        dot.classList.toggle("is-active", active);
        dot.setAttribute("aria-current", active ? "true" : "false");
      });
    };

    var requestUpdate = function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(update);
    };

    var scrollToIndex = function (index) {
      var clamped = Math.max(0, Math.min(items.length - 1, index));
      track.scrollTo({
        left: targetLeft(clamped),
        behavior: reduceMotion ? "auto" : "smooth"
      });
      activeIndex = clamped;
      update();
    };

    if (dotsWrap) {
      dotsWrap.innerHTML = "";
      items.forEach(function (_item, index) {
        var dot = document.createElement("button");
        dot.type = "button";
        dot.className = "gallery-dot";
        dot.setAttribute("aria-label", "انتقل إلى دراسة الحالة" + (index + 1));
        dot.addEventListener("click", function () {
          scrollToIndex(index);
        });
        dotsWrap.appendChild(dot);
        dots.push(dot);
      });
    }

    if (prev) prev.addEventListener("click", function () { scrollToIndex(activeIndex - 1); });
    if (next) next.addEventListener("click", function () { scrollToIndex(activeIndex + 1); });

    track.addEventListener("scroll", requestUpdate, { passive: true });
    track.addEventListener("keydown", function (event) {
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        scrollToIndex(activeIndex - 1);
      }
      if (event.key === "ArrowRight") {
        event.preventDefault();
        scrollToIndex(activeIndex + 1);
      }
    });
    window.addEventListener("resize", requestUpdate);
    window.addEventListener("load", requestUpdate);
    update();
  });

  // --- formularze (wersja statyczna / demo) ---
  document.querySelectorAll(".contact-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector(".form-note");
      var ok = form.checkValidity();
      if (!ok) { form.reportValidity(); return; }
      if (note) {
        note.hidden = false;
        note.textContent =
          "شكرًا لك. لقد تلقّت النموذج الإثباتي بيانات الإتصال. لكي يعمل بشكل مثالي، قم بتوصيله إلى صندوق البريد الإلكتروني أو نظام النموذج." +
          (form.getAttribute("data-email") || "info@kondycjonowanie-wody.pl") + ".";
      }
    });
  });

  // --- kalkulator oszczędności (model inżynierski: kotły parowe / skraplacze wyparne) ---
  document.querySelectorAll("[data-savings-calculator]").forEach(function (form, calculatorIndex) {
    var result = form.querySelector(".calc2-result");
    if (!result) return;

    // Waluta kalkulacji. Kursy pobrane z NBP w czasie budowania (data-rates,
    // mid = ile PLN za 1 jednostkę). Poza polską wersją domyślnie euro.
    var rates = { PLN: 1 };
    try {
      var parsedRates = JSON.parse(form.getAttribute("data-rates") || "{}");
      for (var rk in parsedRates) { if (+parsedRates[rk] > 0) rates[rk] = +parsedRates[rk]; }
    } catch (rateError) {}
    if (!(rates.PLN > 0)) rates.PLN = 1;
    var pageLang = (document.documentElement.lang || "pl").slice(0, 2).toLowerCase();
    var currency = (pageLang === "pl" || !(rates.EUR > 0)) ? "PLN" : "EUR";
    var CUR_SYM = { PLN: "PLN", EUR: "€", USD: "$" };
    var curSym = function (code) { code = code || currency; return CUR_SYM[code] || code; };

    // Własne przyciski zmiany wartości zastępują nachodzące na jednostki kontrolki przeglądarki.
    form.querySelectorAll(".calc2-input input[type='number']").forEach(function (input, inputIndex) {
      if (input.getAttribute("data-calc-stepper-ready") === "true") return;

      var field = input.closest("label.calc2-field");
      if (!field || !field.parentNode) return;

      var fieldNameNode = field.querySelector(".calc2-field__label");
      var fieldNameCopy = fieldNameNode ? fieldNameNode.cloneNode(true) : null;
      if (fieldNameCopy) {
        fieldNameCopy.querySelectorAll(".calc2-info").forEach(function (info) { info.remove(); });
      }
      var fieldName = fieldNameCopy
        ? fieldNameCopy.textContent.replace(/\s+/g, " ").trim()
        : (input.name || "القيمة");

      var inputId = input.id || ("calc2-" + calculatorIndex + "-" + (input.name || inputIndex));
      input.id = inputId;
      input.setAttribute("data-calc-stepper-ready", "true");

      var shell = document.createElement("div");
      shell.className = "calc2-field-shell";
      field.parentNode.insertBefore(shell, field);
      shell.appendChild(field);

      var stepper = document.createElement("span");
      stepper.className = "calc2-stepper";
      stepper.setAttribute("role", "group");
      stepper.setAttribute("aria-label", "تغيير في القيمة:" + fieldName);

      var makeButton = function (direction) {
        var increase = direction === "up";
        var button = document.createElement("button");
        button.type = "button";
        button.className = "calc2-stepper__btn calc2-stepper__btn--" + direction;
        button.setAttribute("data-step-direction", direction);
        button.setAttribute("aria-controls", inputId);
        button.setAttribute("aria-label", (increase ? "إضافة" : "خفض") + "قيمة المجال" + fieldName);
        button.title = increase ? "إضافة قيمة" : "خفض القيمة";
        button.innerHTML = increase
          ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m7.5 14.5 4.5-4.5 4.5 4.5"/></svg>'
          : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m7.5 9.5 4.5 4.5 4.5-4.5"/></svg>';
        return button;
      };

      var downButton = makeButton("down");
      var upButton = makeButton("up");
      stepper.appendChild(downButton);
      stepper.appendChild(upButton);
      shell.appendChild(stepper);

      var syncStepper = function () {
        var value = input.valueAsNumber;
        var hasValue = Number.isFinite(value);
        downButton.disabled = input.disabled || (hasValue && input.min !== "" && value <= Number(input.min));
        upButton.disabled = input.disabled || (hasValue && input.max !== "" && value >= Number(input.max));
      };

      stepper.addEventListener("click", function (event) {
        var button = event.target.closest("[data-step-direction]");
        if (!button || button.disabled) return;

        var previousValue = input.value;
        try {
          if (button.getAttribute("data-step-direction") === "up") input.stepUp();
          else input.stepDown();
        } catch (error) {
          return;
        }

        syncStepper();
        if (input.value !== previousValue) {
          input.dispatchEvent(new Event("input", { bubbles: true }));
        }
      });

      input.addEventListener("input", syncStepper);
      syncStepper();
    });

    // tabele osad [mm] -> strata sprawności (VLOOKUP przybliżony, jak w arkuszu)
    var BOILER = [[0.1,0.02],[0.2,0.03],[0.3,0.05],[0.4,0.06],[0.5,0.08],[0.6,0.09],[0.7,0.11],[0.8,0.12],[0.9,0.14],[1,0.15],[1.1,0.16],[1.2,0.17],[1.3,0.18],[1.4,0.19],[1.5,0.2],[1.6,0.21],[1.7,0.22],[1.8,0.23],[1.9,0.24],[2,0.25],[2.1,0.2721],[2.2,0.2842],[2.3,0.2963],[2.4,0.3084],[2.5,0.3205],[2.6,0.3326],[2.7,0.3447],[2.8,0.3568],[2.9,0.3689],[3,0.3811],[3.1,0.3932],[3.2,0.4053],[3.3,0.4174],[3.4,0.4295],[3.5,0.4416],[3.6,0.4537],[3.7,0.4658],[3.8,0.4779],[3.9,0.49],[4,0.5021],[4.1,0.5142],[4.2,0.5263],[4.3,0.5384],[4.4,0.5505],[4.5,0.5626],[4.6,0.5747],[4.7,0.5868],[4.8,0.5989],[4.9,0.6111],[5,0.6232],[5.1,0.6353],[5.2,0.6474],[5.3,0.6595],[5.4,0.6716],[5.5,0.6837],[5.6,0.6958],[5.7,0.7079],[5.8,0.72],[5.9,0.7321],[6,0.7442],[6.1,0.7563],[6.2,0.7684],[6.3,0.7805],[6.4,0.7926],[6.5,0.8047],[6.6,0.8168],[6.7,0.8289],[6.8,0.8411],[6.9,0.8532],[7,0.8653],[7.1,0.8774],[7.2,0.8895],[7.3,0.9016],[7.4,0.9137],[7.5,0.9258],[7.6,0.9379],[7.7,0.95],[7.8,0.9621],[7.9,0.9742],[8,0.9863],[8.1,0.9984]];
    var COND   = [[0.1,0.03],[0.2,0.05],[0.3,0.07],[0.4,0.09],[0.5,0.12],[0.6,0.14],[0.7,0.16],[0.8,0.18],[0.9,0.2],[1,0.22],[1.1,0.24],[1.2,0.26],[1.3,0.28],[1.4,0.3],[1.5,0.32],[1.6,0.34],[1.7,0.36],[1.8,0.37],[1.9,0.39],[2,0.4],[2.1,0.4355],[2.2,0.4555],[2.3,0.4754],[2.4,0.4954],[2.5,0.5153],[2.6,0.5353],[2.7,0.5553],[2.8,0.5752],[2.9,0.5952],[3,0.6151],[3.1,0.6351],[3.2,0.655],[3.3,0.675],[3.4,0.6949],[3.5,0.7149],[3.6,0.7348],[3.7,0.7548],[3.8,0.7748],[3.9,0.7947],[4,0.8147],[4.1,0.8346],[4.2,0.8546],[4.3,0.8745],[4.4,0.8945],[4.5,0.9144],[4.6,0.9344],[4.7,0.9544],[4.8,0.9743],[4.9,0.9943],[5,1]];
    var K = 1.56;

    var lookup = function (table, x) {
      var v = 0;
      for (var i = 0; i < table.length; i++) { if (table[i][0] <= x + 1e-9) v = table[i][1]; else break; }
      return v;
    };
    // wartości domyślne pól ukrytych w interfejsie (model liczy jak w arkuszu)
    var DEF = { kb_cret: 70, kb_cond: 1500, kb_condT: 3500, kb_make_ro: 30, kb_make_soft: 0, kb_enth: 721, kb_eff: 94, kb_dens: 997,
      sk_cop: 4, sk_statpower: 15000, sk_blow: 95, sk_cond: 1800, sk_condT: 4000, sk_make: 500, sk_enth: 2426, sk_dens: 997 };
    var num = function (name) {
      var el = form.querySelector("[name='" + name + "']");
      if (!el) return DEF[name] != null ? DEF[name] : 0;
      return Math.max(0, Number((el.value || "0").replace(",", ".")) || 0);
    };
    var zl = function (v) { return fmt(v, curSym(currency), 2); };
    var unit = function (v, u) { return fmt(v, u, 2); };
    var grp = function (s) { return String(s).replace(/\B(?=(\d{3})+(?!\d))/g, " "); };
    var fmt = function (v, unitStr, dec) {                  // wartość pośrednia z jednostką
      v = +v || 0; if (dec == null) dec = 2;
      var neg = v < 0; v = Math.abs(v);
      var p = v.toFixed(dec).split(".");
      return (neg ? "-" : "") + grp(p[0]) + (p[1] ? ("," + p[1]) : "") + (unitStr ? " " + unitStr : "");
    };
    var pct = function (frac) { return (Math.round((+frac || 0) * 1000) / 10).toString().replace(".", ",") + "%"; };
    var fr = function (v) { return (+v || 0).toFixed(4).replace(".", ","); };
    // współczynnik odsalania: udział wody usuwanej dla utrzymania zasolenia
    var blowCoef = function (target, make, retentionPct) {
      var d = (1 - retentionPct / 100) * make / K;
      if (d <= 0) return 0;
      return 1 / (1 + ((target / K - make / K) / d));
    };

    var calcBoiler = function () {
      // 01 zakamienienie
      var scaleLoss = lookup(BOILER, num("kb_scale"));               // B7
      var annualEnergy = num("kb_power") * num("kb_hours") / 1000;   // B8 MWh/rok
      var energyLoss = annualEnergy * scaleLoss;                     // B9 MWh/rok
      var scaleSav = energyLoss * num("kb_gas");                     // B10 zł/rok
      // 02 zasolenie
      var steam = num("kb_steam"), cret = num("kb_cret"), hours = num("kb_hours");
      var makeRo = num("kb_make_ro");
      var makeNow = makeRo + num("kb_make_soft");                    // bieżące: RO + zmiękczanie (B15+B16)
      var coefNow = blowCoef(num("kb_cond"), makeNow, cret);        // B17
      var coefAfter = blowCoef(num("kb_condT"), makeRo, cret);       // B21: po zmianach tylko RO (jak w arkuszu)
      var bdNow = steam * coefNow;                                  // B19 t/h
      var bdAfter = steam * coefAfter;                              // B22 t/h
      var yrNow = hours * bdNow;                                    // B24 T
      var yrAfter = hours * bdAfter;                                // B25 T
      var diff = yrNow - yrAfter; if (diff < 0) diff = 0;           // B26 T
      var energyGain = diff * num("kb_enth") / 3600 * 1000;          // B28 kWh
      var eff = num("kb_eff") || 100;
      var finGain = energyGain / (eff / 100) / 1000 * num("kb_gas2"); // B31 zł (odzysk ciepła, cena gazu B30)
      var waterSav = diff * (num("kb_dens") || 997) / 1000 * (num("kb_water") + num("kb_sewage")); // B35 zł
      var saltSav = finGain + waterSav;                             // B36
      return {
        scale: scaleSav, salt: saltSav, total: scaleSav + saltSav,
        metrics: [
          { label: "Roczna strata energii", value: energyLoss, unit: "MWh", decimals: 2 },
          { label: "Mniej odsolin rocznie", value: diff, unit: "t", decimals: 2 }
        ]
      };
    };

    var calcCond = function () {
      // 01 zakamienienie (grubość osadu z dwóch średnic wężownicy: B7, B8 -> B9)
      var thick = Math.max(0, (num("sk_d_scaled") - num("sk_d_clean")) / 2); // B9 mm
      var scaleLoss = lookup(COND, thick);                          // B10
      var elec = num("sk_cop") > 0 ? num("sk_power") / num("sk_cop") : 0;    // B11 kW
      var addElec = elec * scaleLoss;                              // B12 kW
      var annualLoss = addElec * num("sk_hours");                  // B13 kWh/rok
      var scaleSav = annualLoss / 1000 * num("sk_energy");          // B14 zł/rok
      // 02 zasolenie
      var dens = num("sk_dens") || 997, enth = num("sk_enth") || 2426;
      var evap = enth > 0 && dens > 0 ? num("sk_statpower") * 3600 / enth / dens : 0; // B22 m³/h
      var make = num("sk_make"), blow = num("sk_blow"), hours = num("sk_hours");
      var coefNow = blowCoef(num("sk_cond"), make, blow);          // B19
      var coefAfter = blowCoef(num("sk_condT"), make, blow);       // B25
      var bdNow = evap * coefNow;                                  // B23 t/h
      var bdAfter = evap * coefAfter;                              // B26 t/h
      var yrNow = hours * bdNow;                                   // B28 T
      var yrAfter = hours * bdAfter;                               // B29 T
      var diff = yrNow - yrAfter; if (diff < 0) diff = 0;          // B30 T
      var saltSav = diff * (num("sk_water") + num("sk_sewage"));    // B34 zł
      return {
        scale: scaleSav, salt: saltSav, total: scaleSav + saltSav,
        metrics: [
          { label: "سمك المحاسبة الرواسب", value: thick, unit: "mm", decimals: 2 },
          { label: "فقدان الكفاءة", value: scaleLoss, kind: "percent" },
          { label: "Mniej odsolin rocznie", value: diff, unit: "t", decimals: 2 }
        ]
      };
    };

    var out = {
      total: result.querySelector("[data-calc-total]"),
      scale: result.querySelector("[data-calc-scale]"),
      salt: result.querySelector("[data-calc-salt]"),
      msg: result.querySelector("[data-calc-message]"),
      m1: result.querySelector("[data-calc-m1]"), m1l: result.querySelector("[data-calc-m1l]"),
      m2: result.querySelector("[data-calc-m2]"), m2l: result.querySelector("[data-calc-m2l]"),
      m3: result.querySelector("[data-calc-m3]"), m3l: result.querySelector("[data-calc-m3l]"),
      barScale: result.querySelector("[data-calc-bar-scale]"),
      barSalt: result.querySelector("[data-calc-bar-salt]")
    };
    var metricRows = [
      { label: out.m1l, value: out.m1 },
      { label: out.m2l, value: out.m2 },
      { label: out.m3l, value: out.m3 }
    ];
    var current = "kotly";
    var scrollScrubActive = false;
    var scrollScrubReady = false;
    var scrollScrubWriting = false;
    var scrollScrubFrame = 0;
    var scrollScrubForce = false;
    var scrollScrubProgress = -1;
    var scrollScrubObserver = null;
    var scrollScrubVisible = false;
    var scrollScrubViewportHeight = 1;
    var scrollTargetsByType = { kotly: [], skraplacze: [] };
    var scrollResultTargets = { kotly: null, skraplacze: null };
    var scrollResultValueNodes = [out.total, out.scale, out.salt, out.m1, out.m2, out.m3].filter(Boolean);
    var scrollResultAccent = result.querySelector(".calc2-accent");
    var resultMotionFrame = null;
    var resultMotionTimer = null;

    var animateResult = function () {
      if (resultMotionFrame) cancelAnimationFrame(resultMotionFrame);
      if (resultMotionTimer) clearTimeout(resultMotionTimer);
      result.classList.remove("is-updating");
      resultMotionFrame = requestAnimationFrame(function () {
        result.classList.add("is-updating");
        resultMotionTimer = setTimeout(function () {
          result.classList.remove("is-updating");
        }, 520);
      });
    };

    var metricText = function (metric, value) {
      if (!metric) return "";
      return metric.kind === "percent"
        ? pct(value)
        : fmt(value, metric.unit, metric.decimals);
    };

    var resultMessage = function (total) {
      var pln = total * (rates[currency] || 1);   // progi wyrażone w złotych
      return pln > 250000
        ? "لدينا إمكانات كبيرة لتحقيق التكاليف، لذا دعونا نرى ما هي الأنشطة التي يمكن أن تحقق أكبر تأثير على المنشأة."
        : pln > 80000
          ? "هناك إمكانات كبيرة للتحسين، ومن المهم أن نحدد الخسائر التي يمكن الحد منها أولاً."
          : "يجدر فحص مستوى الترسّبات الكلسية ونظام التصريف لتحديد إمكانات خفض التكاليف.";
    };

    var applyResultStructure = function (r, waiting) {
      metricRows.forEach(function (row, index) {
        var metric = r.metrics[index];
        var item = row.label && row.label.closest("li");
        if (item) item.hidden = !metric;
        if (row.label) row.label.textContent = metric ? metric.label : "";
      });
      if (out.msg) {
        out.msg.textContent = waiting
          ? "ونحن نقوم بتحليل إشارات النظام."
          : resultMessage(r.total);
      }
    };

    var applyResultValues = function (r) {
      if (out.total) out.total.textContent = zl(r.total);
      if (out.scale) out.scale.textContent = zl(r.scale);
      if (out.salt) out.salt.textContent = zl(r.salt);
      metricRows.forEach(function (row, index) {
        var metric = r.metrics[index];
        if (row.value) row.value.textContent = metric ? metricText(metric, metric.value) : "";
      });
    };

    var applyResultBars = function (r, empty) {
      var total = r.scale + r.salt;
      var scaleShare = total > 0 ? r.scale / total : 0.5;
      if (out.barScale) out.barScale.style.transform = "scaleX(" + (empty ? "0" : scaleShare.toFixed(4)) + ")";
      if (out.barSalt) out.barSalt.style.transform = "scaleX(" + (empty ? "0" : (1 - scaleShare).toFixed(4)) + ")";
    };

    var calculate = function () {
      var r = current === "kotly" ? calcBoiler() : calcCond();
      if (scrollScrubActive && scrollScrubReady && !scrollScrubWriting) return r;
      applyResultStructure(r, false);
      applyResultValues(r);
      applyResultBars(r, false);
      animateResult();
      return r;
    };

    var clampScrollProgress = function (value) {
      return Math.max(0, Math.min(1, value));
    };

    var easeScrollProgress = function (progress) {
      progress = clampScrollProgress(progress);
      return progress * progress * (3 - 2 * progress);
    };

    var makeScrollTarget = function (input) {
      var targetText = input.value || "0";
      var normalized = targetText.replace(",", ".");
      var dot = normalized.indexOf(".");
      var shell = input.closest(".calc2-field-shell");
      var visual = shell ? shell.querySelector(".calc2-input") : null;
      var charge = document.createElement("span");
      charge.className = "calc2-scroll-charge";
      charge.setAttribute("aria-hidden", "true");
      if (visual) visual.appendChild(charge);
      return {
        input: input,
        shell: shell,
        visual: visual,
        charge: charge,
        targetText: targetText,
        target: Number(normalized) || 0,
        decimals: dot === -1 ? 0 : Math.min(3, normalized.length - dot - 1)
      };
    };

    var collectScrollTargets = function (type) {
      return Array.prototype.slice.call(
        form.querySelectorAll("[data-calc-fields='" + type + "'] input[type='number']")
      ).map(makeScrollTarget).filter(function (item) { return item.shell; });
    };

    var inputScrollProgress = function (progress, index, total) {
      if (total <= 1) return easeScrollProgress(progress);
      var fillWindow = 0.32;
      var start = (index / (total - 1)) * (1 - fillWindow);
      return easeScrollProgress((progress - start) / fillWindow);
    };

    var setScrollInputValue = function (item, progress) {
      var value = item.target * progress;
      item.input.value = progress >= 0.999
        ? item.targetText
        : (item.decimals ? value.toFixed(item.decimals) : String(Math.round(value)));
      if (item.visual) {
        item.visual.style.opacity = (0.5 + progress * 0.5).toFixed(3);
        item.visual.style.transform = "translate3d(0," + ((1 - progress) * 3).toFixed(2) + "px,0)";
      }
      if (item.charge) {
        item.charge.style.opacity = (Math.sin(Math.PI * progress) * 0.72).toFixed(3);
        item.charge.style.transform = "scaleX(" + progress.toFixed(4) + ")";
      }
      item.shell.classList.toggle("is-filling", progress > 0.001 && progress < 0.999);
      item.shell.classList.toggle("is-filled", progress >= 0.999);
    };

    var applyScrollResult = function (progress) {
      var target = scrollResultTargets[current];
      if (!target) return;

      var resultProgress = easeScrollProgress((progress - 0.16) / 0.84);
      var displayed = {
        scale: target.scale * resultProgress,
        salt: target.salt * resultProgress,
        total: target.total * resultProgress,
        metrics: target.metrics.map(function (metric) {
          return {
            label: metric.label,
            value: metric.value * resultProgress,
            unit: metric.unit,
            decimals: metric.decimals,
            kind: metric.kind
          };
        })
      };

      applyResultStructure(displayed, false);
      applyResultValues(displayed);

      var total = target.scale + target.salt;
      var scaleShare = total > 0 ? target.scale / total : 0.5;
      if (out.barScale) out.barScale.style.transform = "scaleX(" + (scaleShare * resultProgress).toFixed(4) + ")";
      if (out.barSalt) out.barSalt.style.transform = "scaleX(" + ((1 - scaleShare) * resultProgress).toFixed(4) + ")";

      scrollResultValueNodes.forEach(function (node) {
        node.style.opacity = (0.34 + resultProgress * 0.66).toFixed(3);
        node.style.transform = "translate3d(0," + ((1 - resultProgress) * 4).toFixed(2) + "px,0)";
      });
      if (scrollResultAccent) {
        scrollResultAccent.style.transform = "scaleX(" + resultProgress.toFixed(4) + ")";
      }

      if (out.msg) {
        out.msg.textContent = resultProgress < 0.01
          ? "وسوف يظهر الإمكانات مع البيانات النظام."
          : resultProgress < 0.985
            ? "يعد النموذج المعايير التالية النظام."
            : resultMessage(target.total);
      }

      result.classList.toggle("is-scroll-complete", resultProgress >= 0.999);
    };

    var measureScrollScrub = function () {
      scrollScrubViewportHeight = Math.max(window.innerHeight || 0, 1);
    };

    var readScrollScrubProgress = function () {
      var formTop = form.getBoundingClientRect().top;
      var startLine = scrollScrubViewportHeight * 0.88;
      var endLine = scrollScrubViewportHeight * 0.16;
      return clampScrollProgress((startLine - formTop) / (startLine - endLine));
    };

    var renderScrollScrub = function (force) {
      if (!scrollScrubActive) return;

      var progress = readScrollScrubProgress();

      if (!force && Math.abs(progress - scrollScrubProgress) < 0.0005) return;
      scrollScrubProgress = progress;
      scrollScrubWriting = true;

      var activeTargets = scrollTargetsByType[current] || [];
      activeTargets.forEach(function (item, index) {
        setScrollInputValue(item, inputScrollProgress(progress, index, activeTargets.length));
      });
      applyScrollResult(progress);

      form.classList.toggle("is-scroll-complete", progress >= 0.999);
      scrollScrubWriting = false;
    };

    var runScrollScrubFrame = function () {
      var shouldForce = scrollScrubForce;
      scrollScrubFrame = 0;
      scrollScrubForce = false;
      renderScrollScrub(shouldForce);
    };

    var requestScrollScrub = function (force) {
      scrollScrubForce = scrollScrubForce || !!force;
      if (scrollScrubFrame) return;
      scrollScrubFrame = requestAnimationFrame(runScrollScrubFrame);
    };

    var onScrollScrubResize = function () {
      measureScrollScrub();
      requestScrollScrub(true);
    };

    var onScrollScrubScroll = function () {
      if (scrollScrubVisible) requestScrollScrub(false);
    };

    var finishScrollScrub = function () {
      if (!scrollScrubActive) return;
      scrollScrubActive = false;
      if (scrollScrubFrame) cancelAnimationFrame(scrollScrubFrame);
      scrollScrubFrame = 0;
      scrollScrubVisible = false;
      window.removeEventListener("scroll", onScrollScrubScroll);
      window.removeEventListener("resize", onScrollScrubResize);
      if (scrollScrubObserver) scrollScrubObserver.disconnect();
      scrollScrubObserver = null;

      scrollScrubWriting = true;
      Object.keys(scrollTargetsByType).forEach(function (type) {
        scrollTargetsByType[type].forEach(function (item) {
          item.input.value = item.targetText;
          item.input.dispatchEvent(new Event("input", { bubbles: true }));
          item.shell.removeAttribute("data-scroll-field");
          item.shell.classList.remove("is-filling", "is-filled");
          if (item.visual) {
            item.visual.style.removeProperty("opacity");
            item.visual.style.removeProperty("transform");
          }
          if (item.charge) item.charge.remove();
        });
      });
      scrollScrubWriting = false;

      scrollResultValueNodes.forEach(function (node) {
        node.style.removeProperty("opacity");
        node.style.removeProperty("transform");
      });
      if (scrollResultAccent) scrollResultAccent.style.removeProperty("transform");

      form.classList.remove("is-scroll-scrubbing", "is-scroll-complete");
      result.classList.remove("is-scroll-scrubbing", "is-scroll-complete");
      result.removeAttribute("aria-busy");
      result.setAttribute("aria-live", "polite");
      calculate();
    };

    var setupScrollScrub = function () {
      if (!("IntersectionObserver" in window)) return false;
      scrollTargetsByType.kotly = collectScrollTargets("kotly");
      scrollTargetsByType.skraplacze = collectScrollTargets("skraplacze");
      if (!scrollTargetsByType.kotly.length || !scrollTargetsByType.skraplacze.length) return false;

      scrollResultTargets.kotly = calcBoiler();
      scrollResultTargets.skraplacze = calcCond();
      Object.keys(scrollTargetsByType).forEach(function (type) {
        scrollTargetsByType[type].forEach(function (item) {
          item.shell.setAttribute("data-scroll-field", "");
        });
      });

      measureScrollScrub();
      scrollScrubReady = true;
      scrollScrubActive = true;
      form.classList.add("is-scroll-scrubbing");
      result.classList.add("is-scroll-scrubbing");
      result.setAttribute("aria-live", "off");
      window.addEventListener("scroll", onScrollScrubScroll, { passive: true });
      window.addEventListener("resize", onScrollScrubResize);

      scrollScrubObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          scrollScrubVisible = entry.isIntersecting;
          if (scrollScrubVisible) requestScrollScrub(true);
          else {
            if (scrollScrubFrame) cancelAnimationFrame(scrollScrubFrame);
            scrollScrubFrame = 0;
            renderScrollScrub(true);
          }
        });
      }, { threshold: 0, rootMargin: "18% 0px 18% 0px" });
      scrollScrubObserver.observe(form);

      renderScrollScrub(true);
      return true;
    };

    // przełącznik typu instalacji
    var groups = form.querySelectorAll("[data-calc-fields]");
    var typebar = form.querySelector(".calc2-typebar");
    var typeButtons = Array.prototype.slice.call(form.querySelectorAll("[data-calc-type]"));
    var categoryLinks = Array.prototype.slice.call(document.querySelectorAll("[data-calc-category]"));
    var typeMotionTimer = null;
    var typeContentTimer = null;
    var typePressTimer = null;

    var syncCategoryLinks = function (type) {
      categoryLinks.forEach(function (link) {
        var active = link.getAttribute("data-calc-category") === type;
        link.classList.toggle("is-active", active);
        if (active) link.setAttribute("aria-current", "true");
        else link.removeAttribute("aria-current");
      });
    };

    var pulseTypebar = function () {
      if (!typebar) return;
      if (typePressTimer) clearTimeout(typePressTimer);
      typebar.classList.remove("is-pressing");
      void typebar.offsetWidth;
      typebar.classList.add("is-pressing");
      typePressTimer = setTimeout(function () {
        typebar.classList.remove("is-pressing");
      }, 360);
    };

    var setType = function (type) {
      if (type !== "kotly" && type !== "skraplacze") return;
      if (type === current) {
        syncCategoryLinks(type);
        pulseTypebar();
        return;
      }

      current = type;
      syncCategoryLinks(type);
      if (typebar) {
        if (typeMotionTimer) clearTimeout(typeMotionTimer);
        typebar.classList.remove("is-pressing", "is-shifting");
        void typebar.offsetWidth;
        typebar.setAttribute("data-active-type", type);
        typebar.classList.add("is-shifting");
        typeMotionTimer = setTimeout(function () {
          typebar.classList.remove("is-shifting");
        }, 640);
      }

      typeButtons.forEach(function (b) {
        var on = b.getAttribute("data-calc-type") === type;
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-selected", on ? "true" : "false");
        b.tabIndex = on ? 0 : -1;
      });
      groups.forEach(function (g) {
        if (g.getAttribute("data-calc-fields") === type) g.removeAttribute("hidden");
        else g.setAttribute("hidden", "");
      });

      if (typeContentTimer) clearTimeout(typeContentTimer);
      form.classList.remove("is-type-switching");
      void form.offsetWidth;
      form.classList.add("is-type-switching");
      typeContentTimer = setTimeout(function () {
        form.classList.remove("is-type-switching");
      }, 620);

      if (scrollScrubActive) requestScrollScrub(true);
      else calculate();
    };

    typeButtons.forEach(function (b) {
      b.tabIndex = b.getAttribute("data-calc-type") === current ? 0 : -1;
      b.addEventListener("click", function () { setType(b.getAttribute("data-calc-type")); });
    });

    syncCategoryLinks(current);
    categoryLinks.forEach(function (link) {
      link.addEventListener("click", function () {
        setType(link.getAttribute("data-calc-category"));
      });
    });

    if (typebar) {
      typebar.addEventListener("keydown", function (event) {
        var activeIndex = typeButtons.findIndex(function (button) {
          return button.getAttribute("data-calc-type") === current;
        });
        var nextIndex = activeIndex;

        if (event.key === "ArrowLeft" || event.key === "ArrowUp") nextIndex = Math.max(0, activeIndex - 1);
        else if (event.key === "ArrowRight" || event.key === "ArrowDown") nextIndex = Math.min(typeButtons.length - 1, activeIndex + 1);
        else if (event.key === "Home") nextIndex = 0;
        else if (event.key === "End") nextIndex = typeButtons.length - 1;
        else return;

        event.preventDefault();
        var nextButton = typeButtons[nextIndex];
        setType(nextButton.getAttribute("data-calc-type"));
        nextButton.focus();
      });
    }

    // suwaki -> podgląd wartości (mm)
    var syncRange = function (input) {
      var o = form.querySelector("[data-out='" + input.name + "']");
      if (o) o.textContent = (parseFloat(input.value) || 0).toFixed(1).replace(".", ",") + " mm";
    };
    form.querySelectorAll("input[type='range']").forEach(function (input) {
      syncRange(input);
      input.addEventListener("input", function () { syncRange(input); });
    });

    var finishScrubForManualControl = function (event) {
      if (!scrollScrubActive || scrollScrubWriting) return;
      if (event && event.target.closest("[data-calc-type]")) return;
      finishScrollScrub();
    };

    var calculateAfterManualChange = function () {
      if (scrollScrubWriting) return;
      if (scrollScrubActive) finishScrollScrub();
      else calculate();
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      calculateAfterManualChange();
    });
    form.addEventListener("input", calculateAfterManualChange);
    form.addEventListener("change", calculateAfterManualChange);

    // --- waluta: konwersja pól cenowych i wyniku ---
    var moneyInputs = Array.prototype.slice.call(form.querySelectorAll("input[data-money]"));
    var currencySeg = form.querySelector("[data-calc-currency]");
    var segButtons = currencySeg
      ? Array.prototype.slice.call(currencySeg.querySelectorAll("[data-cur]"))
      : [];
    var parseAmount = function (raw) {
      return Number(String(raw == null ? "" : raw).replace(",", ".")) || 0;
    };
    var formatAmount = function (v) {                 // wartość do pola number
      return String(Math.round((+v || 0) * 100) / 100);
    };
    var applyCurrency = function (nextCurrency, isInit) {
      if (!(rates[nextCurrency] > 0)) return;
      // Najpierw domknij animację scrolla — przywraca pola do wartości bazowych
      // (w zł), zanim je przeliczymy; inaczej nadpisałaby naszą konwersję.
      if (!isInit && scrollScrubActive) finishScrollScrub();
      moneyInputs.forEach(function (input) {
        var unitNode = input.parentNode
          ? input.parentNode.querySelector("em[data-cur-unit]") : null;
        // Bazę cen trzymamy w PLN (data-base-pln), więc przełączanie walut nie
        // kumuluje zaokrągleń. Pola startują z cenami w złotych.
        if (isInit) input.setAttribute("data-base-pln", parseAmount(input.value));
        var basePln = parseAmount(input.getAttribute("data-base-pln"));
        input.value = formatAmount(basePln / rates[nextCurrency]);
        if (unitNode) {
          unitNode.textContent = curSym(nextCurrency) + (unitNode.getAttribute("data-cur-unit") || "");
        }
      });
      currency = nextCurrency;
      segButtons.forEach(function (button) {
        var on = button.getAttribute("data-cur") === nextCurrency;
        button.classList.toggle("is-active", on);
        button.setAttribute("aria-pressed", on ? "true" : "false");
      });
      if (!isInit) calculate();
    };
    // Ręczna edycja ceny aktualizuje bazę w PLN (pomijamy zapisy animacji scrolla).
    moneyInputs.forEach(function (input) {
      input.addEventListener("input", function () {
        if (scrollScrubWriting) return;
        input.setAttribute("data-base-pln", parseAmount(input.value) * (rates[currency] || 1));
      });
    });
    segButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        applyCurrency(button.getAttribute("data-cur"), false);
      });
    });
    // ustaw walutę startową (przelicza ceny i jednostki) PRZED animacją scrolla
    applyCurrency(currency, true);

    var reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!reducedMotion && "requestAnimationFrame" in window && setupScrollScrub()) {
      form.addEventListener("pointerdown", finishScrubForManualControl, true);
      form.addEventListener("keydown", finishScrubForManualControl, true);
    } else {
      calculate();
    }
  });

  // --- coverflow branż (Nasze branże) ---
  document.querySelectorAll("[data-coverflow]").forEach(function (cf) {
    var stage = cf.querySelector("[data-cf-stage]");
    if (!stage) return;
    var cards = Array.prototype.slice.call(stage.querySelectorAll(".cf-card"));
    if (!cards.length) return;
    var total = cards.length;
    var prevBtn = cf.querySelector("[data-cf-prev]");
    var nextBtn = cf.querySelector("[data-cf-next]");
    var dotsWrap = cf.querySelector("[data-cf-dots]");
    var current = Math.floor(total / 2);
    var timer = null;
    var dots = [];
    var rotateEl = (cf.closest("section") || document).querySelector("[data-cf-rotate]");
    var lastRotate = -1;
    var renderRotate = function (text) {
      if (!rotateEl) return;
      var build = function () {
        rotateEl.classList.remove("is-exiting");
        rotateEl.innerHTML = "";
        Array.from(text).forEach(function (ch, i) {
          var s = document.createElement("span");
          s.className = "cf-rotate__ch";
          s.textContent = ch === " " ? " " : ch;
          s.style.setProperty("--i", i);
          rotateEl.appendChild(s);
        });
      };
      if (rotateEl.childNodes.length && !reduceMotion) {
        rotateEl.classList.add("is-exiting");
        window.setTimeout(build, 220);
      } else {
        build();
      }
    };

    if (dotsWrap) {
      cards.forEach(function (_c, i) {
        var b = document.createElement("button");
        b.type = "button";
        b.setAttribute("aria-label", "أرني قطاعك" + (i + 1));
        b.addEventListener("click", function () { go(i); });
        dotsWrap.appendChild(b);
        dots.push(b);
      });
    }

    var layout = function () {
      cards.forEach(function (card, index) {
        var offset = index - current;
        var pos = ((offset % total) + total) % total;
        if (pos > Math.floor(total / 2)) pos = pos - total;
        var isCenter = pos === 0;
        var isAdjacent = Math.abs(pos) === 1;
        card.style.transform =
          "translateX(" + (pos * 52) + "%) scale(" + (isCenter ? 1 : isAdjacent ? 0.84 : 0.7) + ") rotateY(" + (pos * -10) + "deg)";
        card.style.zIndex = isCenter ? 10 : isAdjacent ? 5 : 1;
        card.style.opacity = isCenter ? "1" : isAdjacent ? "0.42" : "0";
        card.style.filter = isCenter ? "blur(0px)" : "blur(4px)";
        card.style.visibility = Math.abs(pos) > 1 ? "hidden" : "visible";
        card.classList.toggle("is-center", isCenter);
        card.setAttribute("aria-hidden", isCenter ? "false" : "true");
        if (isCenter) card.removeAttribute("tabindex"); else card.setAttribute("tabindex", "-1");
      });
      dots.forEach(function (d, i) { d.classList.toggle("is-active", i === current); });
      if (current !== lastRotate) {
        lastRotate = current;
        renderRotate(cards[current].getAttribute("data-rotate") || "");
      }
    };
    var go = function (i) { current = ((i % total) + total) % total; layout(); restart(); };
    var stop = function () { if (timer) { window.clearInterval(timer); timer = null; } };
    var start = function () { if (reduceMotion || total < 2 || timer) return; timer = window.setInterval(function () { go(current + 1); }, 4000); };
    var restart = function () { stop(); start(); };

    if (nextBtn) nextBtn.addEventListener("click", function () { go(current + 1); });
    if (prevBtn) prevBtn.addEventListener("click", function () { go(current - 1); });

    cards.forEach(function (card, index) {
      card.addEventListener("click", function (e) {
        if (index !== current) { e.preventDefault(); go(index); }
      });
    });

    cf.addEventListener("mouseenter", stop);
    cf.addEventListener("mouseleave", start);
    cf.addEventListener("focusin", stop);
    cf.addEventListener("focusout", start);

    var sx = null;
    stage.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    stage.addEventListener("touchend", function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 40) { go(current + (dx < 0 ? 1 : -1)); }
      sx = null;
    });

    window.addEventListener("resize", layout);
    layout();
    start();
  });

  // --- branże: scrollytelling z rotującym tekstem ---
  document.querySelectorAll("[data-branze-scroll]").forEach(function (section) {
    var shots = Array.prototype.slice.call(section.querySelectorAll(".branze-shot"));
    var data = Array.prototype.slice.call(section.querySelectorAll(".branze-data li"));
    if (!shots.length || !data.length) return;
    var n = Math.min(shots.length, data.length);
    var rotateEl = section.querySelector("[data-branze-rotate]");
    var descEl = section.querySelector("[data-branze-desc]");
    var ctaEl = section.querySelector("[data-branze-cta]");
    var dotsWrap = section.querySelector("[data-branze-dots]");
    var index = -1;
    var dots = [];
    if (dotsWrap) {
      for (var k = 0; k < n; k++) {
        var sp = document.createElement("span");
        dotsWrap.appendChild(sp);
        dots.push(sp);
      }
    }
    var mq = window.matchMedia("(max-width: 860px)");
    var timer = null;

    var renderBranzeRotate = function (text) {
      if (!rotateEl) return;
      var build = function () {
        rotateEl.classList.remove("is-exiting");
        rotateEl.innerHTML = "";
        Array.from(text).forEach(function (ch, i) {
          var s = document.createElement("span");
          s.className = "cf-rotate__ch";
          s.textContent = ch;
          s.style.setProperty("--i", i);
          rotateEl.appendChild(s);
        });
      };
      if (rotateEl.childNodes.length && !reduceMotion) {
        rotateEl.classList.add("is-exiting");
        window.setTimeout(build, 220);
      } else {
        build();
      }
    };

    var setActive = function (i) {
      i = Math.max(0, Math.min(n - 1, i));
      if (i === index) return;
      index = i;
      shots.forEach(function (sh, kk) { sh.classList.toggle("is-active", kk === i); });
      dots.forEach(function (d, kk) { d.classList.toggle("is-active", kk === i); });
      var d = data[i];
      renderBranzeRotate(d.getAttribute("data-name") || "");
      if (descEl) {
        if (reduceMotion) {
          descEl.textContent = d.getAttribute("data-desc") || "";
        } else {
          descEl.classList.add("is-swapping");
          window.setTimeout(function () {
            descEl.textContent = d.getAttribute("data-desc") || "";
            descEl.classList.remove("is-swapping");
          }, 200);
        }
      }
      if (ctaEl) ctaEl.setAttribute("href", d.getAttribute("data-href") || "#");
    };

    var bTicking = false;
    var onBranzeScroll = function () {
      bTicking = false;
      if (mq.matches) return;
      var rect = section.getBoundingClientRect();
      var scrollable = section.offsetHeight - window.innerHeight;
      if (scrollable <= 0) { setActive(0); return; }
      var p = Math.max(0, Math.min(1, (-rect.top) / scrollable));
      setActive(Math.min(n - 1, Math.floor(p * n)));
    };
    var requestBranzeScroll = function () { if (bTicking) return; bTicking = true; requestAnimationFrame(onBranzeScroll); };

    var stopBranzeTimer = function () { if (timer) { window.clearInterval(timer); timer = null; } };
    var startBranzeTimer = function () {
      if (timer || reduceMotion || !mq.matches) return;
      timer = window.setInterval(function () { setActive((index + 1) % n); }, 3600);
    };
    var applyBranzeMode = function () {
      stopBranzeTimer();
      if (mq.matches) { startBranzeTimer(); } else { onBranzeScroll(); }
    };

    window.addEventListener("scroll", requestBranzeScroll, { passive: true });
    window.addEventListener("resize", function () { requestBranzeScroll(); applyBranzeMode(); });
    if (mq.addEventListener) mq.addEventListener("change", applyBranzeMode);
    else if (mq.addListener) mq.addListener(applyBranzeMode);
    section.addEventListener("mouseenter", stopBranzeTimer);
    section.addEventListener("mouseleave", startBranzeTimer);

    setActive(0);
    applyBranzeMode();
  });

  // --- branże: menu + karty (styl agencyjny) ---
  document.querySelectorAll("[data-branze-svc]").forEach(function (sec) {
    var btns = Array.prototype.slice.call(sec.querySelectorAll("[data-branze-tab]"));
    var panes = Array.prototype.slice.call(sec.querySelectorAll("[data-branze-pane]"));
    if (!btns.length || !panes.length) return;
    var media = sec.querySelector("[data-branze-media]");
    var current = -1;
    var setMedia = function (i) {
      if (!media) return;
      var img = getComputedStyle(panes[i]).getPropertyValue("--pane-img").trim();
      if (!img || img === "none") return;
      media.classList.add("is-swapping");
      window.setTimeout(function () {
        media.style.backgroundImage = img;
        media.classList.remove("is-swapping");
      }, 180);
    };
    var activate = function (i) {
      if (i === current) return;
      current = i;
      btns.forEach(function (b, k) {
        var on = k === i;
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-selected", on ? "true" : "false");
      });
      panes.forEach(function (p, k) { p.classList.toggle("is-active", k === i); });
      setMedia(i);
    };
    btns.forEach(function (b, i) {
      b.addEventListener("click", function () { activate(i); });
      b.addEventListener("mouseenter", function () { activate(i); });
      b.addEventListener("focus", function () { activate(i); });
    });
    activate(0);

    // --- scroll-scrub: lewa z lewej krawędzi, prawa (zdjęcie+punkty) z prawej ---
    var leftEls = [].concat(
      Array.prototype.slice.call(sec.querySelectorAll(".branze-svc__intro .eyebrow, .branze-svc__intro h2, .branze-svc__lead")),
      Array.prototype.slice.call(sec.querySelectorAll(".branze-menu li"))
    );
    var rightEl = sec.querySelector(".branze-svc__panels");
    leftEls.forEach(function (el) { el.classList.add("branze-anim"); });
    if (rightEl) rightEl.classList.add("branze-anim-r");
    var easeOut = function (x) { return 1 - Math.pow(1 - x, 3); };
    var sTick = false;
    var applyScrub = function () {
      sTick = false;
      var vh = window.innerHeight || 1;
      var rect = sec.getBoundingClientRect();
      var p = reduceMotion ? 1 : (vh - rect.top) / vh;
      p = Math.max(0, Math.min(1, p));
      leftEls.forEach(function (el, i) {
        var lp = easeOut(Math.max(0, Math.min(1, (p - i * 0.04) / 0.62)));
        el.style.transform = "translateX(" + ((1 - lp) * -100).toFixed(2) + "vw)";
        el.style.opacity = lp.toFixed(3);
      });
      if (rightEl) {
        var rp = easeOut(Math.max(0, Math.min(1, (p - 0.05) / 0.62)));
        rightEl.style.transform = "translateX(" + ((1 - rp) * 100).toFixed(2) + "vw)";
        rightEl.style.opacity = rp.toFixed(3);
      }
    };
    var reqScrub = function () { if (sTick) return; sTick = true; requestAnimationFrame(applyScrub); };
    window.addEventListener("scroll", reqScrub, { passive: true });
    window.addEventListener("resize", reqScrub);
    window.addEventListener("load", reqScrub);
    applyScrub();
  });

  // --- generyczny scroll-scrub: .scrub-l z lewej, .scrub-r z prawej ---
  document.querySelectorAll("[data-scrub]").forEach(function (sec) {
    var lefts = Array.prototype.slice.call(sec.querySelectorAll(".scrub-l"));
    var rights = Array.prototype.slice.call(sec.querySelectorAll(".scrub-r"));
    if (!lefts.length && !rights.length) return;
    var ease = function (x) { return 1 - Math.pow(1 - x, 3); };
    var tick = false;
    var apply = function () {
      tick = false;
      var vh = window.innerHeight || 1;
      var rect = sec.getBoundingClientRect();
      var p = reduceMotion ? 1 : Math.max(0, Math.min(1, (vh - rect.top) / vh));
      lefts.forEach(function (el, i) {
        var lp = ease(Math.max(0, Math.min(1, (p - i * 0.05) / 0.6)));
        el.style.transform = "translateX(" + ((1 - lp) * -100).toFixed(2) + "vw)";
        el.style.opacity = lp.toFixed(3);
      });
      rights.forEach(function (el, i) {
        var rp = ease(Math.max(0, Math.min(1, (p - 0.05 - i * 0.04) / 0.6)));
        el.style.transform = "translateX(" + ((1 - rp) * 100).toFixed(2) + "vw)";
        el.style.opacity = rp.toFixed(3);
      });
    };
    var req = function () { if (tick) return; tick = true; requestAnimationFrame(apply); };
    window.addEventListener("scroll", req, { passive: true });
    window.addEventListener("resize", req);
    window.addEventListener("load", req);
    apply();
  });

  // --- odwracalne wejścia z boków, sterowane pozycją każdego elementu ---
  document.querySelectorAll("[data-scroll-fly]").forEach(function (section) {
    var flyItems = Array.prototype.slice.call(section.querySelectorAll("[data-fly]"));
    if (!flyItems.length) return;
    flyItems.forEach(function (item) { item.classList.add("scroll-fly-item"); });

    var flyTicking = false;
    var clampFly = function (value) { return Math.max(0, Math.min(1, value)); };
    var easeFly = function (value) { return 1 - Math.pow(1 - value, 3); };
    var updateFly = function () {
      flyTicking = false;
      var vh = window.innerHeight || 1;
      var vw = window.innerWidth || document.documentElement.clientWidth || 1;
      var startLine = vh * .94;
      var travelSpan = vh * .42;

      flyItems.forEach(function (item) {
        var direction = item.getAttribute("data-fly") || "left";
        var delay = parseFloat(item.getAttribute("data-fly-delay") || "0") || 0;
        var syncSelector = item.getAttribute("data-fly-sync");
        var syncTarget = syncSelector ? section.querySelector(syncSelector) : null;
        var measuredTop = (syncTarget || item).getBoundingClientRect().top;
        var distanceScale = parseFloat(item.getAttribute("data-fly-distance") || "1") || 1;
        var raw = reduceMotion ? 1 : (startLine - measuredTop) / travelSpan;
        var progress = reduceMotion ? 1 : clampFly((raw - delay) / .74);
        var eased = easeFly(progress);
        var distance = (vw + Math.min(item.offsetWidth || 0, 520) + 100) * distanceScale;
        var x = direction === "right" ? (1 - eased) * distance : -(1 - eased) * distance;

        item.style.translate = x.toFixed(1) + "px 0";
        item.style.opacity = eased.toFixed(3);
        item.style.visibility = progress <= .001 ? "hidden" : "visible";
        item.style.pointerEvents = progress < .08 ? "none" : "";
      });
    };
    var requestFly = function () {
      if (flyTicking) return;
      flyTicking = true;
      requestAnimationFrame(updateFly);
    };

    window.addEventListener("scroll", requestFly, { passive: true });
    window.addEventListener("resize", requestFly);
    window.addEventListener("load", requestFly);
    updateFly();
  });

  // --- listy realizacji / bazy wiedzy: wyszukiwarka + paginacja ---
  // Filtruje pozycje po fragmencie tytułu (element <strong>) i dzieli je na
  // strony po 5 (numerowana nawigacja 1, 2, 3 … N).
  var STORIES_PER_PAGE = 5;
  // animacja pojawiania się wierszy przy zmianie strony: fade-up z efektem domina
  // (każdy kolejny wiersz startuje z narastającym opóźnieniem — kaskada jak spadające kostki)
  function animateStoryRows(els) {
    if (reduceMotion) return;
    els.forEach(function (el, i) {
      if (!el.animate) return;
      el.animate(
        [
          { opacity: 0, transform: "translateY(22px)" },
          { opacity: 1, transform: "translateY(0)" }
        ],
        { duration: 440, delay: Math.min(i, 9) * 85, easing: "cubic-bezier(.2,.75,.25,1)", fill: "backwards" }
      );
    });
  }
  Array.prototype.slice.call(document.querySelectorAll(".company-stories__list")).forEach(function (list) {
    var section = list.closest ? list.closest(".company-stories") : null;
    if (!section) return;
    var input = section.querySelector("[data-stories-search]");
    var pager = section.querySelector("[data-stories-pager]");
    var empty = section.querySelector("[data-stories-empty]");
    if (!input && !pager) return;
    var paginate = !!pager;
    var items = Array.prototype.slice.call(list.querySelectorAll("a"));
    var page = 1;

    function matches() {
      var q = input ? input.value.trim().toLowerCase() : "";
      if (!q) return items;
      return items.filter(function (a) {
        var strong = a.querySelector("strong");   // tytuł
        var cat = a.querySelector("span");          // kategoria (etykieta)
        var hay = ((cat ? cat.textContent + " " : "") + (strong ? strong.textContent : a.textContent)).toLowerCase();
        return hay.indexOf(q) !== -1;
      });
    }

    function pageList(cur, total) {
      var out = [], i;
      if (total <= 7) { for (i = 1; i <= total; i++) out.push(i); return out; }
      out.push(1);
      var left = Math.max(2, cur - 1), right = Math.min(total - 1, cur + 1);
      if (left > 2) out.push("...");
      for (i = left; i <= right; i++) out.push(i);
      if (right < total - 1) out.push("...");
      out.push(total);
      return out;
    }

    function pbtn(label, target, disabled, active, aria) {
      return '<button type="button" class="stories-pager__btn' + (active ? " is-active" : "") + '"'
        + (disabled ? " disabled" : "")
        + ' data-page="' + target + '" aria-label="' + aria + '"'
        + (active ? ' aria-current="page"' : "") + ">" + label + "</button>";
    }

    function drawPager(total) {
      if (!pager) return;
      if (total <= 1) { pager.innerHTML = ""; pager.hidden = true; return; }
      pager.hidden = false;
      var html = pbtn("‹", page - 1, page <= 1, false, "الصفحة السابقة");
      pageList(page, total).forEach(function (n) {
        if (n === "...") { html += '<span class="stories-pager__gap" aria-hidden="true">…</span>'; return; }
        html += pbtn(String(n), n, false, n === page, "الصفحة" + n);
      });
      html += pbtn("›", page + 1, page >= total, false, "الصفحة التالية");
      pager.innerHTML = html;
    }

    function render(animate) {
      var vis = matches();
      var total = Math.max(1, Math.ceil(vis.length / STORIES_PER_PAGE));
      if (page > total) page = total;
      if (page < 1) page = 1;
      var shown = paginate ? vis.slice((page - 1) * STORIES_PER_PAGE, page * STORIES_PER_PAGE) : vis;
      items.forEach(function (a) { a.hidden = true; });
      shown.forEach(function (a) { a.hidden = false; a.classList.add("in-view"); });
      if (empty) empty.hidden = vis.length !== 0;
      drawPager(paginate ? total : 1);
      if (animate) animateStoryRows(shown);
    }

    if (input) {
      input.addEventListener("input", function () { page = 1; render(); });
      input.addEventListener("keydown", function (e) {
        if (e.key === "Escape") { input.value = ""; page = 1; render(); }
      });
    }
    if (pager) {
      pager.addEventListener("click", function (e) {
        var b = e.target.closest ? e.target.closest("button[data-page]") : null;
        if (!b || b.disabled) return;
        var p = parseInt(b.getAttribute("data-page"), 10);
        if (!isNaN(p) && p !== page) {
          page = p;
          render(true);
          // bez auto-przewijania — strona zostaje w miejscu, zmienia się tylko lista
        }
      });
    }
    render();
  });
})();
