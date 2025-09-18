from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

type_of_file_kb = ReplyKeyboardMarkup(           #Клавиатура для выбора типа файла
    keyboard=[
        [KeyboardButton(text = 'JSON')],
        [KeyboardButton(text= 'CSV')]
    ],resize_keyboard=True
)
remove_keyboard = ReplyKeyboardRemove()