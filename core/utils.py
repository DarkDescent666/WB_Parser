from datetime import datetime
import asyncio
from core.user_data import UserData
from core import script

class Error(Exception):
    pass


class ParsPages(UserData):
    async def processing_by_name(self):
            start = datetime.now()
            for page in range(1, self.count_page + 1):
                pg = script.Page_Source(
                    url=f"https://search.wb.ru/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-5551776&inheritFilters=false&lang=ru&page={page}&query={self.item}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false")
                print(f"[+] Обработка страницы {page}")
                task = asyncio.create_task(pg.data_js(
                    min_price=self.min_price, max_price=self.max_price, rt=self.rating),
                                           name=self.user_name)
                if await task == []:
                    task.cancel()
                    print(f"Время работы программы {datetime.now() - start}")
                    return self.path

                task = await task
                if self.file_writer == "CSV":
                    await pg.write_method_csv(task, data_path=self.path)
                else:
                    await pg.write_method_json(task, data_path=self.path)
                    print("Страница обработана")
            else:
                print(f"Время работы программы {datetime.now() - start}")
                return self.path





