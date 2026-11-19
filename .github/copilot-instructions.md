# GitHub Copilot entry

Read `AGENTS.md` at the repository root first. It is the canonical operating manual for this
search-to-apply pipeline. This file only maps tools; `AGENTS.md` wins on any conflict.

## Tooling map (GitHub Copilot CLI / coding agent / VS Code)
- **Discovery:** use web fetch and web search tools for `feed` and `ats` sources.
- **Web forms:** Playwright MCP from `.mcp.json` is the default. See `BROWSER-TOOLING.md` for alternatives
  and the submission flow. If a real signed-in Chrome is available via a `browse` tool, use it for
  auth-gated boards.
- **Email:** use a configured Gmail/SMTP integration with `.env` credentials; queue + log `skipped`
  when it is not configured.
- **Notification:** report the run summary in chat, or write it to `data/run-<date>.log`.

## Non-negotiables
Honor `PAUSE` and `dryRun`, stay under `maxApplicationsPerDay`, dedupe, never fabricate facts, never
bypass a CAPTCHA, verify the resume attached before submitting, log every attempt, and use only the
identity in `config/identity.json`.
