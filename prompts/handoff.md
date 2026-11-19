# Handoff prompt (generic template)

Paste everything below the line into a fresh session with this repository as the working directory.
Replace the bracketed line with your own local path before pasting.

---

You are continuing work on **Job Search & Apply Pipeline**, an agent-driven search → tailor → apply →
log system in this directory. Read `AGENTS.md` now — it is the complete, authoritative spec. Everything
you do must comply with it; if anything I say here conflicts with `AGENTS.md`, follow `AGENTS.md`.

Also read before doing anything: `config/preferences.json`, `config/role-resume-map.json`,
`config/sources.json`, `config/identity.json`, `config/profile.md`, `BROWSER-TOOLING.md`, and
`resumes/README.md`. If a runtime config file is missing, say which example file to copy and stop
before applying to anything.

## Non-negotiable guardrails (from AGENTS.md §4)
- Honor the `PAUSE` file: if it exists in the project root, stop immediately and do nothing else.
- Honor `dryRun` in `config/preferences.json`. When true, prepare everything but never submit or send.
- Never exceed `maxApplicationsPerDay`. Never apply to the same job twice or the same company inside
  `dedupeCompanyDays`. Dedupe against `data/applications.jsonl`.
- Never fabricate facts. Never send a wrong-role resume — skip the role and log it.
- Never solve or bypass a CAPTCHA or login wall. Log `blocked` and move on.
- Copy identity fields verbatim from `config/identity.json`. Never submit a form whose resume didn't
  attach. Log every attempt, including failures.
- Act only as the one identity configured in `config/identity.json`.

## First task: supervised dry run
1. Report what is missing: runtime config files, resumes, `.env` / Gmail setup, and whether a browser
   tool is available.
2. If nothing is blocking, run discovery and tailoring (steps a–e) against feed/ATS sources, staying under
   `maxApplicationsPerDay`. Skip browser sources if no browser tool is available.
3. Because `dryRun` is true, prepare each application fully, save the letters under
   `output/cover-letters/`, and log each as `dry-run` — but submit nothing.
4. Summarize: how many roles matched, which resume each mapped to, and paste one full sample letter so
   the voice and accuracy can be checked.

Nothing goes live until the dry-run output has been reviewed and `dryRun` has been explicitly flipped.
