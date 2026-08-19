import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "chefai.db"
ASSETS_DIR = BASE_DIR / "assets" / "images"
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

APP_NAME = "ChefAI"
PRIMARY = "#F97316"
PRIMARY_HOVER = "#EA580C"
SECONDARY = "#2E7D32"
LIGHT_BG = "#F8F5EF"
DARK_BG = "#171717"
CARD_LIGHT = "#FFFFFF"
CARD_DARK = "#222222"
TEXT_LIGHT = "#27272A"
TEXT_DARK = "#F5F5F4"
MUTED_LIGHT = "#71717A"
MUTED_DARK = "#A1A1AA"

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash").strip() or "gemini-3.6-flash"
