"""compleatly logg function execution

    log function execution line by line
    its threadsafe btw
    """

import sys, time
from threading import current_thread, get_ident, Thread
import traceback, typing
from os.path import samefile, isdir, join
from os import mkdir, listdir
from pathlib import Path
from jpe_types.conversions.intager import baseN
from pickle import dump, load
from tkinter import Tk, Button, Text, END, Label, Scale, HORIZONTAL
from typing import NewType
from inspect import getsource, getsourcelines, getsourcefile
from shutil import rmtree


__all__ = ["SetTrace", "FuncFrames", "loggers", "log", "replay"]
"emmm"

def encriptName(value: int)->str:
    """encript frame id to save 

        it converts a value int to base 36 
        """
    #return baseN(value, 97, numerals="1234567890'^qwertzuiopasdfghjkl$yxcvbnm,-+ç%&/()=`QWERTZUIOP!ASDFGHJKLYXCVBNM;:_<>¦@#°§¬|¢}]~[{£¨")
    return baseN(value, 36, numerals="1234567890qwertzuiopasdfghjklyxcvbnm")
    #return hex(value)

class SetTrace(list):
    """internal
    with SetTrace(monitor):

    the Tracer used to combine everything hapeening in a certain Thread.
    """
    funcCode=""
    lastFrame = None
    startFile = None
    def __init__(self, func, name, tb=[],  directory ="./frameLog"):
        """constructor

            create the listener witch will call func at every log call made by sys
            the name is equivelent to the directory name to log to

            @param func: the logging function
            @type func: function

            @param name: the name of the Thread to that is being loged or more accuratly the name of the subdir in dir to log to
            @type name: str

            @param tb: the starting tb of the log
            @type tb: list<str>

            @param directory: the superdir to log to defualts to ./frameLog
            @type direcroy: os pathname
            """

        assert hasattr(func, "__call__"), f"param func must be callable"
        self.func = func(self)
        "the tracing function"
        assert hasattr(name, "__str__"), f"param name must be str not {type(name)}"
        self.name = str(name)
        "the name of the thread it runs on"
        self._add_active = False
        "weather or not a new function trace is added"
        self._active = False
        "weather its acrive"
        self._name = current_thread().name
        "name of the thread that started it [depricated]"
        self.key = 0
        "the howmaniath log we loged cant be larger than 36**31"
        if not hasattr(tb, "__iter__"): raise TypeError(f"param tb must be ")
        list.__init__(self, tb)
        #self.mainStack = mainStack

        if not hasattr(directory, "__str__"): raise TypeError(f"param directory must be str not {type(directory)}")
        self._dir = directory
        """the directory to log to
        may not be changed"""

        if not isdir(self._dir):
            mkdir(self._dir)
        
        if not isdir(f"{self._dir}/{self._name}"):
            mkdir(f"{self._dir}/{self._name}")
    
    def __str__(self):
        return f"debug Tracer with tb {list.__str__(self)}"
    
    def append(self, val)->None: 
        """append value

        append the value to the tracers tb list if its active"""
        if not samefile(str(val[-1])[19:str(val[-1]).index(",")], Path(__file__)):
            if self._add_active and not val in self:
                list.append(self, self._formatTb(val))
            self._add_active = False
    
    def __contains__(self, other):
        """weather a tb schould be loged
        """
        return list.__contains__(self, self._formatTb(other))
    
    @staticmethod
    def _formatTb(val):
        "get file location"
        tb = []
        
        for x in val:
            x = str(x)
            kommaPos = x.index(",")
            y = x[kommaPos+5:]
            inPos = y.index("in")
            tb.append(x[19:kommaPos] + y[inPos+2:])
        return tb

    def start(self):
        "start the log"
        if not self._active:
            self._active = True
            sys.settrace(self.func)
    def __enter__(self):
        return self
    def __exit__(self, ext_type, exc_value, traceback):
        self._active = False
        sys.settrace(None)
        # http://effbot.org/zone/python-with-statement.htm
        # When __exit__ returns True, the exception is swallowed.
        # When __exit__ returns False, the exception is reraised.
        # This catches Sentinel, and lets other errors through
        # return isinstance(exc_value, Exception)

