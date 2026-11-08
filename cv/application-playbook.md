# Application playbook: how CVs and cover letters are made

Repo copy of the live Claude Doc: https://claude.ai/artifact/QhRxhPALUb1jLPttK7FeLn
The doc is where Harry comments and edits. When it changes, update this copy to match. The app's
Process page (Make stage) summarises each step and links to the doc.

## The six steps

| Step | What happens | Who | Output |
|---|---|---|---|
| 1. Decode | Break the posting into every requirement and match each to proof | Claude | Requirements table in the working doc |
| 2. Draft | Build the CV, then the letter and form answers, from the table | Claude | CV, Cover letter and Form answers tabs |
| 3. Review agent | Check everything, fix, check again, until it passes | Claude, looping | Review log, clean drafts |
| 4. Harry reviews | Read the drafts, comment, strike through, edit | Harry | Comments and edits |
| 5. Learn | Apply the comments, log each lesson, rerun the review agent | Claude | Journal entries, updated playbook |
| 6. Export | Styled .docx and PDF, one page, to Drive | Claude | Files in Career / Applications |

Principles:
1. The posting sets the questions. The drafts answer them, and the coverage matrix proves it.
2. The CV shows evidence. The letter makes the argument. The letter never repeats a CV bullet word for word.
3. Facts come only from the master profile. Most recent figure wins. If in doubt, ask Harry.
4. Start from the last submitted CV (PPRO AE, 5 Nov) and change 5 to 10%.
5. Never scale Harry down.
6. The review agent does the checking, so Harry does the judging.

## Step 1. Decode the job (no stop, runs straight into drafting)

Inputs: the full posting (pasted if blocked, never a summary), the master profile, the latest submitted
CV, the proof bank (`cv/cover-letter-playbook.md`), the edit journal, the job's closer look.

- **1a.** Every sentence that asks for something becomes a row, in the posting's own words, across About
  the role, What you'll do, Who you are and Nice to have. Split compound asks ("strong collaborator who
  prioritises independently" is two rows).
- **1b.** Requirements table columns: requirement, section, must or nice, keywords, best proof with its
  number, strength (0 none, 1 adjacent, 2 direct, 3 direct with a number), where it lives (CV, letter,
  both, form), gap handling.
- **1c.** Total the strengths and show the percentage. Every 0 or 1 gets a decision: bridge it (letter
  only), reframe a true bullet, or leave it. A 5+ year ask is flagged but drafting carries on.
- **1d.** The angle in one line, one company fact with a source, and the change plan (summary sentences
  2 and 3, bullets to reorder, reword or swap, the Core line). Nothing else changes.

## Step 2. Draft from the decode

Working doc tabs: How this was made (decode, fit score, gaps, angle, change plan, coverage matrix, review
log, changes from base), CV, Cover letter (with paragraph map), Form answers.

### CV versus cover letter versus form answers

| | CV | Cover letter | Form answers |
|---|---|---|---|
| Job | Prove it happened | Argue why it matters here | Answer the exact question |
| Reader | Recruiter skimming six seconds, and the ATS | Hiring manager deciding whether to call | Recruiter with a scorecard |
| Contains | Achievements, numbers, scope, tools, keywords | Motivation, why the company and role, the story behind one or two results, the honest gap bridge, the value Harry adds | A compressed letter paragraph |
| Never contains | Motivation, opinions, gaps, first person, "passionate" | A list of CV bullets, figures with no story, stock lines | Anything contradicting the CV |
| Length | One page | 250 to 350 words, four paragraphs | The form's limit, aim for 80% |

### Where each requirement lives

| Kind | Home |
|---|---|
| Must-have skill or experience | CV, always, led by the posting's keyword. Letter optional, with the story |
| Soft skill (collaboration, autonomy) | CV bullet with a concrete example, plus a letter sentence if central. "Strong collaborator" = the CEO and CCO bullet + one letter line on how it worked |
| Nice-to-have | Core line, or one clause in the letter |
| Motivation, why the company | Letter only |
| Gap (0 or 1) | Letter only, as a bridge, or nowhere |
| Logistics | CV header or the form |

Test: with only the CV, would the reader tick every must-have? If not, it is not covered.

### Coverage matrix (in How this was made)

One row per requirement: CV line, letter line, form line, covered, score 0 to 3. Rules: every must-have
has a CV line, every requirement has a line or a written decision to leave it, nothing is answered by the
same words twice, each CV bullet answers one requirement (two at most).

Drafting order: copy the base CV, apply the change plan (summary, Core line, bullets), fill the matrix and
fix any must-have without a CV line, draft the letter from the paragraph map, draft the form answers,
hand to the review agent.

### 2a. CV method

Format is fixed (`cv/format-notes.md`): PROFESSIONAL SUMMARY (about five lines), EXPERIENCE, EDUCATION,
SKILLS & TOOLS. Summary uses Harry's five-sentence structure: change sentences 2 (how he works) and 3
(results and style) only. Sentences 1 (role and book), 4 ("Driven and proactive", Brazil) and 5
(background, M-Pesa) stay. Core line rebuilt in the posting's terms and priority, pushing the limit on
labels. Bullets: move the best proof for each must-have up its role and reword its opening to carry the
keyword. Shape: verb, what, for whom, result with a number. Swap a bullet only if it answers nothing
(the TJX bullet on the Adyen AM role).

