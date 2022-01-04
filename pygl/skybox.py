from OpenGL.GL import *
from OpenGL.GLU import *
import glm
from pygl.shader import *
import numpy as np
from PIL import Image

class Skybox ():
    
    VBO = 0
    VAO = 0
    
    model = glm.mat4(1.0);
    view = glm.mat4(1.0);
    projection = glm.mat4(1.0);


    def __init__(self):

        self.shader = Shader(vertexPath='data/skyboxShader.vs', fragmentPath='data/skyboxShader.fs')

        
        self.vertices = np.array([
        # positions          
        -1.0,  1.0, -1.0,
        -1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
         1.0,  1.0, -1.0,
        -1.0,  1.0, -1.0,
#
        -1.0, -1.0,  1.0,
        -1.0, -1.0, -1.0,
        -1.0,  1.0, -1.0,
        -1.0,  1.0, -1.0,
        -1.0,  1.0,  1.0,
        -1.0, -1.0,  1.0,
#
         1.0, -1.0, -1.0,
         1.0, -1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0, -1.0,
         1.0, -1.0, -1.0,
#
        -1.0, -1.0,  1.0,
        -1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
         1.0, -1.0,  1.0,
        -1.0, -1.0,  1.0,
#
        -1.0,  1.0, -1.0,
         1.0,  1.0, -1.0,
         1.0,  1.0,  1.0,
         1.0,  1.0,  1.0,
        -1.0,  1.0,  1.0,
        -1.0,  1.0, -1.0,
#
        -1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
         1.0, -1.0, -1.0,
         1.0, -1.0, -1.0,
        -1.0, -1.0,  1.0,
         1.0, -1.0,  1.0],
         dtype=np.float32);

        #self.vertices = np.array([
        ##    -1.0, 1.0, 1.0,
        ##    1.0, 1.0, 1.0,
        ##    -1.0, -1.0, 1.0,
        ##    1.0, 1.0, 1.0,
        ##    -1.0, -1.0, 1.0,
        ##    1.0, -1.0, 1.0
        #1.0, -1.0, -1.0,
        # 1.0,  1.0, -1.0,
        #-1.0,  1.0, -1.0,
        #-1.0,  1.0, -1.0,
        #-1.0, -1.0, -1.0,
        # 1.0, -1.0, -1.0
        #], dtype=np.float32);

        self.VAO = glGenVertexArrays(1);
        self.VBO = glGenBuffers(1);

        glBindVertexArray(self.VAO);
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO);
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW);
        
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3*self.vertices.dtype.itemsize, ctypes.c_void_p(0));
        glEnableVertexAttribArray(0);

        faces = [
        
            "./data/skybox/right.png",
            "./data/skybox/left.png",
            "./data/skybox/top.png",
            "./data/skybox/bottom.png",
            "./data/skybox/front.png",
            "./data/skybox/back.png"
        ]
        self.cubemapTexture = self.loadCubemap(faces);

        self.shader.use()
        self.shader.setInt("skybox", 0)
    

    def setMVP(self, model, view, projection):
        self.model = model;
        self.view = view;
        self.projection = projection;
        return 1;    
  

    def draw(self):
        glDepthFunc(GL_LEQUAL);  # change depth function so depth test passes when values are equal to depth buffer's content
        self.shader.use();
        #
        #self.shader.setMat4("model", glm.value_ptr(self.model));
        self.shader.setMat4("view", glm.value_ptr(self.view));
        self.shader.setMat4("projection", glm.value_ptr(self.projection));
        # skybox cube
        glBindVertexArray(self.VAO);
        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.cubemapTexture);
        #glDrawArrays(GL_POINTS, 0, 36);
        glDrawArrays(GL_TRIANGLES, 0, 36);
        glBindVertexArray(0);
        glDepthFunc(GL_LESS); # set depth function back to default
        return 1;
    

    def __del__(self):

        glDeleteVertexArrays(1, self.VAO);
        glDeleteBuffers(1, self.VBO);
    
    def loadCubemap(self, faces):

        textureID = 0;
        textureID = glGenTextures(1);
        glBindTexture(GL_TEXTURE_CUBE_MAP, textureID);

        
        for idx, name in enumerate(faces):
            img = Image.open(name) # .png, .bmp, etc. also work
            img_data = np.array(list(img.getdata()), np.int8)

            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + idx, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data);
            print ('loading {}'.format(name))
        
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE);

        return textureID;
