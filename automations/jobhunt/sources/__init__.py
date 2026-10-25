"""API-backed sources. Each exposes search(spec, fetch_json=None) -> list of job dicts.

A source raises SourceUnavailable (not a generic error) when it can't run, e.g.
missing API key, so the pipeline can report it plainly instead of failing.
"""


class SourceUnavailable(Exception):
    pass
