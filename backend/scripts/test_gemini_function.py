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
from app.utils.model_loader import _predict_with_gemini, GEMINI_MODEL  # noqa: E402

print(f"GEMINI_MODEL is None: {GEMINI_MODEL is None}")
print(f"GEMINI_API_KEY set: {'GEMINI_API_KEY' in os.environ}")

test_text = "This is a contract agreement with automatic renewal and binding arbitration."

print("Testing _predict_with_gemini() directly...")
result = _predict_with_gemini(test_text)

print(f"Gemini result: {result}")
print(f"Result type: {type(result)}")

if result:
    print(f"Keys: {list(result.keys())}")
    if 'category' in result:
        print(f"Category: {result['category']}")
    if 'risk_level' in result:
        print(f"Risk level: {result['risk_level']}")
else:
    print("Gemini result is None or empty")