from pynetest.expectations import expect
from pynetest.pyne_test_collector import describe, it
from pynetest.pyne_tester import pyne


@pyne
def cython_build_test():
    @describe("when cython modules are compiled via setup.py")
    def _():
        @it("they can be imported and used")
        def _(self):
            from agile_ai.cythonized.cat import Cat
            from agile_ai.cythonized.dog import Dog
            cat = Cat()
            dog = Dog()
            expect(cat.name()).to_be("cat")
            expect(dog.name()).to_be("dog")
            expect(cat.friendWith()).to_be("dog")
            expect(dog.friendWith()).to_be("cat")
