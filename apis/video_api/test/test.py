import requests
import unittest
import os
import time

API_URL = "http://127.0.0.1:5001/api/v1/upload"
STATUS_URL = "http://127.0.0.1:5001/api/v1/status"
TEST_VIDEO_PATH = "sample.mp4"  # Replace with a real test video under 100MB


class TestVideoUploadAPI(unittest.TestCase):

    def print_result(self, test_name, expected_status, actual_status):
        print(f"\nTest: {test_name}")
        print(f"Expected Result: HTTP {expected_status}")
        print(f"Actual Result:   HTTP {actual_status}")

    def wait_for_processing(self, job_id, timeout=60):
        """Poll the status endpoint until job is done or timeout."""
        print(f"Waiting for job {job_id} to complete...")
        start = time.time()
        while time.time() - start < timeout:
            response = requests.get(f"{STATUS_URL}/{job_id}")
            if response.status_code == 200:
                return response  # Processed file returned
            elif response.status_code == 102:
                time.sleep(2)  # Job is still processing
            else:
                break  # Unexpected error
        return None

    def test_successful_upload_and_processing(self):
        """Test uploading a valid video and retrieving the processed result."""
        with open(TEST_VIDEO_PATH, "rb") as file:
            response = requests.post(API_URL, files={"file": file})

        self.print_result("Successful Upload", 200, response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertIn("job_id", response.json())

        job_id = response.json().get("job_id")
        result_response = self.wait_for_processing(job_id)

        self.assertIsNotNone(result_response, "Processing did not complete in time.")
        self.assertEqual(result_response.status_code, 200)

        # Save the processed result locally
        result_path = f"processed_result_{job_id}.mp4"
        with open(result_path, "wb") as f:
            f.write(result_response.content)
        print(f"✅ Processed video saved as: {result_path}")

    def test_missing_file_field(self):
        """Test upload request with no file field."""
        response = requests.post(API_URL, files={})
        self.print_result("Missing File Field", 400, response.status_code)
        self.assertEqual(response.status_code, 400)

    def test_invalid_file_type(self):
        """Test uploading an invalid file type."""
        with open(__file__, "rb") as file:  # Upload this Python script
            response = requests.post(API_URL, files={"file": file})
        self.print_result("Invalid File Type", 400, response.status_code)
        self.assertEqual(response.status_code, 400)

    def test_empty_filename(self):
        """Test uploading a file with empty filename (simulated)."""
        file = ("", b"dummy content")
        response = requests.post(API_URL, files={"file": file})
        self.print_result("Empty Filename", 400, response.status_code)
        self.assertEqual(response.status_code, 400)

    # Uncomment to simulate large file rejection (manually test with a real >100MB file)
    # def test_large_file_rejection(self):
    #     """Test uploading a file larger than 100MB."""
    #     big_file_path = "big_file.mp4"
    #     with open(big_file_path, "wb") as f:
    #         f.seek((100 * 1024 * 1024) + 1)
    #         f.write(b"\0")
    #     with open(big_file_path, "rb") as file:
    #         response = requests.post(API_URL, files={"file": file})
    #     os.remove(big_file_path)
    #     self.print_result("Large File Rejection", 413, response.status_code)
    #     self.assertEqual(response.status_code, 413)

if __name__ == "__main__":
    unittest.main()
