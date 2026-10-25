# Claude in Chrome (optional source)

Config: `[sources.chrome] mode` = `off` | `ask` | `on`.

- `off`: never use it. Don't mention it beyond a note "chrome: off".
- `ask` (default): at the start of an interactive run, offer once ("Want me to also check
  LinkedIn in your browser? About N page loads.") and proceed only on yes.
- `on`: use it without asking, still interactive only.
- Never in scheduled/unattended runs, whatever the mode.

Load the `chrome-browser` skill first and follow it (new tab, site permissions, stop and ask on
login walls/CAPTCHAs).

## Why the limits

LinkedIn and Glassdoor terms prohibit automated collection and it is the user's real account.
Keep usage light, human-paced and read-only.

## Rules

1. Read-only: no applying, no connecting, no messaging, no saving/following, no profile edits.
2. Small: at most `max_pages_per_site` result pages per site per run, and only open an
   individual posting when the list snippet isn't enough to judge.
3. Present: the user is in the session. If a CAPTCHA, login prompt or "unusual activity" notice
   appears, stop that site, tell the user, and don't try to get around it.
4. Purpose: LinkedIn for discovery. Glassdoor mainly for salary ranges and reviews of
   already-shortlisted companies (add findings to the job's `notes.md`/description), not mass
   listing collection.
5. Record only what's needed (title, company, location, link, posted, salary, description) into
   `scratch/candidates-chrome.json`. Don't capture other people's personal data.
6. If it didn't work or was blocked, add a `--note` saying so.
