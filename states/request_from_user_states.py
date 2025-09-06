from aiogram.filters.state import StatesGroup,State

class Request_from_user_state(StatesGroup):
    waiting_user_request = State()
    waiting_price_min = State()
    waiting_price_max = State()                 #Состояния для машины состояний в request_from_user для сбора данных от пользователя
    waiting_count_page = State()
    waiting_rating = State()
    waiting_type_file = State()
    start_main = State()