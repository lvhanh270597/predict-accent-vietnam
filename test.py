from models.builder.build_first_time import BuildFirstTime
from models.loader.model import Model

class Main:
    
    def __init__(self):
        # BuildFirstTime()
        model = Model()
        while True:
            sentence = input("Enter your query: ")
            print(model.test_one(sentence))


Main()