from typing import Iterable, List

from agile_ai.geometry.mesh import Mesh
import numpy as np


class WavefrontObj:
    @staticmethod
    def mesh_from_lines(lines: Iterable[str]):
        mesh_names = []
        vertices = []
        faces = []
        mesh_face_slice_indices = []
        mesh_vertex_slice_indices = []
        for l in lines:
            if not l:
                continue
            if l[0] == "g":
                mesh_names.append(l[2:].strip())
                mesh_vertex_slice_indices.append(len(vertices))
                mesh_face_slice_indices.append(len(faces))
            elif l[0] == "v":
                vertex = [float(e) for e in l[2:].strip().split()]
                vertices.append(vertex)
            elif l[0] == "f":
                face = [int(e) for e in l[2:].strip().split()]
                faces.append(face)
        mesh_vertex_slice_indices.append(len(vertices))
        mesh_face_slice_indices.append(len(faces))
        return Mesh(vertices=np.array(vertices, dtype=np.float32),
                    faces=np.array(faces, dtype=int)-1,
                    mesh_names=mesh_names,
                    mesh_face_slice_indices=np.array(mesh_face_slice_indices),
                    mesh_vertex_slice_indices=np.array(mesh_vertex_slice_indices)
                    )
    @staticmethod
    def mesh_to_lines(mesh: Mesh) -> List[str]:
        lines = []
        for mesh_index, mesh_name in enumerate(mesh.mesh_names):
            lines.append(f"g {mesh_name}")
            vertex_slice = slice(*mesh.mesh_vertex_slice_indices[mesh_index:mesh_index+2])
            face_slice = slice(*mesh.mesh_face_slice_indices[mesh_index:mesh_index+2])
            for vertex in mesh.vertices[vertex_slice]:
                lines.append(f"v {vertex[0]} {vertex[1]} {vertex[2]}")
            for face in mesh.faces[face_slice]:
                face = face + 1
                lines.append(f"f {face[0]} {face[1]} {face[2]}")
        return lines