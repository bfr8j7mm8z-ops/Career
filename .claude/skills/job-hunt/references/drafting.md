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

## Working doc (one per application)

Draft in a Claude Doc, not Google Docs, so Harry can comment and edit inside Claude.

1. Create the doc "<Company> · <Role> · application" with three tabs, in order: **How this was
   made** (Inputs, Gauntlet scorecard, What changed from the last version), **CV**, **Cover letter**.
2. Write `workspace` on the application row (`app/SCHEMA.md`): doc link, version, steps done, and
   `open_question`.
3. Ask at most **one** question, as a doc comment anchored on the words it concerns.
4. Keep the markdown copies in the application folder in step (`cv-vN.md`, `cover-letter-vN.md`).

## Gauntlet (required before Harry sees a draft)

Decode the posting into requirements and keywords, map each to master-profile evidence, draft, then
run six critics: **truth checker** (every figure traced to a ✅ line; credit levels respected),
**6-second recruiter**, **hiring manager** for this role, **ATS reader**, **voice/humaniser**, and
**red team** (what an interviewer could catch out). Fix and re-run, up to three rounds. Record each
critic's finding, the fix and the final result in the "Gauntlet scorecard" table.

## Comments, edits and the learning journal

When Harry says "process my comments on <company>" (or at session start, for any workspace with
`open_question` set or new comments): list the doc's comments, act on each (answer questions in the
thread; make requested changes), reply in each thread, then write one `edit_journal` row per change
(said, change, lesson, scope). Before drafting any application, read the journal. When the same
lesson appears on two or more applications, propose it as a style rule via `profile_updates`
and set those rows to `status: "proposed"`.

## Styled files

`python3 -m automations.docs.render cv <folder>/cv-vN.md <out>.docx --pdf` (and `letter` for the
cover letter) builds Word and PDF in the GoCardless CSAM style: Calibri, one A4 page, name 16pt
bold blue (#1A5276), section headings 11pt bold capitals with a blue rule, body 10pt (#2C3E50),
grey details and right-aligned dates. The PDF renders with Carlito (metric-identical to Calibri)
when Calibri isn't installed, so line breaks match Word. Check it is one page. Upload the PDFs to
the app's file store (Artifact asset upload) and store the ids on `workspace`; send the files to
Harry for the Drive folder.

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
