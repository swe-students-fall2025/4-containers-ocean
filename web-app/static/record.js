let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const status = document.getElementById("status");

startBtn.onclick = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    audioChunks = [];
    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

    mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, { type: "audio/webm" });
        const file = new File([blob], "recording.webm");

        const formData = new FormData();
        formData.append("audio", file);

        const res = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        status.innerHTML = "Uploaded: " + data.filename;
    };

    mediaRecorder.start();
    status.textContent = "Recording...";

    startBtn.disabled = true;
    stopBtn.disabled = false;
};

stopBtn.onclick = () => {
    mediaRecorder.stop();
    status.textContent = "Processing...";
    startBtn.disabled = false;
    stopBtn.disabled = true;
};