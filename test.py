import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import glm
from numpy.core.numeric import identity
from pygl.camera import *
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
        self.root.after(500, self.update_text, text_box);
        

    def run(self):
        self.root = tk.Tk()
        
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title('PythonGuides')
        self.root.geometry('400x300')
        self.root.config(bg='#FFFFFF')

        self.text_box = tk.Text(
                    self.root,
                    height=12,
                    width=40
                )
        
        self.text_box.pack(expand=True)
        self.text_box.tag_add("here", "1.0", tk.END)
        self.text_box.tag_config("here", background="black", foreground="green")

        self.root.after(0, self.update_text, self.text_box);
        

        self.root.mainloop()

metric_app = App();




vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 v_color;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0f);
    v_color = a_color;
}
"""

fragment_src = """
# version 330

in vec3 v_color;
out vec4 out_color;

void main()
{
    out_color = vec4(v_color, 1.0);
}
"""

# screen settings
SCR_WIDTH = 800;
SCR_HEIGHT = 600;

move_list = [False, False, False, False, False, False]

# mouse settings
first_mouse = True;
lastX = SCR_WIDTH / 2
lastY = SCR_HEIGHT / 2

# timing
deltaTime = 0.0;  # time between current frame and last frame
lastFrame = 0.0;

mouse_left_down = False;

camera = Camera(position=glm.vec3(0.0, 0.0, 3.0));


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

    camera.ProcessMouseMovement(xoffset, yoffset)

# the window resize callback function


def framebuffer_size_callback(window, width, height):
    global projection

    glViewport(0, 0, width, height)
    projection = glm.mat4.create_perspective_projection_matrix(
        45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

# the keyboard input callback


def key_input_clb(window, key, scancode, action, mode):
    global deltaTime, camera, move_list

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        #camera.ProcessKeyboard(Camera_Movement.FORWARD, deltaTime)
        move_list[int(Camera_Movement.FORWARD)] = True;
    if key == glfw.KEY_W and action == glfw.RELEASE:
        move_list[int(Camera_Movement.FORWARD)] = False;


    if key == glfw.KEY_S and action == glfw.PRESS:
        #camera.ProcessKeyboard(Camera_Movement.BACKWARD, deltaTime)
        move_list[Camera_Movement.BACKWARD] = True;
    if key == glfw.KEY_S and action == glfw.RELEASE:
        move_list[Camera_Movement.BACKWARD] = False;


    if key == glfw.KEY_A and action == glfw.PRESS:
        #camera.ProcessKeyboard(Camera_Movement.LEFT, deltaTime)
        move_list[Camera_Movement.LEFT] = True;
    if key == glfw.KEY_A and action == glfw.RELEASE:
        move_list[Camera_Movement.LEFT] = False;


    if key == glfw.KEY_D and action == glfw.PRESS:
        #camera.ProcessKeyboard(Camera_Movement.RIGHT, deltaTime)
        move_list[Camera_Movement.RIGHT] = True;
    if key == glfw.KEY_D and action == glfw.RELEASE:
        move_list[Camera_Movement.RIGHT] = False;



    if key == glfw.KEY_LEFT_SHIFT and action == glfw.PRESS:
        #camera.ProcessKeyboard(Camera_Movement.UP, deltaTime)
        move_list[Camera_Movement.UP] = True;
    if key == glfw.KEY_LEFT_SHIFT and action == glfw.RELEASE:
        move_list[Camera_Movement.UP] = False;


    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        #camera.ProcessKeyboard(Camera_Movement.DOWN, deltaTime)
        move_list[Camera_Movement.DOWN] = True;
    if key == glfw.KEY_SPACE and action == glfw.RELEASE:
        move_list[Camera_Movement.DOWN] = False;
    # if key in [glfw.KEY_W, glfw.KEY_S, glfw.KEY_D, glfw.KEY_A] and action == glfw.RELEASE:
    #     left, right, forward, backward = False, False, False, False


def process_movement():
    #call processkeyboard from here
    global delta_time, camera, move_list

    for idx, move in enumerate(move_list):
        if move == True:
            camera.ProcessKeyboard(Camera_Movement(idx), deltaTime)

def mouse_button_callback(window, button, action, mods):
    global mouse_left_down
    
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS: 
        mouse_left_down = True;
    elif button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE: 
        mouse_left_down = False;

    


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
    # capture the mouse cursor
#glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

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

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))


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

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)

rotation_loc = glGetUniformLocation(shader, "rotation")
model_loc = glGetUniformLocation(shader, "model")
view_loc = glGetUniformLocation(shader, "view")
projection_loc = glGetUniformLocation(shader, "projection")

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    currentFrame = glfw.get_time();
    deltaTime = currentFrame - lastFrame;
    lastFrame = currentFrame;

    #rot_x = glm.rotate (0.5 * glfw.get_time())
    #rot_y = glm.rotate (0.8 * glfw.get_time())
    transform = glm.mat4(1)
    transform = glm.translate(transform, glm.vec3(0, 0, -10))
    transform = glm.rotate(transform, glfw.get_time(),glm.vec3(0.5,0.8,0))
    projection = glm.perspective(glm.radians(camera.Zoom), 800 / 800, 0.1, 100)
    process_movement();
    view = camera.GetViewMatrix();
    
    metric_app.update_metrics(camera.Position, camera.Yaw, camera.Pitch);
    

    # glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x * rot_y)
    # glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x @ rot_y)
    #glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, glm.value_ptr(transform))

    identitymat = glm.mat4(1)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(transform))
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(projection_loc, 1, GL_FALSE, glm.value_ptr(projection))


    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    #glDrawElements(GL_LINES, len(indices), GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()