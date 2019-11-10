from models.builder.build import Builder

class BuildWithBeforeData(Builder):
        
    def __init__(self):
        """ You have already data in database but you have no local data """
        self.loader = Loader({
            "database"  : True,
            "words"     : True,
            "local_data": False
        })

        self.build_models()         # Build models
        self.save_models()          # Save models    

    
    def build_models(self):
        self.load_refer_dict()
        self.learners = dict()
        self.vectors = dict()
        for word, items in self.words.items():
            vectorizer = VectorGenerator()
            vectorizer.set_data(items["sentences"], self.refer[word])
            X = vectorizer.run()
            y = items["labels"]
            
            self.vectors[word] = vectorizer

            balancer = BalanceData()#"SMOTE", 1)
            balancer.set_data(X, y)
            X, y = balancer.run()

            separater = Separator()
            separater.set_ratio({
                "train" : 0.7,
                "test"  : 0.3
            })
            separater.set_data(X, y)
            data = separater.run()

            X_train, y_train = data["train"]
            X_test, y_test   = data["test"]
            learner = Learner("learner", word, "linear")
            learner.set_data(X_train, y_train)
            learner.run()
            learner.test(X_test, y_test)

            self.learners[word] = learner
          

    def test(self):
        while True:
            sentence = input("Enter your query: ")
            self.test_one(sentence)
    
    def test_one(self, sentence):
        preprocessor = Preprocessor()
        sentence, names = preprocessor.run_for_test(sentence)
        window_data = self.wordgener.run_for_test([sentence])
        print(window_data)
        words = sentence.split()
        for i, word in enumerate(words):
            items = window_data[word]
            sentences = items["sentences"]
            if word in self.vectors:
                vectorizer = self.vectors[word]
                vectorizer.set_data(sentences, self.refer[word])
                X = vectorizer.get()
                words[i] = self.learners[word].predict(X)[0]
            else:
                words[i] = word
        print(' '.join(words))

