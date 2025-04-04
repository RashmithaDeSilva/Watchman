from flask import Flask, Response, jsonify, send_from_directory
import cv2
from ultralytics import YOLO
from datetime import datetime
import os
import subprocess
import threading
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Load YOLOv8n model
model = YOLO("yolov8n.pt")
model.fuse()

# Create footage directory if it doesn't exist
os.makedirs("footages", exist_ok=True)

# Webcam capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Frame processing settings
frame_count = 0
vid_stride = 2  # Process every 2nd frame for performance
recording = False
out = None
no_person_frames = 0
max_no_person_frames = 10  # Number of frames to wait before stopping recording

# Paths for video files
avi_path = None
mp4_path = None

# Flag to control saving
is_saving_enabled = {"enabled": False}

# Convert .avi to .mp4 in background
def convert_to_mp4(avi_file, mp4_file):
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", avi_file,
            "-vcodec", "libx264", "-crf", "23", mp4_file
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True)
        
        os.remove(avi_file)
        print(f"[INFO] Converted and saved: {mp4_file}")
    except Exception as e:
        print(f"[ERROR] FFmpeg conversion failed: {e}")

# Live detection & video stream
def generate_frames():
    global frame_count, out, recording, no_person_frames, avi_path, mp4_path

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1
        if frame_count % vid_stride != 0:
            continue

        # Run inference
        results = model.predict(
            source=frame,
            imgsz=320,
            conf=0.5,
            iou=0.45,
            device='cpu',
            verbose=False
        )[0]

        # Detect person
        person_detected = False
        for box in results.boxes:
            cls_id = int(box.cls[0])
            if model.names[cls_id] == "person":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "person", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                person_detected = True

        # Start recording
        if is_saving_enabled["enabled"] and person_detected:
            no_person_frames = 0
            if not recording:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                avi_path = f"footages/{timestamp}.avi"
                mp4_path = f"footages/{timestamp}.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # AVI format (fast)
                out = cv2.VideoWriter(avi_path, fourcc, 10.0, (640, 480))
                print(f"[INFO] Started recording: {avi_path}")
                recording = True
        else:
            if recording:
                no_person_frames += 1
                if no_person_frames >= max_no_person_frames:
                    recording = False
                    if out:
                        out.release()
                        out = None
                        print(f"[INFO] Stopped recording. Converting to MP4...")
                        # Convert in background
                        threading.Thread(target=convert_to_mp4, args=(avi_path, mp4_path)).start()

        # Write frame to video if recording
        if recording and out:
            out.write(frame)

        # Stream to browser
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Route to video stream
@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/footages")
def list_footages():
    files = os.listdir("footages")
    mp4_files = sorted([f for f in files if f.endswith(".mp4")], reverse=True)
    return jsonify(mp4_files)

@app.route("/footages/<path:filename>")
def download_footage(filename):
    return send_from_directory("footages", filename)

@app.route("/start-saving", methods=["POST"])
def start_saving():
    is_saving_enabled["enabled"] = True
    return jsonify({"message": "Saving started"}), 200

@app.route("/stop-saving", methods=["POST"])
def stop_saving():
    is_saving_enabled["enabled"] = False
    return jsonify({"message": "Saving stopped"}), 200

@app.route("/is-saving", methods=["GET"])
def check_saving_status():
    return jsonify({"saving": is_saving_enabled["enabled"]}), 200

# Run the Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
