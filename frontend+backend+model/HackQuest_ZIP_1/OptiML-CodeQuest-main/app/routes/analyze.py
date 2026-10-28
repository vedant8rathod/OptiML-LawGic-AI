from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.model_loader import predict
from app.utils.file_handler import extract_text_from_file
from app.utils.voice_handler import convert_voice_to_text
from app.utils.embedding_utils import get_embedding
from app.db.database import get_db
from app.db.models import Document

router = APIRouter(prefix="/api/analyze", tags=["Analyze"])

@router.post("/")
async def analyze(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    voice: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    user_id: Optional[int] = None  # optional for future user management
):
    input_text = ""

    # 1️⃣ Text input
    if text:
        input_text += text + " "

    # 2️⃣ File input
    if file:
        file_text = await extract_text_from_file(file)
        input_text += file_text + " "

    # 3️⃣ Voice input
    if voice:
        voice_text = await convert_voice_to_text(voice)
        input_text += voice_text + " "

    combined_text = input_text.strip()

    # 4️⃣ Call the model
    prediction_result = predict(combined_text)

    # 5️⃣ Generate embedding
    embedding_vector = await get_embedding(combined_text)

    # 6️⃣ Save document and embedding to database (best-effort)
    saved_id = None
    try:
        new_doc = Document(
            user_id=user_id,
            filename=file.filename if file else "input_text_or_voice",
            content=combined_text,
            embedding=embedding_vector  # stored as JSON array
        )
        db.add(new_doc)
        await db.commit()
        await db.refresh(new_doc)
        saved_id = new_doc.id
    except Exception as e:
        # Database might be unavailable locally; continue without persisting
        try:
            await db.rollback()
        except Exception:
            pass
        print(f"⚠️ Failed to save to DB: {e}")

    return {
        "input_text": combined_text,
        "prediction": prediction_result,
        "document_id": saved_id
    }