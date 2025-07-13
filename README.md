# 🎙️ Voice Conversational Agentic AI with RAG

A Python-based RESTful API project that enables **bi-directional voice conversations** with a Large Language Model (LLM), enhanced with **Retrieval Augmented Generation (RAG)** using proprietary/internal documents. This voice agent supports speech input/output, document question answering, and maintains conversational memory.

---

## 🚀 Features

- 🎤 Real-time voice input and transcription (STT)
- 🧠 Persistent conversation memory with LLM (OpenAI GPT)
- 📄 RAG on uploaded documents (PDF, TXT, CSV, JSON)
- 📢 TTS output for conversational responses
- 📁 Vector indexing using FAISS, Pinecone, or Weaviate
- 🧩 Modular and easy-to-use RESTful APIs

---

## 📁 Project Structure

```
voice_llm_rag/
├── models/
│ └── schemas.py # Pydantic models for request/response
├── rag_uploads/ # Uploaded documents (PDF, CSV, etc.)
│ ├── HackathonInternalKnowledgeBase.csv
│ └── Voice Conversational Agentic AI.pdf
├── routes/
│ ├── chat.py # /chat endpoint
│ ├── converse.py # /converse endpoint
│ ├── speak.py # /speak endpoint
│ ├── transcribe.py # /transcribe endpoint
│ └── upload_rag_docs.py # /upload_rag_docs endpoint
├── services/
│ ├── llm_service.py # Handles GPT interaction
│ ├── rag_service.py # Handles RAG doc indexing/querying
│ ├── stt_service.py # Handles speech-to-text
│ └── tts_service.py # Handles text-to-speech
├── temp/ # Temporary audio/files
├── utils/ # Utility functions
├── .env # API keys
├── .gitignore
├── app.py # FastAPI app factory
├── architecture.md # Project architecture documentation
├── main.py # Entry point
├── output.mp3 # TTS audio output
├── README.md # You're here!
├── requirements.txt # Python dependencies
├── st_audiorec.py # Streamlit audio recorder (if any)
└── test.py # Test script
```

---

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/voice-agent-rag.git
cd voice-agent-rag
```

2. **Create virtual environment and install dependencies**
```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set your API keys**
Create a `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=optional
AZURE_API_KEY=optional
```

---

## ▶️ Running the App

```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for Swagger UI to test all endpoints.

---

## 📌 API Endpoints

| Endpoint           | Method | Description                                                      |
| ------------------ | ------ | ---------------------------------------------------------------- |
| `/transcribe`      | POST   | Accepts audio, returns transcription + STT time                  |
| `/chat`            | POST   | Accepts conversation + message + context, returns LLM response   |
| `/speak`           | POST   | Converts LLM text to audio, returns output + TTS time            |
| `/converse`        | POST   | End-to-end: Voice input → STT → LLM + RAG → TTS                  |
| `/reset`           | POST   | Resets the conversation memory                                   |
| `/upload_rag_docs` | POST   | Uploads and indexes documents for Retrieval Augmented Generation |


---

## ✅ Supported File Types for RAG

- PDF
- TXT
- CSV
- JSON

All documents are parsed and indexed for contextual response retrieval.

---

## 📦 Dependencies

- `FastAPI`
- `OpenAI`
- `FAISS`, `langchain`
- `PyPDF2`, `pandas`
- `sounddevice`, `numpy`, `requests`

---

## 🧠 Architecture Overview

```
🎤 Voice Input
     ↓
 [Speech-to-Text (STT)]
     ↓
 💬 LLM Chat with Memory + RAG Context
     ↓
 [Text-to-Speech (TTS)]
     ↓
 🔊 Voice Output
```

## 👨‍💻 Author

GOPI BHOYAR

---

## 🤝 Contributions

Feel free to fork this repo, submit issues, or create pull requests. Suggestions and improvements are welcome!
