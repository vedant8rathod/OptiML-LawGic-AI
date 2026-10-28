from __future__ import annotations

"""Offline sample outputs for quick verification without external services.

Use these to validate wiring without needing Postgres, pgvector, or Gemini.
"""

from typing import List

from .core.types import ResearchResult, ClauseAnalysisList


def simulate_legal_research_output() -> ResearchResult:
    return {
        "summary": (
            "Based on the retrieved materials, the doctrine of promissory estoppel prevents a party from"
            " going back on clear promises when the other party has relied upon them to their detriment."
            " The cases indicate courts assess clarity of representation, reliance, and equities."
        ),
        "key_cases": [
            "Motilal Padampat Sugar Mills Co. Ltd. v. State of Uttar Pradesh",
            "Union of India v. Anglo Afghan Agencies",
            "Delhi Cloth & General Mills Co. Ltd. v. Union of India",
        ],
        "timeline": [
            {"date": "1962-12-05", "event": "Promissory estoppel recognized in export promotion scheme", "case_id": "UOI v. Anglo Afghan Agencies"},
            {"date": "1979-12-13", "event": "Expanded equitable application in fiscal matters", "case_id": "Motilal Padampat"},
        ],
    }


def simulate_contract_analysis_output() -> ClauseAnalysisList:
    return [
        {
            "clause": "The Supplier may terminate this Agreement at any time without prior notice.",
            "risk": "High",
            "rewrite": (
                "The Supplier may terminate this Agreement for convenience upon thirty (30) days' prior written notice."
                " This clause does not limit either party's right to terminate for cause, including material breach."
            ),
            "explanation": (
                "Unconditional termination without notice is high risk due to fairness and potential unconscionability."
                " Introducing a notice period and preserving for-cause rights reduces risk while maintaining flexibility."
            ),
        },
        {
            "clause": "All disputes shall be resolved exclusively in Supplier's home jurisdiction.",
            "risk": "Medium",
            "rewrite": (
                "All disputes shall be resolved in the courts of [Mutually Agreed Jurisdiction],"
                " subject to mandatory consumer protection or employment laws, if applicable."
            ),
            "explanation": (
                "Exclusive jurisdiction heavily favoring one party can be unreasonable; offering a mutually agreed forum"
                " and acknowledging mandatory laws improves enforceability."
            ),
        },
    ]
