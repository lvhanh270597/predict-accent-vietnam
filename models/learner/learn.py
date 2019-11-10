from sklearn import svm
from sklearn import naive_bayes
from models.model import *
from system.helpers import file as fman
from os import path

class Learner:

    type_of_models = {
        "linear": svm.LinearSVC,
        "rbf": svm.SVC,
        "naive_bayes": naive_bayes.MultinomialNB
    }

    def __init__(self, name, algorithm):
        self.name = name
        self.algorithm = algorithm
        self.ext_file = "." + algorithm[:3]
        self.model = None

    def set_data(self, X, y):
        """data only list of pair [vector --> label]"""
        self.X, self.y = X, y

    def run(self):
        print("%s -- fitting model..." % self.name)
        self.model = self.type_of_models[self.algorithm]()
        self.model.fit(self.X, self.y)
        print("done!")
    
    def predict(self, X):
        y_pred = self.model.predict(X)
        return y_pred
    
    def test(self, X, y):
        print("%s -- scoring model..." % self.name)
        print(self.model.score(X, y))
        print("done!")

    def save_model(self, config):        
        model_path = config["model_path"]
        model_ext = config["model_ext"]
        learner_config = config["save_learners"]
        model_path = path.join(model_path, learner_config["dir"])
        model_path = path.join(model_path, self.name)
        fman.make_dir(model_path)
        if learner_config["learner"] is True:
            filename = config["format"] % self.name
            fullpath = path.join(model_path, "model.%s" % model_ext)
            fman.save_object(self.model, fullpath)
    
    def load_model(self, config):
        model_path = config["model_path"]
        model_ext = config["model_ext"]
        learner_config = config["load_learners"]
        model_path = path.join(model_path, learner_config["dir"])
        model_path = path.join(model_path, self.name)
        if learner_config["learner"] is True:
            filename = config["format"] % self.name
            fullpath = path.join(model_path, "model.%s" % model_ext)
            self.model = fman.load_object(fullpath)
        