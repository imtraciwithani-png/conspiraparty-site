#!/usr/bin/env python3
"""Build remaining freebie PDFs + wallpapers for preview-freebies-batch."""
from __future__ import annotations
import random
from pathlib import Path
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts"
LOGO = ROOT / "assets" / "img" / "logo-concept-c-print.png"
LOGO_FALLBACK = ROOT / "assets" / "img" / "logo-concept-c.png"
pdfmetrics.registerFont(TTFont("Anton", str(FONT_DIR / "Anton-Regular.ttf")))
pdfmetrics.registerFont(TTFont("SpecialElite", str(FONT_DIR / "SpecialElite-Regular.ttf")))
PAPER, PAPER2 = HexColor("#f4f0e8"), HexColor("#ebe4d4")
INK, RED, MUTED = HexColor("#0b0b0b"), HexColor("#e11d26"), HexColor("#6e6a63")
W, H = letter
MARGIN = 0.5 * inch
ANTON = str(FONT_DIR / "Anton-Regular.ttf")
ELITE = str(FONT_DIR / "SpecialElite-Regular.ttf")

def draw_paper_bg(c):
    c.setFillColor(PAPER); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(PAPER2); c.rect(0,0,W,18,fill=1,stroke=0); c.rect(0,H-18,W,18,fill=1,stroke=0)

def draw_brand_footer(c, page_label=""):
    logo = LOGO if LOGO.exists() else LOGO_FALLBACK
    logo_w, logo_h = 88.0, 0.0
    if logo.exists():
        iw, ih = Image.open(logo).size
        logo_h = logo_w * (ih / iw)
        c.drawImage(str(logo), (W-logo_w)/2, 36, width=logo_w, height=logo_h, mask="auto", preserveAspectRatio=True)
    c.setFillColor(MUTED); c.setFont("SpecialElite", 8)
    c.drawString(MARGIN, 22, "conspiraparty.com  ·  free printable  ·  personal use")
    if page_label: c.drawRightString(W-MARGIN, 22, page_label)

def content_bottom(): return 81

def wrap_lines(c, text, font, size, max_w):
    c.setFont(font, size); words=text.split(); lines=[]; cur=""
    for w in words:
        trial=(cur+" "+w).strip()
        if c.stringWidth(trial, font, size) <= max_w: cur=trial
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines or [""]

# ---------- CHRISTMAS CARDS ----------
XMAS_CARDS = [
    ("MILD EGGNOG", "Santa's Surveillance Network", "Casually suggest NORAD tracks Santa because Santa IS the surveillance network."),
    ("MILD EGGNOG", "Cookie Chain of Custody", "Demand a chain of custody for the cookies. Who touched the plate? Take notes."),
    ("MILD EGGNOG", "Elf on the Shelf Is a Narc", "Announce the Elf is an informant. Ask who debriefed him last night."),
    ("MILD EGGNOG", "Wrapping Paper Black Budget", "Claim fancy wrapping paper is a black-budget psyop. Prefer brown kraft as cover."),
    ("MILD EGGNOG", "Fruitcake Cover Story", "Fruitcake is a cover story for something denser. Pass it left. Watch eyes."),
    ("MILD EGGNOG", "Reindeer GPS Spoof", "Rudolph's nose is a GPS spoof. Ask who benefits from the red glow."),
    ("MEDIUM TIDINGS", "Mall Santa Vetting", "Ask how Mall Santa cleared the background check. Request his file number."),
    ("MEDIUM TIDINGS", "North Pole Bunker", "Propose the North Pole is a bunker, not a village. Vote on the depth."),
    ("MEDIUM TIDINGS", "Stockings Are Dead Drops", "Stockings are dead drops. Guess which relative left the classified candy cane."),
    ("MEDIUM TIDINGS", "Caroling Frequency", "Carolers are broadcasting on a classified frequency. Hum along carefully."),
    ("MEDIUM TIDINGS", "Ugly Sweater Signal", "Ugly sweaters are signal flags. Decode the nearest pattern in 20 seconds."),
    ("MEDIUM TIDINGS", "Snow Day Narrative", "Snow days aren't weather — they're narrative weather. Request the salt."),
    ("SPICY MISTLETOE", "Nice List Algorithm", "The Nice List runs on an opaque algorithm. Demand transparency… then dessert."),
    ("SPICY MISTLETOE", "Both Parties' Holiday Card", "Every side claims the other ruined the holidays. Require one roast from EACH side."),
    ("SPICY MISTLETOE", "Secret Santa Leak", "Secret Santa leaked. Guess the mole without naming anyone. Then wink."),
    ("SPICY MISTLETOE", "Toy Supply Chain", "Toys are delayed by 'supply chain issues' again. Blame elves, logistics, or 'them'."),
    ("SPICY MISTLETOE", "Holiday Group Chat Coup", "The family group chat staged a soft coup. Who seized the admin rights?"),
    ("SPICY MISTLETOE", "Gift Receipt Redaction", "Gift receipts are redacted evidence. Ask what they don't want you returning."),
    ("FULL TINFOIL", "Chimney Portal Theory", "Chimneys are portals. Toast to whatever exits on December 26."),
    ("FULL TINFOIL", "Krampus Is HR", "Krampus works in holiday HR. Ask who filed the complaint."),
    ("FULL TINFOIL", "Yule Log Livestream", "The Yule log livestream is a calming psyop. Keep watching anyway."),
    ("FULL TINFOIL", "New Year Timeline Jump", "We jump timelines at midnight. Ask who's ready and who needs another cookie."),
    ("FULL TINFOIL", "Classified Hot Cocoa", "Pass the cocoa AND the classified documents. Sip suspiciously."),
    ("FULL TINFOIL", "Toast to 'They'", "Propose a toast to whatever 'they' redacted from the holiday specials."),
]
assert len(XMAS_CARDS)==24
TIER_COLORS = {
    "MILD EGGNOG": HexColor("#2f6b3a"),
    "MEDIUM TIDINGS": HexColor("#1a4d7a"),
    "SPICY MISTLETOE": HexColor("#b01e28"),
    "FULL TINFOIL": HexColor("#1a1a1a"),
}

