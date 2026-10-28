from typing import Dict, Any, List
from collections import defaultdict
from app.nlp.ner_engine import LegalNERExtractor
from app.nlp.relation_extractor import LegalRelationExtractor
from app.nlp.coreference_resolver import LegalCoreferenceResolver
from app.nlp.timeline_generator import LegalTimelineGenerator
from app.nlp.privacy_redactor import LegalPrivacyRedactor

class LegalEntityIntelligenceService:
    """
    Unified Orchestrator for Legal Entity Intelligence:
    1. Named Entity Recognition
    2. Grouped Entity Explorer & Deduplication
    3. Relationship Extraction
    4. Coreference Resolution
    5. Case Timeline Construction
    6. Privacy Redaction
    """

    def __init__(self):
        self.ner_extractor = LegalNERExtractor()
        self.relation_extractor = LegalRelationExtractor()
        self.coref_resolver = LegalCoreferenceResolver()
        self.timeline_generator = LegalTimelineGenerator()
        self.redactor = LegalPrivacyRedactor()

    def process_document(self, text: str) -> Dict[str, Any]:
        """Process legal document text and return comprehensive intelligence payload."""
        if not text or not text.strip():
            return {
                "text": "",
                "entities": [],
                "grouped_entities": {},
                "relations": [],
                "coreference_clusters": [],
                "timeline": [],
                "stats": {
                    "total_entities": 0,
                    "unique_entities": 0,
                    "total_relations": 0,
                    "timeline_events": 0
                }
            }

        # 1. Extract NER spans
        entities = self.ner_extractor.extract_entities(text)

        # 2. Group & Deduplicate for Entity Explorer
        grouped_entities = self._group_entities(entities)

        # 3. Extract Relationships
        relations = self.relation_extractor.extract_relations(text, entities)

        # 4. Coreference Resolution
        coref_clusters = self.coref_resolver.resolve(entities, text)

        # 5. Timeline Generation
        timeline = self.timeline_generator.generate_timeline(text, entities)

        unique_texts = set(e["text"].lower().strip() for e in entities)

        return {
            "text": text,
            "entities": entities,
            "grouped_entities": grouped_entities,
            "relations": relations,
            "coreference_clusters": coref_clusters,
            "timeline": timeline,
            "stats": {
                "total_entities": len(entities),
                "unique_entities": len(unique_texts),
                "total_relations": len(relations),
                "timeline_events": len(timeline),
            }
        }

    def redact_document(
        self,
        text: str,
        labels_to_redact: List[str] = None
    ) -> Dict[str, Any]:
        """Redact sensitive PII from text."""
        entities = self.ner_extractor.extract_entities(text)
        return self.redactor.redact_text(text, entities, labels_to_redact)

    def _group_entities(self, entities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group and deduplicate entities for structured Explorer view."""
        grouped = defaultdict(dict)

        category_mapping = {
            "PERSON": "People & Legal Professionals",
            "ADVOCATE": "People & Legal Professionals",
            "JUDGE": "People & Legal Professionals",
            "LEGAL_ROLE": "People & Legal Professionals",
            "ORGANIZATION": "Organizations & Parties",
            "COURT": "Courts & Locations",
            "LOCATION": "Courts & Locations",
            "STATUTE": "Statutes & Provisions",
            "LEGAL_PROVISION": "Statutes & Provisions",
            "DATE": "Dates & Legal Events",
            "LEGAL_EVENT": "Dates & Legal Events",
            "MONEY": "Monetary & Financial",
            "PERCENTAGE": "Monetary & Financial",
            "CASE_NUMBER": "Case Identifiers",
            "EMAIL": "Contact Information",
            "PHONE": "Contact Information",
        }

        for ent in entities:
            group_name = category_mapping.get(ent["label"], "Other Entities")
            norm_key = ent.get("normalized", ent["text"]).strip().lower()

            if norm_key not in grouped[group_name]:
                grouped[group_name][norm_key] = {
                    "text": ent["text"],
                    "normalized": ent.get("normalized", ent["text"]),
                    "label": ent["label"],
                    "confidence": ent.get("confidence", 0.9),
                    "occurrences": [
                        {
                            "start": ent["start"],
                            "end": ent["end"],
                            "text": ent["text"]
                        }
                    ]
                }
            else:
                grouped[group_name][norm_key]["occurrences"].append({
                    "start": ent["start"],
                    "end": ent["end"],
                    "text": ent["text"]
                })

        return {k: list(v.values()) for k, v in grouped.items()}

# Global singleton
entity_intelligence_service = LegalEntityIntelligenceService()
