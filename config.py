import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for Flask
    SECRET_KEY = "visitor_management_secret_key"

    # SQLite database location
    DATABASE = os.path.join(BASE_DIR, "visitor_management.db")

    # Folder for uploaded ID proofs
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    # Maximum upload size (5 MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}