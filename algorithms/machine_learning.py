from sklearn.svm import LinearSVC
import pickle, math
from data_structures.sentence import *
from helpers import data as dman
from config import config

class GuessOne:
    def __init__(self, name):
        self.name = name
        self.windows = config.WINDOW_SIZE
        self.clf = LinearSVC()
        self.X, self.y = [], []

    def set_data(self, data):
        self.sentences = data["sentences"]
        self.refer = data["refer"]
        self.analyze_data()

    def analyze_data(self):
        # print(self.sentences)
        # print(self.refer)
        self.data = []
        self.y = []
        self.docFreq = dict()
        self.vocab = dict()
        cnt = 0
        for X, y in self.sentences:
            self.data.append(X)
            self.y.append(y)
            for word in X.split():
                if word not in self.vocab:
                    self.docFreq[word] = 1
                    self.vocab[word] = cnt
                    cnt += 1
                else:
                    self.docFreq[word] += 1
        self.diff_labels = len(set(self.y))
        # print(self.data)
        # print(self.y)

    def get_bow_vectors(self):
        vectors = []
        for x in self.data:
            vector = [0] * len(self.vocab)
            for word in x.split():
                index = self.vocab[word]
                vector[index] = 1
            vectors.append(vector)
        self.X = vectors

    def get_window_vectors(self):
        vectors = []
        for x in self.data:
            vector = [0] * len(x.split())
            for i, word in enumerate(x.split()):
                index = self.vocab[word]
                vector[i] = index
            vectors.append(vector)
        self.X = vectors

    def get_tfidf_vectors(self):
        vectors = []
        for x in self.data:
            vector = [0] * len(self.vocab)
            for word in x.split():
                index = self.vocab[word]
                vector[index] += 1
            for i in range(len(self.vocab)):
                if vector[i] > 0:
                    vector[i] = - math.log10(vector[i])
            vectors.append(vector)
        self.X = vectors

    def get_dict_feature(self, sentence):
        words = sentence.split()
        half = len(words) // 2
        vector = []
        for nsize in range(config.MAX_LETTERS, 0, -1):
            for i in range(0, len(words) - nsize + 1):
                last_index = i + nsize - 1
                if (i <= half) and (last_index >= half):
                    cur_word = ' '.join(words[i: last_index + 1])
                    if cur_word in self.refer:
                        vector.append(1)
                    else:
                        vector.append(0)
        return vector
    def add_dict_feature(self):
        index = 0
        for sentence in self.data:
            vector = self.get_dict_feature(sentence)
            self.X[index].extend(vector)
            index += 1


    def train_test_split(self, ratio=.7):
        self.strain = int(ratio * len(self.X))
        self.Xtrain = self.X[:self.strain]
        self.Xtest = self.X[self.strain:]
        self.ytrain = self.y[:self.strain]
        self.ytest = self.y[self.strain:]

    def fit(self):
        if self.diff_labels >= 2:
            self.clf.fit(self.Xtrain, self.ytrain)

    def guess(self, sentence):
        words = sentence.split()[:self.windows]
        if self.diff_labels < 2:
            return words[self.windows // 2]

        vector = [0] * len(self.vocab)
        for word in words:
            index = 0
            if word in self.vocab:
                index = self.vocab[word]
            vector[index] = 1
        vector.extend(self.get_dict_feature(' '.join(words)))
        return self.predict(vector)

    def predict(self, vector):
        list_prep = self.clf.predict([vector])
        return list_prep[0]

    def score(self, file_extract):
        accuracy = 1
        if self.diff_labels >= 2:
            accuracy = self.clf.score(self.Xtest, self.ytest)
        message = "Accuracy on word: %s is equal = %.2f" % (self.name, accuracy * 100)
        if file_extract is not None:
            with open(file_extract, "a") as f:
                f.write("%s\n" % message)
        else:
            print(message)

    def save(self, filepath):
        pickle.dump(self.clf, open(filepath, 'wb'))

    def load(self, filepath):
        self.clf = pickle.load(open(filepath, 'rb'))

    def build(self):
        self.get_bow_vectors()
        self.add_dict_feature()
        self.train_test_split()
        self.fit()


class GuessSentence:
    def __init__(self, models):
        self.models = models

    def preprocess(self):
        sentence = Sentence(self.sentence)
        self.old_words = sentence.revert()
        sentence.remove_continue()
        sentence.lower()
        self.sentence = sentence.tokenize()

    def set_sentence(self, sentence):
        self.sentence = sentence
        self.preprocess()

    def get_result(self):
        data = dman.get_window_item(self.sentence, config.WINDOW_SIZE)
        res = []
        for sentence, label, _ in data:
            model = dman.get_item_indices(label, self.models)
            xcur = '__replace__'
            if model is not None:
                if not (label.startswith("__") and label.endswith("__")):
                    xcur = model.guess(sentence)
            res.append(xcur)

        for i, word in enumerate(res):
            if word == '__replace__':
                res[i] = self.old_words[i]
        return ' '.join(res)
