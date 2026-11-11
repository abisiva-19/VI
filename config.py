import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "vithaigal-iyakkam-super-secret-key-2026-prod-jwt-session"
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'vithaigal.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = ("png", "jpg", "jpeg", "webp", "gif")

    # Pagination
    ITEMS_PER_PAGE = 9
    ADMIN_ITEMS_PER_PAGE = 15
