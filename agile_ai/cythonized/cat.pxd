#cython: language_level=3
#All import must be fully qualified starting at the codeRootPackage
from agile_ai.cythonized.dog cimport Dog

cdef class Cat:
    cpdef name(self)
    cpdef friendWith(self)
