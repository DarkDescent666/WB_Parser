
class UserDataByItem:
    dt: str
    item: str
    min_price: int = 0
    max_price: int = 1000000000000
    count_page: int = 1000
    rating: int = 0
    file_writer: str = "CSV"
    path: str
    user_name: str = 'Oleg'


class UserDataBySeller(UserDataByItem):
    brand_id: int = 0





