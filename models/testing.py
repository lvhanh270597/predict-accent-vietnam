
from models import preprocessor
from models import wordgen
from models import vectorgen
from helpers import data as dman
from logs.log import Log

class Testing:

    def __init__(self, env):
        self.env = env
        self.preprocessor = []
        self.wordgener = []
        self.learner = []
        self.step_actions = [
            self.preprocessing,
            self.get_window_items
            # self.word_generating,
            # self.vector_generating,
            # self.testing
        ]
        self.data = dict()
        self.logger = Log("testing")

    def run(self, loader, without_accents, with_accents):
        self.data = loader.load(3)
        self.data["without_accents"] = without_accents
        self.data["with_accents"] = with_accents
        for istep in range(len(self.step_actions)):
            self.step_actions[istep]()

    def preprocessing(self):
        self.preprocessor = preprocessor.Preprocessor("testing-preprocessor")
        self.preprocessor.set_data(self.data['without_accents'])
        sentences, _ = self.preprocessor.run()
        self.preprocessor.set_data(self.data["with_accents"])
        _sentences, listnames = self.preprocessor.run()
        self.data["beautiful"] = {
            "without_accents" : sentences,
            "with_accents" : _sentences,
            "names"     : listnames
        }

    def get_window_items(self):
        vocabularies = self.data["vocabularies"]
        refer = self.data["refer"]
        without_accents, with_accents = self.data["beautiful"]["without_accents"], self.data["beautiful"]["with_accents"]
        for sentence, rsentence in zip(without_accents, with_accents):
            print(sentence)
            print(rsentence)
            window_items = dman.get_window_item(rsentence, self.env["WINDOW_SIZE"])
            for item in window_items:
                window_sent, word, label = item
                predict = word
                if word in vocabularies:
                    vector = dman.get_bow_vectors([window_sent], self.env["NGRAMS"], vocabularies[word])
                    refer_dict_feature = dman.get_dict_feature(window_sent, refer, self.env["MAX_SYLLABLE"])
                    vector[0].extend(refer_dict_feature)
                    predict = self.predict(word, vector)
                print(predict, end=" ")
            print()

        # print(dman.get_bow_vectors(sentences, [1], self.data["vocabularies"]["kip"]))

    # def word_generating(self):
    #     self.wordgener = wordgen.WordGenerator("testing-wordgen", self.env["WINDOW_SIZE"], self.data["listwords"])
    #     without_accents = self.data["beautiful"]["without_accents"]
    #     with_accents = self.data["beautiful"]["with_accents"]
    #     self.wordgener.set_data(without_accents, with_accents)
    #     self.data["words"] = self.wordgener.run_test()
    #
    # def vector_generating(self):
    #     results = []
    #     vocabularies = self.data["vocabularies"]
    #     refer = self.data["refer"]
    #     for data_words in self.data["words"]:
    #         word_vectors = dict()
    #         for word, data in data_words.items():
    #             sentences = data["sentences"]
    #             if word in vocabularies:
    #                 vectorgener = vectorgen.VectorGenerator("testing-vectorgen", word, False, vocabularies[word])
    #                 vectorgener.set_data(sentences, refer[word])
    #                 vectors = vectorgener.run()
    #                 word_vectors[word] = vectors
    #         results.append(word_vectors)
    #     self.data["vectors"] = results
    #
    # def testing(self):
    #     fullsize = len(self.data["vectors"])
    #     self.logger.start(fullsize)
    #     self.fullscore = 0
    #     for data_words, data_vects in zip(self.data["words"], self.data["vectors"]):
    #         cnt = 0
    #         for word in data_vects:
    #             self.logger.progress([word])
    #             current_sents = data_words[word]["sentences"]
    #             current_labels = data_words[word]["labels"]
    #             current_vects = data_vects[word]
    #
    #             print(current_sents, current_labels)
    #             labels_pred = self.predict(word, current_vects)
    #
    #             acc = 0
    #             for sent, y, y_pred in zip(current_sents, current_labels, labels_pred):
    #                 print("%s : predict: %s | correct: %s" % (sent, y_pred, y))
    #                 acc += y_pred == y
    #             print("Accuracy = %.2f%%" % ((acc / len(labels_pred)) * 100))
    #             cnt += acc == len(labels_pred)
    #         self.fullscore += (cnt == len(data_vects))
    #
    #     print("%d full score | %d/%d %.2f%%" % (self.fullscore, self.fullscore, len(self.data["words"]), (self.fullscore / len(self.data["words"])) * 100))

    def predict(self, word, vectors):
        if word not in self.data["models"]:
            result = word
            # this is in onediff list
            loader_words = self.loader.get_data("words")
            if word in loader_words:
                data_word = loader_words[word]
                if len(data_word) > 0:
                    labels = data_word["labels"]
                    result = labels[0]

            return result
        model = self.data["models"][word]
        y_pred = model.predict(vectors)
        return y_pred[0]

    def score(self, list_word_vects, labels):
        models = self.data["models"]
        scores = dict()
        for word, vectors in list_word_vects.items():
            if word in models:
                current_score = models[word].score(vectors, labels)
                scores[word] = current_score
        return scores


