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
- When adding automations (job search, CV updates, application drafting), document how to run them in `automations/README.md`.
