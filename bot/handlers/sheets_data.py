
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.core.redis.redis_client import r
from app.core.db.session import get_db
from app.core.db.models.sheets import Sheets
from sqlalchemy import select
import requests
router = Router()
import httpx
import gspread

gc = gspread.service_account("/Users/b2k4rys/Desktop/gym stat /app/core/configs/service_account.json")



@router.message(Command("get_last_tab_data"))
async def get_last_tab_data(message: Message):
    user = message.from_user
    chat_id = int(message.chat.id)
    
    auth_token = r.get(f"google_token:{chat_id}")

    if not auth_token:
        await message.answer("Not logged in, need auth_token") 
        return
    print(f"HERE IS TOKEN {auth_token}")

    async for session in get_db():
        stmt = select(Sheets).filter_by(telegram_id=int(user.id))
        sheets_obj = (await session.execute(stmt)).scalar_one_or_none()
        if not sheets_obj:
            await message.answer("No linked sheets")
            return
        sheets_id = sheets_obj.sheets_id

    # url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheets_id}"
    # headers = {"Authorization": f"Bearer {auth_token}"}

    # async with httpx.AsyncClient() as client:
    #     response = await client.get(url, headers=headers)
    #     if response.status_code != 200:
    #         await message.answer("Failed to fetch sheet info.")
    #         return
    #     data = response.json()
    #     sheet_titles = [sheet["properties"]["title"] for sheet in data["sheets"]]
    sh = gc.open_by_key(str(sheets_id))
    worksheets = sh.worksheets()
    last_worksheet = worksheets[-1]

    await message.answer(last_worksheet.title)
    

