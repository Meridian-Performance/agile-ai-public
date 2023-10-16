from agile_ai.injection import Marker
from agile_ai.rendering.moderngl_renderer import ModernGLRenderer
from agile_ai.rendering.scene import Scene
from agile_ai_tests.rendering.rendering_test_helpers import get_test_planes, expect_image_match, get_test_spheres, \
    expect_depth_mask_match, expect_xyz_world_match
from agile_ai_tests.test_helpers.pyne_test_helpers import before_each, describe, it, TCBase
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub


class TestContext(TCBase):
    __services__: Marker
    renderer: ModernGLRenderer

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    scene: Scene

@pyne
def moderngl_renderer_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        tc.renderer.initialize_core(1024, 1024)
        tc.scene = tc.renderer.scene

    @describe("When camera geometry is set")  # noqa
    def _():
        @it("The color_image is initialized to the correct size")
        def _(tc: TestContext):
            fx = fy = 1.0
            cx = 125
            cy = 125
            w = 500
            h = 750
            tc.scene.set_camera_geometry(fx, fy, cx, cy, w, h)
            expect(tc.renderer.core.initialized).to_be(True)
            # tc.renderer.core.initialize()
            expect(tc.renderer.get_data().color.shape).to_be((h, w, 3))

    @describe("When planes test pattern color image is rendered")  # noqa
    def _():
        @before_each
        def _(tc: TestContext):
            for plane in get_test_planes():
                tc.scene.add_mesh(plane)

        @it("is correct when rendered with square pixel")  # noqa
        def _(tc: TestContext):
            expect_image_match(tc, "square_pixel")

        @it("is correct when rendered with tall pixel")  # noqa
        def _(tc: TestContext):
            expect_image_match(tc, "tall_pixel")

        @it("is correct when rendered with wide pixel")  # noqa
        def _(tc: TestContext):
            expect_image_match(tc, "wide_pixel")

        @it("is correct when rendered with off center v")  # noqa
        def _(tc: TestContext):
            expect_image_match(tc, "off_center_v")

        @it("is correct when rendered with off center u")  # noqa
        def _(tc: TestContext):
            expect_image_match(tc, "off_center_u")

        @it("is correct when rendered with rotated x")  # noqa
        def _(tc: TestContext):
            expect_image_match(tc, "rotated_x")

        @it("is correct when rendered with rotated y")  # noqa
        def _(tc: TestContext):
            expect_image_match(tc, "rotated_y")

        @it("is correct when rendered with rotated z")  # noqa
        def _(tc: TestContext):
            expect_image_match(tc, "rotated_z")

        @it("is correct when rendered with translated x")  # noqa
        def _(tc: TestContext):
            expect_image_match(tc, "translated_x")

        @it("is correct when rendered with translated y")  # noqa
        def _(tc: TestContext):
            expect_image_match(tc, "translated_y")

        @it("is correct when rendered with translated z")  # noqa
        def _(tc: TestContext):
            expect_image_match(tc, "translated_z")

    @describe("When planes test pattern color image is rendered with only red and blue")  # noqa
    def _():
        @it("doesn't display the other colors")
        def _(tc: TestContext):
            visibilities = []
            for plane in get_test_planes():
                index = tc.scene.add_mesh(plane)
                color = tuple(plane.get_triangle_color())
                visible = (color != (255, 0, 0) and color != (0, 0, 255))
                if not visible:
                    tc.scene.disable_mesh(index)
                visibilities.append(visible)
            expect_image_match(tc, "square_pixel", visibilities)

    @describe("When planes test pattern depth is rendered")  # noqa
    def _():
        @before_each
        def _(tc: TestContext):
            for plane in get_test_planes():
                tc.scene.add_mesh(plane)

        @it("is has the same non-zero mask as the color image")
        def _(tc: TestContext):
            expect_depth_mask_match(tc, "square_pixel")

    @describe("When spheres test pattern X, Y, Z world is rendered")  # noqa
    def _():
        @before_each
        def _(tc: TestContext):
            for sphere in get_test_spheres():
                tc.scene.add_mesh(sphere)

        @it("is correct when rendered with square pixel")  # noqa
        def _(tc: TestContext):
            expect_xyz_world_match(tc, "square_pixel")

        @it("is correct when rendered with tall pixel")  # noqa
        def _(tc: TestContext):
            expect_xyz_world_match(tc, "tall_pixel")

        @it("is correct when rendered with wide pixel")  # noqa
        def _(tc: TestContext):
            expect_xyz_world_match(tc, "wide_pixel")

        @it("is correct when rendered with off center v")  # noqa
        def _(tc: TestContext):
            expect_xyz_world_match(tc, "off_center_v")

        @it("is correct when rendered with off center u")  # noqa
        def _(tc: TestContext):
            expect_xyz_world_match(tc, "off_center_u")

        @it("is correct when rendered with rotated x")  # noqa
        def _(tc: TestContext):
            expect_xyz_world_match(tc, "rotated_x")

        @it("is correct when rendered with rotated y")  # noqa
        def _(tc: TestContext):
            expect_xyz_world_match(tc, "rotated_y")

        @it("is correct when rendered with rotated z")  # noqa
        def _(tc: TestContext):
            expect_xyz_world_match(tc, "rotated_z")

        @it("is correct when rendered with translated x")  # noqa
        def _(tc: TestContext):
            expect_xyz_world_match(tc, "sm_translated_x")

        @it("is correct when rendered with translated y")  # noqa
        def _(tc: TestContext):
            expect_xyz_world_match(tc, "sm_translated_y")

        @it("is correct when rendered with translated z")  # noqa
        def _(tc: TestContext):
            expect_xyz_world_match(tc, "sm_translated_z")
