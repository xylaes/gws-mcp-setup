import os
import argparse
import mimetypes
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

def upload_file(file_path, drive_filename=None):
    """
    Uploads a file to Google Drive using Application Default Credentials (ADC).
    
    Args:
        file_path (str): Path to the local file to upload.
        drive_filename (str): Optional name to give the file in Google Drive.
                              Defaults to the local file's base name.
    
    Returns:
        str: The uploaded file's ID if successful, otherwise None.
    """
    if not os.path.exists(file_path):
        print(f"Error: Local file '{file_path}' does not exist.")
        return None

    # Get local file details
    local_filename = os.path.basename(file_path)
    if not drive_filename:
        drive_filename = local_filename
        
    # Automatically guess the MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream" # Fallback binary type

    print(f"Uploading '{file_path}' as '{drive_filename}' ({mime_type}) to Google Drive...")

    # Load Application Default Credentials (ADC)
    # Since you ran `gcloud auth application-default login`, this will automatically load your credentials
    creds, _ = google.auth.default()

    try:
        # Build the Drive API service client
        service = build("drive", "v3", credentials=creds)

        # Define file metadata in Drive
        file_metadata = {"name": drive_filename}

        # Define media upload body
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        # Execute the upload request
        file_obj = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        file_id = file_obj.get("id")
        print(f"Success! File uploaded successfully. Drive File ID: {file_id}")
        return file_id

    except HttpError as error:
        print(f"An error occurred while uploading to Google Drive: {error}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a local file to Google Drive.")
    parser.add_argument("file_path", help="Path to the local file to upload.")
    parser.add_argument(
        "--name", 
        help="Optional name to give the file in Google Drive (defaults to local file name)."
    )
    
    args = parser.parse_args()
    upload_file(args.file_path, args.name)
