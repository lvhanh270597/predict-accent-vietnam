import os.path
import json
import pickle
from logs import log
from helpers import string as sman

functions = {
    'enterdel' : sman.enterdel,
    'lower' : sman.lower,
    'accentdel' : sman.accentdel
}

def processing(self, description):
    """
    description = {
        name : {
            "path" : /path/to/file,
            "actions" : ["enterdel", ...]
        },
        ...
    }
    """
    data = dict()
    for name, summary in description:
        cur_data = self.load_text(summary["path"])
        for action in summary["actions"]:
            for i, line in enumerate(cur_data):
                cur_data[i] = self.functions[action](line)
        data[name] = cur_data
    return data

def save_text(data, filename, type="w"):
    with open(filename, type) as f:
        f.write("\n".join(data))
    f.close()

def save_data_point(data, filename, type="w"):
    with open(filename, type) as f:
        for X, y in data:
            f.write("%s\t%s\n" % (X, y))
    f.close()

def load_data_point(filename):
    data_points = []
    myfile = open(filename)
    for line in myfile:
        line = line.replace("\n", "")
        X, y = line.split("\t")
        data_points.append(tuple([X, y]))
    return data_points

def check_file(fpath):
    if not os.path.isfile(fpath):
        log.write_log("The file name %s does not exist" % fpath)
        return False
    return True

def check_folder(folder_path):
    if not os.path.isdir(folder_path):
        log.write_log("The folder name %s does not exist!" % folder_path)
        return False
    return True

def load_text(fname):
    data = []
    if check_file(fname):
        with open(fname, "r") as myfile:
            data = myfile.readlines()
    return data

def load_json(fpath):
    data = []
    if check_file(fpath):
        with open(fpath) as myfile:
            data = json.load(myfile)
    return data

def save_json(data, fpath):
    with open(fpath) as myfile:
        json.dump(data, myfile)

def get_filename_ext(filename):
    names = filename.split(".")
    return ("".join(names[:-1]), "." + names[-1])

def save_object(data, filename):
    pickle.dump(data, open(filename, 'wb'))

def load_object(filename):
    return pickle.load(open(filename, 'rb'))

def make_dir(folder_path):
    os.mkdir(folder_path)

def join_path(start, list_items):
    if type(list_items) == str:
        list_items = [list_items]
    add = "/%s" % "/".join(list_items)
    return start + add

