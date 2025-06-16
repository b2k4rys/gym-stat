
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

    results = dict()



    

    values_list = last_worksheet.col_values(1)


    for i in range(1, len(values_list)):
        print(f"{i} COLUMN is {values_list[i]}")

        if not values_list[i]:
            continue

        results[values_list[i]] = list()
        row = last_worksheet.row_values(i+1)
        print(f"{i+1} ROW IS {row}")

        if not row:
            continue

        for j in range(1, len(row)):
            results[values_list[i]].append(row[j])
    
    for exercise, sets in results.items():
        if not sets:
            continue  

        total_volume = 0
        for set_str in sets:
            set_str = set_str.strip()

            if '-' not in set_str:
                continue  

            try:
      
                weight_part, reps_part = map(str.strip, set_str.split('-', 1))

                weight = float(''.join(c for c in weight_part if c.isdigit() or c == '.'))
                reps = int(''.join(c for c in reps_part if c.isdigit()))

                total_volume += weight * reps
            except Exception as e:
                print(f"Error parsing set '{set_str}': {e}")
            continue

    print(f"{exercise.strip()}: {total_volume:.1f} volume")



    await message.answer(last_worksheet.title)
    

