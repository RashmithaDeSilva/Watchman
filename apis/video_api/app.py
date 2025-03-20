from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1GB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE  # Enforce size limit

ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
