import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


HOST = "localhost"
PORT = 8080
ADVANCE_SECONDS = 3


def resolve_data_file() -> Path:
    base_dir = Path(__file__).resolve().parent
    candidates = [
        base_dir / "mock_scan_data.json",
        base_dir / "Content" / "CameraModule" / "MockData" / "mock_scan_data.json",
        base_dir.parent / "mock_scan_data.json",
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Could not find mock_scan_data.json in expected locations."
    )


class ScanState:
    def __init__(self, events):
        if not isinstance(events, list) or not events:
            raise ValueError("mock_scan_data.json must contain a non-empty array.")
        self._events = events
        self._index = 0
        self._lock = threading.Lock()

    @property
    def total(self):
        return len(self._events)

    def get_current(self):
        with self._lock:
            return self._index, self._events[self._index]

    def reset(self):
        with self._lock:
            self._index = 0
            return self._index

    def advance(self):
        with self._lock:
            self._index = (self._index + 1) % len(self._events)
            index = self._index
            event = self._events[self._index]
        self._print_scan(index, event)

    def status_summary(self):
        ok = warning = error = anomaly = 0
        for event in self._events:
            event_status = normalize_status(event)
            if event_status == "ok":
                ok += 1
            elif event_status == "warning":
                warning += 1
            elif event_status == "error":
                error += 1
            if event.get("anomaly"):
                anomaly += 1

        with self._lock:
            current_index = self._index

        return {
            "total": len(self._events),
            "ok": ok,
            "warning": warning,
            "error": error,
            "anomaly": anomaly,
            "current_index": current_index,
        }

    @staticmethod
    def _print_scan(index, event):
        object_id = (
            event.get("object_id")
            or event.get("ObjectID")
            or event.get("Name")
            or "unknown"
        )
        object_type = (
            event.get("object_type")
            or event.get("ObjectType")
            or "unknown"
        )
        status = normalize_status(event)
        print(
            f"[SCAN] Index {index} | {object_id} | {str(object_type).lower()} | {status}",
            flush=True,
        )


def normalize_status(event):
    if "status" in event and event["status"] is not None:
        return str(event["status"]).lower()
    if "IsValid" in event:
        return "ok" if bool(event["IsValid"]) else "error"
    return "warning"


class CameraRequestHandler(BaseHTTPRequestHandler):
    state = None

    def _send_json(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/current":
            _, event = self.state.get_current()
            self._send_json(200, event)
            return
        if path == "/status":
            self._send_json(200, self.state.status_summary())
            return
        if path == "/reset":
            self.state.reset()
            self._send_json(200, {"message": "ok", "current_index": 0})
            return
        self._send_json(404, {"error": "Not Found"})

    def log_message(self, _format, *args):
        return


def start_advancer(state):
    def _loop():
        while True:
            time.sleep(ADVANCE_SECONDS)
            state.advance()

    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()


def main():
    data_path = resolve_data_file()
    with data_path.open("r", encoding="utf-8") as f:
        events = json.load(f)

    state = ScanState(events)
    CameraRequestHandler.state = state
    start_advancer(state)

    server = ThreadingHTTPServer((HOST, PORT), CameraRequestHandler)
    print(f"Loaded {state.total} scan events from: {data_path}", flush=True)
    print(f"Serving on http://{HOST}:{PORT}", flush=True)
    print("Endpoints: /current, /status, /reset", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
