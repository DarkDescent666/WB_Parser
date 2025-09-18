import json
from datetime import datetime
import asyncio
from core.user_data import UserData
from core import script
from core.script_async import Page_Source
class Error(Exception):
    pass


class ParsPages(UserData):

    async def set_data(self,data):
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

    #Парсинг по названию товаров
    async def processing_by_name(self):
            start = datetime.now()
            async_script = Page_Source()
            #Передаем параметры из UserData в скрипт формирования задач gather_data из файла script_async
            task = asyncio.create_task(async_script.gather_data(
                    min_price=UserData.min_price, max_price=UserData.max_price, rt=UserData.rating),
                                           )
            if await task == None:
                print(f"Время работы программы {datetime.now() - start}")

                return self.path








