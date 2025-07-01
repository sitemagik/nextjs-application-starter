import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-bdsm-candles")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/bdsm_candles")
    PORT = 9000
    UPLOAD_FOLDER = "static/uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
