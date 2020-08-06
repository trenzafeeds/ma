"""
ma.py
ma

Kat Cannon-MacMartin | guthrie@marlboro.edu
"""

V = 'v0.01'

import sys
from lib import *

def cprinter(code):
    global V
    codes = {
        'intro' : "Welcome to ma {}.".format(V),
        'repl' : "Press 'n' to create a new watermark template.\nPress 'w' to \
apply a watermark to a single image.\nPress 'b' for a batch job.\nPress 'h' for \
help.\nPress 'q' to quit.",
        'author' : "Input the creator's name or identifier: ",
        'client' : "Next, input the specific client's name or identifier \
(leave blank if not applicable): ",
        'platform' : "Enter the name of the platform on which this content will \
be distributed: "
        }
    return codes[code]

def create_template(args=None):
    wm = WaterMark(None)
    print("Creating a new watermark template.")
    for key in PRINTORDER:
        if key not in ['id', 'date']:
            wm.insert(key, input(cprinter(key)))
    print(wm.dumpjson())

def repl(args=None):
    print(cprinter('repl'))
    cmd = input('> ')
    # 'visible' commands
    if cmd in ['n', 'new']:
        create_template()
    elif cmd == 'w':
        pass
    elif cmd == 'b':
        pass
    elif cmd in ['h', 'help']:
        pass
    elif cmd in ['q', 'exit', 'quit']:
        return 2
    # 'hidden' commands
    elif cmd in ['c', 'clear']:
        clear()
    else:
        err_invalid_command(cmd)
    return 0

def cli(args):
    global PRINTORDER
    wm = WaterMark(None)
    print(cprinter('intro'))
    while repl() != 2:
        pass
    return 0

def main(argv):
    return cli(argv)

if __name__=='__main__':
    main(sys.argv[1:])
