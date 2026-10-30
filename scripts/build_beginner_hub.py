#!/usr/bin/env python3
"""Build beginner-hub pages (preview branch only)."""
from pathlib import Path
import html, urllib.parse

ROOT = Path(__file__).resolve().parents[1]

def esc(s):
    return html.escape(s, quote=True)

def share_box(url, text, image='https://conspiraparty.com/assets/og/index.jpg', cls='page-share'):
    u = esc(url); t = esc(text); i = esc(image)
    qx = urllib.parse.quote(text); qu = urllib.parse.quote(url); qi = urllib.parse.quote(image)
    return (
        f'<div class="share-box {cls}" data-share-url="{u}" data-share-text="{t}" data-share-image="{i}">'
        f'<button class="btn sm share-native" data-share type="button">Share this</button>'
        f'<div class="share-links" hidden>'
        f'<a class="btn sm" href="https://x.com/intent/post?text={qx}&amp;url={qu}" rel="noopener noreferrer" target="_blank">X</a>'
        f'<a class="btn sm" href="https://www.facebook.com/sharer/sharer.php?u={qu}" rel="noopener noreferrer" target="_blank">Facebook</a>'
        f'<a class="btn sm" href="https://www.pinterest.com/pin/create/button/?url={qu}&amp;description={qx}&amp;media={qi}" rel="noopener noreferrer" target="_blank">Pinterest</a>'
        f'<button class="btn sm share-copy" data-copy type="button">Copy link</button>'
        f'</div></div>'
    )

NAV_ITEMS = [
    ('start-here.html', 'Start Here'),
    ('index.html#kit', 'Party Kit'),
    ('free-printables.html', 'Free'),
    ('blog/index.html', 'Blog'),
    ('memes.html', 'Memes'),
    ('weird-news.html', 'Weird News'),
    ('field-guides.html', 'Field Guides'),
    ('shirts.html', 'Shirts'),
    ('quiz.html', 'Quiz'),
    ('gift-guide.html', 'Gifts'),
]

def nav(current=None):
    lis = []
    for href, label in NAV_ITEMS:
        cur = ' aria-current="page"' if current and href == current else ''
        lis.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return '<nav class="main" id="nav" aria-label="Main"><ul>' + ''.join(lis) + '</ul></nav>'

FOOTER_LINKS = [
    ('index.html','Home'),('start-here.html','Start Here'),('glossary.html','Glossary'),
    ('true-stories.html','True Stories'),('quiz-theorist.html','Theorist Quiz'),
    ('theory-of-the-week.html','Theory of the Week'),('starter-list.html','Starter List'),
    ('weird-map.html','Weird Map'),('join-the-agency.html','Join the Agency'),
    ('party-essentials.html','Party Games'),('books.html','Books'),('apparel.html','Apparel'),
    ('gifts.html','Gifts'),('field-guides.html','Field Guides'),('free-printables.html','Free Printables'),
    ('shirts.html','Shirts'),('quiz.html','Which Conspiracy Are You? Quiz'),('memes.html','Memes'),
    ('weird-news.html','Weird News'),('blog/index.html','Blog'),('gift-guide.html','Holiday Gift Guide'),
]

def footer():
    links = ''.join(f'<li><a href="{h}">{l}</a></li>' for h,l in FOOTER_LINKS)
    return f'''<footer><div class="wrap"><nav aria-label="Footer"><ul>{links}</ul></nav>
<p class="disclosure">As an Amazon Associate, Conspiraparty earns from qualifying purchases. Some links on this site are affiliate links, which means we may earn a small commission at no extra cost to you.</p>
<p class="x-follow"><a href="https://x.com/conspiraparty" target="_blank" rel="noopener">Follow @conspiraparty on X</a></p>
<p>All conspiracies on this site are for entertainment. Question everything, especially us. © 2026 Conspiraparty.com</p></div></footer>
<a class="sticky-cta" href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored">Get the Party Kit – 20% off</a>
<script src="assets/site.js" defer></script>
<script src="assets/share.js" defer></script>'''

def signup(form_id='bh'):
    return f'''<section class="redbg" id="signup"><div class="wrap signup"><span class="stamp" style="color:#fff;border-color:#fff">Classified</span>
<h2>Join the Shadow Party Committee</h2>
<p>Get a free <strong>Top Secret Agent ID Badge</strong> printable, plus new free printables and party ideas. No spam, ever.</p>
<form class="signup-form" data-signup data-connected="true" action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="a2adf9e4-98f3-48cf-ab94-208e1705280b">
<input type="hidden" name="subject" value="New Shadow Party Committee recruit">
<input type="hidden" name="from_name" value="Conspiraparty">
<input type="hidden" name="redirect" value="https://conspiraparty.com/thanks.html">
<input type="checkbox" name="botcheck" class="skip" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
<input type="hidden" name="source_page" value="">
<input type="hidden" name="bonus" value="Top Secret Agent ID Badge">
<label class="skip" for="nm-{form_id}">Name (optional)</label>
<input id="nm-{form_id}" type="text" name="name" placeholder="Cover name (optional)" autocomplete="name">
<label class="skip" for="em-{form_id}">Email</label>
<input id="em-{form_id}" type="email" name="email" placeholder="your.cover@email.com" required autocomplete="email">
<button class="btn alt" type="submit">Send My Free Badge</button>
<span class="notice" role="status" aria-live="polite"></span>
</form>
<p class="x-follow-inline"><a class="btn sm x-follow-btn" href="https://x.com/conspiraparty" target="_blank" rel="noopener">Follow @conspiraparty on X</a></p>
</div></section>'''

HUB = '''<p class="beginner-hub-strip">
<a href="start-here.html">Start Here</a> ·
<a href="quiz-theorist.html">Quiz</a> ·
<a href="glossary.html">Glossary</a> ·
<a href="true-stories.html">True Stories</a> ·
<a href="theory-of-the-week.html">Theory of the Week</a> ·
<a href="starter-list.html">Starter List</a> ·
<a href="weird-map.html">Weird Map</a> ·
<a href="join-the-agency.html">Join the Agency</a>
</p>'''

