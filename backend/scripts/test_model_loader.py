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
from app.utils.model_loader import predict  # noqa: E402

test_text = "This is a contract agreement with automatic renewal and binding arbitration."

print("Testing model_loader.predict() directly...")
print(f"GEMINI_API_KEY set: {'GEMINI_API_KEY' in os.environ}")

result = predict(test_text)
print(f"Result type: {type(result)}")
print(f"Result: {result}")

if isinstance(result, dict):
    print(f"Keys: {list(result.keys())}")
    print(f"Category: {result.get('category', 'N/A')}")
    print(f"Risk level: {result.get('risk_level', 'N/A')}")
else:
    print("Result is not a dict")