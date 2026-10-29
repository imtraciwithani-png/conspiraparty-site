#!/usr/bin/env python3
"""Build Suspicious Field Guides: HTML pages, PDFs, OG images, index, nav, sitemap."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = ImageDraw = ImageFont = None

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.colors import Color, black, white, HexColor

ROOT = Path(__file__).resolve().parents[1]
GUIDES_DIR = ROOT / "field-guides"
PDF_DIR = ROOT / "printables" / "field-guides"
OG_DIR = ROOT / "assets" / "og" / "field-guides"
FONT_PATH = ROOT / "assets" / "fonts" / "Anton-Regular.ttf"
LOGO_PATH = ROOT / "assets" / "img" / "logo.png"
SITE = "https://conspiraparty.com"
TODAY = "2026-10-29"

RED = HexColor("#e11d26")
BG = HexColor("#0b0b0b")
CREAM = HexColor("#f2efe8")
DIM = HexColor("#b8b2a6")

# ---------------------------------------------------------------------------
# Guide content (verified public landmarks; entertainment tone)
# ---------------------------------------------------------------------------
GUIDES = [
  {
    "slug": "area-51",
    "title": "Area 51 / Rachel, NV",
    "short": "Area 51",
    "tagline": "Stay outside the gates. Bring snacks. Trust nothing with blinking lights.",
    "intro": "Rachel, Nevada sits on State Route 375 — the Extraterrestrial Highway — a few dusty miles from the most famous base you will never tour. The highway is public. The gift shops are public. The gates are not. This guide is for the tourist trail only: stay on public roads, stay outside any fenced or posted area, and leave the storming to the memes.",
    "warning": "Do not trespass. Area 51 is a restricted military installation. Stay outside the gates and posted boundaries. Looking from public roads and businesses in Rachel is fine. Crossing fences is not.",
    "checklist": [
      "Extraterrestrial Highway (NV-375) road sign photo",
      "Giant alien statue selfie (Alien Research Center, Hiko)",
      "Alien Fresh Jerky pit stop on US-93",
      "Black Mailbox site (Mailbox Rd @ NV-375) — box comes and goes; the lore stays",
      "Alien Burger at the Little A'Le'Inn, Rachel",
      "Someone wearing a tin foil hat unironically",
      "A shirt that says \"Storm Area 51\" sold next to snacks",
      "Night sky so dark you invent three new constellations",
      "A stranger who \"definitely knows a guy who worked there\"",
      "Warning signs that look like they mean it",
      "A drone… or a plane… or a \"plane\"",
      "Gas gauge anxiety (fill up before you go)",
      "A gift-shop \"classified\" sticker on your water bottle",
      "Someone filming the horizon like it's a Netflix special",
      "You leave without getting detained (mission success)",
    ],
    "spots": [
      {"name": "Little A'Le'Inn", "note": "Rachel's alien-themed bar, grill and motel. Public, friendly, and the unofficial HQ for ET Highway tourists."},
      {"name": "Alien Research Center (Hiko)", "note": "Souvenir shop with a big alien statue out front. Research is optional. Photos are mandatory."},
      {"name": "E.T. Fresh Jerky (Hiko)", "note": "Alien murals, snacks and famously clean restrooms at the tip of the ET Highway."},
      {"name": "Black Mailbox site", "note": "Between mile markers 29–30 on NV-375 at Mailbox Road. The mailbox itself gets stolen a lot; the skywatching pull-off remains a classic stop. Stay off private ranch access."},
      {"name": "Extraterrestrial Highway scenic drive", "note": "Public state highway from near Hiko toward Warm Springs. Cattle, desert and vibes. Do not turn down unmarked restricted roads toward the base."},
    ],
    "notes": [
      "The \"Black Mailbox\" was never an Area 51 drop box — it belonged to a local rancher whose mail kept getting rifled by UFO tourists.",
      "Rachel's population is tiny. Support the Inn, tip well, and pack out your trash.",
      "Cell service is patchy. Download this page and the printable before you leave town.",
      "If someone offers you a \"secret tour past the fence,\" decline. Politely. Firmly. With snacks.",
    ],
  },
  {
    "slug": "grand-canyon",
    "title": "Grand Canyon",
    "short": "Grand Canyon",
    "tagline": "A mile-deep hole in the ground. Official story: geology. Unofficial story: discuss among yourselves.",
    "intro": "The Grand Canyon is a National Park with real trails, real rim views and a real gift shop that will sell you a refrigerator magnet. Bring water, stay behind railings and mark every suspiciously perfect sunset. Geology did this. Probably.",
    "warning": "Stay on marked trails and overlooks. Do not climb fences or wander onto unstable rim edges. Heat and dehydration are the real villains here.",
    "checklist": [
      "First rim view that makes your brain reboot",
      "Someone saying \"photos don't do it justice\" (they're right)",
      "A mule train looking extremely done with tourists",
      "California Condor sighting (or a very confident raven)",
      "Layer-cake rock strata you pretend to understand",
      "A ranger talk you half-listened to while staring into the abyss",
      "Sunrise or sunset that looks Photoshopped",
      "Gift-shop fossil that is definitely not from Mars",
      "A tourist posing dangerously close to the rim (don't be them)",
      "Helicopter overhead — scenic tour, not extraction",
      "Phantom Ranch name-drop from someone who hiked down",
      "You drank all your water and still want more",
      "A \"I hiked to the river\" flex (verify blurry selfie)",
      "Night sky so clear the canyon looks bottomless",
      "You left without inventing a hollow-Earth theory… or did you?",
    ],
    "spots": [
      {"name": "Mather Point (South Rim)", "note": "Classic first-look overlook near Grand Canyon Village. Crowded for a reason."},
      {"name": "Yavapai Geology Museum", "note": "Rim views plus exhibits explaining those rock layers. Bring your \"sure, Jan\" face."},
      {"name": "Desert View Watchtower", "note": "Mary Colter's 1932 tower on the East Rim Drive — views and architecture."},
      {"name": "Hermit's Rest", "note": "West end of Hermit Road; stone building, snacks and a less-packed vibe off-peak."},
      {"name": "Grand Canyon Visitor Center", "note": "Orientation, maps and the shuttle hub. Start here so you don't invent your own trail."},
    ],
    "notes": [
      "South Rim is open year-round; North Rim has a shorter season. Check NPS alerts before you go.",
      "The canyon is about a mile deep and up to 18 miles wide. Your phone battery will not survive both rims in one day.",
      "Leave rocks, fossils and artifacts where you found them. The park is not a loot crate.",
      "If your theory involves ancient astronaut landscaping, keep it in the group chat — and stay on the trail.",
    ],
  },
  {
    "slug": "most-suspicious-place",
    "title": "The Most Suspicious Place on Earth",
    "short": "Most Suspicious Place",
    "tagline": "Central Florida. Theme parks. Tunnel talk. Perfectly timed fireworks. Coincidence?",
    "intro": "Central Florida's mega resort area is engineered for wonder: tunnels under the pavement, a private \"utilidor\" culture of backstage logistics, and fireworks that somehow always nail the beat. This guide stays on the public guest side — no logos, no character meet-and-greets required. Just vibes, odd logistics and a checklist for the traveler who notices the seams.",
    "warning": "Stay in guest-accessible areas. Do not enter backstage, cast-only or restricted zones. Follow posted rules and ride height/safety signs.",
    "checklist": [
      "A cast member who appears from nowhere (utilidor energy)",
      "Trash can that somehow never overflows",
      "Fireworks timed to the second",
      "A tunnel or underpass that feels like a portal",
      "Someone in the group swearing the buildings are \"forced perspective\"",
      "A parade route cleared with military precision",
      "Hidden icon pattern in architecture (spot it; invent lore)",
      "A monorail or people-mover that feels like the future, 1971 edition",
      "Gift shop that smells like manufactured nostalgia",
      "A \"secret menu\" tip from a stranger who may be lying",
      "Lightning lane / queue tech that knows too much",
      "A perfectly clean bathroom at peak crowd hour",
      "Nighttime projection mapping on a building facade",
      "You lost track of time in the most suspicious way",
      "Exit past a giant merchandise gauntlet unscathed (wallet: not so much)",
    ],
    "spots": [
      {"name": "Theme park resort area (Orlando / Bay Lake, FL)", "note": "The public guest campuses and resorts. Stick to ticketed and openly accessible spaces."},
      {"name": "Transportation hubs & monorail loops", "note": "Watch the logistics. The choreography of moving millions of people is the real magic trick."},
      {"name": "Disney Springs shopping district (public)", "note": "Public shopping/dining district near the resorts — good for people-watching and \"is this a set?\" moments. Factual place name only; no park logos."},
      {"name": "Lake Buena Vista / resort corridors", "note": "Hotel strips and boulevards where the theming never quite turns off."},
      {"name": "Public overlooks of nighttime spectaculars", "note": "Watch fireworks and projections from guest-allowed viewing areas. No climbing. No drones where banned."},
    ],
    "notes": [
      "Utilidors (underground / backstage corridors) are a real operational feature of parts of the resort — guests don't get a free tour. That's the point of the mystery.",
      "Florida heat is not a conspiracy. Hydrate. Sunscreen. Sit down.",
      "We don't use park logos or character IP here. Your photos of public spaces are your own; our copy stays trademark-safe.",
      "If your kids ask whether the tunnels go to another dimension, say \"maybe\" and buy them a churro.",
    ],
  },
  {
    "slug": "roswell",
    "title": "Roswell, NM",
    "short": "Roswell",
    "tagline": "1947 debris. 2026 gift shops. Same town. Different clearance levels.",
    "intro": "Roswell turned a 1947 ranch-country debris story into a full municipal aesthetic: alien streetlamps, UFO museums and a Main Street that leans all the way in. The alleged crash site is actually closer to Corona, about 75 miles north on BLM land — hike only, no vehicles. Downtown is where the souvenir industrial complex thrives.",
    "warning": "Crash-site access is a hike on BLM land near Corona — no vehicles past the trailhead parking. Respect private property. Downtown attractions are the easy mode.",
    "checklist": [
      "International UFO Museum admission stamp (mental or real)",
      "Main Street alien murals / streetlamps",
      "Photo with a downtown alien statue",
      "Alien Zone photo-op nonsense",
      "UFO McDonald's flyby (yes, it's a thing)",
      "Someone insisting it was a weather balloon with confidence",
      "Someone insisting it was not, with equal confidence",
      "Festival poster leftover from UFO Festival season",
      "Research Center archive rabbit hole (lose 45 minutes)",
      "A shirt that says \"I want to believe\" in three fonts",
      "Planetarium show that is actually about real stars",
      "Visitor Center free alien photo op",
      "You said \"Roswell\" and a local didn't even flinch",
      "Road trip snack that looks radioactive (it's just Takis)",
      "You leave still undecided — correct clearance level",
    ],
    "spots": [
      {"name": "International UFO Museum and Research Center", "note": "114 N Main St. The mothership of downtown lore — exhibits, archives and gift shop. Open daily."},
      {"name": "Roswell Visitor Center", "note": "426 N Main St. Maps, tips and a free souvenir photo with the Visitor Center aliens."},
      {"name": "Alien Zone: Area 51", "note": "216 N Main St. Cheesy photo sets. Lean in."},
      {"name": "UFO Spacewalk / Spaceport Roswell area", "note": "E 2nd St blacklight and VR-ish experiences for when walking Main Street isn't weird enough."},
      {"name": "Alleged UFO Skip Site (near Corona)", "note": "BLM parking off Lincoln County Rd B007 / Transwestern Road; ~1 mile hike. No vehicles on the trail. Far from downtown — plan fuel and water."},
    ],
    "notes": [
      "The 1947 incident was handled through Roswell Army Air Field; the debris field most people mean is nearer Corona than the city limits.",
      "Air Force reports later framed Project Mogul / balloon explanations. The town framed tourism. Both can be true in different ways.",
      "Bottomless Lakes State Park and Bitter Lakes NWR are excellent non-alien side quests nearby.",
      "Buy local. The alien economy funds real humans.",
    ],
  },
  {
    "slug": "denver-airport",
    "title": "Denver International Airport",
    "short": "Denver Airport",
    "tagline": "Blue horse. Gargoyles. Tunnels. The airport that memed itself into legend.",
    "intro": "DEN leans into the bit. A 32-foot blue Mustang with glowing red eyes (officially \"Mustang,\" nicknamed Blucifer) greets Peña Boulevard. Bronze \"Notre Denver\" gargoyles watch baggage claim. Real tunnels move trains, bags and deicing fluid — not lizard cabinets, according to the airport. Bring a long layover and a sense of humor.",
    "warning": "Stay in public terminal areas. Do not enter secure / employee-only zones. Photography rules vary by area — obey signage and TSA instructions.",
    "checklist": [
      "Blucifer (Mustang) red-eye photo from Peña Blvd / public view",
      "Notre Denver gargoyle spotted in baggage claim",
      "Leo Tanguma murals that look… intense",
      "Someone whispering \"Illuminati runway layout\"",
      "Underground train to the concourse (mundane magic)",
      "A talking / animatronic gargoyle bit if it's running",
      "Gift shop selling conspiracy merch about… this airport",
      "Time capsule energy (DEN has one; lore varies)",
      "Mountain views that make the landing worth it",
      "A stranger explaining the New World Airport Commission plaque",
      "You almost missed your connection chasing a mural",
      "Blue horse plush or sticker acquired",
      "Construction tunnels joked about on the airport's own socials",
      "Elitch Gardens memories from the old airport site (deep cut)",
      "You boarded without joining a secret society (or did you?)",
    ],
    "spots": [
      {"name": "Mustang (\"Blucifer\")", "note": "Luis Jiménez sculpture on Peña Boulevard. Red eyes honor neon-sign craft; the artist died in a 2006 studio accident while the piece was unfinished — his children completed it for the 2008 unveil."},
      {"name": "Notre Denver gargoyles", "note": "Cast-bronze pair in east and west baggage claim — public art meant to \"protect\" luggage, named with a nod to Notre-Dame."},
      {"name": "Jeppesen Terminal public art", "note": "Murals, installations and the general \"why does this airport feel like a thesis?\" vibe."},
      {"name": "Passenger train / tunnel ride", "note": "The underground train between terminal and concourses — real, useful and fuel for tunnel theories."},
      {"name": "Airport overlooks & Peña Boulevard approach", "note": "Best Blucifer views are from the public roadway approach, not from a sprint through security."},
    ],
    "notes": [
      "DEN has publicly joked about its own conspiracy reputation, including tunnel projects that are boringly about stormwater and deicing.",
      "The \"secret bunker\" stories usually collide with the much duller truth of baggage systems and utilities.",
      "If your layover is short, pick one: horse, gargoyle or mural. You can't collect them all between C and B.",
      "Entertainment only. The airport is weird. Weird is allowed.",
    ],
  },
  {
    "slug": "mount-rushmore",
    "title": "Mount Rushmore",
    "short": "Mount Rushmore",
    "tagline": "Four faces. One mountain. Infinite \"what's behind the heads\" jokes.",
    "intro": "Mount Rushmore National Memorial carves four U.S. presidents into the Black Hills of South Dakota. The visitor center, Avenue of Flags and evening lighting ceremony are the public show. Hall of Records lore (a real unfinished repository behind the sculpture) keeps the corkboard busy. Stay on park paths; the mountain is not a climbing gym.",
    "warning": "Stay behind railings and on designated walkways. Do not attempt to climb the sculpture or enter closed areas. Weather and lightning shut viewpoints — listen to rangers.",
    "checklist": [
      "Classic Grand View Terrace photo",
      "Avenue of Flags state-flag gauntlet",
      "Someone asking where the fifth face is",
      "Hall of Records mention from a ranger or plaque",
      "Sculptor's Studio stop",
      "Evening lighting ceremony (seasonal)",
      "A kid insisting the presidents can see them",
      "Gift-shop miniature heads",
      "Black Hills drive that feels like a movie establishing shot",
      "You learned Gutzon Borglum's name and immediately forgot it",
      "Crowds synchronized raising phones at golden hour",
      "A \"secret chamber\" theory whispered near the amphitheater",
      "Bison or mountain goat sighting nearby (bonus wildlife)",
      "You resisted the urge to yell echo jokes",
      "Left still unsure what's in the unfinished hall",
    ],
    "spots": [
      {"name": "Grand View Terrace", "note": "Main public viewpoint facing the sculpture. Arrive early for fewer elbows."},
      {"name": "Avenue of Flags", "note": "Walk the state and territory flags on the way to the terrace."},
      {"name": "Lincoln Borglum Visitor Center", "note": "Exhibits, film and context — including the imperfect, unfinished history of the carving."},
      {"name": "Sculptor's Studio", "note": "Tools, models and process geekery for the \"how did they even\" crowd."},
      {"name": "Presidential Trail (when open)", "note": "Closer viewpoints via a walking trail — check seasonal closures and mobility notes."},
    ],
    "notes": [
      "A Hall of Records was begun behind the sculpture as a repository for documents; it was never finished as originally dreamed. That's public NPS history, not a leaked bunker map.",
      "The memorial sits in the Black Hills, sacred to the Lakota and other nations — visit with respect.",
      "Nearby: Crazy Horse Memorial (separate site, privately run) if you're continuing the mountain-carving tour.",
      "No climbing. No drones where prohibited. Your conspiracy can survive a railing.",
    ],
  },
  {
    "slug": "stonehenge",
    "title": "Stonehenge",
    "short": "Stonehenge",
    "tagline": "Neolithic GPS. Tour buses. Still unexplained enough for a party.",
    "intro": "Stonehenge on Salisbury Plain, Wiltshire, is a UNESCO World Heritage site managed with a visitor centre, shuttle and a path around the stone circle. Most visitors don't walk among the stones (special access is limited). Ancient astronomy, engineering flex, or prehistoric party venue — your field notes, your call.",
    "warning": "Stay on visitor paths. Do not touch or climb the stones. Special inner-circle access is ticketed and timed when offered — never hop barriers.",
    "checklist": [
      "First view of the circle from the visitor path",
      "Someone saying \"aliens\" within 60 seconds",
      "Someone saying \"just a calendar\" within 60 seconds",
      "Audio guide fact that sounds made up (it isn't)",
      "Sheep in the distance judging your theories",
      "Solstice lore drop (even if it's October)",
      "Visitor Centre prehistoric houses reconstruction",
      "Shuttle bus that feels like a soft abduction",
      "Photo where the stones look bigger than your life problems",
      "A kid asking who moved the bluestones (good question)",
      "Wind that rearranges your hair into a ritual style",
      "Gift-shop miniature trilithon",
      "Comparison debate: Stonehenge vs. every roadside replica back home",
      "You resisted climbing (heroic)",
      "Left still not sure about the lintels",
    ],
    "spots": [
      {"name": "Stonehenge stone circle (path circuit)", "note": "The classic loop around the monument. Ropes exist for a reason."},
      {"name": "Stonehenge Visitor Centre", "note": "Exhibits, café and the standing-up prehistoric houses — start or end here."},
      {"name": "Exhibition & stone displays", "note": "Context on construction theories, burials and the wider ritual landscape."},
      {"name": "Wiltshire landscape / Avenue views", "note": "Look outward — the site sits in a bigger ceremonial landscape, not a void."},
      {"name": "Salisbury side quest", "note": "Cathedral town nearby for when you need indoor plumbing and cream tea."},
    ],
    "notes": [
      "Bluestones and sarsens were hauled ridiculous distances by Neolithic people with Neolithic tech. That's already weird enough.",
      "English Heritage manages access; inner-circle visits are limited — book officially if that's your mission.",
      "Replicas exist worldwide (including U.S. roadside versions). Collect them like Pokémon if you must.",
      "No drones over the monument. No chisels. No \"just one touch.\"",
    ],
  },
  {
    "slug": "bermuda-triangle",
    "title": "Bermuda Triangle (Miami / Key West jump-off)",
    "short": "Bermuda Triangle",
    "tagline": "Start in South Florida. Point your boat at myth. Return with sunscreen.",
    "intro": "The Bermuda Triangle is a pop-culture wedge of Atlantic roughly between Miami, Bermuda and Puerto Rico. You cannot buy a ticket to the Triangle itself — you launch from real ports. Miami and Key West are the classic U.S. jump-offs: piers, reefs, sunset sails and a century of disappearances that look less spooky once you add \"weather\" and \"old navigation\" to the spreadsheet. Still fun to mark the vibes.",
    "warning": "Ocean travel is serious. Use licensed operators, check weather, wear life jackets and file float plans. This guide is entertainment, not a passage plan.",
    "checklist": [
      "Miami skyline from Biscayne Bay",
      "A boat captain who has a Triangle story ready",
      "Compass joke from someone who owns a phone GPS",
      "Key West southernmost point photo chaos",
      "Sunset that looks like a portal (it's just latitude)",
      "Reef snorkel where the only aliens are parrotfish",
      "A bar that sells \"survived the Triangle\" merch",
      "Flight over water where you briefly do the math",
      "Mention of Flight 19 (1945) from a true-crime podcast brain",
      "Perfectly normal cargo ship doing perfectly normal ship things",
      "Tropical storm app refresh (responsible paranoia)",
      "Key lime something consumed for courage",
      "A seagull that knows too much",
      "You explained magnetic variation incorrectly but with confidence",
      "Dry land afterward — always the goal",
    ],
    "spots": [
      {"name": "Miami / Biscayne Bay waterfront", "note": "Public baywalks, piers and licensed boat tours — your mainland staging area."},
      {"name": "Key West Mallory Square & harbor", "note": "Sunset celebration energy; ferries and charters for legitimate on-water time."},
      {"name": "Southernmost Point Buoy (Key West)", "note": "Photo op chaos. Early morning = fewer elbows."},
      {"name": "Dry Tortugas day trip (ferry / seaplane)", "note": "Fort Jefferson out in the Gulf — remote enough to feel Triangle-adjacent without the myth tax."},
      {"name": "Nova Southeastern / maritime museums (Miami area)", "note": "When you want charts and history instead of vibes."},
    ],
    "notes": [
      "Lloyd's and insurers have long argued the region's loss rates aren't uniquely supernatural once traffic volume is counted — boring, but peer-reviewable.",
      "Gulf Stream currents and sudden weather explain more than portals. Portals are more Instagrammable.",
      "If you charter, pick Coast Guard–licensed operators. Ghost stories don't inflate life jackets.",
      "Puerto Rico and Bermuda are the other corners — this U.S. jump-off guide keeps the packing list shorter.",
    ],
  },
  {
    "slug": "las-vegas",
    "title": "Las Vegas Strip",
    "short": "Las Vegas Strip",
    "tagline": "A neon desert mirage that somehow has a power bill. Suspicious prosperity.",
    "intro": "The Las Vegas Strip (Las Vegas Boulevard South in Clark County) is a public road wrapped in private spectacle: volcanoes, fountains, observation wheels and casinos that never sleep. Conspiracy optional. Sensory overload included. Stay hydrated; the desert is undefeated.",
    "warning": "Traffic is real — use crosswalks. Gambling: set limits. Heat kills vibes and hikers alike. Stay out of restricted back-of-house areas.",
    "checklist": [
      "Welcome to Fabulous Las Vegas sign photo",
      "Fountains doing synchronized watery jazz",
      "A volcano, pirate ship, or other street-side spectacle",
      "Someone who \"has a system\" at the slots",
      "3 a.m. pizza that tastes like victory",
      "Observation deck / High Roller type view of the grid",
      "A wedding chapel that takes walk-ins seriously",
      "LED billboard that knows your browser history (feels like it)",
      "Desert sunrise after a questionable decision set",
      "Street performer who might be a distraction (tip them)",
      "Casino carpet pattern that hides secrets (and stains)",
      "A free drink that was not free in the final accounting",
      "Replica monument that made you say \"wait, is that…\"",
      "You explained the Strip isn't technically in the City of Las Vegas",
      "Left with more stories than chips",
    ],
    "spots": [
      {"name": "Welcome to Fabulous Las Vegas sign", "note": "Public photo plaza at the south end of the Strip. Go early."},
      {"name": "Bellagio Fountains (public sidewalk view)", "note": "Free water show from the boulevard — classic Strip liturgy."},
      {"name": "Linq Promenade / High Roller area", "note": "Pedestrian zone and observation wheel views when you need altitude."},
      {"name": "Fremont Street (downtown, side quest)", "note": "Not the Strip, but the older neon laboratory — LED canopy and buskers."},
      {"name": "Red Rock Canyon (day trip)", "note": "Actual geology 30 minutes west when the carpet patterns start whispering."},
    ],
    "notes": [
      "Most of the Strip is in unincorporated Paradise and Winchester, not the City of Las Vegas. Fun fact for pedants.",
      "\"What happens here\" still ends up on someone's camera roll. Act accordingly.",
      "Area 51 is a long day trip from Vegas — don't combine both without a sleep plan.",
      "Free spectacles exist; you do not need a table minimum to enjoy the boulevard.",
    ],
  },
  {
    "slug": "point-pleasant",
    "title": "Point Pleasant, WV (Mothman)",
    "short": "Point Pleasant",
    "tagline": "Red eyes. Silver Bridge memory. World's only Mothman Museum. Bring binoculars.",
    "intro": "In November 1966, witnesses near the WWII TNT area north of Point Pleasant described a winged, red-eyed figure. Sightings piled up; the Silver Bridge collapse in December 1967 sealed the town into American weird-history. Today: a museum, a 12-foot statue, floodwall murals and public trails through the old ordnance works. Pay respects at the bridge memorial — that part isn't a bit.",
    "warning": "TNT Area / McClintic WMA: stay on legal trails, heed hunting-season rules and don't enter unstable structures. Downtown is strollable and statue-friendly.",
    "checklist": [
      "Mothman Museum visit (400 Main St)",
      "12-foot Mothman statue selfie",
      "Silver Bridge Memorial moment of quiet",
      "Floodwall murals along Riverfront Park",
      "TNT Area / McClintic WMA bunker \"igloos\" from a safe trail",
      "Someone doing the red-eye flashlight joke",
      "Mothman Wings mural photo (behind the Lowe Hotel)",
      "Tu-Endie-Wei State Park river confluence view",
      "A local who is kind about the tourists (tip well)",
      "Festival poster leftover energy (Sept Mothman Festival)",
      "Ohio River towboat sliding past like nothing's weird",
      "Cryptid plush acquired",
      "You read a plaque and got chills that weren't the wind",
      "Night drive where every light is \"probably a tower\"",
      "Left saying \"bird\" and \"not a bird\" in the same sentence",
    ],
    "spots": [
      {"name": "Mothman Museum", "note": "400 Main St. Archives, film props, souvenirs. World's only — they checked."},
      {"name": "Mothman Statue (Gunn Park / Main St)", "note": "12-ft stainless steel by Bob Roach. The required selfie."},
      {"name": "Silver Bridge Memorial", "note": "Riverfront remembrance of the 46 lives lost Dec 15, 1967. Be decent."},
      {"name": "McClintic Wildlife Management Area (TNT Area)", "note": "~5 miles north. Hiking among WWII ordnance-works remnants; first sighting lore lives here. Public WMA rules apply."},
      {"name": "Riverfront Park & floodwall murals", "note": "Ohio River views, history murals and easy downtown walking."},
    ],
    "notes": [
      "John Keel's book and the later film amplified the legend; the museum collects the folklore layer on top of real tragedy and real sightings reports.",
      "Mothman Festival hits downtown each September — book rooms early if that's your infiltration window.",
      "Tu-Endie-Wei State Park marks the Battle of Point Pleasant (1774) — history stacked on history.",
      "Cryptid tourism funds small-town Main Street. Buy coffee. Don't litter the TNT trails.",
    ],
  },
]


NAV_SNIPPET = '<li><a href="field-guides.html">Field Guides</a></li>'


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def share_box(slug: str, title: str, tagline: str) -> str:
    url = f"{SITE}/field-guides/{slug}.html"
    text = f"{title} — Suspicious Field Guide. {tagline} via conspiraparty.com"
    q = quote(url, safe="")
    qt = quote(text, safe="")
    return f'''<div class="share-box" data-share-url="{esc(url)}" data-share-text="{esc(text)}">
  <button type="button" class="btn sm share-native" data-share>Share this guide</button>
  <div class="share-links" hidden>
    <a class="btn sm" href="https://twitter.com/intent/tweet?url={q}&text={qt}" target="_blank" rel="noopener noreferrer">X</a>
    <a class="btn sm" href="https://www.facebook.com/sharer/sharer.php?u={q}" target="_blank" rel="noopener noreferrer">Facebook</a>
    <button type="button" class="btn sm share-copy" data-copy>Copy link</button>
  </div>
</div>'''


def page_chrome_head(title: str, desc: str, canonical: str, og_image: str) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:site_name" content="Conspiraparty">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:type" content="article">
<meta property="og:image" content="{esc(og_image)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(og_image)}">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="../assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
<link rel="preload" href="../assets/fonts/Anton-Regular.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="../assets/style.css">
<link rel="stylesheet" href="../assets/field-guides.css">
</head>
'''


HEADER = '''<body>
<a class="skip" href="#main">Skip to content</a>
<div class="promo">20% off the full printable kit with code <a href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored">LEAKED20</a></div>
<header class="top"><div class="bar"><a class="logo" href="../index.html"><img src="../assets/img/logo.png" alt="Conspiraparty.com – Top Secret Party Kit" width="220" height="70"></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button></div>
<nav class="main" id="nav" aria-label="Main"><ul>
<li><a href="../index.html#kit">Party Kit</a></li>
<li><a href="../free-printables.html">Free</a></li>
<li><a href="../memes.html">Memes</a></li>
<li><a href="../weird-news.html">Weird News</a></li>
<li><a href="../field-guides.html" aria-current="page">Field Guides</a></li>
<li><a href="../shirts.html">Shirts</a></li>
<li><a href="../quiz.html">Quiz</a></li>
<li><a href="../gift-guide.html">Gifts</a></li>
</ul></nav></header>
'''

FOOTER = '''<section class="redbg"><div class="wrap signup"><span class="stamp" style="color:#fff;border-color:#fff">Classified</span>
<h2>Join the Shadow Party Committee</h2>
<p>Free printables and party ideas. No spam, ever.</p>
<form class="signup-form" data-signup data-connected="true" action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="a2adf9e4-98f3-48cf-ab94-208e1705280b">
<input type="hidden" name="subject" value="New Shadow Party Committee recruit">
<input type="hidden" name="from_name" value="Conspiraparty">
<input type="hidden" name="redirect" value="https://conspiraparty.com/thanks.html">
<input type="checkbox" name="botcheck" class="skip" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
<input type="hidden" name="source_page" value="">
<label class="skip" for="emfg">Email</label>
<input id="emfg" type="email" name="email" placeholder="your.cover@email.com" required autocomplete="email">
<button class="btn alt" type="submit">Join</button>
<span class="notice" role="status" aria-live="polite"></span>
</form>
<p class="x-follow-inline"><a class="btn sm x-follow-btn" href="https://x.com/conspiraparty" target="_blank" rel="noopener">Follow @conspiraparty on X</a></p>
</div></section>
</main>
<footer><div class="wrap"><nav aria-label="Footer"><ul>
<li><a href="../index.html">Home</a></li>
<li><a href="../field-guides.html">Field Guides</a></li>
<li><a href="../free-printables.html">Free Printables</a></li>
<li><a href="../weird-news.html">Weird News</a></li>
<li><a href="../privacy.html">Privacy</a></li>
</ul></nav>
<p class="disclosure">As an Amazon Associate, Conspiraparty earns from qualifying purchases.</p>
<p class="x-follow"><a href="https://x.com/conspiraparty" target="_blank" rel="noopener">Follow @conspiraparty on X</a></p>
<p>All conspiracies on this site are for entertainment. Question everything, especially us. © 2026 Conspiraparty.com</p>
</div></footer>
<a class="sticky-cta" href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored">Get the Party Kit – 20% off</a>
<script src="../assets/site.js" defer></script>
<script src="../assets/field-guides.js" defer></script>
</body></html>
'''


SHARE_JS_NOTE = "field-guides.js handles checklist localStorage + share"


def render_guide_html(g: dict) -> str:
    slug = g["slug"]
    title = g["title"]
    desc = f"Suspicious Field Guide to {title}: weird checklist, public landmarks and agent notes. Free printable. Entertainment only."
    canonical = f"{SITE}/field-guides/{slug}.html"
    og = f"{SITE}/assets/og/field-guides/{slug}.jpg"
    checks = "\n".join(
        f'<label class="fg-check"><input type="checkbox" data-fg-check value="{i}"> <span>{esc(item)}</span></label>'
        for i, item in enumerate(g["checklist"])
    )
    spots = "\n".join(
        f'<article class="fg-spot"><h3>{esc(s["name"])}</h3><p>{esc(s["note"])}</p></article>'
        for s in g["spots"]
    )
    notes = "\n".join(f"<li>{esc(n)}</li>" for n in g["notes"])
    warn = ""
    if g.get("warning"):
        warn = f'<p class="fg-warn"><strong>Field rule:</strong> {esc(g["warning"])}</p>'
    return f'''{page_chrome_head(f"{title} Suspicious Field Guide | Conspiraparty", desc, canonical, og)}
{HEADER}
<main id="main" class="fg-page" data-fg-slug="{esc(slug)}">
<section class="hero"><div class="wrap">
<p class="eyebrow" style="margin:0 0 14px;font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;color:var(--text-dim)">Suspicious Field Guide</p>
<h1>{esc(title).upper() if title != "The Most Suspicious Place on Earth" else "THE MOST SUSPICIOUS PLACE ON EARTH"}</h1>
<p class="sub">{esc(g["tagline"])}</p>
{warn}
<div class="hero-actions" style="margin-top:18px">
<a class="btn" href="../printables/field-guides/{esc(slug)}.pdf" download>Download printable</a>
{share_box(slug, title, g["tagline"])}
</div>
</div></section>
<section class="paper"><div class="wrap">
<p class="lead">{esc(g["intro"])}</p>
</div></section>
<section class="cork"><div class="wrap">
<h2>Things That Are <span class="r">Weird</span></h2>
<p class="fg-hint">Tap to check off as you go. Saved on this phone.</p>
<div class="fg-checklist" id="fg-checklist">{checks}</div>
<p class="fg-progress"><span data-fg-count>0</span> / {len(g["checklist"])} logged · <button type="button" class="btn sm" data-fg-reset>Reset</button></p>
</div></section>
<section class="black"><div class="wrap">
<h2>Suspicious <span class="r">Spots</span></h2>
<p class="lead" style="color:var(--text-dim)">Public landmarks only. Stay where guests are welcome.</p>
<div class="fg-spots">{spots}</div>
</div></section>
<section class="paper"><div class="wrap">
<h2>Agent <span class="r">Notes</span></h2>
<ul class="fg-notes">{notes}</ul>
<p style="margin-top:22px"><a href="../field-guides.html">← All Field Guides</a> · <a href="../printables/field-guides/{esc(slug)}.pdf" download>Printable PDF</a></p>
</div></section>
{FOOTER}
'''


def render_index() -> str:
    cards = []
    for g in GUIDES:
        cards.append(
            f'''<a class="card fg-card" href="field-guides/{esc(g["slug"])}.html" style="text-decoration:none">
<img src="assets/og/field-guides/{esc(g["slug"])}.jpg" alt="{esc(g["title"])} field guide" width="600" height="315" loading="lazy">
<h3>{esc(g["title"])}</h3>
<p class="why">{esc(g["tagline"])}</p>
<span class="btn sm">Open guide</span>
</a>'''
        )
    head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Suspicious Field Guides | Conspiraparty</title>
<meta name="description" content="Free Suspicious Field Guides: weird checklists for Area 51, Roswell, Denver Airport, Mothman country and more. Phone-friendly + printable.">
<link rel="canonical" href="{SITE}/field-guides.html">
<meta property="og:site_name" content="Conspiraparty">
<meta property="og:title" content="Suspicious Field Guides | Conspiraparty">
<meta property="og:description" content="Weird checklists for suspicious places. Phone-friendly + printable PDFs.">
<meta property="og:url" content="{SITE}/field-guides.html">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/assets/og/field-guides/index.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Suspicious Field Guides | Conspiraparty">
<meta name="twitter:description" content="Weird checklists for suspicious places. Phone-friendly + printable PDFs.">
<meta name="twitter:image" content="{SITE}/assets/og/field-guides/index.jpg">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/Anton-Regular.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/field-guides.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="promo">20% off the full printable kit with code <a href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored">LEAKED20</a></div>
<header class="top"><div class="bar"><a class="logo" href="index.html"><img src="assets/img/logo.png" alt="Conspiraparty.com – Top Secret Party Kit" width="220" height="70"></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button></div>
<nav class="main" id="nav" aria-label="Main"><ul>
<li><a href="index.html#kit">Party Kit</a></li>
<li><a href="free-printables.html">Free</a></li>
<li><a href="memes.html">Memes</a></li>
<li><a href="weird-news.html">Weird News</a></li>
<li><a href="field-guides.html" aria-current="page">Field Guides</a></li>
<li><a href="shirts.html">Shirts</a></li>
<li><a href="quiz.html">Quiz</a></li>
<li><a href="gift-guide.html">Gifts</a></li>
</ul></nav></header>
<main id="main">
<section class="hero"><div class="wrap">
<p class="eyebrow" style="margin:0 0 14px;font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;color:var(--text-dim)">Travel weird on purpose</p>
<h1>SUSPICIOUS <span class="r">FIELD GUIDES</span></h1>
<p class="sub">Phone checklists for places that feel like a cover story. Mark weird things as you go. Print the PDF for the glove box.</p>
</div></section>
<section class="cork"><div class="wrap">
<div class="grid fg-grid">{"".join(cards)}</div>
<p class="center" style="margin-top:28px;color:var(--text-dim)">Entertainment only. Stay on public land. Question everything, especially us.</p>
</div></section>
<section class="redbg"><div class="wrap signup"><span class="stamp" style="color:#fff;border-color:#fff">Classified</span>
<h2>Join the Shadow Party Committee</h2>
<p>Free printables and party ideas. No spam, ever.</p>
<form class="signup-form" data-signup data-connected="true" action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="a2adf9e4-98f3-48cf-ab94-208e1705280b">
<input type="hidden" name="subject" value="New Shadow Party Committee recruit">
<input type="hidden" name="from_name" value="Conspiraparty">
<input type="hidden" name="redirect" value="https://conspiraparty.com/thanks.html">
<input type="checkbox" name="botcheck" class="skip" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
<input type="hidden" name="source_page" value="">
<label class="skip" for="emidx">Email</label>
<input id="emidx" type="email" name="email" placeholder="your.cover@email.com" required autocomplete="email">
<button class="btn alt" type="submit">Join</button>
<span class="notice" role="status" aria-live="polite"></span>
</form>
<p class="x-follow-inline"><a class="btn sm x-follow-btn" href="https://x.com/conspiraparty" target="_blank" rel="noopener">Follow @conspiraparty on X</a></p>
</div></section>
</main>
<footer><div class="wrap"><nav aria-label="Footer"><ul>
<li><a href="index.html">Home</a></li>
<li><a href="field-guides.html">Field Guides</a></li>
<li><a href="free-printables.html">Free Printables</a></li>
<li><a href="weird-news.html">Weird News</a></li>
<li><a href="privacy.html">Privacy</a></li>
</ul></nav>
<p class="x-follow"><a href="https://x.com/conspiraparty" target="_blank" rel="noopener">Follow @conspiraparty on X</a></p>
<p>All conspiracies on this site are for entertainment. © 2026 Conspiraparty.com</p>
</div></footer>
<a class="sticky-cta" href="https://happyplaceinkandart.etsy.com/listing/4502272966" target="_blank" rel="noopener sponsored">Get the Party Kit – 20% off</a>
<script src="assets/site.js" defer></script>
</body></html>
'''
    return head


def wrap_text(draw, text, font, max_width):
    words = text.split()
    if not words:
        return [""]
    lines, cur = [], words[0]
    for w in words[1:]:
        trial = f"{cur} {w}"
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def render_og(g: dict | None, out: Path, index=False):
    if Image is None:
        print("WARNING: no Pillow", file=sys.stderr)
        return
    W, H = 1200, 630
    bg, red = (11, 11, 11), (225, 29, 38)
    text_c, dim = (242, 239, 232), (184, 178, 166)
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 8], fill=red)
    if LOGO_PATH.exists():
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo_h = 64
        ratio = logo_h / logo.height
        logo = logo.resize((max(1, int(logo.width * ratio)), logo_h), Image.Resampling.LANCZOS)
        img.paste(logo, (48, 36), logo)
    try:
        font_tag = ImageFont.truetype(str(FONT_PATH), 26)
        font_h = ImageFont.truetype(str(FONT_PATH), 54)
        font_s = ImageFont.truetype(str(FONT_PATH), 28)
    except Exception:
        font_tag = font_h = font_s = ImageFont.load_default()
    tag = "FIELD GUIDE"
    tw = int(draw.textlength(tag, font=font_tag)) + 28
    draw.rectangle([48, 120, 48 + tw, 156], fill=red)
    draw.text((62, 124), tag, font=font_tag, fill=(255, 255, 255))
    if index:
        title = "SUSPICIOUS FIELD GUIDES"
        sub = "Weird checklists for places that feel like a cover story."
    else:
        title = g["title"].upper()
        sub = g["tagline"]
    y = 180
    for line in wrap_text(draw, title, font_h, W - 96)[:4]:
        draw.text((48, y), line, font=font_h, fill=text_c)
        y += 60
    draw.text((48, min(y + 16, 480)), "CONSPIRAPARTY.COM", font=font_s, fill=red)
    ty = min(y + 56, 520)
    for line in wrap_text(draw, sub, font_s, W - 96)[:2]:
        draw.text((48, ty), line, font=font_s, fill=dim)
        ty += 34
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "JPEG", quality=88)


def render_pdf(g: dict, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    c = pdfcanvas.Canvas(str(out), pagesize=letter)
    W, H = letter
    margin = 0.65 * inch

    def header(title):
        c.setFillColor(BG)
        c.rect(0, H - 0.55 * inch, W, 0.55 * inch, fill=1, stroke=0)
        c.setFillColor(RED)
        c.rect(0, H - 0.55 * inch, W, 0.08 * inch, fill=1, stroke=0)
        c.setFillColor(CREAM)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin, H - 0.38 * inch, "CONSPIRAPARTY · SUSPICIOUS FIELD GUIDE")
        c.setFont("Helvetica", 9)
        c.drawRightString(W - margin, H - 0.38 * inch, "conspiraparty.com")

    def footer(page_no):
        c.setFillColor(DIM)
        c.setFont("Helvetica", 8)
        c.drawString(margin, 0.4 * inch, "Entertainment only. Stay on public land. © 2026 Conspiraparty.com")
        c.drawRightString(W - margin, 0.4 * inch, f"Page {page_no}")

    # Page 1
    header(g["title"])
    y = H - 0.9 * inch
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, "CLASSIFIED TRAVEL BRIEFING")
    y -= 22
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 18)
    for line in _pdf_wrap(g["title"], 42):
        c.drawString(margin, y, line)
        y -= 22
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(HexColor("#444444"))
    for line in _pdf_wrap(g["tagline"], 78):
        c.drawString(margin, y, line)
        y -= 14
    y -= 8
    if g.get("warning"):
        c.setStrokeColor(RED)
        c.setFillColor(HexColor("#fff5f5"))
        c.roundRect(margin, y - 48, W - 2 * margin, 52, 4, fill=1, stroke=1)
        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin + 8, y - 12, "FIELD RULE")
        c.setFillColor(black)
        c.setFont("Helvetica", 8)
        ty = y - 24
        for line in _pdf_wrap(g["warning"], 92):
            c.drawString(margin + 8, ty, line)
            ty -= 11
        y -= 64
    c.setFillColor(black)
    c.setFont("Helvetica", 9)
    for line in _pdf_wrap(g["intro"], 95):
        c.drawString(margin, y, line)
        y -= 12
    y -= 10
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Things That Are Weird")
    y -= 16
    c.setFillColor(black)
    c.setFont("Helvetica", 9)
    for item in g["checklist"]:
        if y < 1.0 * inch:
            footer(1)
            c.showPage()
            header(g["title"])
            y = H - 0.9 * inch
            c.setFillColor(RED)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin, y, "Things That Are Weird (cont.)")
            y -= 16
            c.setFillColor(black)
            c.setFont("Helvetica", 9)
        c.rect(margin, y - 1, 9, 9, stroke=1, fill=0)
        for i, line in enumerate(_pdf_wrap(item, 88)):
            c.drawString(margin + 16, y, line)
            if i:
                y -= 11
        y -= 15

    # Spots + notes — new page if needed
    if y < 3.2 * inch:
        footer(1)
        c.showPage()
        header(g["title"])
        y = H - 0.9 * inch
        page = 2
    else:
        page = 1
        y -= 8

    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Suspicious Spots (public)")
    y -= 16
    c.setFillColor(black)
    for s in g["spots"]:
        if y < 1.2 * inch:
            footer(page)
            c.showPage()
            page += 1
            header(g["title"])
            y = H - 0.9 * inch
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin, y, s["name"])
        y -= 12
        c.setFont("Helvetica", 8)
        for line in _pdf_wrap(s["note"], 95):
            c.drawString(margin, y, line)
            y -= 10
        y -= 6

    y -= 6
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Agent Notes")
    y -= 16
    c.setFillColor(black)
    c.setFont("Helvetica", 8)
    for n in g["notes"]:
        if y < 0.9 * inch:
            footer(page)
            c.showPage()
            page += 1
            header(g["title"])
            y = H - 0.9 * inch
        for i, line in enumerate(_pdf_wrap("• " + n, 95)):
            c.drawString(margin, y, line)
            y -= 10
        y -= 4

    y -= 10
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(HexColor("#666666"))
    c.drawString(margin, y, "More guides + phone checklists: conspiraparty.com/field-guides.html")
    footer(page)
    c.save()


def _pdf_wrap(text, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


CSS = '''
/* Suspicious Field Guides */
.fg-page .share-box{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:8px}
.fg-page .share-links{display:flex;flex-wrap:wrap;gap:8px}
.fg-page .share-links[hidden]{display:none!important}
.fg-hint{color:var(--text-dim);font-size:.92rem;margin:0 0 14px}
.fg-checklist{display:flex;flex-direction:column;gap:8px}
.fg-check{
  display:flex;gap:12px;align-items:flex-start;
  background:var(--bg);border:1px solid rgba(255,255,255,.12);
  padding:12px 14px;border-radius:6px;cursor:pointer;
  font-size:.95rem;line-height:1.35;
}
.fg-check input{width:20px;height:20px;margin-top:2px;accent-color:var(--red);flex:0 0 auto}
.fg-check:has(input:checked){border-color:var(--red);opacity:.85}
.fg-check:has(input:checked) span{text-decoration:line-through;opacity:.75}
.fg-progress{margin-top:16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;color:var(--text-dim)}
.fg-spots{display:grid;gap:14px;margin-top:18px}
@media(min-width:720px){.fg-spots{grid-template-columns:1fr 1fr}}
.fg-spot{background:var(--bg-2);border:1px solid rgba(255,255,255,.1);padding:16px 18px;border-radius:6px}
.fg-spot h3{margin:0 0 8px;font-family:var(--font-display);letter-spacing:.02em;font-size:1.15rem}
.fg-spot p{margin:0;color:var(--text-dim);font-size:.92rem}
.fg-notes{margin:12px 0 0;padding-left:1.1em;color:var(--text-dim)}
.fg-notes li{margin:0 0 10px}
.fg-warn{
  margin:16px 0 0;padding:12px 14px;border:1px solid var(--red);
  background:rgba(225,29,38,.12);border-radius:6px;font-size:.92rem;
}
.fg-grid .fg-card img{width:100%;height:auto;aspect-ratio:1200/630;object-fit:cover;background:#111}
.fg-card .btn.sm{margin-top:10px;display:inline-flex}
@media(max-width:720px){
  .fg-page .share-native{display:inline-flex}
}
@media(min-width:721px){
  .fg-page .share-native{display:none}
  .fg-page .share-links{display:flex!important}
  .fg-page .share-links[hidden]{display:flex!important}
}
'''

JS = r'''
(function(){
  var page = document.querySelector('.fg-page');
  if(!page) return;
  var slug = page.getAttribute('data-fg-slug') || 'guide';
  var key = 'cp-fg-' + slug;
  var boxes = Array.prototype.slice.call(document.querySelectorAll('[data-fg-check]'));
  var countEl = document.querySelector('[data-fg-count]');

  function load(){
    try{
      var raw = localStorage.getItem(key);
      var set = raw ? JSON.parse(raw) : [];
      if(!Array.isArray(set)) set = [];
      boxes.forEach(function(b){
        b.checked = set.indexOf(b.value) !== -1;
      });
      update();
    }catch(e){}
  }
  function save(){
    var set = boxes.filter(function(b){return b.checked}).map(function(b){return b.value});
    try{ localStorage.setItem(key, JSON.stringify(set)); }catch(e){}
    update();
  }
  function update(){
    var n = boxes.filter(function(b){return b.checked}).length;
    if(countEl) countEl.textContent = String(n);
  }
  boxes.forEach(function(b){ b.addEventListener('change', save); });
  var reset = document.querySelector('[data-fg-reset]');
  if(reset){
    reset.addEventListener('click', function(){
      boxes.forEach(function(b){ b.checked = false; });
      save();
    });
  }
  load();

  function canNativeShare(){
    return typeof navigator !== 'undefined' && typeof navigator.share === 'function'
      && (window.matchMedia('(max-width:720px)').matches || /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent||''));
  }
  document.addEventListener('click', function(e){
    var shareBtn = e.target.closest('[data-share]');
    if(shareBtn){
      var box = shareBtn.closest('.share-box');
      if(!box) return;
      var url = box.getAttribute('data-share-url') || location.href;
      var text = box.getAttribute('data-share-text') || document.title;
      if(canNativeShare()){
        navigator.share({ title: document.title, text: text, url: url }).catch(function(){});
        return;
      }
      var links = box.querySelector('.share-links');
      if(links) links.hidden = !links.hidden;
      return;
    }
    var copyBtn = e.target.closest('[data-copy]');
    if(copyBtn){
      var box = copyBtn.closest('.share-box');
      if(!box) return;
      var url = box.getAttribute('data-share-url') || location.href;
      var done = function(){
        copyBtn.classList.add('copied');
        copyBtn.textContent = 'Copied';
        setTimeout(function(){ copyBtn.classList.remove('copied'); copyBtn.textContent = 'Copy link'; }, 1600);
      };
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(url).then(done).catch(function(){ window.prompt('Copy link', url); });
      } else {
        window.prompt('Copy link', url);
      }
    }
  });
})();
'''


def patch_nav_and_sitemap():
    # Add Field Guides to main nav on key templates (index + a few hubs) — branch only
    targets = [
        "index.html", "free-printables.html", "weird-news.html", "memes.html",
        "shirts.html", "quiz.html", "gift-guide.html", "blog.html",
    ]
    needle = '<li><a href="weird-news.html">Weird News</a></li>'
    insert = needle + '\n<li><a href="field-guides.html">Field Guides</a></li>'
    # weird-news may use different formatting
    for name in targets:
        path = ROOT / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "field-guides.html" in text and "Field Guides" in text:
            continue
        if needle in text:
            text = text.replace(needle, insert, 1)
            path.write_text(text, encoding="utf-8")
            print("nav:", name)
            continue
        # weird-news multiline
        alt = re.search(r'<li><a href="weird-news\.html">Weird News</a></li>', text)
        if alt:
            text = text[:alt.end()] + '\n        <li><a href="field-guides.html">Field Guides</a></li>' + text[alt.end():]
            path.write_text(text, encoding="utf-8")
            print("nav:", name)
            continue
        # href with leading path variants in nested pages skip

    sm = ROOT / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    if "field-guides.html" not in text:
        block = f'''  <url><loc>{SITE}/field-guides.html</loc><lastmod>{TODAY}</lastmod></url>
'''
        for g in GUIDES:
            block += f'''  <url><loc>{SITE}/field-guides/{g["slug"]}.html</loc><lastmod>{TODAY}</lastmod></url>
'''
        text = text.replace("</urlset>", block + "</urlset>")
        sm.write_text(text, encoding="utf-8")
        print("sitemap updated")


def main():
    GUIDES_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    OG_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "assets" / "field-guides.css").write_text(CSS, encoding="utf-8")
    (ROOT / "assets" / "field-guides.js").write_text(JS, encoding="utf-8")
    (ROOT / "field-guides.html").write_text(render_index(), encoding="utf-8")
    render_og(None, OG_DIR / "index.jpg", index=True)
    for g in GUIDES:
        html_path = GUIDES_DIR / f"{g['slug']}.html"
        html_path.write_text(render_guide_html(g), encoding="utf-8")
        render_og(g, OG_DIR / f"{g['slug']}.jpg")
        render_pdf(g, PDF_DIR / f"{g['slug']}.pdf")
        print("built", g["slug"])
    # data dump for previews
    (ROOT / "data" / "field-guides.json").parent.mkdir(exist_ok=True)
    (ROOT / "data" / "field-guides.json").write_text(json.dumps(GUIDES, indent=2), encoding="utf-8")
    patch_nav_and_sitemap()
    print("DONE", len(GUIDES), "guides")


if __name__ == "__main__":
    main()
