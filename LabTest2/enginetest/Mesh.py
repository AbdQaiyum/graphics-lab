from OpenGL.GL import *
import pygame

class Mesh:
    def __init__(self):
        self.vertices = []
        self.triangles = []
        self.vbo = glGenBuffers(1)  # Generate a VBO
        self.draw_type = GL_TRIANGLES

    def draw(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexPointer(3, GL_FLOAT, 0, None)
        glEnableClientState(GL_VERTEX_ARRAY)

        glDrawArrays(self.draw_type, 0, len(self.vertices) // 3)

        glDisableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
