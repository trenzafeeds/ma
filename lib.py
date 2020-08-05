"""
ma
lib.py

Kat Cannon-MacMartin | guthrie@marlboro.edu
"""

# Imports

import sys, os, json

def scriptpath():
    return os.path.dirname(os.path.abspath(__file__))

sys.path.append(scriptpath()+"/Stegano")

from stegano import lsb

# Macros

PRINTORDER = ['id', 'author', 'client', 'platform', 'date'] 

# Class Definitions

class WaterMark:

    def __init__(self, data, custom=False):
        global PRINTORDER
        self.printorder = PRINTORDER
        self.custom = custom
        if data == None: self.data = data
        elif tcheck(data, dict): self.data = data

    def isempty(self):
        return self.data == None

    def insert(self, key, val):
        self.data[key] = val

    def tempinsert(self, tempdata):
        return json.dumps(self.data.update(tempdata))

    def dumpjson(self):
        return json.dumps(self.data)

    def loadjson(self, json_string):
        self.data = json.loads(json_string)

    def printdata(self):
        if self.data == None: print("Watermark is empty.")
        else:
            for field in self.printorder:
                if field in self.data.keys(): pairprint(field, self.data)
            for key in self.data.keys():
                if key not in self.printorder: pairprint(field, self.data)

def write_wm(wm, ifpath, ofpath):
    encoded = lsb.hide(ifpath, wm.dumpjson())
    encoded.save(ofpath)

def read_wm(wm, ifpath):
    """ Returns 2 for STANDARD message read. Returns 3 for CUSTOM message read.
        Returns 1 for NO message read.
    """
    rt = 2
    message = lsb.reveal(ifpath)
    if not message: return 1
    try:
        messsage = json.loads(message)
    except:
        wm.custom = True
        rt = 3
    wm.data = message
    return rt
    

def insert_temps(wm, templist):
    return [ wm.tempinsert(temps) for temps in templist ]

# Utility Functions

def pairprint(key, dictobj):
    print("{}: {}".format(key, dictobj[key]))

def tcheck(var, desired_type):
    if not (type(var) == desired_type):
        err_type_mismatch(var, desired_type)
    else: return True

# Error Messages

def err_type_mismatch(var, desired_type):
    print("Error: Value", str(var), "is of type", type(var),\
          "instead of desired type", desired_type)
    sys.exit(1)
