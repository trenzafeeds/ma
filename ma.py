"""
ma
ma.py

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
be distributed: ",
        'template' : "Enter a name for the template to save: "
        }
    return codes[code]

def create_template():
    wm = WaterMark(None)
    print("Creating a new watermark template.")
    for key in PRINTORDER:
        if key not in ['id', 'date']:
            wm.insert(key, input(cprinter(key)))
    return wm

def create_save_template(templates):
    global TEMPPATH
    wm = create_template()
    wm.insert('template', input(cprinter('template')))
    templates[wm.data['template']] = wm.data
    return write_templates(TEMPPATH, templates)

def list_templates():
    global TEMPPATH
    print("  ----  ")
    print("Currently saved templates:")
    templates = read_templates(TEMPPATH)
    for template in templates.keys():
        print("  - {}".format(template))
    print("  ----  ")
    return 0

def get_template(templates):
    template = 0
    while template == 0:
        name = input(\
                "Input a template name or leave blank to create a new watermark: ")
        if name == '': return 1
        elif name in templates.keys(): template = templates[name]
        else: print("No saved template with title '{}'. Please try again."\
                    .format(name))
    return WaterMark(template)

def apply_wm_cli():
    global TEMPPATH
    t = get_template(read_templates(TEMPPATH))
    if t == 1: t = create_template()
    while True:
        fpath = input("Enter the path to the target file: ")
        if (file_exists(fpath) and file_type(fpath)): break
    while True:
        opath = input("Enter a path to save the watermarked image (leave blank \
to replace the target file): ")
        if opath == '':
            opath = fpath
            break
        elif nfile_exists(path):
            break
    return write_wm(t, fpath, opath)

def repl():
    global TEMPPATH
    print(cprinter('repl'))
    cmd = input('> ')
    # 'visible' commands
    if cmd in ['n', 'new']:
        templates = read_templates(TEMPPATH)
        return create_template(templates)
    elif cmd == 'w':
        apply_wm_cli()
    elif cmd == 'b':
        print("Batch jobs enabled soon :)")
    elif cmd in ['h', 'help']:
        print("Help section coming soon :)")
    elif cmd in ['q', 'exit', 'quit']:
        return 2
    # 'hidden' commands
    elif cmd in ['c', 'clear']:
        clear()
    elif cmd in ['l', 'list']:
        list_templates()
    else:
        err_invalid_command(cmd)
    return 0

def cli(args):
    print(cprinter('intro'))
    while repl() != 2:
        pass
    return 0

def main(argv):
    return cli(argv)

if __name__=='__main__':
    main(sys.argv[1:])
