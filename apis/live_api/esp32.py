from flask import Flask, Response
import cv2
from ultralytics import YOLO
import datetime
import os

app = Flask(__name__)
ESP32_STREAM_URL = 'http://192.168.1.2:80'  # Replace with your ESP32 IP
model = YOLO('yolov8n.pt')

output_dir = "footages"
os.makedirs(output_dir, exist_ok=True)

saving = False
writer = None

# --- Raw Live Stream (no detection) ---
def raw_stream():
    cap = cv2.VideoCapture(ESP32_STREAM_URL)
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/live')
def live():
    return Response(raw_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


# --- Detection Stream with YOLOv8n ---
def detect_stream():
    global saving, writer

    cap = cv2.VideoCapture(ESP32_STREAM_URL)

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, stream=True)
        person_detected = any(
            model.names[int(cls)] == "person"
            for r in results for cls in r.boxes.cls
        )

        annotated_frame = results[0].plot()

        if person_detected and not saving:
            saving = True
            filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".avi"
            filepath = os.path.join(output_dir, filename)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            writer = cv2.VideoWriter(filepath, fourcc, 10.0, (frame.shape[1], frame.shape[0]))
            print(f"[INFO] Started recording: {filename}")

        if not person_detected and saving:
            saving = False
            writer.release()
            writer = None
            print("[INFO] Stopped recording")

        if saving and writer is not None:
            writer.write(frame)

        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/detect')
def detect():
    return Response(detect_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return 'Endpoints: /live (raw stream), /detect (YOLO detection stream)'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
