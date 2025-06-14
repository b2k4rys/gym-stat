import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from app.core.configs.config import BOT_TOKEN
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers import echo, start, login

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def main():

    dp = Dispatcher()
    dp.include_routers(login.router, start.router, echo.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
