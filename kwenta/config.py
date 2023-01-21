import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

BOT_PREFIX = os.environ.get("BOT_PREFIX")

SHEET_ID = os.environ.get("SHEET_ID")

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
