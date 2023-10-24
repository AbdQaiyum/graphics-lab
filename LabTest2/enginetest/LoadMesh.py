from OpenGL.GL import *
from Mesh import *
import pygame
from ctypes import c_float
import array  # Import the array module

class LoadMesh(Mesh):
    def __init__(self, filename, draw_type):
        super().__init__()
        self.filename = filename
        self.draw_type = draw_type
        self.vbo = glGenBuffers(1)  # Generate a VBO
        self.vertices = []  # Separate lists for vertices and triangles/quadrilaterals
        self.triangles = []
        self.quads = []

        self.load_drawing()

    def load_drawing(self):
        with open(self.filename) as fp:
            for line in fp:
                if line.startswith("v "):
                    # Parse vertex coordinates
                    parts = line.split()
                    vx, vy, vz = map(float, parts[1:])
                    self.vertices.extend([vx, vy, vz])

                elif line.startswith("f "):
                    # Parse face indices
                    parts = line.split()
                    vertices = [part.split('/') for part in parts[1:]]
                    face_indices = [int(vertex[0]) - 1 for vertex in vertices]

                    # Handle triangles (3 vertices)
                    if len(face_indices) == 3:
                        self.triangles.extend(face_indices)
                    # Handle quadrilaterals (4 vertices)
                    elif len(face_indices) == 4:
                        self.quads.extend(face_indices)

            self.bind_vbo()

    def bind_vbo(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        vertices_array = array.array('f', self.vertices)
        glBufferData(GL_ARRAY_BUFFER, len(vertices_array) * 4, vertices_array.tobytes(), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, None)

        if self.draw_type == GL_TRIANGLES:
            glDrawElements(GL_TRIANGLES, len(self.triangles), GL_UNSIGNED_INT, array.array('I', self.triangles).tobytes())
        elif self.draw_type == GL_QUADS:
            glDrawElements(GL_QUADS, len(self.quads), GL_UNSIGNED_INT, array.array('I', self.quads).tobytes())

        glDisableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
