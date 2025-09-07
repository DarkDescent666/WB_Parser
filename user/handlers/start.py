from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from user.handlers.menu_user import user_menu

rt = Router()

@rt.message(Command('start'))
async def start_cmd(message: Message,state: FSMContext):
    remove_keyboard = ReplyKeyboardRemove()
    await message.answer('Привет я бот для бизнеса',reply_markup=remove_keyboard)
    await user_menu(message, state)

