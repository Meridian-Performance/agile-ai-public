from agile_ai.configuration import configure_warehouse
from agile_ai.configuration.ingestion_configuration import IngestionConfiguration
from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.ingestion.file_info_ingestor import FileInfoIngestor
from agile_ai.ingestion.file_ingestor import FileIngestor
from agile_ai.injection.decorators import Marker
from agile_ai.memoization.md5_helper import Md5Helper
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.models.file import File
from agile_ai.models.file_info import FileInfo
from agile_ai_tests.test_helpers.pyne_future import an_existing_path
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase, with_stubs
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test, resources_directory
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.attached_spy import attach_stub
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker
    md5_helper: Md5Helper
    ingestion_configuration: IngestionConfiguration

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    file_name: FilePath
    file_info: ObjectOption[FileInfo]
    ingestor: FileIngestor

@pyne
def file_ingestor_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test(configure_warehouse=True)
        configure_warehouse()
        tc.ingestion_configuration.source_data_directory = resources_directory
        tc.file_name = "mp4/jet_colors_25.mp4"
        file_info_ingestor = FileInfoIngestor()
        file_info_ingestor.inputs.file_name = tc.file_name
        tc.file_info = file_info_ingestor.resolve().file_info

    @describe("#resolve")
    def _():
        @it("populates the File object with the file")
        def _(tc: TestContext):
            ingestor = FileIngestor()
            ingestor.inputs.file_info = tc.file_info
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

        @describe("when it is already resolved")
        def _():
            @before_each
            def _(tc: TestContext):
                tc.ingestor = FileIngestor()
                tc.stubs = attach_stub(tc.ingestor, "perform")
                tc.ingestor.inputs.file_info = tc.file_info
                tc.ingestor.resolve()

            @it("doesn't call perform again")
            @with_stubs
            def _(tc: TestContext):
                tc.ingestor.resolve()
                expect(tc.ingestor.perform).was_not_called()
