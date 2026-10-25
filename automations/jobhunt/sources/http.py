"""Tiny JSON-over-HTTP helper (stdlib only) so sources are easy to stub in tests."""
import json
import urllib.request

UA = "career-jobhunt/0.1 (personal job search tool)"


def fetch_json(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)
