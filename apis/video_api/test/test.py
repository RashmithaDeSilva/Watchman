import requests
import unittest
import os

API_URL = "http://127.0.0.1:5001/upload"
TEST_VIDEO_PATH = "sample.mp4"  # Replace with an actual test video

class TestVideoUploadAPI(unittest.TestCase):

    def print_result(self, test_name, expected_status, actual_status):
        print(f"\nTest: {test_name}")
        print(f"Expected Result: HTTP {expected_status}")
        print(f"Actual Result:   HTTP {actual_status}")

    def test_successful_upload(self):
        """Test uploading a valid video file."""
        with open(TEST_VIDEO_PATH, "rb") as file:
            response = requests.post(API_URL, files={"file": file})

        self.print_result("Successful Upload", 200, response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_missing_file_field(self):
        """Test upload request with no file field."""
        response = requests.post(API_URL, files={})

        self.print_result("Missing File Field", 400, response.status_code)
        self.assertEqual(response.status_code, 400)

    def test_invalid_file_type(self):
        """Test uploading an invalid file type."""
        with open(__file__, "rb") as file:  # Uploading this Python script instead of a video
            response = requests.post(API_URL, files={"file": file})

        self.print_result("Invalid File Type", 400, response.status_code)
        self.assertEqual(response.status_code, 400)

    def test_large_file_rejection(self):
        """Test uploading a file larger than 1GB (simulated)."""
        big_file_path = "big_file.mp4"

        # Create a dummy large file (1GB + 1MB) for testing
        with open(big_file_path, "wb") as f:
            f.seek((1 * 1024 * 1024 * 1024) + (1 * 1024 * 1024) - 1)
            f.write(b"\0")

        with open(big_file_path, "rb") as file:
            response = requests.post(API_URL, files={"file": file})

        os.remove(big_file_path)  # Clean up the test file

        self.print_result("Large File Rejection", 413, response.status_code)
        self.assertEqual(response.status_code, 413)  # 413 Payload Too Large

if __name__ == "__main__":
    unittest.main()
