import os
from dotenv import load_dotenv

load_dotenv()

DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
DROPBOX_ROOT_FOLDER = "Master Trims"

if not DROPBOX_ACCESS_TOKEN:
    raise RuntimeError("DROPBOX_ACCESS_TOKEN is not set")

if not ADMIN_PASSWORD:
    raise RuntimeError("ADMIN_PASSWORD is not set")