def draw_card(c, x, y, cw, ch, tier, title, prompt, num):
    c.setStrokeColor(MUTED); c.setDash(3,3); c.setLineWidth(0.8)
    c.rect(x,y,cw,ch,fill=0,stroke=1); c.setDash()
    pad=8; color=TIER_COLORS[tier]
    c.setFillColor(color); c.roundRect(x+pad, y+ch-22, cw-2*pad, 14, 3, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Anton", 7); c.drawCentredString(x+cw/2, y+ch-18, tier)
    c.setFillColor(MUTED); c.setFont("SpecialElite", 7); c.drawRightString(x+cw-pad, y+ch-32, f"#{num:02d}")
    c.setFillColor(INK); c.setFont("Anton", 11)
    ty=y+ch-40
    for ln in wrap_lines(c, title.upper(), "Anton", 11, cw-2*pad-4)[:2]:
        c.drawCentredString(x+cw/2, ty, ln); ty-=13
    c.setStrokeColor(RED); c.setLineWidth(1); c.line(x+pad+4, ty-2, x+cw-pad-4, ty-2); ty-=14
    c.setFillColor(INK)
    for ln in wrap_lines(c, prompt, "SpecialElite", 8, cw-2*pad-4)[:6]:
        c.drawCentredString(x+cw/2, ty, ln); ty-=11
    c.setFillColor(MUTED); c.setFont("SpecialElite", 6); c.drawCentredString(x+cw/2, y+8, "conspiraparty.com")

def build_christmas():
    out = ROOT/"printables"/"christmas-conspiracy-cards.pdf"
    c = canvas.Canvas(str(out), pagesize=letter)
    c.setTitle("Christmas Conspiracy Cards — Conspiraparty"); c.setAuthor("Conspiraparty")
    draw_paper_bg(c); y=H-56
    c.setFillColor(INK); c.setFont("Anton", 28); c.drawCentredString(W/2,y,"CHRISTMAS CONSPIRACY"); y-=30
    c.setFont("Anton", 28); c.drawCentredString(W/2,y,"CARDS"); y-=22
    c.setFillColor(RED); c.setFont("SpecialElite", 11); c.drawCentredString(W/2,y,"How to Play  ·  24 cards in 4 chaos tiers"); y-=18
    c.setStrokeColor(RED); c.setLineWidth(2); c.line(MARGIN+40,y,W-MARGIN-40,y); y-=30
    box_left=MARGIN+28; box_w=W-2*MARGIN-56
    for num,text in [("1","Print on US Letter cardstock. Cut along the dashed lines into 24 cards."),
                     ("2","Shuffle. Guests draw one and read it aloud — or whisper it to a co-conspirator."),
                     ("3","Tiers escalate: Mild Eggnog → Medium Tidings → Spicy Mistletoe → Full Tinfoil."),
                     ("4","Save Full Tinfoil for after the cookies. Use an exit line. Pass the cocoa.")]:
        c.setFillColor(RED); c.circle(box_left+14,y-6,12,fill=1,stroke=0)
        c.setFillColor(white); c.setFont("Anton",14); c.drawCentredString(box_left+14,y-11,num)
        c.setFillColor(INK); lines=wrap_lines(c,text,"SpecialElite",11,box_w-36)
        for i,ln in enumerate(lines): c.drawString(box_left+36,y-4-i*14,ln)
        y -= 14*len(lines)+20
    c.setFillColor(PAPER2); c.setStrokeColor(RED); c.setLineWidth(1.5)
    box_h=100; c.roundRect(box_left,y-box_h,box_w,box_h,8,fill=1,stroke=1)
    c.setFillColor(RED); c.setFont("Anton",13); c.drawString(box_left+16,y-22,"EXIT LINES (USE THESE)")
    c.setFillColor(INK); c.setFont("SpecialElite",10)
    for i,e in enumerate(['"Just kidding — more eggnog?"','"This is satire. Also, pie."','"Question everything, especially me."']):
        c.drawString(box_left+16, y-44-i*16, e)
    y=y-box_h-24
    c.setFillColor(MUTED); c.setFont("SpecialElite",9)
    for ln in wrap_lines(c,"Family-friendly satire. Entertainment only. Roast the season, not real people.", "SpecialElite",9,box_w):
        c.drawCentredString(W/2,y,ln); y-=12
    draw_brand_footer(c,"1 / how to play"); c.showPage()
    for page_i in range(4):
        chunk=XMAS_CARDS[page_i*6:(page_i+1)*6]
        draw_paper_bg(c); y_top=H-42
        c.setFillColor(INK); c.setFont("Anton",16); c.drawCentredString(W/2,y_top,"CHRISTMAS CONSPIRACY CARDS")
        c.setFillColor(RED); c.setFont("SpecialElite",8); c.drawCentredString(W/2,y_top-14,"Cut along dashed lines  ·  Print on cardstock")
        bottom=content_bottom(); grid_top=y_top-28; grid_h=grid_top-bottom
        cols,rows,gap=2,3,10; cw=(W-2*MARGIN-gap)/cols; ch=(grid_h-gap*(rows-1))/rows
        for i,(tier,title,prompt) in enumerate(chunk):
            col,row=i%cols,i//cols
            x=MARGIN+col*(cw+gap); yy=grid_top-(row+1)*ch-row*gap
            draw_card(c,x,yy,cw,ch,tier,title,prompt,page_i*6+1+i)
        draw_brand_footer(c,f"{page_i+2} / cards"); c.showPage()
    c.save(); print("christmas", out, out.stat().st_size); return out

# ---------- JUNIOR AGENT MISSION PACK ----------
def build_junior():
    out = ROOT/"printables"/"junior-agent-mission-pack.pdf"
    c = canvas.Canvas(str(out), pagesize=letter)
    c.setTitle("Junior Agent Mission Pack — Conspiraparty"); c.setAuthor("Conspiraparty")
    # cover / how-to
    draw_paper_bg(c); y=H-60
    c.setFillColor(INK); c.setFont("Anton", 30); c.drawCentredString(W/2,y,"JUNIOR AGENT"); y-=32
    c.setFont("Anton", 26); c.drawCentredString(W/2,y,"MISSION PACK"); y-=24
    c.setFillColor(RED); c.setFont("SpecialElite", 12); c.drawCentredString(W/2,y,"Free sample from Junior Agent's Guide to Totally Real Mysteries"); y-=28
    c.setStrokeColor(RED); c.setLineWidth(2); c.line(MARGIN+50,y,W-MARGIN-50,y); y-=36
    c.setFillColor(INK); c.setFont("SpecialElite", 12)
    for ln in ["Kid-safe silly missions for little field agents.",
               "Color, circle, and invent theories (the fun kind).",
               "Print on US Letter. Crayons strongly encouraged.",
               "Full book link: conspiraparty.com/books.html"]:
        c.drawCentredString(W/2,y,ln); y-=18
    y-=10
    c.setFillColor(PAPER2); c.setStrokeColor(RED); c.roundRect(MARGIN+40,y-90,W-2*MARGIN-80,90,8,fill=1,stroke=1)
    c.setFillColor(RED); c.setFont("Anton",14); c.drawCentredString(W/2,y-28,"MISSION BRIEFING")
    c.setFillColor(INK); c.setFont("SpecialElite",11)
    for i,ln in enumerate(["Complete the pages. Stamp your badge (drawn).", "Tell a grown-up your wildest silly theory.", "Ask for cocoa. Agents need fuel."]):
        c.drawCentredString(W/2, y-50-i*14, ln)
    draw_brand_footer(c,"1 / briefing"); c.showPage()

    # Page 2: UFO coloring / spot
    draw_paper_bg(c)
    c.setFillColor(INK); c.setFont("Anton", 22); c.drawCentredString(W/2, H-50, "MISSION 1: COLOR THE SAUCER")
    c.setFillColor(RED); c.setFont("SpecialElite", 10); c.drawCentredString(W/2, H-68, "Color the flying saucer. Add windows. Name your alien.")
    # saucer outline
    cx, cy = W/2, H/2+40
    c.setStrokeColor(INK); c.setLineWidth(2.5); c.setFillColor(Color(1,1,1,alpha=0))
    c.ellipse(cx-160, cy-30, cx+160, cy+30, fill=0, stroke=1)
    c.ellipse(cx-70, cy+10, cx+70, cy+70, fill=0, stroke=1)
    for dx in (-90,-30,30,90):
        c.circle(cx+dx, cy-5, 8, fill=0, stroke=1)
    # beam
    c.setDash(2,2); c.line(cx-40, cy-30, cx-80, cy-160); c.line(cx+40, cy-30, cx+80, cy-160); c.setDash()
    c.setFillColor(MUTED); c.setFont("SpecialElite", 11)
    c.drawCentredString(W/2, 140, "Alien name: _______________________________")
    c.drawCentredString(W/2, 118, "Where did it land? ________________________")
    draw_brand_footer(c,"2 / mission 1"); c.showPage()

    # Page 3: Bigfoot footprint match
    draw_paper_bg(c)
    c.setFillColor(INK); c.setFont("Anton", 22); c.drawCentredString(W/2, H-50, "MISSION 2: FOOTPRINT FILE")
    c.setFillColor(RED); c.setFont("SpecialElite", 10); c.drawCentredString(W/2, H-68, "Circle the footprint that looks MOST Bigfoot. Invent a cover story for the rest.")
    y = H-120
    labels = ["Definitely a boot", "Suspicious", "BIGFOOT?", "Raccoon with shoes"]
    for i,lab in enumerate(labels):
        x = MARGIN+30 + (i%2)*250
        yy = y - (i//2)*220
        c.setStrokeColor(INK); c.setLineWidth(2)
        # footprint blob
        c.ellipse(x+40, yy-140, x+120, yy-20, fill=0, stroke=1)
        for toe, dx in enumerate([-25,-5,15,35,50]):
            c.circle(x+80+dx, yy-10, 10 if toe!=2 else 12, fill=0, stroke=1)
        c.setFont("Anton", 12); c.setFillColor(INK); c.drawCentredString(x+90, yy-170, lab)
        c.setStrokeColor(MUTED); c.setDash(2,2); c.circle(x+90, yy-80, 70, fill=0, stroke=1); c.setDash()
    draw_brand_footer(c,"3 / mission 2"); c.showPage()

    # Page 4: Connect the dots / red string board
    draw_paper_bg(c)
    c.setFillColor(INK); c.setFont("Anton", 22); c.drawCentredString(W/2, H-50, "MISSION 3: CONNECT THE DOTS")
    c.setFillColor(RED); c.setFont("SpecialElite", 10); c.drawCentredString(W/2, H-68, "Draw lines between clues. What theory did you invent?")
    dots = [(120,520,"Sock"),(300,560,"Dryer"),(480,500,"Portal"),(180,380,"Cat"),(360,360,"Moon"),(460,280,"Mom"),(250,240,"Alien"),(400,180,"Pizza")]
    c.setFillColor(RED); c.setStrokeColor(INK); c.setLineWidth(1.5)
    for x,y,lab in dots:
        c.circle(x,y,10,fill=1,stroke=0)
        c.setFillColor(INK); c.setFont("SpecialElite", 10); c.drawCentredString(x, y-28, lab); c.setFillColor(RED)
    c.setFillColor(INK); c.setFont("SpecialElite", 11)
    c.drawString(MARGIN+20, 140, "My theory: _______________________________________________")
    c.drawString(MARGIN+20, 118, "_________________________________________________________")
    c.setFillColor(MUTED); c.setFont("SpecialElite", 9)
    c.drawCentredString(W/2, 95, "Want more missions? Junior Agent's Guide → conspiraparty.com/books.html")
    draw_brand_footer(c,"4 / mission 3"); c.showPage()
    c.save(); print("junior", out, out.stat().st_size); return out

# ---------- ROAD TRIP BINGO + CHECKLIST ----------
RT_SQUARES = [
    "Weird museum","Roadside giant","Mystery spot","UFO gift shop",
    "Ghost tour flyer","Bigfoot sticker","Area 51 shirt","Tin foil display",
    "Crop circle postcard","Haunted hotel","Secret bunker tour","Oddball diner",
    "Cryptid statue","Alien crossing sign","Conspiracy bookstore","Redacted mural",
    "Cold case podcast","Local legend plaque","Abandoned base","Sky light debate",
    "Tour guide wink","'No photos' zone","Tunnel rumor","Postcard from nowhere",
    "Missing time joke","Black helicopter tease","Welcome to Nowhere","Suspicious rest stop",
    "Vortex gift shop","Pyramid roadside","Mothman merch","Lizard person mug",
    "Flat Earth bumper","Chemtrail chat","Hollow Earth book","Skinwalker joke",
    "Time travel cafe","Portal parking lot","Classified restroom","Agent sunglasses",
]
assert len(RT_SQUARES)>=24

def fit_cell(c, text, max_w, max_h):
    for size in (11,10,9,8,7.5,7,6.5,6):
        leading=size*1.15; words=text.split(); lines=[]; cur=""
        c.setFont("SpecialElite", size)
        for w in words:
            trial=(cur+" "+w).strip()
            if c.stringWidth(trial,"SpecialElite",size)<=max_w: cur=trial
            else:
                if cur: lines.append(cur)
                cur=w
        if cur: lines.append(cur)
        if len(lines)*leading<=max_h: return size, lines
    return 6, [text[:16]+"…"]

def draw_bingo_grid(c, cells, left, bottom, size, free="FREE"):
    n=5; cell=size/n
    c.setStrokeColor(INK); c.setLineWidth(2.2); c.rect(left,bottom,size,size,fill=0,stroke=1); c.setLineWidth(0.9)
    for i in range(1,n):
        c.line(left+i*cell,bottom,left+i*cell,bottom+size)
        c.line(left,bottom+i*cell,left+size,bottom+i*cell)
    idx=0
    for row in range(n):
        for col in range(n):
            cx=left+col*cell+cell/2; cy=bottom+(n-1-row)*cell+cell/2
            if row==2 and col==2:
                c.setFillColor(RED); c.rect(left+col*cell+3, bottom+(n-1-row)*cell+3, cell-6, cell-6, fill=1, stroke=0)
                c.setFillColor(white); c.setFont("Anton", 12); c.drawCentredString(cx, cy-4, free)
            else:
                size_f, lines = fit_cell(c, cells[idx], cell-10, cell-12); idx+=1
                leading=size_f*1.15; total=(len(lines)-1)*leading
                c.setFillColor(INK); c.setFont("SpecialElite", size_f)
                start=cy+total/2-size_f*0.3
                for i,ln in enumerate(lines): c.drawCentredString(cx, start-i*leading, ln)

def build_roadtrip():
    out = ROOT/"printables"/"road-trip-bingo-checklist.pdf"
    c = canvas.Canvas(str(out), pagesize=letter)
    c.setTitle("Road Trip Bingo + Weird-Stop Checklist — Conspiraparty"); c.setAuthor("Conspiraparty")
    rng = random.Random(51)
    # how to
    draw_paper_bg(c); y=H-56
    c.setFillColor(INK); c.setFont("Anton", 28); c.drawCentredString(W/2,y,"SUSPICIOUS ROAD TRIP"); y-=30
    c.setFont("Anton", 26); c.drawCentredString(W/2,y,"BINGO + CHECKLIST"); y-=24
    c.setFillColor(RED); c.setFont("SpecialElite", 11); c.drawCentredString(W/2,y,"Sample from The Suspicious Road Trip Guide"); y-=20
    c.setStrokeColor(RED); c.setLineWidth(2); c.line(MARGIN+40,y,W-MARGIN-40,y); y-=30
    c.setFillColor(INK); c.setFont("SpecialElite", 12)
    for t in ["Print cards for the car. Middle square is FREE.",
              "Mark squares when you spot them on the road.",
              "First to 5 in a row yells 'PULLOVER!'",
              "Checklist page = weird-stop scavenger hunt.",
              "Full guide: conspiraparty.com/books.html"]:
        c.drawCentredString(W/2,y,t); y-=18
    draw_brand_footer(c,"1 / how to"); c.showPage()
    # 4 bingo cards
    for i in range(4):
        pool=RT_SQUARES[:]; rng.shuffle(pool); cells=pool[:24]
        draw_paper_bg(c)
        c.setFillColor(INK); c.setFont("Anton", 22); c.drawCentredString(W/2, H-48, "ROAD TRIP BINGO")
        c.setFillColor(RED); c.setFont("SpecialElite", 9); c.drawCentredString(W/2, H-64, f"Card {i+1} of 4  ·  Yell PULLOVER!")
        bottom=content_bottom(); grid_top=H-80; grid_size=min(W-2*MARGIN-24, grid_top-bottom)
        draw_bingo_grid(c, cells, (W-grid_size)/2, bottom, grid_size)
        draw_brand_footer(c, f"{i+2} / card {i+1}"); c.showPage()
    # checklist
    draw_paper_bg(c)
    c.setFillColor(INK); c.setFont("Anton", 24); c.drawCentredString(W/2, H-50, "WEIRD-STOP CHECKLIST")
    c.setFillColor(RED); c.setFont("SpecialElite", 10); c.drawCentredString(W/2, H-68, "Check off stops as you find them. Agent notes encouraged.")
    checks = [
        "Roadside giant statue","Mystery spot / gravity hill","UFO or alien gift shop",
        "Haunted hotel lobby","Local legend plaque","Cryptid mural or sticker",
        "Oddball museum","'No photos' sign","Abandoned base (from a safe distance)",
        "Diner with a conspiracy menu joke","Tunnel or bunker tour","Postcard from Nowhere",
        "Bigfoot crossing vibe","Time-travel cafe energy","Something you can't explain",
    ]
    y=H-100
    for item in checks:
        c.setStrokeColor(INK); c.setLineWidth(1.2); c.rect(MARGIN+20, y-2, 14, 14, fill=0, stroke=1)
        c.setFillColor(INK); c.setFont("SpecialElite", 12); c.drawString(MARGIN+46, y, item)
        y-=28
    c.setFillColor(MUTED); c.setFont("SpecialElite", 9)
    c.drawCentredString(W/2, 100, "More weird stops in The Suspicious Road Trip Guide → books.html")
    draw_brand_footer(c,"6 / checklist"); c.showPage()
    c.save(); print("roadtrip", out, out.stat().st_size); return out

# ---------- MONTHLY WALLPAPERS ----------
def build_wallpapers():
    outdir = ROOT/"assets"/"wallpapers"
    outdir.mkdir(parents=True, exist_ok=True)
    specs = [
        ("november-2026.png", "NOVEMBER", "2026", "WATCH THE SKIES", "#1a1a2e", "#e11d26", "#f4f0e8"),
        ("december-2026.png", "DECEMBER", "2026", "SANTA IS WATCHING", "#0b1a0f", "#e11d26", "#f4f0e8"),
    ]
    paths=[]
    for name, month, year, tagline, bg, accent, fg in specs:
        im = Image.new("RGB", (1080, 1920), bg)
        d = ImageDraw.Draw(im)
        # grainy border
        d.rectangle([40,40,1040,1880], outline=accent, width=6)
        d.rectangle([56,56,1024,1864], outline=fg, width=2)
        anton_lg = ImageFont.truetype(ANTON, 110)
        anton_md = ImageFont.truetype(ANTON, 72)
        elite = ImageFont.truetype(ELITE, 36)
        elite_sm = ImageFont.truetype(ELITE, 28)
        d.text((1080//2, 280), "CLASSIFIED", fill=accent, font=anton_md, anchor="mm")
        d.text((1080//2, 520), month, fill=fg, font=anton_lg, anchor="mm")
        d.text((1080//2, 640), year, fill=accent, font=anton_lg, anchor="mm")
        # stamp
        d.rectangle([340, 780, 740, 880], outline=accent, width=4)
        d.text((1080//2, 830), "TOP SECRET", fill=accent, font=anton_md, anchor="mm")
        d.text((1080//2, 1100), tagline, fill=fg, font=elite, anchor="mm")
        d.text((1080//2, 1200), "conspiraparty.com", fill="#888888", font=elite_sm, anchor="mm")
        # deco circles
        for cy in (1450, 1550, 1650):
            d.ellipse([490, cy, 590, cy+100], outline=accent, width=3)
        path = outdir/name
        im.save(path, "PNG", optimize=True)
        paths.append(path)
        print("wallpaper", path, path.stat().st_size)
    return paths

# ---------- PREVIEW IMAGES helper ----------
def make_previews(pdf_path: Path, stem: str, title_lines: list[str]):
    import subprocess, tempfile
    tmp = Path(tempfile.mkdtemp())
    # prefer page 2 if multi-page else 1
    subprocess.run(["pdftoppm","-jpeg","-r","140","-f","2","-l","2",str(pdf_path),str(tmp/"p")], check=True)
    jpgs = sorted(tmp.glob("*.jpg"))
    if not jpgs:
        subprocess.run(["pdftoppm","-jpeg","-r","140","-f","1","-l","1",str(pdf_path),str(tmp/"p")], check=True)
        jpgs = sorted(tmp.glob("*.jpg"))
    img = Image.open(jpgs[0]).convert("RGB")
    preview = img.copy(); preview.thumbnail((800,1035), Image.Resampling.LANCZOS)
    img_path = ROOT/"assets"/"img"/f"free-{stem}.jpg"
    preview.save(img_path, "JPEG", quality=88, optimize=True)
    # OG
    og = Image.new("RGB", (1200,630), "#f4f0e8")
    card = img.copy(); card.thumbnail((520,580), Image.Resampling.LANCZOS)
    og.paste(card, (40, (630-card.height)//2))
    d = ImageDraw.Draw(og)
    anton = ImageFont.truetype(ANTON, 56); elite = ImageFont.truetype(ELITE, 24)
    d.rectangle([580,80,1160,550], outline="#e11d26", width=4)
    yy=140
    for ln in title_lines:
        d.text((610, yy), ln, fill="#0b0b0b" if yy==140 else "#e11d26", font=anton)
        yy += 70
    d.text((610, yy+20), "Free printable · conspiraparty.com", fill="#6e6a63", font=elite)
    og_path = ROOT/"assets"/"og"/f"free-{stem}.jpg"; og.save(og_path, "JPEG", quality=88, optimize=True)
    # pin
    pin = Image.new("RGB", (800,1200), "#0b0b0b")
    d = ImageDraw.Draw(pin)
    d.rectangle([40,40,760,1160], outline="#e11d26", width=6)
    d.rectangle([56,56,744,1144], fill="#f4f0e8")
    anton_lg = ImageFont.truetype(ANTON, 52)
    d.text((100, 100), "FREE", fill="#e11d26", font=ImageFont.truetype(ANTON, 40))
    yy=170
    for ln in title_lines:
        d.text((100, yy), ln, fill="#0b0b0b", font=anton_lg); yy+=60
    card2 = img.copy(); card2.thumbnail((640,700), Image.Resampling.LANCZOS)
    pin.paste(card2, ((800-card2.width)//2, min(340, yy+20)))
    d.text((100, 1080), "conspiraparty.com", fill="#6e6a63", font=elite)
    pin_path = ROOT/"assets"/"pins"/f"free-{stem}-pin.jpg"; pin.save(pin_path, "JPEG", quality=88, optimize=True)
    print("previews", stem, img_path.name)
    return img_path

def make_wallpaper_preview():
    # collage of nov+dec for hub card
    nov = Image.open(ROOT/"assets"/"wallpapers"/"november-2026.png").convert("RGB")
    dec = Image.open(ROOT/"assets"/"wallpapers"/"december-2026.png").convert("RGB")
    nov.thumbnail((400,711)); dec.thumbnail((400,711))
    canvas_im = Image.new("RGB", (840, 750), "#0b0b0b")
    canvas_im.paste(nov, (20,20)); canvas_im.paste(dec, (420,20))
    d = ImageDraw.Draw(canvas_im)
    d.text((420, 720), "Monthly Wallpapers", fill="#f4f0e8", font=ImageFont.truetype(ANTON, 28), anchor="mm")
    path = ROOT/"assets"/"img"/"free-monthly-wallpapers.jpg"
    canvas_im.save(path, "JPEG", quality=88, optimize=True)
    og = Image.new("RGB", (1200,630), "#1a1a2e")
    n2=nov.copy(); n2.thumbnail((280,500)); d2=dec.copy(); d2.thumbnail((280,500))
    og.paste(n2, (80,65)); og.paste(d2, (400,65))
    dr=ImageDraw.Draw(og)
    dr.text((720,200), "MONTHLY", fill="#f4f0e8", font=ImageFont.truetype(ANTON, 56))
    dr.text((720,270), "WALLPAPERS", fill="#e11d26", font=ImageFont.truetype(ANTON, 56))
    dr.text((720,360), "Nov + Dec 1080×1920", fill="#aaaaaa", font=ImageFont.truetype(ELITE, 24))
    og_path=ROOT/"assets"/"og"/"free-monthly-wallpapers.jpg"; og.save(og_path,"JPEG",quality=88)
    pin=og.resize((800,1200)); pin_path=ROOT/"assets"/"pins"/"free-monthly-wallpapers-pin.jpg"; pin.save(pin_path,"JPEG",quality=88)
    print("wallpaper preview", path)
    return path

def make_agent_id_preview():
    # static mock of badge for hub card
    im = Image.new("RGB", (800, 1035), "#f4f0e8")
    d = ImageDraw.Draw(im)
    d.rectangle([80,120,720,900], outline="#0b0b0b", width=5)
    d.rectangle([80,120,720,220], fill="#e11d26")
    d.text((400,170), "AGENT ID", fill="#fff", font=ImageFont.truetype(ANTON, 48), anchor="mm")
    d.rectangle([150,260,350,460], outline="#0b0b0b", width=3)
    d.text((250,360), "PHOTO", fill="#6e6a63", font=ImageFont.truetype(ELITE, 22), anchor="mm")
    d.text((520,300), "NAME", fill="#6e6a63", font=ImageFont.truetype(ELITE, 18), anchor="mm")
    d.text((520,340), "AGENT COOL", fill="#0b0b0b", font=ImageFont.truetype(ANTON, 28), anchor="mm")
    d.text((520,420), "RANK", fill="#6e6a63", font=ImageFont.truetype(ELITE, 18), anchor="mm")
    d.text((520,460), "FIELD AGENT", fill="#e11d26", font=ImageFont.truetype(ANTON, 24), anchor="mm")
    d.rectangle([200,560,600,680], outline="#e11d26", width=4)
    d.text((400,620), "TOP SECRET", fill="#e11d26", font=ImageFont.truetype(ANTON, 36), anchor="mm")
    d.text((400,780), "conspiraparty.com", fill="#6e6a63", font=ImageFont.truetype(ELITE, 22), anchor="mm")
    path = ROOT/"assets"/"img"/"free-agent-id-maker.jpg"
    im.save(path, "JPEG", quality=88, optimize=True)
    og = Image.new("RGB", (1200,630), "#f4f0e8")
    badge = im.copy(); badge.thumbnail((420,540)); og.paste(badge, (40,45))
    dr=ImageDraw.Draw(og)
    dr.text((520,180), "AGENT ID", fill="#0b0b0b", font=ImageFont.truetype(ANTON, 64))
    dr.text((520,260), "CARD MAKER", fill="#e11d26", font=ImageFont.truetype(ANTON, 64))
    dr.text((520,360), "Type a name. Download a badge.", fill="#6e6a63", font=ImageFont.truetype(ELITE, 24))
    og_path=ROOT/"assets"/"og"/"free-agent-id-maker.jpg"; og.save(og_path,"JPEG",quality=88)
    pin_path=ROOT/"assets"/"pins"/"free-agent-id-maker-pin.jpg"
    im.resize((800,1200)).save(pin_path,"JPEG",quality=88)
    print("agent id preview", path)
    return path

if __name__ == "__main__":
    xmas = build_christmas()
    junior = build_junior()
    road = build_roadtrip()
    build_wallpapers()
    make_previews(xmas, "christmas-conspiracy-cards", ["CHRISTMAS", "CONSPIRACY CARDS"])
    make_previews(junior, "junior-agent-mission-pack", ["JUNIOR AGENT", "MISSION PACK"])
    make_previews(road, "road-trip-bingo", ["ROAD TRIP", "BINGO"])
    make_wallpaper_preview()
    make_agent_id_preview()
    print("ALL DONE")
