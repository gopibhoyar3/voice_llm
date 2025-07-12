import sounddevice as sd
import wave

fs = 44100
duration = 10  # seconds
filename = "test_output.wav"

print("Recording...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()
print("Recording complete.")

# Save to file
with wave.open(filename, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(fs)
    wf.writeframes(recording.tobytes())

print(f"Saved recording to {filename}")
