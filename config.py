from dotenv import load_dotenv
import os

# Load token from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")