# Job Hunt app: data layout

The app (`app/job-hunt-app.html`, published at https://claude.ai/artifact/FxPHKGLJFPqBe4FMdTjgRK)
keeps live data in its own database. Claude reads and writes it with the `ArtifactData` tool
(pass that URL). This file is the contract between the app and the cloud runs: keep both in step.

Split of responsibilities:
- **Repo** = the backend logic: engine code, skill instructions, config defaults, this schema.
- **App database** = live data: projects, jobs, decisions, applications, uploads, run requests.

All timestamps are ISO 8601 strings. Dates (`posted`, `follow_up`) are `YYYY-MM-DD`.

## projects/{project_id}
Written by the app. Runs read it.
```
name, brief (the user's own words), status: "active" | "paused" | "archived",
nightly: bool (8pm UK run), daily_cap: int (default 50; max jobs added per day),
filters: { locations[], radius_miles, remote: "any"|"remote"|"hybrid"|"onsite", max_office_days,
           pay_min, include_no_salary, leave_min_days, benefits[], industries[], exclude_industries[],
           company_sizes[], seniority[], contract[], posted_within_days, watch_companies[],
           block_companies[], must_words[], never_words[] },
sources: { indeed, reed, career_pages, alert_emails, chrome }   (bools; chrome never in nightly runs)
created_at, updated_at
```

## jobs/{job_id}
Written by runs. `job_id` = the engine's stable id (`model.make_id`: company + title + location), so
the same job from two sources or two projects is one document.
```
title, company, location, url, salary_text, posted, sources[], description (≤ 4000 chars),
project_ids[]   (append, never replace, when a job matches another project),
rank: 0-100     (stage 1 "match": how well it suits the profile + this brief),
rank_reason     (one honest line), gaps[],
checks: { "<Label>": {state: "pass"|"fail"|"unknown", note} }   (judged filters: Leave, Office, Benefits, Pay...)
found_at, run_id
```
Only jobs that clear hard filters are written. At most `daily_cap` new jobs per project per day,
highest rank first.

## decisions/{job_id}
Written by the app.
```
status: "interested" | "shortlisted" | "passed", stage: 1 | 2, project_id,
reasons[] (subset of: Pay, Industry, Role, Location, Company type, Seniority, Office days, Benefits, Company, Other),
note, at, job: {title, company, url, location}   (snapshot)
```
Runs skip any job that already has a decision. The weekly review reads `reasons` and `note`.

## deep/{job_id}
Written by runs (Phase 3) for jobs with status "interested".
```
fit: 0-100, reason, gaps[], intel (short text), intel_sources[], at
```

## applications/{job_id}
Created by the app on "Shortlist to apply"; edited by the user; runs may update `next_step`.
```
job_id, project_id, title, company, url, location,
status: Preparing | Ready to apply | Applied | Interviewing | Offer | Rejected | Withdrawn | Ghosted,
next_step, follow_up, notes, created_at, updated_at
```

## runs/{run_id}
Created by the app ("Run now": kind "manual") or the scheduler ("nightly").
```
project_id, kind, status: "requested" | "running" | "done" | "failed",
requested_at, started_at, finished_at, counts: {found, kept, added}, notes[] (one per skipped/failed source), error
```

## profile_docs/{doc_id}
Written by the app. The file itself is an uploaded asset: read it with the Artifact tool
(`action: "read"`, `path: <asset_id>`).
```
name, kind: CV | Cover letter | Annual review | Claude profile report | LinkedIn export | Other,
note, asset_id, content_type, size, uploaded_at, converted_from ("Word" when a .docx was converted to text)
```

## insights/{week_id}
Written by the weekly review (Phase 4). `week` = Monday's date.
```
week, summary (plain text), suggestions[]: {id, text, status: "proposed"|"accepted"|"rejected"}
```

## Housekeeping
The database holds at most 25,000 documents. Runs delete `jobs` older than 45 days that have no
decision, so the store doesn't fill up.
