import sys
import os
import json
from pathlib import Path

# Load environment first
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=env_path)
    print(f"Loaded .env from: {env_path}")
except ImportError:
    print("Warning: python-dotenv not available")

# Ensure backend is on path
repo_root = Path(__file__).resolve().parents[2]
backend_dir = repo_root / "backend"
sys.path.insert(0, str(backend_dir))

# Import after setting environment
from app.main import app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

client = TestClient(app)

# Test with a simple contract text
simple_contract = "This is a service contract with automatic renewal and binding arbitration clauses."

files = {
    "file": (
        "simple_contract.txt",
        simple_contract.encode(),
        "text/plain",
    )
}

print("Testing analyze endpoint with simple contract...")
print(f"GEMINI_API_KEY set: {'GEMINI_API_KEY' in os.environ}")

resp = client.post("/api/analyze/", files=files)
print(f"Status: {resp.status_code}")

if resp.status_code == 200:
    data = resp.json()
    print(f"Input text length: {len(data['input_text'])}")
    prediction = data.get('prediction', {})
    print(f"Model version: {prediction.get('model_version', 'N/A')}")
    print(f"Category: {prediction.get('category', 'N/A')}")
    print(f"Risk level: {prediction.get('risk_level', 'N/A')}")
    
    # Check if this is real AI analysis
    summary = prediction.get('summary', '')
    if summary and len(summary) > 100:
        print(f"\n✅ Using live Gemini AI analysis!")
        print(f"Summary preview: {summary[:200]}...")
    else:
        print(f"\n⚠️ Using fallback analysis")
        print(f"Full prediction: {prediction}")
else:
    print(f"Error: {resp.text}")