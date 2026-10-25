---
name: job-hunt
description: >
  Natural-language job search and application drafting. Use when the user wants to find jobs,
  run or review a job search, shortlist roles, tailor a CV or cover letter to a posting, draft
  materials for jobs they marked "interested", check application status, or update their search
  focus. Works for anyone: personal context comes from profile/ and cv/, never hard-coded.
  Trigger on: find jobs, job search, look for roles, shortlist, tailor my CV, draft application,
  morning queue, application status, "I'm now looking for ...".
---

# job-hunt

Find roles from what the user *says* (natural language), score them against who they *are*
(profile + CV), put a shortlist in front of them, and only draft tailored materials for roles they
pick. The user never submits through you: they apply themselves.

**Where data lives:** the Job Hunt app's database (see `app/SCHEMA.md`) holds projects, jobs,
decisions, applications and profile uploads; read and write it with the ArtifactData tool. Each
project's brief + filters + sources replace the single search-focus file. Process `runs` with
status "requested" when asked to. Stage 1 (rank and triage, up to `daily_cap` jobs) is cheap; deep
review, company intel and drafting only happen for jobs the user marks Interested.

The repo holds the logic. The engine (`automations/jobhunt/`) does the deterministic
plumbing; you do the judgement. The morning page (`app/index.html`) is how the user reviews the
queue without opening a chat. Read `automations/README.md` for commands and `config/jobhunt.toml`
for which sources are on.

## 0. Check readiness (every run, silently)

Look for: `cv/master-cv.md`, `profile/current-role.md`, `profile/current-search-focus.md`,
`profile/target-companies.md` (optional), `config/jobhunt.toml`.

- Missing master CV or role context: say so in one line and offer to create them from
  `templates/` by asking the user (or by them pasting a CV). Don't invent content. You can still
  search, but scores will be marked as provisional and drafting is blocked until a CV exists.
- Never pull profile context from work connectors (see `HANDOVER.md`). Use what the user tells
  you or uploads.
- Template files with only placeholder text count as missing.

## 1. Turn the request into a search spec

The user talks naturally ("remote partnerships roles at fintechs, 70k+", "anything like the one I
applied to last week"). Combine that with `profile/current-search-focus.md`:

```json
{"country": "gb", "max_age_days": 14, "salary_min": 70000,
 "queries": [{"keywords": "partnerships manager fintech", "location": "London", "remote": false}]}
```

- Use several queries: exact titles plus adjacent titles the user would plausibly take.
- If the request changes their targeting, update `profile/current-search-focus.md` and say what
  changed in one line. Targeting is rolling; never make them re-do an intake.
- Ask a question only if you genuinely can't search without the answer. Otherwise assume and state
  the assumption.

## 2. Gather candidates

Respect `config/jobhunt.toml`; skip disabled sources. Details in `references/sources.md`.

1. **API sources** (Adzuna, Reed): `python3 -m automations.jobhunt search --spec scratch/spec.json --out scratch/candidates-api.json`. Missing keys are reported, not fatal.
2. **Indeed connector** (`mcp__Indeed__search_jobs`, `get_job_details`): write results to `scratch/candidates-indeed.json`.
3. **ATS career pages** via `site:` web searches, plus the user's `target-companies.md` watchlist.
4. **Personal Gmail alerts** (job-alert emails only; never anything else in the inbox).
5. **Chrome** (LinkedIn, Glassdoor): governed by `[sources.chrome] mode`. Follow `references/chrome.md` exactly.
6. **Pasted URLs/text** the user gives you.

Each Claude-gathered file is a JSON list of `{title, company, location, url, posted, description, salary_text, source}`. Keep real descriptions: scoring needs them.

## 3. Build the queue

```
python3 -m automations.jobhunt build scratch/candidates-*.json --spec scratch/spec.json \
    --note "chrome: off" --note "glassdoor: returned nothing"
```

This dedupes across boards, verifies links (blocked boards show "unverified", not dead), drops
stale, dead, already-shown and already-decided jobs, and writes `data/queue/latest.json`.
Pass a `--note` for every source that was skipped, empty or failed. Those show on the page.
Never hide a failure.

## 4. Score fit

Read `references/scoring.md`. For each job in `data/queue/latest.json`, judge fit from the master
CV + role context + search focus + the job description, then:

```
python3 -m automations.jobhunt score scratch/scores.json
```

where `scores.json` is `{"<id>": {"fit": 0-100, "fit_reason": "one honest line", "gaps": ["..."]}}`.
Score every job, including weak ones. The user filters by the page's min-fit slider.

## 5. Hand over

Tell the user, briefly: how many jobs, the top few with fit and reason, any sources that failed,
and how to review (`python3 -m automations.jobhunt serve`, or their hosted page). Don't dump the
whole table into chat unless asked. The page is the review surface.

## 6. Draft for "interested" jobs

`python3 -m automations.jobhunt pending` lists jobs the user marked interested that have no draft.
For each, follow `references/drafting.md`:

1. Create `applications/YYYY-MM-DD-company-role/` (CLAUDE.md convention) with `job-posting.md`,
   `cv.md`, `cover-letter.md`, `notes.md`.
2. Tailor from `cv/master-cv.md`. Trim and reorder, mirror the posting's real wording where it's
   true. **Never add a skill, tool, title or number the user doesn't have.** Gaps go in `notes.md`.
3. Run the human-tone pass (call the `the-humanizer` / `cv-qa-humaniser` skills if available).
4. `python3 -m automations.jobhunt decide <id> interested --folder applications/<folder>`
5. Add a row to `job-search-log.md` with status `Researching`.

## 7. Track outcomes

- When the user says they applied, set the log row to `Applied` with the date.
- With a personal Gmail connected, search only for messages from companies in the log
  (subjects like interview, unfortunately, offer, assessment), update statuses, and flag actions.
- Flag applications with no reply at 7-10 days (follow up) and 21+ days (likely ghosted).
- Look for patterns before changing strategy (see `references/scoring.md`, "Learning from outcomes").
  Say what you changed and why, in a line or two. If there's no clear pattern, say that.

## Scheduled / unattended runs

If no user is present: never ask questions or block. Use the stored spec/search focus, skip
Chrome (not available in the cloud and not to be run unattended), run steps 1-4, and put every
decision and skipped source into the queue notes. Do not draft in unattended runs unless
`pending` already lists interested jobs.

## Ground rules

- No auto-submitting, no creating accounts, no messaging employers or recruiters, no CAPTCHA work.
- Honesty over polish: gaps stated, no invented experience, no fabricated metrics.
- Output is short and finished. Hide mechanics, not failures.
- All data in this repo is personal and private. Don't quote it to external services beyond what
  a search needs, and don't reference employer-confidential information.
