import pytest
from app.nlp.ner_engine import LegalNERExtractor
from app.nlp.relation_extractor import LegalRelationExtractor
from app.nlp.coreference_resolver import LegalCoreferenceResolver
from app.nlp.timeline_generator import LegalTimelineGenerator
from app.nlp.privacy_redactor import LegalPrivacyRedactor
from app.nlp.entity_service import entity_intelligence_service

@pytest.fixture
def sample_legal_text():
    return (
        "In the Supreme Court of India, Writ Petition (Civil) No. 402 of 2021 was heard by Hon'ble Chief Justice D.Y. Chandrachud. "
        "The Petitioner, ABC Technologies Pvt. Ltd., represented by Mr. Harish Salve, Senior Advocate, filed the petition on 15/08/2021. "
        "The Petitioner claimed damages of ₹5,00,000 from Respondent Mr. Rajesh Sharma pursuant to Section 138 of the Negotiable Instruments Act. "
        "For notices, contact legal@abctech.com or +91 98765 43210 in New Delhi."
    )

def test_person_and_org_extraction(sample_legal_text):
    ner = LegalNERExtractor()
    entities = ner.extract_entities(sample_legal_text)
    texts = [e["text"] for e in entities]
    labels = {e["text"]: e["label"] for e in entities}

    assert any("ABC Technologies Pvt. Ltd." in t for t in texts)
    assert any("Mr. Rajesh Sharma" in t for t in texts)

def test_indian_court_and_statute(sample_legal_text):
    ner = LegalNERExtractor()
    entities = ner.extract_entities(sample_legal_text)
    labels = {e["text"]: e["label"] for e in entities}

    assert "Supreme Court of India" in labels
    assert labels["Supreme Court of India"] == "COURT"
    assert any("Negotiable Instruments Act" in k for k in labels)

def test_legal_provision_and_case_number(sample_legal_text):
    ner = LegalNERExtractor()
    entities = ner.extract_entities(sample_legal_text)
    labels = {e["text"]: e["label"] for e in entities}

    assert any("Section 138" in k for k in labels)
    assert any("Writ Petition" in k and "402 of 2021" in k for k in labels)

def test_indian_currency_and_date(sample_legal_text):
    ner = LegalNERExtractor()
    entities = ner.extract_entities(sample_legal_text)
    labels = {e["text"]: e["label"] for e in entities}

    assert "₹5,00,000" in labels
    assert labels["₹5,00,000"] == "MONEY"
    assert "15/08/2021" in labels
    assert labels["15/08/2021"] == "DATE"

def test_character_offsets(sample_legal_text):
    ner = LegalNERExtractor()
    entities = ner.extract_entities(sample_legal_text)
    for ent in entities:
        extracted = sample_legal_text[ent["start"]:ent["end"]]
        assert extracted == ent["text"], f"Offset mismatch: expected '{ent['text']}', got '{extracted}'"

def test_relation_extraction(sample_legal_text):
    ner = LegalNERExtractor()
    entities = ner.extract_entities(sample_legal_text)
    rel_extractor = LegalRelationExtractor()
    relations = rel_extractor.extract_relations(sample_legal_text, entities)

    rel_types = [r["relation_type"] for r in relations]
    assert len(relations) > 0
    assert "represented_by" in rel_types or "heard_by" in rel_types or "contained_in" in rel_types

def test_coreference_resolution(sample_legal_text):
    ner = LegalNERExtractor()
    entities = ner.extract_entities(sample_legal_text)
    coref = LegalCoreferenceResolver()
    clusters = coref.resolve(entities, sample_legal_text)

    assert isinstance(clusters, list)
    assert len(clusters) > 0

def test_timeline_generator(sample_legal_text):
    ner = LegalNERExtractor()
    entities = ner.extract_entities(sample_legal_text)
    timeline_gen = LegalTimelineGenerator()
    events = timeline_gen.generate_timeline(sample_legal_text, entities)

    assert len(events) >= 1
    assert events[0]["date"] == "15/08/2021"

def test_privacy_redaction(sample_legal_text):
    redactor = LegalPrivacyRedactor()
    ner = LegalNERExtractor()
    entities = ner.extract_entities(sample_legal_text)
    res = redactor.redact_text(sample_legal_text, entities, labels_to_redact=["PERSON", "EMAIL", "PHONE", "MONEY"])

    assert "legal@abctech.com" not in res["redacted_text"]
    assert "98765" not in res["redacted_text"]
    assert "₹5,00,000" not in res["redacted_text"]
    assert "[EMAIL_REDACTED]" in res["redacted_text"]
    assert "[PHONE_REDACTED]" in res["redacted_text"]
    assert res["redacted_count"] >= 4

def test_empty_input_handling():
    service = entity_intelligence_service
    res = service.process_document("")
    assert res["stats"]["total_entities"] == 0
    assert res["entities"] == []
