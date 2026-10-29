/* =============================================================================
   ETSY LISTING URLS — single edit spot for new-etsy-items packs
   Used by index.html Shop the Kits (data-etsy-pending) when packs are pending.
   Thanksgiving cards: https://www.etsy.com/listing/4605936572/conspiracy-thanksgiving-table-cards
   Road trip packs removed from site (listings deactivated on Etsy).
   ============================================================================= */
window.ETSY_PENDING_URLS = {};
(function () {
  var map = window.ETSY_PENDING_URLS || {};
  document.querySelectorAll("[data-etsy-pending]").forEach(function (el) {
    var key = el.getAttribute("data-etsy-pending");
    if (key && map[key]) el.setAttribute("href", map[key]);
  });
})();
