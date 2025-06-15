
from aiogram import Router, F, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from urllib.parse import urlencode, urlunparse,  urlparse, ParseResult
import uuid
from app.core.redis.redis_client import r
import json
from app.core.configs.config import GOOGLE_CLIENT_ID, OAUTH_REDIRECT_URL
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from pydantic import BaseModel, HttpUrl, field_validator
import re
from app.core.db.session import get_db
from app.core.db.models.sheets import Sheets
from app.core.db.models.user import User as UserModel
from sqlalchemy import select
router = Router()



@router.message(Command('login'))
async def login_user(message: Message):



    state = str(uuid.uuid4())
    chat_id = str(message.chat.id)

    user = message.from_user
    data = {"username": str(user.username), "telegram_id": int(user.id)}
    json_data = json.dumps(data)
    r.setex(f"user:{state}", 600, json_data)
    r.setex(f"oauth:{state}", 600, chat_id)

    base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    query_params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': OAUTH_REDIRECT_URL,
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/spreadsheets.readonly',
        'state': state,
        'access_type': 'offline',
    }

    parsed = urlparse(base_url)
    auth_url = ParseResult(
        scheme=parsed.scheme,
        netloc=parsed.netloc,
        path=parsed.path,
        params='',
        query=urlencode(query_params, doseq=True),
        fragment=''
    ).geturl()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Login with Google", url=f"{auth_url}")
    )

    await message.reply('Please authenticate with Google to use this bot:', reply_markup=builder.as_markup())


class SheetsUrl(BaseModel):
    url: HttpUrl
    
    @field_validator("url")
    @classmethod
    def check_sheets(cls, value: HttpUrl) -> HttpUrl:
        parsed = urlparse(str(value))
        if parsed.hostname != "docs.google.com":
            raise ValueError("must be google url")
        
        if not re.match(r"^/spreadsheets/d/[^/]+", parsed.path):
            raise ValueError("URL must be a Google Sheets document link")

        return value
class SheeetsForm(StatesGroup):
    waiting_for_message = State()

@router.message(Command("sheets"))
async def link_sheets(message: Message, state: FSMContext):
    await message.answer("Provide the sheets link")
    await state.set_state(SheeetsForm.waiting_for_message)


@router.message(SheeetsForm.waiting_for_message)
async def handle_link(message: Message, state: FSMContext):
    try:
        url = SheetsUrl(url=str(message.text))
        parsed = urlparse(str(url.url))
        match = re.search(r"/spreadsheets/d/([^/]+)", parsed.path)
        if not match:
            raise ValueError("Could not extract sheet ID")

        sheets_id = match.group(1)

        async for session in get_db():
            user = message.from_user
            if (await session.execute(select(UserModel).filter_by(telegram_id=int(user.id)))).scalar_one_or_none() is None:
                await message.answer("User not found in the database.")
                return

            sheets_db = Sheets(telegram_id=int(user.id), sheets_id=int(sheets_id))
            session.add(sheets_db)
            await session.commit()
            await session.refresh(sheets_db)

        await message.answer("Successfully linked sheets")
        await state.clear()

    except Exception as e:
        await message.answer("Invalid Google Sheets link. Please try again.")

