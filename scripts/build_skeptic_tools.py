#!/usr/bin/env python3
"""Generate skeptic-tools preview pages (do not push to main)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACCESS = "a2adf9e4-98f3-48cf-ab94-208e1705280b"

NAV = """<ul><li><a href="start-here.html">Start Here</a></li><li><a href="skeptic-tools.html"{cur_hub}>Skeptic Tools</a></li><li><a href="index.html#kit">Party Kit</a></li><li><a href="free-printables.html">Free</a></li><li><a href="blog/index.html">Blog</a></li><li><a href="memes.html">Memes</a></li><li><a href="weird-news.html">Weird News</a></li><li><a href="field-guides.html">Field Guides</a></li><li><a href="shirts.html">Shirts</a></li><li><a href="quiz.html">Quiz</a></li><li><a href="gift-guide.html">Gifts</a></li></ul>"""

STRIP = """<p class="sk-strip">
<a href="skeptic-tools.html"{a0}>Skeptic Tools</a> ·
<a href="document-vault.html"{a1}>Document Vault</a> ·
<a href="timeline.html"{a2}>Timeline</a> ·
<a href="scoreboard.html"{a3}>Scoreboard</a> ·
<a href="submit.html"{a4}>Community Corkboard</a> ·
<a href="weekly-dig.html"{a5}>Weekly Dig</a> ·
<a href="follow-the-money.html"{a6}>Follow the Money</a>
</p>"""

FOOT = """<footer><div class="wrap"><nav aria-label="Footer"><ul>
<li><a href="index.html">Home</a></li>
<li><a href="start-here.html">Start Here</a></li>
<li><a href="skeptic-tools.html">Skeptic Tools</a></li>
<li><a href="document-vault.html">Document Vault</a></li>
<li><a href="timeline.html">Timeline</a></li>
<li><a href="scoreboard.html">Prediction Scoreboard</a></li>
<li><a href="submit.html">Community Corkboard</a></li>
<li><a href="weekly-dig.html">Weekly Dig</a></li>
<li><a href="follow-the-money.html">Follow the Money</a></li>
<li><a href="weird-news.html">Weird News</a></li>
<li><a href="true-stories.html">True Stories</a></li>
<li><a href="glossary.html">Glossary</a></li>
<li><a href="field-guides.html">Field Guides</a></li>
<li><a href="shirts.html">Shirts</a></li>
<li><a href="free-printables.html">Free Printables</a></li>
<li><a href="blog/index.html">Blog</a></li>
</ul></nav>
<p class="disclosure">As an Amazon Associate, Conspiraparty earns from qualifying purchases. Some links on this site are affiliate links, which means we may earn a small commission at no extra cost to you.</p>
<p class="x-follow"><a href="https://x.com/conspiraparty" target="_blank" rel="noopener">Follow @conspiraparty on X</a></p>
<p>All conspiracies on this site are for entertainment and critical thinking. Question everything, especially us. © 2026 Conspiraparty.com</p></div></footer>
<a class="sticky-cta" href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored">Get the Party Kit – 20% off</a>
<script src="assets/site.js" defer></script>
<script src="assets/share.js" defer></script>
<script src="assets/skeptic-tools.js" defer></script>
"""

DISCLAIMER = """<p class="sk-note"><strong>How to dig:</strong> Primary documents first. Label every voice. We do not hand you a belief. Political rabbit holes roast <em>all</em> sides. Judge for yourself.</p>"""

def page(slug, title, desc, body, strip_idx=0, extra_head="", path_prefix=""):
    cur = ['']*7
    if 0 <= strip_idx < 7:
        cur[strip_idx] = ' aria-current="page"'
    strip = STRIP.format(a0=cur[0], a1=cur[1], a2=cur[2], a3=cur[3], a4=cur[4], a5=cur[5], a6=cur[6])
    nav = NAV.format(cur_hub=' aria-current="page"' if strip_idx == 0 else '')
    css_prefix = path_prefix
    share_url = f"https://conspiraparty.com/{slug}"
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Conspiraparty</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{share_url}">
<meta property="og:site_name" content="Conspiraparty">
<meta property="og:title" content="{title} | Conspiraparty">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{share_url}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://conspiraparty.com/assets/og/index.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} | Conspiraparty">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://conspiraparty.com/assets/og/index.jpg">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="{css_prefix}assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="{css_prefix}assets/img/apple-touch-icon.png">
<link rel="preload" href="{css_prefix}assets/fonts/Anton-Regular.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="{css_prefix}assets/style.css?v=sk1">
<link rel="stylesheet" href="{css_prefix}assets/share.css">
<link rel="stylesheet" href="{css_prefix}assets/skeptic-tools.css?v=sk1">
{extra_head}
</head>
<body><a class="skip" href="#main">Skip to content</a>
<div class="promo">20% off the full printable kit with code <a href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored">LEAKED20</a></div>
<header class="top"><div class="bar"><a class="logo" href="{css_prefix}index.html"><img src="{css_prefix}assets/img/logo.png" alt="Conspiraparty.com – Top Secret Party Kit" width="220" height="70"></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button></div>
<nav class="main" id="nav" aria-label="Main">{nav}</nav></header>
<main id="main">
{body.replace('__STRIP__', strip).replace('__SHARE__', f'''<div class="share-box page-share" data-share-url="{share_url}" data-share-text="{title} — via conspiraparty.com" data-share-image="https://conspiraparty.com/assets/og/index.jpg"><button class="btn sm share-native" data-share type="button">Share this</button><div class="share-links" hidden><a class="btn sm" href="https://x.com/intent/post?text={title.replace(' ', '%20')}%20%E2%80%94%20via%20conspiraparty.com&amp;url={share_url.replace(':','%3A').replace('/','%2F')}" rel="noopener noreferrer" target="_blank">X</a><button class="btn sm share-copy" data-copy type="button">Copy link</button></div></div>''')}
</main>
{FOOT.replace('assets/', css_prefix + 'assets/').replace('href="', 'href="' + css_prefix) if False else FOOT}
"""
    # Fix footer asset paths for nested pages
    if path_prefix:
        html = html.replace('src="assets/', f'src="{path_prefix}assets/')
        html = html.replace('href="assets/', f'href="{path_prefix}assets/')
        # careful: also fix sticky and internal - FOOT already has relative links without prefix for sibling pages
        # For weekly-dig/issue, need ../ for site pages
        html = html.replace('href="index.html"', f'href="{path_prefix}index.html"')
        html = html.replace('href="start-here.html"', f'href="{path_prefix}start-here.html"')
        html = html.replace('href="skeptic-tools.html"', f'href="{path_prefix}skeptic-tools.html"')
        html = html.replace('href="document-vault.html"', f'href="{path_prefix}document-vault.html"')
        html = html.replace('href="timeline.html"', f'href="{path_prefix}timeline.html"')
        html = html.replace('href="scoreboard.html"', f'href="{path_prefix}scoreboard.html"')
        html = html.replace('href="submit.html"', f'href="{path_prefix}submit.html"')
        html = html.replace('href="weekly-dig.html"', f'href="{path_prefix}weekly-dig.html"')
        html = html.replace('href="follow-the-money.html"', f'href="{path_prefix}follow-the-money.html"')
        html = html.replace('href="weird-news.html"', f'href="{path_prefix}weird-news.html"')
        html = html.replace('href="true-stories.html"', f'href="{path_prefix}true-stories.html"')
        html = html.replace('href="glossary.html"', f'href="{path_prefix}glossary.html"')
        html = html.replace('href="field-guides.html"', f'href="{path_prefix}field-guides.html"')
        html = html.replace('href="shirts.html"', f'href="{path_prefix}shirts.html"')
        html = html.replace('href="free-printables.html"', f'href="{path_prefix}free-printables.html"')
        html = html.replace('href="blog/index.html"', f'href="{path_prefix}blog/index.html"')
        html = html.replace('action="https://api.web3forms.com/submit"', 'action="https://api.web3forms.com/submit"')
    out = ROOT / slug
    out.parent.mkdir(parents=True, exist_ok=True)
    # Fix FOOT scripts when path_prefix - already handled via replace assets
    if path_prefix:
        html = html.replace('<script src="assets/', f'<script src="{path_prefix}assets/')
    out.write_text(html)
    print('wrote', out.relative_to(ROOT))


