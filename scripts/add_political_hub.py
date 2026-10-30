#!/usr/bin/env python3
"""Add political/QAnon content to beginner-hub pages. Believers-say vs documented. Roast both sides."""
from pathlib import Path
import re

ROOT = Path('/workspace/cp-beginner')

DISCLAIMER = '''<p class="disclosure political-disclaimer" id="political-disclaimer" style="background:#fff3c4;color:#111;padding:12px 14px;border-left:5px solid var(--red);margin:18px 0"><strong>Full disclosure:</strong> Political rabbit holes below are for entertainment, like Weird News. We roast the spin on <em>all</em> sides. Theories are labeled <strong>what believers say</strong>. Documented history is labeled <strong>what&apos;s documented</strong>. We do not invent factual claims about real people. Question everything, especially us.</p>'''

# ---------- start-here ----------
def patch_start_here():
    p = ROOT/'start-here.html'
    t = p.read_text()
    # add disclaimer after HUB / first lead
    if 'political-disclaimer' not in t:
        t = t.replace('{HUB}'.replace('{HUB}',''), '', 1)  # noop safety
        # insert after first beginner-hub-strip close
        t = t.replace(
            '</p>\n</div></section>\n<section class="cork">',
            '</p>\n'+DISCLAIMER+'\n</div></section>\n<section class="cork">',
            1
        )
        if 'political-disclaimer' not in t:
            t = t.replace(
                '<section class="cork"><div class="wrap">',
                '<section class="cork"><div class="wrap">\n'+DISCLAIMER+'\n',
                1
            )

    political_nodes = '''
<article class="rabbit-node political-section" id="political-map">
<p class="depth">Spicy · Politics (roast both sides)</p>
<h3>Political rabbit holes</h3>
<p>Same corkboard energy as Weird News. Believers have corkboards. Archives have footnotes. We keep them labeled.</p>
<div class="rabbit-branches">
<a href="#qanon-branch">QAnon</a>
<a href="#pizzagate-branch">Pizzagate</a>
<a href="#deep-state-branch">Deep State</a>
<a href="#elections-branch">Election claims</a>
<a href="#epstein-branch">Epstein files</a>
<a href="#jfk-branch">JFK</a>
<a href="#chemtrails-branch">Chemtrails</a>
<a href="#money-branch">Soros / Big Pharma lore</a>
</div></article>

<article class="rabbit-node" id="qanon-branch">
<p class="depth">Believers say · Online movement since ~2017</p>
<h3>QAnon</h3>
<p><strong>Believers say:</strong> anonymous &quot;Q&quot; drops hint at a secret war against a cabal. <strong>What&apos;s documented:</strong> an online phenomenon tracked by journalists and the HBO series <em>Q: Into the Storm</em>; posts appeared on imageboards; the movement spilled into real-world politics. We roast the certainty theater on every side of the comment section.</p>
<div class="rabbit-branches">
<a href="glossary.html#q-drop">Glossary: Q drop</a>
<a href="starter-list.html#q-into-the-storm">Q: Into the Storm</a>
<a href="weird-news.html">Weird News (QAnon tag)</a>
<a href="theory-of-the-week.html">Vote this week</a>
</div></article>

<article class="rabbit-node" id="pizzagate-branch">
<p class="depth">Believers say · 2016 viral theory</p>
<h3>Pizzagate</h3>
<p><strong>Believers say:</strong> coded messages in leaked emails pointed to a DC pizza shop. <strong>What&apos;s documented:</strong> the shop was real; the coded-cabal claim was not proven; a man fired a rifle inside the restaurant in Dec 2016 while &quot;investigating,&quot; was arrested, and later apologized — a real crime sparked by an online theory. Left and right media both turned it into a content machine. We file it under &quot;don&apos;t bring a gun to a meme.&quot;</p>
<div class="rabbit-branches">
<a href="glossary.html#pizzagate">Glossary</a>
<a href="true-stories.html#political">Documented political scandals</a>
<a href="weird-map.html#dc">DC on the weird map</a>
</div></article>

<article class="rabbit-node" id="deep-state-branch">
<p class="depth">Believers say · Permanent bureaucracy lore</p>
<h3>Deep State</h3>
<p><strong>Believers say (right-leaning version):</strong> career intel/bureaucracy sabotages populist presidents. <strong>Believers say (left-leaning version):</strong> corporate capture, dark money, and revolving-door lobbyists are the real shadow government. <strong>What&apos;s documented:</strong> large permanent agencies, classified programs, lobbying, and revolving doors all exist (Church Committee, Snowden leaks, FEC filings). The mystical all-knowing cabal is the party trick. Roast both speeches.</p>
<div class="rabbit-branches">
<a href="glossary.html#deep-state">Glossary: Deep State</a>
<a href="true-stories.html#prism">Snowden / PRISM</a>
<a href="true-stories.html#cointelpro">COINTELPRO</a>
</div></article>

<article class="rabbit-node" id="elections-branch">
<p class="depth">Believers say · 2016 and 2020</p>
<h3>&quot;Stolen election&quot; claims (both cycles)</h3>
<p><strong>2016 believers (left-leaning):</strong> Russian interference and Comey&apos;s letter stole the race. <strong>What&apos;s documented:</strong> U.S. intel assessed Russian influence ops; Mueller investigated; Trump still won the Electoral College. <strong>2020 believers (right-leaning):</strong> widespread fraud stole the race. <strong>What&apos;s documented:</strong> officials from both parties certified results; dozens of lawsuits failed; some people were charged over Jan 6. We roast the &quot;my loss = conspiracy, your loss = democracy&quot; hypocrisy on both teams.</p>
<div class="rabbit-branches">
<a href="glossary.html#stolen-election">Glossary</a>
<a href="true-stories.html#watergate">Watergate (actual stolen-ops vibes)</a>
<a href="theory-of-the-week.html">Weekly vote</a>
</div></article>

<article class="rabbit-node" id="epstein-branch">
<p class="depth">Believers say vs court record</p>
<h3>Epstein &quot;list&quot; lore</h3>
<p><strong>Believers say:</strong> a secret client list will take down everyone. <strong>What&apos;s documented:</strong> Jeffrey Epstein was a convicted sex offender; he died in federal custody in 2019; civil and criminal court filings, flight logs, and later unsealed documents name many associates — naming someone in a document is not the same as a proven crime by that person. We do not invent charges. Bring popcorn and primary PDFs, not pitchforks.</p>
<div class="rabbit-branches">
<a href="true-stories.html#epstein">Court-record summary</a>
<a href="glossary.html#client-list">Glossary: client list</a>
</div></article>

<article class="rabbit-node" id="jfk-branch">
<p class="depth">Believers say · 1963 onward</p>
<h3>JFK assassination theories</h3>
<p><strong>Believers say:</strong> CIA, mob, Cubans, LBJ, or a combo — anything but a lone gunman. <strong>What&apos;s documented:</strong> Warren Commission concluded Oswald acted alone; House Select Committee later found a &quot;probable conspiracy&quot; on acoustic evidence that remains disputed; millions of pages released via the JFK Records Act. Still the champagne of corkboards.</p>
<div class="rabbit-branches">
<a href="true-stories.html#jfk">JFK records note</a>
<a href="starter-list.html#jfk-books">Starter books</a>
<a href="field-guides/mount-rushmore.html">Stone faces elsewhere</a>
</div></article>

<article class="rabbit-node" id="chemtrails-branch">
<p class="depth">Believers say · Sky lines</p>
<h3>Chemtrails / weather control</h3>
<p><strong>Believers say:</strong> those lines are spraying you on purpose; weather is a weapon. <strong>What&apos;s documented:</strong> contrails are a known aviation physics thing; governments have researched weather modification (e.g., cloud seeding) in limited programs; a global secret spray-cabal remains unproven. Pair with the Chemtrail Cowboys tee and a meteorology textbook.</p>
<div class="rabbit-branches">
<a href="shirts.html#chemtrail-cowboys">Chemtrail Cowboys tee</a>
<a href="glossary.html#chemtrail">Glossary</a>
<a href="true-stories.html#northwoods">Northwoods (real pretext planning)</a>
</div></article>

<article class="rabbit-node" id="money-branch">
<p class="depth">Believers say · Money &amp; pharma lore</p>
<h3>Soros / Big Pharma / &quot;they&quot;</h3>
<p><strong>Right-leaning believers say:</strong> George Soros puppet-masters protests and elections. <strong>Left-leaning believers say:</strong> Koch networks, pharma PACs, and billionaire donors buy policy. <strong>What&apos;s documented:</strong> billionaires on every team fund politics (FEC, OpenSecrets); drug companies lobby hard; scapegoating one surname while ignoring the rest is fan fiction. Follow the money — all of it.</p>
<div class="rabbit-branches">
<a href="glossary.html#follow-the-money">Follow the money</a>
<a href="true-stories.html#iran-contra">Iran-Contra</a>
<a href="starter-list.html">Starter list</a>
</div></article>
'''
    # insert before deeper tunnels or before "All eight"
    if 'id="political-map"' not in t:
        if 'id="deeper"' in t:
            t = t.replace('<article class="rabbit-node" id="deeper">', political_nodes + '\n<article class="rabbit-node" id="deeper">', 1)
        else:
            t = t.replace('<div class="center" style="margin-top:32px" id="hub-cards">', political_nodes + '\n<div class="center" style="margin-top:32px" id="hub-cards">', 1)

    # soften family-friendly only line
    t = t.replace('Family-friendly weirdness only.', 'Weirdness welcome — including spicy politics, labeled carefully.')
    p.write_text(t)
    print('start-here patched', 'political-map' in t)

