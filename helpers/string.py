from data_structures.sentence import *
from logs import log
import pickle, os
from datetime import datetime

def get_ngram(_list, n):
    data = []
    nsize = len(_list)
    if n > nsize:
        return []
    for i in range(nsize - n + 1):
        data.append(_list[i : i + n])
    return data

def get_hash_ngram(_list, n, max_v):
    data = get_ngram(_list, n)
    res = []
    for item in data:
        value = 0
        for i in item:
            value = value * max_v + i
        res.append(value)
    return res

def enterdel(string):
    return string.replace("\n", "")
def lower(string):
    return string.lower()
def get_unique_words(list_of_sentences):
    words = set()
    for sentence in list_of_sentences:
        words.update(set(sentence.split()))
    return list(words)

def accentdel(sentence):
    return Sentence().remove_accents(sentence)

def load_text(fname):
    if not os.path.isfile(fname):
        log.write_log("The file name %s does not exist" % fname)
        return []
    with open(fname, "r") as myfile:
        data = myfile.readlines()
    return data

def get_current_time():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
    return date_time
