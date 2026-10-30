#!/usr/bin/env python3
"""Fetch multi-source Breaking headlines for each Rabbit Hole Map topic.

Writes data/rhmap-news.json. Daily routine (8:45 AM MT) should run:
  python3 scripts/fetch_rhmap_news.py

Labels each item Mainstream / Independent / Believers. Keeps at least as
many non-mainstream as mainstream per topic (max 6). No verdict wording.
"""
from __future__ import annotations

import hashlib
import html as html_lib
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "rhmap-news.json"
MAP = ROOT / "data" / "rabbit-hole-map.json"
USER_AGENT = "ConspirapartyRhMapNews/1.0 (+https://conspiraparty.com; daily aggregator)"
MAX_PER_TOPIC = 6

# Headlines that hand down a verdict are skipped (site voice: no verdicts).
VERDICT = re.compile(r"\b(debunk\w*|fact[- ]?check\w*|false claims?|misinformation|disinformation|baseless)\b", re.I)
CTX = ssl.create_default_context()

# Topic → Google News query keywords
TOPIC_QUERIES: dict[str, str] = {
    "qanon": "QAnon OR \"Q Anon\"",
    "nine11": "9/11 OR \"September 11\" OR \"World Trade Center\" attack",
    "uap": "UAP OR UFO OR \"unidentified anomalous\" OR \"unidentified aerial\"",
    "epstein": "Epstein OR \"Jeffrey Epstein\" OR \"Epstein files\"",
    "jfk": "\"JFK assassination\" OR \"John F. Kennedy\" assassination OR Warren Commission",
    "moon": "\"moon landing\" OR \"Apollo 11\" OR \"lunar landing\"",
    "deepstate": "\"deep state\" OR \"administrative state\" OR \"intelligence community\"",
    "election2016": "\"2016 election\" OR \"election interference\" 2016 OR \"Russia collusion\"",
    "election2020": "\"2020 election\" OR \"election integrity\" 2020 OR \"election denial\"",
    "covid": "\"COVID origins\" OR \"lab leak\" OR \"Wuhan Institute\" OR \"SARS-CoV-2 origin\"",
    "chemtrails": "chemtrails OR geoengineering OR \"solar radiation management\" OR \"cloud seeding\"",
    "mkultra": "MKUltra OR \"MK Ultra\" OR \"CIA mind control\"",
    "area51": "\"Area 51\" OR \"Nevada Test and Training Range\"",
    "bigfoot": "Bigfoot OR Sasquatch OR cryptid",
    "flatearth": "\"flat earth\" OR flerfer",
    "birds": "\"birds aren't real\" OR \"birds arent real\" OR \"Birds Aren't Real\"",
    "rothschilds": "Rothschild OR Rothschilds banking OR \"Rothschild family\"",
    "fed": "\"Federal Reserve\" OR \"Fed rate\" OR \"Jerome Powell\" OR FOMC",
    "bilderberg": "Bilderberg OR \"World Economic Forum\" OR \"WEF Davos\"",
}

# Shared independent / believer outlet feeds (scored against topic keywords)
OUTLET_FEEDS = [
    {"name": "ZeroHedge", "url": "https://feeds.feedburner.com/zerohedge/feed", "kind": "Independent"},
    {"name": "The Grayzone", "url": "https://thegrayzone.com/feed/", "kind": "Independent"},
    {"name": "MintPress News", "url": "https://www.mintpressnews.com/feed/", "kind": "Independent"},
    {"name": "Unlimited Hangout", "url": "https://unlimitedhangout.com/feed/", "kind": "Believers"},
    {"name": "Rumble (via Google News)", "url": "https://news.google.com/rss/search?q=site:rumble.com+(UFO+OR+UAP+OR+Epstein+OR+QAnon+OR+%22deep+state%22+OR+%22flat+earth%22+OR+chemtrails)&hl=en-US&gl=US&ceid=US:en", "kind": "Believers"},
    {"name": "The Black Vault", "url": "https://www.theblackvault.com/documentarchive/feed/", "kind": "Independent"},
    {"name": "The Debrief", "url": "https://thedebrief.org/feed/", "kind": "Independent"},
]

