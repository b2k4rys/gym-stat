import gspread 
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.core.redis.redis_client import r
from app.core.db.session import get_db
from app.core.db.models.sheets import Sheets
from sqlalchemy import select

router = Router()


gc = gspread.service_account("/Users/b2k4rys/Desktop/gym stat /app/core/configs/service_account.json")

def get_the_results(worksheets, index):

    last_worksheet = worksheets[index]
    results = dict()


    values_list = last_worksheet.col_values(1)


    for i in range(1, len(values_list)):
        if not values_list[i]:
            continue

        results[values_list[i]] = list()
        row = last_worksheet.row_values(i+1)
 
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
        results[exercise] = total_volume
    return results


@router.message(Command("get_last_workout_data"))
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

    
    sh = gc.open_by_key(str(sheets_id))    
    worksheets = sh.worksheets()

    latest_results = get_the_results(worksheets, -1)
    prev_workout = get_the_results(worksheets, -2)


    res = ""

    print(latest_results)

    print(prev_workout)
    res = ""

    for exercise in latest_results:
        if not latest_results[exercise]:
            res += f"{exercise} - has not been performed in the last workout.\n"
            continue
        if not prev_workout[exercise]:
            res += f"{exercise} - has not been performed in the previous workout.\n"
            continue

        try:
            latest_volume = latest_results[exercise]
            prev_volume = prev_workout[exercise]


            if prev_volume == 0:
                res += f"{exercise}: No previous volume to compare.\n"
                continue

            percentage_change = ((latest_volume - prev_volume) / prev_volume) * 100
            direction = "increased" if percentage_change > 0 else "decreased"
            res += f"{exercise} - {direction} by {abs(percentage_change):.1f}%\n"
        except Exception as e:
            res += f"Error comparing {exercise}: {e}\n"



    await message.answer(res)
    

