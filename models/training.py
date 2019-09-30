from models import preprocessor
from models import wordgen
from models import vectorgen
from models import learner
from helpers import file as fman
from helpers import string as sman

class Training:

    def __init__(self, dataenv):
        self.env = dataenv
        self.data = dict()
        self.preprocessor = []
        self.wordgener = []
        self.step_actions = [
            self.preprocessing,
            self.word_generating,
            self.build
        ]
        self.maxstep = 2
        self.step = 0

    def run(self, loader, step=0):
        self.step = min(step, self.maxstep)
        self.data = loader.load(step)
        for istep in range(step, len(self.step_actions)):
            self.step_actions[istep]()

    def preprocessing(self):
        self.preprocessor = preprocessor.Preprocessor("training-preprocessor")
        self.preprocessor.set_online_save(self.env["BEA_PATH"], 1000)
        raw_files = self.data["raw"]
        if len(raw_files) > 0:
            first_key = list(raw_files.keys())[0]
            first_raw_data = raw_files[first_key]
            self.preprocessor.set_data(first_raw_data)
            sentences, names = self.preprocessor.run()
            self.data["beautiful"] = {
                "sentences" : sentences,
                "names" : set(names)
            }

    def word_generating(self):
        listwords = set(self.data["listwords"])
        # Create word generator with online save at WORD_PATH and interval = 1
        self.wordgener = wordgen.WordGenerator("training-wordgen", self.env["WINDOW_SIZE"], listwords)
        self.wordgener.set_online_save(self.env["WOR_PATH"], interval=1)
        # Get and set data
        sentences = self.data["beautiful"]["sentences"]
        self.wordgener.set_data(sentences)
        data, onelabel = self.wordgener.run()
        self.data["words"] = data
        # Save one label (word --> real word)
        fman.save_text(sman.convert_dict2text(onelabel, self.env["DELIMITER"]), self.env["ONEDIFF"])

    def build(self):
        vectors = dict()
        models = dict()
        refer = self.data["refer"]
        word_data = self.data["words"]
        for word, data in word_data.items():
            # Get sentences and labels
            sentences, labels = data["sentences"], data["labels"]
            # Building vectors of features
            vectorgener = vectorgen.VectorGenerator("training-vectorgen-%s" % word, word)
            current_refer = refer[word]
            vectorgener.set_data(sentences, current_refer)
            list_vector_features = vectorgener.run()
            vectorgener.save(filedir=self.env["VOCAB_PATH"])
            # Building model depended on above vectors of features
            model = learner.Learner("train-learner", word, "linear")
            model.set_data(list_vector_features, labels)
            model.run()
            model.save(filedir=self.env["MOD_PATH"])

            if self.env["REMOVE_VECTOR_MODEL"]:
                del vectorgener, model
            else:
                vectors[word] = vectorgener
                models[word]  = model
        return vectors, models

