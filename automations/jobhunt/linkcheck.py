"""Verify job links are live. Boards that block bots (LinkedIn, Glassdoor) answer
403/999 to anything automated; that means "can't tell", not "dead"."""
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from .sources.http import UA

DEAD_MARKERS = ("no longer available", "job not found", "position has been filled",
                "this job has expired", "no longer accepting applications")


def check(url, timeout=15):
    """Return 'live', 'dead' or 'unverified'."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(200_000).decode("utf-8", "ignore").lower()
            return "dead" if any(m in body for m in DEAD_MARKERS) else "live"
    except urllib.error.HTTPError as e:
        return "dead" if e.code in (404, 410) else "unverified"
    except Exception:
        return "unverified"


def check_all(jobs, checker=check, workers=8):
    """Set link_status in place for jobs still marked unverified."""
    todo = [j for j in jobs if j.get("link_status") == "unverified" and j.get("url")]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for job, status in zip(todo, pool.map(lambda j: checker(j["url"]), todo)):
            job["link_status"] = status
    return jobs
