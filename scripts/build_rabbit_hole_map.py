#!/usr/bin/env python3
"""Build start-here.html as interactive corkboard Rabbit Hole Map."""
from __future__ import annotations
import json, html, re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
WN = json.loads((ROOT / "data/weird-news.json").read_text())
GEN = WN.get("generated_at_display", "Oct 29, 2026")

def esc(s): return html.escape(s or "", quote=True)

# Tag mapping from weird-news tags to our node ids
TAG_TO_NODES = {
  "UFO": ["uap", "area51"],
  "Cryptid": ["bigfoot"],
  "QAnon": ["qanon", "deepstate"],
  "Politics": ["deepstate", "election2016", "election2020"],
  "Odd": ["birds"],
  "Strange": ["uap", "flatearth"],
  "Science": ["covid", "moon"],
}

def breaking_for(node_id, limit=2):
  items = []
  for it in WN.get("items", []):
    tags = TAG_TO_NODES.get(it.get("tag",""), [])
    if node_id in tags or (node_id=="birds" and it.get("tag")=="Odd"):
      items.append(it)
  # fallback: any Politics for political nodes
  if not items and node_id in ("epstein","jfk","nine11","fed","rothschilds","bilderberg","mkultra","chemtrails","covid","moon","flatearth"):
    for it in WN.get("items", []):
      if it.get("tag") in ("Politics","QAnon","Strange","Science","UFO"):
        items.append(it)
        if len(items)>=limit: break
  return items[:limit]

# ---- Graph: nodes + edges -------------------------------------------------
NODES = [
  {"id":"qanon","label":"QAnon","x":520,"y":120,"group":"pol"},
  {"id":"nine11","label":"9/11","x":280,"y":160,"group":"hist"},
  {"id":"uap","label":"UAP Disclosure","x":760,"y":140,"group":"ufo"},
  {"id":"epstein","label":"Epstein Files","x":480,"y":260,"group":"pol"},
  {"id":"jfk","label":"JFK","x":200,"y":280,"group":"hist"},
  {"id":"moon","label":"Moon Landing","x":860,"y":280,"group":"space"},
  {"id":"deepstate","label":"Deep State","x":400,"y":180,"group":"pol"},
  {"id":"election2016","label":"Election 2016","x":160,"y":400,"group":"pol"},
  {"id":"election2020","label":"Election 2020","x":320,"y":420,"group":"pol"},
  {"id":"covid","label":"COVID Origins","x":620,"y":380,"group":"sci"},
  {"id":"chemtrails","label":"Chemtrails","x":780,"y":400,"group":"sci"},
  {"id":"mkultra","label":"MKUltra","x":140,"y":180,"group":"hist"},
  {"id":"area51","label":"Area 51","x":900,"y":180,"group":"ufo"},
  {"id":"bigfoot","label":"Bigfoot","x":940,"y":360,"group":"cryptid"},
  {"id":"flatearth","label":"Flat Earth","x":700,"y":500,"group":"space"},
  {"id":"birds","label":"Birds Aren't Real","x":860,"y":480,"group":"cryptid"},
  {"id":"rothschilds","label":"Banking Dynasties","x":100,"y":100,"group":"money"},
  {"id":"fed","label":"Federal Reserve","x":80,"y":320,"group":"money"},
  {"id":"bilderberg","label":"Bilderberg / WEF","x":240,"y":80,"group":"money"},
]

EDGES = [
  ("qanon","deepstate"),("qanon","epstein"),("qanon","election2020"),
  ("deepstate","mkultra"),("deepstate","jfk"),("deepstate","nine11"),
  ("deepstate","election2016"),("deepstate","election2020"),
  ("epstein","deepstate"),("epstein","fed"),("epstein","bilderberg"),
  ("jfk","mkultra"),("jfk","nine11"),("jfk","area51"),
  ("nine11","fed"),("nine11","deepstate"),
  ("uap","area51"),("uap","deepstate"),("area51","moon"),
  ("moon","flatearth"),("moon","area51"),("flatearth","chemtrails"),
  ("covid","chemtrails"),("covid","deepstate"),("covid","bilderberg"),
  ("fed","rothschilds"),("fed","bilderberg"),("rothschilds","bilderberg"),
  ("rothschilds","deepstate"),("bilderberg","deepstate"),
  ("bigfoot","area51"),("birds","deepstate"),("birds","flatearth"),
  ("election2016","election2020"),("epstein","qanon"),
]

# Content per node
def L(kind, title, url):
  return {"kind":kind,"title":title,"url":url}

CONTENT = {}

CONTENT["qanon"] = {
  "hook":"Anonymous 'Q' drops, a sprawling online mythology, and a movement that jumped from message boards into real-world politics.",
  "paths":[
    {"title":"The drops","to":None,"blurb":"How 'Q' posts started on 4chan/8chan and got read as coded intel."},
    {"title":"Pizzagate adjacency","to":"epstein","blurb":"Believers often link earlier viral claims to later elite-trafficking narratives."},
    {"title":"Deep State frame","to":"deepstate","blurb":"The story treats career intel/bureaucracy as a cabal fighting populists."},
    {"title":"Election stakes","to":"election2020","blurb":"Many drops centered on stolen-election and 'storm' timelines."},
  ],
  "bunk":"Believers say an anonymous military-intel insider ('Q') posted coded crumbs exposing a satanic pedophile cabal inside government and Hollywood, and that Trump was secretly fighting it. They treat failed dates as 'disinfo' or calendar misreads, not falsification.",
  "debunk":"Skeptics say QAnon is ARG-style improvisation + crowdsourced pattern-matching, with no verified insider, repeatedly missed predictions, and real-world harm when people acted on the lore. Researchers map it as a big-tent conspiracy culture, not a single file dump.",
  "believers":"Believers say the drops were military intelligence, that elites run trafficking networks, and that media denial is the cover.",
  "on_record":"Public record: Q posts appeared on anonymous imageboards starting 2017; the identity of 'Q' was never officially confirmed; platforms later banned QAnon content; some believers committed crimes citing the lore (reported in court cases). No U.S. agency has authenticated the drops as official intel.",
  "unanswered":[
    "Who wrote the Q posts, and were multiple people involved over time?",
    "Which specific trafficking claims rest on court records vs social-media rumor?",
    "Why did major predicted 'storm' dates pass without the forecasted mass arrests?",
  ],
  "talk":[
    "If an anonymous poster claimed to be military intel, what would convince you they were real — or not?",
    "Where should people draw the line between asking hard questions and treating online lore as evidence?",
  ],
  "primary":[
    L("Primary document","FBI bulletin context (Vault / public reporting hubs)","https://vault.fbi.gov/cointel-pro"),
    L("Primary document","Church Committee overview (Senate) — historical domestic-intel abuse","https://www.senate.gov/about/powers-procedures/investigations/church-committee.htm"),
  ],
  "dig":[
    L("Believers","QAnon overview (read the claims side)","https://en.wikipedia.org/wiki/QAnon"),
    L("Independent","EFF on mass surveillance programs (context for 'Deep State' fears)","https://www.eff.org/nsa-spying"),
    L("Mainstream","PRISM program overview","https://en.wikipedia.org/wiki/PRISM_(surveillance_program)"),
    L("Believers","Deep State lore page (connected frame)","https://en.wikipedia.org/wiki/Deep_state_conspiracy_theory_in_the_United_States"),
  ],
  "connect":["deepstate","epstein","election2020","mkultra"],
  "hint":"Hosting a party about this? Try Weird News for fresh headlines.",
  "site":[("Weird News","weird-news.html"),("Glossary","glossary.html"),("True Stories","true-stories.html")],
}