# ---------- glossary ----------
def patch_glossary():
    p = ROOT/'glossary.html'
    t = p.read_text()
    if 'political-disclaimer' not in t:
        t = t.replace('<section class="cork"><div class="wrap">', '<section class="cork"><div class="wrap">\n'+DISCLAIMER+'\n', 1)
    extra = [
        ('Q drop', 'An anonymous post believers treat like scripture. Bring a grain of salt the size of a salt mine.'),
        ('WWG1WGA', 'Where We Go One We Go All. Rally chant. Also a reminder that group chats escalate.'),
        ('The Storm', 'QAnon phrase for a coming reckoning. Weather apps remain unimpressed.'),
        ('The Great Awakening', 'Believers say: mass enlightenment incoming. Documented: a lot of YouTube thumbnails.'),
        ('Deep State', 'Believers on the right: rogue bureaucracy. Believers on the left: corporate capture. Documented: agencies and lobbyists exist; comic-book hydra optional.'),
        ('Stolen election', 'Said by different teams about 2016 and 2020. Documented elections still certified; vibes were not.'),
        ('Pizzagate', '2016 email-decoding saga. Documented outcome: a real restaurant, a real armed visit, no proven underground cabal.'),
        ('Crisis actor', 'Believers say: tragedy extras. Documented: a rhetorical nuke that often punches victims. Handle like plutonium.'),
        ('False flag', 'Staging an attack to blame someone else. Documented planning exists in history (see Northwoods). Not every bad day is one.'),
        ('Psyop', 'Psychological operation. Fancy word for getting in your head. Works better when you cooperate.'),
        ('Client list', 'Believers say: one PDF ends the elite. Documented: court files name associates; a name ≠ a conviction.'),
        ('Cabal', 'The ultimate they. If your theory needs every rival at the same brunch, check the catering budget.'),
        ('Normies', 'People who touch grass. Occasionally correct. Annoying to absolute certainty dealers.'),
        ('Red-pilled', 'Believers say: awake. Skeptics say: you joined a new fandom. Hydrate either way.'),
        ('Sheeple (political edition)', 'Insult for voters who disagree. Works identically left and right. Try questions instead.'),
        ('Ballot harvesting lore', 'Believers debate legal absentee collection vs fraud. Documented: laws vary by state; vibes are louder than statutes.'),
        ('Shadowbanning', 'Believers say: platforms mute you. Documented: opaque algorithms exist; so does posting through it.'),
        ('NPC', 'Online insult meaning someone has no free will. Ironically very scripted.'),
        ('Drain the swamp', 'Campaign slogan. Swamp creatures on every letterhead. Bring boots for all parties.'),
        ('Colonial pipeline vibes', 'Modern shorthand for &quot;infrastructure got weird.&quot; Check CISA before the meme.'),
    ]
    # only add if missing
    if 'id="q-drop"' not in t and 'Q drop' not in t:
        block = '<h2 class="center" id="political-glossary" style="margin-top:36px">Political <span class="r">&amp; QAnon lingo</span></h2>\n<p class="lead center">Same joke density. Extra salt. Labels matter.</p>\n<div class="glossary-grid political-section">'
        for term, d in extra:
            slug = re.sub(r'[^a-z0-9]+','-', term.lower()).strip('-')
            block += f'<div class="gloss-term" id="{slug}"><dl><dt>{term}</dt><dd>{d}</dd></dl></div>'
        block += '</div>'
        # before signup / end of cork
        t = t.replace('</div></section>\n<section class="redbg"', block+'\n</div></section>\n<section class="redbg"', 1)
        if 'political-glossary' not in t:
            t = t.replace('</div>\n</div></section>', '</div>\n'+block+'\n</div></section>', 1)
    p.write_text(t)
    print('glossary patched')

