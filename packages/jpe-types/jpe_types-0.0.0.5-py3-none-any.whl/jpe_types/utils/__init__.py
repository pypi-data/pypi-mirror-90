"utils module"

from jpe_types.utils.copy import copy
from jpe_types.utils.logScanner import filePosition,GenralFilesPostions,scanLog

def fallback(last, *fallbacks):
    """decorator for fallback functions

        if the current function retuns an error last will be executed anything after that will be used as a fallback for the one before
        if the last one retuns an error the last error is returned
        @param last: pyobject with __call__ method
        """
    def doWrap(currentFunc):
        def fallback_wraper(*args, **kwargs):
            try:
                return currentFunc(*args, **kwargs)
            except Exception as e:
                if len(fallbacks) == 0:
                    raise e
                return fallback(*fallbacks)(last)(*args, **kwargs)
        return fallback_wraper
    return doWrap
            
        
