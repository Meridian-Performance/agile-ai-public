from agile_ai.configuration.ingestion_configuration import IngestionConfiguration
from agile_ai.data_marshalling.file_path import FilePath
from agile_ai.ingestion.file_info_ingestor import FileInfoIngestor, FileInfo
from agile_ai.ingestion.file_ingestor import FileIngestor
from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai.memoization.warehouse_key import KeyLiteral
from agile_ai.memoization.warehouse_service import register_object_class
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase, fit
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test, resources_directory
from pynetest.pyne_tester import pyne
from pynetest.expectations import expect
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker
    ingestion_configuration: IngestionConfiguration

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    file_name: str

@pyne
def file_info_ingestor_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test(configure_warehouse=True)
        register_object_class(FileInfo)
        tc.ingestion_configuration.source_data_directory = resources_directory

    @describe("#resolve")
    def _():
        @describe("when the file path doesn't have any encoded keys")
        def _():
            @before_each
            def _(tc: TestContext):
                tc.file_name = "mp4/jet_colors_25.mp4"

            @it("outputs a FileInfo with the file info fields set")
            def _(tc: TestContext):
                ingestor = FileInfoIngestor()
                ingestor.inputs.file_name = tc.file_name
                outputs = ingestor.resolve()
                expect(outputs.file_info.is_present()).to_be(True)
                file_info = outputs.file_info.get()
                expect(file_info.md5_hex).to_be("98b2d6387623c482c534b22ac59cb9aa")
                expect(file_info.name).to_be("jet_colors_25")
                expect(file_info.extension).to_be("mp4")
                expect(file_info.key_part).to_be(KeyLiteral("98b2d6387623c482c534b22ac59cb9aa"))
                expect(file_info.file_name).to_be("mp4/jet_colors_25.mp4")
                expect(file_info.tags).to_be([])

        @describe("when the file has encoded keys")
        def _():
            @before_each
            def _(tc: TestContext):
                tc.file_name = "mp4/jet_colors_25.md5:98b2d6387623c482c534b22ac59cb9aa.tags:a.b.c.mp4"

            @it("outputs a FileInfo with the file info fields set from the encoded keys")
            def _(tc: TestContext):
                ingestor = FileInfoIngestor()
                ingestor.inputs.file_name = tc.file_name
                outputs = ingestor.resolve()
                expect(outputs.file_info.is_present()).to_be(True)
                file_info = outputs.file_info.get()
                expect(file_info.md5_hex).to_be("98b2d6387623c482c534b22ac59cb9aa")
                expect(file_info.name).to_be("jet_colors_25")
                expect(file_info.extension).to_be("mp4")
                expect(file_info.key_part).to_be(KeyLiteral("98b2d6387623c482c534b22ac59cb9aa"))
                expect(file_info.file_name).to_be("mp4/jet_colors_25.md5:98b2d6387623c482c534b22ac59cb9aa.tags:a.b.c.mp4")
                expect(file_info.tags).to_be(["a", "b", "c"])

