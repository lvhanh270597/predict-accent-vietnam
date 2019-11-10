from config.config import config
from models.separate_data.separator import Separator
from models.preprocessor.preprocess import Preprocessor
from system.loader.loader import Loader
from models.vectorgen.vectorgenerator import VectorGenerator
from models.wordgen.wordgenerator import WordGenerator
from models.learner.learn import Learner
from models.data.imbalanced import BalanceData
from random import randint

class Builder:

    def __init__(self):
        self.config = config["model"]

    def preprocess(self):
        self.raw_data = self.loader.ldata.data
        self.preprocessor = Preprocessor()
        self.preprocessor.set_data(self.raw_data)
        self.sentences, self.names, self.set_names = self.preprocessor.run()
    
    def push_raw(self):
        data = []
        for i, sen in enumerate(self.raw_data):
            data.append({
                "text" : sen
            })
        print(data)
        self.loader.db.write("raw", data)
    
    def push_beau(self):
        data = []
        for sent, names in zip(self.sentences, self.names):
            data.append({
                "sentence" : sent,
                "names" : names
            })
        print(data)
        self.loader.db.write("beau", data)
    
    def push_names(self):
        data = []
        for name in self.set_names:
            data.append({
                "name" : name
            })
        print(data)
        self.loader.db.write("names", data)

    def wordgenerate(self):
        self.wordgener = WordGenerator("wordgen", self.config["window_size"], self.refer)
        self.wordgener.set_data(self.sentences)
        self.words, self.onelabel = self.wordgener.run()

    def push_words(self):
        data = []
        for _, val in self.words.items():
            data.append(val)
        self.loader.db.write("word", data)

        data = []
        for key, val in self.words.items():
            data.append({
                'origin': key, 
                'label' : val
            })
        self.loader.db.write("onelabel", data)

    def test(self):
        while True:
            sentence = input("Enter your query: ")
            self.test_one(sentence)
    
    def test_one(self, sentence):
        preprocessor = Preprocessor()
        sentence, names = preprocessor.run_for_test(sentence)
        window_data = self.wordgener.run_for_test([sentence])
        print(window_data)
        words = sentence.split()
        for i, word in enumerate(words):
            items = window_data[word]
            sentences = items["sentences"]
            if word in self.vectors:
                vectorizer = self.vectors[word]
                vectorizer.set_data(sentences, self.refer[word])
                X = vectorizer.get()
                words[i] = self.learners[word].predict(X)[0]
            else:
                words[i] = word
        print(' '.join(words))

    