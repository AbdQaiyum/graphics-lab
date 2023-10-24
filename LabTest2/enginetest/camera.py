import pygame
from OpenGL.GLU import *
from math import *

class Camera:
    def __init__(self, screen_width, screen_height):
        self.eye = pygame.math.Vector3(0, 0, 0)
        self.up = pygame.math.Vector3(0, 1, 0)
        self.right = pygame.math.Vector3(1, 0, 0)
        self.forward = pygame.math.Vector3(0, 0, 1)
        self.look = self.eye + self.forward
        self.yaw = -90
        self.pitch = 0
        self.last_mouse = pygame.math.Vector2(screen_width // 2, screen_height // 2)
        self.mouse_sensitivityX = 0.1
        self.mouse_sensitivityY = 0.1

        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos(screen_width // 2, screen_height // 2)

    def rotate(self, yaw, pitch):
        self.yaw += yaw
        self.pitch += pitch

        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        self.forward.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward.y = sin(radians(self.pitch))
        self.forward.z = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.forward = self.forward.normalize()
        self.right = self.forward.cross(pygame.Vector3(0, 1, 0)).normalize()
        self.up = self.right.cross(self.forward).normalize()

    def update(self, screen_width, screen_height):
        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Calculate the change in mouse position from the center
        mouse_change = pygame.math.Vector2(mouse_pos[0] - screen_width // 2, mouse_pos[1] - screen_height // 2)

        # Re-center the mouse pointer
        pygame.mouse.set_pos(screen_width // 2, screen_height // 2)

        # Update the camera rotation based on mouse movement
        self.rotate(mouse_change.x * self.mouse_sensitivityX, mouse_change.y * self.mouse_sensitivityY)

        keys = pygame.key.get_pressed()
        # Camera movement speed
        move_speed = 0.1

        if keys[pygame.K_DOWN]:
            # Move the camera backward (along the negative self.forward direction)
            self.eye -= self.forward * move_speed
        if keys[pygame.K_UP]:
            # Move the camera forward (along the self.forward direction)
            self.eye += self.forward * move_speed
        if keys[pygame.K_LEFT]:
            # Move the camera left (along the self.right direction)
            self.eye -= self.right * move_speed
        if keys[pygame.K_RIGHT]:
            # Move the camera right (along the self.right direction)
            self.eye += self.right * move_speed
        if keys[pygame.K_PAGEUP]:
            # Move the camera up (along the self.up direction)
            self.eye += self.up * move_speed
        if keys[pygame.K_PAGEDOWN]:
            # Move the camera down (along the negative self.up direction)
            self.eye -= self.up * move_speed

        self.look = self.eye + self.forward
        gluLookAt(self.eye.x, self.eye.y, self.eye.z,
                  self.look.x, self.look.y, self.look.z,
                  self.up.x, self.up.y, self.up.z)
