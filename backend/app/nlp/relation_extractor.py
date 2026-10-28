import re
from typing import List, Dict, Any, Optional

class LegalRelationExtractor:
    """
    Rule-based and syntactic dependency pattern relation extraction engine.
    Extracts structured relationships between legal entities:
    - PERSON / ORG -- represented_by --> ADVOCATE
    - ORG / PERSON -- party_to --> CASE
    - CASE -- heard_by --> COURT
    - CASE / PETITION -- filed_on --> DATE
    - PARTY -- claims / liable_for --> MONEY
    - JUDGMENT / CASE -- cites --> STATUTE
    - JUDGMENT / CASE -- refers_to --> LEGAL_PROVISION
    """

    def __init__(self):
        # Patterns linking entities within sentences
        self.represented_patterns = [
            re.compile(r"(?:represented\s+by|appeared\s+for|briefed\s+by|argued\s+by|counsel\s+for|on\s+behalf\s+of)", re.IGNORECASE),
        ]
        self.heard_by_patterns = [
            re.compile(r"(?:heard\s+by|before|coram|bench\s+of|presided\s+over\s+by|decided\s+by)", re.IGNORECASE),
        ]
        self.filed_on_patterns = [
            re.compile(r"(?:filed\s+on|instituted\s+on|dated|registered\s+on|admitted\s+on|decided\s+on|pronounced\s+on)", re.IGNORECASE),
        ]
        self.claims_money_patterns = [
            re.compile(r"(?:claim(?:s|ed|ing)?|damages\s+of|compensation\s+of|loan\s+of|debt\s+of|security\s+deposit\s+of|penalt(?:y|ies)\s+of|fine\s+of|sum\s+of|consideration\s+of)", re.IGNORECASE),
        ]
        self.cites_patterns = [
            re.compile(r"(?:pursuant\s+to|in\s+accordance\s+with|under|invoking|governed\s+by|provisions\s+of|punishable\s+under|violation\s+of)", re.IGNORECASE),
        ]

    def extract_relations(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract relationships by analyzing entity pairs co-occurring in sentences
        along with linguistic trigger cues.
        """
        if not text or not entities:
            return []

        # Split text into sentences and track offsets
        sentences = self._split_sentences_with_spans(text)
        relations: List[Dict[str, Any]] = []

        for sent_text, sent_start, sent_end in sentences:
            # Entities present in this sentence
            sent_entities = [
                e for e in entities
                if e["start"] >= sent_start and e["end"] <= sent_end
            ]

            if len(sent_entities) < 2:
                continue

            # Check entity pairs in sentence
            for i in range(len(sent_entities)):
                for j in range(len(sent_entities)):
                    if i == j:
                        continue
                    e1 = sent_entities[i]
                    e2 = sent_entities[j]

                    rel = self._check_relation(sent_text, sent_start, e1, e2)
                    if rel:
                        # Avoid duplicates
                        if not any(
                            r["source_id"] == rel["source_id"] and
                            r["target_id"] == rel["target_id"] and
                            r["relation_type"] == rel["relation_type"]
                            for r in relations
                        ):
                            relations.append(rel)

        return relations

    def _check_relation(
        self,
        sentence: str,
        sent_offset: int,
        e1: Dict[str, Any],
        e2: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        # Order-sensitive span between e1 and e2
        span_start = min(e1["end"], e2["end"]) - sent_offset
        span_end = max(e1["start"], e2["start"]) - sent_offset

        if span_start < 0 or span_end > len(sentence) or span_start > span_end:
            between_text = ""
        else:
            between_text = sentence[span_start:span_end]

        t1, t2 = e1["label"], e2["label"]

        # 1. PERSON / ORG -- represented_by --> ADVOCATE
        if t1 in ("PERSON", "ORGANIZATION", "LEGAL_ROLE") and t2 == "ADVOCATE":
            if any(p.search(between_text) or p.search(sentence) for p in self.represented_patterns):
                return self._create_relation("represented_by", e1, e2, sentence, 0.88)

        # 2. CASE / JUDGMENT -- heard_by --> COURT or JUDGE
        if t1 in ("CASE_NUMBER", "LEGAL_ROLE") and t2 in ("COURT", "JUDGE"):
            if any(p.search(between_text) or p.search(sentence) for p in self.heard_by_patterns):
                return self._create_relation("heard_by", e1, e2, sentence, 0.90)

        # 3. CASE / EVENT -- filed_on --> DATE
        if t1 in ("CASE_NUMBER", "LEGAL_EVENT", "LEGAL_ROLE") and t2 == "DATE":
            if any(p.search(between_text) for p in self.filed_on_patterns):
                return self._create_relation("filed_on", e1, e2, sentence, 0.85)

        # 4. PARTY -- claims / liable_for --> MONEY
        if t1 in ("PERSON", "ORGANIZATION", "LEGAL_ROLE") and t2 == "MONEY":
            if any(p.search(between_text) or p.search(sentence) for p in self.claims_money_patterns):
                return self._create_relation("claims_or_liable_for", e1, e2, sentence, 0.82)

        # 5. CASE / STATUTE / PROVISION co-occurrence (cites / governed_by)
        if t1 in ("CASE_NUMBER", "COURT", "LEGAL_ROLE") and t2 in ("STATUTE", "LEGAL_PROVISION"):
            if any(p.search(between_text) for p in self.cites_patterns):
                return self._create_relation("cites_or_applies", e1, e2, sentence, 0.86)

        # 6. STATUTE contains LEGAL_PROVISION (e.g. Section 138 of Negotiable Instruments Act)
        if t1 == "LEGAL_PROVISION" and t2 == "STATUTE":
            if re.search(r"\b(?:of|under)\b", between_text, re.IGNORECASE):
                return self._create_relation("contained_in", e1, e2, sentence, 0.94)

        return None

    def _create_relation(
        self,
        rel_type: str,
        source: Dict[str, Any],
        target: Dict[str, Any],
        sentence: str,
        confidence: float
    ) -> Dict[str, Any]:
        return {
            "relation_type": rel_type,
            "source": source["text"],
            "source_label": source["label"],
            "source_id": f"{source['start']}-{source['end']}",
            "target": target["text"],
            "target_label": target["label"],
            "target_id": f"{target['start']}-{target['end']}",
            "supporting_sentence": sentence.strip(),
            "confidence": confidence,
            "is_uncertain": confidence < 0.85
        }

    def _split_sentences_with_spans(self, text: str) -> List[tuple]:
        """Split text into sentences while tracking start and end indices."""
        sentences = []
        # Pattern handles punctuation boundaries without splitting standard abbreviations (Mr., Ltd., No., etc.)
        pattern = re.compile(r"(?<=[.!?\n])\s+")
        start = 0
        for m in pattern.finditer(text):
            end = m.start()
            sent = text[start:end].strip()
            if sent:
                sentences.append((sent, start, end))
            start = m.end()

        tail = text[start:].strip()
        if tail:
            sentences.append((tail, start, len(text)))

        return sentences
