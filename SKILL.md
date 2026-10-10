---
name: nyc-cityjobs-matcher
description: Prompt-only NYC CityJobs search, anonymous work-experience-to-JD matching and exclusion of previously applied jobs, designed for browser agents and scheduled/recurring cloud monitoring. No executable application required.
---

# NYC CityJobs Matcher

## Purpose and host modes
A **prompt-based Skill**, not a standalone job scraper, Python service, job database or CI suite. The host agent must browse official vacancies, reason over JDs, access any available private profile/previous run state, schedule user-authorized work, and notify. Do not assume a future scheduled run auto-loads this SKILL.md.

- **Interactive search:** Respect user-requested search scope (any role family). If target roles are unknown, first ask for an anonymized professional background and infer supported directions; if scope is known, stay within it.
- **Direct posting review:** Compare user-supplied official posting/JD to an anonymized profile, without requiring a prior role choice.
- **Recurring/monitoring:** With explicit user request, build a separately named host task for the search scope, preferred cadence and notification mode. Host task prompts must be **self-contained**, including search filters, anonymized evidence, hard eligibility gates and applied-job exclusion identifiers. See [task-templates.md](references/task-templates.md). Use a supported host scheduling tool and avoid duplicates. Do not claim background monitoring until host confirms creation. Never ask follow-up questions during a scheduled run: report missing configuration and require correction outside the run.

## Data minimization and intake
For personalized recommendations obtain a usable anonymized candidate profile, or reuse one verifiably available in the current host/task settings. Ask only for missing experience, approximate years, duties, skills/tools, measurable scale/results, education/licenses/certifications, civil-service eligibility (optional), salary/location/work-arrangement preferences and explicit target/exclusions. **Do not request or store names of the candidate's employers/agencies or coworkers, contacts, street addresses, employee IDs, case/ticket IDs, secrets, private links, hostnames or account details.** Normalize volunteered employer names to generic employer type. Public agency names appearing in vacancies are fine.

If no profile or the user declines one, offer a **general search** and do not claim personalized fit. Do not reconstruct private experience from unrelated conversations unless the user explicitly provides/authorizes it for the Skill. Keep explicitly selected job scope separate from inferred suggestions; never silently broaden.

## Live search and availability verification
At each run, search current official NYC CityJobs vacancies using host web/browser tools. Other sites are discovery only; verify every recommended vacancy on official `https://cityjobs.nyc.gov/job/...`. Do not invent ID, salary, dates, work arrangement, eligibility or official URL. Extract:
- Agency, exact business title, Job ID, JID/slug, official URL
- Civil-service title, unit/division when available
- Duties, mandatory qualifications vs preferred qualifications
- Salary range, posting date, closing date, location/work arrangement
- Current explicit site status including closed/expired and whether applications are accepted.

An official "expired"/"closed" notice takes precedence over a future stated closing date. A future closing date alone cannot establish that the application is open. Mark inaccessible/ambiguous status as **unverified**, not as an actionable opening. If the host cannot browse/verify official results, say so; do not report zero new jobs or no changes as if verified.

## Evidence-based JD matching
For every verified candidate vacancy, compare each **mandatory requirement**, day-to-day responsibility, and preferred criterion separately to the supplied anonymized profile; classify evidence as `supported`, `partially supported`, `missing`, or `unknown`. Civil-service list/title/appointment/hiring-pool eligibility is a gating condition, not a small score penalty. Confirmed unmet mandatory gate => Low fit / likely disqualified even with many keyword overlaps. Unknown gating requirement prevents Strong match until clarified. Strong = documented mandatory gates + substantial duties evidence; Good = confirmed gates and transferable duties; Stretch = relevant evidence but significant non-disqualifying gaps. Do not invent education/certifications/titles, numeric fit probabilities, or achievements. Read JDs; titles/keywords alone only aid discovery. For Strong/useful Good matches give 3–5 *truthful* resume-tailoring notes.

## Applied Jobs Ledger and conservative deduplication
When user says "applied" / "exclude" without official posting URL, proactively ask for that link in interactive mode. For unattended work, rely only on identifiers already stored in task/private accessible ledger. Prefer official Job ID, URL/JID, agency, exact title, civil-service title, unit, posting date and a short evidence-backed JD signature. Keep application records privately in **host-provided task instructions or state** if available; never add them to this public repo. If host cannot retain state, explain this and give a copy/paste update to the task prompt rather than falsely claiming permanent exclusion.

Strong exclusion: same official Job ID, exact official JID/URL (after sensible canonicalization). A new Job ID with same agency/title is **NOT** enough to exclude; treat as possible repost and require distinctive corroboration (same specific unit, duties, civil-service title, requirements, etc.). Even similar standardized JDs may represent distinct openings. Borderline cases go to **Review**, not auto-excluded. Apply same conservatism to deduplicate current search results. If only an agency/title is known without link, temporarily suppress in the current interactive session, then request official URL for durable exclusions.

The saved task should have a reliable applied-job list or identifiers. If it cannot access that list at runtime, do not claim "not yet applied" has been verified. An application update after task creation must be reflected in saved task instructions or an accessible host ledger before the next scheduled run; merely writing it in another chat may not propagate.

## Cloud scheduling and change alerts
Help create/update tasks **only** on user's explicit request for recurring checks. A task is scoped to a specified search, profile and hard filters; allow multiple independent tasks with different targets/cadences. Use supported host scheduler, not a fabricated background daemon. Do not request a specific minute when an approximate schedule is acceptable. If host does not offer scheduling or skill invocation, supply portable task template for manual paste. First scheduled run sets a baseline; it may return an initial candidate digest if requested, but should not claim a "newly appeared" job without verified previous dated evidence.

At every subsequent run:
1. Recheck official open status and required qualifications of candidate postings.
2. Exclude verified applied records and exact duplicates; flag uncertain reposts separately.
3. Compare **stable official job identifiers** with the last *accessible, successful* run under the same scope. Only label a job "new" if the evidence supports it; also flag material newly verified qualification/status changes.
4. In changes-only mode notify for meaningful newly found, open, not-applied, high-fit opportunities or important verified changes. Do not notify for unchanged old jobs, timestamp-only changes, or unreliable/unverified vacancies.
5. If query fails, do not replace the last successful baseline or claim "no new jobs". If no previous state is accessible, clearly label as a current snapshot, not a delta. Suppress no-change notifications only when the host supports it.

For each recommendation: title, agency, Job ID/JID, salary, post/close date, official link, civil-service title, hard eligibility, minimum qualifications, duties evidence, fit bucket, gaps and 14-day deadline flag; add location/work mode if listed. Alert reports should be concise and source-backed.

## Acceptance
Use [acceptance-scenarios.md](references/acceptance-scenarios.md) for prompt-level evaluation, not executable regression tests. Private state guidance: [STATE_SCHEMA.md](references/STATE_SCHEMA.md); privacy-preserving input: [INTAKE_TEMPLATE.md](references/INTAKE_TEMPLATE.md).
