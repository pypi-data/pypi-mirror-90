"""multiprocessing enchanments

adds Processes that return values as well as Process safe printing

"""

from multiprocessing.queues import Queue as mpQueue
from multiprocessing import Process as mpProcess, Pipe as mpPipe, Manager as mpManager
from multiprocessing.connection import Connection as mpConnection
from multiprocessing.context import BaseContext as mpBaseContext, _default_context
from multiprocessing.managers import SyncManager as mpSyncManager, Namespace as mpNamespace, NamespaceProxy as mpNamespaceProxy
from threading import Thread
from traceback import format_exc
import typing
from pickle import load, dump
from os import remove
from time import sleep


class printer():
    """printStatment class that can be used in all processes
    """
    class printer_queue(mpQueue):
        "the que to put all requests in"
        def __call__(self, *args, **kwargs):
            recver, sender = mpPipe(False)
            self.put_nowait((args, kwargs, sender))
            recver.recv()

    _print_config = {}
    _active = True
    def __init__(self, *args, **kwargs):
        """constructor
        
        see https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queues"""
        self._internal_queue = printer.printer_queue(ctx=_default_context.get_context())
        self._printer = Thread(target=self._print,
                                daemon=True,
                                name="jpe_types.mp.intern.printer")
        self._printer.start() 
    
    def __getstate__(self):
        return self._internal_queue.__getstate__()  
    
    def __setstet(self, state):
        self._internal_queue.__setstate__(state)
    
    def _print(self):
        while self._active:
            try:
                args, kwargs, sender = self._internal_queue.get(False)
                py_oldPrint(*args, **kwargs)
                sender.send(None)
            except:
                pass
    
    def close(self):
        """nothing more to print

            Indicate that no more data will be printed by the current process. The background thread will quit once it has flushed all buffered data to the pipe. This is called automatically when the queue is garbage collected.
        """
        self._internal_queue.close()
Print = printer()._internal_queue
"""print function

the function to print in withc will add everything to a queue witch is then read by a thread of the printer
"""
__builtins__["py_oldPrint"] = __builtins__["print"]
__builtins__["print"] = Print



class context(mpBaseContext):
    "just a placeholder"
    pass

class Process(mpProcess):
    """Process objects represent activity that is run in a separate process. The Process class has equivalents of all the methods of threading.Thread.

        The constructor should always be called with keyword arguments. group should always be None; it exists solely for compatibility with threading.Thread. target is the callable object to be invoked by the run() method. It defaults to None, meaning nothing is called. name is the process name (see name for more details). args is the argument tuple for the target invocation. kwargs is a dictionary of keyword arguments for the target invocation. If provided, the keyword-only daemon argument sets the process daemon flag to True or False. If None (the default), this flag will be inherited from the creating process.

        By default, no arguments are passed to target.

        If a subclass overrides the constructor, it must make sure it invokes the base class constructor (Process.__init__()) before doing anything else to the process."""
    def __init__(self, group=None, target=None, name: str=None, args: tuple=(), kwargs: typing.Dict[str, typing.Any]={}, *, daemon: bool=False):
        """constructor

            @param groop: None:
            @param target: the function to be called
            @type target: callable
            @param name: the name of the 
            @type name: str
            @param args: the arguments of the function
            @type args: tupple
            @param kwargs: the keyword arguments of the function
            @type kwargs: dict
            @param deamon: if the Process is a deamon Process
            @type deamon: bool"""
        if not hasattr(target, "__call__") or target is None: raise TypeError(f"target must be callable or None not {type(target)}")
        if not type(name) or name is None is str: raise TypeError(f"param name must be str not {type(name)}")
        if not type(args) is tuple: raise TypeError(f"param args must be tuple not {type(args)}")
        if not type(kwargs) is dict: raise TypeError(f"param kwargs must be dict not {type(kwargs)}")
        if not type(daemon) is bool or daemon is None: raise TypeError(f"param deamon must be bool not {type(daemon)}")
        self.dataRecever, dataSender = mpPipe(duplex=False)
        mpProcess.__init__(self, group=group, target=target, name=name, args=(Print, dataSender, *args), kwargs=kwargs, daemon=daemon)


    def run(self, *a, **k):
        """internal run function

            run the function and save the return val
            the execute function replaces what is by run in std implementation"""
        self.print: printer.printer_queue = self._args[0]
        dataSender: mpConnection = self._args[1]
        __builtins__["print"] = self.print
        try:
            #this schould be rewriten
            _output_val = self.execute(*self._args[2:], **self._kwargs)
            dataSender.send(_output_val)
        except:
            self.print(f"{format_exc()}in Process {self._name}")
    
    def execute(self, *args, **kwargs):
        """Method to be run in sub-process; can be overridden in sub-class"""
        if self._target:
            return self._target(*args, **kwargs)
    
    def join(self, timeout=None):
        """join Process
        
            If the optional argument timeout is None (the default), the method blocks until the process whose join() method is called terminates. If timeout is a positive number, it blocks at most timeout seconds. Note that the method returns None if its process terminates or if the method times out. Check the process’s exitcode to determine if it terminated.
            A process can be joined many times.
            A process cannot join itself because this would cause a deadlock. It is an error to attempt to join a process before it has been started."""

        mpProcess.join(self, timeout=timeout)
        data = self.dataRecever.recv()
        self.dataRecever.close()
        return data
        
class classScharer:
    """namespace to share a class

    not curently working
    """
    def __init__(self, manager=None):
        self._nameSpace = manager.Namespace()
    
    def __delattr__(self, key):
        self._nameSpace.__delattr__(key)
    
    def __setattr__(self, key, val):
        self._nameSpace.__setattr__(key, val)
    
    def __getattr__(self, key):
        return self._nameSpace.__getattr__(key)