| Don't | Do |
|---|---|
| "Experienced in working with senior stakeholders" | "Collaborated with Fospha's CEO and CCO on…" (Harry's wording) |
| "Managed a team of CSMs" | Pod lead, with the pod of up to six CSMs |
| "Partnerships with Google and Pinterest" | "partnerships such as Google" |
| "Delivered several three-way deals" | "TJX × Google three-way negotiation" |
| "Led the Dyson SEU commercials" | Led the relationship with Dyson |
| "Built Claude skills…" | "Built 20+ AI automation workflows now used across the account management team" |
| "≈ 6 weeks early; saving time" | Six weeks ahead of term, no ≈, no semicolons |

Rate 0 to 3 per requirement. Any must-have under 2 goes back into drafting (Adyen AM: 9/18 to 16/18).
Re-render after every change. When it spills: orphan words, long role labels, the oldest role's weakest
bullet, the Interests line. Never shrink font or margins.

### 2b. Cover letter and form answers

CV only by default. The letter is still drafted because it feeds the form answers.

| Paragraph | Answers | Length | Content |
|---|---|---|---|
| P1 Why this company and role | Why us? | 3 sentences, about 70 words | A checkable point about their business, Harry's current work in one line echoing it, why this role is next with the personal reason |
| P2 Why me | Can you do it? | 4 to 5 connected sentences, about 110 words | One or two results for the biggest must-haves: situation, action, result, so what for them |
| P3 How I work | Will you fit? | 3 to 4 sentences, about 80 words | The named soft skills, one example each, plus the honest gap bridge |
| P4 Value and close | What next? | 2 to 3 sentences, about 50 words | What he'd deliver first in their terms, plain close |

Paragraph map under the letter: each sentence and the requirement it answers. A sentence that answers
nothing is cut.

P1 rethink method: write the angle, find the company fact under it, sentence 1 about the company (never
"I want", "I am writing to apply", "I am excited"), sentence 2 Harry's work echoing it, sentence 3 the
bridge and personal reason, read aloud and fix the joints.

Letter don'ts: "I want" openings, repeating CV bullets without the story, reused lines, unverified client
names, list paragraphs, claimed enthusiasm, hiding or overclaiming a gap.

Form answers: note the limit and aim for 80%, take "why this role" from P1 and "why a good fit" from P2
and P4 with the so what stated, lead with what the company wants to hear, keep figures identical to the
CV, leave salary, notice, sponsorship and start date as marked placeholders for Harry.

## Step 3. The review agent (replaces the gauntlet)

A final checker that loops: run all seven checks, fix every failure, start again from check 1. Stop
when a round finds nothing, or after round 3. Items only Harry can decide stay unchanged and are listed
as open items.

| # | Check | Passes when |
|---|---|---|
| 1 | Truth | Every figure, name, date and scope claim traces to the master profile, most recent first, no known traps |
| 2 | Coverage | Matrix complete, every must-have 2 or 3 in the CV, every gap decided, nothing answered twice in the same words |
| 3 | Reader tests | Six-second skim shows fit, each bullet invites a question, red team finds no indefensible claim |
| 4 | ATS | Posting's top keywords in exact form, standard headings, no tables or text boxes in the CV |
| 5 | Voice and AI tells | No semicolons, ≈, ~, colon joins, stacked clauses, CV first person, "I want", "passionate", "leverage", "spearheaded", "delve", rule-of-three padding, stock lines |
| 6 | Consistency | Figures, dates, titles and names match across CV, letter, form answers. British spelling |
| 7 | Format, last | CV one page, letter 250 to 350 words, form answers within limits |

Output: a review log (round, failures, what changed) in How this was made, and one hand-over comment at
the top of the doc with the fit score before and after, open items, and anything not done and why.
In the app's database the result is stored in `workspace.gauntlet` (field name kept) and shown as
"Review agent".

## Steps 4 to 6

- **Harry reviews:** comment and mention @Claude, strike through to remove, edit directly (kept word for
  word), answer open items. He judges voice, emphasis and anything he would not want to be asked about.
- **Learn:** apply each change and reply on its thread, decide one-off or general, log it in the edit
  journal, add general rules to this playbook and the review agent's checks, propose new facts as profile
  updates, rerun the review agent.
- **Export:** `python3 -m automations.docs.render cv|letter <md> <out.docx> --pdf`, check one page, upload
  to Drive Career / Applications in a `YYYY-MM-DD-company-role` folder, attach to the app card. Once
  submitted and marked Applied, that CV becomes the new base.

## Known traps

| Trap | True version |
|---|---|
| Pod leadership as line management | Pod lead for up to six CSMs |
| "Deals" plural | One TJX × Google three-way negotiation |
| Partner-funded programmes | Only the five won: TJX, Samsonite, American Tourister, TUMI, Hobbs. None in flight |
| Partners named | "partners such as Google". Pinterest removed |
| Dyson SEU commercials | Another AM led them. Harry led the relationship |
| New-market deal (DACH) | Out for signature, not signed |
| Renewals | Six weeks ahead of term |
| Paris senior leadership session | About 15 people |
| The target company's clients | Only if verified, with a source |
| AI work | "AI automation workflows" |
| Conflicting figures | Most recent wins, else ask Harry |

Writing habits corrected: semicolons, ≈ and ~, colon joins, stacked clauses, CV first person, "I want"
and "I am writing to" openings, stock lines, list paragraphs, scaling down, rewriting more than 10% or
touching summary sentences 1, 4 and 5.

Process traps: strikethrough means remove, keep Harry's edits word for word, re-render after every edit,
rebuild doc text as markdown so it does not inherit strikethrough, a must-have answered only in the
letter is not covered.
