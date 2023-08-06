import os, typing
from warnings import warn
try: 
    from jpe_types.utils.Optimizations.subScripts import CppfindFalsInFile
except ImportError:
    warn("jpe_utils.utils.Scanning Cython lod Failure")
    import jpe_types.setup
    jpe_types.setup.run()
    try:
        from jpe_types.utils.Optimizations.subScripts import CppfindFalsInFile
    except:
        CppfindFalsInFile = None
        
class filePosition:
    """the location of a val in files

        the position in the a file set as file with line number created by search algorythem
    """
    def __init__(self, file: str, line: int, doAssersions: bool=True):
        """constructor

            create a new instance of the filePosition containing file and line

            @param file: the file in witch the val was found
            @type file: os path string of a file

            @param line: the line in witch the value was found
            @type line: int

            @param doAssesions: weather or not to assert values
            """

        if doAssersions:
            assert isinstance(file, str), f"file must be str not{type(file)}"
            assert os.path.isfile(file), f"file must be a valid file, {file} is not a valid path"
            assert isinstance(line, int), f"line must be int not {type(line)}"

        self.file = file
        "the fill in witch a solution was found"

        self.line = line   
        "the line number the solution was found in"

    def __str__(self) -> str:
        return f"in file {self.file} at line {self.line}"

    __repr__ = __str__
filePositionType = typing.NewType("filePosition", filePosition)

class GenralFilesPostions(list):
    """the sumary of positions of filePositions

        a subclass of list with all its functionality howerver it adds the posibility to 
            - get the files in witch calles accured as set
    """
    def getFiles(self) -> set:
        """get all the files a result was found in

            @return: set of the paths of the files
        """
        res = set()
        for pos in self:
            res.add(pos.file)
        return res
    
    def __str__(self):
        res = "found solutions here:"
        for value in self:
            res +=  "\n" + value.__str__()
        return res
    def getFilePoses(self):
        """get all the files with line number a result was found in

            @return: set of tuples(file path, line number)
        """
        res = set()
        for pos in self:
            res.add((pos.file, pos.line))
        return res
GenralFilesPostionsType = typing.NewType("GenralFilesPostions", GenralFilesPostions)

def scanLog(val:str ,root: str="./log") -> GenralFilesPostionsType:
    """ask theo
    """
    positions = GenralFilesPostions()
    for path in os.listdir(path=root):
        
        new_path = os.path.join(root, path)
        if os.path.isdir(new_path):
            positions += scanLog(val, new_path)
        else:
            if not CppfindFalsInFile is None:
                positions += cyScanLogFile(val, new_path)
            else:
                positions += pyScanLogFile(val, new_path)
    
    return positions

def pyScanLogFile(val: str, path: str) -> GenralFilesPostionsType:
    "subrutine dont use"
    
    positions = GenralFilesPostions()
    with open(path) as f:
        logFile = f.readlines()
        for lineNumber, line in enumerate(logFile):
            if val in line:
                positions.append(filePosition(path, lineNumber))
    
    return positions
def cyScanLogFile(val: str, path: str) -> GenralFilesPostionsType:
    "subrutine dont use"
    positions = GenralFilesPostions()

    posses = CppfindFalsInFile(path.encode(), val.encode())
    for val in posses:
        positions.append(filePosition(path, val))
    
    return positions
