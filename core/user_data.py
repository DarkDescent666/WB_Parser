
class UserDataByItem:
    item: str
    min_price: int = 0
    max_price: int = 1000000000000
    count_page: int = 1000
    rating: int = 0
    file_writer: str = "CSV"
    path: str
    user_name: str
    brand_id: int = 0


class UserDataBySeller:
    brand_id: int = 0
    file_writer: str
    user_name: str
    path: str




