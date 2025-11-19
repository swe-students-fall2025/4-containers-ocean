"""Placeholder ML client module for project initialization."""


import os
from datetime import datetime
from pymongo import MongoClient
from pydub import AudioSegment
import librosa
import numpy as np
import time

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/emotiondb")
AUDIO_DIR = os.environ.get("AUDIO_DIR", "/data/uploads")

def compute_features(file_path):
    # Load audio
    y, sr = librosa.load(file_path, sr=None)
    # Pitch (fundamental frequency) using pyin
    f0, voiced_flag, _ = librosa.pyin(y, fmin=50, fmax=500)
    mean_f0 = np.nanmean(f0) if f0 is not None else 0.0

    # Energy
    rms = librosa.feature.rms(y=y)
    mean_rms = np.mean(rms)

    # Other features can be added here (MFCCs, spectral centroid, etc.)
    return mean_f0, mean_rms

def predict_emotion(mean_f0, mean_rms):
    """
    Simple heuristic for demonstration:
    - High pitch + high energy -> excited/happy
    - Low pitch + low energy -> sad
    - Otherwise -> neutral
    """
    if mean_f0 > 200 and mean_rms > 0.02:
        return "happy/excited"
    elif mean_f0 < 150 and mean_rms < 0.01:
        return "sad"
    else:
        return "neutral"

def process_audio_file(entry, db):
    filename = entry["filename"]
    input_path = os.path.join(AUDIO_DIR, filename)
    try:
        # Convert webm -> wav if needed
        if filename.endswith(".webm"):
            wav_path = os.path.join(AUDIO_DIR, filename.replace(".webm", ".wav"))
            audio = AudioSegment.from_file(input_path, format="webm")
            audio.export(wav_path, format="wav")
        else:
            wav_path = input_path

        # Extract features
        mean_f0, mean_rms = compute_features(wav_path)
        emotion_result = predict_emotion(mean_f0, mean_rms)

        print(f"{filename}: Predicted emotion -> {emotion_result}")

        # Save to emotion_history
        db.emotion_history.insert_one({
            "filename": filename,
            "emotion": emotion_result,
            "mean_f0": float(mean_f0),
            "mean_rms": float(mean_rms),
            "timestamp": datetime.utcnow()
        })

        # Update queue status
        db.audio_queue.update_one(
            {"_id": entry["_id"]},
            {"$set": {"status": "processed"}}
        )

    except Exception as e:
        print(f"Error processing {filename}: {e}")

def main():
    client = MongoClient(MONGO_URI)
    db = client["emotiondb"]
    print("ML client started, polling for new audio...")

    while True:
        pending_files = list(db.audio_queue.find({"status": "pending"}))
        for entry in pending_files:
            process_audio_file(entry, db)
        time.sleep(5)

if __name__ == "__main__":
    main()
