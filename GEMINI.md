# GEMINI.md — Gemini CLI entry

Read `AGENTS.md` in this directory first — it is the canonical spec for the mission, the per-run workflow
and the guardrails. This file only records Gemini-CLI-specific tooling. If anything here conflicts with
`AGENTS.md`, `AGENTS.md` wins.

## Tooling map (Gemini CLI)
- **Discovery (`feed` / `ats` sources):** use built-in web fetch / Google Search grounding to pull
  JSON/RSS endpoints and find postings and ATS boards.
- **Web-form applications (`browser` / `html` sources + submissions):** Playwright MCP, configured in
  `.gemini/settings.json`. See `BROWSER-TOOLING.md` for the submission flow and alternatives. Auth-gated
  boards need a signed-in session; on a login wall or CAPTCHA, log `blocked` and move on.
- **Email applications:** use a configured Gmail/SMTP MCP with `.env` credentials. If Gmail is not
  configured, queue the email and log `skipped`.
- **Summary notification:** whatever notification tool is configured; otherwise write the summary to
  `data/run-<date>.log`.

## How it runs
`scripts/run.ps1` can invoke Gemini CLI headless against `prompts/daily-run.md`:

```
gemini -p "$(Get-Content prompts/daily-run.md -Raw)" --yolo
```

Auto-submit needs a configured browser/Gmail and `dryRun: false` in `config/preferences.json`.

## Non-negotiables (see AGENTS.md §4)
Honor `PAUSE`, honor `dryRun`, cap at `maxApplicationsPerDay`, dedupe, never fabricate, never solve a
CAPTCHA, log everything to `data/applications.jsonl`, and use only the identity in `config/identity.json`.
