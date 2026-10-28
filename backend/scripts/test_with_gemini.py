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

# Create a more complex contract example
contract_text = """
EMPLOYMENT AGREEMENT

This Employment Agreement ("Agreement") is entered into on [Date] between [Company Name] ("Company") and [Employee Name] ("Employee").

1. TERM: This agreement shall commence on [Start Date] and continue for an initial term of two (2) years, with automatic renewal for successive one-year periods unless either party provides sixty (60) days written notice of termination.

2. COMPENSATION: Employee shall receive a base salary of $[Amount] per year, payable bi-weekly.

3. TERMINATION: Company may terminate this agreement at any time without cause with thirty (30) days notice. Employee may be terminated immediately for cause including breach of confidentiality or misconduct.

4. DISPUTE RESOLUTION: Any disputes arising under this agreement shall be resolved through binding arbitration in accordance with the rules of the American Arbitration Association.

5. NON-COMPETE: Employee agrees not to compete with Company for a period of two (2) years following termination within a 50-mile radius.

6. CONFIDENTIALITY: Employee shall maintain strict confidentiality of all proprietary information and trade secrets.
"""

files = {
    "file": (
        "employment_contract.txt",
        contract_text.encode(),
        "text/plain",
    )
}

print("Testing analyze endpoint with Gemini API...")
print(f"GEMINI_API_KEY set: {'GEMINI_API_KEY' in os.environ}")

resp = client.post("/api/analyze/", files=files)
print(f"Status: {resp.status_code}")

if resp.status_code == 200:
    data = resp.json()
    print(f"Input text length: {len(data['input_text'])}")
    prediction = data.get('prediction', {})
    print(f"Model version: {prediction.get('model_version', 'N/A')}")
    print(f"Analysis type: {prediction.get('analysis_type', 'N/A')}")
    
    # Print findings if available
    findings = prediction.get('findings', [])
    if findings:
        print(f"\nFindings ({len(findings)}):")
        for i, finding in enumerate(findings[:3], 1):  # Show first 3 findings
            print(f"  {i}. {finding.get('clause', 'N/A')}")
            print(f"     Risk: {finding.get('risk', 'N/A')}")
    
    # Check if this is real AI analysis or heuristic fallback
    if 'gemini' in prediction.get('model_version', '').lower():
        print("\n✅ Using live Gemini AI analysis!")
    else:
        print("\n⚠️ Using heuristic fallback analysis")
else:
    print(f"Error: {resp.text}")