import numpy as np

from agile_ai.geometry.colored_mesh import ColoredMesh
from agile_ai.geometry.pose_conversions import Rx
from agile_ai.geometry.shapes.cube import Cube
from agile_ai.injection.decorators import autowire_services, Marker
from agile_ai.rendering.scene import Scene
from agile_ai_tests.test_helpers.pyne_future import exactly_equal_to_array
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase, fit
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.pyne_tester import pyne
from pynetest.expectations import expect
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker
    renderer: Scene

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker



@pyne
def scene_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()

    @describe("when a mesh is added")
    def _():
        @it("it is added to the mesh list as a visible entry")
        def _(tc: TestContext):
            mesh = ColoredMesh(Cube(), triangle_color=(0, 255, 0))
            tc.renderer.add_mesh(mesh)
            expect(tc.renderer.mesh_list[0].colored_mesh).to_be(mesh)
            expect(tc.renderer.mesh_list[0].visible).to_be(True)

        @it("its index is returned")
        def _(tc: TestContext):
            mesh0 = ColoredMesh(Cube(), triangle_color=(0, 255, 0))
            mesh1 = ColoredMesh(Cube(), triangle_color=(0, 255, 0))
            mesh2 = ColoredMesh(Cube(), triangle_color=(0, 255, 0))
            tc.renderer.add_mesh(mesh0)
            tc.renderer.add_mesh(mesh1)
            index = tc.renderer.add_mesh(mesh2)
            expect(tc.renderer.mesh_list[index].colored_mesh).to_be(mesh2)

    @describe("When a mesh is disabled")
    def _():
        @it("it visible entry is made False")
        def _(tc: TestContext):
            mesh = ColoredMesh(Cube(), triangle_color=(0, 255, 0))
            index = tc.renderer.add_mesh(mesh)
            expect(tc.renderer.mesh_list[0].visible).to_be(True)
            tc.renderer.disable_mesh(index)
            expect(tc.renderer.mesh_list[0].visible).to_be(False)

    @describe("When a mesh is enabled")
    def _():
        @it("it visible entry is made True")
        def _(tc: TestContext):
            mesh = ColoredMesh(Cube(), triangle_color=(0, 255, 0))
            index = tc.renderer.add_mesh(mesh)
            expect(tc.renderer.mesh_list[0].visible).to_be(True)
            tc.renderer.disable_mesh(index)
            expect(tc.renderer.mesh_list[0].visible).to_be(False)
            tc.renderer.enable_mesh(index)
            expect(tc.renderer.mesh_list[0].visible).to_be(True)

    @describe("when the camera geometry is set")
    def _():
        @it("it updates K, width, height")
        def _(tc: TestContext):
            fx = 1
            fy = 2
            cx = 3
            cy = 4
            w = 5
            h = 6
            tc.renderer.set_camera_geometry(fx, fy, cx, cy, w, h)
            K = np.array([(fx, 0, cx), (0, fy, cy), (0, 0, 1)])
            expect(tc.renderer.width).to_be(w)
            expect(tc.renderer.height).to_be(h)
            for v, ev in zip(tc.renderer.K.ravel(), K.ravel()):
                expect(v).to_be(ev)

    @describe("when the camera pose is set via set_frame_world_camera")
    def _():
        @it("It updates F_world_camera")
        def _(tc: TestContext):
            F_world_camera = np.eye(4)
            F_world_camera[:3, :3] = Rx(.2)
            F_world_camera[:3, -1] = (.2, .5, 1)
            F_camera_world = np.linalg.inv(F_world_camera)
            tc.renderer.set_frame_world_camera(F_world_camera)
            expect(tc.renderer.F_camera_world).to_be(exactly_equal_to_array(F_camera_world))

    @describe("when the camera pose is set via set_frame_camera_world")
    def _():
        @it("it updates F_world_camera via the inverse")
        def _(tc: TestContext):
            F_world_camera = np.eye(4)
            F_world_camera[:3, :3] = Rx(.2)
            F_world_camera[:3, -1] = (.2, .5, 1)
            F_camera_world = np.linalg.inv(F_world_camera)
            tc.renderer.set_frame_camera_world(F_camera_world)
            expect(tc.renderer.F_camera_world).to_be(exactly_equal_to_array(F_camera_world))
