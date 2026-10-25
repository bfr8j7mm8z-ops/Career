# Sources

Cheapest and most reliable first. Each source is optional (see `config/jobhunt.toml`). Fewer
sources done well beats many done thinly: aggregators first, then targeted, then browser.

| Source | Kind | Setup | Notes |
|---|---|---|---|
| Indeed connector | Claude (MCP) | Connector enabled | `search_jobs` with natural-language query + location; `get_job_details` for the full description; `get_company_data` for company context. Don't call `get_resume` unless the user asks. |
| Adzuna | API (code) | Key; may cost ~£8/month, optional | Aggregates many boards. Set `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`. `country` in config/spec. |
| Reed | API (code) | Free key | UK only. Set `REED_API_KEY`, or store it as a Basic network secret for www.reed.co.uk (cloud). |
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

## Indeed connector: tested notes

- `search_jobs` needs `search`, `location` and `country_code` (e.g. `GB`); `job_type` optional. It
  returns about 10 jobs as markdown: title, job id (`JOBSEARCH_...`), company, location, posted date,
  type, compensation (usually N/A), and a `to.indeed.com` short link. **No description.**
- Call `get_job_details(job_id)` for the full text, but only for jobs worth scoring (relevant title,
  recent), not all of them. Pay often appears only in the description ("Pay: £35,000.00 per year"),
  so copy it into `salary_text` when found.
- The short link from details differs from the one in search for the same job. That's fine: jobs
  dedupe on company + title + location, not URL.
- Titles are loose: "account manager" also returned Account Executive (sales) roles. Run several
  specific queries rather than one broad one, and let fit scoring sort them.
- Dates come as "October 14, 2026" (the engine parses this). Old listings (months old) do appear
  and are dropped by `max_age_days`.
- `to.indeed.com` can't be reached from the cloud sandbox, so links show "unverified", not "live".
  That's expected, not a failure.
