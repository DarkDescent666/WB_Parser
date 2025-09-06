from datetime import datetime

import asyncio

from core import script
import os
import os.path
class Error(Exception):
    pass

async def main(data):

    item = data['request_from_user']
    dt = str(datetime.now().strftime("%d_%m_%y__%H_%M_%S"))
    try:

        min_price = data['min_price']

        max_price = data['max_price']
        count_page = data['count_page']
        rating = int(data['rating'])
        file_writer = data['type_of_file']
        user_name = data['user_name']
        if file_writer == "CSV":
            path = f"products_csv//products_{user_name}_{dt}.csv"
        else:
            path = f"products_json//products_{user_name}_{dt}.json"

        for page in range(1, count_page+1):
            pg = script.Page_Source(item, page=page)
            print(f"[+] Обработка страницы {page}")
            task = asyncio.create_task(pg.data_js(min_price=min_price, max_price=max_price, rt=rating),name=user_name)
            print(await task)
            if await task == []:
                task.cancel()
                return path


            task = await task
            if file_writer == "CSV":
                await pg.write_method_csv(task,data_path=path)
            else:
                await pg.write_method_json(task,user_name,data_path= path)
                print("Страница обработана")
        else:
            return path
    finally:
        pass



async def clear_file(path):
    os.remove(path)



