"""
AI Legal Assistant package

Provides two main features:
- Legal Research Tool
- Contract Analysis & Compliance Checker

Designed to be web-backend ready (FastAPI/Flask) with async Gemini calls and
separate initialization for embeddings and database connections.

Top-level imports are lazy to avoid importing heavy dependencies at package
import time. Import submodules directly for explicit usage, e.g.:

    from ai_legal_assistant.research import legal_research, legal_research_async
    from ai_legal_assistant.contract import analyze_contract, analyze_contract_async
"""

from __future__ import annotations

from importlib import import_module
from typing import Any


def legal_research(*args: Any, **kwargs: Any):
    """Lazy wrapper for research. Prefer importing from submodule directly."""
    return import_module(".research", __name__).legal_research(*args, **kwargs)


def analyze_contract(*args: Any, **kwargs: Any):
    """Lazy wrapper for contract analysis. Prefer importing from submodule directly."""
    return import_module(".contract", __name__).analyze_contract(*args, **kwargs)


__all__ = ["legal_research", "analyze_contract"]
