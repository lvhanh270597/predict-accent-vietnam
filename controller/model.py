from config import config
from os import listdir
from helpers import file as fman
from logs import log
from algorithms.machine_learning import GuessOne, GuessSentence

class Modeler:
    """
    Manage all model of words
    """
    MODEL_ROOT = config.DATA_ROOT + "/models"
    MODEL_EXT = config.MODEL_EXT

    def __init__(self, data_manager):
        self.load_models()
        self.guesser = GuessSentence(self.models)
        self.data_manager = data_manager
        self.set_data()

    def set_data(self):
        for word in self.models:
            self.models[word].set_data(self.data_manager.get_data_word("words", word))

    def load_models(self):
        self.models = dict()
        self.load_model_dir(self.MODEL_ROOT)

    def load_model_dir(self, dirpath):
        for filename in listdir(dirpath):
            fpath = dirpath + "/" + filename
            word, ext = fman.get_filename_ext(filename)
            if ext == self.MODEL_EXT:
                cur_model = GuessOne(word)
                cur_model.load(fpath)
                self.models[word] = cur_model

    def rebuild(self, list_of_words):
        for word in list_of_words:
            if word not in self.models:
                self.models[word] = GuessOne(word)
            self.models[word].set_data(self.data_manager.get_data_word("words", word))
            self.models[word].build()
            fpath = fman.join_path(self.MODEL_ROOT, [word + "." + config.MODEL_EXT])
            self.models[word].save(fpath)

    def backup(self, datadir):
        if not fman.check_folder(datadir):
            log.write_log("Models could be not backup!")
            return False
        for word, model in self.models.items():
            filepath = datadir + "/" + word + self.MODEL_EXT
            self.models[word].save(filepath)
        log.write_alog("Models saved backup at %s!" % datadir)

    def load_backup(self, datadir):
        self.load_model_dir(datadir)

    def guess(self, sentence):
        self.guesser.set_sentence(sentence)
        return self.guesser.get_result()