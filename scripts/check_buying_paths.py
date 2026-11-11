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


banned = (
    "Coming soon to Etsy",
    "Full Cover-Up Bundle",
    "no bundle discount",
    "same invite twice",
    "homepage shop card",
    "product data",
    "not an add-on",
    "$20 customization",
    "$49",
    "event-use",
    "event license",
)

bonus = must_contain(
    "bonus-mission.html",
    "https://ko-fi.com/s/48c4007b56",
    "https://happyplaceinkandart.etsy.com/listing/4600479706",
    "https://ko-fi.com/s/e35cf6ce46",
    "https://happyplaceinkandart.etsy.com/listing/4502272966",
    "The download includes invitations",
    "Buy now – instant download",
    "Also on Etsy",
    "Who Leaked the Files? · $7.99",
    "Decor kit · $12.99",
    "Code LEAKED20 works on the decor kit on Ko-fi and at Etsy checkout.",
)
must_not("bonus-mission.html", *banned, text=bonus)

ppt = must_contain(
    "conspiraparty-ppt-night.html",
    "https://www.etsy.com/listing/4612273604/conspiracy-powerpoint-night-invitation",
    "https://ko-fi.com/s/0c00270052",
    "https://www.etsy.com/listing/4604436132/conspiracy-powerpoint-night-party-kit",
    "The full kit is $9.99 and includes the 5×7 invitation",
    "Invite only is $3.99",
    ">Invite only · $3.99</a>",
    "Buy now – instant download",
    "Also on Etsy",
)
must_not("conspiraparty-ppt-night.html", *banned, text=ppt)

index = must_contain(
    "index.html",
    'id="shop"',
    'id="conspiraparty-party-kit"',
    "The download includes invitations.",
    '<p class="price">$12.99</p><p class="card-cross">20% off with code LEAKED20</p>',
    "https://ko-fi.com/s/e35cf6ce46",
    "https://ko-fi.com/s/48c4007b56",
    "https://ko-fi.com/s/0c00270052",
    "https://ko-fi.com/s/c5f9f86f69",
    "https://ko-fi.com/s/af602f09e4",
    "Buy now – instant download",
    "Also on Etsy",
    "Code LEAKED20 works on Ko-fi and at Etsy checkout.",
    "on Ko-fi and Etsy.",
)

must_contain(
    "free-printables.html",
    'id="paid-kits"',
    "4612273604",
    "index.html#shop",
    "Invite only, $3.99",
    "PowerPoint Night full kit, $9.99",
    "Who Leaked the Files?, $7.99",
    "Decor kit, $12.99",
)
must_not("free-printables.html", *banned)
must_contain(
    "free-top-secret-party-invitation.html",
    "4612273604",
    "index.html#shop",
    ">Invite only · $3.99</a>",
    "The full kit is $9.99",
)
must_not("free-top-secret-party-invitation.html", *banned)
must_contain("join-the-agency.html", 'id="paid-kits"', "4612273604", "index.html#shop", "Invite only is $3.99", "$9.99", "$7.99")
must_not("join-the-agency.html", *banned)
must_contain("shop.html", "$9.99", "$3.99", "$7.99", "$12.99", "ko-fi.com/conspiraparty")
must_not("shop.html", *banned)
must_contain("field-guides.html", "$9.99", "$3.99", "$7.99")
must_not("field-guides.html", *banned)
must_contain("field-guides/roswell.html", "$9.99", "$3.99", "$7.99")
must_not("field-guides/roswell.html", *banned)
must_contain("shop.html", 'href="index.html#shop"', "noindex", "ko-fi.com/conspiraparty")
must_contain("404.html", 'href="index.html#shop"')
must_contain("field-guides.html", 'id="paid-kits"', "index.html#shop")
must_contain("field-guides/roswell.html", 'id="paid-kits"', "../index.html#shop")
must_contain("assets/style.css", ".buy-paths", ".sticky-cta:focus-visible", "min-height:44px")
must_contain("assets/style.css", "a.kofi-etsy")
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

kofi_anchor = re.compile(r'<a\b[^>]*href="https://ko-fi.com/s/[^"]*"[^>]*>.*?</a>', re.S)
for rel in ["index.html", "bonus-mission.html"]:
    for anchor in kofi_anchor.findall(read(rel)):
        if "ko-fi.com/widgets" in anchor or "kofiwidget" in anchor.lower():
            errors.append(f"{rel} embeds a Ko-fi widget")

must_not("index.html", "Enter LEAKED20 at Etsy checkout.", "ko-fi.com/widgets", "kofiwidget")
must_contain(
    "christmas-party-game.html",
    "https://ko-fi.com/s/c5f9f86f69",
    "https://happyplaceinkandart.etsy.com/listing/4601155493",
    "Buy now – instant download",
)
must_contain(
    "alien-gender-reveal-party-ideas.html",
    "https://ko-fi.com/s/af602f09e4",
    "https://happyplaceinkandart.etsy.com/listing/4601156509",
    "Buy now – instant download",
)
must_contain(
    "gift-guide.html",
    "https://ko-fi.com/s/e35cf6ce46",
    "https://ko-fi.com/s/48c4007b56",
    "https://ko-fi.com/s/0c00270052",
    "https://ko-fi.com/s/c5f9f86f69",
    "https://ko-fi.com/s/af602f09e4",
    "On Etsy, use LEAKED20.",
)


if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"buying paths ok ({len(pages)} pages)")
