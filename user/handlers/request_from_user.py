
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, FSInputFile
from aiogram import F
from concurrent.futures import ThreadPoolExecutor
from core.utils import ParsPages
from KeyBoards.ReplyKeyboards.type_of_file_kb import type_of_file_kb
from states.request_from_user_states import Request_from_user_state
from KeyBoards.InlineKeyboard.menu_user_kb import rating_kb
from core.user_data import UserData

rt = Router()


@rt.callback_query(F.data == 'request_from_user')           #Получаем callback от inlineKeyboard из menu_user_kb в главном меню и начинаем сбор данных от пользователя используя машину состояний
async def request_callback_query(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Введите запрос на который хотите получить информацию о товарах')
    await state.set_state(Request_from_user_state.waiting_user_request)

@rt.message(Request_from_user_state.waiting_user_request)
async def request_user(message: Message, state: FSMContext):

    request_from_user = message.text
    await state.update_data(request_from_user = request_from_user)

    await message.answer('Введите минимальную цену подбора')
    await state.set_state(Request_from_user_state.waiting_price_min)

@rt.message(Request_from_user_state.waiting_price_min)                                      #Получаем минимальную цену
async def request_user_min_price(message: Message, state: FSMContext):

    min_price = message.text
    await state.update_data(min_price=int(min_price))

    await message.answer('Введите максимальную цену подбора')
    await state.set_state(Request_from_user_state.waiting_price_max)

@rt.message(Request_from_user_state.waiting_price_max)                                      #Получаем максимальную цену
async def request_user_max_price(message: Message, state: FSMContext):

    max_price = message.text
    await state.update_data(max_price=int(max_price))

    await message.answer('Введите колличество страниц для обработки')
    await state.set_state(Request_from_user_state.waiting_count_page)

@rt.message(Request_from_user_state.waiting_count_page)
async def request_user_count_page(message: Message, state: FSMContext):

    count_page = message.text
    await state.update_data(count_page=int(count_page))

    await message.answer('Выберите интересующий рейтинг товара', reply_markup= rating_kb)
    await state.set_state(Request_from_user_state.waiting_rating)

@rt.callback_query(F.data == 'rating_assessment_1')                                    #Получение рейтинга от пользователя
async def request_user_rating(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await state.update_data(rating=1)

    await callback.message.answer('Выберите тип файла', reply_markup=type_of_file_kb)
    await state.set_state(Request_from_user_state.waiting_type_file)

@rt.callback_query(F.data == 'rating_assessment_2')                                     #Получение рейтинга от пользователя
async def request_user_rating(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await state.update_data(rating=2)

    await callback.message.answer('Выберите тип файла', reply_markup=type_of_file_kb)
    await state.set_state(Request_from_user_state.waiting_type_file)

@rt.callback_query(F.data == 'rating_assessment_3')                                     #Получение рейтинга от пользователя
async def request_user_rating(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await state.update_data(rating=3)

    await callback.message.answer('Выберите тип файла', reply_markup=type_of_file_kb)
    await state.set_state(Request_from_user_state.waiting_type_file)

@rt.callback_query(F.data == 'rating_assessment_4')                                     #Получение рейтинга от пользователя
async def request_user_rating(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await state.update_data(rating=4)

    await callback.message.answer('Выберите тип файла', reply_markup=type_of_file_kb)
    await state.set_state(Request_from_user_state.waiting_type_file)

@rt.callback_query(F.data == 'rating_assessment_5')                                     #Получение рейтинга от пользователя
async def request_user_rating(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await state.update_data(rating=5)

    await callback.message.answer('Выберите тип файла', reply_markup=type_of_file_kb)
    await state.set_state(Request_from_user_state.waiting_type_file)

@rt.message(Request_from_user_state.waiting_type_file)
async def request_user_type_of_file(message: Message, state: FSMContext):       #Собираем все полученные данные от пользователя

    type_of_file = message.text

    await state.update_data(type_of_file=type_of_file,
                            user_name = message.from_user.username)                          # Получаем желаемый пользователем тип файла
    # print(message.from_user.username)
    remove_keyboard = ReplyKeyboardRemove()
    data = await state.get_data()
    await message.answer(f'Все необходимые данные получены\n\n'
                         f'Ваш запрос: {data['request_from_user']}\n'
                         f'Минимальная цена: {data['min_price']}\n'
                         f'Максимальная цена: {data['max_price']}\n'
                         f'Количество страниц для обработки: {data['count_page']}\n'
                         f'Рейтинг: {data['rating']}\n'
                         f'Тип получаемого файла: {data['type_of_file']}',reply_markup=remove_keyboard)
    await state.clear()

    pages = ParsPages(data)
    get_data_items_by_name = await (pages.processing_by_name())
    document = FSInputFile(get_data_items_by_name, filename=get_data_items_by_name)
    await message.answer_document(document=document, caption="Работает!!")




