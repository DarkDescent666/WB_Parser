from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from KeyBoards.ReplyKeyboards.type_of_file_kb import type_of_file_kb
from states.salesman_state import Salesman_get_state

rt = Router()
@rt.callback_query(F.data == 'salesman_name')
async def seller_callback_get_url(callback: CallbackQuery,state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Введите ссылку на страницу продавца')
    await state.set_state(Salesman_get_state.salesman_get_url)

@rt.message(Salesman_get_state.salesman_get_url)
async def seller_get_url(message:Message,state: FSMContext):
    await state.update_data(seller_url = message.text)
    await message.answer('Ссылка получена')
    await state.set_state(Salesman_get_state.salesman_get_type_of_file_in_url)
    await message.answer('Выберите тип файла используя кнопки',reply_markup= type_of_file_kb)

@rt.message(Salesman_get_state.salesman_get_type_of_file_in_url)
async def seller_get_type_of_file(message: Message,state: FSMContext):
    if message.text not in ['JSON','CSV']:
        await message.answer('Пожалуйста, используй кнопки')
        return seller_get_type_of_file

    await state.update_data(salesman_type_of_file = message.text)
