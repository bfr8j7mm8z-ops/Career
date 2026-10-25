"""Job record shape, normalisation and validation."""
import hashlib
import re
from datetime import date, datetime, timedelta
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

FIELDS = (
    "id", "title", "company", "location", "remote", "salary_text", "salary_min",
    "salary_max", "currency", "url", "source", "posted", "found", "description",
    "link_status", "fit", "fit_reason", "gaps", "tags",
)
LINK_STATUSES = ("live", "dead", "unverified")
DECISIONS = ("interested", "maybe", "pass")

_TRACKING = re.compile(r"^(utm_|fbclid$|gclid$|trk|refid$|tracking)", re.I)


def canonical_url(url):
    """Strip tracking params and fragments so the same job dedupes across feeds."""
    if not url:
        return ""
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query) if not _TRACKING.match(k)]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), ""))


def _slug(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def make_id(job):
    """Stable id: same company+title+location is the same job even across boards."""
    key = "|".join(_slug(job.get(k)) for k in ("company", "title", "location"))
    return hashlib.sha1(key.encode()).hexdigest()[:12]


def parse_date(value):
    """Accept ISO dates/datetimes and 'N days ago'; return ISO date string or None."""
    if not value:
        return None
    if isinstance(value, (date, datetime)):
        return value.date().isoformat() if isinstance(value, datetime) else value.isoformat()
    text = str(value).strip().lower()
    m = re.match(r"^(\d+)\+?\s*(day|days|d|hour|hours|h|week|weeks|w)\s*ago$", text)
    if m:
        n, unit = int(m.group(1)), m.group(2)[0]
        delta = {"d": timedelta(days=n), "h": timedelta(0), "w": timedelta(weeks=n)}[unit]
        return (date.today() - delta).isoformat()
    if text in ("today", "just posted"):
        return date.today().isoformat()
    if text == "yesterday":
        return (date.today() - timedelta(days=1)).isoformat()
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y", "%d/%m/%Y"):  # Indeed, UK styles
        try:
            return datetime.strptime(text.title(), fmt).date().isoformat()
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(text.replace("z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def normalise(raw, source=None):
    """Coerce a loosely-shaped dict from any source into the standard job record."""
    job = {k: raw.get(k) for k in FIELDS}
    job["source"] = source or raw.get("source") or "unknown"
    job["url"] = canonical_url(raw.get("url") or "")
    job["posted"] = parse_date(raw.get("posted"))
    job["found"] = parse_date(raw.get("found")) or date.today().isoformat()
    job["title"] = (raw.get("title") or "").strip()
    job["company"] = (raw.get("company") or "").strip()
    job["location"] = (raw.get("location") or "").strip()
    job["description"] = (raw.get("description") or "").strip()
    job["gaps"] = list(raw.get("gaps") or [])
    job["tags"] = list(raw.get("tags") or [])
    job["link_status"] = raw.get("link_status") if raw.get("link_status") in LINK_STATUSES else "unverified"
    fit = raw.get("fit")
    job["fit"] = max(0, min(100, int(fit))) if isinstance(fit, (int, float)) else None
    job["id"] = raw.get("id") or make_id(job)
    return job


def validate(job):
    """Return a list of problems; empty means the record is usable in the queue."""
    problems = []
    for field in ("title", "company", "url"):
        if not job.get(field):
            problems.append(f"missing {field}")
    if job.get("fit") is not None and not 0 <= job["fit"] <= 100:
        problems.append("fit out of range")
    if job.get("link_status") not in LINK_STATUSES:
        problems.append("bad link_status")
    return problems
