from config.config import config
from system.database.mongo import connector
from system.logs.log import Log

class Loader:

    def __init__(self):
        self.load_database()
        self.log = Log("main loader")

    def load_database(self):
        try:
            self.db = connector.AccessDatabase()
        except:
            self.log.write("Can't connect to the database!")
