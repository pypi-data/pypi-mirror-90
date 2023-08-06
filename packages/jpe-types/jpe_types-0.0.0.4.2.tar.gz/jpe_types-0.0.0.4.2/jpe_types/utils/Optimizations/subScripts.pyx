# distutils: language = c++

from libcpp.string cimport string as cstr
from libcpp.list cimport list as clist


cdef extern from "jpe_typeUtilsExtentions/FileScanner.h":
    clist[int] findRefrences(cstr, cstr)

cpdef list[int] CppfindFalsInFile(bytes fileName_py, bytes val_py):

    cdef cstr fileName = fileName_py
    cdef cstr val = val_py

    cdef clist[int] res = findRefrences(fileName, val)
    return res

