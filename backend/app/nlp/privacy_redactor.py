from typing import List, Dict, Any, Tuple

class LegalPrivacyRedactor:
    """
    Performs precise entity redaction on legal documents.
    Removes the underlying sensitive text while maintaining character mapping.
    """

    DEFAULT_SENSITIVE_LABELS = {"PERSON", "PHONE", "EMAIL", "MONEY"}

    def redact_text(
        self,
        text: str,
        entities: List[Dict[str, Any]],
        labels_to_redact: List[str] = None,
        custom_selected_indices: List[Tuple[int, int]] = None
    ) -> Dict[str, Any]:
        """
        Redact sensitive entities from text.
        Returns:
            - redacted_text: string with sensitive terms replaced with [REDACTED <TYPE>]
            - redaction_mapping: list of original vs redacted replacements
            - redacted_count: count of redactions performed
        """
        if not text:
            return {
                "redacted_text": "",
                "redaction_mapping": [],
                "redacted_count": 0
            }

        target_labels = set(labels_to_redact) if labels_to_redact is not None else self.DEFAULT_SENSITIVE_LABELS

        # Spans to redact: list of (start, end, label, text)
        spans_to_redact = []

        for ent in entities:
            if ent["label"] in target_labels:
                spans_to_redact.append((ent["start"], ent["end"], ent["label"], ent["text"]))

        if custom_selected_indices:
            for s, e in custom_selected_indices:
                spans_to_redact.append((s, e, "CUSTOM", text[s:e]))

        # Sort spans by start descending to replace from end to beginning
        # to preserve character offsets during replacements
        spans_to_redact.sort(key=lambda x: x[0], reverse=True)

        redacted_text = text
        mapping = []

        for start, end, label, original_span in spans_to_redact:
            token = f"[{label}_REDACTED]"
            redacted_text = redacted_text[:start] + token + redacted_text[end:]
            mapping.append({
                "original": original_span,
                "replacement": token,
                "label": label,
                "start": start,
                "end": end
            })

        # Return mapping in text order
        mapping.reverse()

        return {
            "redacted_text": redacted_text,
            "redaction_mapping": mapping,
            "redacted_count": len(mapping)
        }
