from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram


from  DirectEnumerator import DirectEnumerator

class ShaderType(DirectEnumerator): 
    VERTEX = 0
    FRAGMENT = 1

class ShaderHandler:
    def __init__(self, vertexShaderSourceFilePath: str
                 , fragmentShaderSourceFilePath: str):
        # Use the shaders from those paths.
        self.setShaderProgram(vertexShaderSourceFilePath
                         , fragmentShaderSourceFilePath)
        
    def setShaderProgram(self, vertexShaderSourceFilePath: str
                         , fragmentShaderSourceFilePath: str):
        
        vertexShader = self.compileShaderFromFile(vertexShaderSourceFilePath
                                                  , ShaderType.VERTEX)
        fragmentShader = self.compileShaderFromFile(fragmentShaderSourceFilePath
                                                    , ShaderType.FRAGMENT)
        
        compiledProgram = compileProgram(vertexShader, fragmentShader)
        # Shader program compile complete, use it. 
        glUseProgram(compiledProgram)
        
        self.shaderProgram = compiledProgram   
        
    def compileShaderFromFile(self, shaderSourceFilePath: str
                                 , shaderTypeIndicator: ShaderType):
        shaderSource = self.readShaderSourceFromFile(shaderSourceFilePath)
        
        shaderType = -1
        if shaderTypeIndicator == ShaderType.VERTEX:
            shaderType = GL_VERTEX_SHADER
        elif shaderTypeIndicator == ShaderType.FRAGMENT:
            shaderType = GL_FRAGMENT_SHADER
        else:
            raiseError("")
        
        compiledShader = compileShader(shaderSource, shaderType)
        
        return compiledShader
        
    def readShaderSourceFromFile(self, shaderSourceFilePath: str):
        shaderSourceFile = open(shaderSourceFilePath, 'r')
        shaderSource = list()
        
        while True:
            if not (sourceLine := shaderSourceFile.readline()): break
            shaderSource.append(sourceLine)
        shaderSource = ''.join(shaderSource)
        
        return shaderSource
        
    def getProgram(self):
        return self.shaderProgram