CONTENT["nine11"] = {
  "hook":"The attacks, the Commission Report, Building 7, and decades of 'what aren't they telling us' debates.",
  "paths":[
    {"title":"Commission Report","to":None,"blurb":"The official multi-volume narrative and its footnotes."},
    {"title":"Building 7 / NIST","to":None,"blurb":"Why WTC 7's collapse became a separate rabbit hole."},
    {"title":"Saudi / 28 pages","to":"deepstate","blurb":"Declassified pages and foreign-funding questions."},
    {"title":"War & money trails","to":"fed","blurb":"Believers connect the attacks to wars, PATRIOT Act powers, and finance."},
  ],
  "bunk":"Believers say the official story leaves explosive gaps (especially WTC 7), that foreknowledge or controlled demolition is on the table, and that intelligence failures look too convenient. Some point to put options, war plans, and the 28 pages.",
  "debunk":"Skeptics point to the 9/11 Commission Report, NIST engineering studies, and the large open-source record of the hijackings. They argue controlled-demolition claims fail physical tests and that bureaucratic failure is not the same as an inside job — while still criticizing intel silos and Saudi-related unanswered questions.",
  "believers":"Believers say jet fuel can't explain molten metal / WTC 7 free-fall signatures, and that the government used the attacks to expand surveillance and wars.",
  "on_record":"On the record: 19 hijackers; four planes; WTC 1/2/7 and Pentagon damage; nearly 3,000 dead. The 9/11 Commission Report (2004) is a public primary document. NIST published WTC collapse reports. Portions of the '28 pages' related to foreign support were later declassified. The PATRIOT Act and wars in Afghanistan/Iraq followed.",
  "unanswered":[
    "What exactly do the remaining still-classified files contain?",
    "How should the public weigh Saudi-related financing questions that investigators flagged?",
    "Why did WTC 7 become such a focal point, and what would a fresh independent engineering review change?",
  ],
  "talk":[
    "Have you ever read even one chapter of the 9/11 Commission Report yourself?",
    "What's the difference between 'intel failed' and 'intel planned it' — and how would you tell?",
  ],
  "primary":[
    L("Primary document","9/11 Commission Report (PDF)","https://www.9-11commission.gov/report/911Report.pdf"),
    L("Primary document","9/11 Commission Report (GovInfo PDF)","https://www.govinfo.gov/content/pkg/GPO-911REPORT/pdf/GPO-911REPORT.pdf"),
  ],
  "dig":[
    L("Mainstream","September 11 attacks overview","https://en.wikipedia.org/wiki/September_11_attacks"),
    L("Independent","National Security Archive (declassified research hub)","https://nsarchive.gwu.edu/"),
    L("Believers","9/11 and Deep State adjacency discussions (start at Deep State page, then branch)","https://en.wikipedia.org/wiki/Deep_state_conspiracy_theory_in_the_United_States"),
    L("Independent","EFF: NSA spying after 9/11 powers expanded","https://www.eff.org/nsa-spying"),
  ],
  "connect":["deepstate","jfk","fed","epstein"],
  "hint":None,
  "site":[("True Stories","true-stories.html"),("Glossary","glossary.html")],
}

CONTENT["uap"] = {
  "hook":"From 'UFOs are for cranks' to Pentagon programs, congressional hearings, and AARO reports — the stigma cracked.",
  "paths":[
    {"title":"2017 NYT / AATIP","to":None,"blurb":"How mainstream coverage shifted overnight."},
    {"title":"2023 House hearing","to":"deepstate","blurb":"Whistleblower testimony under oath — claims vs proof."},
    {"title":"AARO / ODNI reports","to":None,"blurb":"What official assessments actually published."},
    {"title":"Area 51 overlap","to":"area51","blurb":"Classified aircraft testing vs non-human craft claims."},
  ],
  "bunk":"Believers say governments have recovered non-human craft and biologics, run legacy crash-retrieval programs, and that hearings prove a cover-up of non-human intelligence.",
  "debunk":"Skeptics say sensor artifacts, drones, balloons, and classified human tech explain most cases; they note extraordinary claims need extraordinary evidence, and that testimony is not the same as physical proof released to the public.",
  "believers":"Believers say multiple military witnesses describe craft beyond known human tech, and that stigma was the cover.",
  "on_record":"On the record: DoD acknowledged UAP study efforts; ODNI and AARO have issued public reports; Congress held open hearings (including July 2023) with whistleblower claims. Official reports have not released verified alien biologics to the public. Many cases remain unidentified in the data.",
  "unanswered":[
    "What share of UAP cases have prosaic explanations once full sensor data is available?",
    "Are any retrieved materials publicly authenticated as non-human?",
    "How much of the secrecy is just classified aerospace programs?",
  ],
  "talk":[
    "If a pilot reports an object that outruns jets, what evidence would you want before calling it alien?",
    "Should Congress keep holding open UAP hearings even if most cases resolve as balloons?",
  ],
  "primary":[
    L("Primary document","House UAP hearing video (C-SPAN / widely mirrored)","https://www.youtube.com/watch?v=ZCcm2QlVD7M"),
    L("Primary document","UAP topic overview with report citations","https://en.wikipedia.org/wiki/Unidentified_anomalous_phenomenon"),
  ],
  "dig":[
    L("Believers","Area 51 lore (connected node)","https://en.wikipedia.org/wiki/Area_51"),
    L("Independent","National Security Archive","https://nsarchive.gwu.edu/"),
    L("Mainstream","UAP Wikipedia hub (cites ODNI/AARO)","https://en.wikipedia.org/wiki/Unidentified_anomalous_phenomenon"),
    L("Believers","Field guide: Area 51","field-guides/area-51.html"),
  ],
  "connect":["area51","deepstate","moon","jfk"],
  "hint":"Field gear: free Area 51 Suspicious Field Guide on this site.",
  "site":[("Field Guides","field-guides.html"),("Weird News","weird-news.html")],
}

