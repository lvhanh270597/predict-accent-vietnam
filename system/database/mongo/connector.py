import pymongo
from config.config import config

class AccessDatabase:

    def __init__(self):
        self.config = config["database"]
        self.accessor = pymongo.MongoClient("mongodb://%s:%s/" % (self.config["host"], self.config["port"]))
        self.mydb = self.accessor[self.config["dbname"]]

    def write(self, colName, data):
        print("Size of data: %d" % len(data))
        mycol = self.mydb[colName]
        items = mycol.insert_many(data).inserted_ids
        print("Wrote %d/%d successfully!" % (len(items), len(data)))

    def find(self, colName, condition={}, fields=None):
        mycol = self.mydb[colName]
        data = mycol.find(condition, fields)
        return data

    def test(self, colName):
        for item in self.find(colName):
            print(item)

class PushData:
    
    def __init__(self, path):
        self.path = path
        self.datalines = open(path).readlines()
        self.datalines = [
            sen.replace("\n", "") 
            for sen in self.datalines[-5:]
        ]
    
    def writeRaw(self):
        db = AccessDatabase()
        for i, text in enumerate(self.datalines):
            self.datalines[i] = {
                "text" : text
            }
        db.write('raw', self.datalines)
    
    def test(self):
        print(self.datalines[-5:])

# def main():
#     pusher = PushData("./data/VNTQcorpus-small")
#     # pusher.test()
#     pusher.writeRaw()

# main()