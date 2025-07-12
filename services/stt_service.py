# services/stt_service.py
import time
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file_path: str):
    start = time.time()
    with open(file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=f,
            model="whisper-1"
        )
    end = time.time()
    return transcription.text, round(end - start, 2)