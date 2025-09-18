import asyncio
import json
from core.writers import Writers
import aiohttp
from core.user_data import UserDataByItem as UserData
from core.send_file import send


class Page_Source(UserData, Writers):


    #Обработчик страниц
    async def get_page_data(self, products, min_price=0, max_price=1000000000000000, rt=1,path=""):
        try:

            tasks_write = []
            products_list = []
            sellers_list = []
            for product in products:
                if len(product) != 0:
                    price = await self.price_method(product.get("sizes"))
                    rating = int(product.get("rating"))

                    if max_price >= price >= min_price and rating >= rt:
                        products_list.append({
                            "Id": f"https://www.wildberries.ru/catalog/{product.get("id")}/detail.aspx?targetUrl=SP",
                            "Брэнд": product.get("brand"),
                            "Название": product['name'],
                            "Поставщик": product.get("supplier"),
                            "Цена": price,
                            "Рейтинг": rating
                        })
                        sellers_list.append({
                            "SupplierID": product.get("supplierId"),
                            "Поставщик": product.get("supplier")
                        })
            #tasks_write.append(self.write_brand(brands_list))
            await self.write_sellers(sellers_list)
            if UserData.file_writer == "JSON":
                await self.write_method_json(products_list, data_path=self.path)#tasks_write.append(self.write_method_json(products_list, data_path=path))
            else:
                await self.write_method_csv(products_list, data_path=self.path)#tasks_write.append(self.write_method_csv(products_list, data_path=path))
            #await asyncio.gather(*tasks_write)
        except:
            Exception(TypeError)

    #скрипт формирования списка задач из асинхронных HTTP запросов
    async def gather_data(self,message, min_price=0, max_price=1000000000000000, rt=0, seller_id=0,path=""):
        self.path = path

        async with aiohttp.ClientSession() as session:
            tasks = []
            for page in range(1, UserData.count_page+1):

                print(f"[+] Обработка страницы {page}")
                if seller_id == 0:
                    self.__url = f"https://search.wb.ru/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-5551776&inheritFilters=false&lang=ru&page={page}&query={self.item}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"

                else:
                    self.__url = f"https://u-catalog.wb.ru/sellers/v4/catalog?ab_testid=route_score_gaps_3&appType=1&curr=rub&dest=-5551776&lang=ru&page={page}&sort=popular&spp=30&supplier={seller_id}"
                response = await session.get(self.__url)
                products_raw = json.loads(await response.text())
                products = products_raw.get("products")
                task = asyncio.create_task(self.get_page_data(products,min_price=min_price,
                                                              max_price=max_price,rt=rt))

                tasks.append(task)

                if page > 60 or len(products) == 0:
                    break
            await asyncio.gather(*tasks)
            await send(message, path=self.path)

    async def price_method(self, sizes):

        for price in sizes:
            return float(price.get("price").get("product"))/100









