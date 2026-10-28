from __future__ import annotations

# Thin wrapper at project root for convenience
# Builds models/model.pkl using AiLegalAssistantModel

import os
from pathlib import Path
import joblib

try:
    from app.ml.ai_legal_model import AiLegalAssistantModel
except Exception as e:
    raise SystemExit(f"Failed to import AiLegalAssistantModel: {e}")


def main() -> None:
    task = os.getenv("AI_LEGAL_TASK", "contract")
    model = AiLegalAssistantModel(task=task)

    out_dir = Path(__file__).resolve().parent / "models"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "model.pkl"

    joblib.dump(model, out_file)
    print(f"✅ Wrote {out_file}")


if __name__ == "__main__":
    main()
