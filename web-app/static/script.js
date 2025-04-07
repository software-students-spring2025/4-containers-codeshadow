
const startBtn = document.getElementById('startBtn');
const videoElement = document.getElementById('video');  
const boxesContainer = document.getElementById('boxes');
const Emo = document.getElementById('Username');
startBtn.addEventListener('click', function () {
    
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                videoElement.srcObject = stream;  
                boxesContainer.style.display = 'flex';
                startBtn.style.display= 'none';
                Emo.style.display='flex';
            })
            .catch(function (error) {
                console.error('Error accessing the webcam: ', error);
            });
    } else {
        alert('Your browser does not support webcam access');
    }
});