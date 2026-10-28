import os
import joblib
from pathlib import Path

# Resolve model path with fallbacks
def _resolve_model_path() -> str:
    env_path = os.getenv("MODEL_PATH", "").strip()
    if env_path:
        return env_path
    base = Path(__file__).resolve().parents[2]
    candidates = [
        base / "models" / "model.pkl",
        base / "data" / "models" / "model.pkl",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return str(base / "models" / "model.pkl")

MODEL_PATH = _resolve_model_path()

# Try to load the model
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"⚠️ Failed to load model from {MODEL_PATH}: {e}")

def predict(text: str):
    """
    Predict using the loaded model.
    Accepts combined input text (from text, file, or voice).
    Returns model output or a message if the model is not loaded.
    """
    if not model:
        return "⚠️ Model not loaded. Please check model.pkl path or validity."

    # TODO: Add preprocessing if your model expects vectorized input
    # For example, TF-IDF transform or embedding generation

    # Ensure input is a list for sklearn-like models
    try:
        result = model.predict([text])[0]
    except Exception as e:
        result = f"⚠️ Prediction failed: {e}"
    
    return result