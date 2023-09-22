#cython: language_level=3
#All import must be fully qualified starting at the codeRootPackage
from agile_ai.cythonized.cat cimport Cat

cdef class Dog:
    cpdef name(self)
    cpdef friendWith(self)
