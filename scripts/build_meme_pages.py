#!/usr/bin/env python3
"""Build one static share page per Meme Lab meme.

Add a row to MEMES and run this script. It writes:
  m/<slug>.html
  assets/share/memes/<slug>.jpg          full meme, JPEG
  assets/share/memes/<slug>-1200x675.jpg  same meme fitted in a 1200x675 card
  assets/meme-presets.js                 maker lookup for preset vs custom text
and points each meme's X / Facebook / Pinterest links at its /m/ page.
"""
from html import escape
from pathlib import Path
from urllib.parse import quote

def q(value):
    return quote(value, safe="")

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://conspiraparty.com"
CREAM = (245, 239, 224)

# art id, slug, caption, top line, bottom line
MEMES = [
    ("meme-bigfoot-caught", "they-said-it-was-a-bear", "They said it was a bear. The bear declined to comment.", "THEY SAID IT WAS A BEAR.", "THE BEAR DECLINED TO COMMENT."),
    ("meme-facepalm-spy", "the-briefing-was-classified", "The briefing was classified. My face was not.", "THE BRIEFING WAS CLASSIFIED.", "MY FACE WAS NOT."),
    ("meme-mind-blown-alien", "i-came-for-the-dip", "I came for the dip. I stayed for the cover story.", "I CAME FOR THE DIP.", "I STAYED FOR THE COVER STORY."),
    ("meme-shocked-alien", "you-invited-how-many-pigeons", "You invited how many pigeons?", "YOU INVITED", "HOW MANY PIGEONS?"),
    ("meme-shrug-bigfoot", "blurry-on-purpose", "Blurry on purpose. It is a lifestyle.", "BLURRY ON PURPOSE.", "IT IS A LIFESTYLE."),
    ("meme-side-eye-pigeon", "i-work-for-the-crumbs", "I work for the crumbs.", "I WORK FOR", "THE CRUMBS."),
    ("meme-smug-nessie", "tourist-photo", "Tourist photo. I was the tourist.", "TOURIST PHOTO.", "I WAS THE TOURIST."),
    ("meme-string-board-guy", "it-is-all-connected", "It is all connected. Mostly by red string and snacks.", "IT IS ALL CONNECTED.", "MOSTLY BY RED STRING AND SNACKS."),
    ("meme-suspicious-cat", "i-have-seen-the-treat-jar", "I have seen the treat jar. I will not be taking questions.", "I HAVE SEEN THE TREAT JAR.", "I WILL NOT BE TAKING QUESTIONS."),
    ("meme-tea-frog", "the-pond-is-fine", "The pond is fine. I am the pond.", "THE POND IS FINE.", "I AM THE POND."),
]


