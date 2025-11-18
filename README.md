![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

# Containerized App Exercise

# Emotion Vocal Tracking – Project Skeleton

This repository contains the initial scaffold for our containerized Daily Emotion Tracker project.

Person 1 (Kaiyuan) completed the initial project setup — folder structure, placeholder code, Dockerfiles, docker-compose, and basic documentation.  
This setup allows Person 2, 3, and 4 to continue development smoothly.

---

## 📁 Folder Structure Overview


machine-learning-client/
ml_client.py
audio_processor.py
Dockerfile

web-app/
app.py
templates/index.html
static/record.js
Dockerfile

docker-compose.yml


---

### Person 1 — Kaiyuan
Project Initialization (25%)
Set up the full repo structure
Create starter files and placeholder code
Create Dockerfiles for each subsystem
Create docker-compose.yml with placeholder services
Create base Pipfiles
Write root README
Prepare structure for next developers
### Person 2 – Web App Developer
- Implement real Flask routes
- Build emotion dashboard UI
- Integrate MongoDB
- Implement audio upload / trigger

### Person 3 – ML Client Developer
- Implement sounddevice recording
- Use EmoVoice to evaluate pitch/emotion
- Write real results to MongoDB

### Person 4 – Testing & CI
- Add pytest tests (80%+ coverage)
- Add CI workflows in `.github/workflows`
- Add lint/format pipelines
