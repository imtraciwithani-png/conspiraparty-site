(function(){
  function canNativeShare(){
    return typeof navigator !== 'undefined' && typeof navigator.share === 'function'
      && (window.matchMedia('(max-width:720px)').matches || /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent||''));
  }
  function rootFrom(el){
    return el.closest('[data-share-url]') || el.closest('.share-box') || el.closest('.shareable') || el.closest('.tee-card') || el.closest('.news-card') || el.closest('.card') || el.closest('article');
  }
  function shareUrl(root){
    if(!root) return location.href;
    return root.getAttribute('data-share-url') || (root.id ? (location.origin + location.pathname.replace(/\/[^/]*$/,'/') + (location.pathname.split('/').pop()||'') + '#' + root.id) : location.href);
  }
  function shareText(root){
    if(!root) return document.title;
    return root.getAttribute('data-share-text') || document.title;
  }
  document.addEventListener('click', function(e){
    var shareBtn = e.target.closest('[data-share]');
    if(shareBtn){
      e.preventDefault();
      e.stopPropagation();
      var root = rootFrom(shareBtn);
      var box = shareBtn.closest('.share-box') || (root && root.querySelector('.share-box'));
      var url = (box && box.getAttribute('data-share-url')) || shareUrl(root);
      var text = (box && box.getAttribute('data-share-text')) || shareText(root);
      if(canNativeShare()){
        navigator.share({ title: document.title, text: text, url: url }).catch(function(){});
        return;
      }
      var links = box && box.querySelector('.share-links');
      if(links){ links.hidden = !links.hidden; }
      return;
    }
    var copyBtn = e.target.closest('[data-copy]');
    if(copyBtn){
      e.preventDefault();
      e.stopPropagation();
      var root = rootFrom(copyBtn);
      var box = copyBtn.closest('.share-box') || (root && root.querySelector('.share-box'));
      var url = (box && box.getAttribute('data-share-url')) || shareUrl(root);
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
