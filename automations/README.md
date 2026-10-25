# Automations

The job-hunt system: a generic engine plus a morning review page. It contains no personal data;
your CV and context go in `cv/` and `profile/` (templates in `templates/`).

```
 you (natural language)            nightly/scheduled run
        │                                   │
        ▼                                   ▼
  .claude/skills/job-hunt  ──►  gather ──► build queue ──► score fit
  (Claude: judgement)           (Indeed MCP, Adzuna, Reed,   (engine: dedupe, link check,
                                 ATS career pages, Gmail      filter, write data/queue/)
                                 alerts, optional Chrome)
                                              │
                                              ▼
                              app/index.html  (morning page: Interested / Maybe / Pass)
                                              │  decisions → data/decisions.json
                                              ▼
                      Claude drafts tailored CV + cover letter → applications/<folder>/
                                              │
                                              ▼
                        you apply yourself → job-search-log.md → Gmail outcome tracking
```

Split of work: the **engine** (`automations/jobhunt/`, Python 3.11+, stdlib only) moves and cleans
data and is unit-tested. **Claude** (the `job-hunt` skill) interprets requests, searches via
connectors, scores fit and drafts. The **page** is a single static file.

## Using it

Talk to Claude in this repo: "find me ...", "shortlist what came in", "draft the ones I marked
interested", "where are my applications at?". The skill does the rest.

### The morning page

Three ways to connect it (Settings button on the page):

| Mode | How | Best for |
|---|---|---|
| Local server | `python3 -m automations.jobhunt serve` then open http://127.0.0.1:8765 | At your computer; no tokens |
| GitHub | Open `app/index.html` (or host it anywhere static); give it repo, branch and a fine-grained token with *Contents: read & write* on this repo only | Phone or any device; token stays in that browser |
| File | Load a `queue/latest.json` | Quick look, no setup |

Decisions are saved to `data/decisions.json`. Hosting note: GitHub Pages for private repos needs a
paid plan; opening `app/index.html` straight from disk in GitHub mode works without hosting.

### Engine commands (run from the repo root)

```
python3 -m automations.jobhunt search  --spec spec.json --out scratch/candidates-api.json
python3 -m automations.jobhunt build   scratch/candidates-*.json --spec spec.json [--note "..."]
python3 -m automations.jobhunt score   scratch/scores.json
python3 -m automations.jobhunt decide  <id> interested|maybe|pass [--note ..] [--folder ..]
python3 -m automations.jobhunt pending           # interested jobs with no draft yet
python3 -m automations.jobhunt serve   [--port 8765]
python3 -m unittest automations.jobhunt.tests.test_engine   # tests
```

Search spec:
```json
{"country": "gb", "max_age_days": 14, "salary_min": 70000, "results_per_source": 50,
 "queries": [{"keywords": "partnerships manager", "location": "London", "remote": false}]}
```

Data files: `data/queue/YYYY-MM-DD.json` + `latest.json` (the queue), `data/decisions.json`,
`data/seen.json` (so jobs aren't shown twice). Job record fields are in
`automations/jobhunt/model.py`.

### Configuration

`config/jobhunt.toml` turns sources on/off. Chrome is `mode = "ask"` by default: Claude offers it
each interactive run and only uses it on a yes (`"off"` to never, `"on"` to skip asking). It is
never used in scheduled runs. Details in `.claude/skills/job-hunt/references/`.

API keys (Adzuna, Reed): see `references/sources.md` for how to get them, then copy
`.env.example` to `.env`. Sources without keys are skipped with a note on the page, not an error.

## Not set up yet

- Nightly scheduled run (a scheduled Claude task that runs the skill unattended and commits
  `data/` so the page picks it up). Set up once profile + CV exist and keys are in the cloud
  environment's secrets.
- Gmail outcome tracking needs a personal inbox connected.
- Personal profile, master CV and cover letter template (use `templates/`).
