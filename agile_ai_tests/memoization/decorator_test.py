from agile_ai.memoization.decorators import all_args_constructor, self_last_args_memo
from pynetest.expectations import expect
from pynetest.pyne_test_collector import before_each, it, describe, fdescribe
from pynetest.pyne_tester import pyne


@pyne
def decorator_tests():
    @describe("#all_args_constructor")
    def _():
        @before_each
        def _(self):
            @all_args_constructor
            class SomeClass:
                a: int
                b: int

            self.SomeClass = SomeClass

        @it("creates a constructor for all args as kwargs that default to None")
        def _(self):
            some_class = self.SomeClass()
            expect(some_class.a).to_be(None)
            expect(some_class.b).to_be(None)

        @it("creates a constructor that sets any args specified by keywords")
        def _(self):
            some_class = self.SomeClass(a=5)
            expect(some_class.a).to_be(5)
            expect(some_class.b).to_be(None)

        @describe("if non-keyword args are used")
        def _():
            @it("raises a ValueError")
            def _(self):
                expect(lambda: self.SomeClass(5)).to_raise_error_of_type(ValueError)

    @describe("#self_last_args_memo")
    def _():
        @before_each
        def _(self):
            class SomeClass:
                a: int
                b: int
                num_calls: int

                @self_last_args_memo
                def some_fun(self, new_a, new_b):
                    self.a = new_a
                    self.b = new_b
                    self.num_calls += 1

            self.some_class = SomeClass()
            self.some_class.a = 0
            self.some_class.b = 0
            self.some_class.num_calls = 0

        @it("counts the number of distinct calls to some_fun")
        def _(self):

            self.some_class.some_fun(1,new_b=10)
            expect(self.some_class.num_calls).to_be(1)
            expect(self.some_class.a).to_be(1)
            expect(self.some_class.b).to_be(10)

            self.some_class.some_fun(1, new_b = 20)
            expect(self.some_class.num_calls).to_be(2)
            expect(self.some_class.a).to_be(1)
            expect(self.some_class.b).to_be(20)

            self.some_class.some_fun(1, 20)
            expect(self.some_class.num_calls).to_be(3)
            expect(self.some_class.a).to_be(1)
            expect(self.some_class.b).to_be(20)

            self.some_class.some_fun(1,20)
            expect(self.some_class.num_calls).to_be(3)
            expect(self.some_class.a).to_be(1)
            expect(self.some_class.b).to_be(20)

            self.some_class.some_fun(3,20)
            expect(self.some_class.num_calls).to_be(4)
            expect(self.some_class.a).to_be(3)
            expect(self.some_class.b).to_be(20)