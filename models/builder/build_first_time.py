from models.builder.build import Builder
from models.vectorgen.vectorgenerator import VectorGenerator
from models.learner.learn import Learner
from system.loader.loader import Loader
from models.data.imbalanced import BalanceData
from models.separate_data.separator import Separator
from config.config import config

class BuildFirstTime(Builder):
        
    def __init__(self):
        """ You have no data in database """
        super().__init__()
        self.loader = Loader([
            "database",  
            "local_data",
            "refer_dict",
        ])
        self.refer = self.loader.refer
        self.config = config["model"]
        self.preprocess()           # Preprocess data from local data
        self.push_raw()           # Push raw data to database
        self.push_beau()          # Push beau data to database
        self.push_names()         # Push names to database

        self.wordgenerate()         # Create word data
        self.push_words()         # Push word data to database

        self.build_models()         # Build & save models
    
    def build_models(self):
        """After this function: You have model vectors and model learner"""
        # self.learners = dict()
        # self.vectors = dict()
        for word, items in self.words.items():
            vectorizer = VectorGenerator(word)
            vectorizer.set_data(items["sentences"], self.refer[word])
            X = vectorizer.run()
            y = items["labels"]
            # self.vectors[word] = vectorizer
            vectorizer.save_model(self.config)      # Save vector

            balancer = BalanceData()#"SMOTE", 1)
            balancer.set_data(X, y)
            X, y = balancer.run()

            separater = Separator()
            separater.set_ratio({
                "train" : 0.7,
                "test"  : 0.3
            })
            separater.set_data(X, y)
            data = separater.run()

            X_train, y_train = data["train"]
            X_test, y_test   = data["test"]
            learner = Learner(word, "linear")
            learner.set_data(X_train, y_train)
            learner.run()
            learner.test(X_test, y_test)
            learner.save_model(self.config)         # Save model
            # self.learners[word] = learner
            del learner, vectorizer

    def save_models(self):
        for word, vectorizer in self.vectors.items():
            vectorizer.save_model(self.config)
        for word, learner in self.learners.items():
            learner.save_model(self.config)