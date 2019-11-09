from system.logs.log import Log
# from data_structures.sentence import Sentence
# from system.helpers import file as fman

class Model:

    def __init__(self, name="Undefined", writeLog=True):
        self.name = name
        self.verbose = verbose
        self.writeLog = writeLog
        if self.writeLog:
            self.log = Log(self.name)
            self.log.write("Created a %s successully!" % self.name)

    def __del__(self):
        if self.writeLog:
            self.log = Log(self.name)
            self.log.write("End %s!" % self.name)