#!/usr/bin/env python3
"""Build Alien Party Bingo printable: how-to + 10 unique cards + caller sheet.
Preview-only generator for conspiraparty.com. US Letter, vintage cream style.
"""
from __future__ import annotations

import random
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "printables" / "alien-party-bingo.pdf"
FONT_DIR = ROOT / "assets" / "fonts"
LOGO = ROOT / "assets" / "img" / "logo-concept-c-print.png"
LOGO_FALLBACK = ROOT / "assets" / "img" / "logo-concept-c.png"

pdfmetrics.registerFont(TTFont("Anton", str(FONT_DIR / "Anton-Regular.ttf")))
pdfmetrics.registerFont(TTFont("SpecialElite", str(FONT_DIR / "SpecialElite-Regular.ttf")))

PAPER = HexColor("#f4f0e8")
PAPER2 = HexColor("#ebe4d4")
INK = HexColor("#0b0b0b")
RED = HexColor("#e11d26")
MUTED = HexColor("#6e6a63")
LINE = HexColor("#2a2a2a")

# Family-friendly alien / UFO / conspiracy squares (no QAnon, no real politicians)
SQUARES = [
    "UFO sighting",
    "Tin foil hat",
    "Area 51",
    "Probe joke",
    "Crop circle",
    '"I want to believe"',
    "Men in black",
    "Abduction story",
    "Little green men",
    "Government cover-up",
    "Flying saucer",
    "Roswell",
    "Weird light",
    "Classified file",
    "Trust no one",
    "Beam me up",
    "Bigfoot cameo",
    "Alien selfie",
    "Moon landing",
    "Missing time",
    "Close encounter",
    "Black helicopter",
    "Redacted docs",
    "Glow stick",
    "Space cake",
    "Green snack",
    "Star map",
    "Signal jammer",
    "Conspiracy board",
    "Red string",
    '"They\'re watching"',
    "Silver jumpsuit",
    "Antenna headband",
    "Strange static",
    "Midnight sighting",
    "Bermuda Triangle",
    '"The truth is out there"',
    "Crash debris",
    "Secret bunker",
    "Glow-in-the-dark",
]

assert len(SQUARES) >= 24

W, H = letter  # 612 x 792
MARGIN = 0.5 * inch


def draw_paper_bg(c: canvas.Canvas) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # subtle kraft edge band
    c.setFillColor(PAPER2)
    c.rect(0, 0, W, 18, fill=1, stroke=0)
    c.rect(0, H - 18, W, 18, fill=1, stroke=0)


def draw_header_logo(c: canvas.Canvas, y_top: float, width: float = 160) -> float:
    """Draw concept C wordmark centered (print-safe black). Returns y below logo."""
    logo = LOGO if LOGO.exists() else LOGO_FALLBACK
    if logo.exists():
        from PIL import Image as _Image
        iw, ih = _Image.open(logo).size
        aspect = ih / iw
        h = width * aspect
        x = (W - width) / 2
        c.drawImage(
            str(logo),
            x,
            y_top - h,
            width=width,
            height=h,
            mask="auto",
            preserveAspectRatio=True,
        )
        return y_top - h - 4
    return y_top


def draw_site_footer(c: canvas.Canvas, page_label: str = "") -> None:
    c.setFillColor(MUTED)
    c.setFont("SpecialElite", 8)
    left = "conspiraparty.com  ·  free printable  ·  personal use"
    c.drawString(MARGIN, 28, left)
    if page_label:
        c.drawRightString(W - MARGIN, 28, page_label)


def wrap_centered(c: canvas.Canvas, text: str, x: float, y: float, font: str, size: float, max_w: float, leading: float | None = None) -> float:
    """Draw centered wrapped text; return y of last baseline."""
    leading = leading or size * 1.25
    c.setFont(font, size)
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for i, line in enumerate(lines):
        c.drawCentredString(x, y - i * leading, line)
    return y - (len(lines) - 1) * leading


