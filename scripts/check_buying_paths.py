#!/usr/bin/env python3
"""Guard the current buying-path copy. Fails if a known mismatch returns."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []


def read(rel):
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing {rel}")
        return ""
    return path.read_text()


def must_contain(rel, *needles):
    text = read(rel)
    for needle in needles:
        if needle not in text:
            errors.append(f"{rel} missing {needle!r}")
    return text


def must_not(rel, *needles, text=None):
    text = read(rel) if text is None else text
    for needle in needles:
        if needle in text:
            errors.append(f"{rel} still contains {needle!r}")


bonus = must_contain(
    "bonus-mission.html",
    "https://happyplaceinkandart.etsy.com/listing/4600479706",
    "$7.99",
    "no bundle discount",
    "See Who Leaked on Etsy",
)
must_not(
    "bonus-mission.html",
    "Coming soon to Etsy",
    "Full Cover-Up Bundle",
    "bundle discount. Decor",
    text=bonus,
)

ppt = must_contain(
    "conspiraparty-ppt-night.html",
    "https://www.etsy.com/listing/4612273604/conspiracy-powerpoint-night-invitation",
    "$3.99",
    "https://www.etsy.com/listing/4604436132/conspiracy-powerpoint-night-party-kit",
    "already includes the 5×7 invite",
    "no bundle discount",
)
must_not(
    "conspiraparty-ppt-night.html",
    "$20",
    "$49",
    "customization",
    "event-use",
    "event license",
    text=ppt,
)

index = must_contain(
    "index.html",
    'id="shop"',
    'id="conspiraparty-party-kit"',
    "<p class=\"price\">$12.99</p><p class=\"card-cross\">20% off with code LEAKED20</p>",
)
# The flagship card should not go back to a discount-only price line.
if "<p class=\"price\">20% off with LEAKED20</p>" in index:
    errors.append("index.html flagship card dropped the $12.99 price")

must_contain(
    "free-printables.html",
    'id="paid-kits"',
    "4612273604",
    "index.html#shop",
)
must_contain(
    "free-top-secret-party-invitation.html",
    "4612273604",
    "$3.99",
    "index.html#shop",
)
must_contain("join-the-agency.html", 'id="paid-kits"', "4612273604", "index.html#shop")
must_contain("shop.html", 'href="index.html#shop"', "noindex", "ko-fi.com/conspiraparty")
must_contain("404.html", 'href="index.html#shop"')
must_contain("field-guides.html", 'id="paid-kits"', "index.html#shop")
must_contain("field-guides/roswell.html", 'id="paid-kits"', "../index.html#shop")
must_contain("assets/style.css", ".buy-paths", ".sticky-cta:focus-visible", "min-height:44px")
must_contain("scripts/build_field_guides.py", "GUIDE_PAID", "ko-fi.com/conspiraparty")
must_contain("scripts/build_beginner_hub.py", 'id="paid-kits"', "4612273604")
must_contain("products/pending-kits.json", "buying_path_evidence", "4612273604")

# Local links on the pages we touched should resolve.
pages = [
    "index.html",
    "bonus-mission.html",
    "conspiraparty-ppt-night.html",
    "free-printables.html",
    "free-top-secret-party-invitation.html",
    "join-the-agency.html",
    "shop.html",
    "404.html",
    "field-guides.html",
]
pages += [str(p.relative_to(ROOT)) for p in (ROOT / "field-guides").glob("*.html")]
href_re = re.compile(r"""(?:href|src)=["']([^"']+)""")
for rel in pages:
    text = read(rel)
    page = ROOT / rel
    for href in href_re.findall(text):
        raw = href.split("#", 1)[0].split("?", 1)[0].strip()
        if not raw or raw.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//")):
            continue
        target = (ROOT / raw.lstrip("/")) if raw.startswith("/") else (page.parent / raw).resolve()
        if not str(target).startswith(str(ROOT)):
            errors.append(f"{rel} escapes repo: {href}")
            continue
        if not target.exists():
            errors.append(f"{rel} broken local link {href}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"buying paths ok ({len(pages)} pages)")
