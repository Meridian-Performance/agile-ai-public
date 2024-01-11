#cython: language_level=3
#include "cat.pxd"
#include "dog.pxd"
from agile_ai.cythonized.dog cimport Dog

cdef class Cat:
    cpdef name(self):
        return 'cat'
    cpdef friendWith(self):
        cdef Dog dog = Dog()
        return dog.name()

