import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import glm
from numpy.core.numeric import identity
from pygl.camera import *
from pygl.shader import *
from pygl.skybox import *
from OpenGL.GLUT import *

import tkinter as tk
import threading



class App(threading.Thread):

    yawmetric = 0.0
    pitchmetric = 0.0
    positionmetric = glm.vec3(0,0,0);

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def update_metrics(self, position, yaw, pitch):
        self.positionmetric = position
        self.yawmetric = yaw
        self.pitchmetric = pitch

    def callback(self):
        self.root.quit()

    def update_text(self, text_box):
        text_box.delete(0.0, tk.END)
        text_box.insert(tk.END, 'X: {}\n'.format(self.positionmetric[0]))
        text_box.insert(tk.END, 'Y: {}\n'.format(self.positionmetric[1]))
        text_box.insert(tk.END, 'Z: {}\n'.format(self.positionmetric[2]))
        text_box.insert(tk.END, 'Yaw: {}\n'.format(self.yawmetric))
        text_box.insert(tk.END, 'Pitch: {}\n'.format(self.pitchmetric))

        self.text_box.tag_add("here", "1.0", tk.END)
        self.text_box.tag_config("here", background="black", foreground="green")
        
        self.root.after(500, self.update_text, text_box);
        

    def run(self):
        self.root = tk.Tk()
        
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title('PythonGuides')
        self.root.geometry('400x150')
        self.root.config(bg='#FFFFFF')

        self.text_box = tk.Text(
                    self.root,
                    height=12,
                    width=40
                )
        
        self.text_box.pack(expand=True)
        

        self.root.after(0, self.update_text, self.text_box);
        

        self.root.mainloop()

metric_app = App();


# screen settings
SCR_WIDTH = 800;
SCR_HEIGHT = 600;

move_list = [False, False, False, False, False, False, False, False]

# mouse settings
first_mouse = True;
lastX = SCR_WIDTH / 2
lastY = SCR_HEIGHT / 2

# timing
deltaTime = 0.0;  # time between current frame and last frame
lastFrame = 0.0;

mouse_left_down = False;

camera = Camera(position=glm.vec3(1.0, 1.0, 10.0));


projection = glm.perspective(45, SCR_WIDTH / SCR_HEIGHT, 0.1, 100)


def scroll_callback(window, xoffset, yoffset):
    camera.ProcessMouseScroll(yoffset);


# the mouse position callback function
def mouse_callback(window, xpos, ypos):
    global first_mouse, lastX, lastY, camera, mouse_left_down
    
    if mouse_left_down == False:
        return;

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos
    
    lastX = xpos
    lastY = ypos
 
    #constrain jumpyness when clicking
    if abs(xoffset) < 100 and abs(yoffset) < 100:
        camera.ProcessMouseMovement(xoffset, yoffset)

# the window resize callback function
def framebuffer_size_callback(window, width, height):
    global projection, SCR_WIDTH, SCR_HEIGHT

    glViewport(0, 0, width, height)
    SCR_WIDTH = width;
    SCR_HEIGHT = height;

# the keyboard input callback
def key_input_clb(window, key, scancode, action, mode):
    global deltaTime, camera, move_list

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        move_list[int(Camera_Movement.FORWARD)] = True;
    if key == glfw.KEY_W and action == glfw.RELEASE:
        move_list[int(Camera_Movement.FORWARD)] = False;


    if key == glfw.KEY_S and action == glfw.PRESS:
        move_list[Camera_Movement.BACKWARD] = True;
    if key == glfw.KEY_S and action == glfw.RELEASE:
        move_list[Camera_Movement.BACKWARD] = False;


    if key == glfw.KEY_A and action == glfw.PRESS:
        move_list[Camera_Movement.LEFT] = True;
    if key == glfw.KEY_A and action == glfw.RELEASE:
        move_list[Camera_Movement.LEFT] = False;


    if key == glfw.KEY_D and action == glfw.PRESS:
        move_list[Camera_Movement.RIGHT] = True;
    if key == glfw.KEY_D and action == glfw.RELEASE:
        move_list[Camera_Movement.RIGHT] = False;

    if key == glfw.KEY_Q and action == glfw.PRESS:
        move_list[Camera_Movement.ROLL_LEFT] = True;
    if key == glfw.KEY_Q and action == glfw.RELEASE:
        move_list[Camera_Movement.ROLL_LEFT] = False;

    if key == glfw.KEY_E and action == glfw.PRESS:
        move_list[Camera_Movement.ROLL_RIGHT] = True;
    if key == glfw.KEY_E and action == glfw.RELEASE:
        move_list[Camera_Movement.ROLL_RIGHT] = False;


    if key == glfw.KEY_LEFT_SHIFT and action == glfw.PRESS:
        move_list[Camera_Movement.UP] = True;
    if key == glfw.KEY_LEFT_SHIFT and action == glfw.RELEASE:
        move_list[Camera_Movement.UP] = False;


    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        move_list[Camera_Movement.DOWN] = True;
    if key == glfw.KEY_SPACE and action == glfw.RELEASE:
        move_list[Camera_Movement.DOWN] = False;


def process_movement():
    #call processkeyboard from here
    global delta_time, camera, move_list

    for idx, move in enumerate(move_list):
        if move == True:
            camera.ProcessKeyboard(Camera_Movement(idx), deltaTime)