# ---------- true stories ----------
def patch_true_stories():
    p = ROOT/'true-stories.html'
    t = p.read_text()
    if 'political-disclaimer' not in t:
        t = t.replace('<section class="paper"><div class="wrap">', '<section class="paper"><div class="wrap">\n'+DISCLAIMER+'\n', 1)

    more = '''
<div class="political-section" id="political">
<h2 class="center" style="margin-top:36px">Political scandals that <span class="r">actually happened</span></h2>
<p class="lead">Still documented. Still not a fanfic about your uncle&apos;s group chat.</p>

<article class="story-card" id="watergate">
<h3>Watergate</h3>
<p class="when">1972–1974 · Nixon resignation</p>
<p><strong>What&apos;s documented:</strong> A break-in at Democratic National Committee offices in the Watergate complex, cover-up, Washington Post reporting, Senate investigation, and President Nixon&apos;s resignation. The word &quot;gate&quot; has been stuck to every scandal since — bipartisan branding.</p>
<p class="sources"><strong>Sources:</strong> <a href="https://www.archives.gov/education/lessons/watergate-constitution" target="_blank" rel="noopener">National Archives education page</a> · <a href="https://en.wikipedia.org/wiki/Watergate_scandal" target="_blank" rel="noopener">Wikipedia overview</a></p>
</article>

<article class="story-card" id="iran-contra">
<h3>Iran–Contra</h3>
<p class="when">1980s · Reagan administration investigations</p>
<p><strong>What&apos;s documented:</strong> Senior officials facilitated arms sales to Iran and diverted funds to Contra rebels in Nicaragua despite congressional restrictions. Independent counsel and congressional hearings followed. A masterclass in &quot;off-books&quot; becoming on-front-page.</p>
<p class="sources"><strong>Sources:</strong> <a href="https://www.archives.gov/research/iran-contra" target="_blank" rel="noopener">National Archives research hub</a> · <a href="https://en.wikipedia.org/wiki/Iran%E2%80%93Contra_affair" target="_blank" rel="noopener">Wikipedia overview</a></p>
</article>

<article class="story-card" id="prism">
<h3>Snowden / NSA PRISM disclosures</h3>
<p class="when">2013 · Guardian / Washington Post reporting</p>
<p><strong>What&apos;s documented:</strong> Edward Snowden leaked classified material describing bulk collection programs including PRISM. Major outlets authenticated documents; tech firms disputed &quot;direct access&quot; characterizations; public debate and some reforms followed. Surveillance state: not just a costume.</p>
<p class="sources"><strong>Sources:</strong> <a href="https://www.theguardian.com/world/2013/jun/06/us-tech-giants-nsa-data" target="_blank" rel="noopener">Guardian PRISM report</a> · <a href="https://www.theguardian.com/world/2013/jun/23/edward-snowden-nsa-files-timeline" target="_blank" rel="noopener">Snowden timeline</a> · <a href="https://en.wikipedia.org/wiki/PRISM" target="_blank" rel="noopener">Wikipedia: PRISM</a></p>
</article>

<article class="story-card" id="epstein">
<h3>Epstein criminal case (court record)</h3>
<p class="when">2008 Florida deal · 2019 SDNY indictment · death in custody</p>
<p><strong>What&apos;s documented:</strong> Jeffrey Epstein faced sex-crime cases; a controversial Florida non-prosecution agreement; a 2019 federal indictment in New York; death in federal jail awaiting trial; civil litigation and later document unsealing. <strong>Believers say</strong> a single &quot;client list&quot; convicts a cast of famous people. <strong>We do not:</strong> treat every named associate as proven guilty of Epstein&apos;s crimes. Read filings, not just memes.</p>
<p class="sources"><strong>Sources:</strong> <a href="https://www.justice.gov/usao-sdny/pr/jeffrey-epstein-charged-manhattan-federal-court-sex-trafficking-minors" target="_blank" rel="noopener">SDNY indictment press release</a> · <a href="https://en.wikipedia.org/wiki/Jeffrey_Epstein" target="_blank" rel="noopener">Wikipedia (timeline &amp; citations)</a></p>
</article>

<article class="story-card" id="jfk">
<h3>JFK assassination records</h3>
<p class="when">1963 · Warren Commission · HSCA · JFK Records Act releases</p>
<p><strong>What&apos;s documented:</strong> President Kennedy was assassinated in Dallas; Lee Harvey Oswald was arrested and killed; official inquiries disagreed in nuance; huge archives continue to be released. <strong>Believers say</strong> everything from CIA plots to umbrellas of destiny. Corkboards welcome; invented smoking guns are not.</p>
<p class="sources"><strong>Sources:</strong> <a href="https://www.archives.gov/research/jfk" target="_blank" rel="noopener">National Archives JFK Collection</a> · <a href="https://en.wikipedia.org/wiki/Assassination_of_John_F._Kennedy" target="_blank" rel="noopener">Wikipedia overview</a></p>
</article>
</div>
'''
    if 'id="watergate"' not in t:
        t = t.replace(
            'Want the funny version of curiosity?',
            more + '\n<p class="lead" style="margin-top:24px">Want the funny version of curiosity?',
            1
        )
    # update intro that said no living-politician
    t = t.replace(
        'No fringe political cult content. No living-politician drama here.',
        'Political cases included below — documented ones first, believer lore clearly labeled. We roast both sides.'
    )
    t = t.replace(
        'No QAnon. No living-politician drama here.',
        'Political cases included below — documented ones first, believer lore clearly labeled. We roast both sides.'
    )
    p.write_text(t)
    print('true-stories patched')

