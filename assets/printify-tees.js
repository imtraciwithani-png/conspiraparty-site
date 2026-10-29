/* Wire Coming soon buttons from data/printify-tees.json.
   Fill a product's "url" in that file to unlock its buy button. */
(function () {
  var DATA = 'data/printify-tees.json';
  function unlock(card, url) {
    if (!card || !url) return;
    var btn = card.querySelector('[data-buy-url], a.btn.is-soon, a.btn.sm');
    if (!btn) return;
    btn.href = url;
    btn.setAttribute('data-buy-url', url);
    btn.removeAttribute('aria-disabled');
    btn.classList.remove('is-soon');
    btn.target = '_blank';
    btn.rel = 'noopener';
    btn.textContent = 'Buy on Printify';
  }
  fetch(DATA, { credentials: 'same-origin' })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (data) {
      if (!data || !data.products) return;
      data.products.forEach(function (p) {
        if (!p || !p.id || !p.url) return;
        var card = document.querySelector('.card[data-id="' + p.id + '"]');
        unlock(card, p.url);
      });
      var storeBtns = document.querySelectorAll('[data-printify-store]');
      if (data.storeUrl) {
        storeBtns.forEach(function (a) {
          a.href = data.storeUrl;
        });
      }
    })
    .catch(function () { /* keep Coming soon */ });
})();
