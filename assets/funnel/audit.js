/* AI AutoTech — Free AI Business Audit (static, no secrets). */
(function () {
  "use strict";
  var CFG = window.AAT_CONFIG, A = window.AAT;
  var STORE = "aat_audit_v1", RESULT = "aat_audit_result_v1";
  var CONSENT_TEXT = "I agree that AI AutoTech Pty Ltd may contact me by phone, WhatsApp or email about my AI business audit and recommendations. I can ask to be removed at any time.";

  /* ---------- tracking ----------
     Event leads: the printed QR opens /connect, which instantly forwards here with its query string
     plus the event UTM defaults and via=connect. Those visits always get the event attribution
     (eventDefaults, then any real URL params on top), exactly as /connect used to store it.
     Website leads: any visit carrying its own tracking params (website nav/hero/banner/footer links,
     ads, shares) or with no stored session starts a fresh attribution with source=website
     (or source derived from utm_source), so website visitors are never tagged highlevel_event.
     A return visit without params keeps the stored attribution. */
  var qs = new URLSearchParams(location.search);
  var viaConnect = qs.get("via") === "connect";
  var urlHasTracking = A.TRACK_KEYS.some(function (k) { return !!qs.get(k); });
  var tracking = A.readTracking();
  if (viaConnect) {
    tracking = A.applyUrlParams(Object.assign({ utm_term: "", utm_content: "" }, CFG.eventDefaults || {})).tracking;
    var cref = ""; try { cref = sessionStorage.getItem("aat_connect_ref") || ""; } catch (e) {}
    tracking.referrer = cref.slice(0, 400);
    tracking.landing = "/connect";
    tracking.captured_at = new Date().toISOString();
  } else if (!tracking || urlHasTracking) {
    var ev = CFG.eventDefaults || {};
    var isEventUrl = !!ev.utm_source && qs.get("utm_source") === ev.utm_source;
    var base = isEventUrl
      ? Object.assign({ utm_term: "", utm_content: "" }, ev)
      : { source: "website", campaign: "", event: "", qr_source: "", utm_source: "", utm_medium: "", utm_campaign: "", utm_term: "", utm_content: "" };
    tracking = A.applyUrlParams(base).tracking;
    if (!isEventUrl) {
      if (!qs.get("source") && qs.get("utm_source")) tracking.source = qs.get("utm_source").slice(0, 120);
      if (!qs.get("campaign") && qs.get("utm_campaign")) tracking.campaign = qs.get("utm_campaign").slice(0, 120);
    }
    tracking.referrer = (document.referrer || "").slice(0, 400);
    tracking.landing = "/audit";
    tracking.captured_at = new Date().toISOString();
  }
  A.saveTracking(tracking);
  // Tidy the address bar after a QR hop (attribution is stored; a refresh keeps it).
  if (viaConnect && window.history && history.replaceState) {
    try { history.replaceState(null, "", location.pathname + (/[?&]new=1/.test(location.search) ? "?new=1" : "") + location.hash); } catch (e) {}
  }
  var isEvent = tracking.landing === "/connect" || (!!tracking.event && tracking.event === (CFG.eventDefaults || {}).event);
  // "Rather chat on WhatsApp?" link in the top bar (keeps the WhatsApp option /connect used to offer).
  (function () {
    var link = document.getElementById("wa-alt");
    if (!link) return;
    link.href = A.wa(isEvent
      ? "Hi Billy, we met at the HighLevel event. I scanned the AI AutoTech QR code and I'd rather chat on WhatsApp about AI for my business."
      : "Hi Billy, I'd rather chat on WhatsApp than fill in the AI audit. Can you help?");
  })();

  /* ---------- helpers ---------- */
  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function arr(v) { return Array.isArray(v) ? v : (v ? [v] : []); }
  function round5(n) { return Math.max(0.5, Math.round(n * 2) / 2); }
  function fmtH(lo, hi) { lo = round5(lo); hi = Math.max(round5(hi), lo); return lo === hi ? lo + " hrs/week" : lo + "–" + hi + " hrs/week"; }
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var PHONE_RE = /^[+\d][\d\s()-]{6,29}$/;

  /* ---------- questions ---------- */
  var LEAD_SRC = ["Referrals / word of mouth", "Website", "Google search", "Facebook / Instagram", "WhatsApp", "Phone calls", "Walk-ins", "Events / networking", "Paid ads", "Portals / marketplaces"];
  var STAGES = [
    { name: "Contact", kicker: "Stage 1 · About you", title: "Let's start with you", intro: "So we can send your results and reference number.", qs: [
      { id: "firstName", type: "text", label: "First name", auto: "given-name", half: true },
      { id: "lastName", type: "text", label: "Last name", auto: "family-name", half: true },
      { id: "company", type: "text", label: "Business name", auto: "organization" },
      { id: "email", type: "text", label: "Email", input: "email", auto: "email", mode: "email", check: function (v) { return EMAIL_RE.test(v) || "Please enter a valid email address."; } },
      { id: "phone", type: "text", label: "Mobile / WhatsApp number", input: "tel", auto: "tel", mode: "tel", placeholder: "e.g. 082 123 4567", check: function (v) { return (PHONE_RE.test(v) && v.replace(/\D/g, "").length >= 9) || "Please enter a valid mobile number."; } },
      { id: "role", type: "single", label: "Your role", opts: ["Owner / Founder", "MD / CEO", "Manager", "Sales / Marketing", "Operations / Admin", "Other"] },
      { id: "consent", type: "consent" }
    ] },
    { name: "Business profile", kicker: "Stage 2 · Your business", title: "Tell us about your business", intro: "Tap the answers that fit best.", qs: [
      { id: "industry", type: "single", label: "Industry", opts: ["Professional services", "Real estate", "Automotive", "Healthcare / medical", "Beauty & wellness", "Retail / e-commerce", "Construction / trades", "Hospitality / food", "Education / training", "Finance / insurance", "Logistics / transport", "Manufacturing", "Marketing / agency", "Other"] },
      { id: "employees", type: "single", label: "How many people work in the business?", opts: ["Just me", "2–5", "6–20", "21–50", "51–200", "200+"] },
      { id: "products", type: "text", label: "Main products or services", placeholder: "e.g. car servicing, accounting, solar installs" }
    ] },
    { name: "Leads & sales", kicker: "Stage 3 · Leads & sales", title: "How leads become customers", intro: "This is where AI usually finds the fastest wins.", qs: [
      { id: "monthly_leads", type: "single", label: "New enquiries / leads per month", opts: ["0–20", "21–50", "51–150", "151–500", "500+"] },
      { id: "lead_sources", type: "multi", label: "Where do your leads come from?", hint: "Select all that apply", opts: LEAD_SRC },
      { id: "response_time", type: "single", label: "How quickly do new leads get a reply?", opts: ["Under 5 minutes", "Within an hour", "Same day", "Next day", "Longer / inconsistent"] },
      { id: "follow_up", type: "single", label: "How do you follow up leads who don't buy immediately?", opts: ["Automated sequence", "Manual and consistent", "Manual, when we remember", "We rarely follow up"] },
      { id: "lost_leads", type: "multi", label: "Why do leads get lost?", hint: "Select all that apply", opts: ["Slow response", "No follow-up", "After-hours enquiries missed", "Price shoppers", "Unqualified leads", "Don't know"] },
      { id: "booking", type: "single", label: "How are appointments / calls booked?", opts: ["Online booking link", "Phone / WhatsApp back-and-forth", "Email", "We don't book appointments"] }
    ] },
    { name: "Marketing", kicker: "Stage 4 · Marketing", title: "How you attract customers", intro: "Quick taps, no right or wrong answers.", qs: [
      { id: "channels", type: "multi", label: "Active marketing channels", hint: "Select all that apply", opts: ["Facebook", "Instagram", "LinkedIn", "TikTok", "Google Business Profile", "Website / SEO", "Email", "WhatsApp", "Print / radio", "None"], exclusive: ["None"] },
      { id: "content_creation", type: "single", label: "Who creates your content?", opts: ["Me personally", "A team member", "Agency / freelancer", "Nobody"] },
      { id: "paid_ads", type: "single", label: "Do you run paid ads?", opts: ["No", "Meta (Facebook/Instagram)", "Google", "Both / multiple"] }
    ] },
    { name: "Customer service", kicker: "Stage 5 · Customer service", title: "How customers reach you", intro: "", qs: [
      { id: "support_channels", type: "multi", label: "Main channels customers use to contact you", hint: "Select all that apply", opts: ["Phone calls", "WhatsApp", "Email", "Website chat", "Social media DMs", "In person"] },
      { id: "repeat_questions", type: "single", label: "How many repeat / common questions do you get?", opts: ["Very few", "A handful daily", "Dozens daily", "It never stops"] },
      { id: "after_hours", type: "single", label: "What happens to after-hours messages and calls?", opts: ["We answer them", "Missed until the next day", "Auto-reply only"] }
    ] },
    { name: "Operations", kicker: "Stage 6 · Operations", title: "Where the time goes", intro: "Think about the whole team, not just you.", qs: [
      { id: "admin_hours", type: "single", label: "Hours per week spent on repetitive admin (whole team)", opts: ["Under 5 hrs", "5–10 hrs", "10–20 hrs", "20–40 hrs", "40+ hrs"] },
      { id: "time_drain", type: "multi", label: "Biggest time-wasters", hint: "Pick up to 3", max: 3, opts: ["Replying to enquiries", "Following up leads", "Quotes & invoices", "Scheduling", "Reporting", "Data entry", "Marketing / content", "Staff management"] },
      { id: "reporting", type: "single", label: "Business reporting", opts: ["Automated dashboards", "Manual spreadsheets", "No regular reporting"] }
    ] },
    { name: "Tools & next steps", kicker: "Stage 7 · Tools & next steps", title: "Your tools, budget and timing", intro: "Last step, then we build your AI plan.", qs: [
      { id: "tools", type: "multi", label: "Tools you use today", hint: "Select all that apply", opts: ["Google Workspace", "Microsoft 365", "HighLevel", "Other CRM (HubSpot, Zoho…)", "Spreadsheets for leads", "Xero / Sage / QuickBooks", "Shopify / WooCommerce", "Booking software", "Zapier / Make", "None of these"], exclusive: ["None of these"] },
      { id: "wa_business", type: "single", label: "WhatsApp setup", opts: ["WhatsApp Business app", "WhatsApp API / automation", "Personal WhatsApp", "Don't use WhatsApp"] },
      { id: "ai_use", type: "single", label: "Current AI use", opts: ["Not yet", "ChatGPT personally", "Some AI tools in the business", "AI built into our workflows"] },
      { id: "goal_12m", type: "single", label: "Main goal for the next 12 months", opts: ["More leads", "Higher conversion", "Save time / reduce costs", "Better customer experience", "Scale without hiring", "Better visibility & reporting"] },
      { id: "budget", type: "single", label: "Monthly budget range for AI & automation", opts: ["Under R5,000", "R5,000–R10,000", "R10,000–R20,000", "R20,000–R50,000", "R50,000+", "Not sure yet"] },
      { id: "timeline", type: "single", label: "When would you like to start?", opts: ["As soon as possible", "Within a month", "1–3 months", "3–6 months", "Just exploring"] }
    ] }
  ];
  var CONTACT_IDS = ["firstName", "lastName", "company", "email", "phone", "role", "consent"];

  /* ---------- state ---------- */
  function load() { try { return JSON.parse(localStorage.getItem(STORE) || "null"); } catch (e) { return null; } }
  var state = load() || { stage: 0, answers: {}, startedAt: Date.now() };
  if (typeof state.stage !== "number" || state.stage < 0 || state.stage >= STAGES.length) state.stage = 0;
  state.answers = state.answers || {};
  state.startedAt = state.startedAt || Date.now();
  var saveTimer;
  function persist() {
    try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) {}
    var n = $("saved-note"); if (n) { n.textContent = "Progress saved ✓"; clearTimeout(saveTimer); saveTimer = setTimeout(function () { n.textContent = "Progress saved"; }, 1200); }
  }
  function visible(q, a) { return !q.show || q.show(a); }

  /* ---------- rendering ---------- */
  var app = $("app"), nextBtn = $("next"), backBtn = $("back"), navbar = $("navbar");

  function chipHtml(q) {
    var cur = arr(state.answers[q.id]);
    return '<div class="chips" role="group" aria-label="' + esc(q.label) + '">' + q.opts.map(function (o, i) {
      return '<button type="button" class="chip" data-q="' + q.id + '" data-i="' + i + '" aria-pressed="' + (cur.indexOf(o) >= 0) + '">' + esc(o) + "</button>";
    }).join("") + "</div>";
  }
  function qHtml(q) {
    var a = state.answers, inner = "";
    if (q.type === "consent") {
      return '<div class="q" data-qid="consent"><label class="consent"><input type="checkbox" id="f-consent"' + (a.consent ? " checked" : "") + ' /><span>' + esc(CONSENT_TEXT) + '</span></label><p class="privacy-note">Privacy: your details and answers are stored securely by AI AutoTech Pty Ltd (South Africa) and used only to prepare your audit and contact you about it, in line with POPIA. We never sell your information. <a href="/privacy.html" target="_blank" rel="noopener">Privacy policy</a>.</p><p class="q-error">Please tick the box so we can send your audit.</p>' +
        '<div class="hp" aria-hidden="true"><label>Leave empty<input type="text" id="f-hp" tabindex="-1" autocomplete="off" /></label></div></div>';
    }
    if (q.type === "text") {
      inner = '<label class="field"><input id="f-' + q.id + '" type="' + (q.input || "text") + '"' + (q.auto ? ' autocomplete="' + q.auto + '"' : "") + (q.mode ? ' inputmode="' + q.mode + '"' : "") + ' maxlength="' + (q.id === "website" ? 200 : 120) + '" placeholder="' + esc(q.placeholder || "") + '" value="' + esc(a[q.id] || "") + '" data-text="' + q.id + '" /></label>';
    } else if (q.type === "textarea") {
      inner = '<label class="field"><textarea id="f-' + q.id + '" maxlength="500" placeholder="' + esc(q.placeholder || "") + '" data-text="' + q.id + '">' + esc(a[q.id] || "") + "</textarea></label>";
    } else {
      inner = chipHtml(q);
    }
    return '<div class="q" data-qid="' + q.id + '"' + (visible(q, a) ? "" : " hidden") + '><label class="q-label" for="f-' + q.id + '">' + esc(q.label) + (q.optional ? ' <span class="muted small">(optional)</span>' : "") + "</label>" + (q.hint ? '<p class="q-hint">' + esc(q.hint) + "</p>" : "") + inner + '<p class="q-error">' + (q.type === "multi" ? "Please choose at least one." : q.type === "single" ? "Please choose one." : "Please fill this in.") + "</p></div>";
  }

  function renderStage() {
    var s = STAGES[state.stage];
    document.body.classList.remove("is-results");
    navbar.hidden = false; $("topbar").hidden = false;
    var qs = s.qs, html = "", i = 0;
    while (i < qs.length) {
      if (qs[i].half && qs[i + 1] && qs[i + 1].half) {
        html += '<div class="grid2">' + qHtml(qs[i]) + qHtml(qs[i + 1]) + "</div>"; i += 2;
      } else { html += qHtml(qs[i]); i++; }
    }
    var intro = s.intro;
    if (state.stage === 0 && isEvent) intro = "Great to meet you at HighLevel! " + intro;
    app.innerHTML = '<section class="fade-in"><div class="stage-head"><p class="kicker">' + esc(s.kicker) + "</p><h1>" + esc(s.title) + "</h1>" + (intro ? "<p>" + esc(intro) + "</p>" : "") + '</div><div id="qs">' + html + "</div></section>";
    $("stage-name").textContent = s.name;
    $("stage-count").textContent = "Stage " + (state.stage + 1) + " of " + STAGES.length;
    setProgress((state.stage / STAGES.length) * 100);
    navbar.classList.toggle("first", state.stage === 0);
    nextBtn.textContent = state.stage === STAGES.length - 1 ? "See my AI results" : "Continue";
    nextBtn.disabled = false;
  }
  function setProgress(p) { $("progress-bar").style.width = p + "%"; $("progress").setAttribute("aria-valuenow", String(Math.round(p))); }
  function refreshVisibility() {
    STAGES[state.stage].qs.forEach(function (q) {
      var el = app.querySelector('[data-qid="' + q.id + '"]');
      if (el) el.hidden = !visible(q, state.answers);
    });
  }

  app.addEventListener("click", function (e) {
    var chip = e.target.closest(".chip");
    if (!chip) return;
    var q = findQ(chip.getAttribute("data-q")); if (!q) return;
    var val = q.opts[+chip.getAttribute("data-i")];
    if (q.type === "single") {
      state.answers[q.id] = val;
    } else {
      var cur = arr(state.answers[q.id]).slice(), ix = cur.indexOf(val);
      if (ix >= 0) cur.splice(ix, 1);
      else {
        if (q.exclusive && q.exclusive.indexOf(val) >= 0) cur = [];
        else if (q.exclusive) cur = cur.filter(function (v) { return q.exclusive.indexOf(v) < 0; });
        cur.push(val);
        if (q.max && cur.length > q.max) cur.shift();
      }
      state.answers[q.id] = cur;
    }
    var box = chip.parentNode, curVals = arr(state.answers[q.id]);
    Array.prototype.forEach.call(box.querySelectorAll(".chip"), function (c) { c.setAttribute("aria-pressed", String(curVals.indexOf(q.opts[+c.getAttribute("data-i")]) >= 0)); });
    var qel = chip.closest(".q"); if (qel) qel.classList.remove("has-error");
    refreshVisibility(); persist();
  });
  app.addEventListener("input", function (e) {
    var id = e.target.getAttribute && e.target.getAttribute("data-text");
    if (id) { state.answers[id] = e.target.value.slice(0, 500); var qel = e.target.closest(".q"); if (qel) qel.classList.remove("has-error"); persist(); }
    if (e.target.id === "f-hp") state.hp = e.target.value;
  });
  app.addEventListener("change", function (e) {
    if (e.target.id === "f-consent") { state.answers.consent = e.target.checked; var qel = e.target.closest(".q"); if (qel) qel.classList.remove("has-error"); persist(); }
  });
  function findQ(id) { for (var s = 0; s < STAGES.length; s++) for (var j = 0; j < STAGES[s].qs.length; j++) if (STAGES[s].qs[j].id === id) return STAGES[s].qs[j]; return null; }

  function validateStage() {
    var firstBad = null, a = state.answers;
    STAGES[state.stage].qs.forEach(function (q) {
      var el = app.querySelector('[data-qid="' + q.id + '"]'); if (!el) return;
      el.classList.remove("has-error");
      if (!visible(q, a)) return;
      var v = a[q.id], bad = false, msg = null;
      if (q.type === "consent") bad = !v;
      else if (q.type === "multi") bad = !q.optional && arr(v).length === 0;
      else if (q.type === "single") bad = !q.optional && !v;
      else {
        v = (v || "").trim();
        if (!v) bad = !q.optional;
        else if (q.check) { var r = q.check(v); if (r !== true) { bad = true; msg = r; } }
      }
      if (bad) {
        el.classList.add("has-error");
        if (msg) el.querySelector(".q-error").textContent = msg;
        if (!firstBad) firstBad = el;
      }
    });
    if (firstBad) { firstBad.scrollIntoView({ behavior: "smooth", block: "center" }); var inp = firstBad.querySelector("input,textarea"); if (inp && inp.type !== "checkbox") setTimeout(function () { inp.focus({ preventScroll: true }); }, 300); }
    return !firstBad;
  }

  nextBtn.addEventListener("click", function () {
    if (!validateStage()) return;
    if (state.stage < STAGES.length - 1) { state.stage++; persist(); renderStage(); window.scrollTo(0, 0); }
    else submit();
  });
  backBtn.addEventListener("click", function () {
    if (state.stage > 0) { state.stage--; persist(); renderStage(); window.scrollTo(0, 0); }
  });

  /* ---------- rules engine (deterministic, no AI calls) ----------
     v5 (short audit, 30 questions): scores only use questions that are still asked.
     Answers from older saved sessions are tolerated (single values are treated as 1-item lists). */
  var LEADS = { "0–20": 10, "21–50": 35, "51–150": 100, "151–500": 300, "500+": 650 };
  var EMP = { "Just me": 1, "2–5": 3.5, "6–20": 13, "21–50": 35, "51–200": 125, "200+": 250 };
  var ADMIN = { "Under 5 hrs": 3, "5–10 hrs": 7.5, "10–20 hrs": 15, "20–40 hrs": 30, "40+ hrs": 45 };
  var REPEAT = { "Very few": 3, "A handful daily": 8, "Dozens daily": 30, "It never stops": 60 };
  var CRM_TOOLS = ["HighLevel", "Other CRM (HubSpot, Zoho…)", "CRM"];

  function analyse(a) {
    function has(id, v) { return arr(a[id]).indexOf(v) >= 0; }
    function is(id, v) { return a[id] === v; }
    function q(v) { return "“" + v + "”"; }
    function drain(v) { return has("time_drain", v); }
    var L = LEADS[a.monthly_leads] || 0, E = EMP[a.employees] || 1;
    var adminH = ADMIN[a.admin_hours] || 0, rep = REPEAT[a.repeat_questions] || 3;
    var slowReply = is("response_time", "Next day") || is("response_time", "Longer / inconsistent");
    var afterMissed = is("after_hours", "Missed until the next day");
    var waUsed = has("lead_sources", "WhatsApp") || has("support_channels", "WhatsApp") || (a.wa_business && a.wa_business !== "Don't use WhatsApp");
    var phoneUsed = has("support_channels", "Phone calls") || has("support_channels", "Phone") || has("lead_sources", "Phone calls");
    var hasCrm = arr(a.tools).some(function (t) { return CRM_TOOLS.indexOf(t) >= 0; });
    var crmName = has("tools", "HighLevel") ? "HighLevel" : "your CRM";
    var lostKnown = arr(a.lost_leads).filter(function (v) { return v !== "Don't know"; });
    var leadAssump = a.monthly_leads ? " (your answer: " + a.monthly_leads + " leads/month)" : "";
    var leader = ["Owner / Founder", "MD / CEO"].indexOf(a.role) >= 0;

    function leadRecovery(lo, hi, why) {
      if (L < 21 || !lostKnown.length) return "";
      var x = Math.max(1, Math.round(L * lo)), y = Math.max(x, Math.round(L * hi));
      return "If " + why + " recovered " + Math.round(lo * 100) + "–" + Math.round(hi * 100) + "% of your ~" + L + " monthly leads" + leadAssump + ", that is roughly " + x + "–" + y + " extra sales conversations a month. Rand value depends on your average deal size — we'll work it out with you on the strategy session.";
    }

    var A = [];
    function agent(o) { A.push(o); }

    // WhatsApp AI Employee
    (function () {
      var s = 0, p = [];
      if (has("lead_sources", "WhatsApp")) { s += 2; p.push("WhatsApp is one of your lead sources"); }
      if (has("support_channels", "WhatsApp")) { s += 2; p.push("customers contact you on WhatsApp"); }
      if (afterMissed && waUsed) { s += 3; p.push("after-hours messages wait until the next day"); }
      if (rep >= 30 && waUsed) { s += 2; p.push("you get " + q(a.repeat_questions) + " repeat questions"); }
      if ((is("wa_business", "Personal WhatsApp") || is("wa_business", "WhatsApp Business app")) && waUsed) { s += 1; p.push("WhatsApp runs manually from a phone (" + a.wa_business + ")"); }
      if (slowReply && waUsed) { s += 1; p.push("leads usually get a reply " + q(a.response_time)); }
      if (drain("Replying to enquiries")) { s += 1; p.push("replying to enquiries is one of your biggest time-wasters"); }
      agent({ id: "wa", agent: "WhatsApp AI Employee", department: "Customer Service", score: s, p: p,
        solution: "A trained WhatsApp AI Employee on your business number that answers enquiries instantly, 24/7, qualifies them and hands hot leads to your team.",
        how: "Connects to WhatsApp Business (API), learns your services, prices and FAQs, replies in seconds, captures details into your CRM and escalates anything it can't answer.",
        benefit: "No more missed or late WhatsApp enquiries; your team only handles conversations that need a human.",
        h: [rep * 5 * 2 * 0.4 / 60, rep * 5 * 4 * 0.7 / 60],
        ha: "Assumes ~" + rep + " repeat messages a day (your answer: " + q(a.repeat_questions || "Very few") + "), 2–4 min each, 40–70% handled automatically, 5 working days.",
        rev: afterMissed ? leadRecovery(0.02, 0.05, "instant 24/7 replies") : "" });
    })();

    // AI Receptionist
    (function () {
      var s = 0, p = [];
      if (phoneUsed) {
        s += 2; p.push("phone calls are a key channel for you");
        if (afterMissed) { s += 2; p.push("after-hours calls are missed until the next day"); }
        if (slowReply) { s += 1; p.push("enquiries usually get a reply " + q(a.response_time)); }
        if (is("booking", "Phone / WhatsApp back-and-forth")) { s += 1; p.push("bookings happen by phone back-and-forth"); }
        if (E <= 5) { s += 1; p.push("with a small team, calls interrupt billable work"); }
      }
      var calls = Math.max(3, Math.round(rep / 2));
      agent({ id: "rec", agent: "AI Receptionist", department: "Customer Service", score: s, p: p,
        solution: "An AI voice receptionist that answers every call, handles common questions, takes messages and books appointments.",
        how: "Your number forwards to the AI when busy or after hours; it answers with your script, captures caller details and sends you a summary on WhatsApp/email.",
        benefit: "Every call answered — including after hours — without hiring a receptionist.",
        h: [calls * 5 * 3 * 0.3 / 60, calls * 5 * 5 * 0.6 / 60],
        ha: "Assumes ~" + calls + " routine calls a day (derived from your repeat-question volume), 3–5 min each, 30–60% handled by the AI.",
        rev: "" });
    })();

    // Lead Qualification Agent
    (function () {
      var s = 0, p = [];
      if (L >= 51) { s += 2; p.push("you handle ~" + L + " leads a month" + leadAssump); }
      if (L >= 151) s += 1;
      if (has("lost_leads", "Unqualified leads")) { s += 3; p.push("time is lost on unqualified leads"); }
      if (has("lost_leads", "Price shoppers")) { s += 2; p.push("price shoppers take up sales time"); }
      if (is("goal_12m", "Higher conversion")) { s += 2; p.push("your 12-month goal is higher conversion"); }
      if (leader && E <= 5 && L >= 21) { s += 1; p.push("the owner qualifies every lead personally"); }
      agent({ id: "lq", agent: "Lead Qualification Agent", department: "Sales", score: s, p: p,
        solution: "An AI agent that asks every new lead the right questions (budget, need, timeline, location) and scores them before a human gets involved.",
        how: "Runs on WhatsApp, web forms and email; tags each lead hot/warm/cold in your CRM and routes hot leads to the right person immediately.",
        benefit: "Your time goes to buyers, not tyre-kickers.",
        h: [L * 4 * 0.4 / 60 / 4.33, L * 8 * 0.6 / 60 / 4.33],
        ha: "Assumes ~" + L + " leads a month" + leadAssump + ", 4–8 min of manual qualifying each, 40–60% handled by the agent.",
        rev: "" });
    })();

    // Sales Follow-Up Agent
    (function () {
      var s = 0, p = [];
      if (is("follow_up", "Manual, when we remember")) { s += 3; p.push("follow-up happens " + q("when we remember")); }
      if (is("follow_up", "We rarely follow up")) { s += 4; p.push("leads are rarely followed up"); }
      if (is("follow_up", "Manual and consistent")) { s += 1; p.push("follow-up is consistent but manual"); }
      if (has("lost_leads", "No follow-up")) { s += 3; p.push("you lose leads through no follow-up"); }
      if (has("lost_leads", "Slow response")) { s += 1; p.push("slow responses cost you leads"); }
      if (drain("Following up leads")) { s += 3; p.push("following up leads is one of your biggest time-wasters"); }
      if (slowReply) { s += 2; p.push("new leads get a reply " + q(a.response_time)); }
      var auto = is("follow_up", "Automated sequence");
      agent({ id: "fu", agent: "Sales Follow-Up Agent", department: "Sales", score: s, p: p,
        solution: "An AI agent that follows up every open lead and quote automatically on WhatsApp and email until they buy, book or opt out.",
        how: "Triggers from your CRM or WhatsApp; sends personalised, well-timed messages, answers replies and alerts you when someone is ready.",
        benefit: "No lead goes cold because someone was busy.",
        h: auto ? [0.5, 1] : [L * 3 / 60 / 4.33, L * 6 / 60 / 4.33],
        ha: auto ? "You already automate follow-up, so time savings are small; gains come from smarter, two-way replies." : "Assumes ~" + L + " leads a month" + leadAssump + " and 3–6 min of manual follow-up per lead.",
        rev: (has("lost_leads", "No follow-up") || has("lost_leads", "Slow response") || slowReply) ? leadRecovery(0.02, 0.05, "consistent follow-up") : "" });
    })();

    // Appointment Booking Agent
    (function () {
      var s = 0, p = [];
      if (!is("booking", "We don't book appointments")) {
        if (is("booking", "Phone / WhatsApp back-and-forth")) { s += 3; p.push("appointments are booked through back-and-forth messages"); }
        if (is("booking", "Email")) { s += 2; p.push("bookings are arranged by email"); }
        if (drain("Scheduling")) { s += 2; p.push("scheduling is one of your biggest time-wasters"); }
        if (L >= 51 && !is("booking", "Online booking link")) s += 1;
      }
      var bw = is("booking", "We don't book appointments") ? 3 : Math.max(3, Math.round(L * 0.3 / 4.33));
      agent({ id: "book", agent: "Appointment Booking Agent", department: "Sales", score: s, p: p,
        solution: "An AI agent that books, confirms, reschedules and reminds — straight into your calendar.",
        how: "Offers available slots on WhatsApp/web, syncs with Google or Outlook Calendar, sends reminders and handles reschedules.",
        benefit: "Fewer no-shows and no more message ping-pong to find a time.",
        h: [bw * 5 / 60, bw * 10 / 60],
        ha: "Assumes ~" + bw + " bookings a week (about 30% of your leads" + leadAssump + ") and 5–10 min of back-and-forth per booking.",
        rev: "" });
    })();

    // Customer Support Agent
    (function () {
      var s = 0, p = [];
      if (rep >= 8) { s += 1; p.push("you answer " + q(a.repeat_questions) + " repeat questions"); }
      if (rep >= 30) s += 2;
      if (slowReply) { s += 1; p.push("replies usually take " + q(a.response_time)); }
      if (afterMissed) s += 1;
      var n = arr(a.support_channels).length;
      if (n >= 3) { s += 1; p.push("enquiries arrive across " + n + " channels"); }
      if (is("goal_12m", "Better customer experience")) { s += 2; p.push("your 12-month goal is a better customer experience"); }
      agent({ id: "cs", agent: "Customer Support Agent", department: "Customer Service", score: s, p: p,
        solution: "An AI support agent trained on your FAQs, policies and order/job status that resolves routine questions on every channel.",
        how: "Answers on WhatsApp, web chat, email and social DMs from one knowledge base; logs every conversation and escalates complaints to a person.",
        benefit: "Faster, consistent answers and a calmer team.",
        h: [rep * 5 * 3 * 0.3 / 60, rep * 5 * 6 * 0.5 / 60],
        ha: "Assumes ~" + rep + " routine questions a day, 3–6 min each, 30–50% resolved without a person.",
        rev: "" });
    })();

    // Marketing Agent
    (function () {
      var s = 0, p = [];
      var ch = arr(a.channels).filter(function (c) { return c !== "None"; }).length;
      if (has("channels", "None")) { s += 2; p.push("there is no active marketing channel yet"); }
      if (a.paid_ads && a.paid_ads !== "No") { s += 1; p.push("you run paid ads (" + a.paid_ads + ") that need tracking back to paying customers"); }
      if (ch >= 4) { s += 1; p.push("you market on " + ch + " channels"); }
      if (is("goal_12m", "More leads")) { s += 2; p.push("your 12-month goal is more leads"); }
      if (L > 0 && L <= 20) { s += 1; p.push("you get " + a.monthly_leads + " leads a month"); }
      agent({ id: "mkt", agent: "Marketing Agent", department: "Marketing", score: s, p: p,
        solution: "An AI marketing agent that plans campaigns, runs email/WhatsApp nurture sequences and reports what's actually bringing customers.",
        how: "Connects your channels and CRM, schedules campaigns, tracks leads back to their source and sends you a plain-English weekly summary.",
        benefit: "Consistent marketing and clear evidence of what works.",
        h: [(ch || 1) * 0.5, (ch || 1) * 1],
        ha: "Assumes 30–60 min a week of planning, sending and checking results per active channel (" + (ch || 1) + " selected).",
        rev: "" });
    })();

    // Content Agent
    (function () {
      var s = 0, p = [];
      if (is("content_creation", "Me personally")) { s += 2; p.push("you create the content yourself"); }
      if (is("content_creation", "Nobody")) { s += 2; p.push("nobody owns content creation"); }
      if (drain("Marketing / content")) { s += 2; p.push("marketing and content is one of your biggest time-wasters"); }
      if (arr(a.channels).some(function (c) { return ["Facebook", "Instagram", "LinkedIn", "TikTok"].indexOf(c) >= 0; })) s += 1;
      var posts = 3;
      agent({ id: "content", agent: "Content Agent", department: "Marketing", score: s, p: p,
        solution: "An AI content agent that drafts on-brand posts, captions, emails and short-video scripts for you to approve.",
        how: "Learns your brand voice and offers, produces a weekly content calendar, and queues approved posts to your channels.",
        benefit: "Consistent presence without it eating your evenings.",
        h: [posts * 0.3, posts * 0.6],
        ha: "Assumes ~" + posts + " posts a week and 20–40 min saved per post on writing and design.",
        rev: "" });
    })();

    // CRM Automation Agent
    (function () {
      var s = 0, p = [];
      if (!hasCrm && arr(a.tools).length) { s += 3; p.push("there is no CRM" + (has("tools", "Spreadsheets for leads") ? " — leads live in spreadsheets" : "")); }
      if (has("tools", "Spreadsheets for leads")) s += 1;
      if (hasCrm && !has("tools", "Zapier / Make")) { s += 1; p.push(crmName + " isn't connected to other tools with automation yet"); }
      if (drain("Data entry")) { s += 2; p.push("data entry is one of your biggest time-wasters"); }
      if (L >= 51) s += 1;
      agent({ id: "crm", agent: "CRM Automation Agent", department: "Sales", score: s, p: p,
        solution: "An AI agent that captures every lead from WhatsApp, calls, forms and email into one CRM and keeps it updated automatically.",
        how: "Logs conversations, updates deal stages, creates tasks and reminders, and removes copy-paste between systems.",
        benefit: "One accurate pipeline — nothing slips through the cracks.",
        h: [Math.max(0.5, L * 2 / 60 / 4.33), Math.max(1, L * 4 / 60 / 4.33)],
        ha: "Assumes 2–4 min of manual capture/updating per lead for ~" + (L || 0) + " leads a month" + leadAssump + ".",
        rev: "" });
    })();

    // Quote / Proposal Agent
    (function () {
      var s = 0, p = [];
      if (drain("Quotes & invoices")) { s += 4; p.push("quotes & invoices are one of your biggest time-wasters"); }
      if (has("tools", "Xero / Sage / QuickBooks") && drain("Quotes & invoices")) s += 1;
      var qw = Math.max(2, Math.round(L * 0.4 / 4.33));
      agent({ id: "quote", agent: "Quote / Proposal Agent", department: "Sales", score: s, p: p,
        solution: "An AI agent that turns an enquiry or call notes into a branded quote or proposal in minutes, ready for your approval.",
        how: "Uses your price list, templates and past proposals; drafts the document, sends it once approved and triggers follow-up.",
        benefit: "Same-day quotes win more work than slow ones.",
        h: [qw * 15 / 60, qw * 30 / 60],
        ha: "Assumes ~" + qw + " quotes a week (about 40% of your leads" + leadAssump + ") and 15–30 min saved per quote.",
        rev: "" });
    })();

    // Operations Agent
    (function () {
      var s = 0, p = [];
      if (adminH >= 10) { s += 2; p.push("the team spends " + a.admin_hours + " a week on repetitive admin"); }
      if (adminH >= 20) s += 1;
      ["Data entry", "Scheduling", "Staff management"].forEach(function (d) { if (drain(d)) { s += 1; p.push(d.toLowerCase() + " is one of your biggest time-wasters"); } });
      if (is("goal_12m", "Save time / reduce costs")) s += 1;
      agent({ id: "ops", agent: "Operations Agent", department: "Operations", score: s, p: p,
        solution: "An AI operations agent that handles repetitive admin: data entry, job cards, document generation, onboarding checklists and task routing.",
        how: "Connects your email, forms, accounting and job tools; moves data between them and creates the documents and tasks your team does by hand today.",
        benefit: "Your team spends its hours on customers, not copy-paste.",
        h: [adminH * 0.2, adminH * 0.4],
        ha: "Assumes 20–40% of the ~" + adminH + " hrs/week of repetitive admin you reported can be automated.",
        rev: "" });
    })();

    // Reporting Agent
    (function () {
      var s = 0, p = [];
      if (is("reporting", "Manual spreadsheets")) { s += 2; p.push("reports are built manually in spreadsheets"); }
      if (is("reporting", "No regular reporting")) { s += 3; p.push("there is no regular business reporting"); }
      if (drain("Reporting")) { s += 2; p.push("reporting is one of your biggest time-wasters"); }
      if (is("goal_12m", "Better visibility & reporting")) s += 2;
      var man = is("reporting", "Manual spreadsheets");
      agent({ id: "rep", agent: "Reporting Agent", department: "Management", score: s, p: p,
        solution: "An AI reporting agent that pulls numbers from your CRM, accounts, ads and WhatsApp into one automatic dashboard and weekly summary.",
        how: "Scheduled data pulls, a live dashboard and a plain-English report delivered to WhatsApp or email.",
        benefit: "Decisions based on real numbers, without building spreadsheets.",
        h: man ? [2, 4] : [0.5, 1.5],
        ha: man ? "Assumes 2–4 hrs/week currently spent compiling spreadsheets (your answer: manual spreadsheets)." : "You don't report regularly today, so the main gain is visibility; time estimate reflects occasional manual checks.",
        rev: "" });
    })();

    // QA Agent
    (function () {
      var s = 0, p = [];
      if (E >= 6) { s += 1; p.push("a team of " + a.employees + " is hard to quality-check manually"); }
      if (E >= 21) s += 1;
      if (is("response_time", "Longer / inconsistent")) { s += 1; p.push("response times are inconsistent"); }
      if (is("goal_12m", "Better customer experience")) s += 1;
      agent({ id: "qa", agent: "QA Agent", department: "Operations", score: s, p: p,
        solution: "An AI QA agent that reviews calls, chats and job reports against your standards and flags issues early.",
        how: "Scores every conversation or job record, highlights complaints and missed steps, and sends a daily exceptions list.",
        benefit: "Consistent service quality without a manager listening to every call.",
        h: E >= 21 ? [2, 5] : [1, 2],
        ha: "Assumes " + (E >= 21 ? "2–5" : "1–2") + " hrs/week currently spent spot-checking conversations and work for a team of " + (a.employees || "your size") + ".",
        rev: "" });
    })();

    // Management / CEO Brief Agent
    (function () {
      var s = 0, p = [];
      if (leader && E >= 6) { s += 2; p.push("as " + a.role + " of a " + a.employees + " team you chase updates across people and systems"); }
      if (is("reporting", "No regular reporting")) s += 1;
      if (drain("Staff management")) { s += 1; p.push("staff management takes up a lot of your time"); }
      if (is("goal_12m", "Scale without hiring")) { s += 1; p.push("your goal is to scale without hiring"); }
      if (is("goal_12m", "Better visibility & reporting")) { s += 2; p.push("your 12-month goal is better visibility"); }
      agent({ id: "ceo", agent: "Management / CEO Brief Agent", department: "Management", score: s, p: p,
        solution: "A daily AI CEO brief: leads, sales, cash, service issues and team tasks in one WhatsApp message every morning.",
        how: "Reads from your CRM, accounting, inbox and other agents, then summarises what needs your attention today.",
        benefit: "Run the business from one message instead of ten dashboards.",
        h: [1, 2],
        ha: "Assumes 10–20 min a day currently spent chasing updates from people and systems.",
        rev: "" });
    })();

    // rank
    A.sort(function (x, y) { return y.score - x.score; });
    var picked = A.filter(function (x) { return x.score >= 3; }).slice(0, 6);
    if (picked.length < 3) picked = A.filter(function (x) { return x.score > 0; }).slice(0, 3);
    if (picked.length < 3) picked = A.slice(0, 3);
    picked.forEach(function (x, i) {
      x.priority = i < 2 ? 1 : i < 4 ? 2 : 3;
      if (!x.p.length) x.p.push("based on your goals, this is a natural next step once the foundations are in place");
    });

    var lo = 0, hi = 0;
    var recs = picked.map(function (x) {
      var hl = round5(x.h[0]), hh = Math.max(round5(x.h[1]), hl);
      lo += hl; hi += hh;
      var prob = x.p.slice(0, 3).join("; ");
      return { agent: x.agent, department: x.department, priority: x.priority, score: x.score,
        problem: prob.charAt(0).toUpperCase() + prob.slice(1) + ".", solution: x.solution, how: x.how, benefit: x.benefit,
        hours: fmtH(hl, hh), hoursAssumption: x.ha, revenue: x.rev || "" };
    });
    var depts = {};
    recs.forEach(function (r) { (depts[r.department] = depts[r.department] || []).push(r.agent); });
    var team = [];
    ["Sales", "Marketing", "Customer Service", "Operations", "Management"].forEach(function (d) {
      (depts[d] || []).forEach(function (ag) { team.push({ department: d, agent: ag, count: 1 }); });
    });
    var readiness = (is("ai_use", "AI built into our workflows")) ? "Advanced" :
      (is("ai_use", "Some AI tools in the business") || has("tools", "Zapier / Make") || is("wa_business", "WhatsApp API / automation")) ? "Developing" : "Early";
    var totalTop = picked.reduce(function (s, x) { return s + x.score; }, 0);
    var score = { opportunityIndex: Math.min(100, Math.round(25 + totalTop * 1.6)), readiness: readiness, hoursLow: round5(lo), hoursHigh: round5(hi), opportunities: recs.length,
      budget: a.budget || "", timeline: a.timeline || "", auditVersion: "short-30" };
    A.forEach(function (x) { score["agent_" + x.id] = x.score; });
    return { recommendations: recs, team: team, score: score };
  }

  /* ---------- submit ---------- */
  function cleanAnswers() {
    var out = {};
    STAGES.forEach(function (s, si) {
      if (si === 0) return;
      s.qs.forEach(function (q) {
        if (!visible(q, state.answers)) return;
        var v = state.answers[q.id];
        if (v == null || v === "" || (Array.isArray(v) && !v.length)) return;
        out[q.id] = typeof v === "string" ? v.trim().slice(0, 500) : v;
      });
    });
    return out;
  }

  var busy = false;
  function submit() {
    if (busy) return;
    busy = true;
    var a = state.answers, result = analyse(a);
    var t = A.readTracking() || tracking;
    var payload = {
      firstName: (a.firstName || "").trim(), lastName: (a.lastName || "").trim(), company: (a.company || "").trim(),
      email: (a.email || "").trim(), phone: (a.phone || "").trim(), role: a.role || "", website: (a.website || "").trim(),
      industry: a.industry || "", answers: cleanAnswers(), score: result.score, recommendations: result.recommendations,
      recommendedAgents: result.team, consent: a.consent === true, consentText: CONSENT_TEXT,
      tracking: { source: t.source || "", campaign: t.campaign || "", event: t.event || "", qr_source: t.qr_source || "", utm_source: t.utm_source || "", utm_medium: t.utm_medium || "", utm_campaign: t.utm_campaign || "", utm_term: t.utm_term || "", utm_content: t.utm_content || "", referrer: t.referrer || "" },
      elapsedMs: Math.min(Date.now() - (state.startedAt || Date.now()), 86400000), hp: state.hp || ""
    };
    renderBusy();
    var ctrl = typeof AbortController !== "undefined" ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 25000);
    fetch(CFG.apiUrl, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload), signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { return r.json().catch(function () { return { ok: false, error: "Unexpected server response (" + r.status + ")." }; }); })
      .then(function (res) {
        clearTimeout(timer); busy = false;
        if (!res || !res.ok || !res.reference) throw new Error((res && res.error) || "Could not save your audit.");
        var saved = { reference: res.reference, id: res.id, firstName: payload.firstName, company: payload.company, result: result, at: new Date().toISOString() };
        try { localStorage.setItem(RESULT, JSON.stringify(saved)); localStorage.removeItem(STORE); } catch (e) {}
        renderResults(saved);
      })
      .catch(function (err) {
        clearTimeout(timer); busy = false;
        renderError(err && err.name === "AbortError" ? "The connection timed out." : (err && err.message) || "Network error.");
      });
  }

  function renderBusy() {
    navbar.hidden = true;
    setProgress(96);
    $("stage-name").textContent = "Analysing"; $("stage-count").textContent = "Almost done";
    app.innerHTML = '<div class="center-screen fade-in"><div><div class="spinner" aria-hidden="true"></div><h2>Building your AI plan…</h2><p class="sub" style="margin-top:8px;">Analysing your answers and saving your audit securely.</p></div></div>';
    window.scrollTo(0, 0);
  }

  function renderError(msg) {
    navbar.hidden = true;
    var a = state.answers;
    var wa = A.wa("Hi Billy. I'm " + (a.firstName || "") + " from " + (a.company || "my business") + ". I tried to submit the AI AutoTech Business Audit but it didn't go through. Can you help?");
    app.innerHTML = '<div class="center-screen fade-in"><div style="width:100%;"><h2>We couldn\'t save your audit</h2><p class="alert" style="margin:16px 0; text-align:left;">' + esc(msg) + ' Your answers are still saved on this device.</p><div class="cta-stack"><button type="button" class="btn btn-primary" id="retry">Try again</button><a class="btn btn-wa" href="' + wa + '" target="_blank" rel="noopener">WhatsApp AI AutoTech</a><button type="button" class="btn btn-ghost" id="edit">Review my answers</button></div></div></div>';
    $("retry").addEventListener("click", submit);
    $("edit").addEventListener("click", function () { renderStage(); window.scrollTo(0, 0); });
  }

  function renderResults(saved) {
    var r = saved.result, ref = saved.reference, first = saved.firstName || "", company = saved.company || "your business";
    navbar.hidden = true;
    document.body.classList.add("is-results");
    setProgress(100);
    $("stage-name").textContent = "Your AI audit"; $("stage-count").textContent = "Complete ✓";
    var discuss = A.wa("Hi Billy. I'm " + first + " from " + company + ". I've completed the AI AutoTech Business Audit (ref " + ref + ") and I'd like to discuss my recommended AI team.");
    var book = CFG.bookingUrl ? CFG.bookingUrl : A.wa("Hi Billy. I'm " + first + " from " + company + ". I'd like to book my AI strategy session. My AI audit reference is " + ref + ".");
    // Our own /book/ page shows the audit reference to copy into the Google booking form.
    if (CFG.bookingUrl && /^(https:\/\/aiautotech\.co\.za)?\/book\/?(?:[?#]|$)/.test(CFG.bookingUrl) && ref) {
      book = CFG.bookingUrl.split("#")[0] + (CFG.bookingUrl.indexOf("?") >= 0 ? "&" : "?") + "ref=" + encodeURIComponent(ref);
    }
    var s = r.score;
    var opps = r.recommendations.map(function (x, i) {
      return '<article class="opp"><div class="opp-head"><span class="opp-rank">' + (i + 1) + '</span><div><span class="tiny">Priority ' + x.priority + " · " + esc(x.department) + "</span><h3>" + esc(x.agent) + "</h3></div></div><dl>" +
        '<div><dt>Problem detected</dt><dd class="problem">' + esc(x.problem) + "</dd></div>" +
        "<div><dt>Recommended solution</dt><dd>" + esc(x.solution) + "</dd></div>" +
        "<div><dt>How it works</dt><dd>" + esc(x.how) + "</dd></div>" +
        "<div><dt>Operational benefit</dt><dd>" + esc(x.benefit) + "</dd></div></dl>" +
        '<div class="est"><span class="badge-est">Estimate</span><b>' + esc(x.hours) + ' saved</b><span class="tiny">' + esc(x.hoursAssumption) + "</span>" +
        (x.revenue ? '<p style="margin-top:10px;"><span class="badge-est">Estimate</span><b>Revenue opportunity</b></p><span class="tiny">' + esc(x.revenue) + "</span>" : "") + "</div></article>";
    }).join("");
    var depts = {};
    r.team.forEach(function (t) { (depts[t.department] = depts[t.department] || []).push(t); });
    var team = Object.keys(depts).map(function (d) {
      return '<div class="team-dept"><h4>' + esc(d) + "</h4><ul>" + depts[d].map(function (t) { return "<li><b>" + t.count + " ×</b> " + esc(t.agent) + "</li>"; }).join("") + "</ul></div>";
    }).join("");
    var phases = [[1, "Weeks 1–2"], [2, "Weeks 3–6"], [3, "Month 2–3"]].map(function (p) {
      var items = r.recommendations.filter(function (x) { return x.priority === p[0]; });
      if (!items.length) return "";
      return '<div class="phase"><div class="p">Priority ' + p[0] + "<small>" + p[1] + "</small></div><ul>" + items.map(function (x) { return "<li>" + esc(x.agent) + "</li>"; }).join("") + "</ul></div>";
    }).join("");

    app.innerHTML = '<section class="fade-in" style="padding-top:22px;">' +
      '<p class="tagline">Your free AI business audit</p>' +
      '<h1 style="font-size:clamp(1.7rem,7vw,2.4rem);margin-top:10px;">' + esc(first) + ", here's what AI could do for <span>" + esc(company) + "</span></h1>" +
      '<p style="margin-top:14px;"><span class="ref">Reference ' + esc(ref) + '</span></p><p class="small sub" style="margin-top:10px;">Your audit is saved. Billy will review it personally — quote this reference when you get in touch.</p>' +
      '<div class="stats" style="margin-top:18px;"><div class="stat"><strong>' + s.opportunities + '</strong><span>High-priority AI opportunities</span></div><div class="stat"><strong>' + s.hoursLow + "–" + s.hoursHigh + '</strong><span>Estimated hrs/week that could be saved*</span></div><div class="stat"><strong>' + r.team.length + '</strong><span>AI agents in your recommended team</span></div><div class="stat"><strong>' + esc(s.readiness) + '</strong><span>AI readiness level</span></div></div>' +
      '<div class="cta-stack" style="margin-top:18px;"><a class="btn btn-primary" id="cta-book" href="' + esc(book) + '" target="_blank" rel="noopener">Book my audit results call</a></div>' +
      (CFG.bookingUrl ? '<p class="tiny" style="margin-top:8px;">Free 30-minute Google Meet with Billy. When you book, enter your audit reference: <b>' + esc(ref) + '</b></p>' : '') +
      '</section>' +
      '<section style="margin-top:34px;"><p class="tagline">Highest priority AI opportunities</p><h2 style="margin:8px 0 14px;">Where AI fits your business</h2>' + opps + "</section>" +
      '<section style="margin-top:34px;"><p class="tagline">Your recommended AI team</p><h2 style="margin:8px 0 14px;">Your AI team, by department</h2><div class="team">' + team + "</div></section>" +
      '<section style="margin-top:34px;"><p class="tagline">Implementation order</p><h2 style="margin:8px 0 14px;">Suggested rollout</h2><div class="roadmap">' + phases + '</div><p class="small sub" style="margin-top:10px;">Start with Priority 1 to prove value fast, then layer on the rest.</p></section>' +
      '<section class="card" style="margin-top:34px;"><h2>Next step: your AI strategy session</h2><p class="sub" style="margin:8px 0 16px;">A free 30-minute session with Billy to turn this audit into a costed plan for ' + esc(company) + '.</p><div class="cta-stack">' +
      '<a class="btn btn-primary" id="cta-book-2" href="' + esc(book) + '" target="_blank" rel="noopener">Book my audit results call</a>' +
      '<a class="btn btn-wa" id="cta-wa" href="' + esc(discuss) + '" target="_blank" rel="noopener" aria-label="Discuss my AI audit on WhatsApp">WhatsApp AI AutoTech</a>' +
      '<a class="btn btn-ghost" id="cta-site" href="' + esc(CFG.siteUrl) + '">Explore AI AutoTech</a></div></section>' +
      '<p class="disclaimer" style="margin-top:18px;">*All time and revenue figures are estimates calculated from the answers you gave, using the assumptions shown under each item. They are indicative only, not guaranteed results; some agents overlap, so totals are not additive in every case. We confirm real numbers with you before any work starts.</p>' +
      '<p style="margin-top:18px;text-align:center;"><button type="button" class="btn btn-ghost" id="restart" style="min-height:44px;font-size:.78rem;">Start a new audit</button></p>';
    $("restart").addEventListener("click", function () {
      if (!confirm("Start a new audit? Your saved result stays in AI AutoTech's records.")) return;
      try { localStorage.removeItem(RESULT); localStorage.removeItem(STORE); } catch (e) {}
      state = { stage: 0, answers: {}, startedAt: Date.now() }; renderStage(); window.scrollTo(0, 0);
    });
    window.scrollTo(0, 0);
  }

  /* ---------- boot ---------- */
  var prior = null;
  try { prior = JSON.parse(localStorage.getItem(RESULT) || "null"); } catch (e) {}
  if (prior && prior.reference && prior.result && !/[?&]new=1/.test(location.search)) renderResults(prior);
  else { if (/[?&]new=1/.test(location.search)) { try { localStorage.removeItem(RESULT); } catch (e) {} } renderStage(); }

  window.__AAT_AUDIT__ = { analyse: analyse, stages: STAGES };
})();
