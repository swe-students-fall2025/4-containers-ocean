FROM python:3.10-slim

# system deps (ffmpeg is useful for audio format conversion)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

ENV MONGO_URI=mongodb://mongodb:27017/emotiondb
ENV AUDIO_DIR=/data/uploads

CMD ["python", "ml_client.py"]