def page(title, desc, slug, current, body, extra_js=''):
    url = f'https://conspiraparty.com/{slug}'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | Conspiraparty</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="Conspiraparty">
<meta property="og:title" content="{esc(title)} | Conspiraparty">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://conspiraparty.com/assets/og/index.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)} | Conspiraparty">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="https://conspiraparty.com/assets/og/index.jpg">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/Anton-Regular.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/share.css">
<link rel="stylesheet" href="assets/beginner-hub.css">
</head>
<body><a class="skip" href="#main">Skip to content</a>
<div class="promo">20% off the full printable kit with code <a href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored">LEAKED20</a></div>
<header class="top"><div class="bar"><a class="logo" href="index.html"><img src="assets/img/logo.png" alt="Conspiraparty.com – Top Secret Party Kit" width="220" height="70"></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button></div>
{nav(current)}</header>
<main id="main">
{body}
{signup(slug.replace('.html','')[:12])}
</main>
{footer()}
{extra_js}
</body></html>'''

# CSS already written; refresh
(ROOT/'assets/beginner-hub.css').write_text(Path(ROOT/'assets/beginner-hub.css').read_text() if (ROOT/'assets/beginner-hub.css').exists() else '')

# ========== quiz-theorist ==========
quiz_js = r'''
<script>
(function(){
  var R = {
    foil: {t:'The Tin Foil Couture Agent', d:'You dress for the job you want: antenna included. Every party needs a lookout.', u:'https://happyplaceinkandart.etsy.com/listing/4502272966', p:'Conspiraparty Party Kit (LEAKED20)', i:'assets/img/kit-0.webp'},
    alien: {t:'The Friendly Abductee', d:'You waved at the lights. They waved back. Probably. You keep snacks for the mothership.', u:'https://happyplaceinkandart.etsy.com/listing/4601156509', p:'The Truth Is Out There alien kit', i:'assets/img/alien-kit.jpg'},
    leak: {t:'The Cheerful Leaker', d:'Secrets last about 12 seconds around you. Group chats fear your screenshots.', u:'https://happyplaceinkandart.etsy.com/listing/4600479706', p:'Who Leaked the Files? party game', i:'assets/img/wltf-01-kit-cover.webp'},
    bigfoot: {t:'The Trail-Cam Romantic', d:'You believe in blurry things and clean hiking boots. Forests whisper; you take notes.', u:'https://www.etsy.com/listing/4605278398', p:'Junior Cryptid Scout Birthday kit', i:'assets/img/cryptid-scout-kit.webp'},
    slide: {t:'The PowerPoint Prophet', d:'Your theories come with transitions. Red string optional. Laser pointer mandatory.', u:'https://www.etsy.com/listing/4604436132/conspiracy-powerpoint-night-party-kit', p:'Conspiracy PowerPoint Night kit', i:'assets/img/ppt-night-hero.jpg'},
    tour: {t:'The Fake-Band Merch Dealer', d:'You collect tees from bands that never existed. The tour was totally real.', u:'shirts.html', p:'Totally Real Tour shirts', i:'assets/img/tour-merch/chemtrail-cowboys.webp'}
  };
  var f=document.getElementById('quiz'), box=document.getElementById('result');
  var U='https://conspiraparty.com/quiz-theorist.html';
  function show(k){
    var r=R[k]; if(!r) return;
    document.getElementById('rt').textContent='You are: '+r.t;
    document.getElementById('rd').textContent=r.d;
    var a=document.getElementById('ru'); a.href=r.u; a.textContent='Get the '+r.p;
    if(r.u.indexOf('http')!==0) a.removeAttribute('target'); else { a.target='_blank'; a.rel='noopener sponsored'; }
    var im=document.getElementById('ri'); im.src=r.i; im.alt=r.p;
    var txt='I took "Which Conspiracy Theorist Are You?" and I\'m '+r.t+'! What are you?';
    var u=U+'?r='+k;
    document.getElementById('sx').href='https://x.com/intent/post?text='+encodeURIComponent(txt)+'&url='+encodeURIComponent(u);
    document.getElementById('sf').href='https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent(u);
    document.getElementById('sp').href='https://www.pinterest.com/pin/create/button/?url='+encodeURIComponent(U)+'&description='+encodeURIComponent(txt);
    document.getElementById('sc').onclick=function(){navigator.clipboard&&navigator.clipboard.writeText(u); this.textContent='Copied!';};
    f.hidden=true; box.hidden=false; box.scrollIntoView({behavior:'smooth'});
  }
  f.addEventListener('submit', function(e){
    e.preventDefault();
    var c={}; new FormData(f).forEach(function(v){ c[v]=(c[v]||0)+1; });
    var best=null; for(var k in c) if(!best||c[k]>c[best]) best=k;
    show(best);
  });
  document.getElementById('again').onclick=function(){ f.reset(); f.hidden=false; box.hidden=true; window.scrollTo(0,0); };
  var m=location.search.match(/[?&]r=(\w+)/); if(m) show(m[1]);
})();
</script>
'''

Qs = [
  ('Your ideal Friday night is…', [('foil','Building a hat out of kitchen foil, for science'),('alien','Stargazing “just in case”'),('leak','Reading the group chat like it’s a case file'),('bigfoot','A night hike with a flashlight'),('slide','Making a 12-slide deck about nothing'),('tour','Thrifting for mysterious band tees')]),
  ('Pick a snack:', [('foil','Anything wrapped in foil (protection)'),('alien','Glow candy'),('leak','Whatever was left unlabeled in the fridge'),('bigfoot','Trail mix, obviously'),('slide','Coffee strong enough to classify'),('tour','Gas-station tour snacks')]),
  ('Your camera roll is mostly…', [('foil','Hats, antennas, DIY shielding'),('alien','Weird lights in the sky'),('leak','Screenshots of screenshots'),('bigfoot','Blurry trees that might be something'),('slide','Slide screenshots and sticky notes'),('tour','Merch flat-lays')]),
  ('Someone says “trust me.” You…', [('foil','Check their hat first'),('alien','Ask which planet they’re from'),('leak','Tell three friends immediately'),('bigfoot','Ask for footprints'),('slide','Ask for sources in APA format'),('tour','Ask if the tour was real')]),
  ('Your party role is…', [('foil','Running the tin-foil station'),('alien','The one in the little green antenna headband'),('leak','Accidentally spoiling the plot'),('bigfoot','Campfire storyteller'),('slide','Host with the clicker'),('tour','Merch table captain')]),
  ('Pick a motto:', [('foil','“Fashion is armor.”'),('alien','“I want to believe.”'),('leak','“Loose lips throw great parties.”'),('bigfoot','“Not all who wander are lost. Some are hairy.”'),('slide','“Show me the slide.”'),('tour','“The band dropped before the music did.”')]),
  ('Your suspicious place of choice:', [('foil','Any conference room with bad Wi-Fi'),('alien','Area 51 gift shop parking lot'),('leak','The office printer'),('bigfoot','A misty trail at dusk'),('slide','A library after midnight'),('tour','A venue that only exists on a shirt')]),
  ('If you found a manila folder stamped CLASSIFIED, you would…', [('foil','Wrap it in foil first'),('alien','Check for stardust'),('leak','Host a reading party'),('bigfoot','Take it hiking for vibes'),('slide','Turn it into a keynote'),('tour','Print it on a tee')]),
]

fields = []
for i,(q,opts) in enumerate(Qs):
    labs = ''.join(
        f'<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q{i}" value="{v}" required> {esc(lab)}</label>'
        for v,lab in opts
    )
    fields.append(f'<fieldset class="paper quiz-q"><legend><strong>{i+1}. {esc(q)}</strong></legend>{labs}</fieldset>')

quiz_body = f'''
<section class="hero"><div class="wrap center">
<h1>WHICH CONSPIRACY <span class="r">THEORIST</span> ARE YOU?</h1>
<p class="sub">8 questions. 6 classified results. Zero government approval.</p>
{share_box('https://conspiraparty.com/quiz-theorist.html','Which Conspiracy Theorist Are You? Free funny quiz — via conspiraparty.com')}
{HUB}
</div></section>
<section class="cork"><div class="wrap center">
<form id="quiz" style="max-width:640px;margin:0 auto">{''.join(fields)}
<button class="btn big" type="submit">Reveal My File</button></form>
<div id="result" class="paper result-box" hidden>
<span class="stamp">Classified</span>
<h2 id="rt"></h2>
<img id="ri" alt="Your conspiracy theorist quiz result" width="300" height="300" style="max-width:300px;height:auto">
<p id="rd" class="lead"></p>
<p><a id="ru" class="btn big">Get It</a></p>
<p><strong>Share your result:</strong><br>
<a id="sx" class="btn sm" target="_blank" rel="noopener">Share on X</a>
<a id="sf" class="btn sm" target="_blank" rel="noopener">Share on Facebook</a>
<a id="sp" class="btn sm" target="_blank" rel="noopener">Pin It</a>
<button id="sc" class="btn sm" type="button">Copy Link</button></p>
<p><button id="again" class="btn sm" type="button">Take it again</button></p>
</div>
<p style="margin-top:24px">Also try <a href="quiz.html">Which Conspiracy Are You?</a> or the <a href="quiz-cryptid.html">cryptid quiz</a>.</p>
</div></section>
'''
(ROOT/'quiz-theorist.html').write_text(page(
  'Which Conspiracy Theorist Are You? Free Funny Quiz',
  'Take the free Which Conspiracy Theorist Are You quiz. 8 questions, 6 funny results, plus kits and tees to match your file.',
  'quiz-theorist.html','quiz-theorist.html', quiz_body, quiz_js))

# ========== glossary ==========
TERMS = [
  ('MIB','Men In Black. Usually not fashion advice.'),
  ('Black helicopter','The chopper that shows up exactly when you notice something. Coincidence? Sure.'),
  ('False flag','When someone stages a mess and leaves someone else’s calling card.'),
  ('Psyop','Psychological operation. Fancy word for “trying to get in your head.”'),
  ('Cryptid','Creature that science has not RSVP’d for yet. Bigfoot’s LinkedIn category.'),
  ('UFO / UAP','Unidentified flying (or anomalous) thing. Could be a balloon. Could be… a balloon with secrets.'),
  ('Cover-up','The paperwork that arrives after the interesting part.'),
  ('Disinfo','Information designed to confuse. Bring snacks.'),
  ('Limited hangout','Admit a little so nobody asks for the rest.'),
  ('Rabbit hole','What you fell into when you only meant to check one article.'),
  ('Red string','Wall décor for people who outline theories like crime shows.'),
  ('Tin foil hat','Classic fashion. Blocks nothing proven. Looks fantastic in photos.'),
  ('Deep state','A vague basement under every org chart. Great for parties; light on citations.'),
  ('Whistleblower','Person who brought snacks and receipts.'),
  ('Classified','Stamp that means “ask again later,” usually forever.'),
  ('Need to know','The club you’re not in. Yet.'),
  ('Gaslighting','Convincing you the weird thing you saw was fine, actually.'),
  ('Honey pot','A trap that looks like a gift. Also a party snack if labeled correctly.'),
  ('Astroturfing','Fake grassroots. Real lawn care energy.'),
  ('Shadow government','The committee that never puts their names on the invite.'),
  ('Plausible deniability','“I was never here,” printed on official letterhead.'),
  ('Controlled opposition','Critics who somehow always stay on script.'),
  ('Follow the money','Detective advice that also works at bake sales.'),
  ('Sheeple','Rude nickname for people who skip the homework. Don’t be that guest.'),
  ('The narrative','The story you’re told before the footnotes.'),
  ('Off-books','Not in the binder they show the inspector.'),
  ('Compartmentalization','Everyone knows a piece. Nobody gets the puzzle box.'),
  ('Useful idiot','Someone helping a plot without reading the plot. Don’t be one.'),
  ('Gone dark','Stopped posting. Possibly on vacation. Possibly in a bunker.'),
  ('Trust no one','Party rule #1. Except the snack table. Trust the snack table.'),
]
gloss_items = ''.join(
  f'<div class="gloss-term" id="{esc(t.lower().split()[0].replace("/","").replace(".",""))}"><dl><dt>{esc(t)}</dt><dd>{esc(d)}</dd></dl></div>'
  for t,d in TERMS
)
gloss_body = f'''
<section class="hero"><div class="wrap center">
<h1>CONSPIRACY <span class="r">LINGO</span></h1>
<p class="sub">~30 terms. One funny line each. Use responsibly at parties.</p>
{share_box('https://conspiraparty.com/glossary.html','Conspiracy lingo glossary — funny one-liners — via conspiraparty.com')}
{HUB}
</div></section>
<section class="cork"><div class="wrap">
<p class="lead center">Entertainment glossary. Not a field manual. For deeper documented history, see <a href="true-stories.html">Sounds Fake, Actually Happened</a>.</p>
<div class="glossary-grid">{gloss_items}</div>
</div></section>
'''
(ROOT/'glossary.html').write_text(page(
  'Conspiracy Lingo Glossary',
  'Funny glossary of conspiracy slang: MIB, false flag, psyop, cryptid, limited hangout and more. One punchline each.',
  'glossary.html','glossary.html', gloss_body))

print('quiz + glossary done')

# ========== true-stories ==========
STORIES = [
  dict(id='mkultra', title='Project MKUltra', when='CIA · ~1953–1964 (investigated 1975–77)',
       blurb='A CIA “umbrella” program funding behavioral-modification research, including drugs. Many files were destroyed in 1973; surviving records and Church Committee / Senate hearings documented the program. Unwitting testing on U.S. persons was later discontinued after an Inspector General review.',
       sources=[('Senate Intelligence (MKUltra hearing PDF)','https://www.intelligence.senate.gov/wp-content/uploads/2024/08/sites-default-files-hearings-95mkultra.pdf'),
                ('Wikipedia overview','https://en.wikipedia.org/wiki/MKUltra')]),
  dict(id='northwoods', title='Operation Northwoods', when='Joint Chiefs of Staff · 1962 (declassified later)',
       blurb='A JCS memorandum titled “Justification for US Military Intervention in Cuba” proposed staged pretexts (including fake attacks) to justify invading Cuba. It was not carried out. The document is in the National Archives JFK Collection (record 202-10002-10104) and published by the National Security Archive.',
       sources=[('National Archives catalog','https://catalog.archives.gov/id/305036'),
                ('National Security Archive page','https://nsarchive.gwu.edu/CMC-60/joint-chiefs-pretexts-to-invade-Cuba-1962'),
                ('NARA PDF','https://www.archives.gov/files/research/jfk/releases/2018/202-10002-10104.pdf')]),
  dict(id='tonkin', title='Gulf of Tonkin (Aug 1964)', when='Vietnam War · NSA historian review declassified 2005',
       blurb='After a real clash on Aug 2, the Johnson administration cited a second Aug 4 attack to push the Gulf of Tonkin Resolution. NSA historian Robert J. Hanyok’s later study concluded the SIGINT showed no second attack and that reporting was skewed. NSA released related materials in 2005–2006.',
       sources=[('NSA Gulf of Tonkin releases','https://www.nsa.gov/Helpful-Links/NSA-FOIA/Declassification-Transparency-Initiatives/Historical-Releases/Gulf-of-Tonkin/'),
                ('Hanyok Cryptologic Quarterly PDF','https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/cryptologic-quarterly/Skunks.pdf'),
                ('National Security Archive press note','https://nsarchive2.gwu.edu/NSAEBB/NSAEBB132/press20051201.htm')]),
  dict(id='tuskegee', title='USPHS Untreated Syphilis Study at Tuskegee', when='1932–1972 · CDC / National Archives',
       blurb='A U.S. Public Health Service study followed hundreds of Black men with syphilis without informed consent and without offering treatment even after penicillin became standard. The study ended in 1972 after press exposure; President Clinton apologized in 1997.',
       sources=[('CDC official page','https://www.cdc.gov/tuskegee/about/index.html'),
                ('Wikipedia overview','https://en.wikipedia.org/wiki/Tuskegee_Syphilis_Study')]),
  dict(id='cointelpro', title='COINTELPRO', when='FBI · 1956–1971 · Church Committee',
       blurb='FBI “counterintelligence programs” used covert tactics to disrupt domestic groups and individuals. The Church Committee documented the programs from Bureau files. Targets included civil-rights and anti-war organizations among others.',
       sources=[('U.S. Senate: Church Committee overview','https://www.senate.gov/about/powers-procedures/investigations/church-committee.htm'),
                ('FBI Vault: COINTELPRO','https://vault.fbi.gov/cointel-pro'),
                ('Wikipedia overview','https://en.wikipedia.org/wiki/COINTELPRO')]),
  dict(id='mockingbird', title='CIA & the press (Project MOCKINGBIRD)', when='Documented wiretap · Mar–Jun 1963 · “Family Jewels”',
       blurb='Popular histories often use “Operation Mockingbird” for alleged broad CIA media control. What is clearly documented in CIA “Family Jewels” material is Project MOCKINGBIRD: a telephone intercept on two Washington newsmen (Mar 12–Jun 15, 1963), authorized at high levels. Broader CIA–journalist relationships were also examined by the Church Committee—keep the popular nickname separate from the specific cryptonym.',
       sources=[('Wikipedia: Operation Mockingbird (context & debates)','https://en.wikipedia.org/wiki/Operation_Mockingbird'),
                ('Church Committee (Senate overview)','https://www.senate.gov/about/powers-procedures/investigations/church-committee.htm')]),
  dict(id='sunshine', title='Project Sunshine', when='AEC / RAND · 1950s fallout research',
       blurb='A U.S. Atomic Energy Commission research effort (with RAND) studied worldwide effects of nuclear weapons, including strontium-90 uptake. The 1953 RAND/AEC report “Worldwide Effects of Atomic Weapons: Project SUNSHINE” is public. Later reporting and scholarship discussed controversial tissue-collection practices used in fallout studies—treat those details carefully and stick to primary docs.',
       sources=[('RAND report PDF (R-251)','https://www.rand.org/content/dam/rand/pubs/reports/2008/R251.pdf'),
                ('Wikipedia overview','https://en.wikipedia.org/wiki/Project_Sunshine')]),
  dict(id='paperclip', title='Operation Paperclip', when='U.S. postwar · National Archives',
       blurb='A U.S. program that brought German scientists and engineers (including some with Nazi affiliations) to America after WWII for military and aerospace work. Extensively documented in National Archives records and later histories.',
       sources=[('National Archives topical overview','https://www.archives.gov/research/foreign-policy/ww2'),
                ('Wikipedia overview','https://en.wikipedia.org/wiki/Operation_Paperclip')]),
]

story_html = []
for s in STORIES:
    src = ' · '.join(f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(lab)}</a>' for lab,u in s['sources'])
    story_html.append(f'''<article class="story-card" id="{s['id']}">
