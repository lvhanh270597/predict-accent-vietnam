from models.model import Model
from sklearn.model_selection import train_test_split

class Separator(Model):

    def __init__(self, name="separator", minimum=10, shuffle=True):
        super().__init__(name)
        self.ratio = {
            "train": 0.6,
            "dev": 0.2,
            "test": 0.2
        }
        self.minimum = minimum
        self.shuffle = shuffle
        self.X, self.y = [], []
        self.results = dict()

    def set_data(self, X, y):
        self.X, self.y = X, y

    def set_ratio(self, ratio):
        self.ratio = ratio

    def run(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=self.ratio["test"], shuffle=self.shuffle, random_state=42)
        if "dev" in self.ratio:            
            X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=self.ratio["dev"], shuffle=self.shuffle, random_state=42)
            self.results = {
                "train" : [X_train, y_train],
                "dev"   : [X_val, y_val],
                "test"  : [X_test, y_test]
            }
        else:
            self.results = {
                "train" : [X_train, y_train],
                "test"  : [X_test, y_test]
            }
        if len(self.y) <= self.minimum:
            for key in self.results:
                self.results[key] = [self.X[:], self.y[:]]
        return self.results
