import aiofiles
from pathlib import Path
from fastapi import UploadFile

try:
    import docx
    import PyPDF2
    DOCUMENT_PROCESSING_AVAILABLE = True
except ImportError:
    DOCUMENT_PROCESSING_AVAILABLE = False
    print("⚠️ Document processing libraries not available. Some formats will not be fully processed.")

TMP_DIR = Path("tmp")
TMP_DIR.mkdir(exist_ok=True)

async def extract_text_from_file(file: UploadFile) -> str:
    # If processing libs aren't available, still handle .txt directly and avoid fake demo content
    if not DOCUMENT_PROCESSING_AVAILABLE:
        filename = file.filename or "uploaded_file"
        if filename.endswith(".txt"):
            try:
                content = await file.read()
                return content.decode("utf-8", errors="ignore")
            except Exception as e:
                print(f"⚠️ Text file read failed: {e}")
                return f"Uploaded file: {filename}"
        # For non-text types, return a neutral placeholder (no hardcoded demo text)
        return f"Uploaded file: {filename}"
    
    file_path = TMP_DIR / file.filename

    # Save uploaded file temporarily
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    text = ""
    try:
        if file.filename.endswith(".pdf"):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join([page.extract_text() or "" for page in reader.pages]).strip()
        elif file.filename.endswith(".docx"):
            doc = docx.Document(file_path)
            text = "\n".join([p.text for p in doc.paragraphs]).strip()
        elif file.filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read().strip()
        else:
            text = f"Uploaded file: {file.filename}"
    except Exception as e:
        print(f"⚠️ File processing failed: {e}")
        # Avoid demo content; return a neutral placeholder that the caller can handle
        text = f"Uploaded file: {file.filename}"

    # Delete temporary file
    try:
        file_path.unlink()
    except Exception:
        pass
    
    return text
