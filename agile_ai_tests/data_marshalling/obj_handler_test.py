from pathlib import Path

from agile_ai.data_marshalling.obj_handler import ObjHandler
from agile_ai.geometry.mesh import Mesh
from agile_ai.geometry.shapes.cube import Cube
from agile_ai.geometry.shapes.sor import Cylinder
from agile_ai.injection.decorators import Marker
from agile_ai_tests.test_helpers.pyne_future import an_existing_path, exactly_equal_to_array, close_to_array
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test, resources_directory
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker


def match_lines(actual_lines, expected_lines):
    for actual_line, expected_line in zip(actual_lines, expected_lines):
        expect(actual_line).to_be(expected_line)
    expect(len(actual_lines)).to_be(len(expected_lines))


class TestContext(TCBase):
    mesh: Mesh
    file_path: Path


@pyne
def obj_handler_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.file_path = (tc.test_directory / "mesh.obj").path

    @describe("when using ObjHandler to load obj file with groups")
    def _():
        @it("it loads all elements of the groups")
        def _(tc: TestContext):
            file_path = resources_directory / "obj" / "cube_and_triangle.obj"
            obj: Mesh = ObjHandler().load(file_path.path)
            expect(obj.vertices).to_have_length(11)
            expect(obj.faces).to_have_length(13)
            expect(obj.mesh_names).to_match_list(["cube", "triangle"])
            expect(obj.mesh_face_slice_indices).to_have_length(3)
            expect(obj.mesh_vertex_slice_indices).to_have_length(3)

    @describe("when the model is from MeshBuilder")
    def _():
        @before_each
        def _(tc: TestContext):
            tc.mesh = Cylinder()
            tc.mesh.with_name('cylinder')

        @describe("#save")
        def _():
            @it("it writes out the file")
            def _(tc: TestContext):
                ObjHandler.save(tc.file_path, tc.mesh)
                expect(tc.file_path).to_be(an_existing_path())

        @describe("#load")
        def _():
            @before_each
            def _(tc: TestContext):
                ObjHandler.save(tc.file_path, tc.mesh)

            @it("loads the same mesh as was saved")
            def _(tc: TestContext):
                mesh = ObjHandler.load(tc.file_path)
                expect(mesh).to_be_a(Mesh)
                expect(mesh.vertices).to_be(close_to_array(tc.mesh.vertices))
                expect(mesh.faces).to_be(exactly_equal_to_array(tc.mesh.faces))

    @describe("when the model is from two named models added together")
    def _():
        @before_each
        def _(tc: TestContext):
            cylinder = Cylinder().with_name("cylinder")
            cube = Cube().with_name("cube")
            tc.mesh = Mesh.from_mesh_list([cube, cylinder])

        @describe("#save")
        def _():
            @it("it writes out the file")
            def _(tc: TestContext):
                ObjHandler.save(tc.file_path, tc.mesh)
                expect(tc.file_path.exists())

        @describe("#load")
        def _():
            @before_each
            def _(tc: TestContext):
                ObjHandler.save(tc.file_path, tc.mesh)

            @it("loads the same mesh as was saved")
            def _(tc: TestContext):
                mesh = ObjHandler.load(tc.file_path)
                expect(mesh.vertices).to_be(exactly_equal_to_array(tc.mesh.vertices))
                expect(mesh.faces).to_be(exactly_equal_to_array(tc.mesh.faces))
    
    @describe("#matches")
    def _():
        @it("matches only .obj extensions")
        def _(tc: TestContext):
            expect(ObjHandler.matches("test.obj")).to_be(True)
            expect(ObjHandler.matches("test.obj_")).to_be(False)
    @it("is registered with FilePath")
    def _(tc: TestContext):
        expect((tc.test_directory // "test.obj")._handler).to_be(ObjHandler)
