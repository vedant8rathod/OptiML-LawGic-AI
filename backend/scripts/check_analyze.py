import sys
import json
from pathlib import Path

# Ensure backend is on path
repo_root = Path(__file__).resolve().parents[2]
backend_dir = repo_root / "backend"
sys.path.insert(0, str(backend_dir))

from app.main import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

client = TestClient(app)

files = {
    "file": (
        "test.txt",
        b"This is a contract agreement with automatic renewal and binding arbitration.",
        "text/plain",
    )
}

resp = client.post("/api/analyze/", files=files)
print(resp.status_code)
print(resp.text)
