import os
import shutil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Vercel's filesystem is read-only except /tmp, so the SQLite DB and uploads
# must live there. (Data in /tmp is temporary -- use a hosted DB via
# DATABASE_URL for anything permanent.)
IS_VERCEL = bool(os.environ.get("VERCEL"))

if IS_VERCEL:
    _DB_PATH = "/tmp/vithaigal.db"
    _BUNDLED_DB = os.path.join(BASE_DIR, "instance", "vithaigal.db")
    if not os.path.exists(_DB_PATH) and os.path.exists(_BUNDLED_DB):
        shutil.copy(_BUNDLED_DB, _DB_PATH)
    _UPLOADS = "/tmp/uploads"
else:
    _DB_PATH = os.path.join(BASE_DIR, "instance", "vithaigal.db")
    _UPLOADS = os.path.join(BASE_DIR, "static", "images", "uploads")


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "vithaigal-iyakkam-super-secret-key-2026-prod-jwt-session"
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{_DB_PATH}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload configuration
    UPLOAD_FOLDER = _UPLOADS
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = ("png", "jpg", "jpeg", "webp", "gif")

    # Pagination
    ITEMS_PER_PAGE = 9
    ADMIN_ITEMS_PER_PAGE = 15