from fastapi import UploadFile
import tempfile

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️ Speech recognition not available. Using demo mode.")

async def convert_voice_to_text(voice_file: UploadFile) -> str:
    if not SPEECH_RECOGNITION_AVAILABLE:
        return get_demo_voice_text(voice_file.filename)
    
    try:
        # Save voice file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await voice_file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Recognize speech
        r = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)

        return text
    except Exception as e:
        print(f"⚠️ Voice recognition failed: {e}")
        return get_demo_voice_text(voice_file.filename)

def get_demo_voice_text(filename: str) -> str:
    """Generate demo transcription for voice files"""
    return f"""Demo transcription from {filename}: 
    'I need help understanding this legal contract. Can you explain what my obligations are under this agreement and what rights I have as a tenant? I'm particularly concerned about the clause regarding late payment fees and the termination process.'
    
    [This is demo voice transcription - actual speech recognition requires proper setup]"""
