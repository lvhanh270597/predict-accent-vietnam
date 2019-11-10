from sklearn import svm
from sklearn import naive_bayes
from models.model import *

class Learner:

    type_of_models = {
        "linear": svm.LinearSVC,
        "rbf": svm.SVC,
        "naive_bayes": naive_bayes.MultinomialNB
    }

    def __init__(self, name, word, algorithm):
        self.name = name
        self.word = word
        self.algorithm = algorithm
        self.ext_file = "." + algorithm[:3]
        self.model = None

    def set_data(self, X, y):
        """data only list of pair [vector --> label]"""
        self.X, self.y = X, y
        print(self.X)
        print(self.y)

    def run(self):
        print("%s -- fitting model..." % self.name)
        self.model = self.type_of_models[self.algorithm]()
        self.model.fit(self.X, self.y)
        print("done!")
    
    def test(self, X, y):
        print("%s -- scoring model..." % self.name)
        print(self.model.score(X, y))
        print("done!")

    def save(self, filedir):
        print("%s -- saving model..." % self.name)
        cur_dir = fman.join_path(filedir, "%s%s" % (self.word, self.ext_file))
        fman.save_object(self.model, cur_dir)
        print("done!")

    def load(self, filedir):
        fullpath = fman.join_path(filedir, "%s%s" % (self.word, self.ext_file))
        self.model = fman.load_object(fullpath)
        return self.model