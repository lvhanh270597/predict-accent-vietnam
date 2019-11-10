from system.data_structures.sentence import Sentence
from models.model import *

class Preprocessor(Model):
    """
        input:  raw data
        output: [list of names], [beautiful data]
        :raw: list of sentences
    """

    def __init__(self, name="preprocessor"):
        super().__init__(name)
        self.raw = []
        self.sentence_instance = Sentence()

    def set_data(self, raw):
        self.raw = raw

    def run(self):
        list_names, sentences = set(), []
        for sentence in self.raw:
            sentence, names = self.working_on(sentence)
            # Update sentence and list of names
            sentences.append(sentence)
            list_names.update(names)
        return sentences, list_names

    def working_on(self, sentence):
        self.sentence_instance.set_sentence(sentence)
        sentence = self.sentence_instance.beautify()
        return sentence, self.sentence_instance.get_extracted_names()