# ---- Hub ----
page('skeptic-tools.html', 'Skeptic Tools',
     'Document vault, timelines, prediction scoreboard, community corkboard, weekly dig, and follow-the-money cards. Dig primary documents. Judge for yourself.',
     f'''
<section class="hero"><div class="wrap center">
<h1>SKEPTIC <span class="r">TOOLS</span></h1>
<p class="sk-lead">For people who want primary documents, timelines, and hard questions — not a sermon. Pick a tool. Dig in yourself.</p>
__SHARE__
__STRIP__
</div></section>
<section class="black"><div class="wrap">
{DISCLAIMER}
<div class="sk-grid hub">
<a class="sk-hub-card" href="document-vault.html"><h3>Document Vault</h3><p>Searchable declassified files &amp; primary docs with plain-English summaries.</p></a>
<a class="sk-hub-card" href="timeline.html"><h3>Timeline Mode</h3><p>What was claimed vs what surfaced later — dated, with record links.</p></a>
<a class="sk-hub-card" href="scoreboard.html"><h3>Prediction Scoreboard</h3><p>Called it vs still open. Theories later put on the record — and the ones still fighting.</p></a>
<a class="sk-hub-card" href="submit.html"><h3>Community Corkboard</h3><p>Send a topic or a connection. Traci approves before it goes up.</p></a>
<a class="sk-hub-card" href="weekly-dig.html"><h3>Weekly Dig Email</h3><p>One rabbit hole a week. Primary documents to read yourself.</p></a>
<a class="sk-hub-card" href="follow-the-money.html"><h3>Follow the Money</h3><p>Who funded, who profited, who testified — with record links.</p></a>
</div>
<p class="sk-hint">Related: <a href="start-here.html" style="color:#fff;text-decoration:underline">Rabbit Hole Map</a> · <a href="true-stories.html" style="color:#fff;text-decoration:underline">Sounds Fake, Actually Happened</a> · <a href="weird-news.html" style="color:#fff;text-decoration:underline">Weird News</a></p>
<p class="sk-hint" style="margin-top:8px">Hosting a dig night? The <a href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored" style="color:#fff;text-decoration:underline">printable party kit</a> makes a solid prop table — optional, not required.</p>
</div></section>
''', 0)

