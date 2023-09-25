from pathlib import Path

import yaml

from agile_ai.data_marshalling.yaml_handler import YamlHandler
from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_future import an_existing_path
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    path: Path

@pyne
def yaml_handler_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.path = tc.test_directory.path / "file.yaml"

    @describe("#load")
    def _():
        @it("returns the file contents")
        def _(tc: TestContext):
            with tc.path.open("w") as file:
                yaml.dump(dict(a="c", b=1), file)
            content = YamlHandler.load(tc.path)
            expect(content).to_be(dict(a="c", b=1))

    @describe("#save")
    def _():
        @it("saves the content to a file")
        def _(tc: TestContext):
            YamlHandler.save(tc.path, dict(a="c", b="1"))
            with tc.path.open("r") as file:
                content = yaml.load(file, yaml.Loader)
            expect(tc.path).to_be(an_existing_path())
            expect(content).to_be(dict(a="c", b="1"))

    @describe("#matches")
    def _():
        @it("matches only .yaml extensions")
        def _(tc: TestContext):
            expect(YamlHandler.matches("test.yaml")).to_be(True)
            expect(YamlHandler.matches("test.yaml_")).to_be(False)
    @it("is registered with FilePath")
    def _(tc: TestContext):
        expect((tc.test_directory // "test.yaml")._handler).to_be(YamlHandler)
