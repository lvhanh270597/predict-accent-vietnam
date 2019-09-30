
from config.config import ENV
from models import loader
from models import training, testing


class AddAccent:

    def __init__(self):
        self.loader = loader.Loader(ENV)

        self.trainer = training.Training(ENV)

        self.tester = testing.Testing(ENV)

    def train(self, step):
        self.trainer.run(self.loader, step)

    def test(self, without_accents, with_accents):
        self.tester.run(self.loader, without_accents, with_accents)
