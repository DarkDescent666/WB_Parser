from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from KeyBoards.InlineKeyboard.menu_user_kb import menu_kb

rt = Router()

async def user_menu(message: Message, state: FSMContext):
    await state.clear()
    try:
        await message.answer('Главное меню\nВыберите действие:', reply_markup= menu_kb)
    except:
        pass

@rt.message(F.text == "меню")
async def user_menu_text(message: Message, state: FSMContext):
    await user_menu(message, state)

@rt.message(Command('menu'))
async def user_menu_cmd(message: Message, state: FSMContext):
    await user_menu(message, state)
