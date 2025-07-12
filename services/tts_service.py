import time
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def text_to_speech(text: str, output_path="output.mp3"):
    start = time.time()

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",  # you can change this to 'nova', 'shimmer', etc.
        input=text
    )

    audio_path = os.path.join("temp", output_path)

    with open(audio_path, "wb") as f:
        f.write(response.content)  # ✅ access the .content here

    end = time.time()
    return audio_path, round(end - start, 2)
