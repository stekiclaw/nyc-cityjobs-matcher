---
name: nyc-cityjobs-matcher
description: Use when searching NYC CityJobs for high-fit IT roles. Builds matching from a privacy-preserving, anonymized work-experience profile and excludes previously applied jobs using user-supplied official job-posting links.
---

# NYC CityJobs Matcher

## Purpose

Find newly posted or still-open, high-fit NYC CityJobs roles in Windows systems administration, help desk/service desk, desktop support, endpoint support, mobile-device management, infrastructure support, and cyber security analyst work.

This skill is intentionally generic. It must not assume or import any specific person's work history, employer, application history, name, or prior conversations unless the user explicitly supplies that information for this skill.

## Non-negotiable privacy rule

Before performing a personalized job match, obtain an anonymized candidate profile.

The profile may contain:
- job functions and role level;
- years of experience;
- technologies, platforms, and tools;
- environment size or support scope;
- responsibilities;
- measurable accomplishments;
- certifications and education;
- civil-service title/list/exam eligibility, if the user chooses to provide it;
- salary, location, schedule, commute, hybrid/onsite, or other job preferences.

The profile must not require:
- employer/company/agency names from the user's work history;
- coworker, manager, client, or other person names;
- personal contact information;
- exact street addresses;
- employee IDs, case IDs, ticket IDs, asset tags, or account numbers;
- confidential hostnames, internal domains, private URLs, credentials, keys, or secrets.

If the user provides identifying employer or person names unnecessarily, do not repeat them in the normalized profile. Generalize them, for example:
- "NYC public-sector agency"
- "large enterprise"
- "mid-size nonprofit"
- "managed-service provider"

Public employer/agency names appearing in NYC job postings are allowed in search results and the application-exclusion ledger because they describe the public vacancy, not the user's private work history.

## Intake gate

At the start of a personalized search, check whether a usable anonymized candidate profile is already available in the current skill context.

If no usable profile is available, ask the user to provide one before ranking jobs. Use a compact request similar to:

> To match jobs accurately, please send an anonymized work-history summary. Do not include company/agency names or people's names. Include your role types, approximate years of experience, main technologies/tools, responsibilities, environment size, measurable accomplishments, certifications/education, civil-service eligibility if relevant, and any salary/location/work-arrangement preferences.

Do not require a resume. A short bullet summary is sufficient.

If the user declines to provide a profile, the skill may perform a generic NYC CityJobs search, but it must clearly label the output as a general search rather than a personalized fit ranking.

See `references/INTAKE_TEMPLATE.md` for the preferred structured intake.

## Candidate profile normalization

Convert the user's anonymized input into a concise internal matching profile with these fields when available:

- target_role_families
- seniority
- years_experience
- operating_systems
- directory_identity
- endpoint_management
- deployment_imaging
- patching_update_management
- scripting_automation
- collaboration_productivity
- networking
- security
- virtualization_cloud
- hardware_support
- ticketing_itil
- environment_scale
- quantified_accomplishments
- certifications
- education
- civil_service_status
- salary_preferences
- location_preferences
- work_arrangement_preferences
- hard_exclusions

Never invent missing skills or experience.

## Applied-job exclusion rule

Maintain an Applied Jobs Ledger for jobs the user has already applied to.

### When the user says they applied

If the user says they applied to a job, submitted an application, completed an application, or wants a job excluded, and an official posting link is not already present in the same message or immediately available in context, actively request the official job-posting URL.

Use a short request such as:

> Please send the official NYC CityJobs posting link for that application. I’ll use its Job ID/JID and posting details to exclude the same job and materially identical reposts from future results.

Do not ask for application confirmation emails, applicant IDs, names, or other personal information when the posting URL is sufficient.

### After receiving the link

Extract and store, when available:
- canonical official posting URL;
- official Job ID;
- JID/slug from the CityJobs URL;
- agency;
- exact business/job title;
- civil-service title;
- posting date;
- closing date;
- normalized agency + title key;
- a brief fingerprint of the vacancy sufficient to recognize materially identical reposts.

Treat the job as applied even if the posting later closes or the URL changes.

If the supplied URL is inaccessible but clearly identifies the official NYC posting, retain the URL and any extractable identifiers. If the user names an applied job without a link, temporarily suppress that exact title/agency from recommendations for the current interaction and continue requesting the official link for durable deduplication.

See `references/STATE_SCHEMA.md` for the recommended ledger structure.

## Deduplication rules

Exclude an applied job when any strong identifier matches:
1. official Job ID;
2. CityJobs JID/URL slug;
3. canonical official posting URL;
4. agency + materially identical business title;
5. materially identical reposting with substantially the same duties, civil-service title, qualifications, unit, and compensation even if a new URL or JID is used.

