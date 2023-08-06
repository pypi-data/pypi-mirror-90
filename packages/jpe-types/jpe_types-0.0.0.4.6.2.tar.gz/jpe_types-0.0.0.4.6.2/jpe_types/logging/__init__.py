"""logging

logging module add mainly utils for logThread and @log decorator to log function calles"""

from jpe_types.logging import logUtils, stepLogging
from jpe_types.logging.threadLogging import log, _setupLoggers
from jpe_types.logging.stepLogging import log as stepLog
from os import system
from os.path import dirname, isdir
from shutil import rmtree, copyfile

__all__ = ["setup", "openConfig", "log", "logUtils", "clearLog", "stepLog"]

def setup(runName=None):
    """setup the thread loggers
    
    @param runName: overide to std run name if None default us std values set in loggingConfig.json
    @type runName: str or None"""
    assert isinstance(runName, str) or runName is None, f"runName must be str or None not {type(runName)}"
    setattr(logUtils, "runFile", logUtils.create_newRun(runName))

    _setupLoggers()

def clearLog(file: str="./frameLog")->None:
    """remove log dir aka the same dir as the one passed to log

        @param file: the name of the logg tree
        @type file: str
        """
    if not type(file) is str: raise TypeError(f"param file must be str not {type(file)}")
    if isdir(file):
        rmtree(file)

def openConfig():
    """opens the config.json file
    """
    system(f"{dirname(__file__)}/loggingConfig.json")
    val = "n"
    while val!="y":
        val = input("are you done changing confing ?\n(y/n)")

    copyfile(f"{dirname(__file__)}/loggingConfig.json", 
             f"{dirname(__file__)}/loggingConfig.archive.json")
    