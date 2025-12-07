import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

TEMP_DIR = "temp"
INPUT_DIR = f"{TEMP_DIR}/input"
CHUNKS_DIR = f"{TEMP_DIR}/chunks"
