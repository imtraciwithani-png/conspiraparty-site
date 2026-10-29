
(function(){
  var page = document.querySelector('.fg-page');
  if(!page) return;
  var slug = page.getAttribute('data-fg-slug') || 'guide';
  var key = 'cp-fg-' + slug;
  var boxes = Array.prototype.slice.call(document.querySelectorAll('[data-fg-check]'));
  var countEl = document.querySelector('[data-fg-count]');

  function load(){
    try{
      var raw = localStorage.getItem(key);
      var set = raw ? JSON.parse(raw) : [];
      if(!Array.isArray(set)) set = [];
      boxes.forEach(function(b){
        b.checked = set.indexOf(b.value) !== -1;
      });
      update();
    }catch(e){}
  }
  function save(){
    var set = boxes.filter(function(b){return b.checked}).map(function(b){return b.value});
    try{ localStorage.setItem(key, JSON.stringify(set)); }catch(e){}
    update();
  }
  function update(){
    var n = boxes.filter(function(b){return b.checked}).length;
    if(countEl) countEl.textContent = String(n);
  }
  boxes.forEach(function(b){ b.addEventListener('change', save); });
  var reset = document.querySelector('[data-fg-reset]');
  if(reset){
    reset.addEventListener('click', function(){
      boxes.forEach(function(b){ b.checked = false; });
      save();
    });
  }
  load();

})();