CONTENT["epstein"] = {
  "hook":"A convicted sex offender, an island, flight logs, sealed then unsealed court files, and a death that still splits the room.",
  "paths":[
    {"title":"Court unsealings","to":None,"blurb":"Giuffre v. Maxwell and waves of document releases."},
    {"title":"Maxwell conviction","to":None,"blurb":"What a jury found vs what online lore adds."},
    {"title":"Intelligence rumors","to":"deepstate","blurb":"Claims of kompromat / intel ties — labeled as claims."},
    {"title":"Money & clients","to":"fed","blurb":"Banking, billionaires, and who appears in records."},
    {"title":"Island / logistics","to":None,"blurb":"Little St. James, planes, staff — documented pieces vs leaps."},
  ],
  "bunk":"Believers say Epstein ran a blackmail operation for (or with) intelligence services, that client lists are being protected, and that his 2019 jail death was not a simple suicide.",
  "debunk":"Skeptics say the documented sex-trafficking crimes are horrific enough without unproven spy-master plots; they note DOJ materials, autopsy/medical examiner findings of suicide, and warn against treating every famous name in flight logs as proven guilt.",
  "believers":"Believers say the network was bigger than one predator, that powerful people were protected, and that 'suicide' stretches credulity given the broken cameras and prior deal.",
  "on_record":"On the record: Epstein pleaded guilty in Florida (2008 state case); was arrested again in 2019 on federal sex-trafficking charges; died in jail in August 2019 (NYC medical examiner ruled suicide; controversy followed). Ghislaine Maxwell was convicted in 2021 on federal sex-trafficking-related charges. Courts unsealed large document sets in Giuffre v. Maxwell (including January 2024 waves). DOJ maintains an Epstein files page. Being named in a document is not the same as a criminal conviction.",
  "unanswered":[
    "Which associates face unfinished investigations vs rumor?",
    "What surveillance-camera and staffing failures in the jail have been fully explained in public?",
    "How should readers separate civil-case allegations from criminal findings?",
  ],
  "talk":[
    "What's the difference between a name in an unsealed filing and a guilty verdict?",
    "Why do elite abuse cases make people leap to intelligence plots — and when is that fair?",
  ],
  "primary":[
    L("Primary document","U.S. DOJ Epstein files page","https://www.justice.gov/epstein"),
    L("Mainstream","Jeffrey Epstein overview (court timeline)","https://en.wikipedia.org/wiki/Jeffrey_Epstein"),
  ],
  "dig":[
    L("Believers","Deep State connection many readers explore next","https://en.wikipedia.org/wiki/Deep_state_conspiracy_theory_in_the_United_States"),
    L("Independent","National Security Archive (how to read declassified files)","https://nsarchive.gwu.edu/"),
    L("Mainstream","Ghislaine Maxwell overview","https://en.wikipedia.org/wiki/Ghislaine_Maxwell"),
    L("Believers","QAnon adjacency (how online movements absorbed Epstein lore)","https://en.wikipedia.org/wiki/QAnon"),
  ],
  "connect":["deepstate","qanon","fed","bilderberg"],
  "hint":None,
  "site":[("Weird News","weird-news.html"),("True Stories","true-stories.html#watergate")],
}

CONTENT["jfk"] = {
  "hook":"Dallas, 1963. Warren Commission vs House Select Committee. Millions of pages still argued over.",
  "paths":[
    {"title":"Warren Commission","to":None,"blurb":"Lone gunman conclusion and its critics."},
    {"title":"HSCA / acoustic debate","to":None,"blurb":"Later Congress suggested possible conspiracy — then fights over the data."},
    {"title":"CIA / Cuba / Mafia triangles","to":"mkultra","blurb":"Documented plots and contacts fuel alternate maps."},
    {"title":"File releases","to":"deepstate","blurb":"National Archives JFK collection waves."},
  ],
  "bunk":"Believers say Oswald didn't act alone — CIA, Cubans, mob, or LBJ-adjacent plots appear depending on the book — and that destroyed or delayed files prove a cover-up.",
  "debunk":"Skeptics stick with Oswald as the shooter based on ballistics and timeline evidence in the Warren Report, while conceding CIA/FBI withheld information and that secrecy fed distrust. They treat every new name-drop as not automatically a second gunman.",
  "believers":"Believers say the magic-bullet theory is absurd, that intelligence agencies had motive after Bay of Pigs / Cuba plots, and that file delays are the tell.",
  "on_record":"On the record: President Kennedy was assassinated in Dallas on Nov 22, 1963; Lee Harvey Oswald was arrested and then killed by Jack Ruby. The Warren Commission (1964) concluded Oswald acted alone. The HSCA (1979) concluded a 'probable conspiracy' on acoustic evidence later disputed. The National Archives continues JFK Records Collection releases. CIA plots against Castro and other Cold War operations are documented separately.",
  "unanswered":[
    "What remains withheld or redacted, and why?",
    "Does any release change the physical shooting timeline?",
    "How should 'probable conspiracy' from HSCA be read after acoustic critiques?",
  ],
  "talk":[
    "If new files name more CIA contacts, does that prove a second shooter — or just a messy Cold War?",
    "Why do assassinations create permanent alternate maps?",
  ],
  "primary":[
    L("Primary document","National Archives — JFK research hub","https://www.archives.gov/research/jfk"),
    L("Primary document","National Archives — JFK releases","https://www.archives.gov/research/jfk/release"),
  ],
  "dig":[
    L("Mainstream","Assassination of John F. Kennedy overview","https://en.wikipedia.org/wiki/Assassination_of_John_F._Kennedy"),
    L("Independent","National Security Archive","https://nsarchive.gwu.edu/"),
    L("Believers","MKUltra (mind-control lore people connect)","https://en.wikipedia.org/wiki/Project_MKUltra"),
    L("Primary document","Sample CIA CREST-style PDF in reading room","https://www.cia.gov/readingroom/docs/CIA-RDP96-00788R001700210016-5.pdf"),
  ],
  "connect":["mkultra","deepstate","nine11","area51"],
  "hint":None,
  "site":[("True Stories","true-stories.html"),("Glossary","glossary.html")],
}

CONTENT["moon"] = {
  "hook":"Flags, shadows, Van Allen belts, and a cottage industry of documentaries arguing studio vs Sea of Tranquility.",
  "paths":[
    {"title":"Photography anomalies","to":None,"blurb":"Believer docs zoom on lighting, shadows, crosshairs."},
    {"title":"Radiation / Van Allen","to":None,"blurb":"Could 1960s tech transit the belts?"},
    {"title":"Lost tapes / telemetry","to":"deepstate","blurb":"Missing SSTV tapes became a lore magnet."},
    {"title":"Flat Earth crossover","to":"flatearth","blurb":"Some communities merge moon-hoax and flat-earth claims."},
  ],
  "bunk":"Believers say Apollo footage was filmed on Earth, that radiation made crewed transit impossible with 1960s shielding, and that photo anomalies (shadows, wind-blown flag) are the giveaway. Documentaries like Bart Sibrel's and Massimo Mazzucco's American Moon argue the case at length.",
  "debunk":"Skeptics point to retroreflectors on the Moon, independent tracking by other countries, rock samples, and thousands of mission photos/telemetries. They argue 'flag waving' is inertia in vacuum and that radiation risk was managed with trajectory/timing — while admitting NASA PR sometimes oversimplified.",
  "believers":"Believers say you can see the stage lighting in the photos, that later programs can't easily repeat 1969 feats, and that whistleblower interviews were suppressed.",
  "on_record":"On the record: NASA's Apollo 11 mission page and mission materials describe the July 1969 landing. Rock samples and laser retroreflectors are part of the public scientific record. Moon-landing-hoax documentaries exist as published media (Sibrel 2001; Mazzucco's American Moon 2017).",
  "unanswered":[
    "Which specific photo 'anomalies' survive when photographers recreate lighting in vacuum-analog conditions?",
    "What exactly was lost in tape recycling, and what still exists in archives?",
    "Why do Artemis architectures look so different from Apollo — engineering, politics, or both?",
  ],
  "talk":[
    "Watch five minutes of a hoax documentary and five minutes of mission film — what jumps out to you?",
    "If another country tracked Apollo, how much weight does that carry for you?",
  ],
  "primary":[
    L("Primary document","NASA Apollo 11 mission page","https://www.nasa.gov/mission/apollo-11/"),
    L("Mainstream","Apollo 11 overview","https://en.wikipedia.org/wiki/Apollo_11"),
  ],
  "dig":[
    L("Believers","A Funny Thing Happened on the Way to the Moon (Bart Sibrel) — YouTube","https://www.youtube.com/watch?v=xciCJfbTvE4"),
    L("Believers","American Moon (Massimo Mazzucco) — YouTube English","https://www.youtube.com/watch?v=KpuKu3F0BvY"),
    L("Believers","Bart Sibrel site / films","https://www.sibrel.com/"),
    L("Believers","Film page: A Funny Thing Happened…","https://en.wikipedia.org/wiki/A_Funny_Thing_Happened_on_the_Way_to_the_Moon"),
    L("Mainstream","NASA Apollo 11","https://www.nasa.gov/mission/apollo-11/"),
  ],
  "connect":["flatearth","area51","uap","deepstate"],
  "hint":None,
  "site":[("Quiz","quiz-theorist.html"),("Field Guides","field-guides.html")],
}

