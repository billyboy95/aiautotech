/* AI AutoTech redesign — small vanilla helpers */
(function () {
  "use strict";
  document.documentElement.classList.remove("no-js");
  // Mobile menu
  var btn = document.getElementById("nav-toggle"), menu = document.getElementById("mobile-menu");
  if (btn && menu) {
    var set = function (open) {
      menu.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    };
    btn.addEventListener("click", function () { set(!menu.classList.contains("open")); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) set(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && menu.classList.contains("open")) { set(false); btn.focus(); } });
    window.addEventListener("resize", function () { if (window.innerWidth >= 1080) set(false); });
  }
  // Tap glow on touch devices: light the button up the moment it is touched
  var glowSel = ".svc-btn, .outcome";
  document.addEventListener("touchstart", function (e) {
    var el = e.target.closest && e.target.closest(glowSel);
    if (!el) return;
    el.classList.add("is-tapped");
    setTimeout(function () { el.classList.remove("is-tapped"); }, 900);
  }, { passive: true });
  // Reveal on scroll
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add("in"); });
  }
  // Sticky mobile audit bar after the hero
  var bar = document.getElementById("sticky-audit"), hero = document.querySelector(".hero, .svc-hero");
  if (bar && hero && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      bar.classList.toggle("show", !entries[0].isIntersecting);
    }).observe(hero);
  }
  // Year
  var y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
