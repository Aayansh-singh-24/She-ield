import os
import io
import wave
import numpy as np
import speech_recognition as sr
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SafeHer ML Services")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    # allow_methods=["*"],
    allow_headers=["*"],
)

# Distress keywords in English and Hindi (transliterated and Devnagari)
KEYWORDS = [
    # English keywords
    "help", "help me", "emergency", "danger", "save me", "please help",
    # Hindi keywords (Transliterated)
    "bachao", "bachao mujhe", "mujhe bachao", "madad", "madad karo", "meri madad karo", "meri madad kro",
    # Hindi keywords (Devnagari script)
    "बचाओ", "मदद", "मेरी मदद करो"
]

@app.get("/")
def home():
    return {"message": "SafeHer ML Service is running"}

@app.post("/detect-distress")
async def detect_distress(file: UploadFile = File(...)):
    """
    Analyzes an uploaded audio WAV file for:
    1. Speech keywords (e.g., 'help me', 'bachao', 'meri madad kro') using SpeechRecognition.
    2. High-intensity scream sounds using signal processing (amplitude RMS & spectral band energy analysis).
    """
    if not file.filename.lower().endswith(('.wav', '.wave')):
        raise HTTPException(status_code=400, detail="Only WAV format is supported for signal processing compatibility.")

    try:
        audio_content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read audio file: {str(e)}")

    # Create in-memory file objects
    audio_file_sr = io.BytesIO(audio_content)
    audio_file_dsp = io.BytesIO(audio_content)

    # ==========================================
    # 1. KEYWORD DETECTION (Speech-to-Text)
    # ==========================================
    transcript = ""
    keyword_detected = None
    
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_sr) as source:
            # Record the full audio content
            audio_data = recognizer.record(source)

        # Attempt transcription in English
        transcript_en = ""
        try:
            transcript_en = recognizer.recognize_google(audio_data, language="en-US").lower()
            print(f"[Speech-to-Text EN] {transcript_en}")
        except sr.UnknownValueError:
            pass # No speech detected
        except Exception as e:
            print(f"[Speech-to-Text EN Error] {e}")

        # Attempt transcription in Hindi
        transcript_hi = ""
        try:
            transcript_hi = recognizer.recognize_google(audio_data, language="hi-IN").lower()
            print(f"[Speech-to-Text HI] {transcript_hi}")
        except sr.UnknownValueError:
            pass # No speech detected
        except Exception as e:
            print(f"[Speech-to-Text HI Error] {e}")

        # Combine transcripts
        transcripts = []
        if transcript_en:
            transcripts.append(transcript_en)
        if transcript_hi:
            transcripts.append(transcript_hi)
        transcript = " | ".join(transcripts)

        # Check for distress keywords
        for kw in KEYWORDS:
            if kw in transcript_en or kw in transcript_hi:
                keyword_detected = kw
                break

    except Exception as e:
        print(f"[Speech Recognition System Error] {e}")

    # ==========================================
    # 2. SCREAM DETECTION (DSP Signal Analysis)
    # ==========================================
    scream_detected = False
    rms = 0.0
    peak_frequency = 0.0
    energy_ratio = 0.0

    try:
        with wave.open(audio_file_dsp, 'rb') as wav_ref:
            n_channels = wav_ref.getnchannels()
            sampwidth = wav_ref.getsampwidth()
            framerate = wav_ref.getframerate()
            n_frames = wav_ref.getnframes()
            
            raw_frames = wav_ref.readframes(n_frames)
            
            # Match bits per sample
            if sampwidth == 1:
                dtype = np.uint8
                max_val = 128.0
            elif sampwidth == 2:
                dtype = np.int16
                max_val = 32768.0
            elif sampwidth == 4:
                dtype = np.int32
                max_val = 2147483648.0
            else:
                dtype = np.int16
                max_val = 32768.0

            audio_np = np.frombuffer(raw_frames, dtype=dtype)

            # If multi-channel, merge/average channels to mono
            if n_channels > 1:
                audio_np = audio_np.reshape(-1, n_channels).mean(axis=1)

            # Normalize values to range [-1.0, 1.0]
            if sampwidth == 1:
                audio_normalized = (audio_np.astype(np.float32) - 128.0) / 128.0
            else:
                audio_normalized = audio_np.astype(np.float32) / max_val

            # Compute RMS (Root Mean Square) for volume/loudness
            if len(audio_normalized) > 0:
                rms = np.sqrt(np.mean(audio_normalized ** 2))
                
                # Perform FFT (Frequency analysis)
                fft_vals = np.abs(np.fft.rfft(audio_normalized))
                fft_freqs = np.fft.rfftfreq(len(audio_normalized), 1.0 / framerate)

                # Peak frequency
                peak_idx = np.argmax(fft_vals)
                peak_frequency = fft_freqs[peak_idx]

                # Scream frequency band (typically 800 Hz to 4000 Hz)
                scream_mask = (fft_freqs >= 800) & (fft_freqs <= 4000)
                scream_energy = np.sum(fft_vals[scream_mask])
                total_energy = np.sum(fft_vals)

                energy_ratio = (scream_energy / total_energy) if total_energy > 0 else 0.0

                # SCREAM LOGIC:
                # 1. Loud sound: RMS > 0.15 (very loud input signal)
                # 2. High-pitch focus: more than 40% of spectral energy lies between 800Hz and 4000Hz (scream bands)
                if rms > 0.15 and energy_ratio > 0.40:
                    scream_detected = True

            print(f"[DSP Analysis] RMS: {rms:.4f} | Peak Freq: {peak_frequency:.1f}Hz | Scream Band Ratio: {energy_ratio:.4f} | Scream: {scream_detected}")

    except Exception as e:
        print(f"[DSP Analysis Error] {e}")

    # ==========================================
    # 3. CONSOLIDATE RESULTS
    # ==========================================
    distress_detected = bool(keyword_detected or scream_detected)
    reasons = []
    if keyword_detected:
        reasons.append(f"Distress keyword detected: '{keyword_detected}'")
    if scream_detected:
        reasons.append(f"High-frequency scream signature detected (RMS: {rms:.2f}, Band Ratio: {energy_ratio:.2f})")

    response_data = {
        "distress_detected": distress_detected,
        "reason": "; ".join(reasons) if distress_detected else "Normal background audio",
        "transcript": transcript,
        "metrics": {
            "rms": float(rms),
            "peak_frequency": float(peak_frequency),
            "energy_ratio": float(energy_ratio),
            "keyword_match": keyword_detected
        }
    }
    
    if distress_detected:
        print(f"\n🚨 [ALERT TRIGGERED] Distress event detected! Reason: {response_data['reason']}\n")

    return response_data
