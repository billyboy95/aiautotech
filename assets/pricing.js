/* AI AutoTech AIOS price sheet — the only place public prices are defined.
   Approved 27 September 2026. published is false until Billy says these
   figures are a final public offer. Edit this file, then run:
   python3 _build/build.py
   Generated pages and the audit read window.AIOS_PRICING from here. */
window.AIOS_PRICING = {
  "published": false,
  "approvedOn": "2026-09-27",
  "currency": "ZAR",
  "vatIncluded": false,
  "short": "from R299/mo platform + agents from R699",
  "pill": "From R299/mo platform + agents from R699",
  "disclaimer": "Estimate only. ZAR, excl. VAT. Confirmed on your call. Not a final public offer until Billy publishes it.",
  "meta": "Estimate: from R299/mo platform + agents from R699, excl. VAT, confirmed on your call.",
  "positioning": "Competitive with HighLevel-class tools, with the emphasis on bigger output and results.",
  "platform": {
    "name": "Platform",
    "amountLabel": "R299",
    "amount": "299",
    "period": "/mo",
    "includes": "CRM, Lead Agent and a small computer-time pool."
  },
  "agents": [
    {"name": "Starter", "amountLabel": "R699", "amount": "699", "period": "/mo", "includes": "Computer hours included."},
    {"name": "Pro", "amountLabel": "R1,499", "amount": "1499", "period": "/mo", "includes": "Computer hours included."},
    {"name": "Always-On", "amountLabel": "R4,999", "amount": "4999", "period": "/mo", "includes": "Computer hours included."}
  ],
  "discounts": [
    {"label": "3 agents", "off": "10%"},
    {"label": "5 agents", "off": "15%"},
    {"label": "10+ agents", "off": "20%"}
  ],
  "extras": [
    {"name": "Message sends", "detail": "Billed at cost plus a markup. The markup is confirmed on your call."},
    {"name": "Computer-time top-up", "detail": "R799 for 10 hours."},
    {"name": "Premium models or BYOK", "detail": "Premium model use, or bring your own key. Quoted on the call."},
    {"name": "Quick Start setup", "detail": "R2,500 suggested."},
    {"name": "Team Setup", "detail": "R4,999 suggested."}
  ]
};
