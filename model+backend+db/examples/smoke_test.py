from __future__ import annotations

import json
import os
import sys
from pathlib import Path
import importlib.util

# Ensure repo root is on sys.path when executed from examples/
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_legal_assistant.samples import (
    simulate_contract_analysis_output,
    simulate_legal_research_output,
)


def main() -> None:
    query = os.getenv("TEST_QUERY", "doctrine of promissory estoppel in India")
    contract = os.getenv(
        "TEST_CONTRACT",
        "The Supplier may terminate this Agreement at any time without prior notice; All disputes shall be resolved exclusively in Supplier's home jurisdiction.",
    )

    # Determine paths: allow contract analysis to run real if only GOOGLE_API_KEY is set
    has_key = bool(os.getenv("GOOGLE_API_KEY"))
    has_db = bool(os.getenv("DATABASE_URL"))

    def _has_module(name: str) -> bool:
        return importlib.util.find_spec(name) is not None

    has_lc = _has_module("langchain")
    has_gemini = _has_module("langchain_google_genai")

    research_out = simulate_legal_research_output()
    contract_out = simulate_contract_analysis_output()

    # Try real research only if both are present and modules available
    if has_key and has_db and has_lc and has_gemini:
        try:
            from ai_legal_assistant.research import legal_research
            research_out = legal_research(query, top_k=3)
        except Exception:
            # Silent fallback to simulation
            pass

    # Try real contract analysis if key and module are present
    if has_key and has_gemini:
        try:
            from ai_legal_assistant.contract import analyze_contract
            contract_out = analyze_contract(contract)
        except Exception:
            # Silent fallback to simulation
            pass

    print(json.dumps({"research": research_out, "contract": contract_out}, indent=2))


if __name__ == "__main__":
    main()
