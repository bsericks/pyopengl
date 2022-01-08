# pyLearnOpenGL
Project utilizing lessons from https://learnopengl.com/Getting-started/OpenGL translated to Python. This project uses modern OpenGL development (3.0+).

## Current Features
* shader class for loading vertex and fragment shaders
* camera class implementing a modified 'FPS' style camera with roll
* line class implementing a simple drawn line object, used in the demo for making grid/axis lines
* skybox class implementing a cubemap to render a 'milky way' background
* Tkinter window running on a separate thread, outputting periodic camera metrics for debugging purposes

## Running
``` 
> python demo.py
```

Controls: 
* W/A/S/D = move forward/backward/left/right
* Q/E = roll left/right
* mouse click and drag = yaw/pitch camera (adjusts with camera roll to change yaw/pitch relative to current camera orientation)

![Alt Text](./data/giphy.gif)

## Requirements
* python 3+
* OpenGL
* pyglm
* glfw
* numpy
* tkinter
* PIL
* threading