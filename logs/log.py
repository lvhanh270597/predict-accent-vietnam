from time import gmtime, strftime
from config.config import *

def write_log(string):
    with open(LOG_PATH, "a") as myfile:
        datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        myfile.write(datetime+ ": " + string + "\n")
def write_alog(string):
    with open(ACC_PATH, "a") as myfile:
        datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        myfile.write(datetime+ ": " + string + "\n")