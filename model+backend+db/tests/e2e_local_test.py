from __future__ import annotations

import os
import sys
import json
import threading
import time

import requests


def start_backend():
    # Run uvicorn in-process for the backend
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "HackQuest_ZIP_1", "OptiML-CodeQuest-main")))
    os.environ.setdefault("GOOGLE_API_KEY", "")
    # Prefer SQLite fallback for local test
    os.environ.setdefault("DATABASE_URL", f"sqlite+aiosqlite:///{os.path.abspath('lawgic_local.db')}")

    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False, log_level="info")


def run_ai_legal_assistant_smoke():
    # Reuse provided smoke test
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    import examples.smoke_test as smoke
    smoke.main()  # type: ignore[attr-defined]


def main():
    # 1) Start backend in a thread
    t = threading.Thread(target=start_backend, daemon=True)
    t.start()
    time.sleep(2.5)

    # 2) Call backend analyze endpoint
    resp = requests.post("http://127.0.0.1:8000/api/analyze/", data={"text": "Test NDA and IP ownership."})
    print("/api/analyze status:", resp.status_code)
    print("/api/analyze body:", resp.text)

    # 3) Run ai_legal_assistant smoke test
    run_ai_legal_assistant_smoke()


if __name__ == "__main__":
    main()
