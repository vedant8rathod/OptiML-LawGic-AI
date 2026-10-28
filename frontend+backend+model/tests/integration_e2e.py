from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient


def run_backend_test():
    # Configure env for local test
    repo_root = Path(__file__).resolve().parents[1]
    backend_root = repo_root / "HackQuest_ZIP_1" / "OptiML-CodeQuest-main"
    sys.path.insert(0, str(backend_root))

    os.environ.setdefault("GOOGLE_API_KEY", "")
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{repo_root / 'lawgic_local.db'}"

    # Import and test app via ASGI TestClient
    from app.main import app
    with TestClient(app) as client:
        res = client.post("/api/analyze/", data={"text": "Test NDA and IP ownership."})
        print("backend /api/analyze status:", res.status_code)
        print("backend /api/analyze body:", res.text)


def run_ai_module_smoke():
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    import examples.smoke_test as smoke
    smoke.main()  # type: ignore[attr-defined]


if __name__ == "__main__":
    run_backend_test()
    run_ai_module_smoke()
