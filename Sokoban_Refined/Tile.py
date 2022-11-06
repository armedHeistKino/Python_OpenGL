from abc import abstractmethod

# 향후 다양한 타일들이 추가될 수 있단 말이지...
# 그래서 코드에 각 타일의 역할, 특징을 하드코딩 하기보다는
# 주상적인 타일 역할에 나중에 지정하는 방식이었으면 좋겠어

# 그리고 나중에는 색이 아니라 이미지를 불러올건데 
# 이런식으로 색갈로 하드코딩하면 나중에 다 고쳐야 해. 

# 타일끼리의 인터렉션은 어떡할까? 

# OpenGL에게 자신이 어떤 방식으로 그려져야 하는지 지시하는 함수 display()
# 

class Tile:
    def __init__(self, x: int, y: int):
        self.x = 0
        self.y = 0
        
        self.symbol = str()
        
    def set_symbol(self, symbol:str):
        if not len(symbol) == 1:
            raiseError("wrong symbol length. only 1 allowed.")
            
        self.symbol = symbol
        
    def move_by(self, dx:int, dy:int):
        """_summary_
            move the tile location by 'dx' in x axis, 'dy' in y axis.
        Args:
            dx (int): _description_
            dy (int): _description_
        """
        self.x += dx
        self.y += dy
    
    def mapIndex(self, mapWidth: int):
        """_summary_
            returns index in the list.
        """
        return y * mapWidth + x
        
    def displayPosition(self, edge: int, mapWidth: int):
        return [-1 + edge * self.x, 1 - edge * (self.y+1), 0]
        
    @abstractmethod
    def do_when_pushed_by(self, dx:int, dy:int):
        pass
        
    @abstractmethod
    def display(self, l1, l2):
        pass