import os
import joblib

# Allow overriding model path via env; default to /opt/app/models/model.pkl in container
MODEL_PATH = os.getenv("MODEL_PATH") or os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models/model.pkl"))

# Try to load the model
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"⚠️ Failed to load model: {e}")

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