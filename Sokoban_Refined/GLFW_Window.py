import glfw

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from abc import abstractmethod

# User defined.
from ShaderHandler import ShaderHandler

class GLFW_Keyboard_Input:
    @abstractmethod
    def w_pressed(self):
        pass
    @abstractmethod
    def a_pressed(self):
        pass
    @abstractmethod
    def s_pressed(self):
        pass
    @abstractmethod
    def d_pressed(self):
        pass

def GLFW_keyboardInputCallback(window, key, scancode, action, mode):
    if key == glfw.KEY_W and action == glfw.PRESS:
        GLFW_Keyboard_Input.w_pressed()
    if key == glfw.KEY_A and action == glfw.PRESS: 
        GLFW_Keyboard_Input.a_pressed()
    if key == glfw.KEY_S and action == glfw.PRESS: 
        GLFW_Keyboard_Input.s_pressed()
    if key == glfw.KEY_D and action == glfw.PRESS: 
        GLFW_Keyboard_Input.d_pressed()

class GLFW_Window:
    def __init__(self, WIDTH, HEIGHT, TITLE):
        """_fields:_
            (window_refer) is a refer to the GLFWwindow object created.
            (window_width) is a length of width of GLFWwindow.
            (window_height) is a length of height of GLFWwindow.
            (window_title) is a title of GLFWwindow.
        """
        
        # Initialize GLFW.
        if not glfw.init():
            raiseError("glfw.init() failed")
        
        # Create GLFW window.
        window = glfw.create_window(WIDTH, HEIGHT, TITLE, None, None)
        
        # Check if GLFW window is created. if not, terminate process.
        if not window:
            glfw.terminate()
            raiseError("glfw.create_window() failed")
        
        # Setup key input callback function.
        glfw.set_key_callback(window, GLFW_keyboardInputCallback)
        # Make window context current. 
        glfw.make_context_current(window)
        
        # Providing fields for further access...
        self.window_refer = window
        self.window_width = WIDTH
        self.window_height = HEIGHT
        self.window_title = TITLE
        

    
    def run(self):
        while not glfw.window_should_close(self.window_refer):
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT)
            
            offFlag = self.loop()
            if offFlag: break
            
            glfw.swap_buffers(self.window_refer)
        
        glfw.terminate()
    
    @abstractmethod
    def setup(self):
        pass
    
    @abstractmethod
    def loop(self):
        pass
    
class OpenGL_Window(GLFW_Window):
    def setShaderProgram(self, vertexShaderSourcePath: str
                         , fragmentShaderSourcePath: str):
        shaderProgramHandler = ShaderHandler(vertexShaderSourcePath
                                            , fragmentShaderSourcePath)
        self.shaderProgram = shaderProgramHandler.getProgram()
