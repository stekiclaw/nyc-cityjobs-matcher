# NYC CityJobs Matcher Skill

A reusable, privacy-preserving skill for matching NYC CityJobs IT vacancies against an anonymized candidate profile.

## Core behavior

1. On first personalized use, asks the user for anonymized work experience.
2. Explicitly tells the user not to provide employer/company/agency names from their own work history or people's names.
3. Searches current official NYC CityJobs listings and ranks fit using skills, responsibilities, scale, achievements, credentials, civil-service eligibility, and preferences.
4. When the user says they applied to a job, asks for the official job-posting URL if it was not supplied.
5. Extracts Job ID/JID and posting metadata from the link and adds the vacancy to an Applied Jobs Ledger.
6. Excludes the applied vacancy and materially identical reposts from future recommendations.
7. Provides truthful resume-tailoring notes without inventing experience.

## Package structure

- `SKILL.md` — main skill instructions
- `references/INTAKE_TEMPLATE.md` — privacy-preserving experience intake
- `references/STATE_SCHEMA.md` — logical schema for the anonymized profile and applied-job ledger

## Important implementation note

The skill defines the behavior and state model, but actual persistence depends on the host. If the host supports skill/user state, store the normalized profile and Applied Jobs Ledger there. If it does not, maintain them in the active conversation and ask the user to provide/export the ledger when moving to a new environment.
