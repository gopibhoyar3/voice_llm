import streamlit as st
import sounddevice as sd
import numpy as np
import wave
import tempfile
import threading

# Session state init
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

# Function to record audio
def record_audio(duration=10, fs=44100):
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(tmp_file.name, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())

    st.session_state.audio_path = tmp_file.name
    st.session_state.is_recording = False
    st.toast("✅ Recording complete!", icon="🎧")

def st_mic_button():
    mic_style = """
        <style>
            .mic-button {
                background-color: #25a5f7;
                border: none;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                font-size: 24px;
                color: white;
                cursor: pointer;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
            }
            .mic-container {
                display: flex;
                justify-content: center;
                margin-top: 2rem;
            }
        </style>
        <div class="mic-container">
            <form action="" method="post">
                <button name="mic" class="mic-button">🎤</button>
            </form>
        </div>
    """
    st.markdown(mic_style, unsafe_allow_html=True)

    # Capture mic button click
    if st.session_state.is_recording:
        sd.stop()
        st.session_state.is_recording = False
        st.toast("⏹️ Stopped Recording", icon="🔇")
    elif st.session_state.get("mic_click", False) is False and st.session_state.is_recording is False:
        st.session_state.is_recording = True
        threading.Thread(target=record_audio, args=(10,), daemon=True).start()
        st.toast("🎙️ Recording...", icon="🔴")

    if st.session_state.audio_path:
        st.audio(st.session_state.audio_path)
        return st.session_state.audio_path

    return None
