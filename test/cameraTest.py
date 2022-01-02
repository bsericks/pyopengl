import glm
import glfw
from pygl.camera import *
from pygl.shader import *
import sys
import numpy as np

#If we're running from the test directory, this finds the modules in pygl
sys.path.append('./../')


# screen settings
SCR_WIDTH = 800;
SCR_HEIGHT = 600;


# mouse settings
first_mouse = True;
lastX = SCR_WIDTH / 2
lastY = SCR_HEIGHT / 2

# timing
deltaTime = 0.0;  # time between current frame and last frame
lastFrame = 0.0;


camera = Camera(position=glm.vec3(0.0, 0.0, 3.0));


projection = glm.perspective(45, SCR_WIDTH / SCR_HEIGHT, 0.1, 100)


def scroll_callback(window, xoffset, yoffset):
    camera.ProcessMouseScroll(yoffset);


# the mouse position callback function
def mouse_callback(window, xpos, ypos):
    global first_mouse, lastX, lastY, camera

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
    global deltaTime, camera

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        camera.ProcessKeyboard(Camera_Movement.FORWARD, deltaTime)
    if key == glfw.KEY_S and action == glfw.PRESS:
        camera.ProcessKeyboard(Camera_Movement.FORWARD, deltaTime)
    if key == glfw.KEY_A and action == glfw.PRESS:
        camera.ProcessKeyboard(Camera_Movement.FORWARD, deltaTime)
    if key == glfw.KEY_D and action == glfw.PRESS:
        camera.ProcessKeyboard(Camera_Movement.FORWARD, deltaTime)
    # if key in [glfw.KEY_W, glfw.KEY_S, glfw.KEY_D, glfw.KEY_A] and action == glfw.RELEASE:
    #     left, right, forward, backward = False, False, False, False



############################################ object data #######################################


slices = 10

vertices = np.empty(shape=((slices+1) * (slices+1) * 3), dtype=int)
indices = np.empty(shape=((slices) * (slices) * 2 * 4), dtype=int)

vertex_index=0
for j in range (slices+1):
    for i in range (slices+1):
        x = i/slices;
        y = 0;
        z = j/slices;
        vertices[vertex_index] = x;
        vertex_index = vertex_index+1
        vertices[vertex_index] = y;
        vertex_index = vertex_index+1
        vertices[vertex_index] = z;
        vertex_index = vertex_index+1
        

indices_index=0
for j in range (slices):
    for i in range (slices):
        row1 =  j    * (slices+1);
        row2 = (j+1) * (slices+1);

        #indices.append(glm.uvec4(row1+i, row1+i+1, row1+i+1, row2+i+1));
        indices[indices_index] = row1+i; indices_index = indices_index+1;
        indices[indices_index] = row1+i+1; indices_index = indices_index+1
        indices[indices_index] = row1+i+1; indices_index = indices_index+1
        indices[indices_index] = row2+i+1; indices_index = indices_index+1
        
        #indices.append(glm.uvec4(row2+i+1, row2+i, row2+i, row1+i));
        indices[indices_index] = row2+i+1; indices_index = indices_index+1;
        indices[indices_index] = row2+i; indices_index = indices_index+1
        indices[indices_index] = row2+i; indices_index = indices_index+1
        indices[indices_index] = row1+i; indices_index = indices_index+1
        




def main():

     # glfw: initialize and configure
    # ------------------------------
    glfw.init();
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3);
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3);
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE);

    

    # glfw window creation
    # --------------------
    window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", None, None);

    if (window == None):
        print("Failed to create GLFW window");
        glfw.terminate();
        return -1;
    
    glfw.make_context_current(window);
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback);
    glfw.set_cursor_pos_callback(window, mouse_callback);
    glfw.set_scroll_callback(window, scroll_callback);
    
    glfw.set_key_callback(window, key_input_clb)
    # capture the mouse cursor
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    shader = Shader()
    shader.use()
    
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

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

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

    #vao = glGenVertexArrays( 1 );
    #glBindVertexArray( vao );
#
    #vbo = glGenBuffers( 1 );
    #glBindBuffer( GL_ARRAY_BUFFER, vbo );
    #glBufferData( GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW );
#
    #glEnableVertexAttribArray( 0 );
    #glVertexAttribPointer( 0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0) );

    length = len(indices);

    
    glEnable(GL_DEPTH_TEST);

    lastFrame = 0;

    running = True
    while not glfw.window_should_close(window):

        # render
        # ------
        glClearColor(0.2, 0.3, 0.3, 1.0);
        glClear(GL_COLOR_BUFFER_BIT);

        currentFrame = glfw.get_time();
        deltaTime = currentFrame - lastFrame;
        lastFrame = currentFrame;
        
        projection = glm.perspective(45, SCR_WIDTH / SCR_HEIGHT, 0.1, 100)

        shader.setMat4("projection", projection)

        view = camera.GetViewMatrix();
        shader.setMat4("view", view);

        

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0.0, 0.0, 0.0));
        shader.setMat4("model", model)


        #glBindVertexArray(vao);

        #glDrawElements(GL_LINES, length, GL_UNSIGNED_INT, ctypes.c_void_p(0));
        glDrawArrays(GL_POINTS, 0, 8)

        #glBindVertexArray(0);

           
        glfw.poll_events()
        glfw.swap_buffers(window)





main();