print('defs loaded')

# ---------- theory of the week ----------
def patch_totw():
    p = ROOT/'theory-of-the-week.html'
    t = p.read_text()
    # Replace theory content with political one, keep localStorage pattern but new key
    if 'political-disclaimer' not in t:
        t = t.replace('<section class="cork"><div class="wrap">', '<section class="cork"><div class="wrap">\n'+DISCLAIMER+'\n', 1)

    # Update hero eyebrow + replace vote panel theory text
    t = re.sub(
        r'Week of[^<]+Family-friendly',
        'Week of Oct 27, 2026 · Political (roast both sides)',
        t,
        count=1
    )
    # Replace the theory card body if birds still there
    old_theory = None
    if 'Birds aren’t real' in t or 'Birds aren&apos;t real' in t or 'birds-arent-real' in t:
        # replace vote panel inner theory
        t = t.replace('id="birds-arent-real-party"', 'id="deep-state-both-sides"')
        # JS key
        t = t.replace("cp_totw_2026w44_birds", "cp_totw_2026w44_deepstate")
        t = t.replace("birds-arent-real-party", "deep-state-both-sides")

        # Replace headline/paragraph block roughly
        t = re.sub(
            r'<h2 style="margin-top:12px">.*?</h2>\s*<p>.*?</p>\s*<p><em>Related fun on this site:</em>.*?</p>',
            '''<h2 style="margin-top:12px">“The Deep State ate my homework” (both teams)</h2>
<p><strong>Believers on the right say:</strong> a permanent intel/bureaucracy cabal blocks populist presidents. <strong>Believers on the left say:</strong> corporate dark money and captured regulators are the real shadow government. <strong>What&apos;s documented:</strong> huge agencies, classified programs, and billionaire donors on every side exist. The mystical all-knowing hydra is the party trick. Vote the bit — then read <a href="true-stories.html#prism">Snowden/PRISM</a> and <a href="true-stories.html#cointelpro">COINTELPRO</a>.</p>
<p><em>Related:</em> <a href="glossary.html#deep-state">Deep State glossary</a> · <a href="start-here.html#deep-state-branch">Start Here branch</a> · <a href="weird-news.html">Weird News</a></p>''',
            t,
            count=1,
            flags=re.S
        )
    # Add secondary political vote section for screenshot target
    if 'id="political-vote-extra"' not in t:
        extra = '''
<section class="paper political-section" id="political-vote-extra"><div class="wrap">
<h2 class="center">Runner-up theory: <span class="r">election theft (pick a year)</span></h2>
<p class="lead">2016 version popular on the left. 2020 version popular on the right. Same script, swapped jerseys. This page&apos;s main vote stays Deep State; treat this as a discussion prompt, not a second fake poll.</p>
<ul>
<li><strong>Believers (2016):</strong> interference + Comey = stolen. <strong>Documented:</strong> influence ops investigated; Electoral College result stood.</li>
<li><strong>Believers (2020):</strong> fraud = stolen. <strong>Documented:</strong> certifications stood; many lawsuits failed; Jan 6 prosecutions followed for some participants.</li>
</ul>
<p>Roast the double standard. Then pass the snacks.</p>
</div></section>
'''
        t = t.replace('<section class="redbg"', extra + '\n<section class="redbg"', 1)
    p.write_text(t)
    print('totw patched')

