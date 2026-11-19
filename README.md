# Job Search & Apply Pipeline

An agent-driven, **end-to-end search-to-apply pipeline**. It is more than a job search tool: each run
discovers openings, filters and dedupes them, tailors a cover letter, **applies** through the listing's
web form or email, logs every attempt, and sends a summary. It ships in `dryRun` mode and has a one-file
kill switch.

```
discover → filter/dedupe → tailor letter → APPLY (form | email) → log → notify
```

The behavior lives in **`AGENTS.md`**, a plain-English operating manual the agent reads on every run.
There is no compiled app; `scripts/run.ps1` is an optional scheduler entry point that launches a CLI
against `prompts/daily-run.md`.

## Harness support

`AGENTS.md` is the single source of truth. Every harness entry point below is a short tooling map that
defers to it.

| Harness | Entry point | Browser config |
|---|---|---|
| Claude Code | `CLAUDE.md` | `.mcp.json` (Playwright MCP) |
| GitHub Copilot (CLI / coding agent / VS Code) | `.github/copilot-instructions.md` | `.mcp.json` |
| OpenAI Codex CLI | root `AGENTS.md` | `.codex/config.toml` |
| Gemini CLI | `GEMINI.md` | `.gemini/settings.json` |
| opencode | `opencode.json` | `opencode.json` |
| Cursor | `.cursor/rules/pipeline.mdc` | `.mcp.json` |

Browser automation details, including alternatives to Playwright MCP, are in [`BROWSER-TOOLING.md`](BROWSER-TOOLING.md).

## Layout

| Path | What |
|---|---|
| `AGENTS.md` | Canonical operating manual (source of truth) |
| `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursor/rules/pipeline.mdc`, `opencode.json` | Per-harness entry points |
| `BROWSER-TOOLING.md` | Browser tool setup and submission rules |
| `config/*.example.*` | Copy these to the runtime names, then fill in your own details |
| `config/application-template.md`, `config/letter-voice-notes.md` | Reusable base cover-letter formats — edit to your voice |
| `templates/` | Cover-letter and application-email placeholder templates |
| `prompts/daily-run.md` | Trigger prompt fed to the agent each run |
| `scripts/run.ps1` | Optional Windows scheduler entry point |
| `resumes/` | Your role-specific resume PDFs (git-ignored) |
| `data/`, `output/`, `state/` | Runtime logs, generated letters, screenshots and state (git-ignored) |
| `PAUSE` | Create to halt all runs |

## First-time setup

1. **Create your runtime config.** Copy every `config/*.example.*` file to the same name without
   `.example`, then fill it in:
   - `identity.example.json` → `identity.json` — exact strings copied into forms and emails. The agent
     reads these values verbatim; it never retypes them from memory.
   - `preferences.example.json` → `preferences.json` — roles, filters, location rules, daily cap.
   - `role-resume-map.example.json` → `role-resume-map.json` — role → resume filename mapping.
   - `sources.example.json` → `sources.json` — job sources, in the order they should be searched.
   - `profile.example.md` → `profile.md`, `search-preferences.example.md` → `search-preferences.md` —
     your background and search standing rules.
   All runtime copies are git-ignored so personal data never enters version control.
2. **Add resumes.** Put your role-specific PDFs in `resumes/` with filenames matching
   `config/role-resume-map.json`. The pipeline skips a role whose resume is missing; it never
   substitutes a different one.
3. **Configure secrets.** Copy `.env.example` to `.env` and fill it in. Email applications require an
   authorized Gmail connector/OAuth or an SMTP app password. Until then, email applications are queued
   and logged as `skipped`.
4. **Set up a browser tool.** See [`BROWSER-TOOLING.md`](BROWSER-TOOLING.md). Playwright MCP is the
   portable default; a real signed-in Chrome via `browse`, or the `agent-browser` CLI, are alternatives.
5. **Sign in where needed.** Auth-gated boards (LinkedIn, Indeed, Wellfound) need a signed-in browser
   session. Login walls and CAPTCHAs are logged as `blocked`, never bypassed.
6. **Adapt the letter bases.** `config/application-template.md`, `config/letter-voice-notes.md` and
   `templates/` are generic starting points. Replace the example wording with your own voice and
   evidence before sending anything.

## Running it

Start with the trigger prompt in your harness, for example:

```
Follow prompts/daily-run.md and run the pipeline now.
```

Windows scheduler (optional):

```powershell
pwsh ./scripts/run.ps1          # honors dryRun in config/preferences.json
pwsh ./scripts/run.ps1 -Install # weekdays 09:00
pwsh ./scripts/run.ps1 -Uninstall
```

Set `$CLI` at the top of `scripts/run.ps1` to `claude`, `gemini` or `opencode`. Other harnesses can be
invoked directly with `prompts/daily-run.md`; see the entry-point files above.

## Going live

1. Leave `dryRun: true` for the first few runs. Inspect `data/applications.jsonl` and
   `output/cover-letters/`: matches, resume selection and letter voice.
2. When the output looks right, set `dryRun: false` and keep `maxApplicationsPerDay` low for a week.
3. Raise the cap and add sources gradually. Review the audit log regularly.

## Stopping it

- **Pause everything:** create an empty file named `PAUSE` in this folder. Every run aborts while it
  exists. Delete it to resume.
- **Unschedule:** `pwsh ./scripts/run.ps1 -Uninstall`.

## Guardrails

The hard rules live in `AGENTS.md` and include: honor `PAUSE` and `dryRun`; never exceed the daily cap;
never double-apply or contact excluded companies; never fabricate facts or send the wrong resume; never
solve a CAPTCHA or login wall; copy identity fields verbatim from `config/identity.json`; never submit a
form whose resume did not attach; log **every** attempt; act as one configured identity only.

## Honest limitations

- Anti-bot boards (LinkedIn, Indeed, Wellfound) are best-effort. Public feeds and ATS JSON APIs are the
  reliable core.
- Region-local boards without an API are scraped via HTML or browser and may be geo-restricted. Edit
  `sources.json` to the boards relevant to you.
- Browser file upload is the riskiest step. The agent must verify the resume actually attached before
  submitting, and log a `failed` attempt when it cannot.
- Auto-submit carries residual risk. Dry-run, the daily cap, dedupe and the audit log keep it bounded.
- This runs locally on purpose: it needs your signed-in browser and your resumes.
