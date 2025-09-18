import asyncio
import json
from core.writers import Writers
import aiohttp
from core.user_data import UserData


class Page_Source(UserData, Writers):

    async def get_page_data(self, products, min_price=0, max_price=1000000000000000, rt=1):
        try:
            tasks_write = []
            products_list = []
            brands_list = []
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
                        brands_list.append({
                            "SupplierID": product.get("supplierId"),
                            "Поставщик": product.get("supplier")
                        })
            tasks_write.append(self.write_brand(brands_list))
            #await self.write_brand(brands_list)
            if UserData.file_writer == "JSON":
                tasks_write.append(self.write_method_json(products_list, data_path=UserData.path))#await self.write_method_json(products_list, data_path=self.path)
            else:
                tasks_write.append(self.write_method_csv(products_list, data_path=UserData.path))#await self.write_method_csv(products_list, data_path=self.path)
            await asyncio.gather(*tasks_write)
        except:
            Exception(TypeError)

    async def gather_data(self, min_price=0, max_price=1000000000000000, rt=0):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for page in range(1, UserData.count_page+1):

                print(f"[+] Обработка страницы {page}")
                self.__url = f"https://search.wb.ru/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-5551776&inheritFilters=false&lang=ru&page={page}&query={self.item}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
                response = await session.get(self.__url)
                products_raw = json.loads(await response.text())
                products = products_raw.get("products")
                task = asyncio.create_task(self.get_page_data(products,min_price=min_price,max_price=max_price,rt=rt))

                tasks.append(task)

                if page > 60 or len(products) == 0:
                    break
            await asyncio.gather(*tasks)

    async def price_method(self, sizes):

        for price in sizes:
            return float(price.get("price").get("product"))/100









