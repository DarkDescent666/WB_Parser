from datetime import datetime
import asyncio
from core.user_data import UserData
from core import script
from core.script_async import Page_Source
class Error(Exception):
    pass


class ParsPages(UserData):
    async def processing_by_name(self,data):
            start = datetime.now()
            async_script = Page_Source(data)

            task = asyncio.create_task(async_script.gather_data(
                    min_price=self.min_price, max_price=self.max_price, rt=self.rating),
                                           name=self.user_name)
            if await task == None:
                print(f"Время работы программы {datetime.now() - start}")
                return self.path








