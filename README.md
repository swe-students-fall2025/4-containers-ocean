![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Emotion Vocal Tracking – Project README (Updated for Person 3)

This repository contains the containerized multi-service system for our **Daily Emotion Tracker**.  
The system uses **3 Docker containers**:

1. **Web App (Flask)** – Handles browser recording + uploads audio to MongoDB queue.
2. **Machine-Learning Client** – Processes audio files using EmoVoice and writes emotion results to MongoDB.
3. **MongoDB** – Stores queued audio and final emotion logs.

This README is updated so **Person 3** can start working immediately.

---

# How to Run the Project (For Person 3)

Follow these steps exactly.  
You do **not** need Python locally. Everything runs inside Docker.

## 1. Make sure Docker Desktop is running
This project will not work without it.

## 2. Clone the repository
```
git clone <repo-url>
cd 4-containers-ocean
```

## 3. Build all containers
```
docker compose build
```

## 4. Start MongoDB + Web App + ML Client
```
docker compose up -d
```

You should now see three running containers:
- `emotion_web`
- `emotion_mongodb`
- `emotion_ml`

Check with:
```
docker compose ps
```

## 5. Open the web app
Visit:

```
http://localhost:5000
```

You should see the web interface.  
When you click “Record”, the browser saves `recording.webm` and sends it to your Flask backend.

These uploaded files appear in:

```
shared-audio volume → /data/uploads inside containers
```

MongoDB receives entries in the `audio_queue` collection.

---

# What Person 3 Needs to Know

## 1. Where the ML client runs
The machine-learning client code is in:

```
machine-learning-client/ml_client.py
machine-learning-client/audio_processor.py
```

Its Dockerfile is already set up to install:
- ffmpeg
- numpy
- pydub
- pymongo

And it mounts the same shared audio directory as the web app:
```
/data/uploads
```

This is where your ML code will read audio files.

## 2. What the ML client needs to do
You will:

- Poll MongoDB’s `audio_queue` collection for documents with `"status": "pending"`
- Load the webm/wav file from `AUDIO_DIR` (env var)
- Use EmoVoice or pitch detection to classify emotion
- Write an entry into a new collection `emotion_history`
- Update the queue entry status → `"processed"`

You can run ML client logs with:
```
docker compose logs -f ml-client
```

Restart ML client after edits:
```
docker compose up -d --build ml-client
```

## 3. How to enter the ML client container
This is useful when debugging:
```
docker compose exec ml-client sh
```

Inside:
```
ls /data/uploads
python3
```

---

# MongoDB Information (For Person 3)

### Connection string:
```
mongodb://mongodb:27017/emotiondb
```

### Collections already created by Person 2:
- `audio_queue` (incoming audio files)
- `emotion_history` (you will write here)

### Confirm Mongo entries:
```
docker compose exec web-app python
```

Then inside Python:
```python
from pymongo import MongoClient
c = MongoClient("mongodb://mongodb:27017/")
db = c["emotiondb"]
list(db.audio_queue.find())
```

---

# File Paths to Pay Attention To

## Audio directory inside containers:
```
/data/uploads
```

## ML client environment variables:
```
AUDIO_DIR=/data/uploads
MONGO_URI=mongodb://mongodb:27017/emotiondb
```

## Web app upload folder is mapped to the same place:
Meaning ML and Web App see the **same audio file**.

---

# Important Notes for Person 3

- You **do NOT** run Python from your host. Everything is inside Docker.
- You **must add a requirements.txt** in `machine-learning-client` if you add more dependencies later.
- The ML client must be long-running (while-loop that checks the queue periodically).
- Do not modify the working Flask or Web App container — Person 2 has already tested that layer.
- You only work inside:

```
machine-learning-client/
```

---

# Person 3 Workflow Summary

## Step 1  
Run the whole system:
```
docker compose up -d
```

## Step 2  
Check that uploads appear in MongoDB:
```
docker compose exec web-app python
```
Then:
```python
from pymongo import MongoClient
c = MongoClient("mongodb://mongodb:27017/")
db = c["emotiondb"]
list(db.audio_queue.find())
```

## Step 3  
Write ML pipeline inside `ml_client.py`:
- read queue
- analyze audio
- write results

## Step 4  
Rebuild and test your ML container:
```
docker compose up -d --build ml-client
```

## Step 5  
Test multiple recordings through the web browser.

---

# Current System Status

Person 2 has already completed:
- Working browser → Flask upload pipeline  
- Audio saved to shared volume  
- MongoDB queue insertion  
- Docker builds for all services  
- Docker Compose networking works  
- Testing of confirmed entries in MongoDB

---

# Person 3 Deliverables

1. Working ML client loop  
2. Pitch/emotion analysis using EmoVoice or simple heuristic  
3. Writes results to MongoDB  
4. Marks queue entries `"processed"`  
5. Creates/stores emotion metrics in `emotion_history` collection  
6. Tested end-to-end (upload → analysis → DB entry)

---

# Notes on VS Code Warnings

If VS Code shows:
- `flask` cannot be resolved  
- `pymongo` cannot be resolved

That is because your **local machine** does not install Python dependencies.  
This is expected — everything runs in Docker.

Ignore these warnings.

---

# Done

This README gives Person 3 everything needed to start immediately.