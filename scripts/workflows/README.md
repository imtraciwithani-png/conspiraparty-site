# Weird News GitHub Action (preview)

The live path is `.github/workflows/weird-news.yml`.

GitHub blocked pushing that path from this bot token (needs the `workflow` OAuth scope).
The YAML here is the same file for review.

**When Traci approves going live:**
1. Copy `scripts/workflows/weird-news.yml` → `.github/workflows/weird-news.yml` on a push that has workflow scope (or add it in the GitHub UI).
2. Change the job `if:` from `github.ref == 'refs/heads/weird-news'` to allow `main` (or drop the gate).
3. Merge to `main`. Scheduled runs only fire from the default branch.

Until then the Action will not run against main.
