# Drafting tailored CVs and cover letters

Inputs: the app's `profile_docs` (see `app/SCHEMA.md`), the job posting, and the job's rank/deep-review
reasons and gaps.

**Source-of-truth rule.**
- The **Master profile** doc is the evidence base. Every fact, number, title and credit level comes
  from it. Respect its markers: ✅ verified, ⚠️ verify before using, "Led / Pod-led / Supported" credit
  labels, and its list of old CV numbers to retire (e.g. "46 accounts / £2M ARR", "93% retention",
  "~40% reporting time saved"). Never reintroduce a retired number.
- The **master CVs and cover letters** (`is_master: true`) set structure, length, tone and voice. Start
  from the closest one (CS/AM track or partnerships track). Where their numbers disagree with the
  master profile, the master profile wins.
- Pick a summary variant, bullets and stories from the master profile by matching its tags to the job.
- **Conflicting figures: the most recent wins.** If two figures differ and it matters, ask Harry which
  to use before drafting further. Don't guess, and never fall back to an archived number.
- Follow the master profile's section 14: style rules (British English, builder voice, banned bullet),
  layout by target role, and when to use extra evidence from past CVs. The old repo evidence bank in
  `cv/archive/` is superseded: don't draft from it.

## CV

- Start from the master CV. Trim and reorder so the most relevant experience leads. Adjust
  the summary line to the role.
- Reuse the user's own phrasing; rewrite only what the posting needs. Don't launder it into
  generic CV-speak.
- Mirror the posting's wording only where it's true. Never add a skill, tool, title, scope or
  metric not in the master CV or role context. If the posting needs something they lack, leave
  it out and note it in `notes.md`.
- ATS-safe: single column, no tables/graphics, standard headings. Keyword coverage is a soft
  check, not a target to stuff towards.

## Cover letter (under 300 words)

1. Opening: a concrete, researched reason for *this* company (one real detail, found via web
   search). Not "I am writing to express my interest".
2. Middle: two or three achievements mapped directly to the role's needs.
3. Close: availability and what they'd like to discuss.
Specific, a little informal is fine, nothing that could be sent to any company.

## Tone pass (required)

Remove AI-isms: "spearheaded", "leveraged", "results-driven", "passionate about", "proven track
record", "synergy", "seamlessly", "cutting-edge", stacked adjectives. Vary bullet length and
shape: not every bullet is verb + metric + impact. Use the `the-humanizer` and
`cv-qa-humaniser` skills if available.

## Folder contents

`job-posting.md` (original text + link), `cv.md`, `cover-letter.md`, `notes.md` (gaps, company
research, salary/review notes, questions to ask, follow-up date). Add a row to
`job-search-log.md`.
