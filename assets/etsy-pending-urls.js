/* =============================================================================
   ETSY PENDING LISTING URLS — single edit spot for new-etsy-items packs
   Replace each TODO-ETSY-<slug> value with the live listing URL when ready.
   Used by index.html Shop the Kits + field-guides.html "Take it on the road".
   Thanksgiving cards are already live (not a placeholder).
   ============================================================================= */
window.ETSY_PENDING_URLS = {
  /* TODO-ETSY-road-trip-pack */
  "road-trip-pack": "https://www.etsy.com/listing/TODO-ETSY-road-trip-pack",
  /* TODO-ETSY-road-trip-west */
  "road-trip-west": "https://www.etsy.com/listing/TODO-ETSY-road-trip-west",
  /* TODO-ETSY-road-trip-southwest */
  "road-trip-southwest": "https://www.etsy.com/listing/TODO-ETSY-road-trip-southwest"
};
(function () {
  var map = window.ETSY_PENDING_URLS || {};
  document.querySelectorAll("[data-etsy-pending]").forEach(function (el) {
    var key = el.getAttribute("data-etsy-pending");
    if (key && map[key]) el.setAttribute("href", map[key]);
  });
})();
