# CV

## Where the profile lives
- **Living master profile** (single source of truth for facts, figures, stories and style):
  - Live copy: the Job Hunt app's Profile, doc `d-master-profile` (`kind: "Master profile"`), read and
    written with the ArtifactData / Artifact tools. See `app/SCHEMA.md`.
  - Drive copy: Google Drive `Career / Master CV`, "Harry Stichbury master career profile (living, vN)"
    (v2 doc id `1CTWqSsF6O7rl8jIHyxpUh_7s5Ivek5fQQIeR23Wp49g`; the app row stores the current id in
    `drive_doc_id`). The app copy is the live one; the Drive copy is replaced after every update. Older
    Drive versions are renamed "SUPERSEDED …" and kept.
  - It is **not** stored in this repo: it was compiled partly from work systems, and `HANDOVER.md` keeps
    work-connector data out of the repo.
- **Master CVs and cover letters** (structure and voice): the two most recent GoCardless applications
  (CSAM Jun 2026; Global Partnerships Apr 2026), in the app's Profile with `is_master: true`.
- **Finished documents** (.docx/PDF): Google Drive `Career / Applications`.
- `archive/`: the older evidence bank and Jun 2026 CV, superseded. Don't draft from them.

## Rules
1. **Most recent wins.** If two figures differ, assume the most recent is right. If in doubt while
   drafting, ask Harry which to use.
2. Respect the master profile's markers: ✅ verified, ⚠️ verify first, Led / Pod-led / Supported, and its
   list of retired numbers. Never reintroduce a retired number.
3. **The profile keeps growing.** When a session learns something new about Harry, it proposes a profile
   update (app `profile_updates` collection). Harry approves it in the app; then Claude applies it to
   the master profile and logs it in its update log. Nothing changes silently.
4. Tailored versions for specific applications live in `applications/<folder>/` (Markdown source) and
   Drive `Career / Applications` (finished files).
