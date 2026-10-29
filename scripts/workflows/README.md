# Weird News GitHub Action

Canonical path once installed: `.github/workflows/weird-news.yml`

This copy under `scripts/workflows/` is the reviewed YAML (gated to `main`).
If `.github/workflows/` cannot be pushed (needs GitHub `workflow` OAuth scope),
copy this file into `.github/workflows/weird-news.yml` from a token/UI that has that scope.

Schedule: daily 14:00 UTC (~8:00 AM America/Denver). Also supports workflow_dispatch.
