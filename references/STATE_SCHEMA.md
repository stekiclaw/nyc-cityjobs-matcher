# Private host state guidance (not an executable database)

The Skill is **prompt-only**. The host task, saved instructions, memory, or retrievable prior results may carry state. The Skill must not assume any of these are automatically available, especially after changing platform, project or task. Keep all private application records **out of this public GitHub repository**.

## Candidate profile in task instructions
- Explicit requested scope and hard exclusions (never silently broaden).
- Anonymized role functions, approximate experience, skills/tools, duties and scale/achievements.
- Education/licensing and civil-service eligibility if voluntarily supplied.
- Salary, geography and work-mode preferences if supplied.
- Distinguish user-selected role families from inferred optional suggestions.
- Do not store employer/person names or confidential system identifiers from private job history.

## Applied-job record (one per verified application)
- Official canonical `cityjobs.nyc.gov/job/...` URL.
- Job ID and JID slug if known; agency, business and civil-service titles.
- Unit/division, posting/closing dates if officially published.
- A brief verified differentiator (duties/qualifications) **only** if needed for conservative repost review.
- Application state = applied or explicit user exclusion.

Exact official identifiers support durable exclusions **only if the next run can access the records**. Agency+title is NOT a durable unique key. Two distinct openings with the same agency/title must remain candidates or be marked possible repost, never silently excluded.

## Per-task monitoring checkpoint when supported
- Task search scope/profile version, America/New_York as-of date, successful-source timestamp if available.
- Last successfully verified list of `Job ID / JID / URL / official-open-status / fit bucket`.
- Previously alerted stable event keys for notification deduplication.
- Any known inaccessible source or completeness caveat.

Only compare with a *verified and accessible* previous checkpoint. First run = baseline; failed run preserves last good checkpoint. If the host cannot provide cross-run state, task must report current openings only and cannot promise changes-only accuracy. Task instructions may have to be edited when a new job is applied to; changes to a different conversation may not propagate.

**Portability contract:** This is a conceptual state checklist, not a JSON schema or local persistence API. ChatGPT, Muse and other hosts have different capabilities. No local Python helper, database or runtime dependency is needed.
