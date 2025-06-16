from aiogram import Router, F, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import FSInputFile

router = Router()

@router.message(CommandStart())
async def start_message(message: Message):



    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}! To see instructions to this bot use /instructions command"
    )



@router.message(Command("instructions"))
async def instructions(message: Message):
    mail = "bekarys@carbon-scene-462517-h0.iam.gserviceaccount.com"
    image = FSInputFile("bot/media/instructions.png")  

    await message.answer(
        f'''

        1. Login using /login command
        2. Link spreadsheet using /sheets command
        3. Share your spreadsheet with this mail {mail}
        4. Get last workout data using /get_last_workout_data command 

        '''
    )
    await message.answer_photo(image)
