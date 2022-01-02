import sys

#If we're running from the test directory, this finds the modules in pygl
sys.path.append('./../')

from pygl.shader import *
import pygame

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

glClearColor(0.0, 0.5, 0.5, 1.0)
glEnableClientState(GL_VERTEX_ARRAY)

sh = Shader()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    pygame.time.wait(10)
