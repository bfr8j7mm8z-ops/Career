# Session handover: what was done on branch `claude/blissful-euler-7geqpz`

Paste the prompt at the bottom into any other Claude session working on this project.

## State (as of 27 Oct 2026)
- Repo: `bfr8j7mm8z-ops/Career`. Work is on branch `claude/blissful-euler-7geqpz` (pushed, not merged to main, no PR).
- Read `HANDOVER.md` and `CLAUDE.md` first. Their data-handling rules still apply: no pulls from work connectors; no third-party personal data.
- Built in this session (all in `cv/`):
  - `master-cv.md`: current CV, based on the Jun 2026 GoCardless CSAM version.
  - `evidence-bank.md`: every claim and metric from 11 past CVs, grouped by role, with a "Canonical figures" section (latest CV wins) and Schneider Electric kept as optional context.
  - `cv-variants-notes.md`: how past CVs were angled per target role, plus Harry's style notes.
- Google Drive: folder `Career` (id `1yRg0lQ2JkNlWP7dCTTIi9nUEUip6dYwW`) now has subfolders `Applications` (`1nF5mc-hDJ-f8cLd5qiQ6WA23L3F_6ZZu`) and `Master CV` (`1uhGoJTSvja2Raq3xewjICfN-gIABIk8u`). Both are empty. Finished .docx/PDF files go there; the repo holds the Markdown source.
- Old CVs were read from the Drive folder `CVs`. `Anna Stenning 2025 Resume-3` there is someone else's resume and was deliberately excluded.

## Not built yet
- No blueprint or app exists in the repo. `automations/README.md` still says nothing is built.
- Job sourcing (Indeed MCP, Adzuna, Reed, alert emails), morning review queue, auto-drafting, `profile/current-role.md`, `profile/current-search-focus.md`, cover-letter template.
- Waiting on Harry: context covering the gap between the last CV (Jun 2026) and newer roles/experience. Add it to the evidence bank, then refresh the master CV.
- Open, only if needed: exact promotion dates at Fospha; exact Schneider dates; whether the dropped tool metrics (85%, 25h/month, ~40%) are valid.

## Prompt to paste into the other session
> I'm continuing a career-management project in the GitHub repo `bfr8j7mm8z-ops/Career`. Work from another session is on branch `claude/blissful-euler-7geqpz`. Please fetch that branch and read `SESSION-HANDOVER.md`, `HANDOVER.md`, `CLAUDE.md` and everything in `cv/` before doing anything. Treat `cv/evidence-bank.md` (especially "Canonical figures") as the source of truth for CV claims, and don't re-litigate the data-handling decisions in `HANDOVER.md`. Google Drive folder `Career` (id 1yRg0lQ2JkNlWP7dCTTIi9nUEUip6dYwW) is where finished documents go. I've been building a blueprint/app in a different session: here is what it contains: [PASTE OR DESCRIBE IT]. Please reconcile it with what's in the repo, tell me what overlaps or conflicts, then add it to the repo rather than starting a separate copy.
