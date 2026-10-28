from __future__ import annotations

from typing import List, Literal, Optional, TypedDict


class TimelineItem(TypedDict, total=False):
    date: str
    event: str
    case_id: Optional[str]


class ResearchResult(TypedDict):
    """Structured output for the Legal Research tool."""

    summary: str
    key_cases: List[str]
    timeline: List[TimelineItem]


class ClauseAnalysis(TypedDict):
    """Structured output item per clause for Contract Analysis."""

    clause: str
    risk: Literal["Low", "Medium", "High"]
    rewrite: str
    explanation: str


ClauseAnalysisList = List[ClauseAnalysis]
