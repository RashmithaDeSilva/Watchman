from flask import Flask, request, jsonify, send_file
from ultralytics import YOLO
import os
import uuid
import threading
import time
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
PREDICT_SAVE_FOLDER = "predict"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(PREDICT_SAVE_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER
app.config["PREDICT_SAVE_FOLDER"] = PREDICT_SAVE_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

ALLOWED_EXTENSIONS = {"mp4"}

processing_jobs = {}
lock = threading.Lock()  # Thread safety

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Delete predicted and processed videos
def delete_video(video_path):
    time.sleep(30)  # Wait 30 seconds before deletion
    try:
        if os.path.exists(video_path):
            for file in os.listdir(video_path):
                os.remove(os.path.join(video_path, file))
            os.rmdir(video_path)
    except Exception as e:
        print(f"Error deleting folder {video_path}: {e}")

# Delete job ID
def delete_job_id(job_id):
    time.sleep(30)
    with lock:
        processing_jobs.pop(job_id, None)

# Convert AVI to MP4
def convert_to_mp4(avi_path, mp4_path, job_id):
    try:
        cmd = [
            "ffmpeg", "-i", avi_path, "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k", mp4_path
        ]
        subprocess.run(cmd, check=True)

        with lock:
            processing_jobs[job_id] = 1  # Mark job as completed
    except subprocess.CalledProcessError as e:
        print(f"Error converting {avi_path} to MP4: {e}")

# Prosess video
def process_video(filepath, job_id):
    """Handles the YOLO prediction and conversion in a separate thread"""
    try:
        model(
            source=filepath,    
            classes=[0],       
            imgsz=320,         
            conf=0.5,          
            iou=0.45,          
            device="cpu",      
            vid_stride=2,      
            save=True,         
            project=app.config["PREDICT_SAVE_FOLDER"],  
            name=job_id,  
        )

        # Locate the output video
        predict_path = os.path.join(app.config["PREDICT_SAVE_FOLDER"], job_id)
        processed_video = None

        if os.path.exists(predict_path):
            for file in os.listdir(predict_path):
                if file.endswith(".avi"):  
                    processed_video = os.path.join(predict_path, file)
                    break

        try:
            os.remove(filepath)  # Delete uploaded file
        except Exception as e:
            print(f"Error deleting uploaded video: {e}")

        if processed_video:
            processed_mp4_path = os.path.join(app.config["PROCESSED_FOLDER"], job_id)
            os.makedirs(processed_mp4_path, exist_ok=True)

            convert_to_mp4(processed_video, os.path.join(processed_mp4_path, f"{job_id}.mp4"), job_id)

            # Mark job as completed
            processing_jobs[job_id] = 1

            # Delete temporary files after processing
            threading.Thread(target=delete_video, args=(predict_path,)).start()
            threading.Thread(target=delete_video, args=(processed_mp4_path,)).start()

    except Exception as e:
        print(f"Error processing video {job_id}: {e}")

model = YOLO('yolov8n.pt')

@app.route("/api/v1/status/<job_id>", methods=["GET"])
def check_status(job_id):
    with lock:
        if job_id in processing_jobs:
            if processing_jobs[job_id] == 1:
                threading.Thread(target=delete_job_id, args=(job_id,)).start()
                processed_video_path = os.path.join(app.config["PROCESSED_FOLDER"], job_id, f"{job_id}.mp4")
                return send_file(processed_video_path, as_attachment=True)
            return jsonify({"status": "processing"}), 102
    
    return jsonify({"error": "Job not found"}), 404

import threading

@app.route("/api/v1/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # Generate a secure random filename
    hex_name = uuid.uuid4().hex[:64]
    new_filename = f"{hex_name}.mp4"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
    file.save(filepath)

    # Mark job as started
    processing_jobs[hex_name] = 0  

    # Start video processing in a separate thread
    threading.Thread(target=process_video, args=(filepath, hex_name)).start()

    # Return job ID immediately
    return jsonify({"job_id": hex_name}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
