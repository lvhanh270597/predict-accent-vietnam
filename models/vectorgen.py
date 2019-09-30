from helpers import data as dman
from models.model import *
from data_structures.vocabulary import Vocabulary

class VectorGenerator:

    def __init__(self, name, word, auto_build_vocabulary=True, vocab=None, ngrams=[1], max_syl=5):
        self.name = name
        self.word = word
        self.ngrams = ngrams
        self.sentences = []
        self.refer = []
        self.max_syl = max_syl
        self.vocab = dict() if vocab is None else vocab
        self.set_vocab_attr(auto_build_vocabulary, 0.0, 1.0)

    def set_data(self, sentences, refer):
        """Only one word --> sentences"""
        self.sentences = sentences
        self.refer = refer

    def set_vocab_attr(self, auto_build_vocabulary, thresmin, thresmax):
        self.thresmin = thresmin
        self.thresmax = thresmax
        self.auto_build = auto_build_vocabulary

    def get_vocab(self):
        return self.vocab

    def run(self):
        if self.auto_build:
            self.build_vocabulary()
        features_vectors = dman.get_bow_vectors(self.sentences, self.ngrams, self.vocab)
        for i, sentence in enumerate(self.sentences):
            refer_dict_feature = dman.get_dict_feature(sentence, self.refer, self.max_syl)
            features_vectors[i].extend(refer_dict_feature)
        return features_vectors

    def build_vocabulary(self):
        self.vocab = Vocabulary(self.sentences)
        self.vocab.build()

    def save(self, filedir):
        self.vocab.save(filedir, self.word)
