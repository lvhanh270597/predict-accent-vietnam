from config.config import config
from system.database.mongo import connector
from system.loader.localdata import LocalData
from models.vectorgen.vectorgenerator import VectorGenerator
from models.learner.learn import Learner
from system.logs.log import Log

class Loader:

    def __init__(self, list_load=None):
        self.log = Log("main-loader")
        self.functions = {
            "database"      : self.load_database,
            "local_data"    : self.load_localdata,
            "refer_dict"    : self.load_refer,
            "words"         : self.load_words,
            "all_models"    : self.load_models
        }

        if list_load is None:
            self.load_database()
            self.load_localdata()
        else:
            for key in list_load:
                self.functions[key]()

    def load_database(self):
        try:
            self.db = connector.AccessDatabase()
        except:
            self.log.write("Can't connect to the database!")

    def load_localdata(self):
        try:
            self.ldata = LocalData()
        except:
            self.log.write("Can't connect to local data!")
    
    def load_refer(self):
        self.refer = dict()
        for item in self.db.find("refer-dict", {}, {"_id" : 0}):
            key, val = item["word"], item["refer"]
            self.refer[key] = val

    def load_words(self):
        self.words = dict()
        for item in self.db.find("word", {}, {"_id" : 0}):
            print(item)
            word = item["origin"]
            sentences, labels = item["sentences"], item["labels"]
            self.words[word] = {
                "sentences" :   sentences,
                "labels"    :   labels
            }

    def load_models(self):
        list_words = self.words.keys()
        self.vectors = dict()
        self.learners = dict()
        for word in list_words:
            vectorizer = VectorGenerator(name=word)
            vectorizer.load_model(config["model"])
            self.vectors[word] = vectorizer
            learner = Learner(word, "linear")
            learner.load_model(config["model"])
            self.learners[word] = learner