#!/usr/bin/env python3
"""Build Election Night Bingo printable: how-to + 10 unique cards + caller sheet.
Silly watch-party bingo. Roasts media tropes & party vibes, all sides evenly.
No candidate attacks, no verdicts. US Letter, vintage cream style.
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
OUT = ROOT / "printables" / "election-night-bingo.pdf"
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

# Watch-party tropes only — roast the night, not candidates. Even-handed.
SQUARES = [
    '"Too close to call"',
    "Map flashes red",
    "Map flashes blue",
    "Pundit says historic",
    "Someone mutes the TV",
    "Chip bowl emptied",
    "Phone refresh spiral",
    '"Wait for the West"',
    "Swing-state graphic",
    "Channel flip",
    "Victory speech tease",
    "Concession tease",
    '"It\'s not over yet"',
    "Pizza arrives",
    "Graph goes sideways",
    "Exit poll mention",
    "Yells at the screen",
    '"Remember 2000?"',
    "Still counting…",
    "County flips color",
    'Anchor: "nail-biter"',
    "Foil hat joke",
    "Champagne too early",
    '"I told you so"',
    "Polling surprise",
    "Split-screen fight",
    "Chyrons go wild",
    "Group chat explodes",
    '"This timeline"',
    "Someone leaves early",
    "Someone falls asleep",
    "Prediction flipped",
    "Third-party cameo",
    "Write-in joke",
    '"The algorithms"',
    "Someone cites a meme",
    "Voter turnout graphic",
    "Early voting shoutout",
    "Mail ballot mention",
    "Recount rumored",
]

assert len(SQUARES) >= 24

W, H = letter
MARGIN = 0.5 * inch


def draw_paper_bg(c: canvas.Canvas) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(PAPER2)
    c.rect(0, 0, W, 18, fill=1, stroke=0)
    c.rect(0, H - 18, W, 18, fill=1, stroke=0)


def draw_brand_footer(c: canvas.Canvas, page_label: str = "") -> None:
    logo = LOGO if LOGO.exists() else LOGO_FALLBACK
    logo_w = 88.0
    logo_h = 0.0
    if logo.exists():
        from PIL import Image as _Image
        iw, ih = _Image.open(logo).size
        logo_h = logo_w * (ih / iw)
    fine_y = 22
    logo_bottom = fine_y + 14
    if logo.exists():
        x = (W - logo_w) / 2
        c.drawImage(str(logo), x, logo_bottom, width=logo_w, height=logo_h, mask="auto", preserveAspectRatio=True)
    c.setFillColor(MUTED)
    c.setFont("SpecialElite", 8)
    c.drawString(MARGIN, fine_y, "free printable  ·  personal use  ·  conspiraparty.com")
    if page_label:
        c.drawRightString(W - MARGIN, fine_y, page_label)


def content_bottom() -> float:
    return 22 + 14 + 27 + 16


def fit_cell_text(c: canvas.Canvas, text: str, max_w: float, max_h: float) -> tuple[str, float, list[str]]:
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
        if len(lines) * leading <= max_h and all(c.stringWidth(ln, "SpecialElite", size) <= max_w for ln in lines):
            return "SpecialElite", size, lines
    return "SpecialElite", 6, [text[:18] + "…"]


def draw_bingo_grid(c: canvas.Canvas, cells: list[str], left: float, bottom: float, size: float, free_label: str = "I VOTED") -> None:
    n = 5
    cell = size / n
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
                c.setFillColor(RED)
                pad = 3
                c.rect(left + col * cell + pad, bottom + (n - 1 - row) * cell + pad, cell - 2 * pad, cell - 2 * pad, fill=1, stroke=0)
                c.setFillColor(white)
                # Fit "I VOTED" in center
                for fsize in (13, 12, 11, 10):
                    if c.stringWidth(free_label, "Anton", fsize) <= cell - 10:
                        c.setFont("Anton", fsize)
                        break
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
    y = H - 56
    c.setFillColor(INK)
    c.setFont("Anton", 34)
    c.drawCentredString(W / 2, y, "ELECTION NIGHT BINGO")
    y -= 22
    c.setFillColor(RED)
    c.setFont("SpecialElite", 11)
    c.drawCentredString(W / 2, y, "How to Play  ·  10 unique cards + caller sheet")
    y -= 20
    c.setStrokeColor(RED)
    c.setLineWidth(2)
    c.line(MARGIN + 40, y, W - MARGIN - 40, y)
    y -= 32

    rules = [
        ("1", "Give each guest a card. Middle square is FREE: I VOTED."),
        ("2", "Host cuts out caller squares, drops them in a bowl, draws & reads one at a time. Mark it if you have it."),
        ("3", "First to 5 in a row (across, down or diagonal) yells 'CALLED IT!' and wins."),
    ]
    box_left = MARGIN + 28
    box_w = W - 2 * MARGIN - 56
    for num, text in rules:
        c.setFillColor(RED)
        c.circle(box_left + 14, y - 6, 12, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Anton", 14)
        c.drawCentredString(box_left + 14, y - 11, num)
        c.setFillColor(INK)
        c.setFont("SpecialElite", 12)
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
        y -= 16 * len(lines) + 26

    y -= 6
    c.setFillColor(PAPER2)
    c.setStrokeColor(RED)
    c.setLineWidth(1.5)
    box_h = 118
    c.roundRect(box_left, y - box_h, box_w, box_h, 8, fill=1, stroke=1)
    c.setFillColor(RED)
    c.setFont("Anton", 13)
    c.drawString(box_left + 16, y - 22, "WATCH-PARTY VERSION (NO CALLER)")
    c.setFillColor(INK)
    c.setFont("SpecialElite", 11)
    party = (
        "Mark a square when it actually happens on TV or in the room — "
        "someone yells at the screen, the map flips, champagne opens too early. "
        "Satire that roasts every side. Entertainment only."
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
        c.drawString(box_left + 16, y - 44 - i * 15, ln)

    y = y - box_h - 30
    c.setFillColor(MUTED)
    c.setFont("SpecialElite", 10)
    for t in [
        "Print on US Letter. Cardstock feels extra classified.",
        "No real candidate attacks. No verdicts. Just vibes.",
        "Caller sheet is at the back — print, cut, bowl ready.",
    ]:
        c.drawCentredString(W / 2, y, t)
        y -= 15

    c.saveState()
    c.setLineWidth(2.5)
    c.translate(W / 2 + 150, 200)
    c.rotate(16)
    c.setFont("Anton", 18)
    c.setFillColor(Color(0.88, 0.11, 0.15, alpha=0.45))
    c.drawCentredString(0, 0, "CLASSIFIED")
    c.setStrokeColor(Color(0.88, 0.11, 0.15, alpha=0.45))
    c.rect(-68, -8, 136, 26, fill=0, stroke=1)
    c.restoreState()

    draw_brand_footer(c, "1 / how to play")
    c.showPage()


def page_card(c: canvas.Canvas, card_num: int, cells: list[str]) -> None:
    draw_paper_bg(c)
    y = H - 48
    c.setFillColor(INK)
    c.setFont("Anton", 24)
    c.drawCentredString(W / 2, y, "ELECTION NIGHT BINGO")
    y -= 16
    c.setFillColor(RED)
    c.setFont("SpecialElite", 9)
    c.drawCentredString(W / 2, y, f"Card {card_num} of 10")
    y -= 14

    c.saveState()
    c.setFillColor(Color(0.88, 0.11, 0.15, alpha=0.85))
    c.setFont("Anton", 9)
    c.translate(W - MARGIN - 48, H - 42)
    c.rotate(12)
    c.drawCentredString(0, 0, "CLASSIFIED")
    c.setStrokeColor(Color(0.88, 0.11, 0.15, alpha=0.85))
    c.setLineWidth(1.2)
    c.rect(-38, -4, 76, 16, fill=0, stroke=1)
    c.restoreState()

    bottom = content_bottom()
    grid_top = y - 8
    grid_size = min(W - 2 * MARGIN - 24, grid_top - bottom)
    left = (W - grid_size) / 2
    draw_bingo_grid(c, cells, left, bottom, grid_size)

    c.setFillColor(MUTED)
    c.setFont("SpecialElite", 8)
    c.drawCentredString(W / 2, bottom - 10, "5 in a row → yell CALLED IT!   ·   FREE = I VOTED")
    draw_brand_footer(c, f"{card_num + 1} / card {card_num}")
    c.showPage()


def page_caller(c: canvas.Canvas, start_page: int) -> int:
    tiles = SQUARES[:]
    cols, rows_per_page = 4, 8
    per_page = cols * rows_per_page
    pages_needed = (len(tiles) + per_page - 1) // per_page
    page_i = 0
    for p in range(pages_needed):
        draw_paper_bg(c)
        y = H - 48
        c.setFillColor(INK)
        c.setFont("Anton", 24)
        c.drawCentredString(W / 2, y, "CALLER SHEET")
        y -= 18
        c.setFillColor(RED)
        c.setFont("SpecialElite", 9)
        subtitle = "Cut out the squares. Drop them in a bowl. Draw & read one at a time."
        if pages_needed > 1:
            subtitle += f"  ({p + 1}/{pages_needed})"
        c.drawCentredString(W / 2, y, subtitle)
        y -= 22

        chunk = tiles[p * per_page : (p + 1) * per_page]
        grid_left = MARGIN + 10
        grid_right = W - MARGIN - 10
        grid_top = y
        grid_bottom = content_bottom()
        avail_w = grid_right - grid_left
        avail_h = grid_top - grid_bottom
        tile_w = avail_w / cols
        tile_h = avail_h / rows_per_page

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

        draw_brand_footer(c, f"{start_page + page_i} / caller")
        c.showPage()
        page_i += 1
    return page_i


def build() -> Path:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20261103)
    cards = [make_card_cells(rng) for _ in range(10)]
    assert len({tuple(c) for c in cards}) == 10

    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle("Election Night Bingo — Conspiraparty")
    c.setAuthor("Conspiraparty")
    c.setSubject("Free printable Election Night Bingo: 10 unique cards + caller sheet")

    page_how_to(c)
    for i, cells in enumerate(cards, start=1):
        page_card(c, i, cells)
    page_caller(c, start_page=12)
    c.save()
    return OUT


if __name__ == "__main__":
    path = build()
    import pypdf
    r = pypdf.PdfReader(str(path))
    print(f"Wrote {path} ({len(r.pages)} pages, {path.stat().st_size} bytes)")
