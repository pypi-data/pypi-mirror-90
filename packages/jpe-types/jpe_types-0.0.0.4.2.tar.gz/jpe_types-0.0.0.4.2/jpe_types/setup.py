"setup script"

import json
from os.path import dirname, join
from os import system
from sys import executable

def run():
    #update logg utils json file

    path = dirname(__file__)
    #print( f"{executable} {join(path, u"utils/Optimizations/build.py")}")
    try:
        import jpe_types.utils.Optimizations.subScripts
    except ImportError:
        buildScript_path = join(path, "utils", "Optimizations", "build.py")
        outputScriptPath = join(path, "utils", "Optimizations")
        system(f"{executable} {buildScript_path} build_ext --build-lib {outputScriptPath}")

if __name__ == "__main__":
    run()