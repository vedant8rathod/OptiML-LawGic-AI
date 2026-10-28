from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.utils.model_loader import predict_analyze
from app.utils.file_handler import extract_text_from_file
from app.utils.voice_handler import convert_voice_to_text
from app.utils.embedding_utils import get_embedding
from app.db.database import get_db
from app.db.models import Document
import json

router = APIRouter(prefix="/api/analyze", tags=["Analyze"])

@router.post("/")
async def analyze(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    voice: Optional[UploadFile] = File(None),
    language: str = Form("en"),  # Language parameter
    db: Session = Depends(get_db),
    user_id: Optional[int] = None  # optional for future user management
):
    input_text = ""

    # 1️⃣ Text input
    if text:
        input_text += text + " "

    # 2️⃣ File input (simplified for demo)
    if file:
        try:
            file_text = await extract_text_from_file(file)
            input_text += file_text + " "
        except Exception as e:
            input_text += f"[File upload: {file.filename}] "

    # 3️⃣ Voice input (simplified for demo)
    if voice:
        try:
            voice_text = await convert_voice_to_text(voice)
            input_text += voice_text + " "
        except Exception as e:
            input_text += f"[Voice input: {voice.filename}] "

    combined_text = input_text.strip()

    # 4️⃣ Call the model
    prediction_result = predict_analyze(combined_text, language)

    # 5️⃣ Generate embedding
    embedding_vector = await get_embedding(combined_text)

    # 6️⃣ Save document and embedding to database
    try:
        new_doc = Document(
            user_id=user_id,
            filename=file.filename if file else "input_text_or_voice",
            content=combined_text,
            doc_metadata={},  # Use the renamed column
            embedding=json.dumps(embedding_vector)  # Store as JSON string
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        document_id = new_doc.id
    except Exception as e:
        print(f"⚠️ Database save failed: {e}")
        document_id = "demo_mode"

    # Create a summary of the input instead of returning the full text
    input_summary = combined_text[:200] + "..." if len(combined_text) > 200 else combined_text
    
    # Extract document_summary from prediction if available
    document_summary = ""
    if isinstance(prediction_result, dict):
        document_summary = prediction_result.get("document_summary", 
                          prediction_result.get("summary", input_summary))
    
    return {
        "input_text": combined_text,
        "prediction": prediction_result,
        "document_id": document_id
    }