class FuncFrames(list):
    """the current Frame
    
        a class used to extract and save data from the sys frame """
    def __init__(self, frame, event, arg, Tracer):
        """constructor

            creatae the frame and extract data

            @param frame: the sys frame to extract from
                            !no assersions
            @type frame: sts.Frame

            @param event: what type of event hapend
            @type event: str

            @param args: the arg param passed by sys
            @type arg: ???

            @param Trace: the trace that this frame belogs to 
            @type Trace: SetTrace class defined here
            """
        assert type(event) is str, f"param event must be str"

        def getLocals():
            res = {}
            for key, val in frame.f_locals.items():
                if hasattr(val, "__str__"):
                    res[key] = str(val)
            return res


        self.local: dict = getLocals()
        self.event = event
        self.arg   = arg
        self.func = frame.f_code.co_name
        self.funcCode = getsource(frame.f_code)
        self.lineNumber = frame.f_lineno - getsourcelines(frame.f_code)[1]+1
        self.startedThreads = []
        self.endedThreads = []

        self.key   = Tracer.key
        self.trace = Tracer
        Tracer.key += 1
        Tracer.lastFrame = self
    
    def __str__(self):return str(self.startedThreads)
    
    def save(self):
        "save the state"
        dump(self, open(f"{self.trace._dir}/{self.trace._name}/{encriptName(self.key)}.plog", "wb"))
    
    def __getstate__(self):
        value={"local": self.local,
                "event": self.event,
                "arg": str(self.arg) if hasattr(self.arg, "__str__") else "sry could not str convert",
                "func": self.func,
                "funcCode": self.funcCode,
                "lineNumber": self.lineNumber,
                "startedThreads": self.startedThreads,
                "endedThreads": self.endedThreads}
        
        return value
            
    def __setstate__(self, state):
        def load(local, event, arg, func, funcCode, lineNumber, startedThreads, endedThreads):
            self.local = local
            self.event = event
            self.arg = arg
            self.func = func
            self.funcCode = funcCode
            self.lineNumber = lineNumber
            self.startedThreads = startedThreads
            self.endedThreads = endedThreads
        load(**state)
funcFramesType = NewType("FuncFrames", FuncFrames)
"typing type of FuncFrames"

def execLog(Trace: typing.NewType("Trace", SetTrace)):
    """logging function used ty log decorator
    
        purly internal"""
    def monitor(frame, event, arg):
        if Trace._active:
            tb = traceback.extract_stack(f=frame)
            if len(tb) == 0:
                return
            if samefile(str(tb[-1])[19:str(tb[-1]).index(",")], Path(__file__)):
                return
            Trace.append(tb)
            if tb in Trace:
                if event == "line" or event == "return":
                    saveFrame = FuncFrames(frame, event, arg, Trace)
                    saveFrame.save()

                    
        return monitor
    return monitor

loggers: typing.Dict[str, typing.Dict[Thread, SetTrace]] = {}
"""dict of loggers

    a dict conaining loggers by save file and thread it contains SetTrace's

    @type: dict<str, dict<Thread, SetTrace>>
    """
logFile: typing.Dict[Thread, str] = {}
"""dict of files by THread

    the files in witch the log is saved by Thread

    @type: dict<Thread, str>
    """

def log(directory: str="./frameLog"):
    """logging decorator

        log the functions this relates to

        @param directory: the directory to save to
        @type directory: str
        """
    def sublog(function):
        def newLogger(args, kwargs):
            "if logger dosent exist create a new one"
            with SetTrace(execLog, current_thread().name, directory=directory) as Trace:
                #add logger dir
                if not directory in loggers:
                    loggers[directory] = {}

                loggers[directory][current_thread()] = Trace
                Trace.startFile = getsourcefile(function)
                return mainLog(Trace, args, kwargs, function) 
     
        def reuseLogger(args, kwargs):
            "if logger existr reuse it"
            Trace = loggers[directory][current_thread()]
            return mainLog(Trace, args, kwargs, function)       
        def mainLog(Trace, args, kwargs, func):
            "run function"
            logFile[current_thread()] = directory
            Trace.start()
            Trace._add_active = True
            ret = func(*args, **kwargs)
            return ret
            
        def main(*args, **kwargs):
            "fingure out witch function schuld be used"
            if directory in loggers:
                if current_thread() in loggers[directory]: 
                    return reuseLogger(args, kwargs)
            return newLogger(args, kwargs)
            

        return main
    return sublog






