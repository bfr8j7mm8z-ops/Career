# Comparison: "job-skill" (YouTube) vs. this repo's plan

Reference: the `job-skill` SKILL.md + README from the video (India-focused job search skill).
Ours: the scope in `HANDOVER.md` ("Job sourcing plan" and "Revised process/loop").

## The core difference

| | job-skill (his) | Ours |
|---|---|---|
| Starting point | Fixed profile questionnaire, then `/job-skill search` | Context about you (CV, role, background) already on file, plus whatever you say in natural language ("remote partnerships roles at fintechs, £70k+") |
| Direction | Jobs found, then a resume generated for every hit | Jobs found from your intent, CV tailored only for jobs you pick |
| Search focus | Set once at setup | Rolling, overwritten whenever targeting shifts (`profile/current-search-focus.md`) |
| Sourcing | `site:` WebSearch queries over 12 Indian boards | Indeed MCP + Adzuna/Reed APIs + alerts; Chrome extension now proposed for the rest |
| Output | Zip of CV + cover letter per match (fit >= 60%) | Morning shortlist, you mark interested/pass, then drafting |
| Submission | Manual | Manual (same) |
| Status | Fully written, untested for your market | Plan only, nothing built |

## Keep (adapt to our flow)

1. **Fitness score.** A holistic "how well do you actually fit" percentage with a one-line reason, separate from keyword matching. Drop the India weighting (YOE, education/CGPA). Reweight for you: skills/domain overlap, seniority fit, sector (fintech/SaaS), comp and location fit, gaps stated honestly.
2. **Never lie on the CV.** If the JD wants something you don't have, it's logged as a gap, not added.
3. **Human-tone rules** (no "spearheaded/leveraged/results-driven", varied bullet rhythm, no "I am writing to express my interest", reuse your real phrasing). We already have `the-humanizer` and `cv-qa-humaniser` skills, so call them as a final pass instead of duplicating the rules.
4. **Link verification and dedupe.** Fetch each job URL, drop dead or filled listings, flag postings over 30 days old, convert "3 days ago" to dates, dedupe across boards.
5. **Status flow + Gmail outcome detection.** Found, Ready, Applied, Acknowledged, Assessment, Interview, Offer, Rejected, Ghosted (21+ days). Gmail connector parses replies. He restricts it to emails from companies you applied to; keep that. (Needs a **personal** inbox per HANDOVER.)
6. **Pattern analysis on outcomes.** Same-day rejections suggest an ATS filter, rejections after interview suggest prep rather than the CV, and so on. Keep it, but always say plainly when there's no clear pattern.
7. **Unattended mode rules** for any scheduled run (no blocking questions, document decisions in the report).
8. **Follow-up reminders** at 7-10 days.
9. **No auto-submit.** Matches our human-in-the-loop step.

## Drop

- India specifics: Naukri/Instahyre/Cutshort/Hirist/Foundit/Shine/TimesJobs, CTC/LPA, notice-period framing, GATE/CGPA, IST cron conversion, per-country format rules we don't need yet.
- **Generate CV + cover letter for every match.** Wasteful and noisy. We draft on "interested" only.
- **Profile questionnaire up front.** Replaced by your CV + natural language.
- **Hiding the ATS score and failures.** His "output cleanliness" rule suppresses process, which is fine, but also says to stay quiet about failures unless they cut results materially. We should state "Glassdoor returned nothing today", not hide it.
- Keyword-stuffing to a 70% ATS target as a hard gate. A crude formula, and it pushes toward JD-mirroring that can sound robotic. Use keyword coverage as a soft check only.
- `xlsx` tracker. Our markdown `job-search-log.md` plus per-application folders is easier to diff and version.
- The YouTube plug and the "Indian professionals" framing.

## What he does that ours doesn't yet (worth adding)

- `site:` search over **ATS-hosted career pages** is a good low-risk way to reach roles without scraping job boards. For fintech/SaaS targets, point it at Greenhouse, Lever, Ashby, Workable and Wellfound, plus direct company careers pages. Search-engine queries are not scraping a logged-in site.
- Direct company watchlist (he has 8-10 target companies). We'd keep a `profile/target-companies.md`.
- Weekly review of what's working.

## What ours has that his doesn't

- Intent-first, natural-language search.
- CV tailoring per job from a master CV plus role context, with a morning review queue before any drafting.
- Official-source stance (Indeed MCP, Adzuna, Reed, native alerts) and data-handling rules agreed in `HANDOVER.md`.

## Sourcing: proposed layers (cheapest/safest first)

1. **Indeed MCP** (official connector): natural-language query to `search_jobs`, then `get_job_details`. Also `get_company_data` for company context.
2. **Adzuna / Reed APIs**: structured filters, UK coverage. Needs free keys.
3. **`site:` search queries** over ATS career pages and smaller boards (the borrowed idea).
4. **Claude in Chrome** for boards with no API (LinkedIn, Glassdoor, Welcome to the Jungle, etc.), driven in **your own logged-in browser, while you're present**.
5. **Alert emails** (LinkedIn/Glassdoor/Indeed) read via a personal Gmail as a passive feed.
6. **Manual paste-in** as fallback.

### Note on layer 4 (Chrome extension), which revises an earlier decision

`HANDOVER.md` ruled out scraping LinkedIn/Indeed/Glassdoor for ToS and account-ban reasons. Using the Chrome extension is a different thing from a headless scraper (it's your real browser, your real session, at human pace), but it is not risk-free, because LinkedIn and Glassdoor's terms still prohibit automated collection, and it's your account at stake. Suggested guardrails if we go ahead:
- You're present and it's a handful of searches per session, not a bulk crawl or schedule.
- Read-only: no applying, messaging, connecting, or account actions.
- Use it where it adds most. Glassdoor is probably best for **salary and review research on shortlisted companies** rather than job discovery, since listings mostly duplicate other boards.
- Don't schedule it unattended.

## Proposed shape of the build (not started)

One skill, `job-hunt`, in `.claude/skills/job-hunt/SKILL.md`, driven by natural language:

1. **Read context**: `cv/master-cv.md`, `profile/current-role.md`, `profile/current-search-focus.md`, `profile/target-companies.md`.
2. **Interpret the request** ("find me X"), and update the search focus if it changed.
3. **Search** through the layers above, then dedupe and verify links.
4. **Score** with the fitness model and write a ranked shortlist (company, role, salary if known, fit %, reason, gaps, link).
5. **You pick** interested/pass.
6. **Draft** a tailored CV + cover letter into `applications/YYYY-MM-DD-company-role/`, run the humaniser and QA passes, log it in `job-search-log.md`.
7. **Track**: Gmail outcome detection, follow-up reminders, weekly review.

## Open questions

- Location/remote constraints and salary floor (so scoring is meaningful).
- Is `cv/master-cv.md` uploaded yet? Nothing in the repo yet beyond the READMEs.
- Personal Gmail connected for alert emails and outcome detection?
- OK to proceed with Chrome-extension use on the guardrails above?
