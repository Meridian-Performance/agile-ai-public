import numpy as np

from agile_ai.geometry.shapes.planar import Plane
from agile_ai.injection import Marker
from agile_ai.rendering.cv_renderer import CvRenderer
from agile_ai.rendering.scene import Scene
from agile_ai_tests.rendering import rendering_test_helpers
from agile_ai_tests.rendering.rendering_test_helpers import test_cases, show_test, get_test_case_image, \
    expect_image_match, get_test_planes
from agile_ai_tests.test_helpers.pyne_test_helpers import TCBase, before_each, it, describe
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne
from pynetest.test_doubles.stub import MegaStub

DEBUG = [None]

VISUALIZE = True
rendering_test_helpers.VISUALIZE = VISUALIZE


def show_test_cases_against_pylab():
    import pylab
    for name in list(test_cases.keys())[2:]:
        print(name)
        show_test(name)
        pylab.imshow(np.zeros((500, 500, 3), dtype=np.uint8))
        pylab.title("Pylab %s" % name)
        pylab.gcf().canvas.draw()
        input("Pylab")
        img = get_test_case_image(name)
        pylab.clf()
        pylab.imshow(img)
        pylab.title("CV Draw %s" % name)
        pylab.gcf().canvas.draw()
        input("CV Draw")


class TestContext(TCBase):
    __services__: Marker
    renderer: CvRenderer

    __stubs__: Marker
    stubs: MegaStub

    __other__: Marker
    scene: Scene


@pyne
def cv_render_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        tc.scene = tc.renderer.scene
        tc.scene.set_frame_camera_world(np.eye(4))

    @describe("When camera geometry is set")  # noqa
    def _():
        @it("The color_image is initialized to the correct size")
        def _(tc: TestContext):
            fx = fy = 1.0
            cx = 125
            cy = 125
            w = 500
            h = 250
            tc.scene.set_camera_geometry(fx, fy, cx, cy, w, h)
            expect(tc.renderer.color_image.shape).to_be((h, w, 3))

    @describe("When a square is rendered in 2D")  # noqa
    def _():
        @it("Creates the correct image")
        def _(tc: TestContext):
            fx = fy = 1.0
            cx = cy = 0
            w = 500
            h = 300
            tc.scene.set_camera_geometry(fx, fy, cx, cy, w, h)
            # Create a 100x50 square at (75, 50)
            plane = Plane()
            plane.translate((1, 1, 0))
            plane.scale((50, 25, 1))
            plane.translate((75, 50, 0))
            for vs in plane.get_triangle_vertices():
                vs = vs[:, :2]
                tc.renderer.render_2d_triangle(vs, color=(255, 0, 0))
            image = np.zeros((h, w, 3), dtype=np.uint8)
            image[50:100 + 1, 75:175 + 1] = (255, 0, 0)
            DEBUG[0] = (image, tc.renderer.color_image)
            same_count = (image == tc.renderer.color_image).all(2).sum()
            expect(same_count).to_be(h * w)

    @describe("When test pattern is rendered")  # noqa
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

    @describe("When test pattern is rendered with only red and blue")  # noqa
    def _():
        @it("doesn't display the other colors")
        def _(tc: TestContext):
            visibilities = []
            for plane in get_test_planes():
                index = tc.scene.add_mesh(plane)
                color = tuple(plane.get_triangle_colors()[0])
                visible = (color != (255, 0, 0) and color != (0, 0, 255))
                if not visible:
                    tc.scene.disable_mesh(index)
                visibilities.append(visible)
            expect_image_match(tc, "square_pixel", visibilities)
