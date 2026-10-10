#!/usr/bin/env python3
"""Deterministic, offline state and deduplication for official NYC CityJobs posts.

An Agent must fetch and verify official postings separately. This tool does NOT
scrape listings, infer qualifications, or persist private resume data.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import urlsplit, urlunsplit

VERSION = 2
FIELDS = ("canonical_url", "job_id", "jid_slug", "agency", "business_title",
          "civil_service_title", "unit", "duties", "qualifications", "compensation",
          "posting_date", "closing_date", "explicit_status", "apply_available")
WORD = re.compile(r"[a-z0-9]+")
JID = re.compile(r"(?:^|-)jid-(\d+)(?:$|[-/])", re.IGNORECASE)
CLOSED = ("expired", "closed", "filled", "cancelled", "canceled")
DEFAULT_PATH = Path.home() / ".local" / "share" / "nyc-cityjobs-matcher" / "state.json"


def official_url(url):
    """Reject third-party/untrusted URLs and normalize an official job URL."""
    parts = urlsplit(str(url).strip())
    if parts.scheme.lower() not in ("http", "https") or (parts.hostname or "").lower() != "cityjobs.nyc.gov":
        raise ValueError("An official https://cityjobs.nyc.gov job posting URL is required")
    if parts.username or parts.password or parts.port or not parts.path.startswith("/job/"):
        raise ValueError("Only official CityJobs /job/ links are supported")
    return urlunsplit(("https", "cityjobs.nyc.gov", parts.path.rstrip("/"), "", ""))


def text(value):
    return " ".join(str(value or "").casefold().split())


def tokens(value):
    return set(WORD.findall(text(value)))


def jid_from_url(url):
    match = JID.search(urlsplit(url).path)
    return match.group(1) if match else ""


def normalize(record):
    if not isinstance(record, dict):
        raise ValueError("Job record must be an object")
    url = record.get("canonical_url") or record.get("url") or ""
    if not url:
        raise ValueError("Missing official posting URL")
    url = official_url(url)
    cleaned = {field: record.get(field) for field in FIELDS}
    cleaned["canonical_url"] = url
    for field in FIELDS:
        if field not in ("apply_available", "canonical_url"):
            cleaned[field] = str(cleaned.get(field) or "").strip()
    cleaned["jid_slug"] = jid_from_url(url) or cleaned["jid_slug"]
    if cleaned.get("apply_available") not in (True, False, None):
        raise ValueError("apply_available must be boolean or null")
    cleaned["status"] = "applied"
    return cleaned


def load(path):
    if not path.exists():
        return {"version": VERSION, "applied_jobs": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("applied_jobs", []), list):
        raise ValueError("Invalid ledger JSON")
    if data.get("version", 1) not in (1, VERSION):
        raise ValueError("Unsupported state version")
    # v1 migrations keep applied records but never infer missing identifying evidence.
    records = []
    for entry in data.get("applied_jobs", []):
        obj = dict(entry)
        if "canonical_url" not in obj and obj.get("url"):
            obj["canonical_url"] = obj["url"]
        records.append(normalize(obj))
    return {"version": VERSION, "applied_jobs": records}


def save(path, state):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name == "posix":
        os.chmod(path.parent, 0o700)
    fd, tmp = tempfile.mkstemp(prefix=".state-", dir=path.parent)
    try:
        if os.name == "posix":
            os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(state, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def overlap(a, b):
    aa, bb = tokens(a), tokens(b)
    return len(aa & bb) / len(aa | bb) if aa and bb else 0.0


def match(candidate, applied):
    """Return exclude / review / include. Same agency + title alone is NEVER exclusion."""
    a, b = normalize(candidate), normalize(applied)
    for field in ("job_id", "jid_slug", "canonical_url"):
        if a[field] and b[field] and text(a[field]) == text(b[field]):
            return {"decision": "exclude", "reason": "same_" + field}
    if not a["agency"] or not b["agency"] or text(a["agency"]) != text(b["agency"]):
        return {"decision": "include", "reason": "different_agency_or_unknown"}
    if not a["business_title"] or text(a["business_title"]) != text(b["business_title"]):
        return {"decision": "include", "reason": "different_title_or_unknown"}
    # Avoid treating multiple openings with the same agency/title as one vacancy.
    civil_match = a["civil_service_title"] and b["civil_service_title"] and text(a["civil_service_title"]) == text(b["civil_service_title"])
    unit_match = a["unit"] and b["unit"] and text(a["unit"]) == text(b["unit"])
    pay_conflict = a["compensation"] and b["compensation"] and text(a["compensation"]) != text(b["compensation"])
    # Require exact named unit plus distinctive corroborating JD details.
    if civil_match and unit_match and not pay_conflict and (
        len(tokens(a["duties"])) >= 9 and len(tokens(b["duties"])) >= 9
        and len(tokens(a["qualifications"])) >= 7 and len(tokens(b["qualifications"])) >= 7
        and overlap(a["duties"], b["duties"]) >= 0.88
        and overlap(a["qualifications"], b["qualifications"]) >= 0.88
    ):
        return {"decision": "exclude", "reason": "high_confidence_repost"}
    return {"decision": "review", "reason": "same_agency_title_insufficient_evidence"}


def open_status(record, today):
    status = text(record.get("explicit_status"))
    if any(re.search(r"\b" + word + r"\b", status) for word in CLOSED):
        return "closed"
    if status in ("open", "accepting applications"):
        return "open"  # explicit official opening overrides a stale date
    until = record.get("closing_date")
    if until:
        try:
            if dt.date.fromisoformat(str(until)[:10]) < today:
                return "closed"
        except ValueError:
            pass
    return "unknown"  # date alone cannot prove an application is open


def evaluate(records, state, today):
    retained, excluded, review, closed, duplicates = [], [], [], [], []
    seen = []
    for raw in records:
        post = normalize(raw)
        posting = dict(post)
        posting.pop("status")
        posting["open_status"] = open_status(posting, today)
        if posting["open_status"] == "closed":
            closed.append(posting)
            continue
        hits = [match(posting, entry) for entry in state["applied_jobs"]]
        if any(hit["decision"] == "exclude" for hit in hits):
            posting["exclusion_reason"] = next(h["reason"] for h in hits if h["decision"] == "exclude")
            excluded.append(posting)
            continue
        if any(match(posting, entry)["decision"] == "exclude" for entry in seen):
            duplicates.append(posting)
            continue
        seen.append(posting)
        if any(hit["decision"] == "review" for hit in hits):
            posting["review_reason"] = "possible_repost_not_auto_excluded"
            review.append(posting)
        else:
            retained.append(posting)
    return {"candidates": retained, "possible_reposts": review,
            "excluded_applied": excluded, "closed": closed,
            "duplicate_results": duplicates}


def add(state, record):
    post = normalize(record)
    matches = [(i, match(post, old)) for i, old in enumerate(state["applied_jobs"])]
    exact = next((i for i, result in matches if result["reason"] in
                  ("same_job_id", "same_jid_slug", "same_canonical_url")), None)
    if exact is not None:
        # Merge nonempty new official metadata into an existing entry.
        current = state["applied_jobs"][exact]
        for field in FIELDS:
            if post.get(field) not in ("", None):
                current[field] = post[field]
        return "updated"
    state["applied_jobs"].append(post)
    return "added"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--state", type=Path, default=DEFAULT_PATH)
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("add", help="Store one verified official job record")
    a.add_argument("--record", type=Path, required=True, help="JSON object with official URL and known fields")
    f = sub.add_parser("filter", help="Filter verified official job records; no network calls")
    f.add_argument("--input", type=Path, required=True, help="JSON list of official job records")
    f.add_argument("--as-of", help="YYYY-MM-DD, defaults to today")
    sub.add_parser("list", help="List stored applied job records")
    args = p.parse_args()
    if args.command == "add":
        # Only add requires a write; a failed read/parse must never destroy state.
        state = load(args.state)
        record = json.loads(args.record.read_text(encoding="utf-8"))
        action = add(state, record)
        save(args.state, state)
        print(json.dumps({"action": action, "count": len(state["applied_jobs"]), "state": str(args.state)}))
    elif args.command == "filter":
        state = load(args.state)
        today = dt.date.fromisoformat(args.as_of) if args.as_of else dt.date.today()
        records = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError("--input must be a JSON list")
        print(json.dumps(evaluate(records, state, today), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(load(args.state), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
