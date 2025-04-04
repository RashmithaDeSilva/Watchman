import cv2
import base64
import eventlet
from flask import Flask, render_template
from flask_socketio import SocketIO

# Initialize Flask app and Socket.IO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for Socket.IO

@app.route('/')
def index():
    # Render the index.html template on the root URL
    return render_template('index.html')

def capture_frames():
    # Capture frames from the default camera and emit them to clients
    cap = cv2.VideoCapture(0)  # Initialize video capture from the default camera (index 0)

    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    while True:
        ret, frame = cap.read()  # Read a frame from the camera
        if not ret:
            print("Error: Failed to capture frame")
            break

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)  # Convert frame to JPEG format
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')  # Encode JPEG data to base64

        # Emit the encoded frame to all connected clients
        socketio.emit('frame', jpg_as_text)  # Send frame data to clients listening for 'frame' events

        eventlet.sleep(0.1)  # Sleep briefly to allow other tasks to execute

    cap.release()  # Release the camera resource when done

if __name__ == '__main__':
    # Start the Flask server with Socket.IO
    socketio.start_background_task(capture_frames)  # Run capture_frames concurrently in the background
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)