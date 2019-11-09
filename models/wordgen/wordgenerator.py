from models.model import *
from system.helpers import data as dman

class WordGenerator(Model):

    def __init__(self, name, window_size, in_list):
        super().__init__(name)
        self.window_size = window_size
        self.in_list = set(in_list)
        self.sentences = []
        self.real_sentences = []
        self.onelabel = dict()
        self.sentence_instance = Sentence()
        self.result = dict()

    def set_data(self, sentences, real_sentences=[]):
        """Data are only list of sentences"""
        self.sentences = sentences
        self.real_sentences = real_sentences

    def run(self):
        data = dman.create_window_items(self.sentences, self.window_size)
        self.result = dict()
        self.log.start(len(data))
        self.log.set_interval(1)
        for word, data in data.items():
            self.log.progress([word])
            if word not in self.in_list:
                print("%s is not in template words --> skip!" % word)
                continue
            sentences, labels = dman.separate_part(data, 2)
            # Word with only one fix
            if len(set(labels)) == 1:
                self.onelabel[word] = labels[0]
                continue
            new_data = {
                "sentences" : sentences,
                "labels" : labels
            }
            # Save file now
            if self.check_active("online"):
                self.save_word(word, new_data)

            if self.returned:
                self.result[word] = new_data
            else:
                del new_data

        if self.check_active("after"):
            self.save_data()

        if self.returned:
            return self.result, self.onelabel

    def run_test(self):
        self.result = []
        for sentence, rsentence in zip(self.sentences, self.real_sentences):
            data1 = dman.create_window_items([sentence], self.window_size)
            data2 = dman.create_window_items([rsentence], self.window_size)
            self.log.start(len(data1))
            self.log.set_interval(1)
            current_result = dict()
            for word in data1:
                self.log.progress([word])
                if word not in self.in_list:
                    print("%s is not in template words --> skip!" % word)
                    continue
                sentences, _ = dman.separate_part(data1[word], 2)
                _, labels = dman.separate_part(data2[word], 2)

                new_data = {
                    "sentences": sentences,
                    "labels": labels
                }
                current_result[word] = new_data
            self.result.append(current_result)
        return self.result

    def save_data(self):
        for word, cur_data in self.result.items():
            self.save_word(word, cur_data)

    def save_word(self, word, data):
        cur_dir = fman.join_path(self.filedir, word)
        fman.make_dir(cur_dir)
        for key, value in data.items():
            filepath = fman.join_path(cur_dir, key + ".txt")
            fman.save_text(value, filepath)

    def load_data(self, dir):
        cnt, res = 0, dict()
        name_loads = ["sentences", "labels"]
        for word in self.in_list:
            current_dir = fman.join_path(dir, word)
            if not fman.check_folder(current_dir):
                continue
            data = dict()
            for name in name_loads:
                fullpath = fman.join_path(current_dir, name + ".txt")
                if not fman.check_file(fullpath):
                    break
                data[name] = fman.load_text(fullpath)
            if len(data) == len(name_loads):
                cnt += 1
                res[word] = data
        return res
