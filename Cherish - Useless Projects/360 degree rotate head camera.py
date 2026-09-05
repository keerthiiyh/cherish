import http.server
import os
import socketserver

# HTML string served directly from memory
HTML_CONTENT = r'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Funny Camera 360</title>
<style>
body {
    margin: 0;
    background: #111;
    color: white;
    font-family: Arial, sans-serif;
    text-align: center;
}
h1 { margin: 15px; }
.camera {
    width: 90vw;
    max-width: 900px;
    height: 65vh;
    margin: auto;
    position: relative;
    overflow: hidden;
    background: #000;
    border-radius: 20px;
    perspective: 1000px;
}
video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transform-style: preserve-3d;
    transition: transform 0.2s;
}
.overlay {
    position: absolute;
    inset: 0;
    pointer-events: none;
}
.emoji {
    position: absolute;
    font-size: 80px;
    left: 50%;
    top: 35%;
    transform: translate(-50%, -50%);
    display: none;
}
.controls { margin: 20px; }
button {
    padding: 12px 20px;
    margin: 5px;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    cursor: pointer;
}
button:hover { transform: scale(1.05); }
#status { font-size: 18px; margin: 10px; }
</style>
</head>
<body>

<h1>🤪 CAMERA CONFUSION 360°</h1>

<div id="status">Click START CAMERA</div>

<div class="camera" id="cameraBox">
    <video id="video" autoplay playsinline muted></video>
    <div class="overlay">
        <div class="emoji" id="funnyEmoji">🤪</div>
    </div>
</div>

<div class="controls">
    <button onclick="startCamera()">📷 START CAMERA</button>
    <button onclick="rotate360()">🔄 360° ROTATE</button>
    <button onclick="funnyFace()">🤪 FUNNY FACE</button>
    <button onclick="crazy()">😂 CRAZY MODE</button>
    <button onclick="normal()">🙂 NORMAL</button>
</div>

<script>
const video = document.getElementById("video");
const statusText = document.getElementById("status");
const emoji = document.getElementById("funnyEmoji");

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        await video.play();
        statusText.innerHTML = "📷 CAMERA ON — person is visible!";
    } catch(error) {
        statusText.innerHTML = "❌ Camera blocked or missing HTTPS context.";
        console.error(error);
    }
}

function rotate360() {
    statusText.innerHTML = "🔄 360° FACE ROTATION ACTIVATED 😂";
    video.style.transition = "transform 2s ease-in-out";
    video.style.transform = "rotateY(360deg)";
    setTimeout(() => { video.style.transform = "rotateY(0deg)"; }, 2100);
}

function funnyFace() {
    emoji.style.display = "block";
    statusText.innerHTML = "🤪 FUNNY FACE MODE ACTIVATED";
    video.style.filter = "hue-rotate(40deg) saturate(2) contrast(1.2)";
}

function crazy() {
    emoji.style.display = "block";
    emoji.innerHTML = "👽";
    statusText.innerHTML = "😂 CRAZY SNAP MODE";
    video.style.transition = "transform 0.5s";
    video.style.transform = "scaleX(-1) rotate(8deg) scale(1.15)";
    video.style.filter = "hue-rotate(180deg) saturate(3)";
}

function normal() {
    emoji.style.display = "none";
    video.style.transition = "transform 0.3s";
    video.style.transform = "none";
    video.style.filter = "none";
    statusText.innerHTML = "🙂 NORMAL CAMERA";
}
</script>
</body>
</html>
'''


class CameraRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the HTML page on root or direct file request
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode("utf-8"))


def main():
    # Bind to 0.0.0.0 and dynamically pull the PORT set by Render
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 10000))

    # Enable SO_REUSEADDR to easily restart without port conflict issues
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer((host, port), CameraRequestHandler) as httpd:
        print(f"Server starting on {host}:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
