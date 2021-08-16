from aiogram import Bot, Dispatcher, types

from bot.config import settings
from bot.db.base import SessionLocal

bot = Bot(token=settings.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
db = SessionLocal()