# ---------- starter list ----------
def patch_starter():
    p = ROOT/'starter-list.html'
    t = p.read_text()
    if 'political-disclaimer' not in t:
        t = t.replace('<section class="cork"><div class="wrap">', '<section class="cork"><div class="wrap">\n'+DISCLAIMER+'\n', 1)

    block = '''
<div class="political-section" id="political-starter">
<h2 style="margin-top:36px" id="q-into-the-storm">QAnon &amp; political <span class="r">docs / books</span></h2>
<p class="lead">Verified titles. Some explain the movement; some are primary-adjacent history. We are not assigning you a jersey.</p>
<div class="grid">
<article class="card" id="q-into-the-storm-card">
<h3>Q: Into the Storm (HBO, 2021)</h3>
<p class="why">Six-part Cullen Hoback docuseries on QAnon&apos;s online origins, 8chan, and political spillover. Exists; streamed on HBO/Max.</p>
<a class="btn sm" href="https://www.amazon.com/s?k=Q+Into+the+Storm+HBO" target="_blank" rel="noopener sponsored">Find on Amazon</a>
</article>
<article class="card">
<h3>The Storm Is Upon Us — Mike Rothschild</h3>
<p class="why">Journalist&apos;s book on QAnon&apos;s rise. Critical/explanatory; useful for &quot;what is this thing&quot; without joining the fandom.</p>
<a class="btn sm" href="https://www.amazon.com/s?k=The+Storm+Is+Upon+Us+Rothschild" target="_blank" rel="noopener sponsored">Find on Amazon</a>
</article>
<article class="card">
<h3>Active Measures — Thomas Rid</h3>
<p class="why">History of disinformation and political warfare. Helps separate documented influence ops from vibes.</p>
<a class="btn sm" href="https://www.amazon.com/s?k=Active+Measures+Thomas+Rid" target="_blank" rel="noopener sponsored">Find on Amazon</a>
</article>
<article class="card" id="jfk-books">
<h3>JFK records / Warren Commission reading</h3>
<p class="why">Start with National Archives releases, then pick a serious history — not a midnight PDF with Comic Sans.</p>
<a class="btn sm" href="https://www.amazon.com/s?k=Warren+Commission+report" target="_blank" rel="noopener sponsored">Find on Amazon</a>
</article>
<article class="card">
<h3>Dark Money — Jane Mayer</h3>
<p class="why">Left-leaning expose of billionaire political networks. Pair with FEC data so you&apos;re not only dunking one team.</p>
<a class="btn sm" href="https://www.amazon.com/s?k=Dark+Money+Jane+Mayer" target="_blank" rel="noopener sponsored">Find on Amazon</a>
</article>
<article class="card">
<h3>Chaos — Tom O&apos;Neill (already on site picks)</h3>
<p class="why">True-crime / intel-history rabbit hole. Already linked from Conspiraparty book picks.</p>
<a class="btn sm" href="https://amzn.to/4dysGw9" target="_blank" rel="noopener sponsored">View on Amazon</a>
</article>
</div>
<p class="lead">Also: <a href="friends-of-the-committee.html">Friends of the Committee</a> (shows) and <a href="weird-news.html">Weird News</a> for daily political corkboard energy.</p>
</div>
'''
    if 'id="political-starter"' not in t:
        t = t.replace(
            'Also see our <a href="books.html">books page</a>',
            block + '\n<p class="center" style="margin-top:18px">Also see our <a href="books.html">books page</a>',
            1
        )
    p.write_text(t)
    print('starter patched')

