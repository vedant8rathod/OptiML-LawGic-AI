from fastapi import UploadFile
import tempfile
import importlib

sr = None  # Optional dependency
try:
    sr = importlib.import_module("speech_recognition")
except Exception:
    sr = None

async def convert_voice_to_text(voice_file: UploadFile) -> str:
    # Save voice file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        content = await voice_file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # Recognize speech (best-effort if library available)
    if sr is None:
        return ""  # Fallback: empty string when speech_recognition not installed

    r = sr.Recognizer()
    with sr.AudioFile(tmp_path) as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio)
        except Exception:
            text = ""

    return text