# Mainstream outlet feeds (keyword-filtered into topics)
MAIN_FEEDS = [
    {"name": "BBC News", "url": "https://feeds.bbci.co.uk/news/world/rss.xml", "kind": "Mainstream"},
    {"name": "NPR", "url": "https://feeds.npr.org/1001/rss.xml", "kind": "Mainstream"},
    {"name": "The Guardian", "url": "https://www.theguardian.com/world/rss", "kind": "Mainstream"},
    {"name": "Politico", "url": "https://rss.politico.com/politics-news.xml", "kind": "Mainstream"},
]

# Topic keyword stems used to match outlet feed items into nodes
TOPIC_MATCH: dict[str, list[str]] = {
    "qanon": ["qanon", "q anon", "deep state"],
    "nine11": ["9/11", "september 11", "world trade center", "wtc"],
    "uap": ["uap", "ufo", "unidentified aerial", "unidentified anomalous", "flying saucer"],
    "epstein": ["epstein"],
    "jfk": ["jfk", "kennedy assassination", "warren commission", "lee harvey"],
    "moon": ["moon landing", "apollo 11", "lunar landing", "nasa moon"],
    "deepstate": ["deep state", "administrative state", "intelligence community", "cia ", "nsa "],
    "election2016": ["2016 election", "russia collusion", "mueller"],
    "election2020": ["2020 election", "election integrity", "stolen election", "jan. 6", "january 6"],
    "covid": ["covid", "lab leak", "wuhan", "sars-cov", "coronavirus origin"],
    "chemtrails": ["chemtrail", "geoengineering", "solar radiation", "cloud seeding"],
    "mkultra": ["mkultra", "mk ultra", "mind control"],
    "area51": ["area 51", "groom lake"],
    "bigfoot": ["bigfoot", "sasquatch", "cryptid", "skunk ape"],
    "flatearth": ["flat earth", "flerfer"],
    "birds": ["birds aren't real", "birds arent real"],
    "rothschilds": ["rothschild"],
    "fed": ["federal reserve", "fed rate", "jerome powell", "fomc", "central bank"],
    "bilderberg": ["bilderberg", "world economic forum", "wef ", "davos"],
}

MAINSTREAM_HOST_HINTS = (
    "bbc.", "npr.org", "reuters.", "apnews.", "ap.org", "nytimes.", "washingtonpost.",
    "theguardian.", "cnn.", "nbcnews.", "cbsnews.", "abcnews.", "politico.",
    "wsj.", "bloomberg.", "usatoday.", "latimes.", "nypost.", "foxnews.",
    "news.google.com", "associated press",
)
BELIEVER_HOST_HINTS = (
    "unlimitedhangout.", "whitneywebb", "rumble.com", "bitchute.", "odysee.",
    "infowars.", "naturalnews.", "thegatewaypundit.", "beforeitsnews.",
)
INDEPENDENT_HOST_HINTS = (
    "zerohedge.", "thegrayzone.", "mintpress", "theblackvault.", "thedebrief.",
    "liberationtimes.", "intercept.", "consortiumnews.", "responsible statecraft",
)


def fetch_bytes(url: str, timeout: int = 20) -> bytes | None:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            return resp.read()
    except Exception as e:
        print(f"  FAIL {url}: {e}", file=sys.stderr)
        return None


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def text_of(el: ET.Element | None) -> str:
    if el is None:
        return ""
    parts = [el.text or ""]
    for child in el:
        parts.append(text_of(child))
        parts.append(child.tail or "")
    return "".join(parts).strip()


def clean_title(t: str) -> str:
    t = html_lib.unescape(re.sub(r"<[^>]+>", "", t or "")).strip()
    t = re.sub(r"\s+", " ", t)
    # strip trailing " - Source" sometimes duplicated
    return t[:220]


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
    # ISO-ish
    try:
        return datetime.fromisoformat(pub.replace("Z", "+00:00"))
    except Exception:
        return None


def display_date(dt: datetime | None) -> str:
    if not dt:
        return ""
    return dt.astimezone(timezone.utc).strftime("%b %-d, %Y")


