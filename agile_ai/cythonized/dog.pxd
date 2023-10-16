#cython: language_level=3
#All import must be fully qualified starting at the codeRootPackage

cdef class Dog:
    cpdef name(self)
    cpdef friendWith(self)
