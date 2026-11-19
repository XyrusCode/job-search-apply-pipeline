<!--
Email template for email-based applications.
- Subject line matters: role + name, matching any format the listing asks for.
- Attach the role's resume PDF. Attach the cover letter as PDF, or paste it in the body if the listing
  says "no attachments" / "paste in body".
- Keep the body short; the cover letter carries the detail.
- Send only after Gmail is configured (see .env / AGENTS.md §6). Otherwise queue + log skipped.
- Copy every identity field verbatim from config/identity.json.
-->

To: {{application_email}}
Subject: {{job_title}} — {{full_name}}

Hi {{hiring_contact_or_team}},

I'd like to apply for the {{job_title}} role at {{company}}. My resume is attached, and a short cover
letter{{covers_attached_or_below}}.

Quick summary: {{experience_years}} building {{role_focus}} software, recently {{one_relevant_win}}.
Portfolio and code are at {{portfolio}} and {{github}}.

Thanks for your time,
{{full_name}}
{{email}} · {{phone}} · {{portfolio}} · {{github}} · {{linkedin}}

<!-- Attachments: {{resume_filename}} (required), {{cover_letter_pdf}} (if attaching) -->
