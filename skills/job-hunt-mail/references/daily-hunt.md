# Daily hunt mode

The scored, batched pipeline. Runs once a day. Produces ten scored application
drafts, files them to Drive, and sends only what the user approves.

## Folder layout

```
job-hunt/
├── cv.pdf                      the CV, source of truth
├── cv-profile.md               extracted profile (create once)
├── data/jobs.json              scrape output: title, company, loc, sal, salk, src, type, dup, url, date
├── state/seen.json             jobs already drafted or rejected
├── applications/YYYY-MM-DD/    today's drafts
└── reports/YYYY-MM-DD.md       today's summary table
```

There is no job description in `jobs.json`. Descriptions live behind `url`.

## Step 1. Build the CV profile, once

Run only when `cv-profile.md` is missing or the user says the CV changed. Read
`cv.pdf` and write `cv-profile.md` with roles, employers, dates, years per role;
tools tagged `production` / `project` / `mentioned`; domains shipped; scope
evidence as bare numbers (team size, users, revenue, data volume, contract
length); constraints (location, timezone, remote policy, salary floor); and gaps
you noticed.

Then continue straight into Step 2. Do not stop for confirmation.

## Step 2. Load and dedupe

Read `data/jobs.json` and `state/seen.json`. Drop seen URLs, collapse `dup`
siblings.

Report: `161 rows, 40 duplicate links collapsed, 12 seen on earlier runs, 109 roles to screen today`.

## Step 3. Pre-screen, then open the survivors

Opening every page wastes an hour and most are not close.

Pre-screen every role using only `title`, `company`, `loc`, `sal`, `type`. Give
a rough 0-100 from the title and terms alone. Drop anything under 45. Keep the
top 30.

Then open the `url` for those 30 and read the actual post. Extract required
skills and years asked; stated seniority; domain and product; location, remote
policy, timezone overlap; salary or budget as written; anything disqualifying
(clearance, degree requirement, on-site only, agency reposting an old role).

When a page will not load, is expired, or hides behind a login: mark `UNREADABLE`,
score from the sheet fields alone, cap the total at 60, and say why in one line.
Never invent the content of a page you could not read.

## Step 4. Score, 0-100

Four criteria, fixed weights. Report all four subscores every time, never the
total alone.

| Criterion | Max | Rule |
|---|---|---|
| Skills overlap | 40 | Required skills the profile backs as `production`. `project` counts half. `mentioned` and keyword collisions count zero. |
| Seniority fit | 25 | Level asked against years and scope owned. Score the gap both directions. Two levels below loses what two levels above loses. |
| Domain fit | 20 | Industry and problem space against past work. Adjacent scores partial. |
| Practical fit | 15 | Location, remote policy, timezone, salary against constraints. Post hides the number: score low and write `data missing`. Never guess a range. |

Write two sentences per role: one on the strongest match, one on the weakest.

## Step 5. Rank, cut, write

Take the ten highest. One file per role in `applications/YYYY-MM-DD/`, named
`NN-company-role.md`, holding:

1. Score and the four subscores
2. Role, company, source site, salary as written, link, sibling links when posted twice
3. The two sentences from Step 4
4. Three CV points to lead with. Each names employer, number, result. From `cv-profile.md`, never invented
5. The honest gap. What the post asks for and the CV does not carry. Plain, one or two lines, no spin
6. A first paragraph the user can send. Proposal opening on Upwork, cover letter opening on Indeed and Glassdoor

If the post wants Kubernetes and the CV has no Kubernetes, the gap section says
so and the opening paragraph does not mention it.

## Step 6. File into Drive

Drive is where the user reads on the phone. The local folder stays source of
truth. Use a connected Drive integration if one is available (see `SKILL.md`, Backends).

1. Find the folder named `Job Hunt`, create it when missing
2. Inside it, create a folder named `YYYY-MM-DD`
3. Upload each of the ten drafts as a Google Doc, sent as `text/markdown`, named
   `NN — Company — Role` so the folder sorts by rank
4. Upload the day's scores as a Google Sheet. Build a CSV with one row per
   scored role. Send as `text/csv`. Name it `Scores YYYY-MM-DD`
5. Report every link in chat: folder first, then Sheet, then the ten Docs

CSV columns, in order: `Rank, Score, Skills, Seniority, Domain, Practical,
Role, Company, Source, Salary as written, Type, Status, URL`

`Status` is `shortlisted`, `scored`, or `unreadable`.

Never share, never change permissions, never move or delete anything already in
Drive. One folder per day, never overwrite yesterday's. The connector writes a
new Sheet each run rather than appending to an old one. When an upload fails,
keep the local files, say which step failed, and stop. A missing Drive copy is a
small problem, a half-uploaded day is a confusing one.

## Step 7. Send what the user approves

Do not send anything yet. Present the ten drafts in chat, compactly: rank,
company, role, score, the recipient address when one is confirmed, and the one
line gap. Then ask which to send.

The approval gate in `SKILL.md` decides the rest. Re-read it before every send.

When sending, attach the role-appropriate CV file. Restate recipient, subject,
and attachment, send exactly the ranks named, and report each send result as it
lands. A bounced or failed send gets reported, never silently retried.

Listings with no confirmed address are not sendable by email. Say so and leave
them for the user.

## Step 8. Report and remember

`reports/YYYY-MM-DD.md` gets the Drive folder link at the top, the Step 2 and 3
counts, the top ten as a table (rank, score, four subscores, role, company,
source, salary, link), everything scored but not shortlisted as a second table
sorted by score (nothing gets deleted), the `UNREADABLE` roles with reasons, and
what broke.

Then update `state/seen.json`: the ten drafted URLs under `applied_or_drafted`,
anything scoring under 45 under `rejected_below_threshold`.

## Batching

Work in batches of 25 roles. Report after each batch, then continue.

## Running it

```
Use the job-hunt skill. Run today's job hunt.
```

First run only, after a CV change, or on request:

```
Use the job-hunt skill. Rebuild cv-profile.md from cv.pdf and stop.
```