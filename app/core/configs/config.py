from dotenv import load_dotenv
import os

# Load token from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
OAUTH_REDIRECT_URL = os.getenv("OAUTH_REDIRECT_URL")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DATABASE_URL=os.getenv("DATABASE_URL")