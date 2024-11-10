from dataclasses import dataclass
from enum import Enum
from typing import List

class Directions(Enum):
    IDLE = 0
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8

@dataclass
class Cell:
    ways: int = 0
    fixed: bool = False

class Desk:

    desk: List[List[Cell|None]]

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.init_desk()

    def init_desk(self):
        self.desk = [[Cell() for y in range(self.height)] for x in range(self.width)]