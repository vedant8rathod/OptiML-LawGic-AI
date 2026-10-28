from __future__ import annotations

import asyncio
from typing import List

from typing import List

from .core.config import settings
from .core.ner import split_into_clauses, extract_entities
from .core.types import ClauseAnalysis, ClauseAnalysisList
from .core.gemini import ensure_gemini_configured


async def _analyze_clause(clause: str) -> ClauseAnalysis:
    """Analyze a single clause: risk level, rewrite, explanation using Gemini."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    ensure_gemini_configured()
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=settings.google_api_key, temperature=0.2)
    system = (
        "You are a legal compliance and contract risk analyst."
        " Classify risk as Low/Medium/High, explain the reasoning, and propose a compliant rewrite"
        " that preserves intent and aligns with common regulatory and best-practice standards."
    )
    prompt = (
        f"{system}\n\nClause:\n{clause}\n\n"
        "Return STRICT JSON with keys: risk (Low|Medium|High), rewrite (string), explanation (string)."
    )
    res = await llm.ainvoke(prompt)
    import json

    text = res.content if hasattr(res, "content") else str(res)
    try:
        data = json.loads(text)
    except Exception:
        # Fallback parsing heuristics
        data = {"risk": "Medium", "rewrite": clause, "explanation": text[:1000]}

    # Normalize risk
    risk = str(data.get("risk", "Medium")).capitalize()
    if risk not in {"Low", "Medium", "High"}:
        risk = "Medium"

    return ClauseAnalysis(
        clause=clause,
        risk=risk,  # type: ignore[arg-type]
        rewrite=str(data.get("rewrite", clause)),
        explanation=str(data.get("explanation", "")),
    )


async def analyze_contract_async(text: str, max_concurrency: int = 5) -> ClauseAnalysisList:
    """Async contract analysis across clauses with bounded concurrency."""
    clauses = split_into_clauses(text)
    _ = extract_entities(text)  # reserved for future rule-based checks

    sem = asyncio.Semaphore(max_concurrency)

    async def _task(c: str):
        async with sem:
            return await _analyze_clause(c)

    results = await asyncio.gather(*[_task(c) for c in clauses])
    return results


def analyze_contract(text: str, max_concurrency: int = 5) -> ClauseAnalysisList:
    """Sync wrapper for environments that cannot run async easily."""
    return asyncio.run(analyze_contract_async(text, max_concurrency=max_concurrency))
