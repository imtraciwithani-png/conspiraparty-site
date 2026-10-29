#!/usr/bin/env python3
"""Fetch weird/UFO/cryptid/odd/politics/QAnon headlines from public RSS feeds,
filter out tragedy/death, attach skeptic Conspiraparty one-liners, and
write data/weird-news.json + weird-news.html for the static site.

Politics and QAnon are allowed on this page (skeptic roast, no defamatory claims).
No AI API keys. Headlines and links only — never article bodies.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
from urllib.parse import quote
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "weird-news.json"
HTML_PATH = ROOT / "weird-news.html"
MAX_ITEMS = 24
USER_AGENT = "ConspirapartyWeirdNews/1.0 (+https://conspiraparty.com; daily aggregator)"

KIT_URL = "https://happyplaceinkandart.etsy.com/listing/4502272966"
PPT_URL = "https://www.etsy.com/listing/4604436132/conspiracy-powerpoint-night-party-kit"
WEB3_KEY = "a2adf9e4-98f3-48cf-ab94-208e1705280b"

FEEDS = [
    {
        "name": "UPI Odd News",
        "url": "https://rss.upi.com/news/odd_news.rss",
        "tag": "Odd",
        "require_any": [],  # whole feed is odd news
    },
    {
        "name": "Reddit · r/nottheonion",
        "url": "https://www.reddit.com/r/nottheonion/.rss",
        "tag": "Odd",
        "require_any": [],
    },
    {
        "name": "Google News · Odd / weird news",
        "url": "https://news.google.com/rss/search?q=%22odd+news%22+OR+%22weird+news%22+OR+%22strange+but+true%22+OR+bizarre+-death+-killed+-murder&hl=en-US&gl=US&ceid=US:en",
        "tag": "Odd",
        "require_any": [
            "odd", "weird", "strange", "bizarre", "unusual", "curious",
            "quirky", "offbeat",
        ],
    },
    {
        "name": "Google News · UFO / UAP",
        "url": "https://news.google.com/rss/search?q=UFO+OR+UAP+OR+%22unidentified+aerial%22+OR+%22unidentified+anomalous%22+-death+-killed&hl=en-US&gl=US&ceid=US:en",
        "tag": "UFO",
        "require_any": [
            "ufo", "uap", "unidentified aerial", "unidentified anomalous",
            "flying saucer", "orb", "drone swarm", "alien craft",
        ],
    },
    {
        "name": "Google News · Cryptids",
        "url": "https://news.google.com/rss/search?q=Bigfoot+OR+Sasquatch+OR+cryptid+OR+chupacabra+OR+%22Loch+Ness+monster%22+OR+mothman+-death+-killed&hl=en-US&gl=US&ceid=US:en",
        "tag": "Cryptid",
        "require_any": [
            "bigfoot", "sasquatch", "cryptid", "chupacabra", "loch ness",
            "nessie", "mothman", "yeti", "abominable", "jersey devil",
            "skunk ape", "dogman",
        ],
    },
    {
        "name": "Google News · Strange discoveries",
        "url": "https://news.google.com/rss/search?q=%22strange+discovery%22+OR+%22mysterious+object%22+OR+%22scientists+baffled%22+OR+%22unexplained+phenomenon%22+-death+-killed&hl=en-US&gl=US&ceid=US:en",
        "tag": "Strange",
        "require_any": [
            "strange", "mysterious", "baffled", "unexplained", "anomaly",
            "odd discovery", "bizarre", "enigmatic", "puzzling",
        ],
    },
    {
        "name": "The Debrief",
        "url": "https://thedebrief.org/feed/",
        "tag": "UFO",
        "require_any": [
            "ufo", "uap", "alien", "unidentified", "anomalous", "disclosure",
            "orb", "craft", "extraterrestrial", "paranormal", "cryptid",
            "mysterious", "anomaly",
        ],
    },
    {
        "name": "ScienceAlert",
        "url": "https://www.sciencealert.com/feed",
        "tag": "Science",
        "require_any": [
            "mysterious", "strange", "weird", "odd", "anomaly", "ancient",
            "discovery", "baffling", "unexplained", "alien", "mars",
            "moon", "space", "fossil", "creature", "ocean", "deep",
            "pyramid", "lost", "asteroid", "comet",
        ],
    },
    {
        "name": "Google News · QAnon / conspiracy culture",
        "url": "https://news.google.com/rss/search?q=QAnon+OR+%22Q+Anon%22+OR+%22conspiracy+theory%22+OR+%22conspiracy+theories%22+OR+%22deep+state%22+-death+-killed+-murder&hl=en-US&gl=US&ceid=US:en",
        "tag": "QAnon",
        "require_any": [
            "qanon", "q anon", "conspiracy theory", "conspiracy theories",
            "deep state", "false flag", "chemtrail", "flat earth",
            "lizard people", "illuminati", "new world order",
        ],
    },
    {
        "name": "Google News · Bizarre politics",
        "url": "https://news.google.com/rss/search?q=%22bizarre%22+OR+%22strange%22+OR+%22odd%22+OR+%22wild%22+(politics+OR+politician+OR+congress+OR+campaign+OR+election)+-death+-killed+-murder&hl=en-US&gl=US&ceid=US:en",
        "tag": "Politics",
        "require_any": [
            "bizarre", "strange", "odd", "wild", "weird", "absurd",
            "unusual", "viral", "meltdown", "rant", "gaffe",
        ],
    },
    {
        "name": "Google News · Conspiracy theory news",
        "url": "https://news.google.com/rss/search?q=%22conspiracy+theory%22+OR+%22conspiracy+theories%22+OR+conspiracist+OR+%22rabbit+hole%22+-death+-killed&hl=en-US&gl=US&ceid=US:en",
        "tag": "QAnon",
        "require_any": [
            "conspiracy theory", "conspiracy theories", "conspiracist",
            "debunk", "qanon", "deep state", "baseless", "unfounded",
        ],
    },
]

# Politics / QAnon are ALLOWED on this page (Traci approved for Weird News only).
# Keep a no-op so older call sites that mention BLOCK still import cleanly.
BLOCK = re.compile(r"^$")  # never matches

# Tragedy / death / violence — keep the page fun.
TRAGEDY = re.compile(
    r"\b("
    r"dies?|died|dying|death|dead|killed|killing|murder|suicide|fatal|"
    r"funeral|obituary|massacre|shooting|shot dead|stabbed|"
    r"body found|bodies found|corpse|homicide|executed|beheaded|"
    r"terrorist|terror attack|bombing|explosion kills|"
    r"crash kills|plane crash|died of|mourns|victims? of|"
    r"pointing gun|held at gunpoint|brandished"
    r")\b",
    re.I,
)

NOISE = re.compile(
    r"\b("
    r"warehouse sale|%\s*off|under armour|patagonia|outdoor enthusiasts|"
    r"gift guide|gifts for|black friday|cyber monday|coupon|"
    r"product review|unboxing|amazon deal|shop now|"
    r"nfl|nba|mlb|nhl|mls|scoreboard|box score|espn|quarterback|\bqb\b|steelers|yankees|lakers|"
    r"premier league|champions league|stump mic|cricket|liverpool|chelsea|footballer|"
    r"touchdown|homerun|home run|goalkeeper|midfielder|striker|"
    r"wnba|nba finals|clippers|lakers|warriors|turnover just|non-primetime|"
    r"canucks|boeser|hellebuyck|nhl|hockey|mlb pitcher|fantasy football|"
    r"dark web|onion links|lifecycle and onion|"
    r"obituary|wedding announcement|"
    r"best chest|best \d+|the \d+ best|product roundup|"
    r"lunch ride|tires?\b|fork make sense|pinkbike|"
    r"robot\b.*anime|go nagai|manga\b|"
    r"auction at|up for auction|"
    r"nsfw|onlyfans"
    r")\b",
    re.I,
)

ONE_LINERS = {
    "UFO": [
        "Tin foil hats: optional. Curiosity: required.",
        "Filed under: things the neighbors will swear they saw.",
        "Perfect PowerPoint Night opener. Bring snacks.",
        "The sky called. It wants its secrets back.",
        "Not a weather balloon. Not this time. Probably.",
        "Case file stamped CURIOUS. Proceed with popcorn.",
        "Your group chat is going to lose it.",
        "Evidence? Circumstantial. Vibes? Immaculate.",
    ],
    "Cryptid": [
        "Bigfoot called. He wants his alibi back.",
        "Blurry photo energy: elite tier.",
        "Perfect excuse to cancel hiking plans.",
        "The woods keep secrets. And snack crumbs.",
        "Stamp this one: UNCONFIRMED BUT ICONIC.",
        "Field agents: bring binoculars and snacks.",
        "Cryptid sighting or really committed cosplay? Debate tonight.",
        "Nature documentary, but make it suspicious.",
    ],
    "Strange": [
        "Science said 'huh' and left the chat.",
        "Add this to the conspiracy corkboard immediately.",
        "Official explanation pending. Party theories welcome.",
        "The kind of headline that ruins a group sleepover.",
        "Somebody's PowerPoint Night topic just wrote itself.",
        "Classify as: delightfully weird.",
        "They'll say it's normal. We have questions.",
        "Strange enough to screenshot. Do it.",
    ],
    "Odd": [
        "Odd News Department is working overtime.",
        "Reality called in sick. This filled in.",
        "Tell your group chat before someone else does.",
        "Weirdness level: party-ready.",
        "Odd enough for the corkboard. Bring snacks.",
        "The universe is freestyling again.",
        "Pin this to the fridge. Trust us.",
        "Strange but true-ish. Party fuel either way.",
    ],
    "Science": [
        "Lab coats and tin foil: same energy today.",
        "Peer-reviewed? Maybe. Party-reviewed? Absolutely.",
        "Science did a thing. We have theories.",
        "This belongs on the corkboard next to the UFO cutouts.",
        "Somebody call the Shadow Party Committee.",
        "Hypothesis: this is excellent party small talk.",
        "The data is weird. We approve.",
        "Discovery unlocked. Conspiracy optional.",
    ],
    "Politics": [
        "Skeptic mode: ON. Popcorn: also ON.",
        "Both sides brought volume. Receipts still pending.",
        "Filed under: loud takes, quiet evidence.",
        "Question everything. Especially the spin.",
        "Perfect PowerPoint Night bait. Fact-check optional, snacks required.",
        "The timeline wants a timeout. We want a theory board.",
        "Equal-opportunity side-eye. All parties welcome.",
        "Campaign energy meets corkboard energy.",
    ],
    "QAnon": [
        "Rabbit hole detected. Bring a flashlight and a grain of salt.",
        "Trust, but verify. Then verify again. Then throw a party.",
        "Claims are free. Evidence still costs receipts.",
        "Corkboard fuel — label every pin UNCONFIRMED.",
        "Skeptic cosplay recommended. Tin foil optional.",
        "The map is not the territory. The meme is not the brief.",
        "Ask better questions. Skip the absolute certainty.",
        "Entertainment first. Extraordinary claims need extraordinary snacks.",
    ],
}

FALLBACK_LINERS = [
    "Filed under weird. Approved for the party.",
    "Headlines like this are why we throw Conspiracy PowerPoint Night.",
    "Question everything. Especially this.",
    "The truth is out there. Also snacks.",
]

KIT_CTAS = [
    {
        "stamp": "Supply Drop",
        "title": "Turn tonight's headline into a <span class=\"r\">party</span>",
        "blurb": "Print the props, pass out the badges, and let the theories fly. Full printable kit — use code LEAKED20.",
        "btn": "Get the Party Kit – 20% off",
        "href": KIT_URL,
    },
    {
        "stamp": "Mission Brief",
        "title": "Pitch the theory. Vote on awards.",
        "blurb": "Conspiracy PowerPoint Night: slides, host script, and topic cards for the weirdest headlines.",
        "btn": "Get PowerPoint Night – $9.99",
        "href": PPT_URL,
    },
    {
        "stamp": "Free Intel",
        "title": "Need a meme for the group chat?",
        "blurb": "Steal a vintage-style conspiracy meme, then come back for tomorrow's sweep.",
        "btn": "Browse free memes",
        "href": "memes.html",
        "external": False,
    },
]


def fetch_bytes(url: str, timeout: int = 25) -> bytes | None:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.read()
    except Exception as e:
        print(f"  FAIL fetch {url}: {e}", file=sys.stderr)
        return None


def local(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag


def text_of(el: ET.Element | None) -> str:
    if el is None:
        return ""
    parts = [el.text or ""]
    for child in el:
        parts.append(text_of(child))
        parts.append(child.tail or "")
    return "".join(parts).strip()


def parse_rss(data: bytes) -> list[dict]:
    items = []
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        print(f"  FAIL parse: {e}", file=sys.stderr)
        return items

    for item in root.iter():
        if local(item.tag) != "item":
            continue
        title = link = pub = source = desc = ""
        for child in item:
            t = local(child.tag)
            if t == "title":
                title = text_of(child)
            elif t == "link":
                link = (child.text or "").strip() or child.get("href", "")
            elif t == "pubDate":
                pub = (child.text or "").strip()
            elif t == "source":
                source = (child.text or "").strip()
            elif t == "description":
                desc = text_of(child)
        if not link:
            for child in item:
                if local(child.tag) == "link" and child.get("href"):
                    link = child.get("href", "")
        if title and link:
            items.append(
                {
                    "title": clean_title(title),
                    "link": link,
                    "pub": pub,
                    "source": source,
                    "desc": desc,
                }
            )

    if not items:
        for entry in root.iter():
            if local(entry.tag) != "entry":
                continue
            title = link = pub = ""
            for child in entry:
                t = local(child.tag)
                if t == "title":
                    title = text_of(child)
                elif t == "link":
                    href = child.get("href") or (child.text or "").strip()
                    if href and (not link or child.get("rel") == "alternate"):
                        link = href
                elif t in ("published", "updated"):
                    pub = (child.text or "").strip()
            if title and link:
                items.append(
                    {
                        "title": clean_title(title),
                        "link": link,
                        "pub": pub,
                        "source": "",
                        "desc": "",
                    }
                )
    return items


def clean_title(t: str) -> str:
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    t = re.sub(r"\s+", " ", t).strip()
    return t


def parse_date(pub: str) -> datetime | None:
    if not pub:
        return None
    try:
        dt = parsedate_to_datetime(pub)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        pass
    try:
        return datetime.fromisoformat(pub.replace("Z", "+00:00"))
    except Exception:
        return None


def blocked(text: str) -> bool:
    t = text or ""
    if BLOCK.search(t):
        return True
    if TRAGEDY.search(t):
        return True
    if NOISE.search(t):
        return True
    if re.search(r"\byeti\b", t, re.I):
        if not re.search(
            r"\b(bigfoot|sasquatch|cryptid|abominable|himalaya|sighting|creature|monster|snowman)\b",
            t,
            re.I,
        ):
            if re.search(
                r"\b(cooler|tumbler|mug|warehouse|sale|resort|under armour|patagonia|gift)\b",
                t,
                re.I,
            ):
                return True
            if re.search(r"\b(yeti)\b.*\b(sale|warehouse|%|off|gifts?)\b", t, re.I):
                return True
    return False


def pick_liner(tag: str, title: str) -> str:
    pool = ONE_LINERS.get(tag, FALLBACK_LINERS)
    h = int(hashlib.md5(title.encode("utf-8")).hexdigest(), 16)
    return pool[h % len(pool)]


def source_name(feed_name: str, item: dict) -> str:
    title = item["title"]
    if " - " in title and "Google News" in feed_name:
        left, right = title.rsplit(" - ", 1)
        if 2 <= len(right) <= 60 and not right.lower().startswith("http"):
            item["title"] = left.strip()
            return right.strip()
    if item.get("source"):
        return item["source"]
    if "Reddit" in feed_name:
        return "r/nottheonion"
    if "UPI" in feed_name:
        return "UPI Odd News"
    m = re.match(r"https?://(?:www\.)?([^/]+)", item["link"])
    if m:
        return m.group(1)
    return feed_name.split("·")[0].strip()


def gather() -> list[dict]:
    collected: list[dict] = []
    seen_links: set[str] = set()
    seen_titles: set[str] = set()

    for feed in FEEDS:
        print(f"Fetching {feed['name']}…")
        raw = fetch_bytes(feed["url"])
        if not raw:
            continue
        head = raw[:200].lstrip().lower()
        if head.startswith(b"<!doctype") or head.startswith(b"<html"):
            print(f"  SKIP {feed['name']}: HTML not RSS", file=sys.stderr)
            continue
        items = parse_rss(raw)
        print(f"  {len(items)} raw items")
        require = [x.lower() for x in feed.get("require_any", [])]
        for it in items:
            title = it["title"]
            link = it["link"]
            blob = f"{title} {it.get('desc', '')}"
            if blocked(blob):
                continue
            if require and not any(k in blob.lower() for k in require):
                continue
            norm = title.lower().replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
            title_key = re.sub(r"[^a-z0-9]+", "", norm)[:80]
            if link in seen_links or title_key in seen_titles:
                continue
            seen_links.add(link)
            seen_titles.add(title_key)
            src = source_name(feed["name"], it)
            if blocked(it["title"]):
                continue
            dt = parse_date(it["pub"])
            tag = feed["tag"]
            tl = it["title"].lower()
            cryptid_keys = (
                "bigfoot",
                "sasquatch",
                "cryptid",
                "chupacabra",
                "mothman",
                "loch ness",
                "nessie",
                "jersey devil",
                "skunk ape",
            )
            ufo_keys = (
                "ufo",
                "uap",
                "unidentified aerial",
                "unidentified anomalous",
                "flying saucer",
                "alien disclosure",
                "declassified uap",
            )
            strange_keys = (
                "mysterious",
                "strange discovery",
                "baffled",
                "unexplained",
                "anomaly",
                "enigmatic",
            )
            qanon_keys = (
                "qanon",
                "q anon",
                "q-anon",
                "deep state",
                "pizzagate",
                "chemtrail",
                "flat earth",
                "lizard people",
                "illuminati",
                "new world order",
                "false flag",
            )
            politics_keys = (
                "congress",
                "senator",
                "campaign",
                "election",
                "ballot",
                "white house",
                "governor",
                "democrat",
                "republican",
                "gop",
                "maga",
                "primary",
                "midterm",
                "politician",
                "capitol",
                "trump",
                "biden",
                "harris",
                "obama",
                "clinton",
                "pelosi",
                "mcconnell",
                "aoc",
                "voter",
                "polling",
            )
            # QAnon tag: explicit movement/lore words, or "conspiracy theory" in a politics context
            if any(k in tl for k in qanon_keys):
                tag = "QAnon"
            elif "conspiracy theor" in tl and any(k in tl for k in politics_keys + ("ballot", "poll", "deep state", "debunk")):
                tag = "QAnon"
            elif "conspiracy theor" in tl and feed["tag"] == "QAnon":
                tag = "QAnon"
            elif any(k in tl for k in politics_keys):
                tag = "Politics"
            elif any(k in tl for k in cryptid_keys):
                tag = "Cryptid"
            elif any(k in tl for k in ufo_keys):
                tag = "UFO"
            elif any(k in tl for k in strange_keys):
                tag = "Strange"
            elif tag == "UFO" and not any(k in tl for k in ufo_keys):
                tag = "Science"

            if re.search(r"\byeti\b", tl) and not any(
                k in tl
                for k in (
                    "bigfoot",
                    "sasquatch",
                    "cryptid",
                    "abominable",
                    "sighting",
                    "creature",
                    "monster",
                    "snowman",
                    "himalaya",
                )
            ):
                if any(
                    k in tl
                    for k in (
                        "tire",
                        "fork",
                        "ride",
                        "bike",
                        "cooler",
                        "tumbler",
                        "sale",
                        "warehouse",
                        "gift",
                        "expedition everest",
                        "asr",
                    )
                ):
                    continue

            collected.append(
                {
                    "title": it["title"][:200],
                    "url": link,
                    "source": src[:80],
                    "feed": feed["name"],
                    "tag": tag,
                    "published": dt.isoformat() if dt else None,
                    "published_display": (
                        dt.astimezone(timezone.utc).strftime("%b %d, %Y")
                        if dt
                        else "Recently"
                    ),
                    "one_liner": pick_liner(tag, it["title"]),
                    "id": hashlib.md5(link.encode()).hexdigest()[:12],
                }
            )

    def sort_key(x):
        if x["published"]:
            return x["published"]
        return "1970-01-01"

    collected.sort(key=sort_key, reverse=True)

    per_tag_cap = {"UFO": 4, "Cryptid": 3, "Strange": 3, "Odd": 4, "Science": 3, "Politics": 5, "QAnon": 5}
    counts = {k: 0 for k in per_tag_cap}
    balanced = []
    for it in collected:
        tag = it["tag"]
        cap = per_tag_cap.get(tag, 4)
        if counts.get(tag, 0) >= cap:
            continue
        counts[tag] = counts.get(tag, 0) + 1
        balanced.append(it)
        if len(balanced) >= MAX_ITEMS:
            break
    if len(balanced) < MAX_ITEMS:
        ids = {x["id"] for x in balanced}
        for it in collected:
            if it["id"] in ids:
                continue
            balanced.append(it)
            if len(balanced) >= MAX_ITEMS:
                break
    balanced.sort(key=sort_key, reverse=True)
    return balanced[:MAX_ITEMS]



def story_slug(it: dict) -> str:
    """Stable short anchor id for a headline card."""
    base = re.sub(r"[^a-z0-9]+", "-", it["title"].lower()).strip("-")[:48].strip("-")
    sid = it.get("id") or hashlib.md5(it["url"].encode()).hexdigest()[:8]
    if not base:
        base = "story"
    return f"{base}-{sid}"


def share_text(it: dict) -> str:
    return f'{it["title"]} — {it["one_liner"]} via conspiraparty.com'


def render_card(it: dict) -> str:
    title = html.escape(it["title"])
    url = html.escape(it["url"], quote=True)
    source = html.escape(it["source"])
    date = html.escape(it["published_display"])
    liner = html.escape(it["one_liner"])
    tag = html.escape(it["tag"])
    slug = story_slug(it)
    anchor = html.escape(slug, quote=True)
    share_path = f"https://conspiraparty.com/weird-news.html#story-{slug}"
    share_url = html.escape(share_path, quote=True)
    text = share_text(it)
    text_esc = html.escape(text)
    text_q = html.escape(quote(text), quote=True)
    url_q = html.escape(quote(share_path, safe=""), quote=True)
    # Pinterest wants a page image; use site OG image
    media_q = html.escape(quote("https://conspiraparty.com/assets/og/index.jpg", safe=""), quote=True)
    x_href = f"https://x.com/intent/post?text={text_q}&url={url_q}"
    fb_href = f"https://www.facebook.com/sharer/sharer.php?u={url_q}"
    pin_href = f"https://www.pinterest.com/pin/create/button/?url={url_q}&media={media_q}&description={text_q}"
    return f"""<article class="news-card card" id="story-{anchor}" data-tag="{tag}" data-share-url="{share_url}" data-share-text="{text_esc}">
  <div class="news-meta"><span class="news-tag">{tag}</span><span class="news-date">{date}</span></div>
  <h3 class="news-title"><a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a></h3>
  <p class="news-source">via {source}</p>
  <p class="news-liner"><span class="stamp tiny">Conspiraparty take</span> {liner}</p>
  <div class="share-box">
    <button type="button" class="btn sm share-native" data-share>Share this</button>
    <div class="share-links" hidden>
      <a class="btn sm" href="{html.escape(x_href, quote=True)}" target="_blank" rel="noopener noreferrer">X</a>
      <a class="btn sm" href="{html.escape(fb_href, quote=True)}" target="_blank" rel="noopener noreferrer">Facebook</a>
      <a class="btn sm" href="{html.escape(pin_href, quote=True)}" target="_blank" rel="noopener noreferrer">Pinterest</a>
      <button type="button" class="btn sm share-copy" data-copy>Copy link</button>
    </div>
  </div>
