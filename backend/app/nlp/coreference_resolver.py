import re
from typing import List, Dict, Any
from collections import defaultdict

class LegalCoreferenceResolver:
    """
    Groups references referring to the same entity within a legal document.
    Distinguishes confirmed lexical matches from uncertain contextual/role matches.
    """

    def resolve(self, entities: List[Dict[str, Any]], text: str) -> List[Dict[str, Any]]:
        """
        Group entities into coreference clusters.
        Returns a list of clusters with canonical name, entity type, and mentions.
        """
        if not entities:
            return []

        # Filter entities that typically have coreferences: PERSON, ORGANIZATION, LEGAL_ROLE
        target_labels = {"PERSON", "ORGANIZATION", "LEGAL_ROLE", "COURT", "ADVOCATE", "JUDGE"}
        filtered = [e for e in entities if e["label"] in target_labels]

        clusters: List[Dict[str, Any]] = []

        # Step 1: Exact and normalized string matching
        groups = defaultdict(list)
        for ent in filtered:
            clean_key = self._get_cluster_key(ent)
            groups[clean_key].append(ent)

        cluster_id = 1
        for key, mentions in groups.items():
            # Choose canonical mention (longest, most descriptive)
            canonical = max(mentions, key=lambda m: len(m["text"]))
            
            # Determine certainty
            is_confirmed = all(
                self._normalize_text(m["text"]) in self._normalize_text(canonical["text"]) or
                self._normalize_text(canonical["text"]) in self._normalize_text(m["text"])
                for m in mentions
            )

            clusters.append({
                "cluster_id": f"cluster_{cluster_id}",
                "canonical_name": canonical["text"],
                "label": canonical["label"],
                "is_confirmed": is_confirmed,
                "mention_count": len(mentions),
                "mentions": [
                    {
                        "text": m["text"],
                        "start": m["start"],
                        "end": m["end"],
                        "label": m["label"],
                        "confidence": m.get("confidence", 0.9)
                    }
                    for m in mentions
                ]
            })
            cluster_id += 1

        # Sort clusters by mention count descending
        clusters.sort(key=lambda c: c["mention_count"], reverse=True)
        return clusters

    def _get_cluster_key(self, entity: Dict[str, Any]) -> str:
        text = entity["text"].strip()
        label = entity["label"]

        # Remove titles / honorifics for matching
        cleaned = re.sub(r"^(?:Mr\.|Mrs\.|Ms\.|Dr\.|Shri|Smt\.|Hon'?ble|Justice)\s+", "", text, flags=re.IGNORECASE)
        # Remove corporate suffixes for organization matching
        cleaned = re.sub(r"\s+(?:Pvt\.?\s*Ltd\.?|Private\s+Limited|Ltd\.?|Limited|LLP|Inc\.?)$", "", cleaned, flags=re.IGNORECASE)
        
        return f"{label}_{cleaned.lower().strip()}"

    def _normalize_text(self, text: str) -> str:
        return re.sub(r"[^\w\s]", "", text).lower().strip()