def fit_cell_text(c: canvas.Canvas, text: str, max_w: float, max_h: float) -> tuple[str, float, list[str]]:
    """Pick font size and wrap so text fits in cell. Returns (font, size, lines)."""
    for size in (11, 10, 9, 8, 7.5, 7, 6.5, 6):
        leading = size * 1.15
        words = text.split()
        lines: list[str] = []
        cur = ""
        c.setFont("SpecialElite", size)
        for w in words:
            trial = (cur + " " + w).strip()
            if c.stringWidth(trial, "SpecialElite", size) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        if len(lines) * leading <= max_h and all(
            c.stringWidth(ln, "SpecialElite", size) <= max_w for ln in lines
        ):
            return "SpecialElite", size, lines
    # fallback: single line truncated
    return "SpecialElite", 6, [text[:18] + "…"]


def draw_bingo_grid(
    c: canvas.Canvas,
    cells: list[str],
    left: float,
    bottom: float,
    size: float,
    free_label: str = "FREE",
) -> None:
    """Draw 5x5 grid. cells is 24 strings (center is FREE)."""
    n = 5
    cell = size / n
    # outer border
    c.setStrokeColor(INK)
    c.setLineWidth(2.2)
    c.rect(left, bottom, size, size, fill=0, stroke=1)
    c.setLineWidth(0.9)
    for i in range(1, n):
        c.line(left + i * cell, bottom, left + i * cell, bottom + size)
        c.line(left, bottom + i * cell, left + size, bottom + i * cell)

    idx = 0
    for row in range(n):
        for col in range(n):
            cx = left + col * cell + cell / 2
            cy = bottom + (n - 1 - row) * cell + cell / 2
            if row == 2 and col == 2:
                # FREE center
                c.setFillColor(RED)
                pad = 3
                c.rect(
                    left + col * cell + pad,
                    bottom + (n - 1 - row) * cell + pad,
                    cell - 2 * pad,
                    cell - 2 * pad,
                    fill=1,
                    stroke=0,
                )
                c.setFillColor(white)
                c.setFont("Anton", 14)
                c.drawCentredString(cx, cy - 4, free_label)
            else:
                text = cells[idx]
                idx += 1
                max_w = cell - 10
                max_h = cell - 12
                font, fsize, lines = fit_cell_text(c, text, max_w, max_h)
                leading = fsize * 1.15
                total_h = (len(lines) - 1) * leading
                c.setFillColor(INK)
                c.setFont(font, fsize)
                start_y = cy + total_h / 2 - fsize * 0.3
                for i, ln in enumerate(lines):
                    c.drawCentredString(cx, start_y - i * leading, ln)


def make_card_cells(rng: random.Random) -> list[str]:
    pool = SQUARES[:]
    rng.shuffle(pool)
    return pool[:24]