CONTENT["deepstate"] = {
  "hook":"Career bureaucracy, intel agencies, contractors — or a mystical hydra, depending who you ask.",
  "paths":[
    {"title":"Documented programs","to":"mkultra","blurb":"COINTELPRO, MKUltra, PRISM — real files."},
    {"title":"Both-party versions","to":"election2016","blurb":"Right and left accuse different cabals with similar language."},
    {"title":"Epstein / kompromat lore","to":"epstein","blurb":"Blackmail-as-governance theories."},
    {"title":"Q overlay","to":"qanon","blurb":"How online drops branded the idea."},
  ],
  "bunk":"Believers (on the right) say a permanent intel/administrative cabal sabotages elected outsiders. Believers (on the left) say corporate donors, captured regulators, and security state continuity are the real shadow government. Both say 'accountability theater' hides continuity of agendas.",
  "debunk":"Skeptics say agencies are powerful and often abusive (see Church Committee) but not a single omniscient hive mind; incentives, turf wars, and ideology explain a lot without a secret membership card. They warn 'Deep State' can become an unfalsifiable catch-all.",
  "believers":"Believers say leaks, surveillance powers, and revolving-door contractors prove an unaccountable parallel government.",
  "on_record":"On the record: Church Committee documented FBI/CIA abuses; Snowden disclosures revealed PRISM and related programs; classified budgets and contractors are large. Watergate showed a president's apparatus committing crimes. None of that requires a single cartoon cabal — and it also shows why distrust is rational.",
  "unanswered":[
    "Where does legitimate secrecy end and democratic oversight fail?",
    "Which modern programs have never had Church-Committee-level sunlight?",
    "How do left and right 'Deep State' stories talk past each other?",
  ],
  "talk":[
    "Name one documented abuse (COINTELPRO, MKUltra, PRISM). Does that make every rival theory true?",
    "Who benefits when 'Deep State' means whatever you already hated?",
  ],
  "primary":[
    L("Primary document","Church Committee (Senate overview)","https://www.senate.gov/about/powers-procedures/investigations/church-committee.htm"),
    L("Primary document","FBI Vault: COINTELPRO","https://vault.fbi.gov/cointel-pro"),
  ],
  "dig":[
    L("Independent","EFF on NSA spying","https://www.eff.org/nsa-spying"),
    L("Mainstream","PRISM overview","https://en.wikipedia.org/wiki/PRISM_(surveillance_program)"),
    L("Believers","Deep State conspiracy theory page","https://en.wikipedia.org/wiki/Deep_state_conspiracy_theory_in_the_United_States"),
    L("Mainstream","Watergate (Archives education)","https://www.archives.gov/education/lessons/watergate-constitution"),
  ],
  "connect":["mkultra","qanon","epstein","nine11","election2016","election2020"],
  "hint":None,
  "site":[("True Stories","true-stories.html"),("Theory of the Week","theory-of-the-week.html")],
}

CONTENT["election2016"] = {
  "hook":"Russia probes, Comey letters, WikiLeaks, and a left-leaning 'stolen' narrative that flipped jerseys later.",
  "paths":[
    {"title":"ICA / Mueller","to":"deepstate","blurb":"Intelligence assessments and the Special Counsel report."},
    {"title":"Comey / email saga","to":None,"blurb":"Believers on the left still start here."},
    {"title":"CrowdStrike / DNC server lore","to":None,"blurb":"What was examined by whom — still argued."},
    {"title":"2020 mirror","to":"election2020","blurb":"Same script, swapped teams."},
  ],
  "bunk":"Believers on the left said Russian interference + Comey + voter suppression stole 2016 from Clinton. Some still call the Electoral College itself illegitimate relative to the popular vote.",
  "debunk":"Skeptics note Trump won the Electoral College under existing rules; Mueller documented interference and charging decisions without alleging that votes were altered enough to overturn the certified result. They criticize both 'Russia did nothing' minimization and 'every leak was Kremlin' maximalism.",
  "believers":"Believers say influence ops + FBI email timing + Cambridge Analytica-style targeting tipped a close race.",
  "on_record":"On the record: U.S. intelligence assessed Russian interference aimed at the 2016 election; Mueller's investigation produced indictments and a report; the Electoral College result was certified. Debates continue over scope and impact.",
  "unanswered":[
    "How much did influence operations change individual votes vs amplify existing divides?",
    "What would a fully public forensic standard for 'interference mattered' look like?",
  ],
  "talk":[
    "Did you apply the same standard to 2016 doubts as you did to 2020 doubts?",
    "What's the difference between foreign influence and swapped ballots?",
  ],
  "primary":[
    L("Mainstream","Russian interference in 2016 overview","https://en.wikipedia.org/wiki/Russian_interference_in_the_2016_United_States_elections"),
    L("Primary document","DOJ election infrastructure archive hub","https://www.justice.gov/archives/ag/election-infrastructure"),
  ],
  "dig":[
    L("Believers","Deep State frame used by multiple sides","https://en.wikipedia.org/wiki/Deep_state_conspiracy_theory_in_the_United_States"),
    L("Independent","EFF surveillance context","https://www.eff.org/nsa-spying"),
    L("Mainstream","2016 interference overview","https://en.wikipedia.org/wiki/Russian_interference_in_the_2016_United_States_elections"),
    L("Believers","QAnon later absorbed election lore","https://en.wikipedia.org/wiki/QAnon"),
  ],
  "connect":["election2020","deepstate","qanon"],
  "hint":None,
  "site":[("Weird News","weird-news.html"),("Theory of the Week","theory-of-the-week.html")],
}

