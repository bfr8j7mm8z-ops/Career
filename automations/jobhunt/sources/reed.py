"""Reed.co.uk API (UK only; free key: https://www.reed.co.uk/developers).

Auth: HTTP basic with the key as username and an empty password. Either set REED_API_KEY
(sent by us), or store the key as a Basic network secret for www.reed.co.uk in the cloud
environment, in which case the proxy adds the header and we send none.
"""
import base64
import html
import os
import re
import urllib.error
from datetime import datetime
from urllib.parse import urlencode

from . import SourceUnavailable
from .http import fetch_json as _fetch

NAME = "reed"
BASE = "https://www.reed.co.uk/api/1.0/search"
DETAILS = "https://www.reed.co.uk/api/1.0/jobs"
MAX_RESULTS = 100  # Reed caps resultsToTake at 100
FILTERS = ("distanceFromLocation", "permanent", "contract", "temp", "partTime", "fullTime",
           "graduate", "postedByDirectEmployer", "postedByRecruitmentAgency", "maximumSalary")


def _reed_date(text):
    try:
        return datetime.strptime(text, "%d/%m/%Y").date().isoformat()
    except (TypeError, ValueError):
        return None


def _auth():
    key = os.environ.get("REED_API_KEY")
    return {"Authorization": "Basic " + base64.b64encode(f"{key}:".encode()).decode()} if key else {}


def _get(url, fetch):
    try:
        return fetch(url, headers=_auth())
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise SourceUnavailable(f"Reed rejected the request ({e.code}): no valid API key configured") from e
        raise


def _job_url(r):
    return r.get("jobUrl") or (f"https://www.reed.co.uk/jobs/{r['jobId']}" if r.get("jobId") else None)


def _text(markup):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", markup or ""))).strip()


def search(spec, fetch_json=None):
    if spec.get("country", "gb") != "gb":
        raise SourceUnavailable("Reed only covers the UK")
    fetch = fetch_json or _fetch
    jobs = []
    for q in spec.get("queries", []):
        params = {"keywords": q.get("keywords", ""),
                  "resultsToTake": min(spec.get("results_per_source", 50), MAX_RESULTS)}
        for name in FILTERS:  # optional Reed filters, passed through from the query
            if q.get(name) is not None:
                params[name] = str(q[name]).lower() if isinstance(q[name], bool) else q[name]
        if q.get("location"):
            params["locationName"] = q["location"]
        if spec.get("salary_min"):
            params["minimumSalary"] = spec["salary_min"]
        data = _get(f"{BASE}?{urlencode(params)}", fetch)
        for r in data.get("results", []):
            jobs.append({
                "title": r.get("jobTitle"),
                "company": r.get("employerName"),
                "location": r.get("locationName"),
                "url": _job_url(r),
                "posted": _reed_date(r.get("date")),
                "description": r.get("jobDescription"),
                "salary_min": r.get("minimumSalary"),
                "salary_max": r.get("maximumSalary"),
                "currency": r.get("currency"),
                "remote": True if q.get("remote") else None,
            })
    return jobs


def enrich(jobs, fetch_json=None, limit=40):
    """Replace Reed's short search snippet with the full description from the details
    endpoint. Call after filtering so only jobs worth showing cost an API call.
    Returns a note string, or None if nothing to do."""
    fetch = fetch_json or _fetch
    todo = [j for j in jobs if "reed" in (j.get("sources") or [j.get("source")])
            and re.search(r"reed\.co\.uk/jobs/(?:[^/]+/)?(\d+)$", j.get("url") or "")][:limit]
    done = 0
    for job in todo:
        job_id = re.search(r"(\d+)$", job["url"]).group(1)
        try:
            d = _get(f"{DETAILS}/{job_id}", fetch)
        except SourceUnavailable as e:
            return f"reed details: skipped ({e})"
        except Exception:
            continue
        job["description"] = _text(d.get("jobDescription")) or job.get("description", "")
        if d.get("yearlyMinimumSalary") and not job.get("salary_min"):
            job["salary_min"], job["salary_max"] = d["yearlyMinimumSalary"], d.get("yearlyMaximumSalary")
            job["currency"] = d.get("currencyCode") or d.get("currency") or job.get("currency")
        if d.get("externalUrl"):
            job["tags"] = sorted(set(job.get("tags") or []) | {"external-apply"})
        done += 1
    return f"reed details: full descriptions for {done} of {len(todo)} jobs" if todo else None
