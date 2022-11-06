import glfw
import pyrr
import numpy as np

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from enum import Enum

import time

class DirectEnumerator(str, Enum):
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name
    
class TILE(DirectEnumerator):
    SPACE = 0
    WALL = 1
    DESTINATION = 2
    BOX = 3
    BOX_ON_DESTINATION = 4
    PROTAGONIST = 5
    PROTAGONIST_ON_DESTINATION = 6
    
    NULL = 8

class Stage:
    def __init__(self, stageFilePath: str):
        self.stageFilePath = stageFilePath
        self.stage = list()
        
        self.WIDTH = 0
        self.HEIGHT = 0
        
        self.protagonistX = 0
        self.protagonistY = 0
        
        self.readStageFile(self.stageFilePath)
        
    def readStageFile(self, path: str):
        stageFile = open(path, 'r')
        stage = list()
        
        count = 0
        protagonistCount = 0
        
        while True:
            line = stageFile.readline()
            if not line:
                break
            else: self.HEIGHT += 1

            for symbol in line:
                count += 1
                tile = TILE.NULL
                if symbol == " ":
                    tile = TILE.SPACE
                elif symbol == "#":
                    tile = TILE.WALL
                elif symbol == ".":
                    tile = TILE.DESTINATION
                elif symbol == "o":
                    tile = TILE.BOX
                elif symbol == "O":
                    tile = TILE.BOX_ON_DESTINATION
                elif symbol == "p":
                    tile = TILE.SPACE
                    protagonistCount = count
                elif symbol == "P":
                    tile = TILE.DESTINATION
                    protagonistCount = count
                else:
                    count -= 1
                    continue;
                stage.append(tile)

        stageFile.close()
        
        self.stage = stage
        self.protagonistX = protagonistCount % self.HEIGHT - 1
        self.protagonistY = int(protagonistCount / self.HEIGHT)
        
        self.WIDTH = int(count/self.HEIGHT)
        
        return
        
    def tile(self, x, y):
        return self.stage[y * self.WIDTH + x]
        
    def update(self, moveX: int, moveY: int):
        # Process movement 
        currentX = self.protagonistX
        currentY = self.protagonistY
        
        nextX = currentX + moveX
        nextY = currentY + moveY
        
        nnextX = nextX + moveX
        nnextY = nextY + moveY
        
        # move 
        if self.tile(nextX, nextY) == TILE.WALL:
            return
        if self.tile(nextX, nextY) == TILE.SPACE or self.tile(nextX, nextY) == TILE.DESTINATION:
            self.protagonistX = nextX
            self.protagonistY = nextY
            return
        if self.tile(nextX, nextY) == TILE.BOX:
            if self.tile(nnextX, nnextY) == TILE.SPACE:
                self.stage[nnextY * self.WIDTH + nnextX] = TILE.BOX
                self.stage[nextY * self.WIDTH + nextX] = TILE.SPACE         
            elif self.tile(nnextX, nnextY) == TILE.DESTINATION:
                self.stage[nnextY * self.WIDTH + nnextX] = TILE.BOX_ON_DESTINATION
                self.stage[nextY * self.WIDTH + nextX] = TILE.SPACE
            self.protagonistX = nextX
            self.protagonistY = nextY
            return           
        if self.tile(nextX, nextY) == TILE.BOX_ON_DESTINATION:
            if self.tile(nextX, nnextY) == TILE.SPACE:
                self.stage[nnextY * self.WIDTH + nnextX] = TILE.BOX
                self.stage[nextY * self.WIDTH + nextX] = TILE.DESTINATION
            elif self.tile(nnextX, nnextY) == TILE.DESTINATION:
                self.stage[nnextY * self.WIDTH + nnextX] = TILE.BOX_ON_DESTINATION
                self.stage[nextY * self.WIDTH + nextX] = TILE.DESTINATION
            self.protagonistX = nextX
            self.protagonistY = nextY
            return
        return
        
    def win(self):
        for symbol in self.stage:
            if symbol == TILE.DESTINATION:
                return False
        return True
    
    def display(self, modelLocation, colorLocation, edge):
        symbolCount = 0
        for symbol in self.stage:
            x = symbolCount%self.HEIGHT
            y = int(symbolCount/self.HEIGHT)
            
            translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1 + edge * (x), 1 - edge * (y+1), 0]))
            glUniformMatrix4fv(modelLocation, 1, GL_FALSE, translation);
            
            if symbol == TILE.SPACE:
                glUniform3fv(colorLocation, 1, pyrr.Vector3([    0.0,  26/255,     0.0]))
            elif symbol == TILE.WALL:
                glUniform3fv(colorLocation, 1, pyrr.Vector3([230/255, 230/255,     0.0]))
            elif symbol == TILE.DESTINATION:
                glUniform3fv(colorLocation, 1, pyrr.Vector3([204/255, 204/255, 204/255]))
            elif symbol == TILE.BOX:
                glUniform3fv(colorLocation, 1, pyrr.Vector3([153/255, 153/255, 102/255]))
            elif symbol == TILE.BOX_ON_DESTINATION:
                glUniform3fv(colorLocation, 1, pyrr.Vector3([ 61/255,  61/255,  41/255]))
            else:
                continue
            
            glDrawArrays(GL_TRIANGLE_STRIP, 0, 6)
            symbolCount += 1
                    
        translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1 + edge * (self.protagonistX), 1 - edge * (self.protagonistY + 1), 0]))
        glUniformMatrix4fv(modelLocation, 1, GL_FALSE, translation)
        protagonistColor = pyrr.Vector3([0.0, 0.0, 0.0])
        
        if self.tile(self.protagonistX, self.protagonistY) == TILE.DESTINATION: 
            protagonistColor = pyrr.Vector3([153/255, 31/255, 0])
        else:
            protagonistColor = pyrr.Vector3([255/255, 51/255, 0])
            
        glUniform3fv(colorLocation, 1, protagonistColor)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 6)
        
        return 

