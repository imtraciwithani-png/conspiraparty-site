/* 2026 news bingo. No trackers. Marks stay in memory for this visit. */
(function (root, factory) {
  var api = factory();
  root.BingoGame = api;
  if (typeof module === "object" && module.exports) module.exports = api;
  if (typeof document !== "undefined") api.mount(document);
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  var FREE = "FREE";
  var DECKS = {
    weird: [
      "Cop in a shrub writes 74 tickets",
      "Sick gator is a pool float",
      "Do not chase the emu",
      "Teen lassos a runaway sheep",
      "Diapered monkey named McNugget",
      "Kid's AI python panics a town",
      "Trail cam catches a unicorn deer",
      "Wisconsin cat born with 29 toes",
      "Dog hangs eight clothespins",
      "Crying horse toy goes viral",
      "Mountain lion stuck between buildings",
      "Mushroom makes people see tiny humans",
      "Governor saves PB4WEGO plate",
      "Turkeys chase man into a car",
      "Press 2 for Spanish, hear English",
      "Trapped in a phone box ordering kebab",
      "Kangaroo jumps an eight-foot fence",
      "Family buys Hell for under $666K",
      "Live frog found in a salad bag",
      "Faceless dummy in the carpool lane",
      "Hits a fountain, keeps eating McDonald's",
      "Guard dog plays fetch with a burglar",
      "Steers with knees, butters a bagel",
      "USPS announces cryptid stamps"
    ],
    political: [
      "Trump wants New Mexico named New America",
      "Democrats win the House and Senate",
      "Hunters bait Alaska bears with doughnuts",
      "Norway answers Trump with scenic toilets",
      "Mamdani sworn in as New York mayor",
      "Trump posts that the moon is ours",
      "RFK Jr poses as Bond with a carrot",
      "Lake Ontario renamed Lake America",
      "Vance dresses as Dumbledore for Halloween",
      "U.S. forces capture Venezuela's Maduro",
      "Peru mayor race decided by coin toss",
      "Trump makes Oval Office a monument",
      "America marks its 250th birthday",
      "Councilman wears clown gear in meeting",
      "Lula wins a fourth term in Brazil",
      "White House posts Trump as Green Lantern",
      "Judge blocks Trump's triumphal arch",
      "Senator names elliptical Margaret Thatcher",
      "Greenland protests Trump annexation threats",
      "United States withdraws from the WHO",
      "Trump flyer uses a Democrat's photo",
      "Trump wants Canada to pay for smoke",
      "Bolsonaro son claims win for 58 minutes",
      "New START nuclear treaty expires"
    ]
  };
  var TITLES = {
    weird: "2026 Weird News Bingo",
    political: "2026 Political News Bingo"
  };

  function shuffle(list, rng) {
    var a = list.slice();
    var random = rng || Math.random;
    var i, j, tmp;
    for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(random() * (i + 1));
      tmp = a[i];
      a[i] = a[j];
      a[j] = tmp;
    }
    return a;
  }

  function layout(items) {
    if (!items || items.length !== 24) throw new Error("A card needs 24 squares");
    return items.slice(0, 12).concat([FREE]).concat(items.slice(12));
  }

  function lineDefs() {
    var defs = [];
    var r, c;
    for (r = 0; r < 5; r++) {
      defs.push([0, 1, 2, 3, 4].map(function (col) { return r * 5 + col; }));
    }
    for (c = 0; c < 5; c++) {
      defs.push([0, 1, 2, 3, 4].map(function (row) { return row * 5 + c; }));
    }
    defs.push([0, 6, 12, 18, 24]);
    defs.push([4, 8, 12, 16, 20]);
    return defs;
  }

  function winningLines(marked) {
    return lineDefs().filter(function (idxs) {
      return idxs.every(function (i) { return !!marked[i]; });
    });
  }

  function markedCount(marked) {
    var n = 0;
    var i;
    for (i = 0; i < 25; i++) {
      if (i !== 12 && marked[i]) n++;
    }
    return n;
  }

  function shareLine(n) {
    return "I got " + n + " of 24 — how many did you get? conspiraparty.com/bingo.html";
  }

  function mount(doc) {
    var root = doc.getElementById("bingo-app");
    if (!root) return;
    var state = {
      deck: "weird",
      order: { weird: DECKS.weird.slice(), political: DECKS.political.slice() },
      marked: { weird: blankMarks(), political: blankMarks() },
      hadBingo: { weird: false, political: false }
    };

    function blankMarks() {
      var m = [];
      var i;
      for (i = 0; i < 25; i++) m.push(i === 12);
      return m;
    }

    var tabs = root.querySelectorAll("[data-deck]");
    var grid = root.querySelector("[data-grid]");
    var title = root.querySelector("[data-card-title]");
    var countEl = root.querySelector("[data-count]");
    var shareText = root.querySelector("[data-share-line]");
    var celebrate = root.querySelector("[data-celebrate]");
    var live = root.querySelector("[data-live]");
    var shareBtn = root.querySelector("[data-share-score]");
    var randomBtn = root.querySelector("[data-randomize]");

    function render(focusLabel) {
      var cells = layout(state.order[state.deck]);
      var marked = state.marked[state.deck];
      var wins = winningLines(marked);
      var winSet = {};
      wins.forEach(function (line) {
        line.forEach(function (i) { winSet[i] = true; });
      });
      title.textContent = TITLES[state.deck];
      grid.textContent = "";
      cells.forEach(function (label, i) {
        var el;
        if (label === FREE) {
          el = doc.createElement("div");
          el.className = "sq free";
          el.innerHTML = "<strong>FREE SPACE</strong><span>Totally Real News</span>";
          el.setAttribute("aria-label", "Free space, already marked");
        } else {
          el = doc.createElement("button");
          el.type = "button";
          el.className = "sq";
          el.textContent = label;
          el.setAttribute("aria-pressed", marked[i] ? "true" : "false");
          el.addEventListener("click", function () {
            marked[i] = !marked[i];
            render(label);
          });
        }
        if (marked[i]) el.classList.add("is-on");
        if (winSet[i]) el.classList.add("is-line");
        grid.appendChild(el);
      });
      var n = markedCount(marked);
      var line = shareLine(n);
      countEl.textContent = String(n);
      shareText.textContent = line;
      var bingo = wins.length > 0;
      celebrate.hidden = !bingo;
      if (bingo && !state.hadBingo[state.deck]) {
        celebrate.classList.remove("pop");
        void celebrate.offsetWidth;
        celebrate.classList.add("pop");
        if (live) live.textContent = "Bingo. " + line;
      } else if (!bingo && state.hadBingo[state.deck] && live) {
        live.textContent = "Bingo cleared. " + n + " of 24 marked.";
      }
      state.hadBingo[state.deck] = bingo;
      tabs.forEach(function (tab) {
        var on = tab.getAttribute("data-deck") === state.deck;
        tab.setAttribute("aria-selected", on ? "true" : "false");
        tab.classList.toggle("is-on", on);
      });
      if (focusLabel) {
        var buttons = grid.querySelectorAll("button");
        var b;
        for (b = 0; b < buttons.length; b++) {
          if (buttons[b].textContent === focusLabel) {
            buttons[b].focus();
            break;
          }
        }
      }
    }

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        state.deck = tab.getAttribute("data-deck");
        render();
      });
    });

    randomBtn.addEventListener("click", function () {
      state.order[state.deck] = shuffle(DECKS[state.deck]);
      state.marked[state.deck] = blankMarks();
      state.hadBingo[state.deck] = false;
      if (live) live.textContent = "New " + TITLES[state.deck] + " card. Marks cleared.";
      render();
      state.hadBingo[state.deck] = false;
    });

    shareBtn.addEventListener("click", function () {
      var text = shareLine(markedCount(state.marked[state.deck]));
      var url = "https://conspiraparty.com/bingo.html";
      function copied() {
        shareBtn.textContent = "Copied";
        if (live) live.textContent = "Copied the share line.";
        setTimeout(function () { shareBtn.textContent = "Share your score"; }, 1600);
      }
      function fallback() {
        var area = doc.createElement("textarea");
        area.value = text;
        area.setAttribute("readonly", "");
        area.style.position = "fixed";
        area.style.left = "-999px";
        doc.body.appendChild(area);
        area.select();
        try { doc.execCommand("copy"); copied(); }
        catch (err) { if (live) live.textContent = text; }
        doc.body.removeChild(area);
      }
      if (navigator.share) {
        navigator.share({ title: TITLES[state.deck], text: text, url: url }).catch(function (err) {
          if (err && err.name === "AbortError") return;
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(copied).catch(fallback);
          } else fallback();
        });
        return;
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(copied).catch(fallback);
      } else fallback();
    });

    render();
    state.hadBingo.weird = false;
    state.hadBingo.political = false;
  }

  return {
    FREE: FREE,
    DECKS: DECKS,
    TITLES: TITLES,
    shuffle: shuffle,
    layout: layout,
    winningLines: winningLines,
    markedCount: markedCount,
    shareLine: shareLine,
    mount: mount
  };
});