# ---- Vault ----
page('document-vault.html', 'Document Vault',
     'Searchable vault of declassified and primary documents: JFK releases, MKUltra, UAP hearings, Epstein court files, Church Committee, Northwoods, Tonkin, and more.',
     f'''
<section class="hero"><div class="wrap center">
<h1>DOCUMENT <span class="r">VAULT</span></h1>
<p class="sk-lead">Declassified files, hearings, and court records — with a plain-English summary. Open the record. Make up your own mind.</p>
__SHARE__
__STRIP__
</div></section>
<section class="black" id="vault-app"><div class="wrap">
{DISCLAIMER}
<div class="sk-toolbar">
<label class="skip" for="vault-q">Search</label>
<input id="vault-q" type="search" placeholder="Search title, agency, tag…" autocomplete="off">
<label class="skip" for="vault-topic">Topic</label>
<select id="vault-topic"><option value="">All topics</option></select>
</div>
<p class="sk-count" id="vault-count"></p>
<div id="vault-list"></div>
</div></section>
''', 1)

# ---- Timeline ----
page('timeline.html', 'Timeline Mode',
     'Pick a topic. See what was claimed, then what surfaced later — with links to what\'s on the record.',
     f'''
<section class="hero"><div class="wrap center">
<h1>TIMELINE <span class="r">MODE</span></h1>
<p class="sk-lead">Claims have dates. Releases have dates. Put them next to each other.</p>
__SHARE__
__STRIP__
</div></section>
<section class="black" id="timeline-app"><div class="wrap">
{DISCLAIMER}
<div class="sk-toolbar">
<label for="timeline-topic" style="color:#fff;font-weight:700">Topic</label>
<select id="timeline-topic" aria-label="Choose topic"></select>
</div>
<div id="timeline-stage"></div>
</div></section>
''', 2)

