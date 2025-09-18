import json
from datetime import datetime
import asyncio
from core.user_data import UserData
from core import script
from core.script_async import Page_Source
class Error(Exception):
    pass


class ParsPages(UserData):
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








