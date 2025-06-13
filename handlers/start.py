from aiogram import Router, F, html
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.for_che_tam import get_che_tam

router = Router()

@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!, chose your fighter ", reply_markup=get_che_tam()
    )


@router.message(F.text == "Че там")
async def command_che_tam(message: Message) -> None:
    await message.answer("Сет че там 60 штук суши")


@router.message(F.text == "Сет")
async def answer_set(message: Message):
    await message.answer("Хороший выбор чемпион")

    
