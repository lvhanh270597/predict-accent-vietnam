# from system.helpers import file as fman
from config.config import config
from system.database.mongo import connector

class Loader:

    def __init__(self):
        self.load_database()

    def load_database(self):
        self.db = connector.AccessDatabase()