<h3>{esc(s['title'])}</h3>
<p class="when">{esc(s['when'])}</p>
<p>{esc(s['blurb'])}</p>
<p class="sources"><strong>Sources:</strong> {src}</p>
</article>''')

true_body = f'''
<section class="hero"><div class="wrap center">
<h1>SOUNDS FAKE, <span class="r">ACTUALLY HAPPENED</span></h1>
<p class="sub">Documented programs and scandals. Sourced to archives, agencies, and serious overviews. Not party lore.</p>
{share_box('https://conspiraparty.com/true-stories.html','Sounds Fake, Actually Happened — documented cases — via conspiraparty.com')}
{HUB}
</div></section>
<section class="paper"><div class="wrap">
<p class="lead">These are real historical cases. Summaries are short on purpose. Click through to primary or official pages. No invented claims. No QAnon. No living-politician drama here.</p>
{''.join(story_html)}
<p class="lead" style="margin-top:24px">Want the funny version of curiosity? Back to the <a href="start-here.html">rabbit hole map</a> or the <a href="starter-list.html">starter watch/read list</a>.</p>
</div></section>
'''
(ROOT/'true-stories.html').write_text(page(
  'Sounds Fake, Actually Happened',
  'Real documented cases that sound like conspiracy lore: MKUltra, Northwoods, Gulf of Tonkin, Tuskegee, COINTELPRO, Project Sunshine and more, with source links.',
  'true-stories.html','true-stories.html', true_body))

# ========== theory of the week ==========
vote_js = r'''
<script>
(function(){
  var KEY='cp_totw_2026w44_birds';
  var theoryId='birds-arent-real-party';
  function load(){
    try{ return JSON.parse(localStorage.getItem(KEY)||'{"believe":0,"debunk":0,"mine":null}'); }
    catch(e){ return {believe:0,debunk:0,mine:null}; }
  }
  function save(s){ localStorage.setItem(KEY, JSON.stringify(s)); }
  function render(){
    var s=load();
    var b=s.believe|0, d=s.debunk|0, t=b+d;
    var bp=t? Math.round(b*100/t):0, dp=t?100-bp:0;
    document.getElementById('believe-count').textContent=b+' (your device)';
    document.getElementById('debunk-count').textContent=d+' (your device)';
    document.getElementById('believe-fill').style.width=bp+'%';
    document.getElementById('debunk-fill').style.width=dp+'%';
    document.getElementById('vote-status').textContent = s.mine
      ? ('Your vote on this device: '+ (s.mine==='believe'?'Believe It':'Debunk It') +'. Totals are only what this browser has recorded — not a global poll.')
      : 'No vote yet on this device. Totals below are localStorage only — not sitewide numbers.';
    document.getElementById('btn-believe').disabled=!!s.mine;
    document.getElementById('btn-debunk').disabled=!!s.mine;
  }
  function cast(side){
    var s=load();
    if(s.mine) return;
    s[side]=(s[side]|0)+1; s.mine=side; save(s); render();
  }
  document.getElementById('btn-believe').onclick=function(){cast('believe');};
  document.getElementById('btn-debunk').onclick=function(){cast('debunk');};
  document.getElementById('btn-reset').onclick=function(){
    if(confirm('Clear only THIS browser\\'s vote tally for this theory?')){ localStorage.removeItem(KEY); render(); }
  };
  render();
})();
</script>
'''

totw_body = f'''
<section class="hero"><div class="wrap center">
<p class="eyebrow" style="margin:0 0 14px;font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;color:var(--text-dim)">Week of Oct 27, 2026 · Family-friendly</p>
<h1>BELIEVE IT OR <span class="r">DEBUNK IT</span></h1>
<p class="sub">Theory of the week. Cast one vote per browser. We do not invent tallies.</p>
{share_box('https://conspiraparty.com/theory-of-the-week.html','Believe It or Debunk It — Theory of the Week — via conspiraparty.com')}
{HUB}
</div></section>
<section class="cork"><div class="wrap">
<div class="vote-panel paper" style="padding:22px">
<span class="stamp">This week</span>
<h2 style="margin-top:12px">“Birds aren’t real” (the satire)</h2>
<p>A tongue-in-cheek internet bit that claims birds were replaced by government drones. It’s comedy first — which is why it’s a perfect party vote: believe the bit, or debunk it with a straight face?</p>
<p><em>Related fun on this site:</em> <a href="shirts.html#the-robot-pigeons">Robot Pigeons tour tee</a> · <a href="memes.html">memes</a> · <a href="glossary.html">lingo</a></p>
<div style="display:flex;flex-wrap:wrap;gap:10px;margin:18px 0">
<button class="btn big" id="btn-believe" type="button">Believe It</button>
<button class="btn alt" id="btn-debunk" type="button">Debunk It</button>
<button class="btn sm" id="btn-reset" type="button">Reset my device tally</button>
</div>
<p id="vote-status" class="vote-note"></p>
<div class="vote-bars">
<div class="vote-bar"><div class="label"><span>Believe It</span><span id="believe-count">0</span></div><div class="track"><div class="fill" id="believe-fill"></div></div></div>
<div class="vote-bar"><div class="label"><span>Debunk It</span><span id="debunk-count">0</span></div><div class="track"><div class="fill" id="debunk-fill"></div></div></div>
</div>
<p class="vote-note">Label: <strong>your device only</strong>. Counts live in localStorage. Refreshing keeps them; other phones start at zero. No fake global numbers.</p>
</div>
<p class="center" style="margin-top:28px">Want more rabbit holes? <a href="start-here.html">Start Here</a> · <a href="true-stories.html">True stories</a></p>
</div></section>
'''
(ROOT/'theory-of-the-week.html').write_text(page(
  'Theory of the Week: Believe It or Debunk It',
  'Vote Believe It or Debunk It on this week’s family-friendly theory. Tallies are stored on your device only — no fake numbers.',
  'theory-of-the-week.html','theory-of-the-week.html', totw_body, vote_js))

print('true-stories + totw done')

# ========== starter-list ==========
DOCS = [
  ('Hellier (Planet Weird)', 'Documentary series about high strangeness in Kentucky. Available on Amazon Prime Video / Planet Weird.', 'https://www.amazon.com/s?k=Hellier+documentary'),
  ('Area 51 (based on Annie Jacobsen reporting)', 'Book-driven interest; look for interviews/docs that cite declassified records rather than pure rumor.', 'https://www.amazon.com/s?k=Area+51+Annie+Jacobsen'),
  ('The Phenomenon (2020, James Fox)', 'UFO documentary featuring interviews with officials and witnesses. Existence verified via major retailers.', 'https://www.amazon.com/s?k=The+Phenomenon+James+Fox'),
]
PODS = [
  ('Stuff They Don’t Want You To Know', 'Long-running HowStuffWorks show covering mysteries, conspiracies, and weird history with a research bent.', 'https://www.amazon.com/s?k=Stuff+They+Dont+Want+You+To+Know+podcast'),
  ('Ridiculous History', 'Sibling HowStuffWorks show — weird-but-true history energy, great palate cleanser.', 'https://www.amazon.com/s?k=Ridiculous+History+podcast'),
  ('The Conspiracy Theory Podcast (BBC / various editions — search current feed)', 'Search your podcast app; titles rotate. Prefer shows that cite sources.', 'https://www.amazon.com/s?k=conspiracy+theory+podcast'),
]
BOOKS = [
  ('Area 51 — Annie Jacobsen', 'Investigative history of the Nevada test-and-development site. Already featured in Conspiraparty picks.', 'https://amzn.to/43E2MRD'),
  ('Chaos — Tom O’Neill', 'True-crime / intelligence history rabbit hole around the Manson case and COINTELPRO-era agencies.', 'https://amzn.to/4dysGw9'),
  ('The Devil’s Chessboard — David Talbot', 'History focused on Allen Dulles and Cold War intelligence. On the site’s book picks.', 'https://amzn.to/4dQq7V8'),
  ('UFOs and Government (scientific/historical anthologies)', 'Search for sober timelines from university presses or MUFON histories; skip anonymous PDFs.', 'https://www.amazon.com/s?k=UFOs+and+Government+history'),
]

def list_cards(items):
    out=[]
    for title, why, url in items:
        out.append(f'''<article class="card"><h3>{esc(title)}</h3><p class="why">{esc(why)}</p>
<a class="btn sm" href="{esc(url)}" target="_blank" rel="noopener sponsored">Find on Amazon</a></article>''')
    return ''.join(out)

starter_body = f'''
<section class="hero"><div class="wrap center">
<h1>STARTER <span class="r">WATCH &amp; READ</span></h1>
<p class="sub">Documentaries, podcasts, and books that exist. Curiosity fuel — not a doctrine.</p>
{share_box('https://conspiraparty.com/starter-list.html','Starter watch &amp; read list for curious beginners — via conspiraparty.com')}
{HUB}
</div></section>
<section class="cork"><div class="wrap">
<p class="lead">Links are Amazon searches or existing Conspiraparty affiliate picks. Dedicated affiliate tags can be tightened later. Prefer sources that cite archives over anonymous charts.</p>
<h2>Documentaries</h2>
<div class="grid">{list_cards(DOCS)}</div>
<h2 style="margin-top:28px">Podcasts</h2>
<div class="grid">{list_cards(PODS)}</div>
<h2 style="margin-top:28px">Books</h2>
<div class="grid">{list_cards(BOOKS)}</div>
<p class="disclosure" style="margin-top:24px">As an Amazon Associate, Conspiraparty earns from qualifying purchases. Some links may become tagged affiliate links later.</p>
<p class="center" style="margin-top:18px">Also see our <a href="books.html">books page</a> and <a href="friends-of-the-committee.html">Friends of the Committee</a> shows.</p>
</div></section>
'''
(ROOT/'starter-list.html').write_text(page(
  'Starter Watch & Read List',
  'Beginner documentaries, podcasts, and books on conspiracy culture and weird history. Verified titles with Amazon search links.',
  'starter-list.html','starter-list.html', starter_body))

# ========== weird-map ==========
PINS = [
  # cx,cy roughly on simplified US viewBox 0 0 1000 600
  dict(id='a51', name='Area 51 / Rachel, NV', x=220, y=260, href='field-guides/area-51.html', note='Stay outside the gates.'),
  dict(id='roswell', name='Roswell, NM', x=320, y=340, href='field-guides/roswell.html', note='1947 debris energy.'),
  dict(id='denver', name='Denver Airport', x=340, y=250, href='field-guides/denver-airport.html', note='Blue mustang watches.'),
  dict(id='vegas', name='Las Vegas', x=230, y=300, href='field-guides/las-vegas.html', note='Lights, cameras, cover stories.'),
  dict(id='gc', name='Grand Canyon', x=260, y=310, href='field-guides/grand-canyon.html', note='A suspiciously large hole.'),
  dict(id='rushmore', name='Mount Rushmore', x=400, y=180, href='field-guides/mount-rushmore.html', note='What’s behind the heads?'),
  dict(id='pp', name='Point Pleasant, WV', x=720, y=260, href='field-guides/point-pleasant.html', note='Mothman country.'),
  dict(id='florida', name='Central Florida', x=780, y=420, href='field-guides/most-suspicious-place.html', note='Most Suspicious Place.'),
  dict(id='bermuda', name='Bermuda Triangle (offshore)', x=880, y=380, href='field-guides/bermuda-triangle.html', note='Boats, planes, vibes.'),
]

circles = ''.join(
  f'<a href="{p["href"]}"><circle class="map-pin" cx="{p["x"]}" cy="{p["y"]}" r="14" tabindex="0"><title>{esc(p["name"])}</title></circle></a>'
  for p in PINS
)
pin_list = ''.join(
  f'<article class="card"><h3>{esc(p["name"])}</h3><p class="why">{esc(p["note"])}</p><a class="btn sm" href="{p["href"]}">Open field guide</a></article>'
  for p in PINS
)

PACKS = [
  ('West Field Guide Pack', 'https://www.etsy.com/listing/4605965482', '$4.99'),
  ('Southwest Field Guide Pack', 'https://www.etsy.com/listing/4605947387', '$4.99'),
  ('Midwest Field Guide Pack', 'https://www.etsy.com/listing/4605967044', '$4.99'),
  ('South Field Guide Pack', 'https://www.etsy.com/listing/4605948633', '$4.99'),
  ('Northeast Field Guide Pack', 'https://www.etsy.com/listing/4605968178', '$4.99'),
  ('Northern Frontier Pack', 'https://www.etsy.com/listing/4605951249', '$4.99'),
  ('50 States Field Guides', 'https://www.etsy.com/listing/4605950457', '$12.99'),
]
pack_cards = ''.join(
  f'<article class="card"><h3>{esc(n)}</h3><p class="price">{esc(price)}</p><a class="btn sm" href="{esc(u)}" target="_blank" rel="noopener sponsored">Get on Etsy</a></article>'
  for n,u,price in PACKS
)

map_body = f'''
<section class="hero"><div class="wrap center">
<h1>WEIRD <span class="r">MAP</span></h1>
<p class="sub">Tap a pin for a Suspicious Field Guide. Packs cover whole regions.</p>
{share_box('https://conspiraparty.com/weird-map.html','Weird US map of suspicious places — via conspiraparty.com')}
{HUB}
</div></section>
<section class="black"><div class="wrap">
<div class="map-wrap" role="img" aria-label="Simplified US map with suspicious place pins">
<svg viewBox="0 0 1000 600" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect x="40" y="80" width="900" height="440" rx="40" fill="#1a1a1a" stroke="#fff" stroke-width="3"/>
  <text x="500" y="50" fill="#fff" text-anchor="middle" font-family="Anton,Impact,sans-serif" font-size="28" letter-spacing="4">CONSPIRAPARTY FIELD MAP</text>
  <text x="160" y="140" fill="#888" font-size="14">WEST</text>
  <text x="500" y="140" fill="#888" font-size="14">MIDWEST</text>
  <text x="820" y="140" fill="#888" font-size="14">EAST</text>
  {circles}
</svg>
</div>
<p class="center" style="margin-top:12px;opacity:.8;font-size:.9rem">Pins are approximate. For overseas weirdness see the <a href="field-guides/stonehenge.html">Stonehenge guide</a>.</p>
</div></section>
<section class="cork"><div class="wrap">
<h2 class="center">Field <span class="r">guides</span></h2>
<div class="map-list">{pin_list}</div>
<h2 class="center" style="margin-top:36px">Regional <span class="r">printable packs</span></h2>
<p class="lead center">Etsy downloads from Happy Place Ink and Art. Marked AI-assisted where applicable in the shop.</p>
<div class="pack-row">{pack_cards}</div>
<p class="center" style="margin-top:20px"><a class="btn" href="field-guides.html">Browse all free field guides</a></p>
</div></section>
'''
(ROOT/'weird-map.html').write_text(page(
  'Weird Map: Suspicious Places in the US',
  'Interactive-ish US map linking to Conspiraparty Suspicious Field Guides and regional printable field guide packs on Etsy.',
  'weird-map.html','weird-map.html', map_body))

# ========== join-the-agency ==========
join_body = f'''
<section class="hero agency-hero"><div class="wrap center">
<span class="stamp" style="color:#fff;border-color:#fff">Recruiting</span>
<h1>JOIN THE <span class="r">AGENCY</span></h1>
<p class="sub">Shadow Party Committee clearance starts with an email. Free Top Secret Agent ID Badge printable included.</p>
{share_box('https://conspiraparty.com/join-the-agency.html','Join the Agency — free Agent ID Badge — via conspiraparty.com')}
{HUB}
<img class="badge-preview" src="assets/img/logo-stamp.png" alt="Conspiraparty classified stamp preview" width="280" height="280" loading="lazy">
<p class="lead">Print on cardstock. Fill in your cover name. Hang it on a lanyard. Instant agent energy.</p>
<p><a class="btn big" href="#agency-form">Get My Free Badge</a>
<a class="btn alt" href="assets/downloads/top-secret-agent-id-badge.pdf" download>Preview / download PDF</a></p>
<p style="font-size:.85rem;opacity:.8">Prefer the form first? The thank-you page also hands you the badge after signup.</p>
</div></section>
<section class="paper" id="agency-form"><div class="wrap signup" style="max-width:560px;margin:0 auto">
<h2 class="center">Request <span class="r">clearance</span></h2>
<p class="center">Same Web3Forms signup used sitewide. Name optional. No spam, ever.</p>
<form class="signup-form" data-signup data-connected="true" action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="a2adf9e4-98f3-48cf-ab94-208e1705280b">
<input type="hidden" name="subject" value="New Shadow Party Committee recruit">
<input type="hidden" name="from_name" value="Conspiraparty">
<input type="hidden" name="redirect" value="https://conspiraparty.com/thanks.html">
<input type="checkbox" name="botcheck" class="skip" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
<input type="hidden" name="source_page" value="join-the-agency">
<input type="hidden" name="bonus" value="Top Secret Agent ID Badge">
<label class="skip" for="nm-agency">Name (optional)</label>
<input id="nm-agency" type="text" name="name" placeholder="Cover name (optional)" autocomplete="name">
<label class="skip" for="em-agency">Email</label>
<input id="em-agency" type="email" name="email" placeholder="your.cover@email.com" required autocomplete="email">
<button class="btn alt" type="submit">Send My Free Badge</button>
<span class="notice" role="status" aria-live="polite"></span>
</form>
<p class="center" style="margin-top:18px">After you join: <a href="thanks.html">thanks page + badge</a> · <a href="free-printables.html">more freebies</a> · <a href="start-here.html">Start Here hub</a></p>
</div></section>
'''
# join page already has signup in template; skip duplicate by using empty signup override — simplest: custom page write
join_html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Join the Agency: Free Agent ID Badge | Conspiraparty</title>
<meta name="description" content="Join the Shadow Party Committee and get a free Top Secret Agent ID Badge printable. Web3Forms signup. No spam.">
<link rel="canonical" href="https://conspiraparty.com/join-the-agency.html">
<meta property="og:site_name" content="Conspiraparty">
<meta property="og:title" content="Join the Agency: Free Agent ID Badge | Conspiraparty">
<meta property="og:description" content="Join the Shadow Party Committee and get a free Top Secret Agent ID Badge printable.">
<meta property="og:url" content="https://conspiraparty.com/join-the-agency.html">
<meta property="og:type" content="website">
<meta property="og:image" content="https://conspiraparty.com/assets/og/index.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/Anton-Regular.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/share.css">
<link rel="stylesheet" href="assets/beginner-hub.css">
</head>
<body><a class="skip" href="#main">Skip to content</a>
<div class="promo">20% off the full printable kit with code <a href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored">LEAKED20</a></div>
<header class="top"><div class="bar"><a class="logo" href="index.html"><img src="assets/img/logo.png" alt="Conspiraparty.com – Top Secret Party Kit" width="220" height="70"></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button></div>
{nav('join-the-agency.html')}</header>
<main id="main">{join_body}</main>
{footer()}
</body></html>'''
(ROOT/'join-the-agency.html').write_text(join_html)

# ========== refresh start-here with same helpers (already exists) ==========
# ========== update index nav + home card ==========
idx = (ROOT/'index.html').read_text()
# inject Start Here into main nav if missing
if 'start-here.html' not in idx.split('id="nav"',1)[-1][:800]:
    idx = idx.replace(
        '<nav class="main" id="nav" aria-label="Main"><ul><li><a href="index.html#kit">Party Kit</a></li>',
        '<nav class="main" id="nav" aria-label="Main"><ul><li><a href="start-here.html">Start Here</a></li><li><a href="index.html#kit">Party Kit</a></li>',
        1
    )
# footer link
if 'start-here.html' not in idx.split('aria-label="Footer"',1)[-1][:500]:
    idx = idx.replace(
        '<nav aria-label="Footer"><ul><li><a href="index.html" aria-current=page>Home</a></li>',
        '<nav aria-label="Footer"><ul><li><a href="index.html" aria-current=page>Home</a></li><li><a href="start-here.html">Start Here</a></li>',
        1
    )
# home hub teaser after trust section
TEASER = '''
<section class="paper" id="start-here-teaser"><div class="wrap center">
<span class="stamp">New</span>
<h2>Curious? <span class="r">Start Here</span></h2>
<p class="lead">Rabbit hole map, theorist quiz, glossary, true stories, weekly vote, starter list, weird map, and free Agent ID.</p>
<p><a class="btn big" href="start-here.html">Open the beginner hub</a>
<a class="btn alt" href="quiz-theorist.html">Take the theorist quiz</a></p>
</div></section>
'''
if 'id="start-here-teaser"' not in idx:
    idx = idx.replace('</div></section>\n<section class="paper" id="shop">', '</div></section>\n'+TEASER+'\n<section class="paper" id="shop">', 1)
    if 'id="start-here-teaser"' not in idx:
        # fallback: after trust
        idx = idx.replace('<section class="paper" id="shop">', TEASER+'\n<section class="paper" id="shop">', 1)
(ROOT/'index.html').write_text(idx)

# light-touch: add Start Here to a few key page navs
for fname in ['field-guides.html','free-printables.html','quiz.html','shirts.html','memes.html','gift-guide.html']:
    p = ROOT/fname
    if not p.exists():
        continue
    t = p.read_text()
    if 'start-here.html' in t.split('id="nav"',1)[-1][:900]:
        continue
    t2 = t.replace(
        '<nav class="main" id="nav" aria-label="Main"><ul><li><a href="index.html#kit">Party Kit</a></li>',
        '<nav class="main" id="nav" aria-label="Main"><ul><li><a href="start-here.html">Start Here</a></li><li><a href="index.html#kit">Party Kit</a></li>',
        1
    )
    if t2 == t:
        t2 = t.replace(
            '<nav aria-label="Main" class="main" id="nav"><ul><li><a href="index.html#kit">Party Kit</a></li>',
            '<nav aria-label="Main" class="main" id="nav"><ul><li><a href="start-here.html">Start Here</a></li><li><a href="index.html#kit">Party Kit</a></li>',
            1
        )
    if t2 != t:
        p.write_text(t2)
        print('nav updated', fname)

# sitemap hint file note — optional append
sm = ROOT/'sitemap.xml'
if sm.exists() and 'start-here.html' not in sm.read_text():
    text = sm.read_text()
    entries = ''
    for slug in ['start-here.html','quiz-theorist.html','glossary.html','true-stories.html','theory-of-the-week.html','starter-list.html','weird-map.html','join-the-agency.html']:
        entries += f'''  <url>
    <loc>https://conspiraparty.com/{slug}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
'''
    text = text.replace('</urlset>', entries+'</urlset>')
    sm.write_text(text)
    print('sitemap updated')

print('ALL PAGES BUILT')
for f in ['start-here.html','quiz-theorist.html','glossary.html','true-stories.html','theory-of-the-week.html','starter-list.html','weird-map.html','join-the-agency.html','assets/beginner-hub.css']:
    print(f, (ROOT/f).exists(), (ROOT/f).stat().st_size if (ROOT/f).exists() else 0)