CONTENT["election2020"] = {
  "hook":"Mail ballots, late-night counts, lawsuits, Jan 6 — and a right-leaning 'stolen' narrative that mirrored 2016's energy.",
  "paths":[
    {"title":"Lawsuit record","to":None,"blurb":"What courts actually ruled vs what viral clips claimed."},
    {"title":"Cyber / Dominion lore","to":"deepstate","blurb":"Machine theories and their evidence bars."},
    {"title":"Jan 6","to":"qanon","blurb":"Protest, riot, and prosecutions — contested frames."},
    {"title":"2016 mirror","to":"election2016","blurb":"Swap the jerseys, keep the distrust."},
  ],
  "bunk":"Believers on the right say fraud, illegal ballot rules, and machine manipulation stole 2020. They treat certifications as coerced and point to affidavits and anomaly charts.",
  "debunk":"Skeptics say certifications stood, many lawsuits failed on standing or merits, and recounts/audits in key states did not flip electors. They still argue some pandemic rule changes deserved more sunlight — without leaping to nationwide machine theft.",
  "believers":"Believers say statistical impossibilities + suppressed evidence + Big Tech censorship equal a stolen election.",
  "on_record":"On the record: Biden won the certified Electoral College; Trump and allies filed numerous lawsuits with mixed procedural outcomes; some states conducted audits/recounts; Jan 6, 2021 breach of the Capitol led to many federal prosecutions. DOJ has election-infrastructure materials in public archives.",
  "unanswered":[
    "Which specific fraud allegations produced criminal convictions vs viral charts?",
    "How should emergency pandemic voting changes be evaluated without team jerseys?",
  ],
  "talk":[
    "Would you accept the same evidence standard you demand from the other side?",
    "What would a bipartisan, pre-agreed audit protocol look like next time?",
  ],
  "primary":[
    L("Mainstream","Attempts to overturn 2020 overview","https://en.wikipedia.org/wiki/Attempts_to_overturn_the_2020_United_States_presidential_election"),
    L("Primary document","DOJ election infrastructure archive","https://www.justice.gov/archives/ag/election-infrastructure"),
  ],
  "dig":[
    L("Believers","QAnon and election lore","https://en.wikipedia.org/wiki/QAnon"),
    L("Believers","Deep State frame","https://en.wikipedia.org/wiki/Deep_state_conspiracy_theory_in_the_United_States"),
    L("Mainstream","2020 overturn attempts overview","https://en.wikipedia.org/wiki/Attempts_to_overturn_the_2020_United_States_presidential_election"),
    L("Independent","EFF (speech/censorship fights around elections)","https://www.eff.org/nsa-spying"),
  ],
  "connect":["election2016","qanon","deepstate"],
  "hint":None,
  "site":[("Weird News","weird-news.html"),("Theory of the Week","theory-of-the-week.html")],
}

CONTENT["covid"] = {
  "hook":"Lab leak vs zoonosis, gain-of-function fights, and a info-war that made everyone trust less.",
  "paths":[
    {"title":"Lab-leak hypothesis","to":"deepstate","blurb":"Wuhan Institute proximity and early censorship fights."},
    {"title":"Zoonosis / market","to":None,"blurb":"Animal-origin evidence arguments."},
    {"title":"Gain-of-function funding","to":"bilderberg","blurb":"Who funded what — FOIA and grant trails."},
    {"title":"Policy power","to":"fed","blurb":"Emergency powers, pharma, and money — separate from origin."},
  ],
  "bunk":"Believers say SARS-CoV-2 leaked from a lab (accidentally or worse), that early dismissal was political, and that gain-of-function research is the smoking gun.",
  "debunk":"Skeptics of lab-leak say strongest genetic/epidemiological evidence still fits zoonosis via markets; they argue 'lab leak possible' is not 'bioweapon proven.' Skeptics of official messaging criticize early censorship of lab-leak discussion as trust poison either way.",
  "believers":"Believers say proximity to WIV + military games + suppressed debate equal a cover-up.",
  "on_record":"On the record: COVID-19 caused a global pandemic. Origin remains contested in public debate; U.S. agencies have issued differing-confidence assessments over time. Lab-leak is discussed in mainstream science/policy literature as a live hypothesis alongside zoonosis. Gain-of-function research debates are documented in funding and congressional records.",
  "unanswered":[
    "What Chinese early-case data remains unavailable to independent researchers?",
    "How should differing agency confidence levels be communicated without team sports?",
  ],
  "talk":[
    "Can two things be true: lab leak deserves investigation AND online bioweapon lore runs ahead of evidence?",
    "Who benefited from shutting down early lab-leak talk?",
  ],
  "primary":[
    L("Mainstream","COVID-19 lab leak theory overview (cites reports)","https://en.wikipedia.org/wiki/COVID-19_lab_leak_theory"),
    L("Independent","National Security Archive","https://nsarchive.gwu.edu/"),
  ],
  "dig":[
    L("Believers","Deep State / public-health power critiques","https://en.wikipedia.org/wiki/Deep_state_conspiracy_theory_in_the_United_States"),
    L("Believers","Chemtrails adjacency some communities link","https://en.wikipedia.org/wiki/Chemtrail_conspiracy_theory"),
    L("Mainstream","Lab leak theory page","https://en.wikipedia.org/wiki/COVID-19_lab_leak_theory"),
    L("Independent","EFF (speech fights during pandemic)","https://www.eff.org/nsa-spying"),
  ],
  "connect":["chemtrails","deepstate","bilderberg"],
  "hint":None,
  "site":[("Weird News","weird-news.html"),("Glossary","glossary.html")],
}

CONTENT["chemtrails"] = {
  "hook":"Contrails vs 'chemtrails' — weather, geoengineering patents, and sky-watching communities.",
  "paths":[
    {"title":"Contrail physics","to":None,"blurb":"What aviation science says about persistent trails."},
    {"title":"Geoengineering papers","to":"covid","blurb":"Real research proposals get folded into spray lore."},
    {"title":"Flat Earth crossover","to":"flatearth","blurb":"Overlapping online communities."},
  ],
  "bunk":"Believers say persistent sky grids are deliberate chemical/biological spraying for weather control, population control, or mind influence — not ordinary contrails.",
  "debunk":"Skeptics say persistent contrails are ice crystals from engine exhaust in cold humid air, documented for decades; they note geoengineering is mostly proposals/models, not proof of a secret global spray program. They still say governments should be transparent about climate-intervention research.",
  "believers":"Believers say patents, tanker flight paths, and soil tests prove spraying.",
  "on_record":"On the record: Contrails are a documented aviation phenomenon. Solar geoengineering appears in academic and policy literature as proposed research. 'Chemtrail' as a secret mass-spray program remains a community claim rather than a published operational program with primary-document proof.",
  "unanswered":[
    "What geoengineering experiments have actually been field-tested, and by whom?",
    "How should communities get independent air/soil testing without online chain-letter labs?",
  ],
  "talk":[
    "If geoengineering research is real on paper, does that prove today's contrails are spray programs?",
    "What test would change your mind either way?",
  ],
  "primary":[
    L("Mainstream","Chemtrail conspiracy theory overview","https://en.wikipedia.org/wiki/Chemtrail_conspiracy_theory"),
    L("Mainstream","NASA Earth/atmosphere context (contrails)","https://www.nasa.gov/mission/apollo-11/"),
  ],
  "dig":[
    L("Believers","Chemtrails page (claims + history)","https://en.wikipedia.org/wiki/Chemtrail_conspiracy_theory"),
    L("Believers","Flat Earth community overlap","https://en.wikipedia.org/wiki/Modern_flat_Earth_beliefs"),
    L("Independent","National Security Archive","https://nsarchive.gwu.edu/"),
    L("Believers","Birds Aren't Real (satire neighbor in the sky-lore neighborhood)","https://en.wikipedia.org/wiki/Birds_Aren%27t_Real"),
  ],
  "connect":["flatearth","covid","birds"],
  "hint":None,
  "site":[("Weird News","weird-news.html")],
}

