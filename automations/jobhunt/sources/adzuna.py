"""Adzuna aggregator API (free key: https://developer.adzuna.com).

Env: ADZUNA_APP_ID, ADZUNA_APP_KEY. Covers many countries via spec["country"]
(gb, us, au, ca, de, fr, nl, ...). Aggregates several boards in one call, which
keeps per-board effort low.
"""
import os
from urllib.parse import urlencode

from . import SourceUnavailable
from .http import fetch_json as _fetch

NAME = "adzuna"
BASE = "https://api.adzuna.com/v1/api/jobs"


def search(spec, fetch_json=None):
    app_id, app_key = os.environ.get("ADZUNA_APP_ID"), os.environ.get("ADZUNA_APP_KEY")
    if not (app_id and app_key):
        raise SourceUnavailable("ADZUNA_APP_ID / ADZUNA_APP_KEY not set")
    fetch = fetch_json or _fetch
    country = spec.get("country", "gb")
    jobs = []
    for q in spec.get("queries", []):
        params = {
            "app_id": app_id, "app_key": app_key,
            "results_per_page": spec.get("results_per_source", 50),
            "what": q.get("keywords", ""),
            "max_days_old": spec.get("max_age_days", 14),
            "content-type": "application/json",
        }
        if q.get("location"):
            params["where"] = q["location"]
        if spec.get("salary_min"):
            params["salary_min"] = spec["salary_min"]
        data = fetch(f"{BASE}/{country}/search/1?{urlencode(params)}")
        for r in data.get("results", []):
            jobs.append({
                "title": r.get("title"),
                "company": (r.get("company") or {}).get("display_name"),
                "location": (r.get("location") or {}).get("display_name"),
                "url": r.get("redirect_url"),
                "posted": (r.get("created") or "")[:10] or None,
                "description": r.get("description"),
                "salary_min": r.get("salary_min"),
                "salary_max": r.get("salary_max"),
                "remote": True if q.get("remote") else None,
            })
    return jobs
