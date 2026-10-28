from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
import json
import csv
import io

from app.nlp.entity_service import entity_intelligence_service
from app.utils.file_handler import extract_text_from_file
from app.db.database import get_db
from app.db.models import Document

router = APIRouter(prefix="/api/entities", tags=["Legal Entity Intelligence"])

class TextAnalyzeRequest(BaseModel):
    text: str
    language: str = "en"

class RedactRequest(BaseModel):
    text: Optional[str] = None
    document_id: Optional[int] = None
    labels: Optional[List[str]] = None

@router.post("/analyze-text")
def analyze_entities_text(req: TextAnalyzeRequest):
    """Run Legal Entity Intelligence on raw text."""
    if not req.text or not req.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No text provided for entity intelligence analysis."
        )

    results = entity_intelligence_service.process_document(req.text)
    return results

@router.post("/analyze-file")
async def analyze_entities_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: Optional[int] = None
):
    """Run Legal Entity Intelligence on uploaded file (.pdf, .docx, .txt)."""
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid file uploaded."
        )

    # Validate file extension
    allowed = (".pdf", ".docx", ".txt")
    if not file.filename.lower().endswith(allowed):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format. Please upload {', '.join(allowed)}."
        )

    try:
        extracted_text = await extract_text_from_file(file)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract document text: {exc}"
        )

    if not extracted_text or not extracted_text.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Document appears to be empty or contained no extractable text."
        )

    results = entity_intelligence_service.process_document(extracted_text)

    # Persist document metadata and extracted entity stats
    doc_id = None
    try:
        new_doc = Document(
            user_id=user_id,
            filename=file.filename,
            content=extracted_text,
            doc_metadata={
                "type": "legal_entity_analysis",
                "stats": results["stats"]
            },
            embedding=json.dumps([])
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        doc_id = new_doc.id
    except Exception as exc:
        print(f"WARNING: DB save failed during entity analysis: {exc}")

    results["document_id"] = doc_id
    results["filename"] = file.filename
    return results

@router.post("/redact")
def redact_entities(req: RedactRequest, db: Session = Depends(get_db)):
    """Redact sensitive PII from text or document."""
    text_to_redact = req.text

    if not text_to_redact and req.document_id:
        doc = db.query(Document).filter(Document.id == req.document_id).first()
        if doc:
            text_to_redact = doc.content

    if not text_to_redact:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No text or valid document ID provided for redaction."
        )

    labels = req.labels if req.labels else ["PERSON", "PHONE", "EMAIL", "MONEY"]
    redaction_result = entity_intelligence_service.redact_document(text_to_redact, labels)
    return redaction_result

@router.get("/export/csv")
def export_entities_csv(text: str):
    """Export extracted entities as CSV."""
    if not text:
        raise HTTPException(status_code=400, detail="Text required for export")

    results = entity_intelligence_service.process_document(text)
    entities = results.get("entities", [])

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Entity Text", "Normalized", "Category", "Confidence", "Start Offset", "End Offset", "Source"])

    for e in entities:
        writer.writerow([
            e.get("text", ""),
            e.get("normalized", ""),
            e.get("label", ""),
            e.get("confidence", 0.0),
            e.get("start", 0),
            e.get("end", 0),
            e.get("source", ""),
        ])

    csv_data = output.getvalue()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=legal_entities.csv"}
    )
