from system.loader.loader import Loader
from models.vectorgen.vectorgenerator import VectorGenerator

class Main:
    def __init__(self):
        self.loader = Loader()
        s = """bao dien tu cua bao
tan cong tu choi dich
che do tu bao ve
bao dien tu dan tri
bao dien tu cua bao
__num__ vua tu __name__ ve
anh chup tu " dan
thoai loi tu __name__ __name__
moi la tu the he
__other__ khai tu __other__ __other__
__name__ loi tu dau tien
bao dien tu dan tri
bao dien tu cua bao
__num__ nguoi tu vong trong
nha dau tu ban ra
the gioi tu __num__ ."""
        corpus = s.split("\n")
        data = self.loader.db.find_one("refer-dict", {"word" : "tu"})
        refer = data["refer"]
        self.vectorgen = VectorGenerator("tu")
        self.vectorgen.set_data(corpus, refer)
        features_vectors = self.vectorgen.run()
       
        print(features_vectors)

Main()