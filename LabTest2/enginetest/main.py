import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from LoadMesh import *
from camera import *

pygame.init()

# Project settings
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

# Initialize Pygame window
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('OpenGL in Python')
pygame.mouse.set_visible(False)
pygame.mouse.set_pos(screen_width // 2, screen_height // 2)  # Assuming screen_width and screen_height are the window dimensions


# Load the mesh from a file (e.g., "cube.obj") and set the drawing type
mesh = LoadMesh("teapotKBtesting4.obj", GL_QUADS)  # Assuming your OBJ file contains triangles
camera = Camera(screen_width, screen_height)
def initialize():
    glClearColor(*background_color)
    glColor(*drawing_color)

    # Projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 1000.0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    camera_init()
    glPushMatrix()
    mesh.draw()
    glPopMatrix()

def camera_init():
    # modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    camera.update(screen_width, screen_height)


done = False
initialize()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    display()
    pygame.display.flip()
    pygame.time.delay(10)  # Adjust the delay for the desired frame rate

pygame.quit()