# ---- Scoreboard ----
page('scoreboard.html', 'Prediction Scoreboard',
     'Called it vs still open: theories later confirmed by the public record, next to the ones still unresolved. Record links on every card.',
     f'''
<section class="hero"><div class="wrap center">
<h1>PREDICTION <span class="r">SCOREBOARD</span></h1>
<p class="sk-lead"><strong>Called it</strong> = later put on the public record. <strong>Still open</strong> = still contested. No trophies from us — just the trail.</p>
__SHARE__
__STRIP__
</div></section>
<section class="black" id="scoreboard-app"><div class="wrap">
{DISCLAIMER}
<div class="sk-cols">
<div>
<h2 class="sk-col-h called">Called it</h2>
<div id="score-called"></div>
</div>
<div>
<h2 class="sk-col-h open">Still open</h2>
<div id="score-open"></div>
</div>
</div>
</div></section>
''', 3)

# ---- Submit / corkboard ----
page('submit.html', 'Community Corkboard',
     'Submit a rabbit-hole topic or a new connection with sources. Traci reviews before anything is posted. Reader leads appear after approval.',
     f'''
<section class="hero"><div class="wrap center">
<h1>COMMUNITY <span class="r">CORKBOARD</span></h1>
<p class="sk-lead">Got a topic, a connection, or a primary document we missed? Pin it. Nothing goes live until it is approved.</p>
__SHARE__
__STRIP__
</div></section>
<section class="black"><div class="wrap">
{DISCLAIMER}
<div class="sk-form">
<h2 style="color:#111!important;font-family:var(--font-body);text-transform:none;font-size:1.4rem;font-weight:800">Submit a lead</h2>
<p class="hint">Include sources when you can. Political takes are fine if you roast fairly and link out. No harassment, no unverified crime claims about private people.</p>
<form action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="{ACCESS}">
<input type="hidden" name="subject" value="Conspiraparty Community Corkboard submission">
<input type="hidden" name="from_name" value="Conspiraparty Corkboard">
<input type="hidden" name="redirect" value="https://conspiraparty.com/thanks.html">
<input type="checkbox" name="botcheck" class="skip" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
<input type="hidden" name="source_page" value="community-corkboard">
<label for="lead-type">Type</label>
<select id="lead-type" name="lead_type" required>
<option value="topic">New topic</option>
<option value="connection">New connection between topics</option>
<option value="document">Primary document we should add</option>
<option value="other">Other</option>
</select>
<label for="lead-title">Title</label>
<input id="lead-title" type="text" name="title" required maxlength="140" placeholder="Short label for the pin">
<label for="lead-body">What should we dig?</label>
<textarea id="lead-body" name="message" required rows="5" maxlength="4000" placeholder="Your tip, the connection, and why it matters…"></textarea>
<label for="lead-sources">Sources (URLs)</label>
<textarea id="lead-sources" name="sources" rows="3" maxlength="2000" placeholder="https://… one per line. Primary document / Independent / Believers / Mainstream — label them if you can."></textarea>
<label for="lead-email">Email (optional — only if you want a reply)</label>
<input id="lead-email" type="email" name="email" autocomplete="email" placeholder="you@email.com">
<button class="btn" type="submit">Send to the corkboard</button>
</form>
</div>
</div></section>
<section class="cork"><div class="wrap">
<h2 class="center">Reader leads</h2>
<p class="center" style="color:#111;max-width:36rem;margin:0 auto 16px">Approved pins only. Empty until the first batch clears review.</p>
<div id="leads-app"></div>
</div></section>
''', 4)

