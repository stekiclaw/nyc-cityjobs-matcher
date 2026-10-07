# Recommended Skill State

This file defines a logical state model. The host may store it in conversation state, memory, a database, or another persistence layer.

## Candidate profile

```json
{
  "candidate_profile": {
    "profile_version": 1,
    "anonymized": true,
    "target_role_families": [],
    "seniority": null,
    "years_experience": null,
    "operating_systems": [],
    "directory_identity": [],
    "endpoint_management": [],
    "deployment_imaging": [],
    "patching_update_management": [],
    "scripting_automation": [],
    "collaboration_productivity": [],
    "networking": [],
    "security": [],
    "virtualization_cloud": [],
    "hardware_support": [],
    "ticketing_itil": [],
    "environment_scale": null,
    "quantified_accomplishments": [],
    "certifications": [],
    "education": [],
    "civil_service_status": null,
    "salary_preferences": null,
    "location_preferences": null,
    "work_arrangement_preferences": null,
    "hard_exclusions": []
  }
}
```

Do not store employer names from the user's private work history in this normalized profile.

## Applied Jobs Ledger

```json
{
  "applied_jobs": [
    {
      "canonical_url": "https://...",
      "job_id": "...",
      "jid_slug": "...",
      "agency": "...",
      "business_title": "...",
      "civil_service_title": "...",
      "posting_date": "YYYY-MM-DD",
      "closing_date": "YYYY-MM-DD or null",
      "normalized_agency_title": "...",
      "repost_fingerprint": "short normalized description",
      "status": "applied"
    }
  ]
}
```

### Matching priority for exclusions

1. `job_id`
2. `jid_slug`
3. `canonical_url`
4. `normalized_agency_title`
5. `repost_fingerprint`

If only a title/agency is known because the user has not yet supplied the link, use a temporary in-session exclusion and ask for the official link before treating the record as durable.
