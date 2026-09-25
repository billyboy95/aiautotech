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
