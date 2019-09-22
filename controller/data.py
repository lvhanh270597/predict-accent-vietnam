from os import listdir
from config import config
from helpers import data as dman
from helpers import file as fman
from helpers import string as sman
from data_structures.sentence import Sentence


class DataManager:
    def __init__(self):
        self.dataroot = config.DATA_ROOT
        self.list_names = {"ready", "words"}
        self.load_funcs = {
            # "raw" : self.load_raw,
            "words" : self.load_words,
            "ready" : self.load_ready
        }
        self.filenames = dict()
        self.data = {
            "refer" : [],
            "words" : [],
            "full" : []
        }
        for name in self.list_names:
            self.filenames[name] = fman.join_path(self.dataroot, name)
        self.load_data()

    def get_data_word(self, label, next_label):
        if label in self.data:
            if next_label in self.data[label]:
                return self.data[label][next_label]
        return []

    def add_document(self, document):
        sentences = dman.separate_sentence(document)
        for i, sentence in enumerate(sentences):
            sentence = Sentence(sentence)
            sentence.remove_continue()
            sentences[i] = sentence.tokenize()
        # add to full data
        current_time = sman.get_current_time()
        self.data["full"][current_time] = sentences
        # write to full data
        save_path = fman.join_path(self.filenames["ready"], ["full", current_time])
        fman.save_text(sentences, save_path)
        # creating window vector words
        data = dman.create_window_items(sentences, config.WINDOW_SIZE)
        # update word file
        for word, items in data.items():
            word_path = fman.join_path(self.filenames["words"], word)
            refer_data = []
            if word not in self.data["words"]:
                fman.make_dir(word_path)
                refer_data = dman.get_item_indices(word, self.data["refer"], [])
                self.data["words"][word] = {
                    "sentences" : items,
                    "refer" : refer_data
                }
            else:
                self.data["words"][word]["sentences"].extend(items)

            sentence_path = fman.join_path(word_path, "sentences.txt")
            refer_path = fman.join_path(word_path, "refer.txt")
            fman.save_data_point(data[word], sentence_path, "a")
            fman.save_text(refer_data, refer_path, "a")

        list_of_words = data.keys()
        return list_of_words

    def set_filenames(self, description):
        self.filenames = dict()
        for name, fpath in description.items():
            if name in self.list_names:
                self.filenames[name] = fpath

    def load_data(self, list_names=None):
        print("Loading data...")
        if list_names is None:
            list_names = self.list_names
        list_names = list(set(list_names).intersection(self.list_names))
        for name in list_names:
            self.load_funcs[name]()

    # def load_raw(self):
    #     raw_data = dict()
    #     raw_dir = self.filenames["raw"]
    #     for filename in listdir(raw_dir):
    #         name, _ = func.get_filename_ext(filename)
    #         raw_data[name] = func.load_text()

    def load_ready(self):
        print("Loading full data...")
        self.data["full"] = dict()
        fulldata_path = fman.join_path(self.filenames["ready"], "full")
        for filename in listdir(fulldata_path):
            path = fman.join_path(fulldata_path, filename)
            name, _ = fman.get_filename_ext(filename)
            self.data["full"][name] = fman.load_text(path)

        refer_path = fman.join_path(self.filenames["ready"], "refer_dict.json")
        self.data["refer"] = fman.load_json(refer_path)

    def load_words(self):
        print("Loading data words...")
        word_path = self.filenames["words"]
        self.data["words"] = dict()
        for folder in listdir(word_path):
            cur_dir = fman.join_path(word_path, folder)
            self.data["words"][folder] = {
                "sentences" : 0,
                "refer" : 0
            }
            self.data["words"][folder]["sentences"] = fman.load_data_point(fman.join_path(cur_dir, "sentences.txt"))
            self.data["words"][folder]["refer"] = fman.load_text(fman.join_path(cur_dir, "refer.txt"))

    def backup(self, datadir):
        name = "ready"
        cur_dir = fman.join_path(datadir, name)
        fman.make_dir(cur_dir)
        # save ready full data
        fulldata_path = fman.join_path(cur_dir, "full")
        fman.make_dir(fulldata_path)
        for filename, item in self.data[name]:
            cur_path = fman.join_path(fulldata_path, filename)
            fman.save_text(self.data[name]["full"][filename], cur_path)
        fman.save_json(self.data[name]["refer"])
        # save words
        name = "words"
        cur_dir = fman.join_path(datadir, name)
        fman.make_dir(cur_dir)
        for word in self.data["words"]:
            data_word = self.data["words"][word]
            word_dir = fman.join_path(cur_dir, word)
            fman.make_dir(word_dir)
            fman.save_data_point(data_word["sentences"],
                                 fman.join_path(word_dir, "sentences.txt"))
            fman.save_text(data_word["refer"],
                           fman.join_path(word_dir, "refer.txt"))

    def load_backup(self, data_dir):
        self.dataroot = data_dir
        self.load_data()
