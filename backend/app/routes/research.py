from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.utils.model_loader import predict_research
from app.utils.file_handler import extract_text_from_file
from app.utils.voice_handler import convert_voice_to_text
from app.utils.embedding_utils import get_embedding
from app.db.database import get_db
from app.db.models import Document
import json

router = APIRouter(prefix="/api/research", tags=["Research"])

@router.post("/")
async def research(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    voice: Optional[UploadFile] = File(None),
    language: str = Form("en"),  # Language parameter
    db: Session = Depends(get_db),
    user_id: Optional[int] = None
):
    """
    Legal research endpoint that processes multi-modal input
    and returns structured legal analysis.
    """
    input_text = ""

    # 1️⃣ Text input
    if text:
        input_text += text + " "

    # 2️⃣ File input
    if file:
        try:
            file_text = await extract_text_from_file(file)
            input_text += file_text + " "
        except Exception as e:
            input_text += f"[File upload: {file.filename}] "

    # 3️⃣ Voice input
    if voice:
        try:
            voice_text = await convert_voice_to_text(voice)
            input_text += voice_text + " "
        except Exception as e:
            input_text += f"[Voice input: {voice.filename}] "

    combined_text = input_text.strip()

    # 4️⃣ Call the specialized research model
    prediction_result = predict_research(combined_text, language)

    # 5️⃣ Generate embedding
    embedding_vector = await get_embedding(combined_text)

    # 6️⃣ Save to database (best effort)
    document_id = "demo_mode"
    try:
        new_doc = Document(
            user_id=user_id,
            filename=file.filename if file else "research_input",
            content=combined_text,
            doc_metadata={},  # Use the renamed column
            embedding=json.dumps(embedding_vector)
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        document_id = new_doc.id
    except Exception as e:
        print(f"⚠️ Database save failed: {e}")

    return {
        "input_text": combined_text,
        "prediction": prediction_result,
        "document_id": document_id
    }