</article>"""


def render_kit_cta(cta: dict) -> str:
    rel = ' target="_blank" rel="noopener sponsored"' if cta.get("external", True) and cta["href"].startswith("http") else ""
    if cta["href"].endswith(".html"):
        rel = ""
    return f"""<aside class="kit-cta card">
  <span class="stamp tiny">{html.escape(cta["stamp"])}</span>
  <h3>{cta["title"]}</h3>
  <p>{html.escape(cta["blurb"]) if "<" not in cta["blurb"] else cta["blurb"]}</p>
  <a class="btn sm" href="{html.escape(cta["href"], quote=True)}"{rel}>{html.escape(cta["btn"])}</a>
</aside>"""


def render_feed(items: list[dict]) -> str:
    """Interleave kit CTAs every 6 cards so each section links to kits."""
    parts: list[str] = []
    cta_i = 0
    for i, it in enumerate(items):
        parts.append(render_card(it))
        if (i + 1) % 6 == 0 and cta_i < len(KIT_CTAS):
            parts.append(render_kit_cta(KIT_CTAS[cta_i]))
            cta_i += 1
    # Always end with at least one kit CTA if we have cards
    if items and cta_i == 0:
        parts.append(render_kit_cta(KIT_CTAS[0]))
    elif items and cta_i < len(KIT_CTAS) and len(items) % 6 != 0:
        parts.append(render_kit_cta(KIT_CTAS[cta_i]))
    return "\n".join(parts) if parts else (
        '<p class="center lead">No headlines cleared the filters today. '
        "Check back tomorrow — the universe is usually weirder.</p>"
    )


def render_html(items: list[dict], generated_at: str) -> str:
    feed_html = render_feed(items)
    gen_display = html.escape(generated_at)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Weird News &amp; Political Rabbit Holes | Conspiraparty</title>
<meta name="description" content="Daily weird news and political rabbit holes — UFOs, cryptids, wild politics and QAnon with skeptic Conspiraparty takes. Auto-updated. Tragedy filtered. Entertainment only.">
<link rel="canonical" href="https://conspiraparty.com/weird-news.html">
<meta property="og:site_name" content="Conspiraparty">
<meta property="og:title" content="Weird News &amp; Political Rabbit Holes | Conspiraparty">
<meta property="og:description" content="Weird news and political rabbit holes with skeptic Conspiraparty takes. Roast the spin. Bring snacks.">
<meta property="og:url" content="https://conspiraparty.com/weird-news.html">
<meta property="og:type" content="website">
<meta property="og:image" content="https://conspiraparty.com/assets/og/index.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Weird News &amp; Political Rabbit Holes | Conspiraparty">
<meta name="twitter:description" content="Weird news and political rabbit holes. Skeptic takes. Updated automatically.">
<meta name="twitter:image" content="https://conspiraparty.com/assets/og/index.jpg">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/Anton-Regular.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="assets/style.css">
<style>
.news-feed{{display:flex;flex-direction:column;gap:16px;max-width:820px;margin:0 auto}}
.news-card{{padding:18px 18px 16px!important;display:block!important}}
.news-card .news-title{{font-family:var(--font-display);font-size:clamp(1.15rem,3.5vw,1.55rem);line-height:1.15;margin:0 0 8px;text-transform:uppercase;letter-spacing:.02em;font-weight:400}}
.news-card .news-title a{{color:inherit;text-decoration:none}}
.news-card .news-title a:hover{{color:var(--red)}}
.news-meta{{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px;font-size:.82rem;color:var(--text-dim)}}
.news-tag{{font-family:var(--font-display);letter-spacing:.06em;text-transform:uppercase;background:var(--red);color:#fff;padding:3px 8px;font-size:.75rem}}
.news-date{{opacity:.85}}
.news-source{{margin:0 0 12px;font-size:.9rem;color:var(--text-dim)!important}}
.news-liner{{margin:0;padding-top:12px;border-top:1px dashed rgba(255,255,255,.15);font-size:1rem;line-height:1.45;color:#eee!important}}
.stamp.tiny{{font-size:.7rem;padding:1px 8px;transform:rotate(-4deg);margin-right:8px;vertical-align:middle;display:inline-block}}
.filter-bar{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:0 0 22px}}
.filter-bar button{{font:inherit;cursor:pointer;background:#111;color:#fff;border:1px solid rgba(255,255,255,.25);padding:8px 14px;font-family:var(--font-display);letter-spacing:.04em;text-transform:uppercase;border-radius:var(--radius-btn)}}
.filter-bar button[aria-pressed=true],.filter-bar button:hover{{background:var(--red);border-color:var(--red)}}
.updated{{opacity:.7;font-size:.85rem;margin-top:8px;color:var(--text-dim)}}
.disclaimer{{max-width:720px;margin:22px auto 0;font-size:.85rem;opacity:.8;text-align:center;color:var(--text-dim)!important}}
.kit-cta{{text-align:center;padding:22px 20px!important;border:1px solid var(--red)!important;background:#1a1012!important}}
.kit-cta h3{{margin-top:8px}}
.kit-cta .btn{{margin-top:12px;display:inline-flex;width:auto}}
.kit-cta p{{color:#cfcfd4!important}}
.share-box{{margin-top:14px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
.share-box .btn.sm{{width:auto;margin-top:0;padding:6px 12px;font-size:.8rem}}
.share-links{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;width:100%}}
.share-links[hidden]{{display:none!important}}
.share-links:not([hidden]){{display:flex}}
.share-box .share-copy.copied{{background:var(--red);border-color:var(--red)}}
@media (max-width:720px){{
  .share-links{{display:none!important}}
  .news-card .share-native{{display:inline-flex}}
}}
@media (min-width:721px){{
  .news-card .share-native{{display:none}}
  .share-links{{display:flex!important}}
  .share-links[hidden]{{display:flex!important}}
}}
</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Weird News & Political Rabbit Holes","description":"Daily weird news and political rabbit holes — UFOs, cryptids, wild politics and QAnon with skeptic Conspiraparty takes.","url":"https://conspiraparty.com/weird-news.html","isPartOf":{{"@type":"WebSite","name":"Conspiraparty","url":"https://conspiraparty.com/"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://conspiraparty.com/"}},{{"@type":"ListItem","position":2,"name":"Weird News","item":"https://conspiraparty.com/weird-news.html"}}]}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="promo">20% off the full printable kit with code <a href="{KIT_URL}" target="_blank" rel="noopener sponsored">LEAKED20</a></div>
<header class="top">
  <div class="bar">
    <a class="logo" href="index.html"><img src="assets/img/logo.png" alt="Conspiraparty.com – Top Secret Party Kit" width="220" height="70"></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>
  <nav class="main" id="nav" aria-label="Main">
    <ul>
      <li><a href="index.html#kit">Party Kit</a></li>
      <li><a href="free-printables.html">Free</a></li>
      <li><a href="memes.html">Memes</a></li>
      <li><a href="weird-news.html" aria-current="page">Weird News</a></li>
      <li><a href="shirts.html">Shirts</a></li>
      <li><a href="quiz.html">Quiz</a></li>
      <li><a href="gift-guide.html">Gifts</a></li>
    </ul>
  </nav>
</header>

<main id="main">
  <section class="hero">
    <div class="wrap center">
      <span class="stamp">Leaked Daily</span>
      <h1>WEIRD NEWS &amp; <span class="r">POLITICAL</span> RABBIT HOLES</h1>
      <p class="lead">UFOs, cryptids, odd headlines, wild politics and QAnon rabbit holes — with a skeptic Conspiraparty take on each. We roast the spin on all sides. Auto-updated. No tragedy. Entertainment only.</p>
      <p class="updated">Last sweep: {gen_display} UTC · Headlines &amp; links only</p>
    </div>
  </section>

  <section class="cork">
    <div class="wrap">
      <div class="filter-bar" role="group" aria-label="Filter by topic">
        <button type="button" data-tag="all" aria-pressed="true">All</button>
        <button type="button" data-tag="Politics" aria-pressed="false">Politics</button>
        <button type="button" data-tag="QAnon" aria-pressed="false">QAnon</button>
        <button type="button" data-tag="UFO" aria-pressed="false">UFOs</button>
        <button type="button" data-tag="Cryptid" aria-pressed="false">Cryptids</button>
        <button type="button" data-tag="Strange" aria-pressed="false">Strange</button>
        <button type="button" data-tag="Odd" aria-pressed="false">Odd</button>
        <button type="button" data-tag="Science" aria-pressed="false">Science</button>
      </div>
      <div class="news-feed" id="news-feed">
{feed_html}
      </div>
      <p class="disclaimer">We link out to the original publishers. We never copy article bodies. Takes are skeptic entertainment — we roast spin on all sides and never invent factual claims about real people. Tragedy and death stories are filtered. If something sneaks through, blame the algorithm — then throw a party.</p>
    </div>
  </section>

  <section class="black">
    <div class="wrap center">
      <h2>Turn a headline into a <span class="r">party</span></h2>
      <p class="lead">Pick a weird story. Pitch a theory. Vote on awards. Conspiracy PowerPoint Night has the slides, host script and topic cards.</p>
      <p>
        <a class="btn" href="{PPT_URL}" target="_blank" rel="noopener sponsored">Get PowerPoint Night – $9.99</a>
        <a class="btn alt sm" href="{KIT_URL}" target="_blank" rel="noopener sponsored">Full Party Kit – 20% off LEAKED20</a>
      </p>
      <p style="margin-top:18px">
        <a class="btn sm" href="theory-generator.html">Theory Generator</a>
        <a class="btn sm" href="memes.html">Steal a Meme</a>
        <a class="btn sm" href="quiz-cryptid.html">Cryptid Quiz</a>
      </p>
    </div>
  </section>

  <section class="redbg">
    <div class="wrap signup">
      <span class="stamp" style="color:#fff;border-color:#fff">Classified</span>
      <h2>Join the Shadow Party Committee</h2>
      <p>Get a free Top Secret Agent ID Badge printable, plus new free files and party ideas. No spam, ever.</p>
      <form class="signup-form" data-signup data-connected="true" action="https://api.web3forms.com/submit" method="POST">
        <input type="hidden" name="access_key" value="{WEB3_KEY}">
        <input type="hidden" name="subject" value="New Shadow Party Committee recruit">
        <input type="hidden" name="from_name" value="Conspiraparty">
        <input type="hidden" name="redirect" value="https://conspiraparty.com/thanks.html">
        <input type="checkbox" name="botcheck" class="skip" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
        <input type="hidden" name="source_page" value="weird-news">
        <label class="skip" for="nm-wn">Name (optional)</label>
        <input id="nm-wn" type="text" name="name" placeholder="Cover name (optional)">
        <label class="skip" for="em-wn">Email</label>
        <input id="em-wn" type="email" name="email" placeholder="your.cover@email.com" required>
        <button class="btn alt" type="submit">Send My Free Badge</button>
        <span class="notice" role="status" aria-live="polite"></span>
      </form>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <nav aria-label="Footer">
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="party-essentials.html">Party Games</a></li>
        <li><a href="books.html">Books</a></li>
        <li><a href="apparel.html">Apparel</a></li>
        <li><a href="gifts.html">Gifts</a></li>
        <li><a href="supply-drop.html">Supply Drop</a></li>
        <li><a href="free-printables.html">Free Printables</a></li>
        <li><a href="memes.html">Memes</a></li>
        <li><a href="weird-news.html" aria-current="page">Weird News</a></li>
        <li><a href="shirts.html">Shirts</a></li>
        <li><a href="quiz.html">Quiz</a></li>
        <li><a href="gift-guide.html">Gift Guide</a></li>
        <li><a href="blog.html">Blog</a></li>
        <li><a href="friends-of-the-committee.html">Friends of the Committee</a></li>
        <li><a href="privacy.html">Privacy</a></li>
      </ul>
    </nav>
    <p class="disclosure">As an Amazon Associate, Conspiraparty earns from qualifying purchases. Some links on this site are affiliate links, which means we may earn a small commission at no extra cost to you.</p>
    <p>All conspiracies on this site are for entertainment. Question everything, especially us. © 2026 Conspiraparty.com</p>
  </div>
</footer>
<a class="sticky-cta" href="{KIT_URL}" target="_blank" rel="noopener sponsored">Get the Party Kit – 20% off</a>
<script src="assets/site.js" defer></script>
<script>
(function(){{
  var bar = document.querySelector('.filter-bar');
  if(bar){{
    var cards = Array.prototype.slice.call(document.querySelectorAll('.news-card'));
    bar.addEventListener('click', function(e){{
      var btn = e.target.closest('button[data-tag]');
      if(!btn) return;
      var tag = btn.getAttribute('data-tag');
      bar.querySelectorAll('button').forEach(function(b){{ b.setAttribute('aria-pressed', b===btn ? 'true' : 'false'); }});
      cards.forEach(function(c){{
        var show = tag === 'all' || c.getAttribute('data-tag') === tag;
        c.style.display = show ? '' : 'none';
      }});
    }});
  }}
}})();
(function(){{
  function canNativeShare(){{
    return typeof navigator !== 'undefined' && typeof navigator.share === 'function'
      && (window.matchMedia('(max-width:720px)').matches || /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent||''));
  }}
  document.addEventListener('click', function(e){{
    var shareBtn = e.target.closest('[data-share]');
    if(shareBtn){{
      var card = shareBtn.closest('.news-card');
      if(!card) return;
      var url = card.getAttribute('data-share-url') || (location.origin + location.pathname + '#' + card.id);
      var text = card.getAttribute('data-share-text') || document.title;
      if(canNativeShare()){{
        navigator.share({{ title: 'Conspiraparty Weird News', text: text, url: url }}).catch(function(){{}});
        return;
      }}
      var links = card.querySelector('.share-links');
      if(links){{
        links.hidden = !links.hidden;
      }}
      return;
    }}
    var copyBtn = e.target.closest('[data-copy]');
    if(copyBtn){{
      var card = copyBtn.closest('.news-card');
      if(!card) return;
      var url = card.getAttribute('data-share-url') || (location.origin + location.pathname + '#' + card.id);
      var done = function(){{
        copyBtn.classList.add('copied');
        copyBtn.textContent = 'Copied';
        setTimeout(function(){{ copyBtn.classList.remove('copied'); copyBtn.textContent = 'Copy link'; }}, 1600);
      }};
      if(navigator.clipboard && navigator.clipboard.writeText){{
        navigator.clipboard.writeText(url).then(done).catch(function(){{
          window.prompt('Copy link', url);
        }});
      }} else {{
        window.prompt('Copy link', url);
      }}
    }}
  }});
}})();
</script>
</body>
</html>
"""


def main() -> int:
    items = gather()
    now = datetime.now(timezone.utc)
    payload = {
        "generated_at": now.isoformat(),
        "generated_at_display": now.strftime("%b %d, %Y %H:%M"),
        "item_count": len(items),
        "feeds": [f["name"] for f in FEEDS],
        "items": items,
    }
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    HTML_PATH.write_text(render_html(items, payload["generated_at_display"]), encoding="utf-8")
    print(f"Wrote {len(items)} items → {DATA_PATH.relative_to(ROOT)} and {HTML_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
