from models.model import *
from sklearn.model_selection import train_test_split

class Separator(Model):

    FILENAMES = ["sentences.txt", "labels.txt"]

    def __init__(self, shuffle=True):
        super().__init__()
        self.shuffle = shuffle

    def initialize(self):
        self.ratio = {
            "train": 0.6,
            "dev": 0.2,
            "test": 0.2
        }
        self.X = []
        self.y = []
        self.results = dict()
        self.name = "separator"

    def set_data(self, X, y):
        self.X, self.y = X, y

    def set_ratio(self, ratio):
        self.ratio = ratio

    def run(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=self.ratio["test"], shuffle=self.shuffle, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=self.ratio["dev"], shuffle=self.shuffle, random_state=42)
        self.results = {
            "train" : [X_train, y_train],
            "dev"   : [X_val, y_val],
            "test"  : [X_test, y_test]
        }
        return self.results

    def load_data(self, dir):
        self.results = dict()
        for name in ["train", "dev", "test"]:
            new_list = []
            current_dir = fman.join_path(dir, name)
            for _, filename in enumerate(self.FILENAMES):
                fullpath = fman.join_path(current_dir, filename)
                new_list.append(fman.load_text(fullpath))
            self.results[name] = new_list
        return self.results

    def save_at(self, filedir):
        print("Saving data at %s" % filedir)
        for name, data in self.results.items():
            cur_dir = fman.join_path(filedir, name)
            fman.make_dir(cur_dir)
            for i, filename in enumerate(self.FILENAMES):
                fullpath = fman.join_path(cur_dir, filename)
                fman.save_text(self.results[name][i], fullpath)
        print("Saved!")