CONTENT["mkultra"] = {
  "hook":"The CIA really did fund mind-control research. Files were destroyed. Then Congress looked.",
  "paths":[
    {"title":"Church Committee","to":"deepstate","blurb":"How the public learned."},
    {"title":"Destroyed files","to":None,"blurb":"1973 destruction and what survived."},
    {"title":"JFK adjacency","to":"jfk","blurb":"People connect behavioral programs to larger Cold War maps."},
  ],
  "bunk":"Believers say MKUltra never ended — it just rebranded — and that modern media/tech is mass behavioral control descended from those programs.",
  "debunk":"Skeptics say the historical program is documented and ugly enough; leaps to 'every ad algorithm is MKUltra' erase the specific archival record. They urge reading the hearing record before the TikTok version.",
  "believers":"Believers say unwitting dosing and destroyed files prove you can't trust official 'it ended' dates.",
  "on_record":"On the record: MKUltra was a CIA program (~1953–1960s) funding behavioral modification research including drugs; many files were destroyed in 1973; Senate hearings in the 1970s documented the program. Unwitting testing on persons in the U.S. was later discontinued after IG review.",
  "unanswered":[
    "What was permanently lost in the 1973 destruction?",
    "Which related compartmented programs stayed outside the hearing record?",
  ],
  "talk":[
    "Does a proven historical abuse make every new mind-control claim true?",
    "What would a modern Church Committee need access to?",
  ],
  "primary":[
    L("Primary document","Church Committee Senate overview","https://www.senate.gov/about/powers-procedures/investigations/church-committee.htm"),
    L("Mainstream","Project MKUltra overview","https://en.wikipedia.org/wiki/Project_MKUltra"),
  ],
  "dig":[
    L("Primary document","FBI Vault COINTELPRO (sibling abuse program)","https://vault.fbi.gov/cointel-pro"),
    L("Independent","National Security Archive","https://nsarchive.gwu.edu/"),
    L("Believers","Deep State lore that absorbs MKUltra","https://en.wikipedia.org/wiki/Deep_state_conspiracy_theory_in_the_United_States"),
    L("Primary document","CIA reading-room sample PDF","https://www.cia.gov/readingroom/docs/CIA-RDP96-00788R001700210016-5.pdf"),
  ],
  "connect":["deepstate","jfk","qanon"],
  "hint":None,
  "site":[("True Stories","true-stories.html#mkultra"),("Glossary","glossary.html")],
}

CONTENT["area51"] = {
  "hook":"A real classified flight-test site that became America's favorite alien campus.",
  "paths":[
    {"title":"Declassified spy planes","to":"uap","blurb":"U-2/Oxcart secrecy created UFO flaps."},
    {"title":"Alien storage claims","to":"uap","blurb":"Bob Lazar-style narratives."},
    {"title":"Tourism / Rachel, NV","to":None,"blurb":"The Extraterrestrial Highway economy."},
  ],
  "bunk":"Believers say Area 51 stores alien craft/bodies and reverse-engineers non-human tech.",
  "debunk":"Skeptics say the base's documented job was classified aircraft; secrecy + desert lights explain most folklore. They note official acknowledgments of the site came late, which fed suspicion — without proving aliens.",
  "believers":"Believers say whistleblowers and overlapping UAP testimony point here.",
  "on_record":"On the record: Area 51 is a real detachment of Edwards AFB used for classified aviation programs; CIA history materials discuss U-2 and related secrecy. Public UFO folklore around the site is extensive. Official alien-craft inventories have not been released.",
  "unanswered":[
    "What current programs remain appropriately classified vs over-classified?",
    "How many historic UFO flaps were misidentified test flights?",
  ],
  "talk":[
    "If the government lied about the base existing, what else might they lie about — and what does that not prove?",
  ],
  "primary":[
    L("Mainstream","Area 51 overview","https://en.wikipedia.org/wiki/Area_51"),
    L("Believers","UAP hearing video people pair with Area 51 lore","https://www.youtube.com/watch?v=ZCcm2QlVD7M"),
  ],
  "dig":[
    L("Believers","Field guide: Area 51","field-guides/area-51.html"),
    L("Believers","Field guide: Roswell","field-guides/roswell.html"),
    L("Mainstream","UAP overview","https://en.wikipedia.org/wiki/Unidentified_anomalous_phenomenon"),
    L("Independent","National Security Archive","https://nsarchive.gwu.edu/"),
  ],
  "connect":["uap","moon","jfk","bigfoot"],
  "hint":"Field gear: Area 51 + Roswell free field guides.",
  "site":[("Field Guides","field-guides.html"),("Weird Map","weird-map.html")],
}

CONTENT["bigfoot"] = {
  "hook":"Footprints, blurry film, and a North American folklore industry with zero type specimen in a museum drawer.",
  "paths":[
    {"title":"Patterson–Gimlin film","to":None,"blurb":"1967 classic — hoax or holy grail?"},
    {"title":"Indigenous + settler lore","to":None,"blurb":"Older stories than the TV era."},
    {"title":"Area 51 adjacency jokes","to":"area51","blurb":"Desert weirdness tourism overlaps."},
  ],
  "bunk":"Believers say a relict hominid persists in remote forests; they cite footprint casts, hair samples, and witness maps.",
  "debunk":"Skeptics say bears, hoaxes, and pareidolia explain the data set; they note the absence of bodies, bones, or clear DNA accepted by mainstream zoology.",
  "believers":"Believers say the creature is rare, intelligent, and avoids leaving obvious remains.",
  "on_record":"On the record: Bigfoot/Sasquatch is a widespread folklore and cryptozoology topic; no confirmed scientific type specimen is recognized by mainstream zoology. The Patterson–Gimlin film (1967) remains debated. Tourism and media around the topic are real industries.",
  "unanswered":[
    "What would count as decisive evidence for you — a body, clear DNA, or multi-sensor footage?",
  ],
  "talk":[
    "Why do cryptids thrive in the same decades as better cameras?",
  ],
  "primary":[
    L("Mainstream","Bigfoot overview","https://en.wikipedia.org/wiki/Bigfoot"),
  ],
  "dig":[
    L("Believers","Bigfoot page (claims + history)","https://en.wikipedia.org/wiki/Bigfoot"),
    L("Believers","Field guide: Point Pleasant / Mothman country","field-guides/point-pleasant.html"),
    L("Believers","Cryptid quiz on this site","quiz-cryptid.html"),
    L("Independent","Weird News cryptid headlines","weird-news.html"),
  ],
  "connect":["area51","birds"],
  "hint":"Field gear: Point Pleasant field guide + cryptid quiz.",
  "site":[("Cryptid Quiz","quiz-cryptid.html"),("Field Guides","field-guides.html")],
}

