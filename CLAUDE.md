# CLAUDE.md — Claude Code entry

Read `AGENTS.md` in this directory first. It is the canonical spec for the search-to-apply pipeline.
This file only records Claude-Code-specific tooling. If anything here conflicts with `AGENTS.md`,
`AGENTS.md` wins.

## Tooling map (Claude Code)
- **Discovery (`feed` / `ats` sources):** `WebFetch` for direct endpoints, `WebSearch` to find fresh
  postings and ATS boards. No login needed for these.
- **Web-form applications (`browser` / `html` sources + submissions):** Playwright MCP, configured in
  `.mcp.json` and pre-approved in `.claude/settings.json`. See `BROWSER-TOOLING.md` for the submission
  flow and alternatives. `claude-in-chrome` is an option when a signed-in Chrome session is needed.
- **Email applications:** use the configured Gmail connector/MCP or SMTP per `.env`. If Gmail is not
  authorized, queue the email and log `skipped`.
- **Summary notification:** `PushNotification`, or write to `data/run-<date>.log` if unavailable.

## How it runs
`scripts/run.ps1` can launch Claude Code headless against `prompts/daily-run.md`:

```
claude -p "$(Get-Content prompts/daily-run.md -Raw)" --dangerously-skip-permissions
```

Auto-submit needs a configured browser/Gmail and `dryRun: false` in `config/preferences.json`.

## Non-negotiables (see AGENTS.md §4)
Honor `PAUSE`, honor `dryRun`, cap at `maxApplicationsPerDay`, dedupe, never fabricate, never solve a
CAPTCHA, log everything, and use only the identity configured in `config/identity.json`.
