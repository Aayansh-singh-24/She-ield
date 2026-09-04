import io
import wave
import numpy as np
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def create_wav_bytes(duration_sec=1.0, freq=None, noise=False, sample_rate=16000):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    if noise:
        samples = (np.random.uniform(-0.5, 0.5, len(t)) * 32767).astype(np.int16)
    elif freq is not None:
        samples = (np.sin(2 * np.pi * freq * t) * 16000).astype(np.int16)
    else:
        samples = np.zeros(len(t), dtype=np.int16)
    
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())
    return buf.getvalue()

def test_home():
    response = client.get("/")
    print("\n--- Test GET / ---")
    print("Status:", response.status_code)
    print("Response:", response.json())
    assert response.status_code == 200

def test_detect_distress_silence():
    wav_data = create_wav_bytes(duration_sec=1.0)
    files = {"file": ("silence.wav", io.BytesIO(wav_data), "audio/wav")}
    response = client.post("/detect-distress", files=files)
    print("\n--- Test POST /detect-distress (Silence) ---")
    print("Status:", response.status_code)
    res_json = response.json()
    print("Response:", res_json)
    assert response.status_code == 200
    assert res_json["distress_detected"] is False

def test_detect_distress_tone():
    # 440 Hz tone (e.g. dial tone / phone)
    wav_data = create_wav_bytes(duration_sec=1.0, freq=440.0)
    files = {"file": ("tone.wav", io.BytesIO(wav_data), "audio/wav")}
    response = client.post("/detect-distress", files=files)
    print("\n--- Test POST /detect-distress (440Hz Tone) ---")
    print("Status:", response.status_code)
    res_json = response.json()
    print("Response:", res_json)
    assert response.status_code == 200
    assert res_json["distress_detected"] is False

if __name__ == "__main__":
    test_home()
    test_detect_distress_silence()
    test_detect_distress_tone()
    print("\n[SUCCESS] All automated endpoint tests passed cleanly!")
