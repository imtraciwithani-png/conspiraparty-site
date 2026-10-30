# Suspicious Road Trip (preview)

Phone-first companion for **The Suspicious Road Trip Guide** (KDP).

## Modes (localStorage)

- **Kids** (`srt-content-mode=kids`): family-safe Mystery Facts, Mild/Spooky tone, Family HQ (quiz, investigator lesson, car games, junior badges, certificate, parent tips).
- **Adult** (`srt-content-mode=adult`): uncensored dossiers on state pages — believers vs documented, darker history, political conspiracy culture / Q-adjacent internet lore where relevant. **Never shown in Kids mode.**

## Paths

- App: `/road-trip-app/`
- Data: `data/places.json` (book), `data/family.json` (kids + adult layers)
- Screenshots: `preview/` and `preview/big/` (780×1100)

## Preview

```bash
cd /workspace/cp-roadtrip
python3 -m http.server 8899
# http://127.0.0.1:8899/road-trip-app/
```

Branch `road-trip-app` — do not push until Traci approves.
