#cython: language_level=3
#All import must be fully qualified starting at the codeRootPackage

cdef class Cat:
    cpdef name(self)
    cpdef friendWith(self)
