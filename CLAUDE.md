# Career repo

Purpose: long-term career management — CVs, cover letters, job applications, and job-search automation.

## Conventions

- Keep one folder per job application under `applications/`, named `YYYY-MM-DD-company-role/`, containing the job posting, tailored CV/cover letter, and notes.
- Track application status in `job-search-log.md`.
- Treat all content here as personal and private — never reference employer-specific confidential information.

## Notes for future sessions

- The job-hunt engine is Python 3.11+ stdlib only (no install). Tests: `python3 -m unittest automations.jobhunt.tests.test_engine`. Run commands from the repo root.
- The engine and skill are generic and contain no personal data; personal context lives in `cv/` and `profile/`.
- When adding automations (job search, CV updates, application drafting), document how to run them in `automations/README.md`.
