from aiogram.filters.state import StatesGroup,State

class Salesman_get_state(StatesGroup,State):
    salesman_get_name = State()
    salesman_get_url = State()
    salesman_get_type_of_file_in_name = State()
    salesman_get_type_of_file_in_url = State()