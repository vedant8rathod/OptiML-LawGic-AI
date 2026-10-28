import re
from typing import List, Dict, Any

class LegalTimelineGenerator:
    """
    Extracts chronological legal events and associated parties from legal documents.
    """

    def generate_timeline(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not text or not entities:
            return []

        # Find all DATE entities
        date_entities = [e for e in entities if e["label"] == "DATE"]
        if not date_entities:
            return []

        timeline_events: List[Dict[str, Any]] = []

        # For each date, find the surrounding sentence and related entities
        for date_ent in date_entities:
            # Find sentence context
            sent_start, sent_end, sent_text = self._find_surrounding_sentence(text, date_ent["start"], date_ent["end"])

            # Find co-occurring entities in the same sentence
            co_occurring = [
                e["text"] for e in entities
                if e["start"] >= sent_start and e["end"] <= sent_end and e != date_ent
            ]

            # Determine event description
            event_desc = self._summarize_event(sent_text, date_ent["text"])

            timeline_events.append({
                "date": date_ent["text"],
                "normalized_date": date_ent.get("normalized", date_ent["text"]),
                "event_description": event_desc,
                "involved_entities": list(dict.fromkeys(co_occurring)),  # deduplicated
                "supporting_text": sent_text.strip(),
                "start_offset": sent_start,
                "end_offset": sent_end,
                "is_explicit": True
            })

        # Sort timeline by text appearance order
        timeline_events.sort(key=lambda x: x["start_offset"])
        return timeline_events

    def _find_surrounding_sentence(self, text: str, start: int, end: int) -> tuple:
        # Search backwards for sentence start
        prev_break = max(
            text.rfind(".", 0, start),
            text.rfind("!", 0, start),
            text.rfind("?", 0, start),
            text.rfind("\n", 0, start),
        )
        s_start = 0 if prev_break == -1 else prev_break + 1

        # Search forwards for sentence end
        next_break = len(text)
        for delim in [".", "!", "?", "\n"]:
            pos = text.find(delim, end)
            if pos != -1 and pos < next_break:
                next_break = pos + 1

        return s_start, next_break, text[s_start:next_break]

    def _summarize_event(self, sentence: str, date_text: str) -> str:
        # Clean sentence
        clean = sentence.replace("\n", " ").strip()
        if len(clean) > 140:
            return clean[:137] + "..."
        return clean
