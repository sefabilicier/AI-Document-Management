import os
from dotenv import load_dotenv

load_dotenv()

# For SQLite (easier setup)
DATABASE_URL = "sqlite:///./docslim.db"

UPLOAD_DIR = "uploads"
OPTIMIZED_DIR = os.path.join(UPLOAD_DIR, "optimized")
THUMBNAIL_DIR = os.path.join(UPLOAD_DIR, "thumbnails")