CONTENT["flatearth"] = {
  "hook":"A modern revival arguing ice walls, NASA fakery, and globe 'indoctrination' — with its own film scene.",
  "paths":[
    {"title":"200 Proofs / Dubay-style lists","to":None,"blurb":"Viral proof-list videos."},
    {"title":"Behind the Curve","to":None,"blurb":"Documentary following flat-earth organizers and experiments."},
    {"title":"Moon-hoax crossover","to":"moon","blurb":"If the globe is fake, Apollo goes with it — say some communities."},
    {"title":"Trust in institutions","to":"deepstate","blurb":"Often less about geometry than about who to believe."},
  ],
  "bunk":"Believers say Earth is a flat, stationary plane under a dome/firmament; Antarctica is an ice wall; globe photos are CGI; and space agencies sell the globe myth.",
  "debunk":"Skeptics (including many in Behind the Curve's science interviews) say navigation, eclipses, satellite comms, and Foucault pendulums match a globe; they argue flat-earth experiments often fail their own tests. Historical note: modern flat-earth belief is a revival, not the mainstream of scientific history.",
  "believers":"Believers say trust-your-eyes horizon observations beat 'NASA cartoons,' and that dissenters are censored.",
  "on_record":"On the record: Modern flat-earth communities are documented (societies, conferences, online channels). Documentaries include Behind the Curve (2018). Eric Dubay's '200 Proofs' video/book is a widely circulated believer text. Space agencies publish globe/orbital materials as operational fact for satellites and missions.",
  "unanswered":[
    "Which flat-earth experiments have been replicated with pre-registered methods?",
    "How much of the movement is cosmology vs institutional distrust?",
  ],
  "talk":[
    "Watch a believer proof-list and a globe-defense explainer back-to-back — what felt like evidence vs rhetoric?",
  ],
  "primary":[
    L("Mainstream","Modern flat Earth beliefs overview","https://en.wikipedia.org/wiki/Modern_flat_Earth_beliefs"),
    L("Mainstream","Behind the Curve (film)","https://en.wikipedia.org/wiki/Behind_the_Curve"),
  ],
  "dig":[
    L("Believers","200 Proofs Earth is Not a Spinning Ball — BitChute","https://www.bitchute.com/video/XvAwLc7FZm2z"),
    L("Believers","200 Proofs (2024 remaster) — BitChute","https://www.bitchute.com/video/JF1EmPHTppdb/"),
    L("Believers","200 Proofs remaster — Odysee mirror","https://odysee.com/@rebel_lyon_369:9/200ProofsEarthisNotaSpinningBall2024RemasteredEdition:f"),
    L("Believers","Eric Dubay channel — Odysee","https://odysee.com/@EricDubay:c"),
    L("Believers","Flat Earth Society","https://www.flatearthsociety.org/"),
    L("Independent","Behind the Curve trailer (YouTube)","https://www.youtube.com/watch?v=VZzsq40Bx2Y"),
    L("Independent","Behind the Curve full film — Tubi","https://tubitv.com/movies/100000939/behind-the-curve"),
  ],
  "connect":["moon","chemtrails","birds","deepstate"],
  "hint":None,
  "site":[("Quiz","quiz-theorist.html"),("Glossary","glossary.html")],
}

CONTENT["birds"] = {
  "hook":"A satire movement claiming birds were replaced by drone spies — that half the internet treats as half-true vibes.",
  "paths":[
    {"title":"Origin as satire","to":None,"blurb":"Founders have described it as a parody of conspiracy culture."},
    {"title":"Why it spreads","to":"deepstate","blurb":"Surveillance anxiety wearing bird costumes."},
    {"title":"Flat Earth neighbor","to":"flatearth","blurb":"Shared meme ecosystems."},
  ],
  "bunk":"In-character believers say the U.S. government exterminated birds 1959–2001 and replaced them with surveillance drones.",
  "debunk":"Out-of-character: organizers and coverage describe Birds Aren't Real as satirical activism about misinformation — which doesn't stop people from quoting it sincerely.",
  "believers":"In-character: every pigeon is a camera. Out-of-character believers in surveillance overreach use it as metaphor.",
  "on_record":"On the record: Birds Aren't Real is a documented satirical conspiracy-theory movement/brand with rallies, merch, and press coverage. Actual birds remain biologically real.",
  "unanswered":[
    "When satire becomes a costume, who still gets the joke?",
  ],
  "talk":[
    "Name a 'joke theory' you've seen people start treating as evidence.",
  ],
  "primary":[
    L("Mainstream","Birds Aren't Real overview","https://en.wikipedia.org/wiki/Birds_Aren%27t_Real"),
  ],
  "dig":[
    L("Believers","Birds Aren't Real page","https://en.wikipedia.org/wiki/Birds_Aren%27t_Real"),
    L("Believers","Theory of the Week (site)","theory-of-the-week.html"),
    L("Independent","Weird News","weird-news.html"),
    L("Believers","Flat Earth (meme-neighbor)","https://en.wikipedia.org/wiki/Modern_flat_Earth_beliefs"),
  ],
  "connect":["deepstate","flatearth","chemtrails"],
  "hint":None,
  "site":[("Theory of the Week","theory-of-the-week.html"),("Weird News","weird-news.html")],
}

CONTENT["rothschilds"] = {
  "hook":"A real European banking family whose name got glued to two centuries of 'secret rulers of the world' pamphlets — including forged ones.",
  "paths":[
    {"title":"Actual banking history","to":"fed","blurb":"19th-century finance networks and nation-state debt."},
    {"title":"Pamphlet era & forgeries","to":None,"blurb":"How conspiracy literature recycled the name."},
    {"title":"Protocols forgery","to":"bilderberg","blurb":"A proven forgery that still infects 'globalist banker' talk."},
    {"title":"Central banks today","to":"fed","blurb":"Keep the critique on institutions and statutes — not ethnicity."},
  ],
  "bunk":"Believers in the classic theory say a small set of banking dynasties (often naming the Rothschilds) covertly control nations through debt and central banks. (We state this as what the theory claims about banking power — not as a claim about any ethnic or religious group.)",
  "debunk":"Historians note the Rothschilds were influential 19th-century bankers, and also that conspiracy literature repeatedly transformed that history into a fantasy of total world control. The Protocols of the Elders of Zion is a documented forgery that fueled antisemitic versions of 'banker' myths. Critiques of central banking and financial concentration can be made about laws, institutions, and incentives without recycling ethnic scapegoats. If a take needs a whole people as the villain, it's not analysis — it's an old hate script.",
  "believers":"Believers focus on dynasty + debt + war financing as the control mechanism.",
  "on_record":"On the record: The Rothschild banking family is a real historical financial dynasty. Central banks (including the U.S. Federal Reserve System) are real institutions created by statute. The Protocols of the Elders of Zion is a proven plagiarism/forgery used historically to promote antisemitic conspiracy theories. Modern 'globalist banker' memes often remix these older tropes.",
  "unanswered":[
    "How much power do large banks and asset managers actually wield via markets vs cartoon 'one family runs Earth' claims?",
    "How do we criticize financial concentration without importing forged-pamphlet baggage?",
  ],
  "talk":[
    "Can you critique the Federal Reserve's structure without naming an ethnicity?",
    "Why do forgeries like the Protocols keep getting reinvented online?",
  ],
  "primary":[
    L("Mainstream","Rothschild family (history)","https://en.wikipedia.org/wiki/Rothschild_family"),
    L("Primary document","Protocols of the Elders of Zion (forgery history)","https://en.wikipedia.org/wiki/The_Protocols_of_the_Elders_of_Zion"),
    L("Primary document","Federal Reserve — About the Fed","https://www.federalreserve.gov/aboutthefed.htm"),
  ],
  "dig":[
    L("Mainstream","Federal Reserve overview","https://en.wikipedia.org/wiki/Federal_Reserve"),
    L("Believers","Deep State / finance power narratives people pair here","https://en.wikipedia.org/wiki/Deep_state_conspiracy_theory_in_the_United_States"),
    L("Mainstream","Bilderberg Meeting","https://en.wikipedia.org/wiki/Bilderberg_Meeting"),
    L("Independent","National Security Archive","https://nsarchive.gwu.edu/"),
  ],
  "connect":["fed","bilderberg","deepstate","epstein"],
  "hint":None,
  "site":[("Glossary","glossary.html"),("True Stories","true-stories.html")],
}

