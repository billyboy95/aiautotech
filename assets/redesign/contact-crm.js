/* AI AutoTech — contact form -> CRM (primary) + FormSubmit email (backup).
   Progressive enhancement: without JS the form still posts to FormSubmit as before. */
(function () {
  "use strict";
  var CRM_URL = "https://ai-autotech-crm.vercel.app/api/public/contact";
  var FORMSUBMIT_AJAX = "https://formsubmit.co/ajax/4b43618c4f12b0258208d17e157896bb";
  var THANKS_URL = "/thanks.html";
  var form = document.querySelector("form.contact-form");
  if (!form || !window.fetch) return;
  var loadedAt = Date.now();

  var status = form.querySelector(".form-status");
  if (!status) {
    status = document.createElement("p");
    status.className = "form-status";
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");
    status.hidden = true;
    form.appendChild(status);
  }
  var btn = form.querySelector('button[type="submit"]');
  var btnHtml = btn ? btn.innerHTML : "";

  function show(msg, kind) {
    status.hidden = false;
    status.className = "form-status " + (kind || "");
    status.innerHTML = msg;
  }
  function tracking() {
    var p = new URLSearchParams(location.search), t = {};
    try { t = JSON.parse(localStorage.getItem("aat_tracking") || "{}") || {}; } catch (e) {}
    ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"].forEach(function (k) {
      t[k] = (p.get(k) || t[k] || "").slice(0, 120);
    });
    return t;
  }
  function withTimeout(promise, ms) {
    return Promise.race([promise, new Promise(function (_, rej) { setTimeout(function () { rej(new Error("timeout")); }, ms); })]);
  }
  function postJson(url, body) {
    return withTimeout(fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(body)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok || j.ok === false || j.success === "false" || j.success === false) throw new Error(j.error || j.message || ("HTTP " + r.status));
        return j;
      });
    }), 12000);
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (form.checkValidity && !form.checkValidity()) { form.reportValidity(); return; }
    var fd = new FormData(form);
    var v = function (k) { return String(fd.get(k) || "").trim(); };
    // Honeypot: pretend success, send nothing.
    if (v("_honey")) { form.reset(); show("Thanks! Your message has been sent.", "ok"); return; }

    var t = tracking();
    var lead = {
      name: v("name"), email: v("email"), phone: v("phone"), message: v("message"),
      company: v("company") || v("business"),
      page: location.pathname, referrer: (t.referrer || document.referrer || "").slice(0, 400),
      utm_source: t.utm_source, utm_medium: t.utm_medium, utm_campaign: t.utm_campaign,
      utm_term: t.utm_term, utm_content: t.utm_content,
      elapsedMs: Date.now() - loadedAt, _honey: ""
    };
    if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
    status.hidden = true;

    var crm = postJson(CRM_URL, lead).then(function (j) { return { ok: true, id: j.id }; }, function (err) { return { ok: false, err: err }; });
    crm.then(function (c) {
      var mail = {
        name: lead.name, email: lead.email, phone: lead.phone, message: lead.message,
        _subject: "New enquiry from aiautotech.co.za", _template: "table", _captcha: "false",
        crm_status: c.ok ? ("Saved in CRM (id " + c.id + ")") : "NOT saved in CRM — add manually",
        page: lead.page, utm: [lead.utm_source, lead.utm_medium, lead.utm_campaign].filter(Boolean).join(" / ")
      };
      return postJson(FORMSUBMIT_AJAX, mail).then(function () { return { crm: c.ok, mail: true }; }, function () { return { crm: c.ok, mail: false }; });
    }).then(function (res) {
      if (res.crm || res.mail) {
        form.reset();
        if (btn) { btn.disabled = false; btn.innerHTML = btnHtml; }
        show("Thanks! Your message has been sent. Billy will get back to you shortly.", "ok");
        setTimeout(function () { location.href = THANKS_URL; }, 1200);
      } else {
        throw new Error("both failed");
      }
    }).catch(function () {
      if (btn) { btn.disabled = false; btn.innerHTML = btnHtml; }
      show('Sorry, your message could not be sent. Please try again, or ' +
        '<a href="https://wa.me/27646863803?text=' + encodeURIComponent("Hi Billy, I tried the contact form on aiautotech.co.za: " + lead.message.slice(0, 300)) + '" target="_blank" rel="noopener">WhatsApp us</a>' +
        ' / email <a href="mailto:billyfaber06@gmail.com">billyfaber06@gmail.com</a>.', "err");
    });
  });
})();
