#!/usr/bin/env python3
"""Shared HTML fragments for Conspiraparty blog posts.

Daily Rabbit Holes blog routine should import these (or copy the strings)
so new posts keep the X follow link in signup + footer.
"""
from __future__ import annotations

X_URL = "https://x.com/conspiraparty"
FOLLOW_LINK = f'<a href="{X_URL}" target="_blank" rel="noopener">Follow @conspiraparty on X</a>'
FOLLOW_FOOTER = f'<p class="x-follow">{FOLLOW_LINK}</p>'
FOLLOW_BTN = (
    f'<p class="x-follow-inline">'
    f'<a class="btn sm x-follow-btn" href="{X_URL}" target="_blank" rel="noopener">'
    f"Follow @conspiraparty on X</a></p>"
)

# Nested under /blog/ — paths use ../
BLOG_SIGNUP = f'''<section class="redbg" id="signup"><div class="wrap signup"><span class="stamp" style="color:#fff;border-color:#fff">Classified</span><h2>Join the Shadow Party Committee</h2><p>Get a free <strong>Top Secret Agent ID Badge</strong> printable. Name optional. No spam, ever.</p>
<form class="signup-form" data-signup data-connected="true" action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="a2adf9e4-98f3-48cf-ab94-208e1705280b">
<input type="hidden" name="subject" value="New Shadow Party Committee recruit">
<input type="hidden" name="from_name" value="Conspiraparty">
<input type="hidden" name="redirect" value="https://conspiraparty.com/thanks.html">
<input type="checkbox" name="botcheck" class="skip" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
<input type="hidden" name="source_page" value="">
<label class="skip" for="nm-blog">Name (optional)</label>
<input id="nm-blog" type="text" name="name" placeholder="Cover name (optional)">
<label class="skip" for="em-blog">Email</label>
<input id="em-blog" type="email" name="email" placeholder="your.cover@email.com" required>
<button class="btn alt" type="submit">Send My Free Badge</button>
<span class="notice" role="status" aria-live="polite"></span>
</form>
{FOLLOW_BTN}
</div></section>'''

BLOG_FOOTER = f'''<footer><div class="wrap"><nav aria-label="Footer"><ul>
<li><a href="../index.html">Home</a></li><li><a href="index.html">Blog</a></li><li><a href="../weird-news.html">Weird News</a></li><li><a href="../gift-guide.html">Holiday Gift Guide</a></li>
<li><a href="../free-printables.html">Free Printables</a></li><li><a href="../party-essentials.html">Party Games</a></li>
</ul></nav>
<p class="disclosure">As an Amazon Associate, Conspiraparty earns from qualifying purchases.</p>
{FOLLOW_FOOTER}
<p>All conspiracies on this site are for entertainment. Question everything, especially us. © 2026 Conspiraparty.com</p></div></footer>'''
