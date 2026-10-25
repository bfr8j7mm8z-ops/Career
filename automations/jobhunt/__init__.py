"""Job-hunt engine: deterministic plumbing (fetch, dedupe, verify, queue).

Judgement work (reading the user's intent, scoring fit, drafting) is done by
Claude via .claude/skills/job-hunt. This package only moves and cleans data.
"""