# ---- Weekly dig ----
page('weekly-dig.html', 'Weekly Dig Email',
     'One rabbit hole a week with primary documents to read yourself. Free signup. Sample Issue 01 inside.',
     f'''
<section class="hero"><div class="wrap center">
<h1>WEEKLY <span class="r">DIG</span></h1>
<p class="sk-lead">One rabbit hole a week. Primary documents, a short brief, and questions to ask a friend. No spam sermon — just the homework.</p>
__SHARE__
__STRIP__
</div></section>
<section class="black"><div class="wrap">
{DISCLAIMER}
<div class="sk-grid two">
<div class="sk-signup">
<h3>Get the Weekly Dig</h3>
<p>Fridays. Short. Linked to the vault and the map. Unsubscribe anytime.</p>
<form class="signup-form" data-signup data-connected="true" action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="{ACCESS}">
<input type="hidden" name="subject" value="Weekly Dig signup">
<input type="hidden" name="from_name" value="Conspiraparty Weekly Dig">
<input type="hidden" name="redirect" value="https://conspiraparty.com/thanks.html">
<input type="checkbox" name="botcheck" class="skip" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
<input type="hidden" name="source_page" value="weekly-dig">
<input type="hidden" name="list" value="weekly-dig">
<label class="skip" for="wd-name">Name</label>
<input id="wd-name" type="text" name="name" placeholder="Cover name (optional)" autocomplete="name">
<label class="skip" for="wd-email">Email</label>
<input id="wd-email" type="email" name="email" required placeholder="your.cover@email.com" autocomplete="email">
<button class="btn" type="submit">Subscribe</button>
<span class="notice" role="status" aria-live="polite"></span>
</form>
</div>
<article class="sk-card">
<h3>What you get</h3>
<ul>
<li>One topic from the Rabbit Hole Map</li>
<li>2–4 Dig in yourself links (Primary / Mainstream / Independent / Believers)</li>
<li>3 talk prompts for friends or group chat</li>
<li>Optional hint at a printable or field guide — never the whole pitch</li>
</ul>
<p><a href="weekly-dig/issue-01.html"><strong>Read sample Issue 01 →</strong></a></p>
</article>
</div>
</div></section>
''', 5)

# ---- Follow the money ----
page('follow-the-money.html', 'Follow the Money',
     'Cards per topic: who funded, who profited, who testified — with links to what\'s on the record.',
     f'''
<section class="hero"><div class="wrap center">
<h1>FOLLOW THE <span class="r">MONEY</span></h1>
<p class="sk-lead">Funding trails, profit motives, and sworn testimony. Correlation is not a plot proof — it is a trail to walk.</p>
__SHARE__
__STRIP__
</div></section>
<section class="black" id="money-app"><div class="wrap">
{DISCLAIMER}
<div class="sk-toolbar">
<label for="money-topic" style="color:#fff;font-weight:700">Topic</label>
<select id="money-topic" aria-label="Choose topic"></select>
</div>
<div id="money-stage"></div>
</div></section>
''', 6)

