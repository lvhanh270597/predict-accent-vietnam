from models.separate_data.separator import Separator
from system.loader.loader import Loader
from models.vectorgen.vectorgenerator import VectorGenerator

class Main:
    def __init__(self):
        self.separator = Separator()
        self.separator.ratio = {
            "train" : 0.7,
            "test"  : 0.3
        }
        self.loader = Loader()
        db_data = self.loader.db.find("raw", {}, {"_id" : 0, "text" : 1})
        X, y = [], []
        for item in db_data:
            X.append(item["text"])
            y.append(1)
        
        self.separator.set_data(X, y)
        results = self.separator.run()
        print(results)

Main()