# ---------- weird map ----------
def patch_map():
    p = ROOT/'weird-map.html'
    t = p.read_text()
    if 'political-disclaimer' not in t:
        t = t.replace('<section class="black"><div class="wrap">', DISCLAIMER + '\n<section class="black"><div class="wrap">', 1)

    # Add DC pin in SVG if missing
    if 'id="dc-pin"' not in t and 'Washington, DC' not in t:
        # insert circle before closing svg
        dc_circle = '<a id="dc-pin" href="#dc"><circle class="map-pin" cx="790" cy="250" r="14" tabindex="0"><title>Washington, DC</title></circle></a>\n'
        t = t.replace('</svg>', dc_circle + '</svg>', 1)

    dc_section = '''
<section class="paper political-section" id="dc"><div class="wrap">
<h2 class="center">Capital <span class="r">corkboard</span></h2>
<p class="lead">DC is where documented scandals and believer lore share a Metro card.</p>
<div class="map-list">
<article class="card"><h3>Washington, DC</h3><p class="why"><strong>Documented:</strong> Watergate, Capitol, agencies, lobbying. <strong>Believers say:</strong> every basement hides a different cabal depending on which cable news they hate.</p><a class="btn sm" href="true-stories.html#watergate">Watergate</a></article>
<article class="card"><h3>Pentagon / intel corridor lore</h3><p class="why">Believers point at black budgets. Documented black budgets and classified programs exist — see Church Committee and Snowden-era reporting.</p><a class="btn sm" href="true-stories.html#prism">PRISM</a></article>
<article class="card"><h3>Comet Ping Pong (Pizzagate site)</h3><p class="why">Real restaurant. Viral theory. Documented armed incident in 2016. We do not endorse investigating pizza with firearms.</p><a class="btn sm" href="start-here.html#pizzagate-branch">Start Here: Pizzagate</a></article>
<article class="card"><h3>National Archives</h3><p class="why">Where JFK files, Church Committee trails, and FOIA dreams go to become PDFs.</p><a class="btn sm" href="https://www.archives.gov/" target="_blank" rel="noopener">archives.gov</a></article>
</div>
</div></section>
'''
    if 'id="dc"' not in t:
        t = t.replace('<section class="cork"><div class="wrap">', dc_section + '\n<section class="cork"><div class="wrap">', 1)
    p.write_text(t)
    print('weird-map patched')

