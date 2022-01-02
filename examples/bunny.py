import pygame
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from PIL import Image
import numpy
import math

scene = pywavefront.Wavefront('f16.obj', collect_faces=True)

width = 8*50;
height = 6*50;
camX = 0;
camZ = 0;
yaw = 0;
pitch = 0;

class Motion(object):
    __slots__ = ['forward', 'backward', 'left', 'right']
    
def passive_motion(x, y):
    # two variables to store X and Y coordinates, as observed from the center
    #  of the window
    
    dev_x = (width/2)-x;
    dev_y = (height/2)-y;

    #/* apply the changes to pitch and yaw*/
    yaw+=dev_x/10.0;
    pitch+=dev_y/10.0;


def read_texture(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.int8)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D,texture_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return texture_id
    


cubeVertices = ((20,20,20),(20,20,-20),(20,-20,-20),(20,-20,20),(-20,20,20),(-20,-20,-20),(-20,-20,20),(-20, 20,-20))
cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))

scene_box = (scene.vertices[0], scene.vertices[0])
for vertex in scene.vertices:
    min_v = [min(scene_box[0][i], vertex[i]) for i in range(3)]
    max_v = [max(scene_box[1][i], vertex[i]) for i in range(3)]
    scene_box = (min_v, max_v)

scene_size     = [scene_box[1][i]-scene_box[0][i] for i in range(3)]
max_scene_size = max(scene_size)
scaled_size    = 5
scene_scale    = [scaled_size/max_scene_size for i in range(3)]
scene_trans    = [-(scene_box[1][i]+scene_box[0][i])/2 for i in range(3)]


def wireCube():
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()
    
    
def solidCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()
    
    
def Model():
    glPushMatrix()
    glScalef(*scene_scale)
    glTranslatef(*scene_trans)

    for mesh in scene.mesh_list:
        glBegin(GL_TRIANGLES)
        for face in mesh.faces:
            for vertex_i in face:
                glVertex3f(*scene.vertices[vertex_i])
        glEnd()

    glPopMatrix()
    
def camera(d_yaw, d_pitch, mot):
    
    global camX, camZ, yaw, pitch
    if (mot.left == True):
        camX += math.cos(math.radians((yaw+90+90)))/5.0;
        camZ -= math.sin(math.radians((yaw+90+90)))/5.0;
    if (mot.right == True):
        #glTranslatef(1, 0, 0)
        camX += math.cos(math.radians((yaw+90-90)))/5.0;
        camZ -= math.sin(math.radians((yaw+90-90)))/5.0;
    if (mot.forward == True):
        #glTranslatef(0, 1, 0)
        camX += math.cos(math.radians((yaw+90)))/5.0;
        camZ -= math.sin(math.radians((yaw+90)))/5.0;
    if (mot.backward == True):
        #glTranslatef(0, -1, 0)
        camX += math.cos(math.radians((yaw+90+180)))/5.0;
        camZ -= math.sin(math.radians((yaw+90+180)))/5.0;
        
    glRotatef(-d_pitch, 1, 0, 0);
    glRotatef(-d_yaw, 0, 1, 0);
    glTranslatef(-camX, 0, -camZ);


def main():
        pygame.init()
        
        
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (display[0] / display[1]), 1, 500.0)
        glTranslatef(0.0, 0.0, -10)
        
        print ('Vendor: %s' % (glGetString(GL_VENDOR)))
        print ('Opengl version: %s' % (glGetString(GL_VERSION)))
        print ('GLSL Version: %s' % (glGetString(GL_SHADING_LANGUAGE_VERSION)))
        print ('Renderer: %s' % (glGetString(GL_RENDERER)))
        
        
        button_down = False
        button2_down = False
        
        camX = 0;
        camZ = -10
        
        yaw = 0;
        pitch = 0;
        
        motion = Motion()

        while True:
            d_yaw = 0
            d_pitch = 0
            
            motion.left = False;
            motion.right  = False;
            motion.forward = False;
            motion.backward = False;
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        #glTranslatef(-1, 0, 0)
                        motion.left = True;
                    if event.key == pygame.K_RIGHT:
                        #glTranslatef(1, 0, 0)
                        motion.right = True;
                    if event.key == pygame.K_UP:
                        #glTranslatef(0, 1, 0)
                        motion.forward = True;
                    if event.key == pygame.K_DOWN:
                        #glTranslatef(0, -1, 0)
                        motion.backward = True;
                        
                        
                if event.type == pygame.MOUSEMOTION:
                    
                    if button_down == True:
                        #print(event.rel)
                        d_pitch = event.rel[1]/10;
                        d_yaw = event.rel[0]/10;
                        
                        yaw = yaw + d_yaw
                        pitch = pitch + d_pitch
                        
                        #glRotatef(event.rel[1]*0.1, 1, 0, 0)
                        #glRotatef(event.rel[0]*0.1, 0, 1, 0)
                    if button2_down == True:
                         #glTranslatef(event.rel[0]*0.01, -event.rel[1]*0.01, 0)
                         x = x + event.rel[0]*0.01
                         y = y + event.rel[1]*0.01
                         
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4: # wheel rolled up
                    glScaled(1.05, 1.05, 1.05);
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: # wheel rolled down
                    glScaled(0.95, 0.95, 0.95);
                 
            for event in pygame.mouse.get_pressed():
                #print(pygame.mouse.get_pressed())
                if pygame.mouse.get_pressed()[0] == 1:
                    button_down = True
                elif pygame.mouse.get_pressed()[0] == 0:
                    button_down = False
                    
                if pygame.mouse.get_pressed()[2] == 1:
                    button2_down = True
                elif pygame.mouse.get_pressed()[2] == 0:
                    button2_down = False
                    
            camera(d_yaw, d_pitch, motion)
            
            print("yaw:{} pitch:{} motion:{}".format(yaw, pitch, motion))

            
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            Model()
            solidCube()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            pygame.display.flip()
            pygame.time.wait(10)

main()