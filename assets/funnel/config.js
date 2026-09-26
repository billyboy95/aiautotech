/* AI AutoTech event funnel config. Public values only: never put secrets here. */
window.AAT_CONFIG = {
  apiUrl: "https://ai-autotech-crm.vercel.app/api/public/audit",
  whatsappNumber: "27646863803",
  // Set to a booking page (e.g. Calendly / Google Calendar appointment link) when ready.
  // While empty, "Book my AI strategy session" opens WhatsApp with a pre-filled booking message.
  // Branded booking page that embeds the Google Calendar appointment schedule; audit adds ?ref=<reference>.
  bookingUrl: "https://aiautotech.co.za/book/",
  siteUrl: "https://aiautotech.co.za/",
  eventDefaults: {
    source: "highlevel_event",
    campaign: "highlevel_2026",
    event: "highlevel",
    qr_source: "billy_phone_qr",
    utm_source: "highlevel",
    utm_medium: "qr",
    utm_campaign: "highlevel_event_2026"
  }
};
window.AAT = window.AAT || {};
window.AAT.wa = function (text) {
  return "https://wa.me/" + window.AAT_CONFIG.whatsappNumber + "?text=" + encodeURIComponent(text);
};
window.AAT.TRACK_KEYS = ["source","campaign","event","qr_source","utm_source","utm_medium","utm_campaign","utm_term","utm_content"];
window.AAT.readTracking = function () {
  var t = null;
  try { t = JSON.parse(localStorage.getItem("aat_tracking") || sessionStorage.getItem("aat_tracking") || "null"); } catch (e) {}
  return t;
};
window.AAT.saveTracking = function (t) {
  var s = JSON.stringify(t);
  try { localStorage.setItem("aat_tracking", s); } catch (e) {}
  try { sessionStorage.setItem("aat_tracking", s); } catch (e) {}
};
/* Merge real URL params over a base object. */
window.AAT.applyUrlParams = function (base) {
  var p = new URLSearchParams(location.search), out = Object.assign({}, base), changed = false;
  window.AAT.TRACK_KEYS.forEach(function (k) {
    var v = p.get(k);
    if (v) { out[k] = v.slice(0, 120); changed = true; }
  });
  return { tracking: out, changed: changed };
};
/* Persist campaign attribution (LinkedIn, Facebook, WhatsApp, QR, and any other utm_*).
   Internal links use utm_source=website and must not wipe a stored external campaign.
   /connect still forces the printed-QR event defaults via via=connect. */
window.AAT.externalReferrer = function () {
  var r = document.referrer || "";
  if (!r) return "";
  try {
    var host = new URL(r).hostname.replace(/^www\./, "");
    var me = location.hostname.replace(/^www\./, "");
    if (host && me && host === me) return "";
  } catch (e) {}
  return r.slice(0, 400);
};
window.AAT.captureCampaign = function (opts) {
  opts = opts || {};
  var qs = new URLSearchParams(location.search);
  var viaConnect = qs.get("via") === "connect";
  var urlHasTracking = window.AAT.TRACK_KEYS.some(function (k) { return !!qs.get(k); });
  var stored = window.AAT.readTracking();
  var ev = (window.AAT_CONFIG && window.AAT_CONFIG.eventDefaults) || {};
  var isEventUrl = !!ev.utm_source && qs.get("utm_source") === ev.utm_source;
  var incoming = qs.get("source") || qs.get("utm_source") || "";
  var internalNav = urlHasTracking && (incoming === "" || incoming === "website");

  if (viaConnect) {
    var tracking = window.AAT.applyUrlParams(Object.assign({ utm_term: "", utm_content: "" }, ev)).tracking;
    var cref = "";
    try { cref = sessionStorage.getItem("aat_connect_ref") || ""; } catch (e) {}
    tracking.referrer = cref.slice(0, 400);
    tracking.landing = "/connect";
    tracking.captured_at = new Date().toISOString();
    window.AAT.saveTracking(tracking);
    return { tracking: tracking, viaConnect: true };
  }

  var storedExternal = stored && stored.source && stored.source !== "website" && stored.source !== "lead_magnet";
  if (storedExternal && !isEventUrl && (!urlHasTracking || internalNav)) {
    return { tracking: stored, viaConnect: false };
  }

  if (!stored || urlHasTracking || isEventUrl) {
    var base = isEventUrl
      ? Object.assign({ utm_term: "", utm_content: "" }, ev)
      : { source: "website", campaign: "", event: "", qr_source: "", utm_source: "", utm_medium: "", utm_campaign: "", utm_term: "", utm_content: "" };
    var next = window.AAT.applyUrlParams(base).tracking;
    if (!isEventUrl) {
      if (!qs.get("source") && qs.get("utm_source")) next.source = qs.get("utm_source").slice(0, 120);
      if (!qs.get("campaign") && qs.get("utm_campaign")) next.campaign = qs.get("utm_campaign").slice(0, 120);
    }
    var ref = window.AAT.externalReferrer();
    next.referrer = (ref || (stored && stored.referrer) || "").slice(0, 400);
    next.landing = (opts.landing || location.pathname || "").slice(0, 120);
    next.captured_at = new Date().toISOString();
    window.AAT.saveTracking(next);
    return { tracking: next, viaConnect: false };
  }

  return { tracking: stored, viaConnect: false };
};
