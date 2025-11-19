![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Emotion Vocal Tracking

A containerized multi-service system for a Daily Emotion Tracker, consisting of three Docker containers:

Web App (Flask) – Handles browser recording, uploads audio to MongoDB, and displays a dashboard of analyzed emotions.

Machine-Learning Client – Processes audio using EmoVoice logic and writes emotion results to MongoDB.

MongoDB – Stores queued audio and final emotion logs.

This README is updated for Person 4, who is responsible for CI, testing, dashboard integration, and full system verification.

🚀 How to Run the Project (Person 4)

You do not need Python installed locally—everything runs inside Docker.

1. Start Docker Desktop

This project will not run without it.

2. Clone the repository
   git clone <repo-url>
   cd 4-containers-ocean

3. Build all containers
   docker compose build

4. Start MongoDB + Web App + ML Client
   docker compose up -d

## You should now see three running containers:

emotion_web

emotion_mongodb

emotion_ml

Check status with:

docker compose ps

5. Open the Web App

http://localhost:5000

- Click Record in the UI — the browser saves recording.webm and sends it to the Flask backend.

- Stored files appear in:

/data/uploads (shared Docker volume)

- MongoDB receives new entries in the audio_queue collection.

- The dashboard displays all past recordings and their analyzed emotions.

## 📊 Dashboard Integration (Main Task for Person 4)

The dashboard must allow users to:

View all past recordings

See the emotion label (happy or sad)

Play back audio directly in the browser

## Example Flask Route

```python
from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient("mongodb://mongodb:27017/")["emotiondb"]

@app.route('/')
def index():
    history = list(db.emotion_history.find().sort("timestamp", -1))
    return render_template('index.html', history=history)

<div>
  <p>{{ entry.filename }} – {{ entry.emotion }} – {{ entry.timestamp }}</p>
  <audio controls>
    <source src="/uploads/{{ entry.filename }}" type="audio/wav">
  </audio>
</div>
{% endfor %}
```

## 🎯 Goal

The dashboard should visually and interactively show **all stored emotion analyses**, including audio playback and detected emotion labels.

---

# 🔧 CI / GitHub Actions Setup

**Required workflows:**

- `web-app-ci.yml`
- `ml-client-ci.yml`

---

## Each workflow should:

- Install dependencies
- Run **black** (formatting)
- Run **pylint** (linting)
- Run **pytest** with coverage
- Fail if **coverage < 80%**

---

## 🧪 Test Directories

- web-app/tests/
- machine-learning-client/tests/

---

## Tests should validate:

- Web app file upload route
- `process_audio_file` in the ML client
- MongoDB inserts and updates
- Dashboard correctly displays analyzed emotions

---

# 🐳 Docker-Compose Finalization

Start all containers with:

bash
docker compose up -d --build

Check volume mapping:

/data/uploads → shared between Web App & ML Client

# 🔁 End-to-End Testing Checklist

Record audio in the browser

Upload goes to MongoDB audio_queue

ML Client polls → analyzes pitch → predicts emotion

ML Client writes results to emotion_history

Dashboard displays the new entry + audio playback

Check DB entries manually:
from pymongo import MongoClient
db = MongoClient("mongodb://mongodb:27017/")["emotiondb"]
list(db.audio_queue.find())
list(db.emotion_history.find())

# 🤖 ML Client Emotion Detection Reference

Pipeline created by Person 3:

Load .wav file from /data/uploads

Analyze pitch with EmoVoice logic

If high pitch → emotion = "happy"

If low pitch → emotion = "sad"

Insert into emotion_history

Mark queue entry "status": "processed"

Tests must validate this entire chain.

# 📁 File Paths & Environment Variables

Shared audio directory:
/data/uploads

ML Client environment variables:
AUDIO_DIR=/data/uploads
MONGO_URI=mongodb://mongodb:27017/emotiondb

The web app and ML client both mount the same shared volume.

# ✅ Person 4 Deliverables Summary

CI workflows for Web App + ML Client

≥ 80% Pytest coverage

Fully working Docker Compose stack

Dashboard UI showing emotions + audio playback

Verified E2E pipeline (browser → ML → dashboard)

Updated, consistent README (this file)
