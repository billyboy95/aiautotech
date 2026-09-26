/* Capture utm_* and the external referrer on any marketing page, before a click
   overwrites the address with internal utm_source=website links. */
(function () {
  "use strict";
  if (!window.AAT || !window.AAT.captureCampaign) return;
  window.AAT.captureCampaign({ landing: location.pathname });
})();