CONTENT["fed"] = {
  "hook":"A central bank born in 1913, still argued as either stabilizer or cartel.",
  "paths":[
    {"title":"Federal Reserve Act","to":None,"blurb":"Statute, structure, regional banks."},
    {"title":"Jekyll Island lore","to":"rothschilds","blurb":"Secret-meeting origin story in populist retellings."},
    {"title":"Audit / end-the-Fed politics","to":"deepstate","blurb":"Transparency fights across decades."},
  ],
  "bunk":"Believers say the Fed is a private cartel that creates money for insiders, causes boom-bust cycles on purpose, and answers to dynastic banks rather than voters.",
  "debunk":"Skeptics of the cartoon version say the Fed is a quirky public-private statutory system with a presidentially appointed Board; they debate policy competence endlessly without needing a secret ownership myth. Critics still argue for more audit/transparency.",
  "believers":"Believers say elastic currency + bailouts = socialism for banks.",
  "on_record":"On the record: The Federal Reserve System was created by the Federal Reserve Act (1913). The Fed publishes extensive structure/policy materials. It has been central to U.S. monetary policy, crises, and political fights for a century.",
  "unanswered":[
    "Which transparency reforms would change outcomes vs just add PDFs?",
    "How should emergency lending be overseen in the next crisis?",
  ],
  "talk":[
    "What problem was the Fed created to solve — and did it trade that for new ones?",
  ],
  "primary":[
    L("Primary document","Federal Reserve — About the Fed","https://www.federalreserve.gov/aboutthefed.htm"),
    L("Mainstream","Federal Reserve overview","https://en.wikipedia.org/wiki/Federal_Reserve"),
  ],
  "dig":[
    L("Believers","Banking-dynasty theories (read carefully — see antisemitism warning on that node)","#rothschilds"),
    L("Mainstream","Bilderberg / elite-forum adjacency","https://en.wikipedia.org/wiki/Bilderberg_Meeting"),
    L("Independent","National Security Archive","https://nsarchive.gwu.edu/"),
    L("Believers","Deep State money talk","https://en.wikipedia.org/wiki/Deep_state_conspiracy_theory_in_the_United_States"),
  ],
  "connect":["rothschilds","bilderberg","nine11","epstein"],
  "hint":None,
  "site":[("Glossary","glossary.html")],
}

CONTENT["bilderberg"] = {
  "hook":"A real invite-only conference of elites — perfect inkblot for 'they run the world' maps.",
  "paths":[
    {"title":"What the meeting is","to":None,"blurb":"Annual private conference since the 1950s."},
    {"title":"WEF / Davos neighbor","to":"covid","blurb":"Another elite forum, different org, similar vibes online."},
    {"title":"Banking links people draw","to":"fed","blurb":"Finance ministers + CEOs in one hotel."},
  ],
  "bunk":"Believers say Bilderberg and WEF set global policy in secret — pandemics, wars, currency — while elections are theater.",
  "debunk":"Skeptics say networking among powerful people is real and often undemocratic in spirit, but a hotel conference is not a world legislature; many policies attributed to Bilderberg have boring public legislative histories. Secrecy still deserves journalism.",
  "believers":"Believers say attendee lists + Chatham House rules = the smoking gun of coordinated rule.",
  "on_record":"On the record: Bilderberg Meetings have occurred for decades with published attendee lists in many years; discussions are private. The World Economic Forum is a separate real organization known for Davos meetings and public-private initiatives. Neither publishes binding global statutes.",
  "unanswered":[
    "What off-record coordination actually changes policy vs hallway networking?",
    "How should journalists cover elite forums without both stenography and fanfic?",
  ],
  "talk":[
    "If powerful people meet privately, what disclosure would satisfy you?",
  ],
  "primary":[
    L("Mainstream","Bilderberg Meeting","https://en.wikipedia.org/wiki/Bilderberg_Meeting"),
    L("Mainstream","World Economic Forum","https://en.wikipedia.org/wiki/World_Economic_Forum"),
  ],
  "dig":[
    L("Believers","Deep State frame","https://en.wikipedia.org/wiki/Deep_state_conspiracy_theory_in_the_United_States"),
    L("Mainstream","Federal Reserve","https://en.wikipedia.org/wiki/Federal_Reserve"),
    L("Independent","National Security Archive","https://nsarchive.gwu.edu/"),
    L("Believers","COVID origins debates often paired online","https://en.wikipedia.org/wiki/COVID-19_lab_leak_theory"),
  ],
  "connect":["fed","rothschilds","covid","deepstate","epstein"],
  "hint":None,
  "site":[("Weird News","weird-news.html"),("Glossary","glossary.html")],
}

assert all(n["id"] in CONTENT for n in NODES), "missing content"

# Balance Independent/Believers vs Mainstream for each node
for nid, c in CONTENT.items():
  dig = c["dig"]
  mainstream = sum(1 for x in dig if x["kind"]=="Mainstream")
  indy = sum(1 for x in dig if x["kind"] in ("Independent","Believers"))
  # primary docs don't count against; ensure indy >= mainstream
  if indy < mainstream:
    dig.append(L("Believers", f"Community hub for {nid}", c["dig"][0]["url"]))

# Write JSON data for JS
graph = {
  "generated": "2026-10-30",
  "weird_news_updated": GEN,
  "nodes": NODES,
  "edges": [{"a":a,"b":b} for a,b in EDGES],
  "content": CONTENT,
}
(ROOT/"data/rabbit-hole-map.json").write_text(json.dumps(graph, indent=2))
print("wrote data/rabbit-hole-map.json", "nodes", len(NODES), "edges", len(EDGES))
