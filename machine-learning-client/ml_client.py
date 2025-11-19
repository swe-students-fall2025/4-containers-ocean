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
    mean_rms = float(np.mean(rms))

    # Send back simple features
    return mean_f0, mean_rms


def predict_emotion(mean_f0, mean_rms):

    if mean_f0 > 170 and mean_rms > 0.015:
        return "happy/excited"

    # Sad detection remains the same
    if mean_f0 < 150 and mean_rms < 0.01:
        return "sad"

    # Everything else
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

        # Simple log line in container logs
        print(
            f"{filename}: f0={mean_f0:.2f}, rms={mean_rms:.5f}, emotion={emotion_result}"
        )

        # Save result to emotion_results collection
        db.emotion_results.insert_one(
            {
                "filename": filename,
                "emotion": emotion_result,
                "mean_f0": float(mean_f0),
                "mean_rms": float(mean_rms),
                "timestamp": datetime.utcnow(),
            }
        )

        # Mark queue entry as processed
        db.audio_queue.update_one(
            {"_id": entry["_id"]}, {"$set": {"status": "processed"}}
        )

    except Exception as exc:  # keep errors visible in logs
        print(f"Error processing {filename}: {exc}")


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
