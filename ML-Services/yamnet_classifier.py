import os
import io
import wave
import csv
import numpy as np
import scipy.signal
import tensorflow as tf

class YAMNetClassifier:
    """
    Deep Learning Audio Classifier using Google's pre-trained YAMNet model.
    Trained on 521 AudioSet categories to accurately detect human screams/yells
    and filter out environmental/street noise like car horns, sirens, and traffic.
    """
    
    # Target distress sound categories in AudioSet
    DISTRESS_CLASSES = {
        "Screaming",
        "Yell",
        "Shout",
        "Children shouting",
        "Crying, sobbing",
        "Baby cry, infant cry",
        "Wail, moan",
        "Groan",
    }
    
    # Noise/Distractor categories that should suppress false scream alarms
    NOISE_CLASSES = {
        "Vehicle horn, car horn, honking",
        "Air horn, truck horn",
        "Train horn",
        "Car alarm",
        "Alarm",
        "Alarm clock",
        "Siren",
        "Civil defense siren",
        "Police car (siren)",
        "Ambulance (siren)",
        "Fire engine, fire truck (siren)",
        "Emergency vehicle",
        "Traffic noise, roadway noise",
        "Engine",
        "Motor vehicle (road)",
        "Aircraft engine",
        "Jet engine",
        "Smoke detector, smoke alarm",
        "Fire alarm",
        "Foghorn",
    }

    def __init__(self, model_path: str = None, class_map_path: str = None, distress_threshold: float = 0.25):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(base_dir, "models")
        
        self.model_path = model_path or os.path.join(models_dir, "yamnet.tflite")
        self.class_map_path = class_map_path or os.path.join(models_dir, "yamnet_class_map.csv")
        self.distress_threshold = distress_threshold
        
        # Load class map
        self.class_names = self._load_class_map(self.class_map_path)
        
        # Map class names to indices
        self.distress_indices = [i for i, name in enumerate(self.class_names) if name in self.DISTRESS_CLASSES]
        self.noise_indices = [i for i, name in enumerate(self.class_names) if name in self.NOISE_CLASSES]
        
        # Initialize TFLite interpreter
        self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.waveform_input_index = self.input_details[0]["index"]
        self.scores_output_index = self.output_details[0]["index"]
        
        print(f"[YAMNet] Initialized with {len(self.class_names)} classes, {len(self.distress_indices)} distress targets, {len(self.noise_indices)} noise filters.")

    def _load_class_map(self, path: str) -> list:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Class map CSV not found at: {path}")
            
        classes = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                classes.append(row["display_name"])
        return classes

    def preprocess_audio(self, audio_bytes: bytes) -> np.ndarray:
        """
        Parses WAV audio bytes, downmixes to mono, resamples to 16,000 Hz,
        and normalizes samples to float32 in [-1.0, 1.0].
        """
        with wave.open(io.BytesIO(audio_bytes), "rb") as wav_file:
            n_channels = wav_file.getnchannels()
            sampwidth = wav_file.getsampwidth()
            framerate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            
            raw_frames = wav_file.readframes(n_frames)
            
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

            # Convert multi-channel to mono
            if n_channels > 1:
                audio_np = audio_np.reshape(-1, n_channels).mean(axis=1)

            # Normalize to float32 in range [-1.0, 1.0]
            if sampwidth == 1:
                audio_float = (audio_np.astype(np.float32) - 128.0) / 128.0
            else:
                audio_float = audio_np.astype(np.float32) / max_val

            # Resample to 16,000 Hz if necessary
            target_sr = 16000
            if framerate != target_sr and len(audio_float) > 0:
                # Calculate new number of samples
                num_target_samples = int(len(audio_float) * float(target_sr) / framerate)
                audio_float = scipy.signal.resample(audio_float, num_target_samples).astype(np.float32)

            return audio_float

    def classify(self, audio_bytes: bytes) -> dict:
        """
        Runs YAMNet inference on the given WAV audio bytes.
        Returns detailed classification metrics, distress scores, and noise flags.
        """
        waveform = self.preprocess_audio(audio_bytes)
        
        # Ensure minimum length of 0.975s (15600 samples) by zero-padding if too short
        min_samples = 15600
        if len(waveform) < min_samples:
            waveform = np.pad(waveform, (0, min_samples - len(waveform)), mode="constant")

        # Resize input tensor to match waveform length
        self.interpreter.resize_tensor_input(self.waveform_input_index, [len(waveform)], strict=False)
        self.interpreter.allocate_tensors()
        
        self.interpreter.set_tensor(self.waveform_input_index, waveform)
        self.interpreter.invoke()
        
        # Output shape: [N_frames, 521]
        scores = self.interpreter.get_tensor(self.scores_output_index)
        
        # Frame-aggregated scores: take max across frames for burst sounds like screams
        max_frame_scores = np.max(scores, axis=0)
        mean_frame_scores = np.mean(scores, axis=0)
        
        # Overall top predicted class
        top_idx = int(np.argmax(mean_frame_scores))
        top_detected_class = self.class_names[top_idx]
        top_detected_confidence = float(mean_frame_scores[top_idx])

        # Evaluate distress classes
        top_distress_class = None
        top_distress_score = 0.0
        for idx in self.distress_indices:
            score = float(max_frame_scores[idx])
            if score > top_distress_score:
                top_distress_score = score
                top_distress_class = self.class_names[idx]

        # Evaluate noise classes
        top_noise_class = None
        top_noise_score = 0.0
        for idx in self.noise_indices:
            score = float(max_frame_scores[idx])
            if score > top_noise_score:
                top_noise_score = score
                top_noise_class = self.class_names[idx]

        # Top 5 overall predicted classes
        top_5_indices = np.argsort(mean_frame_scores)[::-1][:5]
        top_5_predictions = [
            {"class": self.class_names[i], "score": round(float(mean_frame_scores[i]), 4)}
            for i in top_5_indices
        ]

        # Decision Logic:
        # 1. Check if distress score reaches threshold
        is_distress_candidate = top_distress_score >= self.distress_threshold
        
        # 2. Check if horn/siren/traffic noise strongly dominates the signal
        noise_suppressed = False
        if is_distress_candidate and top_noise_score > (top_distress_score * 1.5) and top_noise_score > 0.45:
            # Noise dominates scream artifact
            noise_suppressed = True
            is_distress = False
        else:
            is_distress = is_distress_candidate

        return {
            "distress_detected": is_distress,
            "distress_class": top_distress_class if is_distress else None,
            "distress_confidence": round(top_distress_score, 4),
            "noise_suppressed": noise_suppressed,
            "top_noise_class": top_noise_class,
            "top_noise_confidence": round(top_noise_score, 4),
            "top_detected_class": top_detected_class,
            "top_detected_confidence": round(top_detected_confidence, 4),
            "top_predictions": top_5_predictions,
        }
