from flask import Flask, request, jsonify, send_file
from ultralytics import YOLO
import os
import uuid

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
PREDICT_SAVE_FOLDER = "predict"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(PREDICT_SAVE_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER
app.config["PREDICT_SAVE_FOLDER"] = PREDICT_SAVE_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

ALLOWED_EXTENSIONS = {"mp4"}  # Add other formats if needed

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Load a small YOLO model optimized for CPU
model = YOLO('yolov8n.pt')

@app.route("/upload", methods=["POST"])
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
    
    # Process video with YOLO
    results = model(
        source=filepath,    # Process only this file
        classes=[0],        # Detect only "person"
        imgsz=320,          # Reduce image size for faster processing
        conf=0.5,           # Confidence threshold
        iou=0.45,           # Intersection over Union threshold
        device="cpu",       # Use CPU
        vid_stride=2,       # Skip frames to speed up processing
        save=True,          # Save processed video
        project=app.config["PREDICT_SAVE_FOLDER"],# Predict video save main folder
        name=hex_name,  # Save file name
    )
    
    # Find the output video
    processed_video = None
    predict_path = os.path.join(app.config["PREDICT_SAVE_FOLDER"], hex_name)  # Path where YOLO saves output

    if os.path.exists(predict_path):
        for file in os.listdir(predict_path):
            if file.endswith(".avi"):  # Ensure get the processed video
                processed_video = os.path.join(predict_path, file)
                break
    
    try:
        # Delete uploaded video after processing
        os.remove(filepath)
    except Exception as e:
        print(f"Error deleting folder upload {new_filename}: {e}")
    
    if processed_video:
        # Load processed video
        response = send_file(processed_video, as_attachment=True)

        # # Delete only the "new_filename" directory inside PREDICT_SAVE_FOLDER
        # try:
        #     for file in os.listdir(predict_path):
        #         os.remove(os.path.join(predict_path, file))  # Delete files inside the folder
        #     os.rmdir(predict_path)  # Remove the empty folder
        # except Exception as e:
        #     print(f"Error deleting folder {predict_path}: {e}")

        # Send the processed video to the user
        return response
    
    return jsonify({"error": "Processing failed"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)  
