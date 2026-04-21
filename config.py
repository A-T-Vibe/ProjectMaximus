import os
from dotenv import load_dotenv

load_dotenv()

# --- YouTube ---
YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secret.json")

# --- Meta (Instagram + Facebook) ---
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
META_INSTAGRAM_ACCOUNT_ID = os.getenv("META_INSTAGRAM_ACCOUNT_ID", "")

# --- TikTok ---
TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN", "")

# --- Kling AI ---
KLING_API_KEY = os.getenv("KLING_API_KEY", "")
KLING_MONTHLY_CREDIT_LIMIT = 166

# --- Hailuo (MiniMax) ---
HAILUO_API_KEY = os.getenv("HAILUO_API_KEY", "")
HAILUO_GROUP_ID = os.getenv("HAILUO_GROUP_ID", "")
HAILUO_MONTHLY_CREDIT_LIMIT = 100

# --- Pika ---
PIKA_API_KEY = os.getenv("PIKA_API_KEY", "")
PIKA_MONTHLY_CREDIT_LIMIT = 150

# --- Posting schedule (UK time) ---
POST_TIMES = ["08:00", "16:00", "18:00"]
TIMEZONE = "Europe/London"

# --- Video settings ---
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_DURATION_MIN = 15
VIDEO_DURATION_MAX = 30

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
VIDEOS_DIR = os.path.join(DATA_DIR, "videos")
AUDIO_DIR = os.path.join(DATA_DIR, "audio")
DB_PATH = os.path.join(BASE_DIR, "projectmaximus.db")
