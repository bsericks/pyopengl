from OpenGL.GL import *
from OpenGL.GLU import *
import glm
from pygl.shader import *
import numpy as np

class Line ():
    
    VBO = 0
    VAO = 0
    vertices = np.array([0.0,0.0,0.0,0.0,0.0,0.0], dtype=np.float32);
    startPoint = glm.vec3(0,0,0);
    endPoint = glm.vec3(0,0,0);
    
    model = glm.mat4(1.0);
    view = glm.mat4(1.0);
    projection = glm.mat4(1.0);

    lineColor = glm.vec3(0,0,0);

    def __init__(self, start, end, shader):

        self.line_shader = shader
        self.startPoint = start;
        self.endPoint = end;
        self.lineColor = glm.vec3(1,1,1);
        self.model = glm.mat4(1.0);

        #self.vertices = [
        #     start.x, start.y, start.z,
        #     end.x, end.y, end.z,
        #]
        np.put(self.vertices, [0,1,2,3,4,5], [start.x, start.y, start.z, end.x, end.y, end.z])
        
        self.vertices

        self.VAO = glGenVertexArrays(1);
        self.VBO = glGenBuffers(1);
        glBindVertexArray(self.VAO);

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO);

        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW);

        # 8 = sizeof float
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 8, ctypes.c_void_p(0));
        glEnableVertexAttribArray(0);

        glBindBuffer(GL_ARRAY_BUFFER, 0); 
        glBindVertexArray(0); 

    

    def setMVP(self, model, view, projection):
        self.model = model;
        self.view = view;
        self.projection = projection;
        return 1;
    

    def setColor(self, color):
        self.lineColor = color;
        return 1;
    

    def draw(self):
        self.line_shader.use()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);  
        self.line_shader.setMat4("model", glm.value_ptr(self.model))
        self.line_shader.setMat4("view", glm.value_ptr(self.view))
        self.line_shader.setMat4("projection", glm.value_ptr(self.projection))

        self.line_shader.setVec3("color", self.lineColor[0], self.lineColor[1], self.lineColor[2])

        glBindVertexArray(self.VAO);
        glDrawArrays(GL_LINES, 0, 2);
        return 1;
    

    def __del__(self):

        glDeleteVertexArrays(1, self.VAO);
        glDeleteBuffers(1, self.VBO);
    
