from config.config import config
from system.database.mongo import connector

class Loader:

    def __init__(self):
        self.load_database()
        self.load_log()

    def load_database(self):
        self.db = connector.AccessDatabase()
