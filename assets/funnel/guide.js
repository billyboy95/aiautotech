/* Lead magnet: name, business, email, WhatsApp -> CRM audit endpoint, source=lead_magnet. */
(function () {
  "use strict";
  var CFG = window.AAT_CONFIG, A = window.AAT;
  var form = document.getElementById("guide-form");
  if (!form || !CFG || !A) return;
  var loadedAt = Date.now();
  var CONSENT = "I agree that AI AutoTech Pty Ltd may contact me by phone, WhatsApp or email about this guide and AI for my business. I can ask to be removed at any time.";
  var GUIDE = "The 10 jobs your business should hand to AI this year (South African edition, 2026)";
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var PHONE_RE = /^[+\d][\d\s()-]{6,29}$/;
  A.captureCampaign({ landing: "/guide/" });

  var status = document.getElementById("guide-status");
  var btn = form.querySelector('button[type="submit"]');
  var btnHtml = btn ? btn.innerHTML : "";

  function show(msg, kind) {
    if (!status) return;
    status.hidden = false;
    status.className = "form-status " + (kind || "");
    status.innerHTML = msg;
  }
  function splitName(name) {
    var parts = name.trim().split(/\s+/);
    var first = (parts.shift() || "").slice(0, 60);
    var last = parts.join(" ").slice(0, 60);
    if (!last) last = ".";
    return { firstName: first, lastName: last };
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var fd = new FormData(form);
    var v = function (k) { return String(fd.get(k) || "").trim(); };
    if (v("company_website")) { form.reset(); show("Thanks. Your guide link is ready.", "ok"); return; }
    var name = v("name"), business = v("business"), email = v("email"), phone = v("whatsapp");
    if (!name || !business) { show("Please add your name and business.", "err"); return; }
    if (!EMAIL_RE.test(email)) { show("Please enter a valid email address.", "err"); return; }
    if (!(PHONE_RE.test(phone) && phone.replace(/\D/g, "").length >= 9)) { show("Please enter a valid WhatsApp number.", "err"); return; }
    if (!form.querySelector("#guide-consent").checked) { show("Please tick the box so we can send the guide and contact you about it.", "err"); return; }

    var who = splitName(name);
    var t = A.readTracking() || {};
    var payload = {
      firstName: who.firstName,
      lastName: who.lastName,
      company: business.slice(0, 120),
      email: email.slice(0, 160),
      phone: phone.slice(0, 30),
      role: "",
      website: "",
      industry: "",
      answers: {
        offer: "lead_magnet",
        guide: GUIDE,
        attribution_source: (t.source || "").slice(0, 80)
      },
      score: {},
      recommendations: [],
      recommendedAgents: [],
      consent: true,
      consentText: CONSENT,
      tracking: {
        source: "lead_magnet",
        campaign: t.campaign || t.utm_campaign || "",
        event: t.event || "",
        qr_source: t.qr_source || "",
        utm_source: t.utm_source || "",
        utm_medium: t.utm_medium || "",
        utm_campaign: t.utm_campaign || "",
        utm_term: t.utm_term || "",
        utm_content: t.utm_content || "",
        referrer: (t.referrer || A.externalReferrer() || "").slice(0, 400)
      },
      elapsedMs: 0,
      hp: v("company_website")
    };

    if (btn) { btn.disabled = true; btn.textContent = "Sending your guide…"; }
    status.hidden = true;
    send(payload, 0);

    function send(body, attempt) {
      var elapsed = Date.now() - loadedAt;
      var wait = elapsed < 16000 ? 16000 - elapsed : 0;
      setTimeout(function () {
        body.elapsedMs = Math.min(Date.now() - loadedAt, 86400000);
        var ctrl = typeof AbortController !== "undefined" ? new AbortController() : null;
        var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 25000);
        fetch(CFG.apiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
          signal: ctrl ? ctrl.signal : undefined
        }).then(function (r) {
          return r.json().catch(function () { return { ok: false, error: "Unexpected server response (" + r.status + ")." }; });
        }).then(function (res) {
          clearTimeout(timer);
          if (res && res.ok && res.reference && !res.id && attempt < 1) { send(body, attempt + 1); return; }
          if (!res || !res.ok || !res.reference || !res.id) throw new Error((res && res.error) || "Could not save your details.");
          form.hidden = true;
          var done = document.getElementById("guide-done");
          if (done) {
            done.hidden = false;
            var ref = document.getElementById("guide-ref");
            if (ref) ref.textContent = res.reference;
          }
        }).catch(function (err) {
          clearTimeout(timer);
          if (btn) { btn.disabled = false; btn.innerHTML = btnHtml; }
          var wa = A.wa("Hi Billy, I tried to get the free AI guide on aiautotech.co.za and the form did not go through. My name is " + name + ".");
          show((err && err.name === "AbortError" ? "The connection timed out." : (err && err.message) || "Network error.") +
            ' Please try again, or <a href="' + wa + '" target="_blank" rel="noopener">WhatsApp +27 64 686 3803</a>.', "err");
        });
      }, wait);
    }
  });
})();
