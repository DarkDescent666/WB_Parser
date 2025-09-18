from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Спарсить запрос',callback_data='request_from_user')],
        [InlineKeyboardButton(text='Спарсить продавца', callback_data='salesman')],
        [InlineKeyboardButton(text='Спарсить что-то еще', callback_data='  .!.  ')]
    ]
)

rating_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='0',callback_data='rating_assessment_0')],
        [InlineKeyboardButton(text='1',callback_data='rating_assessment_1')],
        [InlineKeyboardButton(text='2',callback_data='rating_assessment_2')],
        [InlineKeyboardButton(text='3',callback_data='rating_assessment_3')],
        [InlineKeyboardButton(text='4',callback_data='rating_assessment_4')],
        [InlineKeyboardButton(text='5',callback_data='rating_assessment_5')]
    ]


)
salesman_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Имя продавца', callback_data='salesman_name')],

    ]
)