# ---------- join the agency ----------
def patch_join():
    p = ROOT/'join-the-agency.html'
    t = p.read_text()
    if 'political-disclaimer' not in t:
        # after hero sub
        t = t.replace(
            '<main id="main">',
            '<main id="main">\n'+DISCLAIMER+'\n',
            1
        )
    wink = '''
<section class="black political-section" id="agency-wink"><div class="wrap center">
<h2>Clearance levels <span class="r">(joke edition)</span></h2>
<p class="lead">Whether you arrived from Bigfoot Twitter or a Q drop rabbit hole, the badge is still free and still cardboard. We do not issue real security clearances, secret decoder rings, or voting advice. We do roast the spin on all sides and hand you a printable.</p>
<ul style="text-align:left;max-width:560px;margin:18px auto;line-height:1.5">
<li><strong>Level Foil:</strong> You just want the party hat.</li>
<li><strong>Level Corkboard:</strong> You color-code theories and still cite sources.</li>
<li><strong>Level Archive:</strong> You open the National Archives before the meme page.</li>
<li><strong>Level Both-Sides Roast:</strong> You dunk on every jersey. Preferred.</li>
</ul>
<p><a class="btn" href="start-here.html#political-map">See the political map</a> <a class="btn alt" href="weird-news.html">Weird News</a></p>
</div></section>
'''
    if 'id="agency-wink"' not in t:
        t = t.replace('<section class="paper" id="agency-form">', wink + '\n<section class="paper" id="agency-form">', 1)
    # wink in sub copy
    t = t.replace(
        'Shadow Party Committee clearance starts with an email.',
        'Shadow Party Committee clearance starts with an email — whether you came for Bigfoot or the political corkboard.'
    )
    p.write_text(t)
    print('join patched')

