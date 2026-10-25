"""Local server for the morning page. Reads the queue from disk and writes
decisions back to data/decisions.json. Bound to localhost only."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import model, pipeline

APP = pipeline.ROOT / "app"


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, (APP / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/queue":
            self._send(200, pipeline.load_json(pipeline.QUEUE_DIR / "latest.json",
                                               {"jobs": [], "notes": [], "generated": None}))
        elif self.path == "/api/decisions":
            self._send(200, pipeline.load_json(pipeline.DECISIONS, {"decisions": {}}))
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/decision":
            return self._send(404, {"error": "not found"})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            if body.get("status") not in model.DECISIONS or not body.get("id"):
                raise ValueError("need id and status in interested/maybe/pass")
            rec = pipeline.set_decision(body["id"], body["status"], body.get("note", ""), job=body.get("job"))
        except (ValueError, json.JSONDecodeError) as e:
            return self._send(400, {"error": str(e)})
        self._send(200, rec)

    def log_message(self, *args):
        pass


def serve(port=8765):
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Morning page: http://127.0.0.1:{port}  (Ctrl+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
