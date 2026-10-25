import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from automations.jobhunt import model, pipeline
from automations.jobhunt.sources import SourceUnavailable, adzuna, reed

TODAY = date(2026, 10, 25)


class ModelTests(unittest.TestCase):
    def test_canonical_url_strips_tracking(self):
        self.assertEqual(model.canonical_url("HTTPS://X.com/job/1/?utm_source=a&id=7#top"),
                         "https://x.com/job/1?id=7")

    def test_parse_date(self):
        self.assertEqual(model.parse_date("2026-10-20T10:00:00Z"), "2026-10-20")
        self.assertIsNone(model.parse_date("soonish"))
        self.assertEqual(model.parse_date("today"), date.today().isoformat())

    def test_same_job_same_id_across_boards(self):
        a = model.normalise({"title": "Account Manager", "company": "Acme", "location": "London", "url": "https://a.com/1"})
        b = model.normalise({"title": "account manager", "company": "ACME ", "location": "london", "url": "https://b.com/9"})
        self.assertEqual(a["id"], b["id"])

    def test_validate(self):
        self.assertTrue(model.validate(model.normalise({"title": "x"})))
        ok = model.normalise({"title": "x", "company": "y", "url": "https://z.com/1"})
        self.assertEqual(model.validate(ok), [])


class SourceTests(unittest.TestCase):
    def test_adzuna_requires_keys(self):
        with mock.patch.dict(os.environ, {}, clear=True), self.assertRaises(SourceUnavailable):
            adzuna.search({"queries": [{"keywords": "x"}]})

    def test_adzuna_maps_results(self):
        payload = {"results": [{"title": "AM", "company": {"display_name": "Acme"},
                                "location": {"display_name": "London"}, "redirect_url": "https://a.com/1",
                                "created": "2026-10-24T00:00:00Z", "salary_min": 50000}]}
        with mock.patch.dict(os.environ, {"ADZUNA_APP_ID": "i", "ADZUNA_APP_KEY": "k"}):
            jobs = adzuna.search({"queries": [{"keywords": "am"}]}, fetch_json=lambda url: payload)
        self.assertEqual(jobs[0]["company"], "Acme")
        self.assertEqual(jobs[0]["posted"], "2026-10-24")

    def test_reed_without_key_sends_no_auth_and_maps_401(self):
        import urllib.error
        seen = {}
        def ok(url, headers=None):
            seen["h"] = headers
            return {"results": []}
        def denied(url, headers=None):
            raise urllib.error.HTTPError(url, 401, "no", {}, None)
        with mock.patch.dict(os.environ, {}, clear=True):
            reed.search({"queries": [{"keywords": "x"}]}, fetch_json=ok)
            self.assertEqual(seen["h"], {})
            with self.assertRaises(SourceUnavailable):
                reed.search({"queries": [{"keywords": "x"}]}, fetch_json=denied)

    def test_reed_params_cap_url_fallback_and_enrich(self):
        seen = []
        def fetch(url, headers=None):
            seen.append(url)
            if "/jobs/55" in url:
                return {"jobDescription": "<p>Full &amp; real</p><ul><li>One</li></ul>", "yearlyMinimumSalary": 60000,
                        "yearlyMaximumSalary": 70000, "currencyCode": "GBP", "salary": "£60,000 - £70,000 per annum", "externalUrl": "https://x.com/apply"}
            return {"results": [{"jobId": 55, "jobTitle": "AM", "employerName": "Acme", "locationName": "Leeds",
                                 "jobDescription": "snippet"}]}
        spec = {"results_per_source": 500, "queries": [{"keywords": "am", "fullTime": True, "distanceFromLocation": 20}]}
        jobs = reed.search(spec, fetch_json=fetch)
        self.assertIn("resultsToTake=100", seen[0])
        self.assertIn("fullTime=true", seen[0])
        self.assertIn("distanceFromLocation=20", seen[0])
        self.assertEqual(jobs[0]["url"], "https://www.reed.co.uk/jobs/55")
        merged = pipeline.merge([dict(j, source="reed") for j in jobs])
        note = reed.enrich(merged, fetch_json=fetch)
        self.assertEqual(merged[0]["description"], "Full & real One")
        self.assertEqual((merged[0]["salary_min"], merged[0]["currency"]), (60000, "GBP"))
        self.assertIn("external-apply", merged[0]["tags"])
        self.assertEqual(merged[0]["salary_text"], "£60,000 - £70,000 per annum")
        self.assertIn("1 of 1", note)
        # Reed echoing its own URL as externalUrl is not an external apply
        own = pipeline.merge([dict(jobs[0], source="reed")])
        reed.enrich(own, fetch_json=lambda url, headers=None: {"jobDescription": "x", "externalUrl": "https://www.reed.co.uk/jobs/am/55"})
        self.assertNotIn("external-apply", own[0]["tags"])

    def test_reed_uk_only_and_date(self):
        with mock.patch.dict(os.environ, {"REED_API_KEY": "k"}):
            with self.assertRaises(SourceUnavailable):
                reed.search({"country": "us", "queries": []})
            payload = {"results": [{"jobTitle": "AM", "employerName": "Acme", "locationName": "Leeds",
                                    "jobUrl": "https://r.com/1", "date": "24/10/2026"}]}
            jobs = reed.search({"queries": [{"keywords": "am"}]}, fetch_json=lambda url, headers=None: payload)
        self.assertEqual(jobs[0]["posted"], "2026-10-24")
        self.assertEqual(jobs[0]["title"], "AM")

    def test_run_api_sources_reports_not_raises(self):
        cfg = {"sources": {"adzuna": {"enabled": True}, "reed": {"enabled": True}}}
        with mock.patch.dict(os.environ, {}, clear=True), \
                mock.patch.object(reed, "search", side_effect=SourceUnavailable("no valid API key configured")):
            jobs, notes = pipeline.run_api_sources({"queries": []}, cfg)
        self.assertEqual(jobs, [])
        self.assertEqual(len(notes), 2)
        self.assertTrue(all("skipped" in n for n in notes))


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        patches = {"DATA": self.tmp, "QUEUE_DIR": self.tmp / "queue",
                   "DECISIONS": self.tmp / "decisions.json", "SEEN": self.tmp / "seen.json"}
        for k, v in patches.items():
            p = mock.patch.object(pipeline, k, v)
            p.start()
            self.addCleanup(p.stop)

    def job(self, n, **kw):
        base = {"title": f"Role {n}", "company": f"Co{n}", "location": "London",
                "url": f"https://x.com/{n}", "posted": "2026-10-24", "source": "t"}
        return {**base, **kw}

    def test_merge_dedupes_and_keeps_both_sources(self):
        a = self.job(1, source="adzuna", description="short")
        b = self.job(1, source="reed", url="https://other.com/9", description="a much longer description")
        merged = pipeline.merge([a, b])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["sources"], ["adzuna", "reed"])
        self.assertEqual(merged[0]["description"], "a much longer description")

    def test_filters(self):
        dead = self.job(1, link_status="dead")
        stale = self.job(2, posted="2026-08-01")
        bad = {"title": "no company"}
        fresh = self.job(3)
        q = pipeline.build_queue([dead, stale, bad, fresh], spec={"max_age_days": 14},
                                 check_links=False, today=TODAY)
        self.assertEqual([j["company"] for j in q["jobs"]], ["Co3"])
        self.assertEqual((q["dropped"]["dead"], q["dropped"]["stale"], q["dropped"]["invalid"]), (1, 1, 1))

    def test_linkcheck_marks_dead_but_not_blocked(self):
        statuses = {"https://x.com/1": "dead", "https://x.com/2": "unverified", "https://x.com/3": "live"}
        q = pipeline.build_queue([self.job(1), self.job(2), self.job(3)], check_links=True,
                                 checker=lambda u: statuses[u], today=TODAY, spec={"max_age_days": 14})
        self.assertEqual({j["company"]: j["link_status"] for j in q["jobs"]},
                         {"Co2": "unverified", "Co3": "live"})

    def test_seen_and_decisions_hidden_next_day(self):
        q1 = pipeline.build_queue([self.job(1), self.job(2)], check_links=False, today=TODAY)
        pipeline.write_queue(q1, today=TODAY)
        pipeline.set_decision(q1["jobs"][0]["id"], "pass")
        q2 = pipeline.build_queue([self.job(1), self.job(2), self.job(3)], check_links=False, today=TODAY)
        self.assertEqual([j["company"] for j in q2["jobs"]], ["Co3"])
        q3 = pipeline.build_queue([self.job(1), self.job(3)], check_links=False, include_seen=True, today=TODAY)
        self.assertEqual([j["company"] for j in q3["jobs"]], ["Co3"])  # decided jobs stay hidden even with include_seen

    def test_scores_sort_and_pending(self):
        q = pipeline.build_queue([self.job(1), self.job(2)], check_links=False, today=TODAY)
        ids = {j["company"]: j["id"] for j in q["jobs"]}
        n = pipeline.apply_scores(q, {ids["Co2"]: {"fit": 90, "fit_reason": "great", "gaps": ["x"]},
                                      ids["Co1"]: {"fit": 40, "fit_reason": "meh"}})
        self.assertEqual(n, 2)
        self.assertEqual([j["company"] for j in q["jobs"]], ["Co2", "Co1"])
        pipeline.write_queue(q, today=TODAY)
        pipeline.set_decision(ids["Co2"], "interested")
        self.assertEqual([j["company"] for j in pipeline.pending_drafts()], ["Co2"])
        pipeline.set_decision(ids["Co2"], "interested", folder="applications/2026-10-25-co2-role")
        self.assertEqual(pipeline.pending_drafts(), [])

    def test_decision_snapshot_survives_queue_turnover(self):
        pipeline.set_decision("zzz", "interested", job={"title": "T", "company": "C", "url": "https://x.com/z", "extra": 1})
        (p,) = pipeline.pending_drafts()
        self.assertEqual((p["id"], p["company"]), ("zzz", "C"))
        self.assertNotIn("extra", pipeline.load_json(pipeline.DECISIONS, {})["decisions"]["zzz"]["job"])

    def test_bad_decision_rejected(self):
        with self.assertRaises(ValueError):
            pipeline.set_decision("abc", "maybe-later")


if __name__ == "__main__":
    unittest.main()