global stage
def keyboardInputCallback(self, key, scancode, action, mode):
    if key == glfw.KEY_W and action == glfw.PRESS:
        stage.update( 0, -1)
    if key == glfw.KEY_A and action == glfw.PRESS: 
        stage.update(-1,  0)
    if key == glfw.KEY_S and action == glfw.PRESS: 
        stage.update( 0,  1)
    if key == glfw.KEY_D and action == glfw.PRESS: 
        stage.update( 1,  0)

class Sokoban:
    def __init__(self, WIDTH: int, HEIGHT: int, TITLE: str):
        global stage
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.TITLE = TITLE
        
        if not glfw.init():
            raise Exception("glfw.init() failed")
        
        window = glfw.create_window(WIDTH, HEIGHT, TITLE, None, None)
        
        if not window:
            glfw.terminate()
            raise Exception("glfw.create_window() failed")
        
        glfw.set_key_callback(window, keyboardInputCallback)
        glfw.make_context_current(window)
        
        self.window = window
        
        stage = Stage("Stage01.txt")
        
    def __del__(self):
        glfw.terminate()
    
    def setShader(self, shaderPath: str, shaderType: int):
        """
            shaderType: 
                (0) vertex shader
                (1) fragment shader
                (default) raise Error
        """
        shaderFile = open(shaderPath, 'r')
        shader = list()
        
        while True:
            if not (line := shaderFile.readline()): break
            shader.append(line)
        
        shaderSource = ''.join(shader)
        
        shaderCompileType = -1
        if shaderType == 0: shaderCompileType = GL_VERTEX_SHADER
        elif shaderType == 1: shaderCompileType = GL_FRAGMENT_SHADER
        else: raise Exception("unable shader type error")
        
        compiledShaderRefer = compileShader(shaderSource, shaderCompileType)
        
        return compiledShaderRefer
        
    def setShaderProgram(self, vShaderPath: str, fShaderPath: str):
        vShaderRefer = self.setShader(vShaderPath, 0)
        fShaderRefer = self.setShader(fShaderPath, 1)
        
        shaderProgramRefer = compileProgram(vShaderRefer, fShaderRefer)
        glUseProgram(shaderProgramRefer)
        
        self.shaderProgram = shaderProgramRefer
        
    def initialSetup(self, nSquares: int):
        """
            Set up OpenGL shape (square)
        """
        edge = 0.125
        self.edge = edge
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

        self.modelLocation = glGetUniformLocation(self.shaderProgram, "model")
        self.colorLocation = glGetUniformLocation(self.shaderProgram, "tileColor")
        
    def start(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            
            glClear(GL_COLOR_BUFFER_BIT)
            glClearColor(0.0, 26/255, 0.0, 1)
            
            isComplete = self.gameloop(stage);
            if isComplete: break
            
            glfw.swap_buffers(self.window)
    
    def gameloop(self, stage: Stage):
        if stage.win(): return True
        stage.display(self.modelLocation, self.colorLocation, self.edge)
        
sokoban = Sokoban(800, 800, "Sokoban_Refined")
sokoban.setShaderProgram("vShader.vs", "fShader.fs")
sokoban.initialSetup(20)
sokoban.start()
