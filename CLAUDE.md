# Career repo

Purpose: long-term career management — CVs, cover letters, job applications, and job-search automation.

## Conventions

- Keep one folder per job application under `applications/`, named `YYYY-MM-DD-company-role/`, containing the job posting, tailored CV/cover letter, and notes.
- Track application status in `job-search-log.md`.
- Treat all content here as personal and private — never reference employer-specific confidential information.

## Notes for future sessions

- The job-hunt engine is Python 3.11+ stdlib only (no install). Tests: `python3 -m unittest automations.jobhunt.tests.test_engine`. Run commands from the repo root.
- The engine and skill are generic and contain no personal data.
- The Job Hunt app (`app/job-hunt-app.html`, published at https://claude.ai/artifact/FxPHKGLJFPqBe4FMdTjgRK) is the main interface. Its database holds live data (projects, jobs, decisions, applications, profile uploads); `app/SCHEMA.md` is the contract. Read and write it with the ArtifactData tool. Republish the app from the repo file so the URL stays the same.
- **Harry's profile:** the living master profile (live copy in the Job Hunt app's Profile; a matching copy in Google Drive `Career / Master CV`, replaced after each update) is the single source of truth for CV facts and figures. It is not stored in the repo (part of it was compiled from work systems; see `HANDOVER.md`). `cv/archive/` holds the superseded evidence bank: don't draft from it. See `cv/README.md`.
- **Conflicting figures:** assume the most recent is right; if in doubt while drafting a CV, ask Harry which to use.
- **Profile updates:** when a session learns something new about Harry, propose it as a `profile_updates` row in the app for him to approve; apply approved ones at the start of a session. Details in `.claude/skills/job-hunt/SKILL.md`.
- **Finished documents** (.docx/PDF) go to Google Drive `Career / Applications` (folder id `1nF5mc-hDJ-f8cLd5qiQ6WA23L3F_6ZZu`, parent `Career` = `1yRg0lQ2JkNlWP7dCTTIi9nUEUip6dYwW`).
- When adding automations (job search, CV updates, application drafting), document how to run them in `automations/README.md`.