# ---- Issue 01 ----
# Custom builder for nested path
issue_body = f'''
<section class="hero"><div class="wrap center">
<h1>WEEKLY DIG <span class="r">#01</span></h1>
<p class="sk-lead">Gulf of Tonkin — when the SIGINT did not match the sales pitch.</p>
<p class="sk-strip">
<a href="../weekly-dig.html">Weekly Dig</a> ·
<a href="../document-vault.html">Document Vault</a> ·
<a href="../skeptic-tools.html">Skeptic Tools</a> ·
<a href="../start-here.html">Rabbit Hole Map</a>
</p>
</div></section>
<section class="paper"><div class="wrap">
<article class="sk-issue">
<p class="sk-meta">Sample issue · Oct 30, 2026 · ~6 min dig</p>
<h2>The brief</h2>
<p>August 1964: a real clash on the 2nd, a disputed "second attack" on the 4th, and a Congressional resolution that opened the door to a wider war. Years later, NSA historical work said the Aug 4 SIGINT did not support the public claim. This is a classic "sounds fake → actually on the record" trail — and a reminder to separate <em>what was sold</em> from <em>what the files show</em>.</p>
<h3>Dig in yourself</h3>
<ul>
<li><strong>Independent:</strong> <a href="https://nsarchive2.gwu.edu/NSAEBB/NSAEBB132/press20051201.htm" target="_blank" rel="noopener">National Security Archive — Tonkin press note / briefing book</a></li>
<li><strong>Independent:</strong> <a href="https://nsarchive2.gwu.edu/NSAEBB/NSAEBB132/" target="_blank" rel="noopener">NSAEBB 132 — Gulf of Tonkin collection</a></li>
<li><strong>Mainstream:</strong> <a href="https://en.wikipedia.org/wiki/Gulf_of_Tonkin_incident" target="_blank" rel="noopener">Wikipedia overview (follow its citations)</a></li>
<li><strong>Primary document:</strong> <a href="https://www.archives.gov/research/pentagon-papers" target="_blank" rel="noopener">Pentagon Papers at NARA</a> (wider Vietnam decision trail)</li>
</ul>
<h3>What's on the record</h3>
<p>NSA released historical materials in 2005–06. Historian Robert J. Hanyok's study argued the Aug 4 attack reporting was skewed. The Gulf of Tonkin Resolution remains a legislative fact; the intelligence picture under it is what shifted.</p>
<h3>Still open / talk about it</h3>
<ol>
<li>If SIGINT was clear by 2001 in draft form, why did the public wait years for the release?</li>
<li>How should citizens treat "urgent" war claims the next time timelines move faster than FOIA?</li>
<li>What other modern flashpoints deserve the same claim-vs-release timeline treatment?</li>
</ol>
<p><em>Optional prop:</em> print a "CLASSIFIED" stamp for dig night — or grab something from the <a href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored">party kit</a> if you like the aesthetic. The files matter more than the merch.</p>
<p><a href="../weekly-dig.html"><strong>← Back to Weekly Dig signup</strong></a> · <a href="../timeline.html">Open Timeline Mode</a> · <a href="../scoreboard.html">See it on the Scoreboard</a></p>
</article>
</div></section>
'''

# Write issue with path_prefix
slug = 'weekly-dig/issue-01.html'
title = 'Weekly Dig #01 — Gulf of Tonkin'
desc = 'Sample Weekly Dig: Gulf of Tonkin claim vs later SIGINT releases. Primary and independent links to dig yourself.'
path_prefix = '../'
cur_hub = ''
nav = NAV.format(cur_hub=cur_hub)
# simplify nav hrefs with prefix manually in page() — call page with path_prefix
share_url = 'https://conspiraparty.com/weekly-dig/issue-01.html'
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Conspiraparty</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{share_url}">
<meta property="og:site_name" content="Conspiraparty">
<meta property="og:title" content="{title} | Conspiraparty">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{share_url}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://conspiraparty.com/assets/og/index.jpg">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="../assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="../assets/style.css?v=sk1">
<link rel="stylesheet" href="../assets/share.css">
<link rel="stylesheet" href="../assets/skeptic-tools.css?v=sk1">
</head>
<body><a class="skip" href="#main">Skip to content</a>
<div class="promo">20% off the full printable kit with code <a href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored">LEAKED20</a></div>
<header class="top"><div class="bar"><a class="logo" href="../index.html"><img src="../assets/img/logo.png" alt="Conspiraparty.com – Top Secret Party Kit" width="220" height="70"></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button></div>
<nav class="main" id="nav" aria-label="Main"><ul>
<li><a href="../start-here.html">Start Here</a></li>
<li><a href="../skeptic-tools.html">Skeptic Tools</a></li>
<li><a href="../weird-news.html">Weird News</a></li>
<li><a href="../weekly-dig.html">Weekly Dig</a></li>
</ul></nav></header>
<main id="main">
{issue_body}
</main>
<footer><div class="wrap"><nav aria-label="Footer"><ul>
<li><a href="../index.html">Home</a></li>
<li><a href="../skeptic-tools.html">Skeptic Tools</a></li>
<li><a href="../weekly-dig.html">Weekly Dig</a></li>
<li><a href="../document-vault.html">Document Vault</a></li>
</ul></nav>
<p>Question everything, especially us. © 2026 Conspiraparty.com</p></div></footer>
<script src="../assets/site.js" defer></script>
<script src="../assets/share.js" defer></script>
</body></html>
"""
(ROOT / 'weekly-dig').mkdir(exist_ok=True)
(ROOT / slug).write_text(html)
print('wrote', slug)
print('done')