def parse_rss(data: bytes) -> list[dict]:
    items: list[dict] = []
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        print(f"  FAIL parse: {e}", file=sys.stderr)
        return items
    # RSS items
    for item in root.iter():
        if local(item.tag) != "item":
            continue
        title = link = pub = source = ""
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
            elif t == "updated" and not pub:
                pub = (child.text or "").strip()
        if title and link:
            items.append({"title": clean_title(title), "link": link, "pub": pub, "source": source})
    # Atom entries
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
                    href = child.get("href", "")
                    if href and (child.get("rel") in (None, "alternate") or not link):
                        link = href
                elif t in ("updated", "published") and not pub:
                    pub = (child.text or "").strip()
            if title and link:
                items.append({"title": clean_title(title), "link": link, "pub": pub, "source": ""})
    return items


def google_news_url(query: str) -> str:
    q = urllib.parse.quote(query)
    return f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"


def host_of(url: str) -> str:
    try:
        return urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")
    except Exception:
        return ""


def classify_kind(default: str, source: str, url: str) -> str:
    blob = f"{source} {url} {host_of(url)}".lower()
    if any(h in blob for h in BELIEVER_HOST_HINTS):
        return "Believers"
    if any(h in blob for h in INDEPENDENT_HOST_HINTS):
        return "Independent"
    if any(h in blob for h in MAINSTREAM_HOST_HINTS):
        return "Mainstream"
    if default:
        return default
    return "Independent"


def source_label(feed_name: str, item: dict) -> str:
    if item.get("source"):
        return item["source"]
    # Google News titles often end with " - Outlet"
    title = item.get("title", "")
    if " - " in title and "Google" in feed_name:
        left, right = title.rsplit(" - ", 1)
        if 2 <= len(right) <= 60:
            item["title"] = left.strip()
            return right.strip()
    host = host_of(item.get("link", ""))
    if host:
        return host
    return feed_name


def matches_topic(text: str, topic_id: str) -> bool:
    stems = TOPIC_MATCH.get(topic_id, [])
    tl = text.lower()
    return any(s in tl for s in stems)


def dedupe_key(title: str, url: str) -> str:
    norm = re.sub(r"[^a-z0-9]+", "", title.lower())[:80]
    return hashlib.sha1((norm + "|" + host_of(url)).encode()).hexdigest()[:16]


