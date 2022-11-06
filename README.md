# Dependencies!!!
Be advised that, setting up for OpenGL developing environment in Python is wholly taught from: https://www.youtube.com/watch?v=LqPPvPKUfV4

* **Python-binded glfw** https://github.com/FlorianRhiem/pyGLFW
* **Python-binded OpenGL** https://github.com/mcfletch/pyopengl
* **Pyrr** https://github.com/adamlwgriffiths/Pyrr
* **Numpy** 


## Sokoban_Old
Python의 OpenGL 라이브러리를 배우고 실제로 작동하는지 간단히 보기 위해 작성한 예제 게임입니다. 작동 가능성만 확인하기 위해 작성된 코드이므로 향후 수정은 고려하지 않아 코드가 매우 난잡한 상태입니다.
파일은 크게 두 가지의 클래스: Stage와 Sokoban으로 이루어져있습니다.

**Stage**는 소코반 게임 스테이지의 정보를 저장하고 유지하는 역할입니다. 
* 스테이지의 가로 및 세로 길이를 저장 및 유지합니다.
* 스테이지의 구성상태(맵)을 저장및 유지합니다.
* **readStageFile(self, path)** .txt파일에서 스테이지를 읽어옵니다. 또한 스테이지 구성상태를 저장합니다.
* **update(self, moveX, moveY)** 스테이지에 변형이 가해진 경우 (플레이어가 이동하거나, 이동하면서 박스를 민 경우) 구성상태에 이 사실을 갱신합니다.
* **tile(self, x, y)** 스테이지 구성상태(맵)을 읽어 (x, y) 위치에 있는 타일의 정보를 가져옵니다.
* **win(self)** 스테이지를 완수했는지 검사합니다. 
* **display((self, modelLocation, colorLocation, edge)** Shader에 블록이 윈도우 창에서 어디 위치해야 하는지, 무슨 색으로 표현되어야 하는지를 보냅니다. 그리고 그 정보를 사용해서 정사각형을 그립니다.

**Sokoban**은 소코반 게임 윈도우를 구성하기 위한 GLFW, OpenGL 초기설정을 하고 게임을 구성하는 설정중 일부를 수행합니다. (나머지는 **Stage**에서 수행합니다.)
* 소코반 게임 창의 가로 및 세로 길이를 저장 및 유지합니다. 
* 게임을 구동하는데 필요한 GLFW 함수를 호출하고 그 결과를 유지합니다.
* **setShader()**, **setShaderProgram()**은 OpenGL의 정점 섀이더와 프래그먼트 섀이더를 컴파일 한 후 로드 및 유지합니다. 
* **initialSetup()**은 게임 화면을 그리는데 필요한 OpenGL 요소를 만들고 유지합니다.
* **start()**, **gameloop()**은 게임이 지속실행되는 while loop을 구성합니다.

## Sokoban_Refined
작동 증명을 위해 단순하고 엉멍으로 설계되었던 Sokoban_Old를 개선하기 위해 작성중인 코드입니다. 목표는 다음과 같습니다.
1. 코드를 프로그램을 구성하는 역할 단위로 나누어 좀 더 보기 쉽게 개선합니다.
2. 로직과 설계를 분리하여 향후 추가될 Tile에 능동적으로 대처할 수 있는 코드를 작성할 수 있게 합니다.
3. OpenGL 코드와 실제 사용코드를 분리하여 깔끔한 코드를 작성할 수 있게 개선합니다. 
4. 잠재적으로, Cell을 사용하는 게임 방식을 구현하는데 쉽게 사용할 수 있는 코드를 작성합니다. 
