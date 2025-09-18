import json


class Sellers:

     def get_idSeller(self,name_seller):
         with open("/sellers.json", "r", encoding="UTF-8") as brands_js:
            brands = json.load(brands_js)
            for items in brands:
                if name_seller.lower() == items["Поставщик"].lower():
                    return items["SupplierID"]



seller = Sellers().get_idSeller("мЬюзик хамер")
