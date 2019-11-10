from system.loader.loader import Loader
from models.preprocessor.preprocess import Preprocessor
from models.wordgen.wordgenerator import WordGenerator
from config.config import config

class Model:
    
    def __init__(self):
        self.loader = Loader([
            "database",
            "refer_dict",
            "words", 
            "all_models"            
        ])
    
    def test(self, queries):
        res = []
        for query in queries:
            res.append(self.test_one(query))
        return res

    def test_one(self, sentence):
        preprocessor = Preprocessor()
        wordgener = WordGenerator("wordgen", config["model"]["window_size"], [])
        sentence, names = preprocessor.run_for_test(sentence)
        window_data = wordgener.run_for_test([sentence])
        words = sentence.split()
        for i, word in enumerate(words):
            if word not in window_data: continue
            items = window_data[word]
            sentences = items["sentences"]
            if word in self.loader.vectors:
                vectorizer = self.loader.vectors[word]
                vectorizer.set_data(sentences, self.loader.refer[word])
                X = vectorizer.run_for_test(sentences)
                words[i] = self.loader.learners[word].predict(X)[0]
            else:
                words[i] = word
        return ' '.join(words)
