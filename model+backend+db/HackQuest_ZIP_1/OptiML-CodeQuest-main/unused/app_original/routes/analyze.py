from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.model_loader import predict
from app.utils.file_handler import extract_text_from_file
from app.utils.voice_handler import convert_voice_to_text
from app.utils.embedding_utils import get_embedding
from app.db.database import get_db
from app.db.models import Document, Embedding, ContractAnalysisResult

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

    # 6️⃣ Save document, embedding, and analysis to database (best-effort)
    saved_id = None
    import json
    analysis_payload = prediction_result
    if isinstance(analysis_payload, str):
        try:
            analysis_payload = json.loads(analysis_payload)
        except Exception:
            pass

    # Retry small loop for transient DB issues
    last_err = None
    for _ in range(3):
        try:
            new_doc = Document(
                user_id=user_id,
                filename=file.filename if file else "input_text_or_voice",
                content=combined_text,
                embedding=embedding_vector
            )
            db.add(new_doc)
            await db.flush()

            db.add(Embedding(document_id=new_doc.id, vector=embedding_vector))
            db.add(ContractAnalysisResult(document_id=new_doc.id, result=analysis_payload))

            await db.commit()
            await db.refresh(new_doc)
            saved_id = new_doc.id
            last_err = None
            break
        except Exception as e:
            last_err = e
            try:
                await db.rollback()
            except Exception:
                pass
    if last_err:
        return {"error": f"DB persist failed: {last_err}", "input_text": combined_text, "prediction": prediction_result}

    return {
        "input_text": combined_text,
        "prediction": analysis_payload,
        "document_id": saved_id
    }