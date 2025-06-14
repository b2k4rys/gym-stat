from fastapi import APIRouter, Request
from app.core.redis.redis_client import r
import requests
from app.core.configs.config import GOOGLE_CLIENT_ID, CLIENT_SECRET, OAUTH_REDIRECT_URL
from bot.bot import bot  
import asyncio
from app.core.db.models.user import User as UserModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from fastapi import Depends
from fastapi.exceptions import HTTPException
import json
router = APIRouter()

@router.get("/callback")
async def get_state(request: Request, session: AsyncSession = Depends(get_db)):

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

    chat_id = r.get(f"oauth:{state}")
    if not chat_id:
        return {"error": "Unknown state"}
    
    raw = r.get(f"user:{state}")
    if raw:
        user_data = json.loads(raw)
    user = (await session.execute(select(UserModel).filter_by(telegram_id=user_data["telegram_id"]))).scalar_one_or_none()
    if user is None:
        user_db = UserModel(username=user_data["username"], telegram_id=user_data["telegram_id"])
        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)
    response = requests.post(token_url, data=payload)
    tokens = response.json()


    r.set(f"google_token:{chat_id}", tokens['access_token'])


    message = f"✅ Successfully logged in!\nAccess token: {tokens['access_token'][:20]}..."
    asyncio.create_task(bot.send_message(chat_id, message))

    return {"status": "OK", "message": "You can now close this tab."}
    