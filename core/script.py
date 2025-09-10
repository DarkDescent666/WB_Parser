import json
import requests
import csv


class Page_Source:
    counter = 0

    def __init__(self, url):
        """Инициализация URL, количества обрабатываемых страниц и запроса к API"""
        self.__url = url
        self.__resp = requests.get(self.__url)

    async def data_js(self, min_price=0, max_price=1000000000000000, rt=1):
        """Получение необходимых данных с API, фильтрация и заполнение их в список словарей"""

        products_raw = self.__resp.json()
        products = products_raw.get("products")
        products_list = []
        brands_list = []

        try:
            if len(products) != 0:
                for product in products:
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
                # print(brands_list)
                await self.write_brand(brands_list)

        except:
            Exception(TypeError)
        return products_list

    async def price_method(self, sizes):
        # '''Методо получения отфильтрованной цены, вызывается в data_js'''
        for price in sizes:
            return float(price.get("price").get("product"))/100

    @classmethod
    async def write_method_csv(cls, items, data_path):
        """Метод класса для записи данных в формат CSV"""
        fieldnames = ["Id", "Брэнд", "Название", "Поставщик", "Цена", "Рейтинг"]

        with open(data_path, "a", newline='', encoding="UTF-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
            if cls.counter == 0:
                writer.writeheader()
                cls.counter += 1

            writer.writerows(items)

    async def write_method_json(self, items, data_path):
        # '''Метод записи в формат JSON'''

        try:
            with open(data_path, "r", encoding="UTF-8") as file_load:
                data = json.load(file_load)
        except:
            data = []

        for item in items:
            data.append(item)

        with open(data_path, "w", encoding="UTF-8") as file_load:
            json.dump(data, file_load, ensure_ascii=False, indent=4)

    async def write_brand(self, brands):
        # '''Метод записи в формат JSON'''

        try:
            with open("brands.json", "r", encoding="UTF-8") as file_load:
                data = json.load(file_load)
        except:
            data = []

        for brand in brands:
            if brand not in data:
                data.append(brand)
            else:
                continue

        with open("brands.json", "w", encoding="UTF-8") as file_load:
            json.dump(data, file_load, ensure_ascii=False, indent=4)