def mouse_button_callback(window, button, action, mods):
    global mouse_left_down, lastX, lastY
    
    glfw.set_cursor_pos(window, SCR_WIDTH/2, SCR_HEIGHT/2)

    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS: 
        mouse_left_down = True;
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        
    elif button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE: 
        mouse_left_down = False;
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
        
    
    lastX, lastY = glfw.get_cursor_pos(window);


def window_resize(window, width, height):
    glViewport(0, 0, width, height)

# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 600, 600)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)

# make the context current
glfw.make_context_current(window)

glfw.make_context_current(window);
glfw.set_framebuffer_size_callback(window, framebuffer_size_callback);
glfw.set_cursor_pos_callback(window, mouse_callback);
glfw.set_scroll_callback(window, scroll_callback);
glfw.set_mouse_button_callback(window, mouse_button_callback);
    
glfw.set_key_callback(window, key_input_clb)
    

glEnable(GL_DEPTH_TEST);

vertices = [-0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, 0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5, 0.5, 1.0, 1.0, 1.0,

            -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
             0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5, -0.5, 1.0, 1.0, 1.0]

indices = [0, 1, 2, 2, 3, 0,
           4, 5, 6, 6, 7, 4,
           4, 5, 1, 1, 0, 4,
           6, 7, 3, 3, 2, 6,
           5, 6, 2, 2, 1, 5,
           7, 4, 0, 0, 3, 7]

#vertices = [-0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
#             0.5, -0.5, 0.5, 0.0, 1.0, 0.0]

#indices = [0, 1]

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

shader = Shader()    



vao = glGenVertexArrays( 1 );
glBindVertexArray( vao );

# Vertex Buffer Object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Element Buffer Object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

glBindBuffer(GL_ARRAY_BUFFER, 0); 
glBindVertexArray(0); 

shader.use()
glClearColor(0, 0.1, 0.1, 1)

from pygl.line import *

line_shader = Shader(vertexPath='data/lineShader.vs', fragmentPath='data/lineShader.fs')

x_axis = Line(glm.vec3(50, 0, 0), glm.vec3(49,0,0), line_shader)
x_axis.setColor(glm.vec3(1.0,1.0,0))
y_axis = Line(glm.vec3(0, 50, 0), glm.vec3(0,0,0), line_shader)
y_axis.setColor(glm.vec3(0.0,1.0,1.0))
z_axis = Line(glm.vec3(0, 0, 50), glm.vec3(0,0,0), line_shader)
z_axis.setColor(glm.vec3(1.0,0.0,1.0))

x_grid_lines = []
z_grid_lines = []

for a in range(11):
    x_grid_lines.append(Line(glm.vec3(100, 0, 0), glm.vec3(-100,0,0), line_shader))
    z_grid_lines.append(Line(glm.vec3(0, 0, 100), glm.vec3(0,0,-100), line_shader))

glLineWidth(2.0);

from pygl.skybox import *

skybox = Skybox();

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);  


    currentFrame = glfw.get_time();
    deltaTime = currentFrame - lastFrame;
    lastFrame = currentFrame;

    projection = glm.perspective(glm.radians(camera.Zoom), SCR_WIDTH / SCR_HEIGHT, 0.1, 200)

    glDepthMask(GL_FALSE);
    view = glm.mat4(glm.mat3(camera.GetViewMatrix())); # remove translation from the view matrix
    skybox.setMVP(glm.mat4(1), view, projection);
    skybox.draw()
    glDepthMask(GL_TRUE);


    transform = glm.mat4(1)
    transform = glm.translate(transform, glm.vec3(0, 0, 0))
    transform = glm.rotate(transform, glfw.get_time(),glm.vec3(0.5,0.8,0))
    
    process_movement();
    view = camera.GetViewMatrix();
    
    metric_app.update_metrics(camera.Position, camera.Yaw, camera.Pitch);
    
    identitymat = glm.mat4(1)
    shader.use()
    shader.setMat4('model', glm.value_ptr(transform))
    shader.setMat4('view', glm.value_ptr(view))
    shader.setMat4('projection', glm.value_ptr(projection))

   
    glBindVertexArray( vao );
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    #glDrawElements(GL_LINES, len(indices), GL_UNSIGNED_INT, None)

    #transform = glm.mat4(1)
    #transform = glm.translate(transform, glm.vec3(0, 0, 0))
    x_axis.setMVP(glm.mat4(1), view, projection);
    x_axis.draw();

    #transform = glm.mat4(1)
    #transform = glm.translate(transform, glm.vec3(0, 0, 2))
    y_axis.setMVP(glm.mat4(1), view, projection);
    y_axis.draw();

    z_axis.setMVP(glm.mat4(1), view, projection);
    z_axis.draw();

    for a in range(11):
        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(-50, 0, -50+(a*10)))
        x_grid_lines[a].setMVP(transform, view, projection)
        x_grid_lines[a].draw();

        transform = glm.mat4(1)
        transform = glm.translate(transform, glm.vec3(-50+(a*10), 0, -50))
        z_grid_lines[a].setMVP(transform, view, projection)
        z_grid_lines[a].draw();
        
    


    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()