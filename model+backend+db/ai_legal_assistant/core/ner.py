from __future__ import annotations

from typing import List, Dict, Optional
import re

from .config import settings

_nlp = None
_HAS_SPACY = None  # type: Optional[bool]


def _import_spacy():
    global _HAS_SPACY
    if _HAS_SPACY is not None:
        return _HAS_SPACY
    try:
        import spacy  # type: ignore
        _HAS_SPACY = True
        return True
    except Exception:
        _HAS_SPACY = False
        return False


def get_nlp():
    if not _import_spacy():
        return None
    global _nlp
    if _nlp is None:
        import spacy  # type: ignore
        try:
            _nlp = spacy.load(settings.spacy_model)
        except Exception:
            try:
                _nlp = spacy.load("en_core_web_sm")
            except Exception:
                _nlp = None
    return _nlp


def extract_entities(text: str) -> Dict[str, List[str]]:
    """Extract named entities; returns empty dict if spaCy unavailable."""
    nlp = get_nlp()
    if nlp is None:
        return {}
    doc = nlp(text)
    entities: Dict[str, List[str]] = {}
    for ent in getattr(doc, "ents", []):
        entities.setdefault(ent.label_, []).append(ent.text)
    for k, v in entities.items():
        entities[k] = list(dict.fromkeys(v))
    return entities


def split_into_clauses(text: str) -> List[str]:
    """Clause segmentation.

    Uses spaCy sentence boundaries when available; otherwise falls back to
    regex-based splitting on punctuation and newlines.
    """
    nlp = get_nlp()
    parts: List[str] = []
    if nlp is not None:
        doc = nlp(text)
        for sent in doc.sents:
            subparts = [p.strip() for p in sent.text.split(";") if p.strip()]
            parts.extend(subparts)
    else:
        # Fallback: split on ; . : and newlines conservatively
        rough = re.split(r"[;\n]|(?<=[.!?])\s+", text)
        parts = [p.strip() for p in rough if p and len(p.strip()) > 0]
    # Filter very short fragments
    return [p for p in parts if len(p) > 10]
