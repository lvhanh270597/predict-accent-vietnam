from system.loader.loader import Loader

class Main:
    def __init__(self):
        self.loader = Loader()
        db_data = self.loader.db.find("raw", {}, {"_id" : 0, "text" : 1})
        for item in db_data:
            print(item["text"])

Main()