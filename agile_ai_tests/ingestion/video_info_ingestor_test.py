from agile_ai.configuration.ingestion_configuration import IngestionConfiguration
from agile_ai.ingestion.file_info_ingestor import FileInfoIngestor
from agile_ai.ingestion.file_ingestor import FileIngestor
from agile_ai.ingestion.video_info_ingestor import VideoInfoIngestor
from agile_ai.injection.decorators import Marker
from agile_ai.memoization.object_option import ObjectOption
from agile_ai.memoization.warehouse_key import KeyLiteral
from agile_ai.memoization.warehouse_service import register_object_class
from agile_ai.models.file import File
from agile_ai.models.file_info import FileInfo
from agile_ai.models.video_info import VideoInfo
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test, resources_directory
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker
    ingestion_configuration: IngestionConfiguration

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    file_name: str
    file_info: FileInfo
    file_option: ObjectOption[File]
@pyne
def video_info_ingestor_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test(configure_warehouse=True)
        register_object_class(VideoInfo)
        register_object_class(FileInfo)
        register_object_class(File)
        tc.ingestion_configuration.source_data_directory = resources_directory

    @describe("#resolve")
    def _():
        @before_each
        def _(tc: TestContext):
            tc.file_name = "mp4/jet_colors_25.mp4"
            file_info_ingestor = FileInfoIngestor()
            file_info_ingestor.inputs.file_name = tc.file_name
            tc.file_info = file_info_ingestor.resolve().file_info
            file_ingestor = FileIngestor()
            file_ingestor.inputs.file_info = tc.file_info
            tc.file_option = file_ingestor.resolve().file

        @it("outputs a VideoInfo with the file info fields set")
        def _(tc: TestContext):
            ingestor = VideoInfoIngestor()
            ingestor.inputs.file = tc.file_option
            outputs = ingestor.resolve()
            expect(outputs.video_info.is_present()).to_be(True)
            video_info = outputs.video_info.get()
            expect(video_info.md5_hex).to_be("98b2d6387623c482c534b22ac59cb9aa")
            expect(video_info.height).to_be(128)
            expect(video_info.width).to_be(256)
            expect(video_info.frame_count).to_be(25)

