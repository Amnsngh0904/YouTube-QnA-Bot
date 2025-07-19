import whisper
import os
import json
from hashlib import md5
from deep_translator import GoogleTranslator

TRANSCRIPT_CACHE_DIR = "cache/transcripts"
model = whisper.load_model("medium")

def transcribe_audio(audio_path):
    os.makedirs(TRANSCRIPT_CACHE_DIR, exist_ok=True)
    transcript_path = os.path.join(TRANSCRIPT_CACHE_DIR, f"{md5(audio_path.encode()).hexdigest()}.json")

    if os.path.exists(transcript_path):
        with open(transcript_path, "r") as f:
            transcript = json.load(f)["text"]
    else:
        result = model.transcribe(audio_path, task="translate")  # Translates to English if needed
        transcript = result["text"]
        with open(transcript_path, "w") as f:
            json.dump(result, f)

    # Extra translation step (in case Whisper's translation is partial or poor)
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(transcript)
    except Exception as e:
        print(f"Translation failed: {e}")
        translated = transcript  # fallback to original

    return translated
