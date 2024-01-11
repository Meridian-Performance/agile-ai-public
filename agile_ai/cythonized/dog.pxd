#cython: language_level=3
#All import must be fully qualified starting at the codeRootPackage

#pragma once

cdef class Dog:
    cpdef name(self)
    cpdef friendWith(self)
