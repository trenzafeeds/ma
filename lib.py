"""
ma
lib.py

Kat Cannon-MacMartin | guthrie@marlboro.edu
"""

# Imports

import sys, os, json
from datetime import date

def scriptpath():
    return os.path.dirname(os.path.abspath(__file__))

sys.path.append(scriptpath()+"/Stegano")

from stegano import lsb

# Macros

PRINTORDER = ['id', 'author', 'client', 'platform', 'date']
FILETYPES = ['.jpg', '.jpeg', '.png']
DATE = date.today()
TEMPPATH = scriptpath() + "/config/templates"

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
        if self.data == None: self.data = {}
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
            for field in self.data.keys():
                if field not in self.printorder: pairprint(field, self.data)

def write_wm(wm, ifpath, ofpath):
    encoded = lsb.hide(ifpath, wm.dumpjson())
    encoded.save(ofpath)
    return 0

def read_wm(wm, ifpath):
    """ Returns 2 for STANDARD message read. Returns 3 for CUSTOM message read.
        Returns 1 for NO message read.
    """
    rt = 2
    message = lsb.reveal(ifpath)
    if not message: return 1
    try:
        message = json.loads(message)
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

def clear():
    if os.name == 'nt': _ = os.system('cls')
    else: _ = os.system('clear')

def read_templates(path):
    with open(path, 'r') as f:
        try: return json.loads(f.read())
        except:
            err_doc_read("templates file")
            return {}

def write_templates(path, templates):
    with open(path, 'w') as f:
        try: f.write(json.dumps(templates))
        except:
            err_doc_read("templates file")
            return 1
        return 0

def file_exists(path):
    if os.path.exists(path): return True
    else: return err_file_nexist(path)

def file_type(path):
    global FILETYPES
    if os.path.splitext(path)[1] in FILETYPES: return True
    else: return err_file_type_nsupported(os.path.splitext(path)[1])

def nfile_direxists(path):
    if os.path.split(path)[0] == '': return True
    else:
        if os.path.isdir(os.path.split(path)[0]): return True
        else: return err_invalid_dir(path)
    
# Error Messages

def err_type_mismatch(var, desired_type):
    print("Error: Value", str(var), "is of type", type(var),\
          "instead of desired type", desired_type)
    sys.exit(1)

def err_invalid_command(command):
    print("Error: {} is not a valid command. Press 'h' for more help."\
          .format(command))
    return False

def err_doc_read(id):
    print("Error reading {}. Some functionality may not be available."\
          .format(id))
    return False

def err_file_nexist(path):
    print("Error: File '{}' does not exist.".format(path))
    return False

def err_file_type_nsupported(ext):
    print("Error: '{}' files are not supported at this time.".format(ext))
    return False

def err_invalid_dir(path):
    print("Error: the file {} does not have a valid directory path.".format(path))
