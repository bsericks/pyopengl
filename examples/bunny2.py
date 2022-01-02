import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from ctypes import *
import numpy as np

import pywavefront



vertex = """
#version 330 core
layout (location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
"""


fragment = """
#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
"""

vertex_data = np.array([0.75, 0.75, 0.0,
                        0.75, -0.75, 0.0,
                        -0.75, -0.75, 0.0], dtype=np.float32)

color_data = np.array([1, 0, 0,
                        0, 1, 0,
                        0, 0, 1], dtype=np.float32)


class ShaderProgram(object):
    """ Helper class for using GLSL shader programs
    """
    def __init__(self, vertex, fragment):
        """
        Parameters
        ----------
        vertex : str
            String containing shader source code for the vertex
            shader
        fragment : str
            String containing shader source code for the fragment
            shader
        """
        self.program_id = glCreateProgram()
        vs_id = self.add_shader(vertex, GL_VERTEX_SHADER)
        frag_id = self.add_shader(fragment, GL_FRAGMENT_SHADER)

        glAttachShader(self.program_id, vs_id)
        glAttachShader(self.program_id, frag_id)
        glLinkProgram(self.program_id)

        if glGetProgramiv(self.program_id, GL_LINK_STATUS) != GL_TRUE:
            info = glGetProgramInfoLog(self.program_id)
            glDeleteProgram(self.program_id)
            glDeleteShader(vs_id)
            glDeleteShader(frag_id)
            raise RuntimeError('Error linking program: %s' % (info))
        glDeleteShader(vs_id)
        glDeleteShader(frag_id)

    def add_shader(self, source, shader_type):
        """ Helper function for compiling a GLSL shader
        Parameters
        ----------
        source : str
            String containing shader source code
        shader_type : valid OpenGL shader type
            Type of shader to compile
        Returns
        -------
        value : int
            Identifier for shader if compilation is successful
        """
        try:
            shader_id = glCreateShader(shader_type)
            glShaderSource(shader_id, source)
            glCompileShader(shader_id)
            if glGetShaderiv(shader_id, GL_COMPILE_STATUS) != GL_TRUE:
                info = glGetShaderInfoLog(shader_id)
                raise RuntimeError('Shader compilation failed: %s' % (info))
            return shader_id
        except:
            glDeleteShader(shader_id)
            raise

    def uniform_location(self, name):
        """ Helper function to get location of an OpenGL uniform variable
        Parameters
        ----------
        name : str
            Name of the variable for which location is to be returned
        Returns
        -------
        value : int
            Integer describing location
        """
        return glGetUniformLocation(self.program_id, name)

    def attribute_location(self, name):
        """ Helper function to get location of an OpenGL attribute variable
        Parameters
        ----------
        name : str
            Name of the variable for which location is to be returned
        Returns
        -------
        value : int
            Integer describing location
        """
        return glGetAttribLocation(self.program_id, name)


scene = pywavefront.Wavefront('bunny.obj', collect_faces=True)

verts = np.array(scene.vertices, dtype="float32")
flatverts = (verts.flatten())
print(len(scene.vertices))

def main():

    pygame.init ()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    glClearColor (0.0, 0.5, 0.5, 1.0)
    glEnableClientState (GL_VERTEX_ARRAY)

    gluPerspective(45, (display[0] / display[1]), 1, 500.0)
    glTranslatef(0.0, -1.0, -5)
    
    # Lets compile our shaders since the use of shaders is now
    # mandatory. We need at least a vertex and fragment shader
    # begore we can draw anything
    program = ShaderProgram(fragment=fragment, vertex=vertex)
    
    

    #vertices = [ 0.0, 1.0, 0.0,  0.0, 0.0, 0.0,  1.0, 1.0, 0.0 ]
    vbo = glGenBuffers (1)
    glBindBuffer (GL_ARRAY_BUFFER, vbo)
    glBufferData (GL_ARRAY_BUFFER, len(flatverts)*4, flatverts, GL_STATIC_DRAW)

    button_down = False
    running = True
    while running:
    
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                #print(event.rel)
                if button_down == True:
                    #pitch = pitch + event.rel[1]*0.1;
                    #yaw = yaw + event.rel[0]*0.1;
                    glRotatef(event.rel[1]*0.1, 1, 0, 0)
                    glRotatef(event.rel[0]*0.1, 0, 1, 0)
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
                
        
        
        glClear (GL_COLOR_BUFFER_BIT)
        
        #glUseProgram(program.program_id)
        
        glPushMatrix()
        #view = gluLookAt(0,0,6,0,0,0,0,1,0)
        
        
        glBindBuffer (GL_ARRAY_BUFFER, vbo)
        glVertexPointer (3, GL_FLOAT, 0, None)

        glDrawArrays (GL_POINTS, 0, len(scene.vertices))
        glPopMatrix()
        
        pygame.display.flip ()
        pygame.time.wait(10)
        
main()