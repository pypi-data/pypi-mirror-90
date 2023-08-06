"""cach dir 

see chach dir"""
from jpe_types.caching.cachDirPy import strCachDir
from shutil import rmtree
from os.path import isdir

__all__ = ["strCachDir", "clearCach"]

def clearCach():
    "cleat data cach"
    if isdir("./cach"):
        rmtree("./cach")