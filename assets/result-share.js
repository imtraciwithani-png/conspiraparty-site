/* Client-side result card and dare-style share links. Nothing is uploaded. */
(function (w) {
  function shareUrl(base, key) {
    var root = String(base || "").split("?")[0];
    return root + "?r=" + encodeURIComponent(key) + "&ref=share";
  }
  function dare(quiz, title, url) {
    return "Dare you. I got \u201c" + title + "\u201d on " + quiz + ". Bet you get something weirder. " + url;
  }
  function wrap(g, text, x, y, max, lh) {
    var words = String(text || "").split(/\s+/);
    var line = "";
    var yy = y;
    words.forEach(function (word) {
      var trial = line ? line + " " + word : word;
      if (g.measureText(trial).width > max && line) {
        g.fillText(line, x, yy);
        yy += lh;
        line = word;
      } else {
        line = trial;
      }
    });
    if (line) g.fillText(line, x, yy);
    return yy;
  }
  function paint(opts) {
    var c = document.createElement("canvas");
    c.width = 1080;
    c.height = 1350;
    var g = c.getContext("2d");
    g.fillStyle = "#f6f0e4";
    g.fillRect(0, 0, 1080, 1350);
    g.fillStyle = "#c8102e";
    g.fillRect(0, 0, 1080, 36);
    g.fillStyle = "#111";
    g.font = "700 40px system-ui, Segoe UI, sans-serif";
    wrap(g, opts.quiz || "Conspiraparty", 72, 140, 936, 52);
    g.font = "700 72px system-ui, Segoe UI, sans-serif";
    var y = wrap(g, opts.title || "", 72, 280, 936, 84);
    g.font = "36px system-ui, Segoe UI, sans-serif";
    wrap(g, opts.line || "", 72, y + 80, 936, 50);
    g.fillStyle = "#c8102e";
    g.fillRect(0, 1248, 1080, 102);
    g.fillStyle = "#fff";
    g.font = "700 36px system-ui, Segoe UI, sans-serif";
    g.fillText("conspiraparty.com", 72, 1312);
    var a = document.createElement("a");
    a.download = "conspiraparty-result.png";
    a.href = c.toDataURL("image/png");
    a.click();
  }
  function bind(el, href) {
    if (!el) return;
    if (el.tagName === "A") el.href = href;
  }
  function apply(opts) {
    var url = shareUrl(opts.base, opts.key);
    var text = dare(opts.quiz, opts.title, url);
    bind(opts.x, "https://x.com/intent/post?text=" + encodeURIComponent(text) + "&url=" + encodeURIComponent(url));
    bind(opts.sms, "sms:?&body=" + encodeURIComponent(text));
    bind(opts.wa, "https://wa.me/?text=" + encodeURIComponent(text));
    if (opts.copy) {
      opts.copy.onclick = function () {
        var btn = this;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(function () { btn.textContent = "Copied"; });
        } else {
          btn.textContent = url;
        }
      };
    }
    if (opts.save) {
      opts.save.onclick = function () { paint(opts); };
    }
    return { url: url, text: text };
  }
  w.CPResultShare = { shareUrl: shareUrl, dare: dare, paint: paint, apply: apply };
})(window);
