# Application template (reusable base)

A reusable base for the **email body / cover letter**. Copy it into your own config, then tune the wording,
length and evidence to your voice and the role. `AGENTS.md` governs when and how a letter is sent; this
file only describes its shape.

The email body *is* the letter. The resume PDF is the only required attachment. If a listing asks for the
letter as a separate PDF, follow that instruction instead.

## Mechanics

- **Email application.** Subject: the job title as posted. Acceptable variants: `{Role} – {Your Name}`,
  `Application for {Role} Position`. Body: the letter below. Attachment: the role-matched resume.
- **Portal or form.** Paste the letter alone, unless the field asks for a different format.
- **Salutation.** `Dear Recruiter,` by default. `Dear {Company} team,` when applying through a named
  agency or consultancy.
- **Length.** Around 340–420 words. Shorter reads rushed; cut anything that does not earn its place.
- **Formatting.** Prose only. No bullets, headers or bold unless the portal requires them.
- **Delivery.** Every draft comes back in chat as copyable plain text in a fenced `text` block, and is
  saved to `output/cover-letters/<date>_<company>_<role>.md`. A file path is not a substitute for the text.

## The letter

**1. Opener (2–3 sentences).**
`I'm applying for the {job_title} role at {company}.` Then years, then stack, then a specific hook from
the posting (remote status, contract, assessment, a nice-to-have). Never open with flattery or the
company's mission.

**2. Lead project (4–6 sentences).**
Open with `The work I'd point you to first is ...`. Cover what it is, who used it, the hard part and the
judgement call inside it. One sentence should be an actual decision, phrased as a decision. Structural
numbers are fine; performance figures are not.

**3. Supporting projects (two, 1–3 sentences each).**
`Before that, ...`. Pick the two that answer this posting's requirements, not the two easiest to describe.
A third, if it earns its place, arrives as `Earlier at {employer} ...`.

**4. Collaboration and judgement (3–5 sentences).**
`The collaboration side runs through all of it: ...` or a first-person variant. Code review as a habit
rather than a gate, documentation for whoever picks the system up next, technical behaviour explained to
non-engineers. Team scope lands here.

**5. Honest gap (only when the posting asks for something the candidate does not have).**
One short plain paragraph: `One honesty line: ...` / `One gap I should name.` /
`The one part I would want to ramp quickly is ...`. Name the missing skill plainly, then say what
transfers. Never claim it, never slip it into the stack list, never apologise twice.

**6. Links.**
`More of my work is at {portfolio} and {github}.` On its own line. Take these from `config/identity.json`.

**7. Close.**
`Thank you for considering the application. I'm available for an interview and can give {notice}.`
Contract role: `I'm available to start immediately on a contract.` Permanent role: `can start with
standard notice`.

**8. Sign-off.**
`Best regards,` then the contact block **copied verbatim** from `config/identity.json`. Never retype the
phone number or links from memory.

## Numbers policy

- Allowed: structural counts you can verify from the CV (years, module or page counts, team sizes,
  number of delivered projects), stack versions, certification names and dates.
- Not allowed: percentages, latency, uptime, user counts, multipliers, "pixel-perfect", or any invented
  performance figure. The resume carries those.

## Hard rules

1. Eight blocks, in the order above. Blocks 3 and 4 may be swapped for backend or full-stack heavy
   postings. Never merge them.
2. Never understate seniority. Use the experience framing in the candidate's profile.
3. No AI tells: no "passionate", "excited to apply", "eager to", "esteemed", "leverage", "proven track
   record", no rule-of-three padding, no "not just X, but Y", no templated closers. Vary sentence length.
   Prefer zero em-dashes.
4. Name the company and something specific from the post in the first two sentences.
5. Vary which projects and team-scope facts appear across letters. A batch must not read as one letter
   with the nouns swapped.
6. Drop every placeholder. No `{{...}}`, no `[brackets]`, no TODO.
7. Never submit or send without checking the guardrails in `AGENTS.md` §4.
8. Compose from a file on disk. Grep for `google.com/url?q=`, `&ust=`, `&sa=E` and `{{` before the text
   is used anywhere.
9. Never invent an employer, a metric, a date or a tool. If the CV does not support it, it does not
   appear.
10. Always hand the letter over as copyable plain text in chat, in a fenced `text` block, even when it
    is also saved to a file.
