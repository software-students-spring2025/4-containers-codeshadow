const video = document.querySelector("#video");
const startBtn = document.querySelector("#startBtn");
const container = document.querySelector(".contain");

startBtn.addEventListener("click", () => {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            console.log("Camera access granted.");
            video.srcObject = stream;
            video.play();
            container.style.display = "flex";
            startBtn.style.display = "none";
            setInterval(() => captureAndSendImage(video), 5000); // every 5 sec
        })
        .catch((err) => console.error("Camera error:", err));
});

function captureAndSendImage(videoElement) {
    if (!videoElement.videoWidth || !videoElement.videoHeight) {
        console.warn("Video not ready yet.");
        return;
    }

    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoElement, 0, 0);

    const base64Image = canvas.toDataURL('image/jpeg');

    fetch('/submit-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: base64Image })
    })
    .then(res => res.json())
    .then(data => {
        if (data.emotion) {
            console.log("Emotion Detected:", data.emotion);
        } else {
            console.log("Server response:", data);
        }
    })
    .catch(err => console.error('Emotion detection failed', err));
}
