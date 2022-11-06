import glfw
import pyrr
import numpy as np

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from abc import abstractmethod

# User defined. 
from GLFW_Window import OpenGL_Window
from Tile import Tile
from DirectEnumerator import DirectEnumerator

# 전역 함수
def raiseError(self, msg: str):
    print(msg)
    
class Wall(Tile):
    def do_when_pushed_by(self, dx, dy):
        return
    
    def display(self):
        return pyrr.Vector3([230/255, 230/255, 0/255])

class Space(Tile):
    def do_when_pushed_by(self, dx, dy):
        return
    def display(self):
        return pyrr.Vector3([  0/255,  26/255, 0/255])

class Stage:
    stageMap = [Wall(0, 0), Wall(1, 0), Wall(2, 0)
                , Wall(0, 1), Space(1, 1), Wall(2, 1)
                , Wall(0, 2), Wall(1, 2), Wall(2, 2)]
    height = 3
    width = 3
    
    def display(self, modelLocation, colorLocation):
        x, y = 0, 0
        edge = 0.125
        for tile in self.stageMap:
            if x % self.width == 0:
                x, y = 0, y+1
                
            translationMatrix = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1 + edge*(x), 1 - edge*(y), 0]))
            colorVector = tile.display()
            
            glUniformMatrix4fv(modelLocation, 1, GL_FALSE, translationMatrix)
            glUniform3fv(colorLocation, 1, colorVector)
            
            glDrawArrays(GL_TRIANGLE_STRIP, 0, 6)
            
            x += 1
    
global STAGE            
STAGE = Stage()      

class SokobanGame(OpenGL_Window):
    def setup(self):
        edge = 0.125
        square = np.array([  0.0,  0.0, 0.0, 0.0, 0.0, 0.0, \
                            edge,  0.0, 0.0, 0.0, 0.0, 0.0, \
                             0.0, edge, 0.0, 0.0, 0.0, 0.0, \
                            edge,  0.0, 0.0, 0.0, 0.0, 0.0, \
                             0.0, edge, 0.0, 0.0, 0.0, 0.0, \
                            edge, edge, 0.0, 0.0, 0.0, 0.0 ], dtype=np.float32)
        
        VBO = glGenBuffers(1)
        
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, square.nbytes, square, GL_STATIC_DRAW)
        
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        
        self.modelUniformLocation = glGetUniformLocation(self.shaderProgram, "model")
        self.colorUniformLocation = glGetUniformLocation(self.shaderProgram, "tileColor")
        
    def loop(self):
        glClearColor(  0/255,  26/255, 0/255, 1)
        # if STAGE.win(): print("win!")
        STAGE.display(self.modelUniformLocation, self.colorUniformLocation)
        
game = SokobanGame(800, 800, "Sokoban")
game.setShaderProgram("vShader.vs", "fShader.fs")
game.setup()
game.run()