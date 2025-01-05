document.getElementById('uploadBtn').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function() {
    var file = this.files[0];
    if (file) {
        var videoContainer = document.getElementById('videoContainer');
        videoContainer.innerHTML = ''; // Clear previous video if any
        var video = document.createElement('video');
        video.src = URL.createObjectURL(file);
        video.controls = true;
        videoContainer.appendChild(video);
    }
});
