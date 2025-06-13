from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_che_tam() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Че там")
    kb.button(text="Сет")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)