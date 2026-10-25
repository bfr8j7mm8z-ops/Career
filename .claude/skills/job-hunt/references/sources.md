# Sources

Cheapest and most reliable first. Each source is optional (see `config/jobhunt.toml`). Fewer
sources done well beats many done thinly: aggregators first, then targeted, then browser.

| Source | Kind | Setup | Notes |
|---|---|---|---|
| Indeed connector | Claude (MCP) | Connector enabled | `search_jobs` with natural-language query + location; `get_job_details` for the full description; `get_company_data` for company context. Don't call `get_resume` unless the user asks. |
| Adzuna | API (code) | Key; may cost ~£8/month, optional | Aggregates many boards. Set `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`. `country` in config/spec. |
| Reed | API (code) | Free key | UK only. Set `REED_API_KEY`. |
| ATS career pages | Claude (web search) | None | Queries like `site:boards.greenhouse.io "partnerships manager" London`, `site:jobs.lever.co ...`, `site:jobs.ashbyhq.com ...`, `site:apply.workable.com ...`. Good for startups/scale-ups. Also search the user's watchlist: `"<company>" careers "<role>"`. |
| Gmail alerts | Claude (MCP) | Personal Gmail | Read job-alert emails (LinkedIn/Indeed/Glassdoor alerts) from the last few days. Extract title, company, link. Nothing else in the inbox. |
| Chrome | Claude (browser) | Claude in Chrome | See `chrome.md`. Optional, off by default unless config says otherwise. |
| Manual | You | None | URLs or pasted postings from the user. |

## Getting API keys (for the user)

- **Adzuna** (optional; the user reports ~£8/month, I could not verify): sign up at developer.adzuna.com → create an app → copy *Application ID* and
  *Application Key*.
- **Reed**: sign in at reed.co.uk/developers → request the jobseeker API key.
- Put them in a local `.env` file (gitignored; see `.env.example`) and export them before
  running, or add them as secrets in the cloud environment that runs scheduled searches.
  Never commit keys.

## Adding a board later

If it has an API: add `automations/jobhunt/sources/<name>.py` with `search(spec, fetch_json=None)`
returning loose job dicts (raise `SourceUnavailable` when it can't run), register it in
`pipeline.API_SOURCES`, add a `[sources.<name>]` block to the config, and add a test using a
stubbed `fetch_json`. If it doesn't, add a row here and let Claude drive it.