def page_how_to(c: canvas.Canvas) -> None:
    draw_paper_bg(c)
    y = H - 40
    y = draw_header_logo(c, y, width=180)
    y -= 8

    c.setFillColor(INK)
    c.setFont("Anton", 36)
    c.drawCentredString(W / 2, y, "ALIEN PARTY BINGO")
    y -= 22
    c.setFillColor(RED)
    c.setFont("SpecialElite", 11)
    c.drawCentredString(W / 2, y, "How to Play  ·  10 unique cards + caller sheet")
    y -= 18

    # red rule
    c.setStrokeColor(RED)
    c.setLineWidth(2)
    c.line(MARGIN + 40, y, W - MARGIN - 40, y)
    y -= 36

    rules = [
        (
            "1",
            "Give each guest their own card; middle square is FREE.",
        ),
        (
            "2",
            "Host cuts out the caller squares, drops them in a bowl, draws one at a time and reads it out; mark it if you have it.",
        ),
        (
            "3",
            "First to 5 in a row (across, down or diagonal) yells 'COVER-UP!' and wins.",
        ),
    ]

    box_left = MARGIN + 28
    box_w = W - 2 * MARGIN - 56
    for num, text in rules:
        # number badge
        c.setFillColor(RED)
        c.circle(box_left + 14, y - 6, 12, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Anton", 14)
        c.drawCentredString(box_left + 14, y - 11, num)

        c.setFillColor(INK)
        c.setFont("SpecialElite", 12)
        # wrap text to the right of badge
        text_x = box_left + 36
        max_w = box_w - 36
        words = text.split()
        lines: list[str] = []
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if c.stringWidth(trial, "SpecialElite", 12) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for i, ln in enumerate(lines):
            c.drawString(text_x, y - 4 - i * 16, ln)
        y -= 16 * len(lines) + 28

    # Party version callout
    y -= 8
    c.setFillColor(PAPER2)
    c.setStrokeColor(RED)
    c.setLineWidth(1.5)
    box_h = 110
    c.roundRect(box_left, y - box_h, box_w, box_h, 8, fill=1, stroke=1)
    c.setFillColor(RED)
    c.setFont("Anton", 14)
    c.drawString(box_left + 16, y - 24, "PARTY VERSION (NO CALLER)")
    c.setFillColor(INK)
    c.setFont("SpecialElite", 11)
    party = (
        "Mark a square when it actually happens at the party, "
        "like someone saying 'Area 51' or putting on a tin foil hat."
    )
    words = party.split()
    lines = []
    cur = ""
    max_w = box_w - 32
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, "SpecialElite", 11) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for i, ln in enumerate(lines):
        c.drawString(box_left + 16, y - 48 - i * 15, ln)

    y = y - box_h - 36
    c.setFillColor(MUTED)
    c.setFont("SpecialElite", 10)
    tips = [
        "Print on US Letter. Cardstock feels extra classified.",
        "Print one card per guest from the 10 unique cards inside.",
        "Caller sheet is at the back — print, cut out the squares, bowl ready.",
    ]
    for t in tips:
        c.drawCentredString(W / 2, y, t)
        y -= 16

    # CLASSIFIED stamp vibe
    c.saveState()
    c.setStrokeColor(RED)
    c.setFillColor(Color(0.88, 0.11, 0.15, alpha=0.12))
    c.setLineWidth(2.5)
    c.translate(W / 2 + 160, H / 2 + 40)
    c.rotate(18)
    c.setFont("Anton", 22)
    c.setFillColor(Color(0.88, 0.11, 0.15, alpha=0.55))
    c.drawCentredString(0, 0, "CLASSIFIED")
    c.setStrokeColor(Color(0.88, 0.11, 0.15, alpha=0.55))
    c.rect(-70, -8, 140, 28, fill=0, stroke=1)
    c.restoreState()

    draw_site_footer(c, "1 / how to play")
    c.showPage()


def page_card(c: canvas.Canvas, card_num: int, cells: list[str], total_pages: int) -> None:
    draw_paper_bg(c)
    y = H - 32
    y = draw_header_logo(c, y, width=120)
    y -= 2

    c.setFillColor(INK)
    c.setFont("Anton", 26)
    c.drawCentredString(W / 2, y, "ALIEN PARTY BINGO")
    y -= 14
    c.setFillColor(RED)
    c.setFont("SpecialElite", 9)
    c.drawCentredString(W / 2, y, f"Card {card_num} of 10  ·  conspiraparty.com")
    y -= 10

    # CLASSIFIED corner stamp
    c.saveState()
    c.setFillColor(Color(0.88, 0.11, 0.15, alpha=0.85))
    c.setFont("Anton", 9)
    c.translate(W - MARGIN - 50, H - 55)
    c.rotate(12)
    c.drawCentredString(0, 0, "CLASSIFIED")
    c.setStrokeColor(Color(0.88, 0.11, 0.15, alpha=0.85))
    c.setLineWidth(1.2)
    c.rect(-38, -4, 76, 16, fill=0, stroke=1)
    c.restoreState()

    grid_size = min(W - 2 * MARGIN - 20, y - 70)
    left = (W - grid_size) / 2
    bottom = 58
    # nudge if needed
    if bottom + grid_size > y - 8:
        grid_size = y - 8 - bottom
        left = (W - grid_size) / 2

    draw_bingo_grid(c, cells, left, bottom, grid_size)

    c.setFillColor(MUTED)
    c.setFont("SpecialElite", 8)
    c.drawCentredString(
        W / 2,
        42,
        "5 in a row → yell COVER-UP!   ·   FREE center square",
    )
    draw_site_footer(c, f"{card_num + 1} / card {card_num}")
    c.showPage()


