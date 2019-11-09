from system.loader.loader import Loader
from models.wordgen.wordgenerator import WordGenerator

class Main:
    def __init__(self):
        self.loader = Loader()
        self.wordgen = WordGenerator("word-gen", 5, [])
        db_data = self.loader.db.find("raw", {}, {"_id" : 0, "text" : 1})
        data = []
        for item in db_data:
            data.append(item["text"])
        print(data)
Main()