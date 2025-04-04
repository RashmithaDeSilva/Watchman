# 🛡️ Watchman

**Watchman** is a CCTV storage management system that uses AI-powered object detection to store only the important parts of CCTV footage. It supports both real-time detection from live CCTV streams and analysis of uploaded footage, with a focus on detecting humans. The system is optimized for minimal-resource devices like Raspberry Pi Zero 2 W using a custom-trained YOLOv8n model.

---

## 🚀 Features

- 🎥 Real-time human detection from CCTV or webcam streams
- 📁 Analyze uploaded CCTV footage for object detection
- 💾 Save only relevant footage (when a person is detected)
- 🧠 YOLOv8n model trained and optimized for low-resource environments
- 🌐 Responsive frontends for both live and upload modes using Next.js
- 🐳 Fully containerized microservices architecture using Docker

---

## 🧱 Project Structure

```
watchman/
    ├── apis/
        ├── live-api/ # Flask API for real-time CCTV analysis 
        ├── video-api/ # Flask API for analyzing uploaded videos
    ├── frontends
        ├── local/ # Next.js frontend for live detection 
        ├── cloud/ # Next.js frontend for video upload analysis 
    ├── model/ # YOLOv8n trained model (only detects person)
        ├── notebooks
    ├── README.md 
    └── docker-compose.yml # Optional Docker Compose file
```

---

## 🧪 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Object Detection**: YOLOv8n (Ultralytics)
- **Video Processing**: FFmpeg
- **Containerization**: Docker
- **Hardware Support**: Raspberry Pi Zero 2 W, ESP32-CAM

---

## 📦 Live Detection API

This service allows real-time analysis of live video streams (from a webcam or IP camera). It detects humans and saves footage only when someone is present.

### 🔧 Key Features

- Connect to webcam or network CCTV
- Detect only `person` class
- Start and stop detection dynamically
- Save `.avi` when detection is triggered
- Convert `.avi` to `.mp4` using FFmpeg in the background
- Serve saved footage on request

### 📡 Endpoints
```
POST /start_stream # Start video stream from source 

GET /video_feed # Raw MJPEG stream 

POST /start_detection # Start YOLOv8n person detection 

POST /stop_detection # Stop detection and recording 

GET /footages # List recorded footage
```

---

## 📁 Upload Footage API

This API allows users to upload video files (e.g., from existing CCTV footage) for offline human detection.

### 🔧 Key Features

- Upload video up to 1GB
- Run detection with YOLOv8n on uploaded file
- Return video with bounding boxes over detected humans
- Simple integration with Next.js frontend

### 📡 Endpoints
```
POST /upload # Upload video for processing 

GET /processed/<filename> # Retrieve detected video
```

---

## 🧠 YOLOv8n Model

- Trained on [constantinwerner/human-detection-dataset](https://huggingface.co/datasets/constantinwerner/human-detection-dataset)
- Detects only the `person` class
- Optimized using YOLOv8n for minimal-size devices like Raspberry Pi
- Saved model available in the `model/` directory

---

## 🌐 Frontends

Two separate frontends have been developed using **Next.js + Tailwind CSS**:

### 🔴 `frontend-live`

- Interface for live video stream and detection
- Watch video in real-time
- Start/stop detection and view saved footages

### 📤 `frontend-upload`

- Upload CCTV footage (drag and drop supported)
- View processed video with detections

---

## 📂 Footage Directory

All detected footage is stored in the `footages/` directory as:

```
footages/ ├── 2025-04-04_15-22-10.avi # Raw 
recording └── 2025-04-04_15-22-10.mp4 # 
Auto-converted by FFmpeg
```

---

## 🐳 Dockerization

Each service is containerized for easy deployment. You can build and run them individually or with Docker Compose.

### 🔨 Build and Run Manually

```bash
docker build -t watchman-live live-detection-api/
docker run -p 5000:5000 watchman-live

docker build -t watchman-upload upload-analysis-api/
docker run -p 5001:5000 watchman-upload
docker-compose up --build
```
---

### ⚙️ Requirements
* Python 3.9+

* Node.js 18+

* FFmpeg installed

* Ultralytics YOLOv8 installed (pip install ultralytics)

* Docker (optional but recommended)

* Raspberry Pi (for edge use case)
---

### 🧠 Future Plans
* WebSocket-based live dashboard

* Cloud storage support for detected footages

* Multi-camera stream handling

* Admin dashboard with statistics
