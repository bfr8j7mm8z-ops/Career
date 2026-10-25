"""Reed.co.uk API (UK only; free key: https://www.reed.co.uk/developers).

Env: REED_API_KEY (sent as the basic-auth username, empty password).
"""
import base64
import os
from datetime import datetime
from urllib.parse import urlencode

from . import SourceUnavailable
from .http import fetch_json as _fetch

NAME = "reed"
BASE = "https://www.reed.co.uk/api/1.0/search"


def _reed_date(text):
    try:
        return datetime.strptime(text, "%d/%m/%Y").date().isoformat()
    except (TypeError, ValueError):
        return None


def search(spec, fetch_json=None):
    key = os.environ.get("REED_API_KEY")
    if not key:
        raise SourceUnavailable("REED_API_KEY not set")
    if spec.get("country", "gb") != "gb":
        raise SourceUnavailable("Reed only covers the UK")
    fetch = fetch_json or _fetch
    auth = {"Authorization": "Basic " + base64.b64encode(f"{key}:".encode()).decode()}
    jobs = []
    for q in spec.get("queries", []):
        params = {"keywords": q.get("keywords", ""), "resultsToTake": spec.get("results_per_source", 50)}
        if q.get("location"):
            params["locationName"] = q["location"]
        if spec.get("salary_min"):
            params["minimumSalary"] = spec["salary_min"]
        data = fetch(f"{BASE}?{urlencode(params)}", headers=auth)
        for r in data.get("results", []):
            jobs.append({
                "title": r.get("jobTitle"),
                "company": r.get("employerName"),
                "location": r.get("locationName"),
                "url": r.get("jobUrl"),
                "posted": _reed_date(r.get("date")),
                "description": r.get("jobDescription"),
                "salary_min": r.get("minimumSalary"),
                "salary_max": r.get("maximumSalary"),
                "currency": r.get("currency"),
                "remote": True if q.get("remote") else None,
            })
    return jobs
