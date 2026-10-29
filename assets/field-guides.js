
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

  function canNativeShare(){
    return typeof navigator !== 'undefined' && typeof navigator.share === 'function'
      && (window.matchMedia('(max-width:720px)').matches || /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent||''));
  }
  document.addEventListener('click', function(e){
    var shareBtn = e.target.closest('[data-share]');
    if(shareBtn){
      var box = shareBtn.closest('.share-box');
      if(!box) return;
      var url = box.getAttribute('data-share-url') || location.href;
      var text = box.getAttribute('data-share-text') || document.title;
      if(canNativeShare()){
        navigator.share({ title: document.title, text: text, url: url }).catch(function(){});
        return;
      }
      var links = box.querySelector('.share-links');
      if(links) links.hidden = !links.hidden;
      return;
    }
    var copyBtn = e.target.closest('[data-copy]');
    if(copyBtn){
      var box = copyBtn.closest('.share-box');
      if(!box) return;
      var url = box.getAttribute('data-share-url') || location.href;
      var done = function(){
        copyBtn.classList.add('copied');
        copyBtn.textContent = 'Copied';
        setTimeout(function(){ copyBtn.classList.remove('copied'); copyBtn.textContent = 'Copy link'; }, 1600);
      };
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(url).then(done).catch(function(){ window.prompt('Copy link', url); });
      } else {
        window.prompt('Copy link', url);
      }
    }
  });
})();
