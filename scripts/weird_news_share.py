#!/usr/bin/env python3
"""Per-story Weird News share pages + OG images."""
from __future__ import annotations

import html
import json
import sys
import time
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    Image = ImageDraw = ImageFont = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
SHARE_DIR = ROOT / "weird-news" / "s"
SHARE_OG_DIR = ROOT / "assets" / "og" / "weird-news"
SHARE_MAX_AGE_DAYS = 30
LOGO_PATH = ROOT / "assets" / "img" / "logo.png"
FONT_PATH = ROOT / "assets" / "fonts" / "Anton-Regular.ttf"


def _wrap_text(draw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    cur = words[0]
    for w in words[1:]:
        trial = f"{cur} {w}"
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def render_share_og_image(it: dict, slug: str) -> Path | None:
    if Image is None:
        print("WARNING: Pillow missing; skip OG image", file=sys.stderr)
        return None
    SHARE_OG_DIR.mkdir(parents=True, exist_ok=True)
    out = SHARE_OG_DIR / f"{slug}.jpg"
    W, H = 1200, 630
    bg, red = (11, 11, 11), (225, 29, 38)
    text_c, dim = (242, 239, 232), (184, 178, 166)
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 8], fill=red)
    if LOGO_PATH.exists():
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo_h = 70
        ratio = logo_h / logo.height
        logo = logo.resize((max(1, int(logo.width * ratio)), logo_h), Image.Resampling.LANCZOS)
        img.paste(logo, (48, 36), logo)
    try:
        font_tag = ImageFont.truetype(str(FONT_PATH), 28)
        font_h = ImageFont.truetype(str(FONT_PATH), 52)
        font_s = ImageFont.truetype(str(FONT_PATH), 28)
        font_f = ImageFont.truetype(str(FONT_PATH), 26)
    except Exception:
        font_tag = font_h = font_s = font_f = ImageFont.load_default()
    tag = (it.get("tag") or "Weird").upper()
    tw = int(draw.textlength(tag, font=font_tag)) + 28
    draw.rectangle([48, 128, 48 + tw, 166], fill=red)
    draw.text((62, 132), tag, font=font_tag, fill=(255, 255, 255))
    title = it["title"].upper()
    lines = _wrap_text(draw, title, font_h, W - 96)
    y = 186
    for line in lines[:5]:
        draw.text((48, y), line, font=font_h, fill=text_c)
        y += 58
    take = it.get("one_liner") or ""
    draw.text((48, min(y + 12, 470)), "CONSPIRAPARTY TAKE", font=font_s, fill=red)
    ty = min(y + 48, 510)
    for line in _wrap_text(draw, take, font_s, W - 96)[:2]:
        draw.text((48, ty), line, font=font_s, fill=dim)
        ty += 34
    draw.rectangle([0, H - 56, W, H], fill=(20, 20, 20))
    draw.rectangle([0, H - 56, 8, H], fill=red)
    draw.text((48, H - 42), "conspiraparty.com/weird-news", font=font_f, fill=text_c)
    img.save(out, "JPEG", quality=88, optimize=True)
    return out


def render_share_page(it: dict, slug: str) -> Path:
    SHARE_DIR.mkdir(parents=True, exist_ok=True)
    out = SHARE_DIR / f"{slug}.html"
    title = html.escape(it["title"])
    liner = html.escape(it["one_liner"])
    tag = html.escape(it["tag"])
    source = html.escape(it["source"])
    src_url = html.escape(it["url"], quote=True)
    canon = f"https://conspiraparty.com/weird-news/s/{slug}.html"
    og_img = f"https://conspiraparty.com/assets/og/weird-news/{slug}.jpg"
    anchor = f"https://conspiraparty.com/weird-news.html#story-{slug}"
    anchor_js = json.dumps(anchor)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Conspiraparty Weird News</title>
<meta name="description" content="{liner}">
<link rel="canonical" href="{html.escape(canon, quote=True)}">
<meta property="og:site_name" content="Conspiraparty">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{liner}">
<meta property="og:url" content="{html.escape(canon, quote=True)}">
<meta property="og:type" content="article">
<meta property="og:image" content="{html.escape(og_img, quote=True)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{liner}">
<meta name="twitter:image" content="{html.escape(og_img, quote=True)}">
<meta http-equiv="refresh" content="2;url={html.escape(anchor, quote=True)}">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="/assets/img/favicon-64.png">
<link rel="stylesheet" href="/assets/style.css">
<style>
.share-landing{{max-width:720px;margin:0 auto;padding:48px 24px}}
.share-landing h1{{font-size:clamp(1.6rem,5vw,2.4rem);margin:0 0 12px}}
.share-landing .take{{margin-top:18px;padding-top:14px;border-top:1px dashed rgba(255,255,255,.15)}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<main id="main" class="share-landing">
  <span style="display:inline-block;background:var(--red);color:#fff;padding:3px 8px;font-family:var(--font-display);letter-spacing:.06em;text-transform:uppercase;font-size:.75rem;margin-bottom:12px">{tag}</span>
  <h1>{title}</h1>
  <p style="color:var(--text-dim)">via {source}</p>
  <p class="take"><strong style="color:var(--red)">Conspiraparty take</strong> — {liner}</p>
  <p style="margin-top:28px">
    <a class="btn" href="{html.escape(anchor, quote=True)}">Open on Weird News</a>
    <a class="btn sm" href="{src_url}" target="_blank" rel="noopener noreferrer">Read the source</a>
  </p>
  <p style="margin-top:22px"><a class="btn sm x-follow-btn" href="https://x.com/conspiraparty" target="_blank" rel="noopener">Follow @conspiraparty on X</a></p>
</main>
<script>setTimeout(function(){{ location.replace({anchor_js}); }}, 1800);</script>
</body>
</html>
"""
    out.write_text(page, encoding="utf-8")
    return out


def write_share_pages(items: list[dict], story_slug) -> list[str]:
    slugs: list[str] = []
    for it in items:
        slug = story_slug(it)
        slugs.append(slug)
        render_share_og_image(it, slug)
        render_share_page(it, slug)
    return slugs


def prune_share_pages(keep_slugs: list[str]) -> int:
    keep = set(keep_slugs)
    cutoff = time.time() - SHARE_MAX_AGE_DAYS * 86400
    removed = 0
    for folder, suffix in ((SHARE_DIR, ".html"), (SHARE_OG_DIR, ".jpg")):
        if not folder.exists():
            continue
        for path in folder.iterdir():
            if not path.is_file() or path.suffix != suffix:
                continue
            if path.stem in keep:
                continue
            try:
                if path.stat().st_mtime >= cutoff:
                    continue
            except OSError:
                continue
            path.unlink(missing_ok=True)
            removed += 1
    return removed
