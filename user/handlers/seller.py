from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from KeyBoards.InlineKeyboard.menu_user_kb import salesman_kb
from states.salesman_state import Salesman_get_state

rt = Router()

@rt.callback_query(F.data == 'salesman')
async def seller_callback_query(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Выберите удобный способ поиска продавца',reply_markup=salesman_kb)

@rt.callback_query(F.data == 'salesman_name')
async def seller_callback_get_name(callback: CallbackQuery,state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Введите имя продавца')
    await state.set_state(Salesman_get_state.salesman_get_name)

@rt.message(Salesman_get_state.salesman_get_name)
async def seller_get_name(message: Message,state:FSMContext):
    await state.update_data(salesman_name = message.text)
    await message.answer(f'Имя продавца получено: {message.text}')