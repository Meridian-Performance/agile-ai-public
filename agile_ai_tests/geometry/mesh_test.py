from typing import Tuple

import numpy as np

from agile_ai.geometry.mesh import Mesh
from agile_ai.geometry.shapes.cube import Cube
from agile_ai_tests.test_helpers.pyne_future import exactly_equal_to_array, close_to_array
from agile_ai_tests.test_helpers.pyne_test_helpers import TCBase, before_each, describe, it, xdescribe
from agile_ai_tests.test_helpers.test_helpers import reset_and_configure_test
from pynetest.expectations import expect
from pynetest.pyne_tester import pyne


class TestContext(TCBase):
    mesh: Mesh
    mesh_copy: Mesh
    mesh_short: Mesh
    submesh: Mesh
    mesh: Mesh
    vertices: Tuple
    faces: Tuple
    cube1: Cube
    cube2: Cube


@pyne
def mesh_test():
    @before_each(TestContext)
    def _(tc: TestContext):
        reset_and_configure_test()
        vertices = [(0, 0, 1), (0, 1, 0), (0, 1, 1), (0, 0, 0)]
        colors = [(0, 0, .5), (0, .5, 0), (0, .5, .5), (0, .5, 0)]
        triangles = [(0, 1, 2), (0, 3, 1)]
        vertices = np.array(vertices).T
        RGB = np.array(colors).T
        faces = np.array(triangles).T
        tc.mesh = Mesh(vertices, faces, RGB)
        tc.mesh_copy = Mesh(vertices.copy(), faces.copy(), RGB.copy())
        tc.mesh_short = Mesh(vertices.T[:3].T, faces.T[:1].T, RGB.T[:3].T)
        tc.submesh = Mesh(vertices, faces.T[1:].T, RGB)
        tc.mesh = Mesh(vertices, faces)
        tc.vertices = vertices
        tc.RGB = RGB
        tc.faces = faces

    @describe(":from_mesh_list")
    def _():
        @before_each
        def _(tc: TestContext):
            tc.cube1 = Cube()
            tc.cube2 = Cube()
            tc.cube2.translate((3, 3, 3))

        @it("combines meshes into a new mesh")
        def _(tc: TestContext):
            combined = Mesh.from_mesh_list([tc.cube1, tc.cube2])
            expect(combined.vertex_count).to_be(tc.cube1.vertex_count + tc.cube2.vertex_count)
            expect(combined.face_count).to_be(tc.cube1.face_count + tc.cube2.face_count)
            triangles_1 = tc.cube1.get_triangle_vertices()
            triangles_2 = tc.cube2.get_triangle_vertices()
            triangles_combined = combined.get_triangle_vertices()
            expect(triangles_combined).to_be(close_to_array(np.vstack((triangles_1, triangles_2))))

    @xdescribe("#get_sub_mesh_by_index")
    def _():
        @it("returns the mesh corresponding to the index")
        def _(tc: TestContext):
            cube_1 = Cube().with_name("cube_1")
            cube_2 = Cube().translate((100, 0, 0)).with_name("cube_2")
            cube_3 = Cube().translate((0, 0, 100)).with_name("cube_3")
            mesh = Mesh.from_mesh_list([cube_1, cube_2, cube_3])
            expect(mesh.get_sub_mesh_by_index(0).triangle_vertices).to_be(exactly_equal_to_array(cube_1.triangle_vertices))
            expect(mesh.get_sub_mesh_by_index(1).triangle_vertices).to_be(exactly_equal_to_array(cube_2.triangle_vertices))
            expect(mesh.get_sub_mesh_by_index(2).triangle_vertices).to_be(exactly_equal_to_array(cube_3.triangle_vertices))

        @describe("when filter_vertices=True")
        def _():
            @it("returns the mesh corresponding to the index, with only the vertices belonging to that mesh")
            def _(tc: TestContext):
                cube_1 = Cube().with_name("cube_1")
                cube_2 = Cube().translate((100, 0, 0)).with_name("cube_2")
                cube_3 = Cube().translate((0, 0, 100)).with_name("cube_3")
                mesh = Mesh.from_mesh_list([cube_1, cube_2, cube_3])
                mesh_1 = mesh.get_sub_mesh_by_index(0, filter_vertices=True)
                mesh_2 = mesh.get_sub_mesh_by_index(1, filter_vertices=True)
                mesh_3 = mesh.get_sub_mesh_by_index(2, filter_vertices=True)
                expect(mesh_1.triangle_vertices).to_be(exactly_equal_to_array(cube_1.triangle_vertices))
                expect(mesh_2.triangle_vertices).to_be(exactly_equal_to_array(cube_2.triangle_vertices))
                expect(mesh_3.triangle_vertices).to_be(exactly_equal_to_array(cube_3.triangle_vertices))
                expect(mesh_1.vertices).to_have_length(8)
                expect(mesh_2.vertices).to_have_length(8)
                expect(mesh_3.vertices).to_have_length(8)

        @describe("when filter_vertices=True")
        def _():
            @it("returns the mesh corresponding to the index, with all vertices")
            def _(tc: TestContext):
                cube_1 = Cube().with_name("cube_1")
                cube_2 = Cube().translate((100, 0, 0)).with_name("cube_2")
                cube_3 = Cube().translate((0, 0, 100)).with_name("cube_3")
                mesh = Mesh.from_mesh_list([cube_1, cube_2, cube_3])
                mesh_1 = mesh.get_sub_mesh_by_index(0, filter_vertices=True)
                mesh_2 = mesh.get_sub_mesh_by_index(1, filter_vertices=True)
                mesh_3 = mesh.get_sub_mesh_by_index(2, filter_vertices=True)
                expect(mesh_1.triangle_vertices).to_be(exactly_equal_to_array(cube_1.triangle_vertices))
                expect(mesh_2.triangle_vertices).to_be(exactly_equal_to_array(cube_2.triangle_vertices))
                expect(mesh_3.triangle_vertices).to_be(exactly_equal_to_array(cube_3.triangle_vertices))
                expect(mesh_1.vertices).to_have_length(mesh.vertex_count)
                expect(mesh_2.vertices).to_have_length(mesh.vertex_count)
                expect(mesh_3.vertices).to_have_length(mesh.vertex_count)

