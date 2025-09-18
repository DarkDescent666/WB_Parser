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
    await state.set_state(Salesman_get_state.salesman_get_type_of_file_in_name)
    await message.answer('Выберите тип файла используя кнопки',reply_markup= type_of_file_kb)

@rt.message(Salesman_get_state.salesman_get_type_of_file_in_name)
async def seller_get_type_of_file(message: Message,state: FSMContext):
    if message.text not in ['JSON','CSV']:
        await message.answer('Пожалуйста, используй кнопки')
        return seller_get_type_of_file

    await state.update_data(salesman_type_of_file = message.text)

    await state.update_data(user_name = message.from_user.username)
    await message.answer(f'ID продавца получено: {message.text}')

    remove_keyboard = ReplyKeyboardRemove()

    data = await state.get_data()
    await state.clear()
    pages = ParsPages()
    await pages.set_data_by_seller(data)

    get_data_items_by_seller = await (pages.processing_by_name())

    document = FSInputFile(get_data_items_by_seller, filename=get_data_items_by_seller)
    await message.answer_document(document=document, caption="Работает!!")


