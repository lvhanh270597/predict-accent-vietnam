from system.loader.loader import Loader
from models.preprocessor.preprocess import Preprocessor

class Main:
    def __init__(self):
        self.loader = Loader()
        db_data = self.loader.db.find("raw", {}, {"_id" : 0, "text" : 1})
        data = []
        for item in db_data:
            data.append(item["text"])
        
        self.preprocessor = Preprocessor()
        self.preprocessor.set_data(data)
        result = self.preprocessor.run()
        print(result)

Main()