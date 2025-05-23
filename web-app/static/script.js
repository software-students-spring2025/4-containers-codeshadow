const video = document.querySelector("#video");
const startBtn = document.querySelector("#startBtn");
const container = document.querySelector(".contain");

const emojiDisplay = document.querySelector("#emojiDisplay");
const box = document.querySelector(".box")

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
        if (data.emotion && data.emoji) {
            console.log("Emotion Detected:", data.emotion);
            emojiDisplay.innerHTML = ` <span style="font-size: 8rem;">${data.emoji}</span>`;
            changeBackgroundColor(data.emotion);
        } else {
            emojiDisplay.innerHTML = `Could not detect emotion 😕`;
        }
    })
    .catch(err => {
        console.error('Emotion detection failed', err);
        emojiDisplay.innerHTML = `Error detecting emotion 😕`;
    });
}

async function sendImageToServer(base64Image) {
    const response = await fetch("/submit-image", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ image: base64Image })
    });
  
    const data = await response.json();
    console.log("Detected Emotion:", data.emotion, "Emoji:", data.emoji);
  
    // Update the emoji in the DOM
    const emojiDisplay = document.getElementById("emojiDisplay");
    if (emojiDisplay) {
      emojiDisplay.textContent = data.emoji;
    }
  }
  
  function changeBackgroundColor(emotion) {
    switch (emotion.toLowerCase()) {
        case 'happy':
            box.style.backgroundColor = 'yellow';
            break;
        case 'sad':
            box.style.backgroundColor = 'blue';
            break;
        case 'angry':
            box.style.backgroundColor = 'red';
            break;
        case 'surprised':
            box.style.backgroundColor = 'orange';
            break;
        case 'neutral':
            box.style.backgroundColor = 'gray';
            break;
        default:
            box.style.backgroundColor = 'aqua'; 
    }
}
