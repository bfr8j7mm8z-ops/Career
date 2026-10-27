# Session handover

## State (27 Oct 2026)
- Repo `bfr8j7mm8z-ops/Career`, branch `claude/zen-shannon-sf0ved`. It now includes the CV work from
  `claude/blissful-euler-7geqpz` (merged, then archived to `cv/archive/`).
- Read `CLAUDE.md`, `HANDOVER.md` (incl. "Updates since this handover") and `cv/README.md` first.
- **Job Hunt app** (main interface): https://claude.ai/artifact/FxPHKGLJFPqBe4FMdTjgRK. Data contract:
  `app/SCHEMA.md`. Phase 1 is live (projects, filters, two-stage triage, "Why I said no", applications,
  profile uploads, suggested profile updates).
- **Blueprint** (the plan): https://claude.ai/artifact/6WjCRPKJ3FGmgZgVNwjLAK, source `docs/blueprint.html`.
- **Profile:** living master profile v2 in the app's Profile (and the original in Drive `Career / Master CV`).
  Single source of truth; not in the repo. Master CVs/cover letters: the two latest GoCardless applications.
- **Engine:** `automations/jobhunt/` (Python stdlib; `python3 -m unittest automations.jobhunt.tests.test_engine`).
- Drive: `Career` (`1yRg0lQ2JkNlWP7dCTTIi9nUEUip6dYwW`) → `Applications` (`1nF5mc-hDJ-f8cLd5qiQ6WA23L3F_6ZZu`)
  for finished documents; `Master CV` (`1uhGoJTSvja2Raq3xewjICfN-gIABIk8u`) holds the master profile
  and old applications for reference.

## Next
- Harry tests Phase 1 (create projects, Run now, then ask Claude to "process my run requests").
- Phase 2: Run now and the 8pm schedule start cloud runs; push notifications.
- Phase 3: company intel, the CV and cover letter gauntlet, review studio. Phase 4: assisted apply,
  outreach drafts, reply tracking, weekly improvement loop.
- Open profile questions: see master profile section 13 (retention rate, Schneider dates, SalesWolf
  market size, contact details for external CVs).
