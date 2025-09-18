
from datetime import datetime
import asyncio
from core.user_data import UserDataByItem,UserDataBySeller
from core.script_async import Page_Source
class Error(Exception):
    pass


class ParsPages:
    def __init__(self):
        UserDataByItem.dt = str(datetime.now().strftime("%d_%m_%y__%H_%M_%S"))

    async def set_data_by_item(self,data):
        UserDataByItem.item = data['request_from_user']
        UserDataByItem.min_price = data['min_price']
        UserDataByItem.max_price = data['max_price']
        UserDataByItem.count_page = data['count_page']
        UserDataByItem.file_writer = data['type_of_file']
        UserDataByItem.user_name = data['user_name']
        UserDataByItem.rating = data['rating']
        if UserDataByItem.file_writer == "CSV":
            UserDataByItem.path = f"products_csv//products_{UserDataByItem.user_name}_{UserDataByItem.dt}.csv"
        else:
            UserDataByItem.path = f"products_json//products_{UserDataByItem.user_name}_{UserDataByItem.dt}.json"
    async def set_data_by_seller(self,data):
        UserDataBySeller.brand_id = data["salesman_name"]
        UserDataByItem.user_name = data['user_name']

        if UserDataByItem.file_writer == "CSV":
            UserDataByItem.path = f"products_csv//products_{UserDataByItem.user_name}_{UserDataByItem.dt}.csv"
        else:
            UserDataByItem.path = f"products_json//products_{UserDataByItem.user_name}_{UserDataByItem.dt}.json"

    #Парсинг по названию товаров
    async def processing_by_name(self):
            start = datetime.now()
            async_script = Page_Source()
            #Передаем параметры из UserData в скрипт формирования задач gather_data из файла script_async
            task = asyncio.create_task(async_script.gather_data(
                    min_price=UserDataByItem.min_price, max_price=UserDataByItem.max_price, rt=UserDataByItem.rating, seller_id=UserDataBySeller.brand_id),
                                           )
            if await task == None:
                print(f"Время работы программы {datetime.now() - start}")
                UserDataByItem.item = ""
                UserDataByItem.min_price = 0
                UserDataByItem.max_price = 10000000000
                UserDataByItem.count_page = 0
                UserDataByItem.file_writer = "CSV"
                UserDataByItem.user_name = ""
                UserDataByItem.rating = 0
                UserDataBySeller.brand_id = 0
                return UserDataByItem.path







