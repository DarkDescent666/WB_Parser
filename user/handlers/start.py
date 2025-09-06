from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from user.handlers.menu_user import user_menu

rt = Router()

@rt.message(Command('start'))
async def start_cmd(message: Message,state: FSMContext):
    await message.answer('Привет я бот для бизнеса')
    await user_menu(message, state)

