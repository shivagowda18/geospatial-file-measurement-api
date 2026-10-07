from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_upload_kml():
    file_path = (
        Path(__file__).resolve().parents[1]
        / "sample_data"
        / "test_polygon.kml"
    )

    with file_path.open("rb") as file:
        response = client.post(
            "/api/files/",
            files={
                "file": (
                    "test_polygon.kml",
                    file,
                    "application/vnd.google-earth.kml+xml",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test_polygon.kml"
    assert data["feature_count"] == 1
    assert data["crs"] == "EPSG:4326"
    assert data["status"] == "COMPLETED"

    measurement = data["measurements"][0]

    assert measurement["geometry_type"] == "Polygon"
    assert measurement["unit"] == "m²"
    assert measurement["measurement"] > 0

def test_get_measurements():
    file_path = (
        Path(__file__).resolve().parents[1]
        / "sample_data"
        / "test_polygon.kml"
    )

    with file_path.open("rb") as file:
        upload_response = client.post(
            "/api/files/",
            files={
                "file": (
                    "test_polygon.kml",
                    file,
                    "application/vnd.google-earth.kml+xml",
                )
            },
        )

    assert upload_response.status_code == 200

    file_id = upload_response.json()["id"]

    response = client.get(
        f"/api/files/{file_id}/measurements/"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["file_id"] == file_id
    assert len(data["measurements"]) == 1
    assert data["measurements"][0]["geometry_type"] == "Polygon"
    assert data["measurements"][0]["measurement"] > 0

def test_get_file():
    file_path = (
        Path(__file__).resolve().parents[1]
        / "sample_data"
        / "test_polygon.kml"
    )

    with file_path.open("rb") as file:
        upload_response = client.post(
            "/api/files/",
            files={
                "file": (
                    "test_polygon.kml",
                    file,
                    "application/vnd.google-earth.kml+xml",
                )
            },
        )

    assert upload_response.status_code == 200

    file_id = upload_response.json()["id"]

    response = client.get(
        f"/api/files/{file_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == file_id
    assert data["filename"] == "test_polygon.kml"
    assert data["feature_count"] == 1
    assert data["status"] == "COMPLETED"

def test_reject_unsupported_file_type():
    response = client.post(
        "/api/files/",
        files={
            "file": (
                "test.txt",
                b"This is not a supported geospatial file.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert "Unsupported file type" in data["detail"]

def test_invalid_zip():
    response = client.post(
        "/api/files/",
        files={
            "file": (
                "invalid.zip",
                b"This is not a real ZIP file.",
                "application/zip",
            )
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Uploaded ZIP file is invalid."

def test_get_missing_file():
    response = client.get(
        "/api/files/does-not-exist"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "File not found."

def test_point_has_no_measurement():
    file_path = (
        Path(__file__).resolve().parents[1]
        / "sample_data"
        / "test_point.zip"
    )

    with file_path.open("rb") as file:
        response = client.post(
            "/api/files/",
            files={
                "file": (
                    "test_point.zip",
                    file,
                    "application/zip",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["feature_count"] == 1
    assert data["features"][0]["geometry_type"] == "Point"

    measurement = data["measurements"][0]

    assert measurement["measurement"] is None
    assert measurement["unit"] is None
    assert measurement["message"] == "No measurement required for Point."