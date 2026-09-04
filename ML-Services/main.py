import os
import io
import wave
import numpy as np
import speech_recognition as sr
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from yamnet_classifier import YAMNetClassifier

app = FastAPI(title="SafeHer ML Services")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pre-trained YAMNet classifier at startup
try:
    yamnet_classifier = YAMNetClassifier()
except Exception as e:
    print(f"[YAMNet Initialization Error] {e}")
    yamnet_classifier = None

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
    return {
        "message": "SafeHer ML Service is running",
        "models": {
            "speech_recognition": "Google Web Speech API (Multilingual EN/HI)",
            "acoustic_classifier": "Google YAMNet Deep Learning (AudioSet 521 classes)"
        }
    }

@app.post("/detect-distress")
async def detect_distress(file: UploadFile = File(...)):
    """
    Analyzes an uploaded audio WAV file for:
    1. Speech keywords (e.g., 'help me', 'bachao', 'meri madad kro') using SpeechRecognition.
    2. High-precision scream/distress classification using Google's YAMNet Deep Learning model.
       Explicitly suppresses false alarms from street noises (car horns, sirens, traffic).
    """
    if not file.filename.lower().endswith(('.wav', '.wave')):
        raise HTTPException(status_code=400, detail="Only WAV format is supported for acoustic analysis.")

    try:
        audio_content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read audio file: {str(e)}")

    # ==========================================
    # 1. KEYWORD DETECTION (Speech-to-Text)
    # ==========================================
    transcript = ""
    keyword_detected = None
    audio_file_sr = io.BytesIO(audio_content)
    
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_sr) as source:
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
    # 2. DEEP LEARNING ACOUSTIC CLASSIFICATION (YAMNet)
    # ==========================================
    yamnet_result = {
        "distress_detected": False,
        "distress_class": None,
        "distress_confidence": 0.0,
        "noise_suppressed": False,
        "top_noise_class": None,
        "top_noise_confidence": 0.0,
        "top_detected_class": "Unknown",
        "top_detected_confidence": 0.0,
        "top_predictions": []
    }

    if yamnet_classifier is not None:
        try:
            yamnet_result = yamnet_classifier.classify(audio_content)
            print(f"[YAMNet Analysis] Distress: {yamnet_result['distress_detected']} ({yamnet_result['distress_class']} @ {yamnet_result['distress_confidence']:.2%}) | Top Class: {yamnet_result['top_detected_class']} @ {yamnet_result['top_detected_confidence']:.2%} | Noise Suppressed: {yamnet_result['noise_suppressed']}")
        except Exception as e:
            print(f"[YAMNet Inference Error] {e}")

    # ==========================================
    # 3. CONSOLIDATE RESULTS (Multi-Modal Fusion)
    # ==========================================
    scream_detected = yamnet_result.get("distress_detected", False)
    distress_detected = bool(keyword_detected or scream_detected)
    
    reasons = []
    if keyword_detected:
        reasons.append(f"Distress keyword detected: '{keyword_detected}'")
    if scream_detected:
        distress_class = yamnet_result.get("distress_class", "Screaming")
        conf = yamnet_result.get("distress_confidence", 0.0)
        reasons.append(f"Distress acoustic signature detected: '{distress_class}' (confidence: {conf:.1%})")

    if not distress_detected and yamnet_result.get("noise_suppressed"):
        reason_str = f"Environmental noise detected: '{yamnet_result.get('top_noise_class')}' (scream false alarm prevented)"
    elif distress_detected:
        reason_str = "; ".join(reasons)
    else:
        reason_str = f"Normal audio: '{yamnet_result.get('top_detected_class', 'Background')}'"

    response_data = {
        "distress_detected": distress_detected,
        "reason": reason_str,
        "transcript": transcript,
        "metrics": {
            "yamnet_distress_detected": scream_detected,
            "yamnet_distress_class": yamnet_result.get("distress_class"),
            "yamnet_distress_confidence": yamnet_result.get("distress_confidence", 0.0),
            "top_detected_class": yamnet_result.get("top_detected_class"),
            "top_detected_confidence": yamnet_result.get("top_detected_confidence", 0.0),
            "noise_suppressed": yamnet_result.get("noise_suppressed", False),
            "top_noise_class": yamnet_result.get("top_noise_class"),
            "keyword_match": keyword_detected,
            "top_predictions": yamnet_result.get("top_predictions", [])
        }
    }
    
    if distress_detected:
        print(f"\n🚨 [SAFEHER ALERT TRIGGERED] Distress event detected! Reason: {response_data['reason']}\n")

    return response_data