def balance_pick(cands: list[dict], limit: int = MAX_PER_TOPIC) -> list[dict]:
    """Prefer recent; keep non-mainstream count >= mainstream."""
    cands = sorted(cands, key=lambda x: x.get("_ts") or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    non_c = [c for c in cands if c["kind"] != "Mainstream"]
    main_c = [c for c in cands if c["kind"] == "Mainstream"]
    target_non = (limit + 1) // 2
    picked: list[dict] = []
    seen: set[str] = set()

    def add_from(pool: list[dict], n: int) -> None:
        for it in pool:
            if len(picked) >= limit or n <= 0:
                return
            if it["dedupe"] in seen:
                continue
            seen.add(it["dedupe"])
            picked.append(dict(it))
            n -= 1

    add_from(non_c, min(target_non, limit))
    add_from(main_c, limit - len(picked))
    add_from(non_c, limit - len(picked))
    add_from(main_c, limit - len(picked))

    while True:
        main_n = sum(1 for p in picked if p["kind"] == "Mainstream")
        non_n = len(picked) - main_n
        if non_n >= main_n:
            break
        unused = [c for c in non_c if c["dedupe"] not in seen]
        if not unused:
            break
        swapped = False
        for i in range(len(picked) - 1, -1, -1):
            if picked[i]["kind"] == "Mainstream":
                seen.discard(picked[i]["dedupe"])
                it = unused[0]
                seen.add(it["dedupe"])
                picked[i] = dict(it)
                swapped = True
                break
        if not swapped:
            break

    return picked[:limit]



def item_record(feed_name: str, raw: dict, kind_default: str) -> dict:
    src = source_label(feed_name, raw)
    url = raw["link"]
    title = raw["title"]
    dt = parse_date(raw.get("pub", ""))
    kind = classify_kind(kind_default, src, url)
    return {
        "title": title,
        "url": url,
        "source": src,
        "kind": kind,
        "published_display": display_date(dt),
        "published_iso": dt.isoformat() if dt else "",
        "dedupe": dedupe_key(title, url),
        "_ts": dt or datetime.min.replace(tzinfo=timezone.utc),
        "_feed": feed_name,
    }


def main() -> int:
    node_ids = list(TOPIC_QUERIES.keys())
    if MAP.exists():
        try:
            nodes = json.loads(MAP.read_text()).get("nodes", [])
            ids = [n["id"] for n in nodes]
            if ids:
                node_ids = ids
        except Exception:
            pass

    buckets: dict[str, list[dict]] = {nid: [] for nid in node_ids}
    feed_status: dict[str, str] = {}

    # 1) Per-topic Google News
    for nid in node_ids:
        q = TOPIC_QUERIES.get(nid)
        if not q:
            continue
        url = google_news_url(q)
        print(f"GN {nid}…")
        raw = fetch_bytes(url)
        if not raw:
            feed_status[f"GN:{nid}"] = "fail"
            continue
        feed_status[f"GN:{nid}"] = "ok"
        for it in parse_rss(raw)[:20]:
            # GN is a mix; default Independent unless outlet is clearly mainstream
            rec = item_record(f"Google News · {nid}", it, "Independent")
            rec["kind"] = classify_kind("Independent", rec["source"], rec["url"])
            buckets[nid].append(rec)
        # Independent / believer-tilted Google News pass
        q2 = q + ' (ZeroHedge OR Grayzone OR MintPress OR "Black Vault" OR Rumble OR Substack OR "Unlimited Hangout" OR Debrief)'
        raw2 = fetch_bytes(google_news_url(q2))
        feed_status[f"GN-indie:{nid}"] = "ok" if raw2 else "fail"
        if raw2:
            for it in parse_rss(raw2)[:12]:
                rec = item_record(f"Google News indie · {nid}", it, "Independent")
                rec["kind"] = classify_kind("Independent", rec["source"], rec["url"])
                if rec["kind"] == "Mainstream":
                    rec["kind"] = "Independent"
                buckets[nid].append(rec)

    # 2) Outlet feeds → match into topics
    for feed in OUTLET_FEEDS + MAIN_FEEDS:
        print(f"Feed {feed['name']}…")
        raw = fetch_bytes(feed["url"])
        if not raw or raw.lstrip()[:1] not in (b"<", b"\xef"):  # rough XML check
            # still try parse
            if not raw:
                feed_status[feed["name"]] = "fail"
                continue
        if raw and b"<html" in raw[:200].lower():
            print(f"  SKIP {feed['name']}: HTML not RSS", file=sys.stderr)
            feed_status[feed["name"]] = "html"
            continue
        items = parse_rss(raw or b"")
        if not items:
            feed_status[feed["name"]] = "empty"
            continue
        feed_status[feed["name"]] = f"ok:{len(items)}"
        for it in items[:40]:
            blob = f"{it['title']} {it.get('link','')}"
            matched = [nid for nid in node_ids if matches_topic(blob, nid)]
            if not matched:
                continue
            rec = item_record(feed["name"], it, feed["kind"])
            for nid in matched:
                buckets[nid].append(dict(rec))

    # Assemble
    now = datetime.now(timezone.utc)
    topics_out: dict[str, list[dict]] = {}
    counts: dict[str, int] = {}
    for nid in node_ids:
        picked = balance_pick([c for c in buckets.get(nid, []) if not VERDICT.search(c.get("title", ""))])
        clean = []
        for p in picked:
            clean.append({
                "title": p["title"],
                "url": p["url"],
                "source": p["source"],
                "kind": p["kind"],
                "published_display": p["published_display"],
                "published_iso": p.get("published_iso", ""),
            })
        topics_out[nid] = clean
        counts[nid] = len(clean)
        kinds = {}
        for p in clean:
            kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
        print(f"  {nid}: {len(clean)} {kinds}")

    payload = {
        "generated_at": now.isoformat(),
        "generated_at_display": now.strftime("%b %-d, %Y %-I:%M %p UTC"),
        "script": "scripts/fetch_rhmap_news.py",
        "max_per_topic": MAX_PER_TOPIC,
        "feed_status": feed_status,
        "topics": topics_out,
        "counts": counts,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT} total={sum(counts.values())}")
    ok = [k for k, v in feed_status.items() if str(v).startswith("ok")]
    fail = [k for k, v in feed_status.items() if not str(v).startswith("ok")]
    print("feeds_ok:", ", ".join(ok))
    if fail:
        print("feeds_fail:", ", ".join(f"{k}={feed_status[k]}" for k in fail))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
