import os
import pytest
from unittest.mock import patch, MagicMock
from googleapiclient.errors import HttpError
from upload_to_drive import upload_file

@pytest.fixture
def mock_file(tmp_path):
    """Creates a temporary file for testing."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Hello, this is a test file.")
    return str(file_path)


@patch("upload_to_drive.google.auth.default")
@patch("upload_to_drive.build")
@patch("upload_to_drive.MediaFileUpload")
def test_upload_file_success(mock_media_file_upload, mock_build, mock_auth_default, mock_file):
    """Tests a successful file upload."""
    # Setup mocks
    mock_creds = MagicMock()
    mock_auth_default.return_value = (mock_creds, "test-project")

    mock_service = MagicMock()
    mock_build.return_value = mock_service

    mock_files = MagicMock()
    mock_service.files.return_value = mock_files

    mock_create = MagicMock()
    mock_files.create.return_value = mock_create

    expected_file_id = "test-file-id-123"
    mock_create.execute.return_value = {"id": expected_file_id}

    # Call the function
    result = upload_file(mock_file, "custom_name.txt")

    # Assertions
    assert result == expected_file_id
    mock_auth_default.assert_called_once()
    mock_build.assert_called_once_with("drive", "v3", credentials=mock_creds)
    mock_media_file_upload.assert_called_once_with(mock_file, mimetype="text/plain", resumable=True)
    mock_files.create.assert_called_once_with(
        body={"name": "custom_name.txt"},
        media_body=mock_media_file_upload.return_value,
        fields="id"
    )

@patch("upload_to_drive.google.auth.default")
@patch("upload_to_drive.build")
def test_upload_file_not_found(mock_build, mock_auth_default):
    """Tests when the local file does not exist."""
    result = upload_file("nonexistent_file.txt")

    assert result is None
    mock_auth_default.assert_not_called()
    mock_build.assert_not_called()

@patch("upload_to_drive.google.auth.default")
@patch("upload_to_drive.build")
@patch("upload_to_drive.MediaFileUpload")
def test_upload_file_http_error(mock_media_file_upload, mock_build, mock_auth_default, mock_file):
    """Tests handling of an HttpError during upload."""
    # Setup mocks
    mock_creds = MagicMock()
    mock_auth_default.return_value = (mock_creds, "test-project")

    mock_service = MagicMock()
    mock_build.return_value = mock_service

    mock_files = MagicMock()
    mock_service.files.return_value = mock_files

    mock_create = MagicMock()
    mock_files.create.return_value = mock_create

    # Mock an HttpError
    mock_resp = MagicMock()
    mock_resp.status = 500
    mock_create.execute.side_effect = HttpError(resp=mock_resp, content=b"Internal Server Error")

    # Call the function
    result = upload_file(mock_file)

    # Assertions
    assert result is None
    mock_auth_default.assert_called_once()

@patch("upload_to_drive.google.auth.default")
@patch("upload_to_drive.build")
@patch("upload_to_drive.MediaFileUpload")
def test_upload_file_default_name_and_mime(mock_media_file_upload, mock_build, mock_auth_default, tmp_path):
    """Tests upload with default name (no drive_filename) and unknown mime type."""
    # Setup mocks
    mock_creds = MagicMock()
    mock_auth_default.return_value = (mock_creds, "test-project")

    mock_service = MagicMock()
    mock_build.return_value = mock_service

    mock_files = MagicMock()
    mock_service.files.return_value = mock_files

    mock_create = MagicMock()
    mock_files.create.return_value = mock_create

    expected_file_id = "test-file-id-456"
    mock_create.execute.return_value = {"id": expected_file_id}

    # Create a file with no extension to trigger fallback mime type
    file_path = tmp_path / "unknown_file"
    file_path.write_bytes(b"some binary data")

    # Call the function
    result = upload_file(str(file_path))

    # Assertions
    assert result == expected_file_id
    mock_media_file_upload.assert_called_once_with(str(file_path), mimetype="application/octet-stream", resumable=True)
    mock_files.create.assert_called_once_with(
        body={"name": "unknown_file"},
        media_body=mock_media_file_upload.return_value,
        fields="id"
    )
