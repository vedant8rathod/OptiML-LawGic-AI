from __future__ import annotations

import json
from typing import Any, List, Sequence
import os


class AiLegalAssistantModel:
    """
    Picklable wrapper with .predict() returning JSON strings.
    Real LLM path uses Gemini when AI_LEGAL_USE_REAL=1 and GOOGLE_API_KEY is set.
    Falls back to simulated deterministic output otherwise.
    """

    def __init__(self, task: str = "contract") -> None:
        self.task = task

    def _predict_single(self, text: str) -> str:
        try:
            use_real = bool(os.getenv("AI_LEGAL_USE_REAL", "").strip()) and bool(os.getenv("GOOGLE_API_KEY", "").strip())
            if self.task == "contract":
                if use_real:
                    try:
                        import google.generativeai as genai
                        genai.configure(api_key=os.environ["GOOGLE_API_KEY"].strip())
                        prompt = (
                            "You are a contract analysis assistant. Analyze the following text and return a JSON array of objects with keys: "
                            "clause (string), risk (High|Medium|Low), rewrite (string), explanation (string). Respond with JSON only.\n\n"
                            f"Text:\n{text}\n\nJSON:"
                        )
                        model = genai.GenerativeModel("gemini-1.5-pro")
                        resp = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                        content = resp.text if hasattr(resp, "text") else str(resp)
                        try:
                            result = json.loads(content)
                        except Exception:
                            resp2 = model.generate_content(prompt + "\nReturn STRICT JSON only with no prose.", generation_config={"response_mime_type": "application/json"})
                            content2 = resp2.text if hasattr(resp2, "text") else str(resp2)
                            result = json.loads(content2)
                        return json.dumps(result)
                    except Exception:
                        pass
                result = [
                    {
                        "clause": "The Supplier may terminate this Agreement at any time without prior notice.",
                        "risk": "High",
                        "rewrite": (
                            "The Supplier may terminate this Agreement for convenience upon thirty (30) days' prior written notice. "
                            "This clause does not limit either party's right to terminate for cause, including material breach."
                        ),
                        "explanation": (
                            "Unconditional termination without notice is high risk due to fairness and potential unconscionability. "
                            "Introducing a notice period and preserving for-cause rights reduces risk while maintaining flexibility."
                        ),
                    },
                    {
                        "clause": "All disputes shall be resolved exclusively in Supplier's home jurisdiction.",
                        "risk": "Medium",
                        "rewrite": (
                            "All disputes shall be resolved in the courts of [Mutually Agreed Jurisdiction], subject to mandatory consumer protection or employment laws, if applicable."
                        ),
                        "explanation": (
                            "Exclusive jurisdiction heavily favoring one party can be unreasonable; offering a mutually agreed forum and acknowledging mandatory laws improves enforceability."
                        ),
                    },
                ]
                return json.dumps(result)
            else:
                if use_real:
                    try:
                        import google.generativeai as genai
                        genai.configure(api_key=os.environ["GOOGLE_API_KEY"].strip())
                        prompt = (
                            "You are a legal research assistant. Summarize the question and return JSON with keys: "
                            "summary (string), key_cases (array of strings), timeline (array of {date,event,case_id}). Respond with JSON only.\n\n"
                            f"Query:\n{text}\n\nJSON:"
                        )
                        model = genai.GenerativeModel("gemini-1.5-pro")
                        resp = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
                        content = resp.text if hasattr(resp, "text") else str(resp)
                        try:
                            data = json.loads(content)
                        except Exception:
                            resp2 = model.generate_content(prompt + "\nReturn STRICT JSON only with no prose.", generation_config={"response_mime_type": "application/json"})
                            content2 = resp2.text if hasattr(resp2, "text") else str(resp2)
                            data = json.loads(content2)
                        return json.dumps(data)
                    except Exception:
                        pass
                data = {"summary": "Concise legal summary unavailable (simulation mode).", "key_cases": [], "timeline": []}
                return json.dumps(data)
        except Exception as e:
            return f"ai_legal_assistant unavailable or failed: {e}"

    def predict(self, X: Any) -> List[str]:
        if isinstance(X, str):
            return [self._predict_single(X)]
        if isinstance(X, Sequence):
            return [self._predict_single(str(x)) for x in X]
        return [self._predict_single(str(X))]
