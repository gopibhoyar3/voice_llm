from fastapi import FastAPI, UploadFile, File
from models.schemas import ChatRequest
from services import stt_service, llm_service, tts_service, rag_service
import os

app = FastAPI()

@app.post("/upload_rag_docs")
async def upload_rag_docs(file: UploadFile = File(...)):
    os.makedirs("rag_uploads", exist_ok=True)
    path = f"rag_uploads/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    try:
        rag_service.index_document(path)
        return {"status": "Document indexed successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/transcribe")
async def transcribe(file: UploadFile):
    os.makedirs("temp", exist_ok=True)
    path = f"temp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    text, duration = stt_service.transcribe_audio(path)
    return {"text": text, "duration_seconds": duration}

@app.post("/chat")  # ✅ Fixed decorator
async def chat(payload: ChatRequest):
    rag_chunks = rag_service.retrieve_relevant_chunks(payload.user_message)
    rag_context = "\n".join(rag_chunks)

    response = llm_service.chat_with_memory(
        user_message=payload.user_message,
        rag_context=rag_context
    )
    return {"response": response}

@app.post("/converse")
async def converse(file: UploadFile = File(...)):
    import os
    import time

    os.makedirs("temp", exist_ok=True)
    audio_path = f"temp/{file.filename}"
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    try:
        print("🔍 Step 1: Starting transcription")
        user_message, stt_duration = stt_service.transcribe_audio(audio_path)
        print(f"✅ Transcription done: {user_message}")
    except Exception as e:
        return {"error": f"Transcription failed: {str(e)}"}

    try:
        print("🔍 Step 2: Getting RAG chunks")
        rag_chunks = rag_service.retrieve_relevant_chunks(user_message)
        rag_context = "\n".join(rag_chunks)
        print(f"✅ RAG context retrieved")
    except Exception as e:
        return {"error": f"RAG failed: {str(e)}"}

    try:
        print("🔍 Step 3: Getting LLM response")
        llm_response = llm_service.chat_with_memory(user_message, rag_context)
        print(f"✅ LLM response: {llm_response}")
    except Exception as e:
        return {"error": f"LLM failed: {str(e)}"}

    try:
        print("🔍 Step 4: Synthesizing audio")
        audio_output_path, tts_duration = tts_service.text_to_speech(llm_response)
        print(f"✅ Audio file at: {audio_output_path}")
    except Exception as e:
        return {"error": f"TTS failed: {str(e)}"}

    return {
        "transcription": user_message,
        "response": llm_response,
        "audio_file": audio_output_path
    }


@app.post("/speak")
async def speak(text: str):
    audio_path, duration = tts_service.text_to_speech(text)
    return {"audio_file": audio_path, "duration_seconds": duration}

@app.post("/reset")
async def reset():
    llm_service.reset_conversation()
    return {"status": "conversation memory cleared"}
