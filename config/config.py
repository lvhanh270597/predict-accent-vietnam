ENV = dict()

# SET FOR ENVIRONMENT
ENV["STA"] = "DEV" # OR RELEASE

# SET FOR DATA
ENV["BASE_DIR"] = "./"
ENV["DATA_DIR"] = "./data"
ENV["RAW_PATH"] = "%s/%s" % (ENV["DATA_DIR"], "raw")
ENV["BEA_PATH"] = "%s/%s" % (ENV["DATA_DIR"], "beautiful")
ENV["LEA_PATH"] = "%s/%s" % (ENV["DATA_DIR"], "learning")
ENV["WOR_PATH"] = "%s/%s" % (ENV["DATA_DIR"], "words")
ENV["VOCAB_PATH"] = "%s/%s" % (ENV["DATA_DIR"], "vocabularies")
ENV["MOD_PATH"] = "%s/%s" % (ENV["DATA_DIR"], "models")
ENV["LISTNAMES"] = "%s/%s" % (ENV["DATA_DIR"], "listnames.txt")
ENV["LISTWORDS"] = "%s/%s" % (ENV["DATA_DIR"], "listwords.txt")
ENV["ONEDIFF"] = "%s/%s" % (ENV["DATA_DIR"], "onediff.txt")
ENV["REFER"] = "%s/%s" % (ENV["DATA_DIR"], "refer_dict.json")
ENV["COUNT"] = "%s/%s" % (ENV["DATA_DIR"], "count.txt")
ENV["DICTIONARY"] =  "%s/%s" % (ENV["DATA_DIR"], "Viet74K.txt")

# SET LOG DATA
ENV["LOG_ERR"] = "./logs/errors"
ENV["LOG_ACC"] = './logs/access'
ENV["LOG_DIR"] = "./logs/"

# SET FOR MODELS
ENV["WINDOW_SIZE"] = 5
ENV["MAX_WORDS"] = 5
ENV["MAX_SYLLABLE"] = 5
ENV["NGRAMS"] = [1]
ENV["REMOVE_VECTOR_MODEL"] = True

# SET SAVE & LOAD DATA
ENV["SAVE_AFTER"] = 20

# SET OTHER
ENV["DELIMITER"] = "\t"