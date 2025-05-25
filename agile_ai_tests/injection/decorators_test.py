from agile_ai.injection.decorators import autowire_services, Marker, autowire, get_service, autowire_context, \
    reset_autowire, inject
from agile_ai.injection.interfaces import Service
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase, fdescribe, fit
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker


class SomeClass:
    pass


class SomeServiceA(Service):
    pass


class SomeServiceB(Service):
    pass


@autowire_services
class SomeClassWithServices:
    __services__: Marker
    some_service_a: SomeServiceA
    some_service_b: SomeServiceB
    some_class: SomeClass


@pyne
def decorators_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        autowire_context.reset()

    @describe("#autowire")
    def _():
        @it("adds the class to the autowire context")
        def _(tc: TestContext):
            class SomeAutowiredClass:
                some_class: SomeClass = autowire(SomeClass)
            _ = SomeAutowiredClass().some_class
            expect(autowire_context.instance_by_cls[SomeClass]).to_be_a(SomeClass)

        @it("returns an instance of the class")
        def _(tc: TestContext):
            class SomeAutowiredClass:
                some_class: SomeClass = autowire(SomeClass)
            some_class = SomeAutowiredClass().some_class
            expect(some_class).to_be_a(SomeClass)

    @describe("#reset_autowire")
    def _():
        @before_each
        def _(tc: TestContext):
            class SomeAutowiredClass:
                some_class: SomeClass = autowire(SomeClass)
            _ = SomeAutowiredClass().some_class

        @it("clears all classes from the autowire_context")
        def _(tc: TestContext):
            reset_autowire()
            expect(autowire_context.instance_by_cls).to_have_length(0)

    @describe("#autowire_services")
    def _():
        @it("autowires all Service classes under the service marker")
        def _(tc: TestContext):
            instance = SomeClassWithServices()
            some_service_a = instance.some_service_a
            some_service_b = instance.some_service_b
            expect(some_service_a).to_be_a(SomeServiceA)
            expect(some_service_b).to_be_a(SomeServiceB)
            expect(autowire_context.instance_by_cls).to_have_length(2)
            expect(autowire_context.instance_by_cls[SomeServiceA]).to_be(some_service_a)
            expect(autowire_context.instance_by_cls[SomeServiceB]).to_be(some_service_b)

    @describe("#get_service")
    def _():
        @it("returns the autowired class")
        def _(tc: TestContext):
            some_service_a_1 = get_service(SomeServiceA)
            expect(get_service(SomeServiceA)).to_be_a(SomeServiceA)
            some_service_a_2 = get_service(SomeServiceA)
            expect(some_service_a_1).to_be(some_service_a_2)

    @describe("#inject")
    def _():
        @it("injects the instance")
        def _(tc: TestContext):
            some_service_a = SomeServiceA()
            inject(some_service_a)
            some_service_a_injected = get_service(SomeServiceA)
            expect(some_service_a_injected).to_be(some_service_a)

        @describe("when an alternate cls type is provided")
        def _():
            @it("injects the instance for the other class")
            def _(tc: TestContext):
                some_service_a = SomeServiceA()
                inject(some_service_a, for_cls=SomeServiceB)
                some_service_a_as_b = get_service(SomeServiceB)
                expect(some_service_a_as_b).to_be(some_service_a)
