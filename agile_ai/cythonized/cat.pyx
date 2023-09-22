#cython: language_level=3
cdef class Cat:
    cpdef name(self):
        return 'cat'
    cpdef friendWith(self):
        cdef Dog dog = Dog()
        return dog.name()

