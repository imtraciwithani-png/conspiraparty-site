/* =============================================================================
   ETSY LISTING URLS — single edit spot for new-etsy-items packs
   Used by index.html Shop the Kits + field-guides.html "Take it on the road".
   Thanksgiving cards: https://www.etsy.com/listing/4605936572/conspiracy-thanksgiving-table-cards
   ============================================================================= */
window.ETSY_PENDING_URLS = {
  "road-trip-pack": "https://www.etsy.com/listing/4605919469/suspicious-road-trip-pack-printable",
  "road-trip-west": "https://www.etsy.com/listing/4605920433/suspicious-west-road-trip-pack-printable",
  "road-trip-southwest": "https://www.etsy.com/listing/4605940094/suspicious-southwest-road-trip-pack"
};
(function () {
  var map = window.ETSY_PENDING_URLS || {};
  document.querySelectorAll("[data-etsy-pending]").forEach(function (el) {
    var key = el.getAttribute("data-etsy-pending");
    if (key && map[key]) el.setAttribute("href", map[key]);
  });
})();
