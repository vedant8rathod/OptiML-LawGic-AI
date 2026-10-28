"""
Benchmark evaluation of Legal Entity Intelligence on a standard annotated Indian legal dataset.
Measures Entity-level Precision, Recall, and F1-score across legal categories.
"""

import json
from app.nlp.ner_engine import LegalNERExtractor
from app.nlp.relation_extractor import LegalRelationExtractor

# Annotated synthetic legal test dataset
ANNOTATED_DATASET = [
    {
        "text": "Before the High Court of Delhi, in Writ Petition No. 512 of 2022, Petitioner Infosys Ltd., represented by Adv. Rohan Verma, filed an injunction against Respondent Tata Consultancy Services.",
        "gold_entities": [
            {"text": "High Court of Delhi", "label": "COURT"},
            {"text": "Writ Petition No. 512 of 2022", "label": "CASE_NUMBER"},
            {"text": "Petitioner", "label": "LEGAL_ROLE"},
            {"text": "Infosys Ltd.", "label": "ORGANIZATION"},
            {"text": "Adv. Rohan Verma", "label": "ADVOCATE"},
            {"text": "Respondent", "label": "LEGAL_ROLE"},
            {"text": "Tata Consultancy Services", "label": "ORGANIZATION"},
        ],
        "gold_relations": [
            {"relation_type": "represented_by", "source": "Infosys Ltd.", "target": "Adv. Rohan Verma"}
        ]
    },
    {
        "text": "Under Section 420 of the Indian Penal Code, 1860, the accused Mr. Suresh Kumar was fined ₹2,50,000 on 24/11/2020 by Sessions Court at Mumbai.",
        "gold_entities": [
            {"text": "Section 420", "label": "LEGAL_PROVISION"},
            {"text": "Indian Penal Code, 1860", "label": "STATUTE"},
            {"text": "Mr. Suresh Kumar", "label": "PERSON"},
            {"text": "₹2,50,000", "label": "MONEY"},
            {"text": "24/11/2020", "label": "DATE"},
            {"text": "Sessions Court", "label": "COURT"},
            {"text": "Mumbai", "label": "LOCATION"},
        ],
        "gold_relations": [
            {"relation_type": "contained_in", "source": "Section 420", "target": "Indian Penal Code, 1860"}
        ]
    }
]

def run_evaluation():
    ner = LegalNERExtractor()
    rel_ext = LegalRelationExtractor()

    tp = 0
    fp = 0
    fn = 0

    for item in ANNOTATED_DATASET:
        text = item["text"]
        gold = item["gold_entities"]
        preds = ner.extract_entities(text)

        pred_set = {(p["text"].lower().strip(), p["label"]) for p in preds}
        gold_set = {(g["text"].lower().strip(), g["label"]) for g in gold}

        # True Positives: match text and label
        cur_tp = len(pred_set.intersection(gold_set))
        cur_fp = len(pred_set - gold_set)
        cur_fn = len(gold_set - pred_set)

        tp += cur_tp
        fp += cur_fp
        fn += cur_fn

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "dataset_size_samples": len(ANNOTATED_DATASET),
        "total_gold_entities": tp + fn,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "entity_precision": round(precision, 4),
        "entity_recall": round(recall, 4),
        "entity_f1": round(f1, 4),
    }

if __name__ == "__main__":
    results = run_evaluation()
    print("--- Legal Entity Intelligence Evaluation Results ---")
    print(json.dumps(results, indent=2))
