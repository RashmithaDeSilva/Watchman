import os
import pytest
from app import app, is_saving_enabled

# pytest test.py

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_start_saving(client):
    response = client.post("/start-saving")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Saving started"
    assert is_saving_enabled["enabled"] is True

def test_stop_saving(client):
    response = client.post("/stop-saving")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Saving stopped"
    assert is_saving_enabled["enabled"] is False

def test_check_saving_status(client):
    # Ensure known state
    is_saving_enabled["enabled"] = True
    response = client.get("/is-saving")
    assert response.status_code == 200
    assert response.get_json()["saving"] is True

    is_saving_enabled["enabled"] = False
    response = client.get("/is-saving")
    assert response.status_code == 200
    assert response.get_json()["saving"] is False

def test_list_footages(client, tmp_path):
    # Setup mock files
    test_dir = tmp_path / "footages"
    test_dir.mkdir()
    test_file = test_dir / "test_video.mp4"
    test_file.write_text("mock video content")

    # Patch the footage directory
    original_dir = os.listdir
    os.listdir = lambda path: ["test_video.mp4"] if path == "footages" else original_dir(path)

    response = client.get("/footages")
    assert response.status_code == 200
    assert "test_video.mp4" in response.get_json()

    # Revert monkeypatch
    os.listdir = original_dir

def test_download_footage(client, tmp_path):
    test_dir = tmp_path / "footages"
    test_dir.mkdir()
    test_file = test_dir / "sample.mp4"
    test_file.write_text("dummy content")

    # Patch send_from_directory behavior
    app.config["TESTING"] = True
    os.makedirs("footages", exist_ok=True)
    with open("footages/sample.mp4", "w") as f:
        f.write("dummy content")

    response = client.get("/footages/sample.mp4")
    assert response.status_code == 200
    assert response.data == b"dummy content"

    os.remove("footages/sample.mp4")

def test_video_route_exists(client):
    response = client.get("/video")
    # Can't fully test streaming, just check response is being returned
    assert response.status_code == 200
    assert response.content_type.startswith("multipart/x-mixed-replace")
