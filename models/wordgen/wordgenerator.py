from models.model import *
from system.helpers import data as dman
from system.data_structures.sentence import Sentence

class WordGenerator(Model):

    collection_name = "word"
    fields = [
        "origin", 
        "sentences", 
        "labels"
    ]

    def __init__(self, name, window_size, in_list):
        super().__init__(name)
        self.window_size = window_size
        self.in_list = set(in_list)
        self.check_in_list = len(self.in_list) > 0
        self.sentences = []
        self.onelabel = dict()
        self.sentence_instance = Sentence()
        self.result = dict()

    def set_data(self, sentences):
        """Data are only list of sentences"""
        self.sentences = sentences

    def run(self):
        data = dman.create_window_items(self.sentences, self.window_size)
        self.result = dict()
        for word, data in data.items():
            if (self.check_in_list) and (word not in self.in_list):
                print("%s is not in template words --> skip!" % word)
                continue
            sentences, labels = dman.separate_part(data, 2)
            # Word with only one fix
            if len(set(labels)) == 1:
                self.onelabel[word] = labels[0]
                continue
            new_data = {
                "origin" : word, 
                "sentences" : sentences,
                "labels" : labels
            }
            self.result[word] = new_data
        return self.result, self.onelabel

    def run_for_test(self, sentences):
        data = dman.create_window_items(sentences, self.window_size)
        result = dict()
        for word, data in data.items():
            sentences, labels = dman.separate_part(data, 2)
            # Word with only one fix
            new_data = {
                "origin" : word, 
                "sentences" : sentences,
                "labels" : labels
            }
            result[word] = new_data
        return result

    def save_words(self, db_instance):
        data = []
        for word, cur_data in self.result.items():
            item = dict()
            for field in self.fields:
                item[field] = cur_data[field]
            data.append(item)
        
        for word, cur_data in self.onelabel.items():
            data.append({
                "origin" : word, 
                "label" : cur_data
            })

        db_instance.write(self.collection_name, data)

    def get_words(self, db_instance, words):
        data = dict()
        for word in words:
            db_data = db_instance.find(self.collection_name, {"origin" : word}, {"_id" : 0})
            data[word] = dict()
            for items in db_data:
                data[word] = items
        return data