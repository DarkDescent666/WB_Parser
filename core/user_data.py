from datetime import datetime


class UserData:
    def __init__(self,data):
        self.dt = str(datetime.now().strftime("%d_%m_%y__%H_%M_%S"))
        self.item = data['request_from_user']
        self.min_price = data['min_price']
        self.max_price = data['max_price']
        self.count_page = data['count_page']
        self.rating = int(data['rating'])
        self.file_writer = data['type_of_file']
        self.user_name = data['user_name']
        if self.file_writer == "CSV":
            self.path = f"products_csv//products_{self.user_name}_{self.dt}.csv"
        else:
            self.path = f"products_json//products_{self.user_name}_{self.dt}.json"
    # def __init__(self):
    #     self.dt = str(datetime.now().strftime("%d_%m_%y__%H_%M_%S"))
    #     self.item = "Самокак"
    #     self.min_price = 11
    #     self.max_price = 98989
    #     self.count_page = 100
    #     self.rating = 1
    #     self.file_writer ="JSON"
    #     self.user_name = "UserName"
    #     if self.file_writer == "CSV":
    #         self.path = f"products_csv//products_{self.user_name}_{self.dt}.csv"
    #     else:
    #         self.path = f"products_json//products_{self.user_name}_{self.dt}.json"