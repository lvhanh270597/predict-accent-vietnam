from models.separate_data.separator import Separator
from system.loader.loader import Loader
from models.vectorgen.vectorgenerator import VectorGenerator
from models.learner.learn import Learner
from random import randint

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
            y.append(randint(0, 1))
        
        self.separator.set_data(X, y)
        results = self.separator.run()

        X_raw, y = results["train"]
        self.vectorgen = VectorGenerator()
        self.vectorgen.set_data(X_raw, dict())
        X = self.vectorgen.run()

        self.learner = Learner("learner", "tu", "linear")
        self.learner.set_data(X, y)
        self.learner.run()

        X, y = results["test"]
        self.vectorgen.set_data(X, [])
        X = self.vectorgen.get()
        self.learner.test(X, y)
        print(results)

Main()