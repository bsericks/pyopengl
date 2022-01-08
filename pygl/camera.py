import glm
from math import sin, cos

# Defines several possible options for camera movement. Used as abstraction to stay away from window-system specific input methods
from enum import IntEnum

from numpy.lib.histograms import _ravel_and_check_weights
class Camera_Movement(IntEnum):
    FORWARD = 0
    BACKWARD = 1
    LEFT = 2 
    RIGHT = 3
    UP = 4
    DOWN = 5
    ROLL_LEFT = 6
    ROLL_RIGHT = 7


# Default camera values
YAW         = -90.0
PITCH       =  0.0
SPEED       =  5
SENSITIVITY =  0.005
ZOOM        =  45.0

class Camera:

    # camera Attributes
    Position = glm.vec3
    Front = glm.vec3 
    Up = glm.vec3 
    Right = glm.vec3 
    WorldUp = glm.vec3 
    # euler Angle
    Yaw = -90.0
    Pitch = 0.0
    Roll = 0.0
    # camera option
    MovementSpeed = SPEED
    MouseSensitivity = 0.05
    Zoom = 45.0

    # constructor with vectors
    def __init__(self, position = glm.vec3(0.0, 0.0, 0.0), up = glm.vec3(0.0, 1.0, 0.0), yaw = YAW, pitch = PITCH):
    
        Front = glm.vec3(0.0, 0.0, -1.0)
        Right = glm.vec3(0.0, -1.0, 0.0)
        MovementSpeed = SPEED
        MouseSensitivity = SENSITIVITY
        Zoom = ZOOM

        self.Position = position;
        self.WorldUp = up;
        self.Up = up;
        self.Yaw = yaw;
        self.Pitch = pitch;
        self.updateCameraVectors();
    

    # returns the view matrix calculated using Euler Angles and the LookAt Matrix
    def GetViewMatrix(self):
        return glm.lookAt(self.Position, self.Position + self.Front, self.Up);

    # processes input received from any keyboard-like input system. Accepts input parameter in the form of camera defined ENUM (to abstract it from windowing systems)
    def ProcessKeyboard(self, direction, deltaTime):
    
        velocity = self.MovementSpeed * deltaTime;
        if (direction == Camera_Movement.FORWARD):
            self.Position += self.Front * velocity;
        if (direction == Camera_Movement.BACKWARD):
            self.Position -= self.Front * velocity;
        if (direction == Camera_Movement.LEFT):
            self.Position -= self.Right * velocity;
        if (direction == Camera_Movement.RIGHT):
            self.Position += self.Right * velocity;
        if (direction == Camera_Movement.ROLL_LEFT):
            self.Roll -= 1
        if (direction == Camera_Movement.ROLL_RIGHT):
            self.Roll += 1
        if (direction == Camera_Movement.UP):
            self.Position += self.Up * velocity;
        if (direction == Camera_Movement.DOWN):
            self.Position -= self.Up * velocity;
        
        self.updateCameraVectors();
    

    # processes input received from a mouse input system. Expects the offset value in both the x and y direction.
    def ProcessMouseMovement(self, xoffset, yoffset, constrainPitch = True):
    
        xoffset *= self.MouseSensitivity;
        yoffset *= self.MouseSensitivity;

        self.Yaw   += xoffset*cos(glm.radians(self.Roll)) + yoffset*sin(glm.radians(self.Roll));
        self.Pitch += yoffset*cos(glm.radians(self.Roll)) - xoffset*sin(glm.radians(self.Roll))

        # make sure that when pitch is out of bounds, screen doesn't get flipped
        if (constrainPitch):

            if (self.Pitch > 89.0):
                self.Pitch = 89.0

            if (self.Pitch < -89.0):
                self.Pitch = -89.0
        

        # update Front, Right and Up Vectors using the updated Euler angles
        self.updateCameraVectors();
    

    # processes input received from a mouse scroll-wheel event. Only requires input on the vertical wheel-axis
    def ProcessMouseScroll(self, yoffset):
    
        self.Zoom -= yoffset;
        if (self.Zoom < 1.0):
            self.Zoom = 1.0
        if (self.Zoom > 45.0):
            self.Zoom = 45.0 
    

    # calculates the front vector from the Camera's (updated) Euler Angles
    def updateCameraVectors(self):
    
        roll = 45
        # calculate the new Front vector
        front = glm.vec3();
        front.x = cos(glm.radians(self.Yaw)) * cos(glm.radians(self.Pitch))
        front.y = sin(glm.radians(self.Pitch))
        front.z = sin(glm.radians(self.Yaw)) * cos(glm.radians(self.Pitch))

        self.Front = glm.normalize(front);
        # also re-calculate the Right and Up vector
        

        if True:
            self.Right = glm.normalize(glm.cross(self.Front, self.WorldUp));  # normalize the vectors, because their length gets closer to 0 the more you look up or down which results in slower movement.
        
            self.Up    = glm.normalize(glm.cross(self.Right, self.Front));

        if False:
            #roll_mat = glm.rotate(glm.mat4(1.0), glm.radians(roll), self.Front);
            #self.Up = glm.mat3(roll_mat) * self.Up;

            right = glm.vec3();
            right.x = cos(glm.radians(self.Yaw))   * sin(glm.radians(self.Pitch))*sin(glm.radians(roll)) - sin(glm.radians(self.Yaw))*cos(glm.radians(roll))
            right.y = sin(glm.radians(self.Yaw))   * sin(glm.radians(self.Pitch))*sin(glm.radians(roll)) + cos(glm.radians(self.Yaw))*cos(glm.radians(roll))
            right.z = cos(glm.radians(self.Pitch)) * cos(glm.radians(roll))
   
            self.Right = glm.normalize(right)
   
            up = glm.vec3();
            up.x = cos(glm.radians(self.Yaw))   * sin(glm.radians(self.Pitch))*cos(glm.radians(roll)) + sin(glm.radians(self.Yaw))*sin(glm.radians(roll))
            up.y = sin(glm.radians(self.Yaw))   * sin(glm.radians(self.Pitch))*cos(glm.radians(roll)) - cos(glm.radians(self.Yaw))*sin(glm.radians(roll))
            up.z = cos(glm.radians(self.Yaw))   * cos(glm.radians(roll))
   
            self.Up = glm.normalize(up)

        if True:
            roll_mat = glm.rotate(glm.mat4(1.0), glm.radians(self.Roll), self.Front);
            self.Right = glm.mat3(roll_mat) * self.Right;
            self.Up = glm.mat3(roll_mat) * self.Up;