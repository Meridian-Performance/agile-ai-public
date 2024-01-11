#cython: language_level=3
#include "cat.pxd"
from agile_ai.cythonized.cat cimport Cat

cdef class Dog:
    cpdef name(self):
        return 'dog'
    cpdef friendWith(self):
        cdef Cat cat = Cat()
        return cat.name()
    
