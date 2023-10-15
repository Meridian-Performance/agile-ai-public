from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai.memoization.md5_helper import Md5Helper
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test, resources_directory
from pynetest.pyne_tester import pyne
from pynetest.expectations import expect
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker
    md5_helper: Md5Helper

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    file_path: FilePath

@pyne
def md5_helper_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.file_path = resources_directory / "mp4" // "jet_colors_25.mp4"

    @describe("#digest_file")
    def _():
        @it("returns thed md5 hex digest")
        def _(tc: TestContext):
            expect(tc.md5_helper.digest_file(tc.file_path)).to_be("98b2d6387623c482c534b22ac59cb9aa")

