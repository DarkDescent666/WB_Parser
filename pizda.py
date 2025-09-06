import requests
import re

class Brands:

    def get_brand_name(self):
        st = str(input())
        regex = '(?<=brands/).+'
        brand_name = re.search(regex,st)
        print(brand_name)
        return brand_name[0]

    def get_brand_id(self):
        resp = requests.get(f'https://static-basket-01.wbbasket.ru/vol0/data/brands/{self.get_brand_name()}.json')
        brand_id = resp.json()
        print(brand_id)
        return brand_id['id']

bd = Brands()

bd.get_brand_id()
