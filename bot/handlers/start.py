from aiogram import Router, F, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import FSInputFile

router = Router()

@router.message(CommandStart())
async def start_message(message: Message):
    mail = "bekarys@carbon-scene-462517-h0.iam.gserviceaccount.com"
    image = FSInputFile("bot/media/instructions.png")  


    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}! To use this bot you need to share your google spreadsheet with this mail {mail} and login using /login command"
    )
    await message.answer_photo(image)



