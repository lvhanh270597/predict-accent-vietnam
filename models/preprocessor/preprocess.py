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
        set_names, list_names, sentences = set(), [], []
        for sentence in self.raw:
            sentence, names = self.working_on(sentence)
            # Update sentence and list of names
            set_names.update(names)
            sentences.append(sentence)
            list_names.append(list(names))
        return sentences, list_names, set_names

    def run_for_test(self, sentence):
        self.test = dict()
        sentence, names = self.working_on(sentence)
        # Update sentence and list of names
        return sentence, names

    def restore(self, sentence, names):
        return Sentence().restore_sentence(sentence, names)

    def working_on(self, sentence):
        self.sentence_instance.set_sentence(sentence)
        sentence = self.sentence_instance.beautify()
        return sentence, self.sentence_instance.get_extracted_names()