import csv
import json
class Writers:
    counter = 0
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

    async def write_sellers(self, brands):
        # '''Метод записи в формат JSON'''

        try:
            with open("sellers.json", "r", encoding="UTF-8") as file_load:
                data = json.load(file_load)
        except:
            data = []

        for brand in brands:
            if brand not in data:
                data.append(brand)
            else:
                continue

        with open("sellers.json", "w", encoding="UTF-8") as file_load:
            json.dump(data, file_load, ensure_ascii=False, indent=4)