For borderline reposts, explain the ambiguity instead of silently excluding a potentially distinct vacancy.

For non-applied search results, deduplicate the result set using the same keys before ranking.

## Search scope

Search official NYC CityJobs listings for newly posted or still-open roles related to:
- Windows systems administration;
- systems/infrastructure support;
- help desk/service desk;
- desktop support;
- endpoint engineering/support;
- mobile-device management / UEM / MDM;
- Microsoft 365 support;
- identity / Active Directory support;
- endpoint security;
- cyber security analyst work.

Prioritize role concepts such as:
- Senior Systems Administrator
- Windows Support Engineer
- Senior Helpdesk Technician
- Service Desk Technician
- Desktop Support Engineer
- Endpoint/MDM Engineer
- Systems Specialist
- Infrastructure Support Engineer
- Cyber Security Analyst

Do not limit results to exact title matches; evaluate duties and requirements.

## Source rules

Use current web research for every search run.

Prefer official NYC sources as the source of truth. Third-party pages may be used for discovery only; verify the vacancy against an official NYC posting before recommending it.

Verify that the job is still open when possible. Do not present a closed or expired posting as actionable.

## Matching framework

Rank only jobs that are not in the Applied Jobs Ledger.

Assess fit using the anonymized candidate profile. Weight:
- overlap with required technical skills;
- overlap with day-to-day duties;
- seniority and years-of-experience alignment;
- scale and complexity of prior environment;
- transferable accomplishments;
- education/certification requirements;
- civil-service title, exam, permanent-title, or hiring-pool eligibility;
- salary and work-arrangement preferences when supplied;
- likely disqualifiers.

Suggested qualitative buckets:
- Strong match
- Good match
- Stretch match
- Low fit / likely disqualified

Do not inflate fit because of keyword overlap when a mandatory eligibility requirement is missing.

## Technical keywords to inspect

Pay particular attention to requirements involving:
- Windows desktop/server administration
- Active Directory / Entra ID
- Group Policy
- Microsoft Endpoint Configuration Manager / SCCM
- Intune / Workspace ONE / other MDM or UEM
- WSUS
- MDT / Autopilot / OS deployment
- PowerShell
- WinRM / remote administration
- endpoint troubleshooting
- imaging and provisioning
- patch management
- Microsoft 365
- Teams and collaboration support
- hardware/software troubleshooting
- endpoint security
- identity and access management
- networking fundamentals
- vulnerability management
- SIEM / EDR / security operations when relevant

## Required output for each recommended match

For every remaining match, include:
- exact job title;
- agency;
- official Job ID;
- official JID/slug when available;
- location or work arrangement when listed;
- salary range;
- posting date;
- closing date;
- civil-service title;
- minimum qualification requirements;
- exam, permanent-title, hiring-pool, or civil-service eligibility requirements;
- direct official application link;
- fit bucket;
- concise explanation of why it fits or does not fit the anonymized profile;
- meaningful gaps, preferred qualifications, and likely disqualifiers.

Flag deadlines within 14 calendar days of the search date.

## Resume-tailoring notes

For each Strong match and useful Good match, provide 3–5 concrete resume-tailoring notes.

Only use experience contained in the anonymized candidate profile. Never invent qualifications, certifications, accomplishments, employer names, projects, or metrics.

Tailoring should focus on:
- exact relevant ATS keywords from the posting;
- which existing skills/accomplishments should be moved higher;
- how to reframe truthful experience to mirror the job's responsibilities;
- which quantified accomplishments are most relevant;
- which less-relevant content can be deemphasized.

Do not write false claims merely to satisfy a requirement.

## Interaction after recommendations

When the user later says they applied to one of the recommended roles:
1. check whether the official posting URL is present;
2. if missing, request it;
3. parse identifiers and add the job to the Applied Jobs Ledger;
4. confirm that the vacancy and materially identical reposts will be excluded from subsequent searches.

If the user shares multiple applied-job links at once, process them in one batch.

## Empty-result behavior

If no meaningful high-fit, not-yet-applied role is found:
- in an interactive/manual search, state briefly that no meaningful new high-fit un-applied role was found;
- in a scheduled/notification workflow that supports silent runs, do not notify unless there is a meaningful new match.

## Safety and accuracy

- Never fabricate a job, Job ID, salary, deadline, or qualification.
- Distinguish required qualifications from preferred qualifications.
- Treat civil-service/title eligibility as a potential gating condition, not a minor gap.
- Do not infer that the user holds a certification, degree, title, exam status, or permanent status unless provided.
- Do not expose or request unnecessary personally identifying employment information.
- Do not use the user's private work-history employer names as matching features even if they are volunteered; normalize them to employer type unless the user explicitly asks otherwise.