def card_jpg(src: Path, full_out: Path, wide_out: Path):
    im = Image.open(src).convert("RGB")
    full_out.parent.mkdir(parents=True, exist_ok=True)
    im.save(full_out, "JPEG", quality=90, optimize=True, progressive=True)
    canvas = Image.new("RGB", (1200, 675), CREAM)
    scale = min(1200 / im.width, 675 / im.height)
    nw, nh = max(1, int(im.width * scale)), max(1, int(im.height * scale))
    fitted = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(fitted, ((1200 - nw) // 2, (675 - nh) // 2))
    canvas.save(wide_out, "JPEG", quality=90, optimize=True, progressive=True)
    return im.size


def page_html(slug, caption, full_name, wide_name, full_size):
    page = f"{SITE}/m/{slug}.html"
    full = f"{SITE}/assets/share/memes/{full_name}"
    wide = f"{SITE}/assets/share/memes/{wide_name}"
    cap = escape(caption, quote=True)
    x = escape(
        "https://x.com/intent/post?text=" + q(caption) + "&url=" + q(page),
        quote=True,
    )
    fb = escape("https://www.facebook.com/sharer/sharer.php?u=" + q(page), quote=True)
    pin = escape(
        "https://www.pinterest.com/pin/create/button/?url="
        + q(page)
        + "&media="
        + q(wide)
        + "&description="
        + q(caption),
        quote=True,
    )
    w, h = full_size
    return f"""<!doctype html>
<html lang="en"><head><meta name="p:domain_verify" content="b26c4f540597647634b6bc6353fd9f22"/>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cap} | Conspiraparty</title>
<meta name="description" content="{cap}">
<link rel="canonical" href="{page}">
<meta property="og:site_name" content="Conspiraparty">
<meta property="og:title" content="{cap}">
<meta property="og:description" content="{cap}">
<meta property="og:url" content="{page}">
<meta property="og:type" content="article">
<meta property="og:image" content="{wide}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="675">
<meta property="og:image:alt" content="{cap}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{cap}">
<meta name="twitter:description" content="{cap}">
<meta name="twitter:image" content="{wide}">
<meta name="twitter:image:alt" content="{cap}">
<meta name="theme-color" content="#111111">
<link rel="icon" href="../assets/img/favicon-64.png">
<link rel="stylesheet" href="../assets/style.css?v=kofi1">
<link rel="stylesheet" href="../assets/redesign.css?v=memepage1">
<link rel="stylesheet" href="../assets/share.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="promo">20% off the full printable kit with code <a href="https://ko-fi.com/s/e35cf6ce46" rel="noopener sponsored" target="_blank">LEAKED20</a> on Ko-fi and Etsy</div>
<header class="top"><div class="bar"><a class="logo" href="../index.html"><img src="../assets/img/logo.png" alt="Conspiraparty" width="220" height="70"></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button></div>
<nav class="main" id="nav" aria-label="Main"><ul><li><a href="../index.html">Home</a></li><li><a href="../party-kits.html">Party Kits</a></li><li><a href="../case-files.html">Case Files</a></li><li><a href="../memes.html">Meme Lab</a></li><li><a href="../gift-guide.html">Gift Guide</a></li><li><a href="../leak-it.html">Share</a></li></ul><ul class="occasion-nav"><li><a href="../thanksgiving-host.html">Thanksgiving</a></li><li><a href="../office-christmas-party.html">Office Christmas</a></li><li><a href="../white-elephant.html">White Elephant</a></li><li><a href="../gift-guide.html">Gift Guide</a></li></ul></nav>
</header>
<main id="main">
<section class="v2-cream v2-section"><div class="wrap center">
<h1>{cap}</h1>
<img class="meme-full" src="../assets/share/memes/{full_name}" alt="{cap}" width="{w}" height="{h}">
<p><a class="btn" href="../assets/share/memes/{full_name}" download>Download</a></p>
<p><a href="{x}" rel="noopener" target="_blank">Share on X</a> · <a href="{fb}" rel="noopener" target="_blank">Facebook</a> · <a href="{pin}" rel="noopener" target="_blank">Pinterest</a></p>
<p><a href="../memes.html">Make your own in Meme Lab</a></p>
</div></section>
</main>
<footer><div class="wrap">
<nav aria-label="Footer"><ul><li><a href="../index.html">Home</a></li><li><a href="../party-kits.html">Party Kits</a></li><li><a href="../case-files.html">Case Files</a></li><li><a href="../memes.html">Meme Lab</a></li><li><a href="../gift-guide.html">Gift Guide</a></li><li><a href="../gift-shop.html">Gift Shop</a></li><li><a href="../leak-it.html">Share</a></li><li><a href="../weird-news.html">Weird News</a></li><li><a href="../blog/index.html">Rabbit Holes</a></li><li><a href="../free-printables.html">Free Printables</a></li></ul></nav>
<p class="disclosure">As an Amazon Associate, Conspiraparty earns from qualifying purchases. Some links on this site are affiliate links, which means we may earn a small commission at no extra cost to you.</p>
<p class="art-disclosure">Illustrations made with AI assistance (Recraft) and edited by Traci.</p>
<p>All conspiracies on this site are for entertainment. Question everything, especially us. © 2026 Conspiraparty.com</p>
</div></footer>
<script src="../assets/site.js" defer></script>
<script data-goatcounter="https://conspiraparty.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body></html>
"""


def presets_js():
    rows = []
    for art, slug, _caption, top, bottom in MEMES:
        rows.append(
            "  {src:'assets/art/spot/%s-800.webp', slug:'%s', top:%s, bottom:%s}"
            % (art, slug, json_str(top), json_str(bottom))
        )
    return "window.MEME_PRESETS=[\n" + ",\n".join(rows) + "\n];\n"


def json_str(value):
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def patch_lab(by_caption):
    path = ROOT / "memes.html"
    text = path.read_text()
    for caption, slug in by_caption.items():
        page = f"{SITE}/m/{slug}.html"
        wide = f"{SITE}/assets/share/memes/{slug}-1200x675.jpg"
        old = escape(
            "https://x.com/intent/post?text="
            + quote(caption + " — conspiraparty.com", safe="?")
            + "&url="
            + q(SITE + "/memes.html"),
            quote=True,
        )
        x = escape(
            "https://x.com/intent/post?text=" + q(caption) + "&url=" + q(page),
            quote=True,
        )
        fb = escape("https://www.facebook.com/sharer/sharer.php?u=" + q(page), quote=True)
        pin = escape(
            "https://www.pinterest.com/pin/create/button/?url="
            + q(page)
            + "&media="
            + q(wide)
            + "&description="
            + q(caption),
            quote=True,
        )
        new = (
            f'<a href="{x}" rel="noopener" target="_blank">Share on X</a>'
            f' · <a href="{fb}" rel="noopener" target="_blank">Facebook</a>'
            f' · <a href="{pin}" rel="noopener" target="_blank">Pinterest</a>'
        )
        needle = f'<a href="{old}" rel="noopener" target="_blank">Share on X</a>'
        if needle not in text:
            raise SystemExit(f"share link not found for {caption}")
        text = text.replace(needle, new, 1)
    if 'src="assets/meme-presets.js"' not in text:
        text = text.replace(
            '<script defer src="assets/share.js"></script>',
            '<script src="assets/meme-presets.js"></script><script defer src="assets/share.js"></script>',
            1,
        )
    path.write_text(text)


def patch_sitemap(slugs):
    path = ROOT / "sitemap.xml"
    text = path.read_text()
    block = []
    for slug in slugs:
        loc = f"{SITE}/m/{slug}.html"
        if loc in text:
            continue
        img = f"{SITE}/assets/share/memes/{slug}-1200x675.jpg"
        block.append(
            f"  <url><loc>{loc}</loc><lastmod>2026-11-11</lastmod>"
            f"<image:image><image:loc>{img}</image:loc></image:image></url>"
        )
    if not block:
        return
    anchor = '  <url><loc>https://conspiraparty.com/memes.html</loc>'
    idx = text.find(anchor)
    if idx < 0:
        raise SystemExit("sitemap memes.html entry missing")
    line_end = text.find("\n", idx)
    text = text[: line_end + 1] + "\n".join(block) + "\n" + text[line_end + 1 :]
    path.write_text(text)


def main():
    out_dir = ROOT / "m"
    img_dir = ROOT / "assets" / "share" / "memes"
    out_dir.mkdir(exist_ok=True)
    by_caption = {}
    for art, slug, caption, _top, _bottom in MEMES:
        src = ROOT / "assets" / "art" / "spot" / f"{art}-card-800.webp"
        full_name = f"{slug}.jpg"
        wide_name = f"{slug}-1200x675.jpg"
        size = card_jpg(src, img_dir / full_name, img_dir / wide_name)
        (out_dir / f"{slug}.html").write_text(page_html(slug, caption, full_name, wide_name, size))
        by_caption[caption] = slug
        print(slug, size)
    (ROOT / "assets" / "meme-presets.js").write_text(presets_js())
    patch_lab(by_caption)
    patch_sitemap([slug for _a, slug, _c, _t, _b in MEMES])


if __name__ == "__main__":
    main()
