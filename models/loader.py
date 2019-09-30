from helpers import file as fman

class Loader:

    def __init__(self, env):
        self.load_funcs = {
            "raw": {
                "function": fman.load_folder,
                "args": env["RAW_PATH"]
            },
            "beautiful": {
                "function": fman.load_folder,
                "args": env["BEA_PATH"]
            },
            "models": {
                "function": fman.load_objects_on_folder,
                "args": env["MOD_PATH"]
            },
            "learning": {
                "function": fman.load_folder,
                "args": env["LEA_PATH"]
            },
            "words": {
                "function": fman.load_data_words,
                "args": env["WOR_PATH"]
            },
            "dictionary": {
                "function": fman.load_text,
                "args": env["DICTIONARY"]
            },
            "refer": {
                "function": fman.load_json,
                "args": env["REFER"]
            },
            "listwords" : {
                "function": fman.load_text,
                "args": env["LISTWORDS"]
            },
            "onediff" : {
                "function" : fman.load_text2dict,
                "args" : env["ONEDIFF"]
            },
            "listnames" : {
                "function" : fman.load_text,
                "args" : env["LISTNAMES"]
            },
            "count" : {
                "function" : fman.load_text,
                "args" : env["COUNT"]
            },
            "vocabularies": {
                "function": fman.load_vocabulary,
                "args": env["VOCAB_PATH"]
            }
        }
        self.always = [
            "refer",
            "dictionary",
            "onediff",
            "listnames",
            "listwords"
        ]
        self.load_step = [
            ["raw"],                        # For preprocessing
            ["beautiful"],                  # For word generating
            ["words"],                      # For building
            ["vocabularies", "models"]      # For testing
        ]
        self.data = dict()

    def load(self, step):
        load_items = self.always[:]
        if (step >= 0) and (step < len(self.load_step)):
            load_items.extend(self.load_step[step][:])
        for key in load_items:
            item = self.load_funcs[key]
            self.data[key] = item["function"](item["args"])
        return self.data

    def load_data(self, key):
        if key in self.load_funcs:
            self.load_funcs[key]()

    def get_data(self, key):
        return self.data[key] if key in self.data else []

    def set_data(self, key, data):
        self.data[key] = data

