import copy
import datetime as dt
import tempfile
import unittest
from pathlib import Path
from scripts.cityjobs_state import official_url, normalize, match, add, load, save, evaluate, open_status

URL = "https://cityjobs.nyc.gov/job/sample-in-manhattan-jid-12345"
def job(**kwargs):
    return dict({"canonical_url": URL, "job_id": "9999", "agency": "Agency A",
                 "business_title": "Analyst", "civil_service_title": "Analyst",
                 "unit": "Operations", "duties": " ".join("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda".split()),
                 "qualifications": "one two three four five six seven eight nine",
                 "compensation": "90000"}, **kwargs)

class CityJobsTests(unittest.TestCase):
    def test_url_validation(self):
        for value in ("https://evil.com/job/a-jid-1", "https://cityjobs.nyc.gov.evil.com/job/a-jid-1",
                      "file:///etc/passwd", "https://cityjobs.nyc.gov@evil.com/job/a-jid-1"):
            with self.assertRaises(ValueError):
                official_url(value)
    def test_url_strip_tracking(self):
        self.assertEqual(official_url(URL+"?utm_source=x#hello"), URL)
    def test_jid(self):
        self.assertEqual(normalize(job())["jid_slug"], "12345")
    def test_exact_duplicate(self):
        self.assertEqual(match(job(), job())["decision"], "exclude")
    def test_same_title_distinct_job(self):
        a = job()
        b = {**a, "canonical_url": "https://cityjobs.nyc.gov/job/other-jid-45678",
             "job_id": "8888", "unit": "Engineering"}
        self.assertEqual(match(b,a)["decision"], "review")
    def test_different_agency(self):
        b = {**job(), "canonical_url": "https://cityjobs.nyc.gov/job/other-jid-45678",
             "job_id": "8888", "agency": "Agency B"}
        self.assertEqual(match(b,job())["decision"], "include")
    def test_confirmed_repost(self):
        b = {**job(), "canonical_url": "https://cityjobs.nyc.gov/job/other-jid-45678", "job_id": "8888"}
        self.assertEqual(match(b,job())["reason"], "high_confidence_repost")
    def test_closure_overrides_date(self):
        self.assertEqual(open_status({"explicit_status":"expired", "closing_date":"2099-01-01"}, dt.date(2026,10,10)), "closed")
    def test_date_alone_unknown(self):
        self.assertEqual(open_status({"closing_date":"2099-01-01"}, dt.date(2026,10,10)), "unknown")
    def test_persist_restart(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"state.json"
            state=load(path)
            self.assertEqual(add(state,job()),"added")
            save(path,state)
            fresh=load(path)
            self.assertEqual(add(fresh,job()),"updated")
            self.assertEqual(len(fresh["applied_jobs"]),1)
    def test_filter(self):
        state={"version":2,"applied_jobs":[normalize(job())]}
        b={**job(),"canonical_url":"https://cityjobs.nyc.gov/job/other-jid-45678","job_id":"8888","unit":"Other"}
        result=evaluate([job(),b],state,dt.date(2026,10,10))
        self.assertEqual(len(result["excluded_applied"]),1)
        self.assertEqual(len(result["possible_reposts"]),1)
    def test_reject_wrong_type(self):
        with self.assertRaises(ValueError): normalize([])
if __name__=="__main__": unittest.main()
