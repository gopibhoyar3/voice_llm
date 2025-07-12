import streamlit as st
st.set_page_config(page_title="🎙️ Voice LLM + RAG", layout="centered")

import sounddevice as sd
import numpy as np
import wave
import tempfile
import requests
import queue
import time

# --- Device Selection ---
devices = sd.query_devices()
input_devices = [f"{i}: {d['name']}" for i, d in enumerate(devices) if d['max_input_channels'] > 0]
selected = st.selectbox("🎤 Select Microphone", input_devices)
selected_index = int(selected.split(":")[0])
sd.default.device = (selected_index, None)

st.title("📚 Voice Chat with LLM + RAG")

# --- Session Setup ---
if "doc_uploaded" not in st.session_state:
    st.session_state.doc_uploaded = False
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None
if "recording" not in st.session_state:
    st.session_state.recording = False

# --- Step 1: Upload Document ---
st.subheader("📄 Step 1: Upload a Document")
uploaded_file = st.file_uploader("Choose a PDF, TXT, CSV, or JSON", type=["pdf", "txt", "csv", "json"])

if uploaded_file and not st.session_state.doc_uploaded:
    with st.spinner("📡 Uploading and indexing document..."):
        response = requests.post(
            "http://localhost:8080/upload_rag_docs",
            files={"file": (uploaded_file.name, uploaded_file.read())}
        )
    if response.ok:
        st.success("✅ Document indexed successfully!")
        st.session_state.doc_uploaded = True
    else:
        st.error("❌ Document upload failed.")

# --- Step 2: Record Voice ---
if st.session_state.doc_uploaded:
    st.markdown("---")
    st.subheader("🎤 Step 2: Ask Your Question")

    if st.button("🎙️ Start Recording"):
        fs = 44100
        max_duration = 180  # 3 minutes
        silence_threshold = 30  # lower for better sensitivity
        silence_limit_sec = 1.0
        chunk_duration = 0.2  # 200 ms

        q_audio = queue.Queue()
        recorded = []
        last_spoke_time = time.time()
        speech_started = False
        start_time = time.time()

        def callback(indata, frames, time_info, status):
            volume = np.sqrt(np.mean(indata**2)) * 1000  # RMS energy
            q_audio.put((indata.copy(), volume))

        st.toast("🔴 Recording started... Speak now", icon="🎤")
        stream = sd.InputStream(callback=callback, channels=1, samplerate=fs)
        stream.start()

        while True:
            if time.time() - start_time > max_duration:
                st.toast("⏱️ Max duration reached. Stopping...", icon="⏹️")
                break

            try:
                data, volume = q_audio.get(timeout=1)
                recorded.append(data)

                if volume > silence_threshold:
                    last_spoke_time = time.time()
                    speech_started = True

                if speech_started and (time.time() - last_spoke_time) > silence_limit_sec:
                    st.toast("⏹️ Silence detected. Stopping...", icon="📴")
                    break

            except queue.Empty:
                break

        stream.stop()

        if recorded:
            audio_array = np.concatenate(recorded, axis=0)
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            with wave.open(tmp_file.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(fs)
                wf.writeframes((audio_array * 32767).astype(np.int16).tobytes())

            st.session_state.audio_path = tmp_file.name
            st.toast("✅ Recording saved!", icon="📁")
        else:
            st.warning("⚠️ No audio detected. Please try again.")
            st.session_state.audio_path = None

# --- Step 3: Playback & Display Response in Chat Format ---
if st.session_state.audio_path:
    # Display user's voice as audio and text (if needed)
    st.markdown("### 🗣️ Your Recording")
    st.audio(st.session_state.audio_path, format="audio/wav")

    with open(st.session_state.audio_path, "rb") as f:
        audio_bytes = f.read()

    with st.spinner("🤖 Assistant is thinking..."):
        response = requests.post(
            "http://localhost:8080/converse",
            files={"file": ("recording.wav", audio_bytes, "audio/wav")}
        )

    if response.ok:
        result = response.json()
        st.success("")

        # 👤 User prompt (transcribed)
        st.markdown("#### 👤 You said:")
        with st.chat_message("user"):
            st.markdown(result['transcription'])

        # 🤖 Assistant reply
        st.markdown("#### 🤖 Assistant says:")
        with st.chat_message("assistant"):
            st.markdown(result["response"])
            st.audio(result["audio_file"], format="audio/mp3")

        # Clear previous audio so it doesn’t replay unless new input comes
        st.session_state.audio_path = None

    else:
        st.error(f"❌ Error: {response.text}")

