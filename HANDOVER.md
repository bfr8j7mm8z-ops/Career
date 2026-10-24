# Handover: moving this project to a personal Claude account

This repo was started from a work Claude account, but all storage is in your
**personal** GitHub repo (`bfr8j7mm8z-ops/Career`), so nothing here is lost or
left behind on the work account. This doc is the context needed to pick back
up on a personal Claude account with no loss of continuity.

## Why the move

Decision made: job-search activity (even just planning/automation) shouldn't
run on a work-provisioned Claude account, for conflict-of-interest/optics
reasons, independent of whether anyone is actively monitoring it. Storage was
never at risk (GitHub repo is personal), only the account doing the work.
Action: continue all future sessions from a personal Claude account, same
GitHub connection.

## What exists so far

Repo structure:
```
Career/
├── README.md
├── CLAUDE.md              — project instructions auto-loaded each session
├── HANDOVER.md            — this file
├── .gitignore
├── job-search-log.md      — application tracker (empty, ready to use)
├── cv/README.md           — master CV goes here (not yet created)
├── cover-letters/README.md
├── applications/README.md
└── automations/README.md  — sourcing plan notes (see below)
```

Not yet done:
- `cv/master-cv.md` — user said they'll upload CV content manually
- `cover-letters/template.md` — same, manual upload pending
- `profile/current-role.md` — role context (brands, stakeholders, deal types,
  content/decks produced) — to be written from what the user describes in
  chat directly, **not** pulled from Fathom/HubSpot/email connectors
- `profile/current-search-focus.md` — rolling, user-updated doc of what
  roles/criteria they're currently targeting; explicitly NOT a fixed one-time
  intake, gets overwritten as targeting shifts

## Data handling decisions (agreed with user — don't re-litigate these)

- Brand names the user works with professionally (e.g. clients of their
  employer), stakeholder names/titles (CEOs, CMOs), and deal context/notes
  are OK to store in this repo as the user's own working notes — this
  includes commercial detail like pricing discussed in deals, since it's
  already disclosed to the user and not being published anywhere else.
- NOT OK: any third party's personal data (beyond their professional
  role/title).
- Do not pull data directly from Fathom, HubSpot, Outlook, or other work
  connectors into this repo. Role context should come from what the user
  describes directly in chat, or from CVs/docs they manually upload.

## Job sourcing plan (researched, not yet built)

Scraping LinkedIn/Indeed/Glassdoor was ruled out — violates ToS, real risk of
account bans (LinkedIn especially enforces this aggressively). Plan instead:

- **Indeed** — official Indeed MCP server (beta, available via Claude
  connectors) — compliant, direct job search/description/apply-link access.
- **Adzuna** — free developer API key (developer.adzuna.com), aggregates
  multiple boards, filterable by keyword/location/salary/date, good UK/EU
  coverage.
- **Reed.co.uk** — free API key, UK-focused, poll-only (no webhooks/push).
- **LinkedIn** — no official public jobs API; unofficial/community MCP
  servers found are scraping-based or require handing over LinkedIn
  credentials/cookies to unaudited third-party code — avoid these (ban risk,
  credential exposure, ToS violation, unstable). Use LinkedIn's own native
  job-alert emails instead (sanctioned feature).
- **Glassdoor** — no public API either; same approach, use their native
  email job alerts.
- Separate follow-up task (user's, not yet started): tune the actual job
  alert searches on LinkedIn/Indeed/Glassdoor so the right roles start
  landing by email. Needs a personal inbox connected (not a work inbox).

## Revised process/loop (agreed structure)

1. **Role context** (`profile/current-role.md`) — from user's direct
   description + uploaded CVs, not connector pulls.
2. **Search focus** (`profile/current-search-focus.md`) — rolling, user
   updates it whenever targeting changes; not a fixed intake.
3. **Job sourcing** — Indeed MCP + Adzuna/Reed APIs + LinkedIn/Glassdoor
   email alerts (see above); manual paste-in as interim/fallback method.
4. **Morning review queue** — shortlist of sourced jobs (company, role, est.
   salary, fit vs. search focus + role context) for user to mark
   interested/pass.
5. **Drafting** — for "interested" jobs, generate tailored CV + cover letter
   from the masters + role context + that job posting.
6. **Human-in-the-loop submission** — user pastes the final materials into
   the actual application themselves; no auto-submission (also avoids
   anti-bot ToS issues on application portals).
7. **Tracking** — logged in `job-search-log.md`.

## Immediate next steps on the personal account

1. Confirm this repo is accessible from the personal Claude account (same
   GitHub connection).
2. User uploads CV + cover letter content.
3. User describes current role (brands, stakeholders, deal types, content
   produced) directly in chat → build `profile/current-role.md`.
4. Set up `profile/current-search-focus.md` once the user has a first pass
   at what they're targeting.
5. Pick a personal inbox to receive job alerts from, and start tuning
   LinkedIn/Indeed/Glassdoor alert searches (separate task, user-driven).
6. Register free API keys for Adzuna and Reed when ready to wire up sourcing.
7. Check availability of the official Indeed MCP connector on the personal
   account.
