import re
from typing import List, Dict, Any, Optional
from app.nlp.legal_patterns import (
    ENTITY_CATEGORIES,
    COURT_PATTERNS,
    STATUTE_PATTERNS,
    PROVISION_PATTERNS,
    CASE_NUMBER_PATTERNS,
    MONEY_PATTERNS,
    PERCENT_PATTERNS,
    EMAIL_PATTERN,
    PHONE_PATTERN,
    LEGAL_ROLE_PATTERNS,
    JUDGE_PATTERNS,
    ADVOCATE_PATTERNS,
    LEGAL_EVENT_PATTERNS,
    DATE_PATTERNS,
    ORG_PATTERNS,
    LOCATION_PATTERNS,
    PERSON_PATTERNS,
)

class LegalNERExtractor:
    """
    Robust Legal Named Entity Recognition engine for Indian and general legal documents.
    Combines rule-based grammar patterns, context heuristics, and regex extraction
    to achieve high precision and recall without unnecessary external API dependence.
    """

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        self.court_regex = [re.compile(p, re.IGNORECASE) for p in COURT_PATTERNS]
        self.statute_regex = [re.compile(p, re.IGNORECASE) for p in STATUTE_PATTERNS]
        self.provision_regex = [re.compile(p, re.IGNORECASE) for p in PROVISION_PATTERNS]
        self.case_no_regex = [re.compile(p, re.IGNORECASE) for p in CASE_NUMBER_PATTERNS]
        self.money_regex = [re.compile(p, re.IGNORECASE) for p in MONEY_PATTERNS]
        self.percent_regex = [re.compile(p, re.IGNORECASE) for p in PERCENT_PATTERNS]
        self.email_regex = re.compile(EMAIL_PATTERN, re.IGNORECASE)
        self.phone_regex = re.compile(PHONE_PATTERN)
        self.role_regex = [re.compile(p, re.IGNORECASE) for p in LEGAL_ROLE_PATTERNS]
        self.judge_regex = [re.compile(p) for p in JUDGE_PATTERNS]
        self.advocate_regex = [re.compile(p) for p in ADVOCATE_PATTERNS]
        self.event_regex = [re.compile(p, re.IGNORECASE) for p in LEGAL_EVENT_PATTERNS]
        self.date_regex = [re.compile(p, re.IGNORECASE) for p in DATE_PATTERNS]
        self.org_regex = [re.compile(p) for p in ORG_PATTERNS]
        self.location_regex = [re.compile(p) for p in LOCATION_PATTERNS]
        self.person_regex = [re.compile(p) for p in PERSON_PATTERNS]

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract all legal entities from text with exact character offsets.
        Resolves overlaps by giving precedence to more specific legal categories.
        """
        if not text or not text.strip():
            return []

        candidates: List[Dict[str, Any]] = []

        # 1. Contact Info
        for m in self.email_regex.finditer(text):
            candidates.append(self._build_candidate(m, "EMAIL", 0.99, "regex_deterministic"))
        for m in self.phone_regex.finditer(text):
            candidates.append(self._build_candidate(m, "PHONE", 0.95, "regex_deterministic"))

        # 2. Case Numbers & Citations
        for regex in self.case_no_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "CASE_NUMBER", 0.92, "legal_citation_pattern"))

        # 3. Judges & Advocates
        for regex in self.judge_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "JUDGE", 0.94, "judicial_title_pattern"))
        for regex in self.advocate_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "ADVOCATE", 0.92, "advocate_title_pattern"))

        # 4. Courts & Forums
        for regex in self.court_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "COURT", 0.95, "court_gazetteer"))

        # 5. Statutes & Provisions
        for regex in self.statute_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "STATUTE", 0.93, "statute_gazetteer"))
        for regex in self.provision_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "LEGAL_PROVISION", 0.90, "statutory_provision_pattern"))

        # 6. Legal Roles
        for regex in self.role_regex:
            for m in regex.finditer(text):
                # Ensure boundary context
                candidates.append(self._build_candidate(m, "LEGAL_ROLE", 0.88, "legal_role_lexicon"))

        # 7. Money & Percentage
        for regex in self.money_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "MONEY", 0.95, "financial_pattern"))
        for regex in self.percent_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "PERCENTAGE", 0.95, "percentage_pattern"))

        # 8. Dates & Legal Events
        for regex in self.date_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "DATE", 0.92, "temporal_pattern"))
        for regex in self.event_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "LEGAL_EVENT", 0.85, "legal_event_lexicon"))

        # 9. Organizations
        for regex in self.org_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "ORGANIZATION", 0.90, "corporate_suffix_pattern"))

        # 10. Locations
        for regex in self.location_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "LOCATION", 0.88, "geographic_gazetteer"))

        # 11. Persons (with honorifics or explicit name structure)
        for regex in self.person_regex:
            for m in regex.finditer(text):
                candidates.append(self._build_candidate(m, "PERSON", 0.85, "person_honorific_pattern"))

        # Resolve overlaps: Longer spans or higher priority categories win
        return self._resolve_overlaps(candidates)

    def _build_candidate(self, match: re.Match, label: str, confidence: float, source: str) -> Dict[str, Any]:
        val = match.group(0).strip()
        return {
            "text": val,
            "label": label,
            "start": match.start(),
            "end": match.end(),
            "confidence": confidence,
            "source": source,
            "normalized": self._normalize_entity(val, label)
        }

    def _normalize_entity(self, text: str, label: str) -> str:
        """Normalize values for clean filtering and deduplication."""
        cleaned = re.sub(r"\s+", " ", text).strip()
        if label == "MONEY":
            # Standardize symbol
            return cleaned.replace("Rs.", "₹").replace("Rs ", "₹").replace("INR ", "₹")
        if label == "DATE":
            return cleaned
        if label == "STATUTE":
            return cleaned.title()
        if label == "COURT":
            return cleaned.title()
        return cleaned

    def _resolve_overlaps(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out overlapping entity spans, keeping the most specific/highest priority."""
        if not candidates:
            return []

        # Category precedence map: higher number means higher priority when span overlaps
        priority = {
            "JUDGE": 10,
            "ADVOCATE": 9,
            "CASE_NUMBER": 8,
            "LEGAL_PROVISION": 7,
            "STATUTE": 6,
            "COURT": 5,
            "EMAIL": 5,
            "PHONE": 5,
            "MONEY": 5,
            "PERCENTAGE": 5,
            "ORGANIZATION": 4,
            "PERSON": 3,
            "LEGAL_ROLE": 3,
            "LEGAL_EVENT": 2,
            "DATE": 2,
            "LOCATION": 1,
        }

        # Sort primarily by start asc, length desc, then priority desc
        candidates.sort(
            key=lambda x: (
                x["start"],
                -(x["end"] - x["start"]),
                -priority.get(x["label"], 0)
            )
        )

        resolved: List[Dict[str, Any]] = []
        last_end = -1

        for cand in candidates:
            start = cand["start"]
            end = cand["end"]

            if start >= last_end:
                resolved.append(cand)
                last_end = end
            else:
                # Overlap detected
                prev = resolved[-1]
                cand_pri = priority.get(cand["label"], 0)
                prev_pri = priority.get(prev["label"], 0)
                cand_len = end - start
                prev_len = prev["end"] - prev["start"]

                # If current candidate has strictly higher priority or significantly longer span
                if cand_pri > prev_pri and cand_len >= prev_len:
                    resolved[-1] = cand
                    last_end = end

        return resolved