# ---------- quiz ----------
def patch_quiz():
    p = ROOT/'quiz-theorist.html'
    t = p.read_text()
    if 'political-disclaimer' not in t:
        t = t.replace('<section class="cork"><div class="wrap center">', '<section class="cork"><div class="wrap center">\n'+DISCLAIMER+'\n', 1)

    # Add 2 political questions before submit button if not present
    if 'name="q8"' not in t:
        q_pol = '''
<fieldset class="paper quiz-q political-section" id="political-quiz-qs"><legend><strong>9. Your take on &quot;the Deep State&quot; is…</strong></legend>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q8" value="qanon" required> Believers on the right are onto something about bureaucracy</label>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q8" value="resist" required> Believers on the left are onto something about dark money</label>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q8" value="leak" required> I just want the documents, not the jersey</label>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q8" value="slide" required> I made a slide deck roasting both</label>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q8" value="foil" required> I wrapped my remote in foil and changed the channel</label>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q8" value="tour" required> I bought a tee that mocks every cabal</label>
</fieldset>
<fieldset class="paper quiz-q"><legend><strong>10. Stolen-election talk comes up at dinner. You…</strong></legend>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q9" value="qanon" required> Ask which year — 2016 or 2020 — and watch the room short-circuit</label>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q9" value="resist" required> Quote a report, then admit your team overplayed it once</label>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q9" value="leak" required> Screenshot the chat for the group archive</label>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q9" value="slide" required> Propose a PowerPoint Night sudden-death round</label>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q9" value="bigfoot" required> Change the subject to Bigfoot like a diplomat</label>
<label style="display:block;margin:8px 0;cursor:pointer"><input type="radio" name="q9" value="tour" required> Sell them a Totally Real Tour shirt as a peace treaty</label>
</fieldset>
'''
        t = t.replace('<button class="btn big" type="submit">Reveal My File</button>', q_pol + '\n<button class="btn big" type="submit">Reveal My File</button>', 1)

    # Add political results to JS R object
    if '"qanon"' not in t:
        insert = '''    qanon: {t:'The Q-Adjacent Corkboard Captain', d:'You collect drops like trading cards but (hopefully) still check primary sources. Believers on your feed are loud; archives are louder. Roast certainty theater.', u:'weird-news.html', p:'Weird News political rabbit holes', i:'assets/img/logo-stamp.png'},
    resist: {t:'The Both-Sides Resistance Archivist', d:'You distrust billionaires, bureaus, and anyone who says trust them. Dark money and deep state are both real hobbies — documented pieces, mythical hydra optional.', u:'true-stories.html#prism', p:'Snowden/PRISM true story', i:'assets/img/kit-0.webp'},
'''
        t = t.replace('var R = {', 'var R = {\n' + insert, 1)
        # if minified differently
        if insert.strip()[:20] not in t:
            t = t.replace('var R={', 'var R={' + insert.replace('\n','').replace('    ',''), 1)

    # Update hero sub
    t = t.replace(
        '8 questions. 6 classified results.',
        '10 questions. Political results included. Still zero government approval.'
    )
    p.write_text(t)
    print('quiz patched')

# CSS tweak for political sections
def patch_css():
    css = ROOT/'assets/beginner-hub.css'
    t = css.read_text()
    extra = '''
.political-disclaimer{font-size:.92rem;line-height:1.45}
.political-section{scroll-margin-top:80px}
.rabbit-node.political-section{box-shadow:6px 6px 0 #111}
'''
    if '.political-disclaimer' not in t:
        css.write_text(t + extra)
    print('css patched')

def main():
    patch_css()
    patch_start_here()
    patch_glossary()
    patch_true_stories()
    patch_totw()
    patch_starter()
    patch_map()
    patch_join()
    patch_quiz()
    print('ALL POLITICAL PATCHES DONE')

if __name__ == '__main__':
    main()