class replay(Tk):
    """replay a log file

        replay logg file
        """
    def __init__(self, file: str="./frameLog", name: str="MainThread", baseTime: float=10, master=None):
        """constructor

            @param file: the dir in witch stuff got loged
            @type file: str
            @param name: the thread name to be used
            @type name: str
            @param baseTime: the max time to wait beween auto steps
            @type baseTime: float
            @param master: the log of the thread that initiated it
            @type master: replay
            """
        assert isinstance(file, str), f"param file must be str not {type(file)}"
        self._dir:str = file
        "the dir of the log"
        assert isinstance(name, str), f"param name must be str not {type(name)}"
        self.name:str = name
        "the threads name"
        Tk.__init__(self)
        self.baseTime: float = baseTime
        "max time betwean steps"
        self.master = self if master is None else master
        self.kids: list = [self]
        "every instance of reply with this as tis master"
        self.kidThreads = {}
        "the threads of all threads used by master"

        self._autoStep=False

        self.key: int = 0

        self._createTk()
    
    def autoStep(self):
        while self._autoStep:
            if self.stepThrew.get()==0:
                continue

            time.sleep(abs(self.baseTime/self.stepThrew.get()))
            for element in self.kids:
                if self.stepThrew.get()>0:
                    element.next()
                else:
                    element.prev()

    def toggleAutoSep(self):
        params = {True: "stop autostep",
                  False:"start autostep"}
        self.master._autoStep = not self.master._autoStep
        for element in self.master.kids:
            element.autoStepThrewCode.config(text=params[self.master._autoStep])
        if self.master._autoStep:
            Thread(target=self.master.autoStep,
                   daemon=True,
                   name="stepThrewCode").start()

    def _createTk(self):
        self.codeText = Text(self) 
        self.codeText.pack()

        self.var_label = Text(self)
        self.var_label.pack()
        self.title(f"Thread {self.name}")

        self.nextButton = Button(self,
                                 command=self.next,
                                 text="next")
        self.nextButton.pack(side="bottom")

        self.prevButton = Button(self,
                                 command=self.prev,
                                 text="last")
        self.prevButton.pack(side="bottom")

        if self.master is self:
            self.stepThrew = Scale(self, from_=-100, to=100, orient=HORIZONTAL)
            self.stepThrew.pack()

        self.autoStepThrewCode = Button(self, command=self.master.toggleAutoSep, text="start autostep")
        self.autoStepThrewCode.pack()

        self.show()
    
    def show(self) -> None:
        "show the log state"
        data: funcFramesType = load(open(f"{self._dir}/{self.name}/{encriptName(self.key)}.plog", "rb"))

        def create_Thread(threadName):
            newThreadLog = replay(self._dir, threadName, master=self.master)
            self.master.kids.append(newThreadLog)
            self.master.kidThreads[threadName] = newThreadLog
            newThreadLog.mainloop()

        for threadName in data.startedThreads:
            if isdir(join(self._dir, threadName)):
                tlogExe = Thread(target=create_Thread,
                                args=(threadName,),
                                daemon=True,
                                name=f"replay {threadName}")
                tlogExe.start()
        
        for removedThreads in data.endedThreads:
            if removedThreads in self.master.kidThreads:
                self.master.kidThreads[removedThreads].destroy()
            

        self.var_label.delete("1.0", END)
        self.codeText. delete("1.0", END)
        for key, val in data.local.items():
            self.var_label.insert(END, f"{key} is {val}\n")
        
        if data.event == "return":
            self.var_label.insert(END, f"return Value is {data.arg}")


        self.codeText.insert(END, data.funcCode)
        self.codeText.tag_add("currentLine", f"{data.lineNumber}.0", f"{data.lineNumber}.end")
        self.codeText.tag_config("currentLine", background="yellow", foreground="black")


    def __iadd__(self, val):
        assert isinstance(val, int), f"cant use non int stepsize"
        if self.key+val < 0: 
            self.key=0
        elif f"{encriptName(self.key+val)}.plog" in listdir(f"{self._dir}/{self.name}"):
            self.key += val
        self.show()
    def __isub__(self, val):
        self.__iadd__(-val)
    def next(self): self.__iadd__(1)
    def prev(self): self.__isub__(1)

