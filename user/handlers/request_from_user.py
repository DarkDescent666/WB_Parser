from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, FSInputFile
from aiogram import F

from core.utils import ParsPages
from core.user_data import UserData
from KeyBoards.ReplyKeyboards.type_of_file_kb import type_of_file_kb
from states.request_from_user_states import Request_from_user_state
from KeyBoards.InlineKeyboard.menu_user_kb import rating_kb

from core.utils import Error



from validators.valid_for_request_from_user import valid_max_price, valid_count_page, valid_min_price


rt = Router()


@rt.callback_query(F.data == 'request_from_user')
async def request_callback_query(callback: CallbackQuery, state: FSMContext):
    '''#Получаем callback от inlineKeyboard из menu_user_kb в главном меню и начинаем сбор данных от пользователя используя машину состояний'''
    await callback.message.delete()
    await callback.message.answer('Введите запрос на который хотите получить информацию о товарах')
    await state.set_state(Request_from_user_state.waiting_user_request)

@rt.message(Request_from_user_state.waiting_user_request)
async def request_user(message: Message, state: FSMContext):
    '''#Получаем минимальную цену '''

    await state.update_data(request_from_user = message.text)

    await message.answer('Введите минимальную цену подбора')
    await state.set_state(Request_from_user_state.waiting_price_min)

@rt.message(Request_from_user_state.waiting_price_min)
async def request_user_min_price(message: Message, state: FSMContext):
    '''#Получаем максимальную цену для фильтра подбора товаров'''


    if await valid_min_price(message,state) is False:
        return request_user_min_price



    await message.answer('Введите максимальную цену подбора')
    await state.set_state(Request_from_user_state.waiting_price_max)

@rt.message(Request_from_user_state.waiting_price_max)
async def request_user_max_price(message: Message, state: FSMContext):

    '''Получаем максимальную цену подбора товара'''

    if await valid_max_price(message,state) is False:
        return request_user_max_price

    '''Получаем колличество страниц для обработки ботом'''
    await message.answer('Введите колличество страниц для обработки')

    await state.set_state(Request_from_user_state.waiting_count_page)

@rt.message(Request_from_user_state.waiting_count_page)
async def request_user_count_page(message: Message, state: FSMContext):
    '''#Получение минимального рейтинга товаров от пользователя'''

    if await valid_count_page(message,state) is False:
        return request_user_count_page


    await message.answer('Выберите интересующий рейтинг товара', reply_markup=rating_kb)
    await state.set_state(Request_from_user_state.waiting_rating)


@rt.callback_query(F.data == 'rating_assessment_1')
async def request_user_rating(callback: CallbackQuery, state: FSMContext):
    '''#Получение рейтинга от пользователя от 1 до 5'''

    await callback.message.delete()
    await state.update_data(rating=1)

    await callback.message.answer('Выберите тип файла', reply_markup=type_of_file_kb)
    await state.set_state(Request_from_user_state.waiting_type_file)

@rt.callback_query(F.data == 'rating_assessment_2')
async def request_user_rating(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await state.update_data(rating=2)

    await callback.message.answer('Выберите тип файла', reply_markup=type_of_file_kb)
    await state.set_state(Request_from_user_state.waiting_type_file)

@rt.callback_query(F.data == 'rating_assessment_3')
async def request_user_rating(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await state.update_data(rating=3)

    await callback.message.answer('Выберите тип файла', reply_markup=type_of_file_kb)
    await state.set_state(Request_from_user_state.waiting_type_file)

@rt.callback_query(F.data == 'rating_assessment_4')
async def request_user_rating(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await state.update_data(rating=4)

    await callback.message.answer('Выберите тип файла', reply_markup=type_of_file_kb)
    await state.set_state(Request_from_user_state.waiting_type_file)

@rt.callback_query(F.data == 'rating_assessment_5')
async def request_user_rating(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await state.update_data(rating=5)

    await callback.message.answer('Выберите тип файла', reply_markup=type_of_file_kb)
    await state.set_state(Request_from_user_state.waiting_type_file)

@rt.message(Request_from_user_state.waiting_type_file)
async def request_user_type_of_file(message: Message, state: FSMContext):
    '''Собираем все полученные данные от пользователя'''
    ''' Получаем желаемый пользователем тип файла'''


    if message.text != ('JSON' or 'CSV'):
        await message.answer('Пожалуйста, используй кнопки')
        return request_user_type_of_file

    await state.update_data(type_of_file=message.text,
                            user_name = message.from_user.username)


    remove_keyboard = ReplyKeyboardRemove()

    data = await state.get_data()



    await message.answer(f'Все необходимые данные получены\n\n'
                         f'Ваш запрос: {data['request_from_user']}\n'
                         f'Минимальная цена: {data['min_price']}\n'
                         f'Максимальная цена: {data['max_price']}\n'
                         f'Количество страниц для обработки: {data['count_page']}\n'
                         f'Рейтинг: {data['rating']}\n'
                         f'Тип получаемого файла: {data['type_of_file']},',reply_markup=remove_keyboard)
    await state.clear()
    #Записываем данные от пользователя в переменные класса UserData
    UserData.dt = str(datetime.now().strftime("%d_%m_%y__%H_%M_%S"))
    UserData.item = data['request_from_user']
    UserData.min_price = data['min_price']
    UserData.max_price = data['max_price']
    UserData.count_page = data['count_page']
    UserData.file_writer = data['type_of_file']
    UserData.user_name = data['user_name']
    UserData.rating = data['rating']
    if UserData.file_writer == "CSV":
        UserData.path = f"products_csv//products_{UserData.user_name}_{UserData.dt}.csv"
    else:
        UserData.path = f"products_json//products_{UserData.user_name}_{UserData.dt}.json"


    pages = ParsPages()
    #
    get_data_items_by_name = await (pages.processing_by_name())
    document = FSInputFile(get_data_items_by_name, filename=get_data_items_by_name)
    await message.answer_document(document=document, caption="Работает!!")




