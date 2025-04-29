from flask import Flask, request, jsonify, send_file
from ultralytics import YOLO
import os
import uuid
import threading
import time
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for the app

# Define folders for file management
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
PREDICT_SAVE_FOLDER = "predict"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB max file size

# Create necessary directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(PREDICT_SAVE_FOLDER, exist_ok=True)

# Configure Flask app settings
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER
app.config["PREDICT_SAVE_FOLDER"] = PREDICT_SAVE_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# Define allowed file extensions
ALLOWED_EXTENSIONS = {"mp4"}

# Dictionary to keep track of processing jobs
processing_jobs = {}
lock = threading.Lock()  # Lock for thread safety

# Load YOLOv8 model
model = YOLO('watchman_v3.pt')

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to delete predicted and processed videos after a delay
def delete_video(video_path):
    time.sleep(30)  # Wait 30 seconds before deletion
    try:
        if os.path.exists(video_path):
            for file in os.listdir(video_path):
                os.remove(os.path.join(video_path, file))
            os.rmdir(video_path)  # Remove directory after files are deleted
    except Exception as e:
        print(f"Error deleting folder {video_path}: {e}")

# Function to remove job ID after processing
def delete_job_id(job_id):
    time.sleep(30)  # Wait before deletion
    with lock:
        processing_jobs.pop(job_id, None)

# Function to convert AVI video to MP4 format
def convert_to_mp4(avi_path, mp4_path, job_id):
    try:
        cmd = [
            "ffmpeg", "-i", avi_path, "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k", mp4_path
        ]
        subprocess.run(cmd, check=True)  # Run ffmpeg command to convert video

        with lock:
            processing_jobs[job_id] = 1  # Mark job as completed
    except subprocess.CalledProcessError as e:
        print(f"Error converting {avi_path} to MP4: {e}")

# Function to process the uploaded video
def process_video(filepath, job_id):
    """Handles YOLO object detection and video processing in a separate thread"""
    try:
        model(
            source=filepath,     # Input video path
            classes=[0],         # Detect only "person" class (class ID 0)
            imgsz=320,           # Set image size for YOLO
            conf=0.5,            # Confidence threshold
            iou=0.45,            # Intersection over Union (IoU) threshold
            device="cpu",        # Run on CPU
            vid_stride=2,        # Process every second frame for efficiency
            save=True,           # Save output video
            project=app.config["PREDICT_SAVE_FOLDER"],  # Output directory
            name=job_id,         # Output file name
            verbose=False,
            stream=False
        )

        # Locate the processed video output
        predict_path = os.path.join(app.config["PREDICT_SAVE_FOLDER"], job_id)
        processed_video = None

        if os.path.exists(predict_path):
            for file in os.listdir(predict_path):
                if file.endswith(".avi"):  # Check for AVI output file
                    processed_video = os.path.join(predict_path, file)
                    break

        # Remove uploaded file after processing
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error deleting uploaded video: {e}")

        if processed_video:
            # Create a folder for processed MP4 videos
            processed_mp4_path = os.path.join(app.config["PROCESSED_FOLDER"], job_id)
            os.makedirs(processed_mp4_path, exist_ok=True)

            # Convert processed AVI file to MP4
            convert_to_mp4(processed_video, os.path.join(processed_mp4_path, f"{job_id}.mp4"), job_id)

            # Mark job as completed
            processing_jobs[job_id] = 1

            # Schedule deletion of temporary files
            threading.Thread(target=delete_video, args=(predict_path,)).start()
            threading.Thread(target=delete_video, args=(processed_mp4_path,)).start()

    except Exception as e:
        print(f"Error processing video {job_id}: {e}")

# API endpoint to check the status of a job
@app.route("/api/v1/status/<job_id>", methods=["GET"])
def check_status(job_id):
    with lock:
        if job_id in processing_jobs:
            if processing_jobs[job_id] == 1:  # Job completed
                threading.Thread(target=delete_job_id, args=(job_id,)).start()  # Schedule job ID deletion
                processed_video_path = os.path.join(app.config["PROCESSED_FOLDER"], job_id, f"{job_id}.mp4")
                return send_file(processed_video_path, as_attachment=True)  # Send processed file
            return jsonify({"status": "processing"}), 102  # Job still processing
    
    return jsonify({"error": "Job not found"}), 404  # Job ID not found

import threading

# API endpoint to upload a video for processing
@app.route("/api/v1/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400  # No file in request

    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400  # Empty filename
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400  # Invalid file type

    # Generate a unique random filename
    hex_name = uuid.uuid4().hex[:64]
    new_filename = f"{hex_name}.mp4"
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
    file.save(filepath)  # Save the uploaded file

    # Mark job as started
    processing_jobs[hex_name] = 0  

    # Start video processing in a separate thread
    threading.Thread(target=process_video, args=(filepath, hex_name)).start()

    # Return job ID to the client
    return jsonify({"job_id": hex_name}), 200

# Run the Flask application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
