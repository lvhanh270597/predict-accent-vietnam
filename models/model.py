from logs.log import Log
from data_structures.sentence import Sentence
from helpers import file as fman

class Model(object):

    def __init__(self, name="Undefined", save=False, returned=True):
        self.save = save
        self.returned = returned
        self.filedir = "./"
        self.name = name
        self.type = {
            "online": "a",
            "after": "w"
        }
        self.initialize()
        self.log = Log(self.name)
        print("Created a %s successully!" % self.name)

    def initialize(self):
        pass

    def set_data(self, data):
        pass

    def load_data(self, dir):
        pass

    def save_data(self):
        pass

    def set_online_save(self, filedir, interval=20):
        self.save = "online"
        self.log.set_interval(interval=interval)
        fman.remove_folder(filedir)
        fman.make_dir(filedir)
        self.filedir = filedir

    def set_after_save(self, filedir):
        self.save = "after"
        self.filedir = filedir
        self.returned = True

    def run(self):
        pass

    def check_active(self, status):
        if self.save == "after":
            return self.log.cnt >= self.log.full
        return (status == self.save) and self.log.check_active()

    def __del__(self):
        print("End %s!" % self.name)