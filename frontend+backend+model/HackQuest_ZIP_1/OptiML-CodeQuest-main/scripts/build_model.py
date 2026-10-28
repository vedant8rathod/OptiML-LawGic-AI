from __future__ import annotations

import os
from pathlib import Path

import joblib

from app.ml.ai_legal_model import AiLegalAssistantModel


def main() -> None:
    # Choose task via env or default to contract analysis
    task = os.getenv("AI_LEGAL_TASK", "contract")  # "contract" or "research"
    model = AiLegalAssistantModel(task=task)

    out_dir = Path(__file__).resolve().parents[1] / "models"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "model.pkl"

    joblib.dump(model, out_file)
    print(f"✅ Wrote {out_file}")


if __name__ == "__main__":
    main()
