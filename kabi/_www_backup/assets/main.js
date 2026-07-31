/* Kabi-Chemie — drobna interaktywność (bez zależności) */
(function () {
  "use strict";

  // --- menu mobilne ---
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

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
    item.addEventListener("pointerenter", function () {
      if (mq.matches) return;
      clearSubmenuTimer(item);
      openSubmenu(item);
    });
    item.addEventListener("pointerleave", function () { if (!mq.matches) scheduleSubmenuClose(item); });
    if (panel) {
      panel.addEventListener("pointerenter", function () { clearSubmenuTimer(item); });
      panel.addEventListener("pointerleave", function () { if (!mq.matches) scheduleSubmenuClose(item); });
    }
    item.addEventListener("focusin", function () { if (!mq.matches) openSubmenu(item); });
    item.addEventListener("focusout", function () {
      if (mq.matches) return;
      window.setTimeout(function () {
        if (!item.contains(document.activeElement)) closeSubmenu(item);
      }, 0);
    });
    link.addEventListener("click", function (e) {
      var li = link.parentElement;
      if (!mq.matches) {
        if (li.getAttribute("data-click-open") !== "true") {
          e.preventDefault();
          openSubmenu(li);
          li.setAttribute("data-click-open", "true");
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
        // każda liczba pojawia się, gdy linia "dorysuje się" do jej miejsca
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
    core.setAttribute("title", "Kliknij, aby ukryć lub pokazać etapy procesu");
    var hint = document.createElement("span");
    hint.className = "proc-hub__hint";
    hint.textContent = "Kliknij, aby zwinąć";
    core.appendChild(hint);
    var toggle = function () {
      var hidden = arc.classList.toggle("steps-hidden");
      core.setAttribute("aria-expanded", hidden ? "false" : "true");
      hint.textContent = hidden ? "Kliknij, aby rozwinąć" : "Kliknij, aby zwinąć";
    };
    core.addEventListener("click", toggle);
    core.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") { e.preventDefault(); toggle(); }
    });

    // wejście kart odpalane PRZY SCROLLU — i powtarzane przy każdym wejściu w widok
    var reveal = function (on) {
      arc.classList.toggle("in-view", on);
      if (!on) arc.classList.remove("proc-ready");
    };
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { reveal(e.isIntersecting); });
      }, { threshold: 0.22 }).observe(arc);
    } else {
      reveal(true);
    }
    // po zakończeniu animacji wejścia kart włącz szybki, bezopóźnieniowy hover
    steps.addEventListener("transitionend", function (e) {
      if (e.propertyName === "transform" && arc.classList.contains("in-view")) arc.classList.add("proc-ready");
    });
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

  // --- animowany akordeon kart w sekcji "Czym się zajmujemy" ---
  // --- animowana rolka cytatow Kabi-Chemie ---
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
        dot.setAttribute("aria-label", "Przejdź do case study " + (index + 1));
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

  var getContactField = function (form, names) {
    for (var i = 0; i < names.length; i++) {
      var el = form.querySelector("[name='" + names[i] + "']");
      if (el) return el;
    }
    return null;
  };

  var buildContactTemplate = function (form) {
    var identityField = getContactField(form, ["identity", "name"]);
    var phoneField = getContactField(form, ["phone", "tel"]);
    var emailField = getContactField(form, ["email"]);
    var topicField = getContactField(form, ["topic", "type", "installation", "goal"]);
    var identityValue = (identityField && identityField.value || "").trim();
    var phoneValue = (phoneField && phoneField.value || "").trim();
    var emailValue = (emailField && emailField.value || "").trim();
    var topicValue = (topicField && topicField.value || "").trim();
    var topicText = topicValue || "doboru rozwiązania dla instalacji";
    var topicDetails = {
      "audytu technicznego": "Chcemy sprawdzić aktualny stan instalacji, parametry wody i możliwe obszary oszczędności.",
      "kondycjonowania wody kotłowej": "Chcemy dobrać bezpieczny program kondycjonowania wody kotłowej i ograniczyć ryzyko kamienia, korozji oraz strat energii.",
      "odkamieniania instalacji": "Chcemy omówić bezpieczne usunięcie osadów oraz ocenę, czy instalacja wymaga czyszczenia chemicznego.",
      "ochrony antykorozyjnej": "Chcemy ograniczyć ryzyko korozji i dobrać sposób zabezpieczenia instalacji do warunków pracy zakładu.",
      "ochrony membran RO": "Chcemy skonsultować ochronę membran RO, stabilność parametrów i możliwe przyczyny spadku wydajności.",
      "układów chłodniczych": "Chcemy omówić pracę układu chłodniczego, jakość wody obiegowej i dobór programu zabezpieczenia skraplaczy.",
      "serwisu urządzeń": "Chcemy ustalić zakres serwisu urządzeń, automatyki lub dozowania oraz najbliższy możliwy termin kontaktu.",
      "analizy wody": "Chcemy wykonać lub omówić analizę wody i przełożyć wyniki na konkretne zalecenia dla instalacji.",
      "białych certyfikatów": "Chcemy sprawdzić, czy planowane działania mogą kwalifikować się do białych certyfikatów i jak przygotować dane do oceny.",
      "doboru najlepszego rozwiązania": "Nie mamy jeszcze pewności, który kierunek będzie najlepszy, dlatego prosimy o krótką diagnozę i rekomendację kolejnego kroku."
    };
    var details = topicDetails[topicValue] || "Chcemy omówić sytuację z inżynierem KABI-CHEMIE i ustalić najlepszy kolejny krok.";
    var contactLines = [];
    if (identityValue) contactLines.push("Firma / osoba kontaktowa: " + identityValue);
    if (phoneValue) contactLines.push("Telefon: " + phoneValue);
    if (emailValue) contactLines.push("E-mail: " + emailValue);
    var contactBlock = contactLines.length ? contactLines.join("\n") : "Dane kontaktowe zostały wpisane w formularzu.";
    var closing = identityValue || "Dziękujemy";

    return (
      "Dzień dobry,\n\n" +
      "prosimy o kontakt w sprawie " + topicText + ".\n" +
      details + "\n\n" +
      "Dane kontaktowe:\n" +
      contactBlock + "\n\n" +
      "Pozdrawiamy serdecznie\n" +
      closing
    );
  };

  var syncContactTemplate = function (form, force) {
    var messageField = getContactField(form, ["message"]);
    if (!messageField) return;
    if (!force && messageField.dataset.userEdited === "true") return;
    var next = buildContactTemplate(form);
    if (force || !messageField.value.trim() || messageField.dataset.templateValue === messageField.value) {
      messageField.value = next;
      messageField.dataset.templateValue = next;
    }
  };

  // --- formularze (wersja statyczna / demo) ---
  document.querySelectorAll(".contact-form").forEach(function (form) {
    var identityField = getContactField(form, ["identity", "name"]);
    var phoneField = getContactField(form, ["phone", "tel"]);
    var emailField = getContactField(form, ["email"]);
    var topicField = getContactField(form, ["topic", "type", "installation", "goal"]);
    var messageField = getContactField(form, ["message"]);

    var updateTemplate = function () { syncContactTemplate(form, false); };

    [identityField, phoneField, emailField].forEach(function (field) {
      if (!field) return;
      field.addEventListener("input", updateTemplate);
      field.addEventListener("change", updateTemplate);
    });
    if (topicField) {
      topicField.addEventListener("input", updateTemplate);
      topicField.addEventListener("change", updateTemplate);
    }
    if (messageField) {
      messageField.addEventListener("input", function () {
        if (!messageField.value.trim()) {
          messageField.dataset.userEdited = "";
          syncContactTemplate(form, true);
          return;
        }
        messageField.dataset.userEdited = "true";
      });
    }

    syncContactTemplate(form, true);

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector(".form-note");
      var ok = form.checkValidity();
      if (!ok) { form.reportValidity(); return; }
      syncContactTemplate(form, false);
      if (note) {
        note.hidden = false;
        note.textContent =
          "Dziękujemy! To demonstracyjny formularz — wiadomość jest już uzupełniona gotowym szablonem. Aby działał w praktyce, podłącz go do skrzynki e-mail lub systemu formularzy. Tymczasem napisz na " +
          (form.getAttribute("data-email") || "info@kondycjonowanie-wody.pl") + ".";
      }
    });
  });

  // --- kalkulator oszczędności (model inżynierski: kotły parowe / skraplacze wyparne) ---
  document.querySelectorAll("[data-savings-calculator]").forEach(function (form) {
    var result = form.querySelector(".calc2-result");
    if (!result) return;

    // tabele osad [mm] -> strata sprawności (VLOOKUP przybliżony, jak w arkuszu)
    var BOILER = [[0.1,0.02],[0.2,0.03],[0.3,0.05],[0.4,0.06],[0.5,0.08],[0.6,0.09],[0.7,0.11],[0.8,0.12],[0.9,0.14],[1,0.15],[1.1,0.16],[1.2,0.17],[1.3,0.18],[1.4,0.19],[1.5,0.2],[1.6,0.21],[1.7,0.22],[1.8,0.23],[1.9,0.24],[2,0.25]];
    var COND   = [[0.1,0.02],[0.2,0.04],[0.3,0.06],[0.4,0.08],[0.5,0.1],[0.6,0.12],[0.7,0.14],[0.8,0.16],[0.9,0.17],[1,0.18],[1.1,0.19],[1.2,0.2],[1.3,0.22],[1.4,0.24],[1.5,0.25],[1.6,0.26],[1.7,0.27],[1.8,0.28],[1.9,0.29],[2,0.3]];
    var K = 1.56;

    var lookup = function (table, x) {
      var v = 0;
      for (var i = 0; i < table.length; i++) { if (table[i][0] <= x + 1e-9) v = table[i][1]; else break; }
      return v;
    };
    var num = function (name) {
      var el = form.querySelector("[name='" + name + "']");
      return Math.max(0, Number((el && el.value || "0").replace(",", ".")) || 0);
    };
    var zl = function (v) { return fmt(v, "zł", 2); };
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
        m1l: "Wzrost zużycia gazu", m1: pct(scaleLoss),
        m2l: "Roczna strata energii", m2: fmt(energyLoss, "MWh", 2),
        m3l: "Mniej odsolin rocznie", m3: fmt(diff, "t", 2),
        steps: {
          kb_loss: pct(scaleLoss), kb_annualE: fmt(annualEnergy, "MWh", 2), kb_lossE: fmt(energyLoss, "MWh", 2), kb_scaleSav: zl(scaleSav),
          kb_coefNow: fr(coefNow), kb_bdNow: fmt(bdNow, "t/h", 3), kb_coefAfter: fr(coefAfter), kb_bdAfter: fmt(bdAfter, "t/h", 3),
          kb_yrNow: fmt(yrNow, "t", 2), kb_yrAfter: fmt(yrAfter, "t", 2), kb_diff: fmt(diff, "t", 2),
          kb_energyGain: fmt(energyGain, "kWh", 2), kb_finGain: zl(finGain), kb_waterSav: zl(waterSav), kb_saltSav: zl(saltSav)
        }
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
        m1l: "Wyliczona grubość osadu", m1: fmt(thick, "mm", 2),
        m2l: "Strata sprawności", m2: pct(scaleLoss),
        m3l: "Mniej odsolin rocznie", m3: fmt(diff, "t", 2),
        steps: {
          sk_thick: fmt(thick, "mm", 1), sk_loss: pct(scaleLoss), sk_elec: fmt(elec, "kW", 2), sk_addElec: fmt(addElec, "kW", 2),
          sk_lossE: fmt(annualLoss, "kWh", 2), sk_scaleSav: zl(scaleSav),
          sk_coefNow: fr(coefNow), sk_evap: fmt(evap, "m³/h", 2), sk_bdNow: fmt(bdNow, "t/h", 3),
          sk_coefAfter: fr(coefAfter), sk_bdAfter: fmt(bdAfter, "t/h", 3),
          sk_yrNow: fmt(yrNow, "t", 2), sk_yrAfter: fmt(yrAfter, "t", 2), sk_diff: fmt(diff, "t", 2), sk_saltSav: zl(saltSav)
        }
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
    var current = "kotly";

    var fillSteps = function (steps) {
      if (!steps) return;
      Object.keys(steps).forEach(function (k) {
        var el = form.querySelector("[data-step='" + k + "']");
        if (el) el.textContent = steps[k];
      });
    };

    var calculate = function () {
      var r = current === "kotly" ? calcBoiler() : calcCond();
      if (out.total) out.total.textContent = zl(r.total);
      if (out.scale) out.scale.textContent = zl(r.scale);
      if (out.salt) out.salt.textContent = zl(r.salt);
      if (out.m1) out.m1.textContent = r.m1; if (out.m1l) out.m1l.textContent = r.m1l;
      if (out.m2) out.m2.textContent = r.m2; if (out.m2l) out.m2l.textContent = r.m2l;
      if (out.m3) out.m3.textContent = r.m3; if (out.m3l) out.m3l.textContent = r.m3l;
      var tot = r.scale + r.salt, ps = tot > 0 ? r.scale / tot * 100 : 50;
      if (out.barScale) out.barScale.style.width = ps.toFixed(1) + "%";
      if (out.barSalt) out.barSalt.style.width = (100 - ps).toFixed(1) + "%";
      fillSteps(r.steps);
      if (out.msg) {
        out.msg.textContent = r.total > 250000
          ? "Bardzo duży potencjał oszczędności - warto policzyć też biały certyfikat. Potwierdźmy wynik audytem technicznym."
          : r.total > 80000
            ? "Realny potencjał poprawy. Audyt wskaże, które straty da się ograniczyć najszybciej."
            : "Potencjał umiarkowany, ale wciąż warto sprawdzić zakamienienie i poziom odsalania instalacji.";
      }
    };

    // przełącznik typu instalacji
    var groups = form.querySelectorAll("[data-calc-fields]");
    var setType = function (type) {
      current = type;
      form.querySelectorAll("[data-calc-type]").forEach(function (b) {
        var on = b.getAttribute("data-calc-type") === type;
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-selected", on ? "true" : "false");
      });
      groups.forEach(function (g) {
        if (g.getAttribute("data-calc-fields") === type) g.removeAttribute("hidden");
        else g.setAttribute("hidden", "");
      });
      calculate();
    };
    form.querySelectorAll("[data-calc-type]").forEach(function (b) {
      b.addEventListener("click", function () { setType(b.getAttribute("data-calc-type")); });
    });

    // suwaki -> podgląd wartości (mm)
    var syncRange = function (input) {
      var o = form.querySelector("[data-out='" + input.name + "']");
      if (o) o.textContent = (parseFloat(input.value) || 0).toFixed(1).replace(".", ",") + " mm";
    };
    form.querySelectorAll("input[type='range']").forEach(function (input) {
      syncRange(input);
      input.addEventListener("input", function () { syncRange(input); });
    });

    form.addEventListener("submit", function (e) { e.preventDefault(); calculate(); });
    form.addEventListener("input", calculate);
    form.addEventListener("change", calculate);
    calculate();
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
        b.setAttribute("aria-label", "Pokaż branżę " + (i + 1));
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
})();
