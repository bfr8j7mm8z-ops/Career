"""Merge, dedupe, filter and persist the morning queue."""
import json
import tomllib
from datetime import date, datetime, timedelta
from pathlib import Path

from . import linkcheck, model
from .sources import SourceUnavailable, adzuna, reed

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
QUEUE_DIR = DATA / "queue"
DECISIONS = DATA / "decisions.json"
SEEN = DATA / "seen.json"
CONFIG = ROOT / "config" / "jobhunt.toml"

API_SOURCES = {"adzuna": adzuna, "reed": reed}


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text())
    except FileNotFoundError:
        return default


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def load_config(path=CONFIG):
    with open(path, "rb") as f:
        return tomllib.load(f)


def run_api_sources(spec, config, sources=API_SOURCES):
    """Run every enabled API source. Returns (jobs, notes); never raises for a bad source."""
    jobs, notes = [], []
    for name, mod in sources.items():
        if not config.get("sources", {}).get(name, {}).get("enabled", False):
            continue
        try:
            found = mod.search(spec)
        except SourceUnavailable as e:
            notes.append(f"{name}: skipped ({e})")
            continue
        except Exception as e:  # network/API failure should be reported, not hidden
            notes.append(f"{name}: failed ({type(e).__name__}: {e})")
            continue
        for j in found:
            j["source"] = name
        notes.append(f"{name}: {len(found)} results")
        jobs.extend(found)
    return jobs, notes


def merge(jobs):
    """Dedupe by id or URL; keep the richest record and remember every source."""
    by_key, out = {}, []
    for raw in jobs:
        job = model.normalise(raw)
        job["sources"] = sorted(set(raw.get("sources") or []) | {job["source"]})
        existing = by_key.get(job["id"]) or (by_key.get(job["url"]) if job["url"] else None)
        if existing is None:
            out.append(job)
            by_key[job["id"]] = job
            if job["url"]:
                by_key[job["url"]] = job
            continue
        existing["sources"] = sorted(set(existing["sources"]) | set(job["sources"]))
        for field in ("description", "salary_text", "salary_min", "salary_max", "currency",
                      "posted", "remote", "fit", "fit_reason"):
            if existing.get(field) in (None, "") and job.get(field) not in (None, ""):
                existing[field] = job[field]
        if len(job["description"]) > len(existing["description"]):
            existing["description"] = job["description"]
    return out


def filter_jobs(jobs, max_age_days=None, decisions=None, seen=None, today=None):
    """Drop dead links, invalid records, stale posts, passed jobs and ones already shown."""
    today = today or date.today()
    decisions, seen = decisions or {}, seen or {}
    kept, dropped = [], {"dead": 0, "invalid": 0, "stale": 0, "decided": 0, "seen": 0}
    for job in jobs:
        if model.validate(job):
            dropped["invalid"] += 1
        elif job["link_status"] == "dead":
            dropped["dead"] += 1
        elif max_age_days and job["posted"] and (
                today - datetime.fromisoformat(job["posted"]).date()) > timedelta(days=max_age_days):
            dropped["stale"] += 1
        elif job["id"] in decisions:
            dropped["decided"] += 1
        elif job["id"] in seen:
            dropped["seen"] += 1
        else:
            kept.append(job)
    return kept, dropped


def sort_key(job):
    return (-(job["fit"] if job["fit"] is not None else -1), job["posted"] or "")


def build_queue(candidates, spec=None, notes=None, config=None, check_links=True,
                include_seen=False, checker=linkcheck.check, today=None):
    """candidates: loose job dicts from any source. Returns the queue document."""
    config = config or {}
    today = today or date.today()
    jobs = merge(candidates)
    if check_links and config.get("linkcheck", {}).get("enabled", True):
        linkcheck.check_all(jobs, checker=checker)
    decisions = load_json(DECISIONS, {}).get("decisions", {})
    seen = {} if include_seen else load_json(SEEN, {})
    max_age = (spec or {}).get("max_age_days") or config.get("search_defaults", {}).get("max_age_days")
    kept, dropped = filter_jobs(jobs, max_age, decisions, seen, today)
    kept.sort(key=sort_key)
    return {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "spec": spec or {},
        "notes": list(notes or []),
        "dropped": dropped,
        "jobs": kept,
    }


def write_queue(queue, today=None):
    today = today or date.today()
    save_json(QUEUE_DIR / f"{today.isoformat()}.json", queue)
    save_json(QUEUE_DIR / "latest.json", queue)
    seen = load_json(SEEN, {})
    for job in queue["jobs"]:
        seen.setdefault(job["id"], today.isoformat())
    save_json(SEEN, seen)


def apply_scores(queue, scores):
    """scores: {job_id: {fit, fit_reason, gaps}}; returns count updated."""
    n = 0
    for job in queue["jobs"]:
        s = scores.get(job["id"])
        if not s:
            continue
        fit = s.get("fit")
        job["fit"] = max(0, min(100, int(fit))) if isinstance(fit, (int, float)) else None
        job["fit_reason"] = s.get("fit_reason", "")
        job["gaps"] = list(s.get("gaps") or [])
        n += 1
    queue["jobs"].sort(key=sort_key)
    return n


def set_decision(job_id, status, note="", folder=None, job=None):
    if status not in model.DECISIONS:
        raise ValueError(f"status must be one of {model.DECISIONS}")
    doc = load_json(DECISIONS, {"decisions": {}})
    rec = doc["decisions"].get(job_id, {})
    rec.update(status=status, at=datetime.now().isoformat(timespec="seconds"))
    if note:
        rec["note"] = note
    if folder:
        rec["draft_folder"] = folder
    if job:  # snapshot so the decision stays readable after the job leaves the queue
        rec["job"] = {k: job.get(k) for k in ("title", "company", "location", "url", "fit", "fit_reason", "salary_text")}
    doc["decisions"][job_id] = rec
    save_json(DECISIONS, doc)
    return rec


def pending_drafts():
    """Interested jobs with no drafted application folder yet, joined to queue details."""
    decisions = load_json(DECISIONS, {}).get("decisions", {})
    jobs = {}
    for f in sorted(QUEUE_DIR.glob("2*.json")):
        for j in load_json(f, {}).get("jobs", []):
            jobs[j["id"]] = j
    return [dict(jobs.get(i) or d.get("job") or {"id": i}, id=i, decision=d) for i, d in decisions.items()
            if d.get("status") == "interested" and not d.get("draft_folder")]
