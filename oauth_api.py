from fastapi import FastAPI, Request
import requests
from config import GOOGLE_CLIENT_ID, CLIENT_SECRET, OAUTH_REDIRECT_URL, BOT_TOKEN

from bot import bot  
from handlers.login import oauth_sessions
import asyncio


app = FastAPI()

@app.get("/callback")
async def get_state(request: Request):

    code = request.query_params.get("code")
    state = request.query_params.get("state")
    if not code:
        return {"error": "No code received"}


    token_url = "https://oauth2.googleapis.com/token"

    payload = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": OAUTH_REDIRECT_URL,  
        "grant_type": "authorization_code"
    }

    chat_id = oauth_sessions.get(state)
    if not chat_id:
        return {"error": "Unknown state"}
    
    response = requests.post(token_url, data=payload)
    tokens = response.json()



    message = f"✅ Successfully logged in!\nAccess token: {tokens['access_token'][:20]}..."
    asyncio.create_task(bot.send_message(chat_id, message))

    return {"status": "OK", "message": "You can now close this tab."}
    