from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

import sys, os

def scriptpath():
    return os.path.dirname(os.path.abspath(__file__))

sys.path.append(scriptpath()+"/Stegano")

buildOptions = dict(packages = ['stegano'], excludes = [])

base = 'Console'

executables = [
    Executable('ma.py', base=base)
]

setup(name='ma',
      version = '0.01',
      description = 'Virtual watermarking',
      options = dict(build_exe = buildOptions),
      executables = executables)
