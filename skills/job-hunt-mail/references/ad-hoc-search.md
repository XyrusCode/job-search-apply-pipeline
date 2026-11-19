# Ad-hoc mode

Search named boards on demand. No scoring, no Drive, no daily state file. Every
listing leaves the user with something actionable: a real URL, or a draft.

## Gather the profile first

Once, then reuse across runs (memory, a config file, or ask):

- Role and stack focus
- Location, and whether to search local, remote, or both
- Sources in priority order. Ask if not given. Job boards are highly region- and
  industry-specific, so do not assume a default list
- Contact sign-off: email, phone, portfolio
- Real quantified experience for drafts. Pull from the CV or ask. Never invent stats
- Whether to name past employers or keep experience generic ("in a previous role"). Ask once, remember

## Step 1. Search, in priority order

For each source:

- Prefer a connected connector or API when one exists
- Otherwise web-search the role plus location or remote qualifier on that
  specific site, then fetch the listing pages for title, company, pay, remote
  status, post date
- Capture the actual URL when the source provides one. Never fabricate or guess
- Some aggregators only surface listings via search snippets with no fetchable
  page. Note that explicitly instead of presenting a broken link
- Remote-only means remote from the listing content, not the title. Watch for
  "remote" labels that mean remote-from-one-country or fixed timezone hours.
  Flag these instead of silently including them
- If a source returns nothing new, say so. The user should know it was checked
- Expand past the given source list only when asked, or when the given sources
  return nothing relevant. Confirm before broadening

## Step 2. Dedupe

Check sent mail, existing drafts, and anything the user has already mentioned
applying to. Skip duplicates and say so explicitly.

## Step 3. URL or draft

Every new opening gets one. Real URL available: hand it over. Not available:
draft an application email.

## Step 4. Draft the email

Write the draft to a local file first so nothing is sent by accident. Use a
confirmed employer address only; never guess one. When no address is confirmed,
address the draft to the user instead and say plainly that the employer address
was not recoverable.

Subject line:

```
{Job Title} — {User's Name} [{Company} — apply via {channel}]
```

`{channel}` describes how to actually apply: a platform easy-apply, a specific
form URL, or "apply via {Source}, direct posting link unavailable".

Body:

- Opener naming the specific role and what it involves. No generic flattery, no
  reused template line
- 1-2 paragraphs of concrete fit. Real quantified experience matched to what this
  listing asks for
- Follow the stated preference on naming past employers
- Low-key, specific closing, not a hard sell
- Sign-off with the user's contact info

Voice rules live in `SKILL.md`. They are not optional here; drafted emails are
the most-read artifact this skill produces.

## Step 5. Send, after approval

Do not send while drafting. Show the drafts, then let the approval gate in
`SKILL.md` decide.

Send through a connected mail integration configured for the user's own address (see `SKILL.md`, Backends), attaching the role-appropriate CV.
Report each result. A bounce or failure gets reported, never silently retried.

Listings needing a web form are not sendable by email. Hand those back as a link
and say so.

## Step 6. Cleanup

When the user says a listing is expired, fake, or already applied to:

- Find the matching draft
- Delete it using the ID the mechanism actually requires. Some mail APIs
  distinguish a draft ID from the underlying message or thread ID, and using the
  wrong one fails silently. Confirm which is expected before deleting
- Confirm what was removed and list what is still active

For bulk deletion by age, check dates and content first. Only touch drafts from
this workflow, not unrelated old mail.

## Step 7. Report back

Scannable. One line per job: title, company, key qualifier (pay, remote,
timezone caveat), then either the URL or "drafted". When listing sources, give a
plain `Job — Company → source: X` list rather than prose.

## Adjacent cases

- **Multiple resume versions.** Match the version to the job type when saying
  what to attach, rather than assuming one default
- **Attaching files.** Large files sent inline often exceed a single call's
  limit. Check the practical size limit first. If it will not fit, say so and
  default to the user attaching manually
- **Freelance platforms.** When a marketplace tool is connected (Upwork or
  similar), use it directly instead of generic web search. It gives live account
  data (proposals, job feed, filters) that public search cannot
- **No connector available.** Check before assuming. If truly absent, fall back
  to web search and say plainly that it is a weaker view: no account data, no
  bidding or application history