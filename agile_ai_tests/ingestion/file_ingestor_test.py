from agile_ai.configuration import configure_warehouse
from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.ingestion.file_info_ingestor import FileInfo
from agile_ai.ingestion.file_ingestor import FileIngestor, File
from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai.memoization.md5_helper import Md5Helper
from agile_ai.memoization.object_option import ObjectOption
from agile_ai_tests.test_helpers.pyne_future import an_existing_path
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase, fit
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
def file_ingestor_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test(configure_warehouse=True)
        configure_warehouse()
        tc.file_path = resources_directory / "mp4" // "jet_colors_25.mp4"

    @describe("#resolve")
    def _():
        @it("populates the File object with the file")
        def _(tc: TestContext):
            ingestor = FileIngestor()
            ingestor.inputs.file_path = tc.file_path
            outputs = ingestor.resolve()
            expect(outputs.file).to_be_a(ObjectOption)
            file = outputs.file.get()
            expect(file).to_be_a(File)
            expect(file.file_info.is_present()).to_be(True)
            file_info = file.file_info.get()
            expect(file_info).to_be_a(FileInfo)
            expect(file_info.md5_hex).to_be("98b2d6387623c482c534b22ac59cb9aa")
            expect(file.path.path.parts[-1]).to_be("file.mp4")
            expect(file.path).to_be(an_existing_path())
            expect(tc.md5_helper.digest_file(file.path)).to_be("98b2d6387623c482c534b22ac59cb9aa")