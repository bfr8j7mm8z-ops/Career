"""Command line for the job-hunt engine. Run from the repo root:

    python3 -m automations.jobhunt <command> ...
"""
import argparse
import json
import sys
from pathlib import Path

from . import pipeline


def cmd_search(args):
    spec = json.loads(Path(args.spec).read_text())
    jobs, notes = pipeline.run_api_sources(spec, pipeline.load_config())
    pipeline.save_json(args.out, {"notes": notes, "jobs": jobs})
    print("\n".join(notes) or "no API sources enabled")
    print(f"wrote {len(jobs)} candidates to {args.out}")


def cmd_build(args):
    config = pipeline.load_config()
    spec = json.loads(Path(args.spec).read_text()) if args.spec else {}
    jobs, notes = [], list(args.note or [])
    for p in args.inputs:
        data = json.loads(Path(p).read_text())
        if isinstance(data, dict):
            notes.extend(data.get("notes", []))
            jobs.extend(data["jobs"])
        else:
            jobs.extend(data)
    queue = pipeline.build_queue(jobs, spec, notes, config,
                                 check_links=not args.no_linkcheck, include_seen=args.include_seen)
    pipeline.write_queue(queue)
    print(f"queue: {len(queue['jobs'])} jobs; dropped {queue['dropped']}")
    for n in queue["notes"]:
        print(" -", n)


def cmd_score(args):
    path = pipeline.QUEUE_DIR / "latest.json"
    queue = pipeline.load_json(path, None)
    if queue is None:
        sys.exit("no queue yet: run `build` first")
    scores = json.loads(Path(args.scores).read_text())
    n = pipeline.apply_scores(queue, scores)
    pipeline.save_json(path, queue)
    dated = pipeline.QUEUE_DIR / f"{queue['generated'][:10]}.json"
    pipeline.save_json(dated, queue)
    print(f"scored {n} of {len(queue['jobs'])} jobs")


def cmd_decide(args):
    print(pipeline.set_decision(args.id, args.status, args.note or "", args.folder))


def cmd_pending(args):
    for j in pipeline.pending_drafts():
        print(f"{j['id']}  {j.get('company', '?')} - {j.get('title', '?')}  {j.get('url', '')}")


def cmd_serve(args):
    from . import server
    server.serve(args.port)


def main(argv=None):
    p = argparse.ArgumentParser(prog="jobhunt")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="query enabled API sources (Adzuna, Reed)")
    s.add_argument("--spec", required=True, help="search spec JSON (see automations/README.md)")
    s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_search)

    s = sub.add_parser("build", help="merge candidates, dedupe, verify links, write the queue")
    s.add_argument("inputs", nargs="+", help="candidate JSON files (from `search` or Claude-gathered)")
    s.add_argument("--spec")
    s.add_argument("--note", action="append", help="status line to show on the page, e.g. a source that returned nothing")
    s.add_argument("--no-linkcheck", action="store_true")
    s.add_argument("--include-seen", action="store_true")
    s.set_defaults(fn=cmd_build)

    s = sub.add_parser("score", help="merge Claude's fit scores into the latest queue")
    s.add_argument("scores", help='JSON: {"<id>": {"fit": 80, "fit_reason": "...", "gaps": []}}')
    s.set_defaults(fn=cmd_score)

    s = sub.add_parser("decide", help="record interested/maybe/pass for a job id")
    s.add_argument("id")
    s.add_argument("status", choices=["interested", "maybe", "pass"])
    s.add_argument("--note")
    s.add_argument("--folder", help="applications/ folder once drafted")
    s.set_defaults(fn=cmd_decide)

    s = sub.add_parser("pending", help="list interested jobs still awaiting drafts")
    s.set_defaults(fn=cmd_pending)

    s = sub.add_parser("serve", help="serve the morning page locally and save decisions to disk")
    s.add_argument("--port", type=int, default=8765)
    s.set_defaults(fn=cmd_serve)

    args = p.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
