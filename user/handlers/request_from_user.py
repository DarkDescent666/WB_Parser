import asyncio
from datetime import datetime
from time import sleep

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, FSInputFile
from aiogram import F

from core.user_data import UserData
from KeyBoards.ReplyKeyboards.type_of_file_kb import type_of_file_kb
from states.request_from_user_states import Request_from_user_state
from KeyBoards.InlineKeyboard.menu_user_kb import rating_kb
from core.utils import Error, ParsPages

rt = Router()


async def user_rq_vl(data,message: Message, state:FSMContext):

    if data["min_price"] > data["max_price"]:
        remove_keyboard = ReplyKeyboardRemove()
        await message.answer("Неверно введены данные для фильрации:\n"
                       "Минимальная цена должна быть меньше максимальной",reply_markup=remove_keyboard)

        await state.set_state(Request_from_user_state.waiting_price_min)
        return request_user_min_price(message,state)
    else:
        return message.answer('Начинаю обработку данных')


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

    async def validation():
        try:
            if int(message.text) >= 0 :
                await state.update_data(min_price= int(message.text))
            else:
                raise Error("Значение долно быть больше или равно нулю")
        except:
            await message.delete()
            await message.answer('Цена должна быть числом больше нуля,введите значение снова')
            await validation()

    await validation()


    await message.answer('Введите максимальную цену подбора')
    await state.set_state(Request_from_user_state.waiting_price_max)

@rt.message(Request_from_user_state.waiting_price_max)
async def request_user_max_price(message: Message, state: FSMContext):
    '''Получаем колличество страниц для обработки ботом'''

    async def validation():
        try:
            await state.update_data(max_price=int(message.text))
        except:
            await message.delete()
            await message.answer('Цена должна быть числом,введите значение снова')
            await validation()

    await validation()

    await message.answer('Введите количество страниц для обработки')
    await state.set_state(Request_from_user_state.waiting_count_page)

@rt.message(Request_from_user_state.waiting_count_page)
async def request_user_count_page(message: Message, state: FSMContext):
    '''#Получение минимального рейтинга товаров от пользователя'''

    async def validation():
        try:
            await state.update_data(count_page=int(message.text))
        except:
            await message.delete()
            await message.answer('Количество страниц должно быть числом,введите значение снова')
            await validation()

    await validation()

    await message.answer('Выберите интересующий рейтинг товара', reply_markup=rating_kb)
    await state.set_state(Request_from_user_state.waiting_rating)

@rt.callback_query(F.data == 'rating_assessment_0')
async def request_user_rating(callback: CallbackQuery, state: FSMContext):
    '''#Получение рейтинга от пользователя от 1 до 5'''
    await callback.message.delete()
    await state.update_data(rating=0)

    await callback.message.answer('Выберите тип файла', reply_markup=type_of_file_kb)
    await state.set_state(Request_from_user_state.waiting_type_file)
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

    if message.text not in ['JSON','CSV']:
        await message.delete()
        await message.answer('Пожалуйста, используй кнопки')
        return request_user_type_of_file



    await state.update_data(type_of_file=message.text,
                            user_name = message.from_user.username)
    # print(message.from_user.username)
    remove_keyboard = ReplyKeyboardRemove()

    data = await state.get_data()

    validator = await user_rq_vl(data=data,message= message,state =state)
    await validator
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




