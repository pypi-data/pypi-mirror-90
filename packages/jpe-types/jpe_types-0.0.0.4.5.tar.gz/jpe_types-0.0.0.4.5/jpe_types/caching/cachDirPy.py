import pickle
import typing
from os.path import join, isdir
from os import mkdir, remove, listdir, rmdir
from shutil import copytree as copyFiles
from shutil import rmtree
from warnings import warn


class NothingAtAll:
    pass

class unpicklableObject(Warning):
    "raised when a value that cant be added to this is added"
    pass

class strCachDir:
    r"""directory with saved items

        a dict with itens and keys saved to file the key must be a string if it isnt keys will be found by the __str__ method
        alsow no \, /, 
        """
    dirFile = None
    lastKey = None
    def __init__(self, inpdict: dict={}):
        """costructor

        create a strCachDir

        @param dir: the inital directory
        @type dir: dict
        """
        self._createDir()
        for key, val in inpdict.items():
            self.__setitem__(key, val)
    
    def _createDir(self):
        "create dir file and save it"
        if not isdir("./cach"):
            mkdir("./cach")
        
        self.dirFile = f"./cach/strDir_{id(self)}"
        if not isdir(self.dirFile):
            mkdir(self.dirFile)
    
    def _isSetup(self):
        "check weather we are setup"
        assert not self.dirFile is None, "setup before this operation"
        assert isdir("./cach"), f"cach may not be deleted"
        assert isdir(self.dirFile), f"nothing in cach may be deleted manualy"

    def _getKeyName(self, key):
        self._isSetup()
        assert hasattr(key, "__str__"), f"key must be str for strCachDir not {type(key)}"
        key = str(key)
        assert not "/" in key, "/ invalid char for key"
        return key

    def __setitem__(self, key, val):
        "add an item"
        key = self._getKeyName(key)

        pickle.dump(val, open(join(self.dirFile, key), "wb"))
        self.lastkey = key

    def __getitem__(self, key):
        key = self._getKeyName(key)

        return pickle.load(open(join(self.dirFile, key), "rb"))
    def get(self, key):
        try:
            return self.__getitem__(key)
        except:
            return
    def pop(self, key):
        val = self.__getitem__(key)
        remove(join(self.dirFile, key))
        return val

    def popitem(self):
        """return the last key"""
        return self.__getitem__(self.lastkey)

    def __str__(self):
        return f"cach dir with keys {self.keys()}"

    def __delitem__(self, key):
        key = self._getKeyName(key)

        remove(join(self.dirFile, key))
    
    def __contains__(self, key):
        key = self._getKeyName(key)
        return key in listdir(self.dirFile)

    def keys(self) -> list:
        return listdir(self.dirFile)
    def __iter__(self):
        return self.keys().__iter__()

    def __copy__(self):
        copied_Dir = strCachDir()
        rmdir(copied_Dir.dirFile)
        copyFiles(self.dirFile, copied_Dir.dirFile)
        return copied_Dir
    
    def __len__(self):
        return len(listdir(self.dirFile))

    def clear(self):
        rmtree(self.dirFile)
        self._createDir()

    def __eq__(self, other):
        if not isinstance(other, (dict, strCachDir)):
            return False
        for myKey, otherKey in zip (self.__iter__(), other):
            if not myKey == otherKey:
                return False
            
            if not self[myKey] == other[otherKey]:
                return False
        return True

    @staticmethod
    def fromkeys(keys):
        return strCachDir(dict.fromkeys(keys))
    
    def items(self)->list:
        out = []
        for key in self:
            out.append((key, self[key]))
        return out

    def setdefault(self, key, val):
        """emm

        The setdefault() method retuns the value of the item with the specified key.
        If the key dose not exist, insert the key, with the specified value, see example below
        
        @param key: the key of the value
        @type key: str
        @param val: the what to set the value to optional
        @type val: any"""
        res = self.get(key)
        if res is None:
            self.__setitem__(key, val)
            res = val
        return res

    def update(self, dic=NothingAtAll, **kwargs) -> None:
        """

        The update() method updates the dictonary with the elements from another dictionary object or from an iterable of key/value paris.

        @param dic: the dict of the value to be returned
        """
        def subscript(**kwargs):
            for key, val in kwargs.items():
                if key == "dic" and val is NothingAtAll:
                    continue
                self[key] = val
            return


        if isinstance(dic, dict):
            return subscript(**dic, **kwargs)
        return subscript(dic=dic, **kwargs) 

    def values(self):
        out = []
        for key in self:
            out.append(self[key])
        return out



