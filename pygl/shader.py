from OpenGL.GL import *
from OpenGL.GLU import *


class Shader():


    program_id = 0;
    # 1. retrieve the vertex/fragment source code from filePath
    

    def __init__(self, vertexPath='data/vertexShader.glsl', fragmentPath='data/fragmentShader.glsl'):

        vertexCode = '';
        fragmentCode = '';

        try:
            with open(vertexPath,'r',newline='') as rf:
                vertexCode = rf.read()

            with open(fragmentPath,'r',newline='') as rf:
                fragmentCode = rf.read()

        except:
            print("could not open files")

        
        vs_id = self.add_shader(vertexCode, GL_VERTEX_SHADER)
        frag_id = self.add_shader(fragmentCode, GL_FRAGMENT_SHADER)

        self.program_id = glCreateProgram()
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

    def use(self):
        glUseProgram(self.program_id); 

    def setBool(self, name, value):
        glUniform1i(glGetUniformLocation(self.program_id, name), value); 

    def setInt(self, name, value):
        glUniform1i(glGetUniformLocation(self.program_id, name), value); 
    
    def setFloat(self, name, value): 
        glUniform1f(glGetUniformLocation(self.program_id, name), value); 

    #def setVec2(self, name, value):
    #    glUniform2fv(glGetUniformLocation(self.program_id, name), 1, value[0]); 
    
    def setVec2(self, name, x, y):
        glUniform2f(glGetUniformLocation(self.program_id, name), x, y); 
    
    #def setVec3(self, name, value):
    #    glUniform3fv(glGetUniformLocation(self.program_id, name), 1, value[0]); 
    
    def setVec3(self, name, x, y, z):
        glUniform3f(glGetUniformLocation(self.program_id, name), x, y, z); 

    #def setVec4(self, name, value):
    #    glUniform4fv(glGetUniformLocation(self.program_id, name), 1, value[0]); 
    
    def setVec4(self, name, x, y, z, w):
        glUniform4f(glGetUniformLocation(self.program_id, name), x, y, z, w); 
    
    def setMat2(self, name, mat): 
        glUniformMatrix2fv(glGetUniformLocation(self.program_id, name), 1, GL_FALSE, mat);
    
    def setMat3(self, name, mat):
        glUniformMatrix3fv(glGetUniformLocation(self.program_id, name), 1, GL_FALSE, mat);
    
    def setMat4(self, name, mat):
        glUniformMatrix4fv(glGetUniformLocation(self.program_id, name), 1, GL_FALSE, mat);
    

    def __del__(self):
        glDeleteProgram(self.program_id);
    