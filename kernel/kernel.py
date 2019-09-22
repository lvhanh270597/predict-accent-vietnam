from controller.data import DataManager
from controller.model import Modeler
from helpers import string as sman

class Kernel:
    def __init__(self):
        self.datactl = DataManager()
        self.modelctl = Modeler(self.datactl)
    def add_document(self, document):
        list_rebuild = self.datactl.add_document(document)
        self.modelctl.rebuild(list_rebuild)
    def rebuild(self, list_of_words):
        self.modelctl.rebuild(list_of_words)
    def backup(self, backup_dir):
        self.datactl.backup(backup_dir)
        self.modelctl.backup(backup_dir)
    def load_backup(self, data_bck_dir, model_bck_dir):
        self.datactl.load_backup(data_bck_dir)
        self.modelctl.load_backup(model_bck_dir)
    def guess(self, sentence):
        return self.modelctl.guess(sentence)
