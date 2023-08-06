"setup script"

import json
from os.path import dirname, join
from os import system
from threading import Thread
from sys import executable

def run():
    #update logg utils json file

    path = dirname(__file__)
    #print( f"{executable} {join(path, u"utils/Optimizations/build.py")}")
    buildScript_path = join(path, "utils", "Optimizations", "build.py")
    outputScriptPath = join(path, "utils", "Optimizations")
    import os
    for file in [f for f in os.listdir(dirname(executable)) if f.endswith('.exe')]:
        if file != "Removeepydoc.exe":
            try:
                    system(f"{join(dirname(executable), file)} {buildScript_path} build_ext --build-lib {outputScriptPath}",)
            except:
                pass

if __name__ == "__main__":
    run()