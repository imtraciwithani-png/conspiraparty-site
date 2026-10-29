#!/usr/bin/env python3
"""Build Thanksgiving Table Conspiracy Cards printable (US Letter).

How-to page + ~24 cut-out cards in 4 tiers. Concept C print logo in footer
with generous space. conspiraparty.com on every page. Never say 'hand-cut'.
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "printables" / "thanksgiving-table-conspiracy-cards.pdf"
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
CREAM = HexColor("#f5eedc")

W, H = letter
MARGIN = 0.5 * inch

# Tiers: Mild Gravy → Medium Stuffing → Spicy Cranberry → Full Tinfoil
# Satire / theories people believe / jokes. Roast all sides. No slurs.
# Never state false claims about real people as fact.
CARDS: list[tuple[str, str, str]] = [
    # tier, title, prompt
    ("MILD GRAVY", "The Turkey Swap",
     "Casually ask who else thinks this turkey was switched at the last minute."),
    ("MILD GRAVY", "Canned Cranberry File",
     "Declare that real cranberry sauce is classified — the can is the cover story."),
    ("MILD GRAVY", "Plant at the Table",
     "Wonder aloud which relative is the government plant. Make eye contact with everyone."),
    ("MILD GRAVY", "Mashed Potato Cover-Up",
     "Suggest the mashed potatoes are hiding something. Dig carefully."),
    ("MILD GRAVY", "Green Bean Psyop",
     "Announce green bean casserole is a Midwest psyop. Ask who authorized it."),
    ("MILD GRAVY", "Big Butter Theory",
     "Claim pie crust was invented by Big Butter. Request a second slice as evidence."),
    ("MEDIUM STUFFING", "Birds Aren't Real",
     "Point at a window bird and whisper: charging station or spy drone?"),
    ("MEDIUM STUFFING", "Denver Airport Tunnel",
     "Ask if Aunt Carol's basement connects to the Denver Airport tunnels."),
    ("MEDIUM STUFFING", "Garage Moon Landing",
     "Suggest the moon landing was filmed in Uncle Rick's garage. Ask for the outtakes."),
    ("MEDIUM STUFFING", "Finland & This Casserole",
     "Finland doesn't exist — and neither does this casserole. Defend your claim for 30 seconds."),
    ("MEDIUM STUFFING", "Sock Warehouse",
     "Missing socks go to a warehouse in Nevada. Ask who has an alibi."),
    ("MEDIUM STUFFING", "Bigfoot Avoidance",
     "Bigfoot is avoiding THIS family specifically. Vote on why."),
    ("SPICY CRANBERRY", "Bipartisan Lizard Round",
     "Ask which politician is secretly a lizard — then require one name from EACH party."),
    ("SPICY CRANBERRY", "Deep State Group Chat",
     "Propose: what if the 'deep state' is just group chats that got out of hand?"),
    ("SPICY CRANBERRY", "Every Admin's Conspiracy",
     "Every administration says the last one was the conspiracy. Coincidence? Take a poll."),
    ("SPICY CRANBERRY", "The Other Side Is a Cult",
     "The only bipartisan agreement: the other side is in a cult. Ask for receipts, gently."),
    ("SPICY CRANBERRY", "Q Fanfic Theory",
     "What if Q was just a very committed fanfic author? Keep it as a joke — watch the room."),
    ("SPICY CRANBERRY", "Who the Swamp Drains For",
     "Ask who the real swamp drains for… then pass dessert before anyone answers."),
    ("FULL TINFOIL", "Gravy & Classified Docs",
     "Pass the gravy AND the classified documents. Toast to whatever 'they' redacted."),
    ("FULL TINFOIL", "Pre-Carve Drop Check",
     "Someone here checked a 'drop' before carving. Guess who without saying names."),
    ("FULL TINFOIL", "Turkey Timer Tracker",
     "Joke that the turkey timer is a tracking device — then watch who flinches."),
    ("FULL TINFOIL", "Stolen Midterms, Both Ways",
     "Ask if the midterms were 'stolen' — then immediately ask about BOTH sides' stolen claims."),
    ("FULL TINFOIL", "Narrative Weather",
     "Storms aren't weather — they're narrative weather. Then ask for the salt."),
    ("FULL TINFOIL", "Toast to 'They'",
     "Propose a toast to whatever 'they' don't want you to know. Watch everyone toast."),
]

assert len(CARDS) == 24

TIER_COLORS = {
    "MILD GRAVY": HexColor("#2f6b3a"),       # sage green
    "MEDIUM STUFFING": HexColor("#8a5a1a"),  # brown
    "SPICY CRANBERRY": HexColor("#b01e28"),  # red
    "FULL TINFOIL": HexColor("#1a1a1a"),     # black
}


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
        c.drawImage(
            str(logo), x, logo_bottom,
            width=logo_w, height=logo_h, mask="auto", preserveAspectRatio=True,
        )
    c.setFillColor(MUTED)
    c.setFont("SpecialElite", 8)
    c.drawString(MARGIN, fine_y, "conspiraparty.com  ·  free printable  ·  personal use")
    if page_label:
        c.drawRightString(W - MARGIN, fine_y, page_label)


def content_bottom() -> float:
    return 22 + 14 + 27 + 18  # ~81


def wrap_lines(c: canvas.Canvas, text: str, font: str, size: float, max_w: float) -> list[str]:
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
    return lines or [""]


def page_how_to(c: canvas.Canvas) -> None:
    draw_paper_bg(c)
    y = H - 56
    c.setFillColor(INK)
    c.setFont("Anton", 28)
    c.drawCentredString(W / 2, y, "THANKSGIVING TABLE")
    y -= 30
    c.setFont("Anton", 28)
    c.drawCentredString(W / 2, y, "CONSPIRACY CARDS")
    y -= 22
    c.setFillColor(RED)
    c.setFont("SpecialElite", 11)
    c.drawCentredString(W / 2, y, "How to Play  ·  24 cards in 4 chaos tiers")
    y -= 18
    c.setStrokeColor(RED)
    c.setLineWidth(2)
    c.line(MARGIN + 40, y, W - MARGIN - 40, y)
    y -= 32

    rules = [
        ("1", "Print on US Letter cardstock. Cut along the dashed lines into 24 cards."),
        ("2", "Shuffle. Guests draw one card and read it aloud — or whisper it to a co-conspirator."),
        ("3", "Tiers escalate: Mild Gravy → Medium Stuffing → Spicy Cranberry → Full Tinfoil."),
        ("4", "First person to get uninvited next year… loses? Wins? The Committee is undecided."),
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
        lines = wrap_lines(c, text, "SpecialElite", 11, box_w - 36)
        for i, ln in enumerate(lines):
            c.drawString(box_left + 36, y - 4 - i * 14, ln)
        y -= 14 * len(lines) + 22

    # Exit lines box
    y -= 4
    c.setFillColor(PAPER2)
    c.setStrokeColor(RED)
    c.setLineWidth(1.5)
    box_h = 118
    c.roundRect(box_left, y - box_h, box_w, box_h, 8, fill=1, stroke=1)
    c.setFillColor(RED)
    c.setFont("Anton", 13)
    c.drawString(box_left + 16, y - 22, "EXIT LINES (USE THESE)")
    c.setFillColor(INK)
    exits = [
        '"Just kidding — please pass the rolls."',
        '"This is satire. Also, pie."',
        '"I read it on a napkin. Unverified."',
        '"Question everything, especially me. Who wants coffee?"',
    ]
    yy = y - 42
    for e in exits:
        c.setFont("SpecialElite", 10)
        c.drawString(box_left + 16, yy, e)
        yy -= 16

    y = y - box_h - 28
    # Disclaimer
    c.setFillColor(MUTED)
    c.setFont("SpecialElite", 9)
    disc = (
        "Entertainment only. Satire that roasts every side. Cards are jokes and "
        "theories people believe — not factual claims about real people. No hate. No calls to harm. Pass the gravy."
    )
    for ln in wrap_lines(c, disc, "SpecialElite", 9, box_w):
        c.drawCentredString(W / 2, y, ln)
        y -= 12

    y -= 10
    c.setFillColor(INK)
    c.setFont("SpecialElite", 10)
    tips = [
        "Optional: deal Mild cards first; save Full Tinfoil for after dessert.",
        "Kids at the table? Stick to Mild Gravy + Medium Stuffing.",
        "More party chaos: conspiraparty.com party kit (code LEAKED20).",
    ]
    for t in tips:
        c.drawCentredString(W / 2, y, t)
        y -= 14

    # CLASSIFIED stamp
    c.saveState()
    c.translate(W / 2 + 160, 200)
    c.rotate(14)
    c.setFont("Anton", 18)
    c.setFillColor(Color(0.88, 0.11, 0.15, alpha=0.4))
    c.drawCentredString(0, 0, "CLASSIFIED")
    c.setStrokeColor(Color(0.88, 0.11, 0.15, alpha=0.4))
    c.setLineWidth(2)
    c.rect(-62, -7, 124, 22, fill=0, stroke=1)
    c.restoreState()

    draw_brand_footer(c, "1 / how to play")
    c.showPage()


def draw_card(
    c: canvas.Canvas,
    x: float, y: float, cw: float, ch: float,
    tier: str, title: str, prompt: str, num: int,
) -> None:
    # dashed cut border
    c.setStrokeColor(MUTED)
    c.setDash(3, 3)
    c.setLineWidth(0.8)
    c.rect(x, y, cw, ch, fill=0, stroke=1)
    c.setDash()

    pad = 8
    # tier badge
    color = TIER_COLORS[tier]
    c.setFillColor(color)
    c.roundRect(x + pad, y + ch - 22, cw - 2 * pad, 14, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Anton", 7)
    c.drawCentredString(x + cw / 2, y + ch - 18, tier)

    # card number
    c.setFillColor(MUTED)
    c.setFont("SpecialElite", 7)
    c.drawRightString(x + cw - pad, y + ch - 32, f"#{num:02d}")

    # title
    c.setFillColor(INK)
    c.setFont("Anton", 11)
    title_lines = wrap_lines(c, title.upper(), "Anton", 11, cw - 2 * pad - 4)
    ty = y + ch - 40
    for ln in title_lines[:2]:
        c.drawCentredString(x + cw / 2, ty, ln)
        ty -= 13

    # red rule
    c.setStrokeColor(RED)
    c.setLineWidth(1)
    c.line(x + pad + 4, ty - 2, x + cw - pad - 4, ty - 2)
    ty -= 14

    # prompt
    c.setFillColor(INK)
    prompt_lines = wrap_lines(c, prompt, "SpecialElite", 8, cw - 2 * pad - 4)
    for ln in prompt_lines[:6]:
        c.drawCentredString(x + cw / 2, ty, ln)
        ty -= 11

    # tiny site
    c.setFillColor(MUTED)
    c.setFont("SpecialElite", 6)
    c.drawCentredString(x + cw / 2, y + 8, "conspiraparty.com")


def page_cards(c: canvas.Canvas, cards: list[tuple[str, str, str]], start_num: int, page_label: str) -> None:
    """Draw up to 6 cards per page (2 cols x 3 rows)."""
    draw_paper_bg(c)
    y_top = H - 42
    c.setFillColor(INK)
    c.setFont("Anton", 16)
    c.drawCentredString(W / 2, y_top, "THANKSGIVING CONSPIRACY CARDS")
    c.setFillColor(RED)
    c.setFont("SpecialElite", 8)
    c.drawCentredString(W / 2, y_top - 14, "Cut along dashed lines  ·  Print on cardstock")

    bottom = content_bottom()
    grid_top = y_top - 28
    grid_h = grid_top - bottom
    cols, rows = 2, 3
    gap = 10
    cw = (W - 2 * MARGIN - gap) / cols
    ch = (grid_h - gap * (rows - 1)) / rows

    for i, (tier, title, prompt) in enumerate(cards):
        col = i % cols
        row = i // cols
        x = MARGIN + col * (cw + gap)
        y = grid_top - (row + 1) * ch - row * gap
        draw_card(c, x, y, cw, ch, tier, title, prompt, start_num + i)

    draw_brand_footer(c, page_label)
    c.showPage()


def build() -> Path:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle("Thanksgiving Table Conspiracy Cards — Conspiraparty")
    c.setAuthor("Conspiraparty")
    page_how_to(c)
    # 24 cards → 4 pages of 6
    for page_i in range(4):
        chunk = CARDS[page_i * 6:(page_i + 1) * 6]
        page_cards(c, chunk, start_num=page_i * 6 + 1, page_label=f"{page_i + 2} / cards")
    c.save()
    print(f"Wrote {OUT} ({5} pages, {len(CARDS)} cards)")
    return OUT


if __name__ == "__main__":
    build()
