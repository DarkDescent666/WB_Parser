
from datetime import datetime
import asyncio

from aiogram.types import Message

from core.user_data import UserDataByItem,UserDataBySeller
from core.script_async import Page_Source
class Error(Exception):
    pass


class ParsPages:
    def __init__(self):
        self.dt = str(datetime.now().strftime("%d_%m_%y__%H_%M_%S"))

    async def set_data_by_item(self,data):
        UserDataByItem.item = data['request_from_user']
        UserDataByItem.min_price = data['min_price']
        UserDataByItem.max_price = data['max_price']
        UserDataByItem.count_page = data['count_page']
        UserDataByItem.file_writer = data['type_of_file']
        UserDataByItem.user_name = data['user_name']
        UserDataByItem.rating = data['rating']
        if UserDataByItem.file_writer == "CSV":
            UserDataByItem.path = f"products_csv//products_{UserDataByItem.user_name}_{self.dt}.csv"
        else:
            UserDataByItem.path = f"products_json//products_{UserDataByItem.user_name}_{self.dt}.json"

    async def set_data_by_seller(self,data):
        UserDataBySeller.brand_id = data["salesman_name"]
        UserDataBySeller.user_name = data['user_name']
        UserDataBySeller.file_writer = data["salesman_type_of_file"]
        if UserDataBySeller.file_writer == "CSV":
            UserDataBySeller.path = f"products_csv//products_{UserDataBySeller.user_name}_{self.dt}.csv"
        else:
            UserDataBySeller.path = f"products_json//products_{UserDataBySeller.user_name}_{self.dt}.json"

    #Парсинг по названию товаров
    async def processing_by_name(self, message: Message):

            start = datetime.now()
            async_script = Page_Source()
            #Передаем параметры из UserData в скрипт формирования задач gather_data из файла script_async
            task = asyncio.create_task(async_script.gather_data(
                    min_price=UserDataByItem.min_price,
                max_price=UserDataByItem.max_price,
                rt=UserDataByItem.rating,
                path=UserDataByItem.path, message=message),
                                           )
            if await task == None:
                print(f"Время работы программы {datetime.now() - start}")

    async def processing_by_seller(self, message: Message):
        start = datetime.now()
        async_script = Page_Source()
        # Передаем параметры из UserData в скрипт формирования задач gather_data из файла script_async
        task = asyncio.create_task(async_script.gather_data(
            seller_id=UserDataBySeller.brand_id, path=UserDataBySeller.path, message=message),
        )
        if await task == None:
            print(f"Время работы программы {datetime.now() - start}")








