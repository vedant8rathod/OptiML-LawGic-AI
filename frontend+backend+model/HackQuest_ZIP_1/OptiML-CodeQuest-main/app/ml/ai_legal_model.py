from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, List, Sequence
import os


class AiLegalAssistantModel:
    """
    A thin, picklable wrapper that adapts ai_legal_assistant into a scikit-learn-like
    interface with .predict(). Intended for use with joblib.load in the backend.

    Note: This does NOT freeze remote LLMs or databases into the pickle; it simply
    packages a Python class that, when loaded, will call into the live
    ai_legal_assistant code available in the environment.
    """

    def __init__(self, task: str = "contract") -> None:
        self.task = task  # "contract" or "research" (default contract)

    def _ensure_project_on_path(self) -> None:
        """Attempt to ensure the repo root is importable for ai_legal_assistant."""
        here = Path(__file__).resolve()
        # Try a few parent levels up to find ai_legal_assistant
        for up in range(1, 7):
            candidate = here.parents[up - 1].parents[0] if up == 1 else here.parents[up - 1]
            if (candidate / "ai_legal_assistant").exists():
                if str(candidate) not in sys.path:
                    sys.path.insert(0, str(candidate))
                break

    def _predict_single(self, text: str) -> str:
        self._ensure_project_on_path()
        try:
            # Use simulated outputs unless explicitly told to use real LLMs
            use_real = bool(os.getenv("AI_LEGAL_USE_REAL", "").strip()) and bool(os.getenv("GOOGLE_API_KEY", "").strip())
            if self.task == "contract":
                if use_real:
                    from ai_legal_assistant.contract import analyze_contract
                    result = analyze_contract(text)
                else:
                    from ai_legal_assistant.samples import simulate_contract_analysis_output
                    result = simulate_contract_analysis_output()
                return json.dumps(result)
            else:
                if use_real:
                    from ai_legal_assistant.research import legal_research
                    result = legal_research(text)
                else:
                    from ai_legal_assistant.samples import simulate_legal_research_output
                    result = simulate_legal_research_output()
                return json.dumps(result)
        except Exception as e:
            return f"ai_legal_assistant unavailable or failed: {e}"

    def predict(self, X: Any) -> List[str]:
        """Sklearn-like predict. Accepts string or sequence of strings. Returns list of strings."""
        if isinstance(X, str):
            return [self._predict_single(X)]
        if isinstance(X, Sequence):
            return [self._predict_single(str(x)) for x in X]
        return [self._predict_single(str(X))]
