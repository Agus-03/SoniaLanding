"""
Minimal prototype API for the SONIA Early Adopter CTA.

Run:
    python server.py

Then open:
    http://localhost:8080

The aggregate counter is stored in sonia_events.db (SQLite).
For the real thesis validation deployment, move this endpoint into SONIA's
existing backend and add rate limiting / privacy controls.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
import sqlite3
import urllib.parse

ROOT = Path(__file__).resolve().parent
DB = ROOT / "sonia_events.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT NOT NULL,
                page TEXT,
                referrer TEXT,
                utm_source TEXT,
                utm_medium TEXT,
                utm_campaign TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

class Handler(BaseHTTPRequestHandler):
    def _json(self, status, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path != "/api/early-adopter-click":
            self._json(404, {"ok": False})
            return

        length = int(self.headers.get("Content-Length", "0"))
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self._json(400, {"ok": False})
            return

        if body.get("event") != "early_adopter_cta_click":
            self._json(400, {"ok": False})
            return

        with sqlite3.connect(DB) as conn:
            conn.execute("""
                INSERT INTO events
                (event, page, referrer, utm_source, utm_medium, utm_campaign)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                body.get("event"),
                body.get("page"),
                body.get("referrer"),
                body.get("utm_source"),
                body.get("utm_medium"),
                body.get("utm_campaign"),
            ))
            total = conn.execute(
                "SELECT COUNT(*) FROM events WHERE event='early_adopter_cta_click'"
            ).fetchone()[0]

        self._json(200, {"ok": True, "total_clicks": total})

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"

        if self.path.startswith("/api/"):
            self._json(404, {"ok": False})
            return

        requested = urllib.parse.unquote(self.path.lstrip("/"))
        file = (ROOT / requested).resolve()

        if ROOT not in file.parents and file != ROOT:
            self._json(403, {"ok": False})
            return

        if not file.exists() or not file.is_file():
            self._json(404, {"ok": False})
            return

        content_type = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
        }.get(file.suffix, "application/octet-stream")

        data = file.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    init_db()
    print("SONIA landing: http://localhost:8080")
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