def page_caller(c: canvas.Canvas, start_page: int) -> int:
    """Caller sheet with all squares as cut-out tiles. Returns pages used."""
    tiles = SQUARES[:]
    # layout: title + grid of cut-out tiles
    cols, rows_per_page = 4, 8
    per_page = cols * rows_per_page
    pages_needed = (len(tiles) + per_page - 1) // per_page
    page_i = 0
    for p in range(pages_needed):
        draw_paper_bg(c)
        y = H - 36
        y = draw_header_logo(c, y, width=130)
        y -= 2
        c.setFillColor(INK)
        c.setFont("Anton", 24)
        c.drawCentredString(W / 2, y, "CALLER SHEET")
        y -= 14
        c.setFillColor(RED)
        c.setFont("SpecialElite", 9)
        subtitle = "Cut out the squares. Drop them in a bowl. Draw & read one at a time."
        if pages_needed > 1:
            subtitle += f"  ({p + 1}/{pages_needed})"
        c.drawCentredString(W / 2, y, subtitle)
        y -= 18

        chunk = tiles[p * per_page : (p + 1) * per_page]
        # tile grid
        grid_left = MARGIN + 10
        grid_right = W - MARGIN - 10
        grid_top = y
        grid_bottom = 50
        avail_w = grid_right - grid_left
        avail_h = grid_top - grid_bottom
        tile_w = avail_w / cols
        tile_h = avail_h / rows_per_page

        c.setStrokeColor(INK)
        c.setDash(1, 2)
        c.setLineWidth(0.7)
        for i, text in enumerate(chunk):
            row = i // cols
            col = i % cols
            x = grid_left + col * tile_w
            ty = grid_top - (row + 1) * tile_h
            c.setDash(1, 2)
            c.setStrokeColor(MUTED)
            c.rect(x + 2, ty + 2, tile_w - 4, tile_h - 4, fill=0, stroke=1)
            c.setDash()
            # text
            max_w = tile_w - 12
            max_h = tile_h - 12
            font, fsize, lines = fit_cell_text(c, text, max_w, max_h)
            leading = fsize * 1.15
            total_h = (len(lines) - 1) * leading
            cx = x + tile_w / 2
            cy = ty + tile_h / 2
            c.setFillColor(INK)
            c.setFont(font, fsize)
            start_y = cy + total_h / 2 - fsize * 0.3
            for li, ln in enumerate(lines):
                c.drawCentredString(cx, start_y - li * leading, ln)

        c.setDash()
        draw_site_footer(c, f"{start_page + page_i} / caller")
        c.showPage()
        page_i += 1
    return page_i


def build() -> Path:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(42)  # reproducible unique cards
    cards = [make_card_cells(rng) for _ in range(10)]
    # ensure uniqueness of arrangements
    sigs = {tuple(c) for c in cards}
    assert len(sigs) == 10, "cards not unique"

    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle("Alien Party Bingo — Conspiraparty")
    c.setAuthor("Conspiraparty")
    c.setSubject("Free printable alien party bingo: 10 unique cards + caller sheet")

    page_how_to(c)
    for i, cells in enumerate(cards, start=1):
        page_card(c, i, cells, total_pages=0)
    # caller pages start after how-to + 10 cards
    page_caller(c, start_page=12)

    c.save()
    return OUT


if __name__ == "__main__":
    path = build()
    import pypdf

    r = pypdf.PdfReader(str(path))
    print(f"Wrote {path} ({len(r.pages)} pages, {path.stat().st_size} bytes)")
