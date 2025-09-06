from aiogram import  Bot
from dotenv import load_dotenv
import os
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


load_dotenv()

TOKEN: str = f"{os.getenv('TOKEN')}"

bot= Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
