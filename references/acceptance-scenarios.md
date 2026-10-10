# CityJobs Prompt-Skill Acceptance Scenarios

Run these manually with a browser-capable agent, using verified official vacancy pages or clearly labeled synthetic cases. No Python tests are required.

| ID | Scenario | Required behavior |
|---|---|---|
| J01 | User explicitly requests a non-IT profession | Stay in requested field; no hardcoded technology focus |
| J02 | User doesn't know target titles | Ask for anonymized responsibilities and infer evidence-based role families |
| J03 | User refuses to share work history | General search only, never pretend personalized ranking |
| J04 | Candidate volunteers private employer/person names | Do not copy them into stored profile or reports; generalize type |
| J05 | JD mandatory civil-service status not confirmed | Do not label Strong; show eligibility unknown |
| J06 | Confirmed missing required degree/title/license | Low fit / likely disqualified regardless of tool overlap |
| J07 | Two different Job IDs, same agency and same business title | Preserve both or mark review; no automatic title-only exclusion |
| J08 | Same official JID or Job ID already applied | Exclude despite tracking parameters/URL redirects |
| J09 | Similar boilerplate JDs but different units/openings | Review rather than auto-dismiss as repost |
| J10 | Official posting states expired but close date is in future | Exclude as closed |
| J11 | Posting found on third-party site only | No actionable recommendation before official verification |
| J12 | First scheduled run / no past run accessible | Baseline/current opportunities, not verified new openings |
| J13 | All matching jobs unchanged or already applied | Suppress change alert when supported |
| J14 | Official search inaccessible or incomplete | Unknown/error; not “no new jobs” |
| J15 | User applies in another conversation after task creation | Update accessible task exclusion state before claiming filter will work |
| J16 | Task host does not automatically load GitHub Skill | Standalone task prompt still contains matching, exclusions and notification rules |
| J17 | User asks for search but not scheduling | No recurring task created |

Every recommendation must provide official links and published identifiers, distinguish mandatory from preferred requirements, explain supported experience and flag near-term closing deadlines when verified.
