from models.model import *

class Preprocessor(Model):
    """
        input:  raw data
        output: [list of names], [beautiful data]
        :raw: list of sentences
    """
    FILENAMES = ["names.txt", "sentences.txt"]

    def initialize(self):
        self.raw = []
        self.sentence_instance = Sentence()

    def set_data(self, raw):
        self.raw = raw

    def run(self):
        list_names, sentences = set(), []
        current_names, current_sents = set(), []
        self.log.start(len(self.raw))
        for sentence in self.raw:
            self.log.progress()
            sentence, names = self.working_on(sentence)
            # Update sentence and list of names
            current_sents.append(sentence)
            current_names.update(names)
            # If accept write online, write append this sentence
            if self.log.check_active():
                if self.save == "online":
                    self.save_data(current_sents, current_names, self.type["online"])
                if self.returned:
                    list_names.update(current_names)
                    sentences.extend(current_sents)
                del current_names, current_sents
                current_sents, current_names = [], set()

        if self.returned:
            list_names.update(current_names)
            sentences.extend(current_sents)
        if self.save == "online":
            self.save_data(current_sents, current_names, self.type["online"])
        if self.save == "after":
            self.save_data(sentences, list_names, "after")
        if self.returned:
            return sentences, list_names

    def working_on(self, sentence):
        self.sentence_instance.set_sentence(sentence)
        sentence = self.sentence_instance.beautify()
        return sentence, self.sentence_instance.get_extracted_names()

    def load_data(self, filedir):
        fullpath = fman.join_path(filedir, self.FILENAMES[1])
        sentences = fman.load_text(fullpath)
        fullpath = fman.join_path(filedir, self.FILENAMES[0])
        names = fman.load_text(fullpath)
        return sentences, names

    def save_data(self, sentences, listnames, type):
        print("Saving data...")
        curpath = fman.join_path(self.filedir, self.FILENAMES[0])
        fman.save_text(listnames, curpath, type)
        curpath = fman.join_path(self.filedir, self.FILENAMES[1])
        fman.save_text(sentences, curpath, type)
        print("Saved!")