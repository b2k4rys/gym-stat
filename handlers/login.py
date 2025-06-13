
from aiogram import Router, F, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from urllib.parse import urlencode, urlunparse,  urlparse, ParseResult
import uuid
from config import GOOGLE_CLIENT_ID, OAUTH_REDIRECT_URL
router = Router()


@router.message(Command('login'))
async def login_user(message: Message):
    chat_id = str(message.chat.id)
    state = str(uuid.uuid4())
    base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    query_params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': OAUTH_REDIRECT_URL,
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.events',
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
